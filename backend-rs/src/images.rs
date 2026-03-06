use std::{fs, path::{Path, PathBuf}};

use axum::{
    body::Bytes,
    extract::Path as PathExtractor,
    http::{HeaderMap, HeaderValue, StatusCode, header},
    response::IntoResponse,
};
use prost::Message;

use crate::{
    AdminToken, ImageDelete, ImageUpload, StateResponse, StorageInfo, ADMIN_HASH, IMAGE_STORE,
    log_and_respond, respond,
};

fn scan_storage_info() -> StorageInfo {
    let images_dir = Path::new(IMAGE_STORE.as_str());

    if !images_dir.exists() {
        return StorageInfo {
            size: 0,
            count: 0,
            files: vec![],
        };
    }

    let entries = match fs::read_dir(images_dir) {
        Ok(entries) => entries,
        Err(_) => {
            return StorageInfo {
                size: 0,
                count: 0,
                files: vec![],
            };
        }
    };

    let mut files = Vec::new();
    let mut total_size: u64 = 0;

    for entry in entries.flatten() {
        let path = entry.path();

        if path.is_file() {
            if let Some(filename) = path.file_name() {
                if let Some(name) = filename.to_str() {
                    files.push(name.to_string());

                    if let Ok(metadata) = fs::metadata(&path) {
                        total_size += metadata.len();
                    }
                }
            }
        }
    }

    StorageInfo {
        size: total_size,
        count: files.len() as u32,
        files,
    }
}

pub async fn get_storage_info(data: Bytes) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let admin_token = AdminToken::decode(data.as_ref())
        .map_err(|_| respond(StatusCode::BAD_REQUEST, "failed"))?;

    if admin_token.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }
    let storage_info = scan_storage_info();

    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/octet-stream"),
        )]),
        storage_info.encode_to_vec(),
    ))
}

pub async fn get_image(
    PathExtractor(image_hash_and_ext): PathExtractor<String>,
) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let mut image_path = PathBuf::from(IMAGE_STORE.as_str());
    image_path.push(&image_hash_and_ext);
    let data = fs::read(image_path)
        .map_err(|_| respond(StatusCode::INTERNAL_SERVER_ERROR, "Image not found."))?;
    let ext = image_hash_and_ext.split('.').last().unwrap();
    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_str(&format!("image/{}", ext)).unwrap(),
        )]),
        data,
    ))
}

pub async fn remove_image(data: Bytes) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let deleted_image = ImageDelete::decode(data.as_ref())
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;

    if deleted_image.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }

    let mut deleted_path = PathBuf::from(IMAGE_STORE.as_str());
    deleted_path.push(&deleted_image.filename);

    fs::remove_file(&deleted_path)
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;

    Ok((
        StatusCode::OK,
        StateResponse {
            message: "success".to_string(),
        }
        .encode_to_vec(),
    ))
}

pub async fn upload_image(data: Bytes) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let upload_image = ImageUpload::decode(data.as_ref())
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;

    if upload_image.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }

    let filename = upload_image.filename;
    let mut file_path = PathBuf::from(IMAGE_STORE.as_str());
    file_path.push(&filename);

    if !file_path.exists() {
        let image_data = upload_image.image;
        fs::write(file_path, image_data)
            .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;
    }

    Ok((
        StatusCode::OK,
        StateResponse { message: filename }.encode_to_vec(),
    ))
}
