
import os
from typing import Annotated

import aiofiles
from google.protobuf.message import Message
from fastapi import APIRouter, Response, Body

from app.pbf import Event_pb2
from app.v1 import parse_protobuf
from app.config import IMAGE_STORE, PUBLIC_PREFIX


image_router = APIRouter(
    prefix=f"{PUBLIC_PREFIX}/images",
    tags=["images"]
)


@image_router.get("")
async def image_get(h: str):
    try:
        async with aiofiles.open(os.path.join(IMAGE_STORE, h), "rb") as rd:
            img = await rd.read()
    except Exception as e:
        message: Message = Event_pb2.StateResponse()
        message.message = "Image not found."
        return Response(
            message.SerializeToString(), 404,
            media_type="application/octet-stream"
        )
    _, ext = h.split('.')
    return Response(
        content=img,
        status_code=200,
        media_type=f"image/{ext}"
    )

@image_router.delete("")
async def image_remove(data: Annotated[bytes, Body()]):
    valid, wrapped = parse_protobuf("ImageDelete", data, "token")
    if not valid: return wrapped
    target = os.path.join(IMAGE_STORE, wrapped.filename)
    response: Message = Event_pb2.StateResponse()
    try:
        os.remove(target)
    except Exception as e:
        response.message = str(e)
        return Response(
            response.SerializeToString(), 500,
            media_type="application/octet-stream"
        )
    response.message = "success"
    return Response(
        response.SerializeToString(), 200,
        media_type="application/octet-stream"
    )

@image_router.post("")
async def image_upload(data: Annotated[bytes, Body()]):
    valid, wrapped = parse_protobuf("ImageUpload", data, "token")
    if not valid: return wrapped
    given_file = wrapped.filename
    image_data = wrapped.image
    filepath = os.path.join(IMAGE_STORE, given_file)
    if not os.path.exists(filepath):
        async with aiofiles.open(filepath, "wb") as wt:
            await wt.write(image_data)
    message: Message = Event_pb2.StateResponse()
    message.message = given_file
    return Response(
        message.SerializeToString(), 200,
        media_type="application/octet-stream"
    )

@image_router.post("/info")
async def storage_info(data: Annotated[bytes, Body()]):
    valid, wrapped = parse_protobuf("AdminToken", data, "token")
    if not valid: return wrapped

    filenames = os.listdir(IMAGE_STORE)
    filecount = len(filenames)
    filepath = [os.path.join(IMAGE_STORE, file) for file in filenames]
    total_size = sum([os.path.getsize(file) for file in filepath])

    result: Message = Event_pb2.StorageInfo()
    result.size = total_size
    result.count = filecount
    for file in filenames:
        result.files.append(file)
    return Response(
        result.SerializeToString(),
        status_code=200,
        media_type="application/octet-stream"
    )
