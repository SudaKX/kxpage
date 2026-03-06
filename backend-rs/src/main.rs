include!("pb/events.rs");

mod events;
mod images;

use axum::{
    Router,
    http::StatusCode,
    routing::{get, post},
};
use dotenv::dotenv;
use events::{delete_event, get_event, post_event, put_event};
use images::{get_image, get_storage_info, remove_image, upload_image};
use lazy_static::lazy_static;
use prost::Message;
use rusqlite::Connection;
use std::sync::Arc;
use std::{env, error::Error};
use tokio::sync::Mutex;

lazy_static! {
    pub(crate) static ref ADMIN_HASH: String = {
        use sha2::{Digest, Sha512};
        let admin_pwd = env::var("ADMIN_PWD").unwrap_or_else(|_| "kxpage-password".to_string());
        let mut hasher = Sha512::new();
        hasher.update(admin_pwd.as_bytes());
        format!("{:x}", hasher.finalize())
    };
    pub(crate) static ref IMAGE_STORE: String =
        env::var("IMAGE_STORE").unwrap_or_else(|_| "./assets/images".to_string());
    static ref DATABASE_PATH: String =
        env::var("DATABASE_PATH").unwrap_or_else(|_| "./data/database.db".to_string());
    static ref ADDR: std::net::SocketAddr = {
        let ip: std::net::IpAddr = env::var("IP_ADDRESS")
            .unwrap_or_else(|_| "127.0.0.1".to_string())
            .parse()
            .unwrap_or(std::net::IpAddr::V4(std::net::Ipv4Addr::LOCALHOST));
        let port: u16 = env::var("PORT")
            .unwrap_or_else(|_| "8000".to_string())
            .parse()
            .unwrap_or(3000);
        std::net::SocketAddr::from((ip, port))
    };
    static ref PUBLIC_PREFIX: String =
        env::var("PUBLIC_PREFIX").unwrap_or_else(|_| "/api/v1".to_string());
}

#[derive(Clone)]
pub(crate) struct AppState {
    pub(crate) database: Arc<Mutex<Connection>>,
}

fn connect_to_database() -> Result<Connection, Box<dyn Error>> {
    let conn = Connection::open(DATABASE_PATH.as_str())?;

    conn.execute(
        "CREATE TABLE IF NOT EXISTS events (
        uuid VARCHAR(36) PRIMARY KEY,
        time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        title VARCHAR(255) NOT NULL,
        href TEXT DEFAULT NULL,
        image_hash VARCHAR(70) DEFAULT NULL,
        desc TEXT DEFAULT NULL
        )",
        (),
    )?;

    Ok(conn)
}

pub(crate) fn respond(status: StatusCode, message: impl Into<String>) -> (StatusCode, Vec<u8>) {
    let resp = StateResponse {
        message: message.into(),
    };
    (status, resp.encode_to_vec())
}

pub(crate) fn log_and_respond<E>(
    status: StatusCode,
    message: impl Into<String>,
    err: E,
) -> (StatusCode, Vec<u8>)
where
    E: std::fmt::Display,
{
    eprintln!("{}", err);
    respond(status, message)
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    dotenv().ok();

    let conn = Arc::new(Mutex::new(connect_to_database()?));

    let state = AppState { database: conn };

    let app = Router::new()
        .route(
            &(PUBLIC_PREFIX.clone() + "/images/info"),
            post(get_storage_info),
        )
        .route(&(PUBLIC_PREFIX.clone() + "/events"), get(get_event))
        .route(
            &(PUBLIC_PREFIX.clone() + "/events"),
            post(post_event).put(put_event).delete(delete_event),
        )
        .route(
            &(PUBLIC_PREFIX.clone() + "/images"),
            get(get_image).post(upload_image).delete(remove_image),
        )
        // .layer(axum::extract::DefaultBodyLimit::max(10 * 1024 * 1024)) // 10MB
        .with_state(state);

    let listener = tokio::net::TcpListener::bind(*ADDR).await.unwrap();
    axum::serve(listener, app).await.unwrap();

    Ok(())
}
