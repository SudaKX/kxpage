fn main() {
    std::fs::create_dir_all("src/pb").expect("Failed to create output directory");

    prost_build::Config::new()
        .out_dir("src/pb") // 设置proto输出目录
        .compile_protos(&["assets/event.proto"], &["."]) // 要处理的proto文件
        .expect("Failed to compile proto files");
}
