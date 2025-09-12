
import aiomysql
import asyncio
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
db_pool: aiomysql.Pool = None
loop = None

def use_event_loop(_loop):
    global loop
    loop = _loop

async def connect_to_db() -> aiomysql.Pool:

    conn: aiomysql.Connection = await aiomysql.connect(
        host=MYSQL_HOST, user=mysql_user, password=mysql_pass,
        port=MYSQL_PORT, loop=loop, autocommit=False
    )
    cur: aiomysql.Cursor = await conn.cursor()
    await cur.execute("SHOW DATABASES")
    await conn.commit()

    databases = await cur.fetchall()
    database_exist = any(db[0] == "kxpage" for db in databases)
    print(database_exist)
    if not database_exist:
        await cur.execute("CREATE DATABASE IF NOT EXISTS kxpage;")
        await conn.commit()
    
    await cur.close()
    conn.close()

    pool: aiomysql.Pool = await aiomysql.create_pool(
        host=MYSQL_HOST, user=mysql_user, password=mysql_pass,
        port=MYSQL_PORT, loop=loop, autocommit=False, db="kxpage",
        pool_recycle=1800
    )

    async with pool.acquire() as conn:
        if not database_exist:
            cursor: aiomysql.Cursor = await conn.cursor()
            await cursor.execute("""CREATE TABLE events (
uuid VARCHAR(36) PRIMARY KEY,
ev_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
ev_title VARCHAR(255) NOT NULL,
ev_href TEXT DEFAULT NULL,
image_hash VARCHAR(70) DEFAULT NULL,
ev_desc TEXT DEFAULT NULL
);
""")    
            await conn.commit()
            await cursor.close()

    return pool

async def create_db_pool():
    global db_pool
    while True:
        try:
            db_pool = await connect_to_db()
            break
        except Exception as e:
            print(e)
            await asyncio.sleep(3)

async def close_db_pool():
    db_pool.terminate()
    await db_pool.wait_closed()
