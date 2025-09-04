
import time
import pymysql
from google.protobuf.message import Message
from fastapi import Response
from app.pbf import Event_pb2
from app.config import ADMIN_HASH

def parse_protobuf(
    msg_type: str, data: bytes, validation: str | None = None
) -> tuple[bool, Response | Message]:
    message = getattr(Event_pb2, msg_type)
    wrapped: Message = message()
    try:
        wrapped.ParseFromString(data)
    except Exception:
        response: Message = Event_pb2.StateResponse()
        response.message = "failed"
        return False, Response(
            response.SerializeToString(), 400,
            media_type="application/octet-stream"
        )
    if validation:
        given_hash = getattr(wrapped, validation)
        if given_hash != ADMIN_HASH:
            response: Message = Event_pb2.StateResponse()
            response.message = "failed"
            return False, Response(
                response.SerializeToString(), 401,
                media_type="application/octet-stream"
            )
    return True, wrapped

from app.config import MYSQL_HOST, MYSQL_AUTH, MYSQL_PORT

mysql_user, mysql_pass = MYSQL_AUTH.split(':')

db = None

def connect_to_db() -> None:
    global db

    conn = pymysql.connect(
        host=MYSQL_HOST, user=mysql_user, password=mysql_pass,
        port=MYSQL_PORT
    )

    # 创建游标
    cursor = conn.cursor()

    # 执行查询
    cursor.execute("SHOW DATABASES")
    conn.commit()
    databases = cursor.fetchall()

    # 判断数据库是否存在
    database_exist = any(db[0] == "kxpage" for db in databases)

    if not database_exist:
        cursor.execute("CREATE DATABASE IF NOT EXISTS kxpage")
        conn.commit()

    # 关闭游标和连接
    cursor.close()
    conn.close()

    db = pymysql.connect(
        host=MYSQL_HOST, user=mysql_user, password=mysql_pass,
        port=MYSQL_PORT, database="kxpage"
    )

    if not database_exist:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE events (
uuid VARCHAR(36) PRIMARY KEY,
ev_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ev_title VARCHAR(255) NOT NULL,
ev_href TEXT DEFAULT NULL,
image_hash VARCHAR(70) DEFAULT NULL,
ev_desc TEXT DEFAULT NULL
);
""")    
        db.commit()
        cursor.close()

while True:
    try:
        connect_to_db()
        break
    except Exception as e:
        print(e)
        time.sleep(3)
