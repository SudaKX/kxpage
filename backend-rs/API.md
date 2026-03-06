# kx-page-rs API 文档

本文档介绍 kx-page 服务提供的 HTTP 接口。除特别说明外，所有请求/响应均使用
`src/pb/events.rs` 中的 Protocol Buffers，并以 `application/octet-stream`
作为 `Content-Type`。

> **路径说明**
>
> 服务器会自动在所有接口前添加 `PUBLIC_PREFIX`（默认空字符串）。下方列出的路径均为
> 未加前缀的形式，例如当 `PUBLIC_PREFIX=/kx-api/v1` 时，请求应发送到 `/kx-api/v1/...`。

## 鉴权

除仅用于读取的两个 GET 接口外，其余均为管理员接口，需要在请求体 protobuf 的
`token` 字段中携带管理员令牌。令牌是 `ADMIN_PWD` 的 SHA-512 哈希值（服务器端计算），
口令明文不会通过网络传输。

## 环境变量

服务器在启动时通过 `.env` 加载下列配置：

| 变量名 | 默认值  | 说明  |
|-----------------|----------------------|---------------------------|
| `ADMIN_PWD`     | `kxpage-password`    | 管理口令，用于计算 `token` 哈希。|
| `IMAGE_STORE`   | `./assets/images`    | 图片存储目录。|
| `DATABASE_PATH` | `./data/database.db` | SQLite 数据库文件路径。 |
| `PUBLIC_PREFIX` | `"/api/v1"`          | 所有路由的公共前缀（例如 `/api/v1`）。 |
| `IP_ADDRESS`    | `127.0.0.1`          | 监听 IP。              |
| `PORT`          | `8000`               | 监听端口。              |

## 公共接口

### GET `/api/v1/events`

查询给定时间点（最多往前 6 个月）的事件。

- **查询参数**
  - `q`（可选）：Base64 URL Safe 编码的 `YYYY-MM-DD HH:MM:SS` 字符串；省略时使用当前时间。
- **返回**：`EventList`，`event_time` 字段会被格式化为 `YYYY/MM/DD`。
- **状态码**
  - `200 OK`：成功。
  - `500 Internal Server Error`：数据库访问失败。

### GET `/api/v1/images/{filename}`

下载已存储的图片。

- **路径参数**
  - `filename`：文件名（如 `<hash>.png`）。
- **返回**：图片字节，`Content-Type=image/<扩展名>`。
- **状态码**
  - `200 OK`：成功。
  - `500 Internal Server Error`：文件不存在或读取失败。

## 管理接口

以下接口均需 `token`。
已按照默认的 `PUBLIC_PREFIX=/api/` 填充为完整路径。

### POST `/api/v1/events`

批量创建事件。

- **请求体**：`EventPost`
  - `token`
  - `events`：`EventSpec` 数组。每项需包含 `event_uuid`、`event_title`、
    `event_description`、`event_href`（可为空字符串）、`event_time`（`YYYY/MM/DD` 格式）、
    `image_hash`（可为空字符串）。
- **返回**：`StateResponse`，`message=success`。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。

### PUT `/api/v1/events`

更新单条事件。

- **请求体**：`EventUpdate`
  - `token`
  - `event`：新的 `EventSpec`。
- **返回**：`StateResponse`。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。

### DELETE `/api/v1/events`

按 UUID 删除事件。

- **请求体**：`EventDelete`
  - `token`
  - `uuids`：UUID 字符串数组。
- **返回**：`StateResponse`。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。

### POST `/api/v1/images`

上传图片（若文件已存在则忽略）。
因为 Axum 的默认 `DefaultBodyLimit` 只有 2 MiB，所以无法上传过大的图片。

- **请求体**：`ImageUpload`
  - `token`
  - `filename`
  - `image`：图片字节。
- **返回**：`StateResponse`，`message` 为最终文件名。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。

### DELETE `/api/v1/images`

删除图片。

- **请求体**：`ImageDelete`
  - `token`
  - `filename`
- **返回**：`StateResponse`。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。

### POST `/api/v1/images/info`

查看图片目录统计信息。
后端管理器需要依托此接口初始化。

- **请求体**：`AdminToken`
  - `token`
- **返回**：`StorageInfo`，包含 `size`（字节）、`count`、`files` 列表。
- **状态码**：`200 OK` / `401 Unauthorized` / `400|500 错误`。
