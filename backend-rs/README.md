# README

使用 Rust Axum 重写的后端，补全了 [API 文档](API.md)。

## 部署

1. 克隆仓库
2. 根据 `.env.example` 文件创建 `.env` 文件，更改配置信息
3. `cargo build -r`
4. 把编译出的可执行文件与以下文件放在一起：
  
    ```text
    后端根文件夹
    ├── data（文件夹）
    ├── asstes
    │   └── images（文件夹）
    └── kx-page-rs.exe
    ```

    `data` 文件夹下会自动创建数据库文件
5. 运行
