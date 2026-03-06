use axum::{
    body::Bytes,
    extract::{Query, State},
    http::{HeaderMap, HeaderValue, StatusCode, header},
    response::IntoResponse,
};
use base64::{Engine, engine::general_purpose::URL_SAFE};
use prost::Message;
use std::collections::HashMap;

use crate::{
    AppState, EventDelete, EventList, EventPost, EventSpec, EventUpdate, StateResponse, ADMIN_HASH,
    log_and_respond, respond,
};

pub async fn get_event(
    State(state): State<AppState>,
    Query(params): Query<HashMap<String, String>>,
) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let date = if let Some(q) = params.get("q") {
        match Engine::decode(&URL_SAFE, &q) {
            Ok(bytes) => match String::from_utf8(bytes) {
                Ok(s) => s,
                Err(_) => q.clone(),
            },
            Err(_) => q.clone(),
        }
    } else {
        chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string()
    };

    let conn = state.database.lock().await;

    let mut stmt = conn
        .prepare(
            "SELECT uuid, time, title, href, desc, image_hash
                FROM events
                WHERE time >= datetime(?1, '-6 months')
                AND time < ?1
                ORDER BY time DESC",
        )
        .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

    let events_iter = stmt
        .query_map([&date], |row| {
            Ok(EventSpec {
                event_uuid: row.get(0)?,
                event_title: row.get(2)?,
                event_time: row.get(1)?,
                event_href: row.get::<usize, Option<String>>(3)?.unwrap_or_default(),
                event_description: row.get::<usize, Option<String>>(4)?.unwrap_or_default(),
                image_hash: row.get::<usize, Option<String>>(5)?.unwrap_or_default(),
            })
        })
        .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

    let events: Vec<EventSpec> = events_iter
        .collect::<Result<Vec<EventSpec>, rusqlite::Error>>()
        .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

    let events = EventList {
        events: events
            .into_iter()
            .map(|mut event| {
                if let Ok(dt) =
                    chrono::NaiveDateTime::parse_from_str(&event.event_time, "%Y-%m-%d %H:%M:%S")
                {
                    event.event_time = dt.format("%Y/%m/%d").to_string();
                }
                event
            })
            .collect(),
    };

    let data = events.encode_to_vec();

    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/octet-stream"),
        )]),
        data,
    ))
}

pub async fn put_event(
    State(state): State<AppState>,
    data: Bytes,
) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let event_update = EventUpdate::decode(data.as_ref())
        .map_err(|_| respond(StatusCode::INTERNAL_SERVER_ERROR, "failed"))?;

    if event_update.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }

    if event_update.event.is_none() {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    };

    let event = event_update.event.unwrap();

    let mut changes: Vec<String> = vec![];

    changes.push(format!("title='{}'", event.event_title));
    changes.push(format!("time='{}'", event.event_time));

    if !event.event_href.is_empty() {
        changes.push(format!("href='{}'", event.event_href));
    }

    if !event.event_description.is_empty() {
        changes.push(format!("desc='{}'", event.event_description));
    }

    if !event.image_hash.is_empty() {
        changes.push(format!("image_hash='{}'", event.image_hash));
    }

    println!("{:?}", changes);

    let conn = state.database.lock().await;

    let sql = format!("UPDATE events SET {} WHERE uuid = ?1;", changes.join(", "));

    let mut stmt = conn
        .prepare(&sql)
        .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

    stmt.execute([&event.event_uuid])
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;

    let resp = StateResponse {
        message: "success".to_string(),
    };

    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/octet-stream"),
        )]),
        resp.encode_to_vec(),
    ))
}

pub async fn delete_event(
    State(state): State<AppState>,
    data: Bytes,
) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let event_delete = EventDelete::decode(data.as_ref())
        .map_err(|_| respond(StatusCode::INTERNAL_SERVER_ERROR, "failed"))?;

    if event_delete.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }

    let conn = state.database.lock().await;

    let delete_collection = event_delete.uuids.join(", ");

    let mut stmt = conn
        .prepare("DELETE FROM events WHERE uuid IN (?1);")
        .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

    stmt.execute((&delete_collection,))
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;

    let resp = StateResponse {
        message: "success".to_string(),
    };

    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/octet-stream"),
        )]),
        resp.encode_to_vec(),
    ))
}

pub async fn post_event(
    State(state): State<AppState>,
    data: Bytes,
) -> Result<impl IntoResponse, (StatusCode, Vec<u8>)> {
    let event_post = EventPost::decode(data.as_ref())
        .map_err(|_| respond(StatusCode::INTERNAL_SERVER_ERROR, "failed"))?;

    if event_post.token != *ADMIN_HASH {
        return Err(respond(StatusCode::UNAUTHORIZED, "failed"));
    }

    let conn = state.database.lock().await;

    for event in event_post.events {
        let date = chrono::NaiveDate::parse_from_str(&event.event_time, "%Y/%m/%d")
            .map_err(|_| respond(StatusCode::INTERNAL_SERVER_ERROR, "failed"))?;
        let datetime = date.and_hms_opt(0, 0, 0).unwrap();

        let href = if event.event_href.is_empty() {
            None
        } else {
            Some(event.event_href.as_str())
        };
        let image_hash = if event.image_hash.is_empty() {
            None
        } else {
            Some(event.image_hash.as_str())
        };

        let mut stmt = conn
            .prepare(
                "INSERT INTO events (uuid, time, title, href, image_hash, desc)
                    VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
            )
            .map_err(|e| log_and_respond(StatusCode::INTERNAL_SERVER_ERROR, "failed", e))?;

        stmt.execute((
            &event.event_uuid,
            &datetime.format("%Y-%m-%d %H:%M:%S").to_string(),
            &event.event_title,
            href.as_ref(),
            image_hash.as_ref(),
            &event.event_description,
        ))
        .map_err(|e| log_and_respond(StatusCode::BAD_REQUEST, "failed", e))?;
    }

    let resp = StateResponse {
        message: "success".to_string(),
    };

    Ok((
        HeaderMap::from_iter([(
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/octet-stream"),
        )]),
        resp.encode_to_vec(),
    ))
}
