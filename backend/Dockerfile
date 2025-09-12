# Dockerfile

# 1. 使用官方的 Python 基础镜像
# 使用 -slim 版本可以显著减小镜像体积
FROM python:3.12-slim

# 2. 设置工作目录
# 容器内的所有后续操作都将在此目录下进行
WORKDIR /api

# 3. 复制依赖文件并安装
# 这一步单独复制 requirements.txt 是为了利用 Docker 的层缓存。
# 只要 requirements.txt 没有变化，Docker 就会使用缓存的层，而不会重新安装依赖，从而加快构建速度。
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir -r /api/requirements.txt

# 4. 复制项目代码
# 将当前目录下的所有文件（除了 .dockerignore 中指定的）复制到容器的 /app 目录中
COPY . /api

# 5. 暴露端口
# 告诉 Docker 容器在运行时会监听 8000 端口
EXPOSE 8000

# 6. 定义启动命令
# 当容器启动时，执行此命令来运行 FastAPI 应用。
# --host 0.0.0.0 是必须的，它让应用可以从容器外部访问。
CMD ["python3", "main.py"]