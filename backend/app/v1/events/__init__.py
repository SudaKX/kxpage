
import atexit
import asyncio
from base64 import b64decode
from datetime import datetime
from google.protobuf.message import Message
from typing import Annotated
from fastapi import APIRouter, Response, Body
from app.config import PUBLIC_PREFIX
from app.v1 import parse_protobuf
from app.pbf import Event_pb2
from .. import db

event_router = APIRouter(
    prefix=f"{PUBLIC_PREFIX}/events",
    tags=["events"]
)

@event_router.get("")
async def get_events(q: str = ""):

    def parse_query(q: str) -> str:
        q += "=" * (len(q) - len(q) // 4)
        bs = b64decode(q, altchars=b"-_")
        return bs.decode("utf-8")

    target = (
        parse_query(q)
        if q else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    def execute():
        cursor = db.cursor()
        cursor.execute(
f"""SELECT uuid, ev_time, ev_title, ev_href, ev_desc, image_hash
FROM events
WHERE ev_time >= DATE_SUB('{target}', INTERVAL 6 MONTH)
  AND ev_time < '{target}'
ORDER BY ev_time DESC;
""")
        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    result = await asyncio.to_thread(execute)

    ev_list: Message = Event_pb2.EventList()
    for record in result:
        uuid, dtime, title, href, desc, img_hash = record
        event = ev_list.events.add()
        event.eventUUID = uuid
        event.eventTitle = title
        event.eventDescription = desc
        if href: event.eventHref = href
        event.eventTime = dtime.strftime("%Y/%m/%d")
        if img_hash: event.imageHash = img_hash

    data = ev_list.SerializeToString()

    return Response(
        content=data,
        status_code=200,
        media_type="application/octet-stream"
    )

@event_router.post("")
async def post_events(data: Annotated[bytes, Body()]):
    valid, wrapped = parse_protobuf("EventPost", data, "token")
    if not valid: return wrapped

    def executor():
        cursor = db.cursor()
        for event in wrapped.events:
            uuid = event.eventUUID
            title = event.eventTitle
            desc = event.eventDescription
            href = f"'{event.eventHref}'" if event.eventHref else "NULL"
            time = datetime.strptime(event.eventTime, "%Y/%m/%d").strftime("%Y-%m-%d %H:%M:%S")
            img_hash = f"'{event.imageHash}'" if event.imageHash else "NULL"

            query = \
    f"INSERT INTO events VALUES ('{uuid}', '{time}', '{title}', {href}, {img_hash}, '{desc}');"
            cursor.execute(query)
        db.commit()
        cursor.close()

    await asyncio.to_thread(executor)
    message: Message = Event_pb2.StateResponse()
    message.message = "success"
    return Response(
        message.SerializeToString(), 200, media_type="application/octet-stream"
    )

@event_router.put("")
async def put_event(data: Annotated[bytes, Body()]):
    valid, message = parse_protobuf("EventUpdate", data, "token")
    if not valid: return message
    changes = []
    uuid = message.event.eventUUID
    if m := message.event.eventTitle: changes.append(f"ev_title='{m}'")
    if m := message.event.eventTime: changes.append(f"ev_time='{m}'")
    m = message.event.eventHref or ''
    changes.append(f"ev_href='{m}'")
    m = message.event.eventDescription or ''
    changes.append(f"ev_desc='{m}'")
    m = message.event.imageHash or ''
    changes.append(f"image_hash='{m or ''}'")
    set_clause = "SET " + ','.join(changes)
    
    def executor() -> None:
        query = \
f"""UPDATE events {set_clause} WHERE `uuid`='{uuid}';"""
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

    await asyncio.to_thread(executor)
    response: Message = Event_pb2.StateResponse()
    response.message = "success"
    return Response(
        response.SerializeToString(), 200, media_type="application/octet-stream"
    )

@event_router.delete("")
async def delete_events(data: Annotated[bytes, Body()]):
    valid, wrapped = parse_protobuf("EventDelete", data, "token")
    if not valid: return wrapped

    collection = '(' + ",".join([f"'{uuid}'" for uuid in wrapped.uuids]) + ')'

    def executor() -> None:
        cursor = db.cursor()
        query = f"DELETE FROM events WHERE uuid IN {collection};"
        cursor.execute(query)
        db.commit()
        cursor.close()

    await asyncio.to_thread(executor)
    message: Message = Event_pb2.StateResponse()
    message.message = "success"
    return Response(
        message.SerializeToString(), 200, media_type="application/octet-stream"
    )


def _end_of_life() -> None:
    db.close()

atexit.register(_end_of_life)
