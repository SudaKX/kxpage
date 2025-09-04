
import os
import requests
import hashlib
from base64 import urlsafe_b64encode
from typing import TypedDict, Optional
from google.protobuf.message import Message
from uuid import uuid4 as random_uuid, UUID
from datetime import datetime
from .pbf import Event_pb2

class StorageInfo(TypedDict):
    size: int
    count: int
    files: list[str]

class EventSpec(TypedDict, total=False):
    uuid: str
    title: str
    description: str
    href: str
    time: str
    image: str

class StateResponse(TypedDict):
    message: str

PBF_HEADER = {
    'X-Requested-With': 'XMLHttpRequest',
    "Content-Type": "application/octet-stream"
}

class KXPageClient:
    
    _host_url: str
    _admin_hash: str

    def __init__(
        self, url: str = "http://localhost:8000/api/v1",
        password: str = "kxpage_password"
    ):
        self._host_url = url.removesuffix("/")
        h = hashlib.sha512()
        h.update(password.encode("utf-8"))
        self._admin_hash = h.hexdigest()
    
    # Images

    def upload_image(self, path: str) -> StateResponse:
        with open(path, "rb") as rd:
            image_data = rd.read()
        h = hashlib.sha256()
        h.update(image_data)
        image_hash = h.hexdigest()
        _, filename = os.path.split(os.path.normpath(path))
        _, ext_name = os.path.splitext(filename)
        hashed_filename = image_hash + ext_name

        payload: Message = Event_pb2.ImageUpload()
        payload.token = self._admin_hash
        payload.filename = hashed_filename
        payload.image = image_data

        response = requests.post(
            f"{self._host_url}/images", payload.SerializeToString(),
            headers=PBF_HEADER
        )
        if response.status_code == 200:
            message: Message = Event_pb2.StateResponse()
            message.ParseFromString(response.content)
            return {"message": message.message}
        else:
            return {"message": "failed"}
    
    def fetch_image(self, image_hash: str) -> bytes:
        response = requests.get(
            f"{self._host_url}/images?h={image_hash}",
            headers={ 'X-Requested-With': 'XMLHttpRequest' }
        )
        if response.status_code == 200:
            return response.content
        return bytes()

    def delete_image(self, image_hash: str) -> StateResponse:
        body: Message = Event_pb2.ImageDelete()
        body.token = self._admin_hash
        body.filename = image_hash
        response = requests.delete(
            f"{self._host_url}/images",
            data=body.SerializeToString(),
            headers=PBF_HEADER
        )
        wrapped: Message = Event_pb2.StateResponse()
        wrapped.ParseFromString(response.content)
        return { "message": wrapped.message }

    # Events

    def fetch_event(self, time_before: str | None = None) -> list[EventSpec]:
        if time_before:
            given_time = datetime.strptime(time_before, "%Y/%m/%d")
            time_bytes = given_time.strftime("%Y-%m-%d %H:%M:%S").encode("utf-8")
            query = urlsafe_b64encode(time_bytes).decode("utf-8")
            url = f"/events?q={query}"
        else:
            url = "/events"
        url = url.rstrip("=")
        response = requests.get(self._host_url + url, headers=PBF_HEADER)
        if response.status_code == 200:
            results: list[EventSpec] = []
            events: Message = Event_pb2.EventList()
            events.ParseFromString(response.content)
            for item in events.events:
                results.append({
                    "uuid": item.eventUUID,
                    "title": item.eventTitle,
                    "description": item.eventDescription,
                    "href": item.eventHref,
                    "time": item.eventTime,
                    "image": item.imageHash
                })
            return results
        else:
            return []

    def update_event(
        self,
        uuid: UUID | str,
        *,
        event_time: Optional[datetime] = None,
        event_title: Optional[str] = None,
        event_href: Optional[str] = None,
        event_description: Optional[str] = None,
        image_hash: Optional[str] = None
    ) -> StateResponse:
        pack: Message = Event_pb2.EventUpdate()
        pack.token = self._admin_hash
        pack.event.eventUUID = uuid
        if event_time: pack.event.eventTime = event_time.strftime("%Y-%m-%d %H:%M:%S")
        if event_title: pack.event.eventTitle = event_title
        if event_href: pack.event.eventHref = event_href
        if event_description: pack.event.eventDescription = event_description
        if image_hash: pack.event.imageHash = image_hash

        response = requests.put(
            f"{self._host_url}/events", pack.SerializeToString(),
            headers=PBF_HEADER
        )

        if response.status_code == 200:
            message: Message = Event_pb2.StateResponse()
            message.ParseFromString(response.content)
            return {"message": message.message}
        else:
            return {"message": "failed"}

    def append_event(self, events: list[EventSpec]) -> StateResponse:
        now_str = datetime.now().strftime("%Y/%m/%d")

        for event in events:
            event["uuid"] = str(random_uuid())
            event.setdefault("time", now_str)
            event.setdefault("description", "没有介绍哦~ T^T")
        
        pack: Message = Event_pb2.EventPost()
        pack.token = self._admin_hash
        for event in events:
            ev = pack.events.add()
            ev.eventUUID = event["uuid"]
            ev.eventTitle = event["title"]
            ev.eventTime = event["time"]
            ev.eventDescription = event["description"]
            if (ref := event.get("href", None)): ev.eventHref = ref
            if (img := event.get("image", None)): ev.imageHash = img
        response = requests.post(
            f"{self._host_url}/events",
            pack.SerializeToString(), headers=PBF_HEADER
        )
        if response.status_code == 200:
            message: Message = Event_pb2.StateResponse()
            message.ParseFromString(response.content)
            return {"message": message.message}
        else:
            return {"message": "failed"}

    def delete_event(self, *uuids: UUID | str) -> StateResponse:
        uuids = [str(uuid) for uuid in uuids]
        pack: Message = Event_pb2.EventDelete()
        pack.token = self._admin_hash
        for uuid in uuids:
            pack.uuids.append(uuid)
        response = requests.delete(
            f"{self._host_url}/events",
            data=pack.SerializeToString(),
            headers=PBF_HEADER
        )
        if response.status_code == 200:
            message: Message = Event_pb2.StateResponse()
            message.ParseFromString(response.content)
            return {"message": message.message}
        else:
            return { "message": "failed" }

    # Chores

    def get_storage_info(self) -> StorageInfo:
        payload: Message = Event_pb2.AdminToken()
        payload.token = self._admin_hash
        response = requests.post(
            f"{self._host_url}/images/info",
            payload.SerializeToString(),
            headers=PBF_HEADER
        )
        if response.status_code == 200:
            result: Message = Event_pb2.StorageInfo()
            result.ParseFromString(response.content)
            return {
                "size": result.size,
                "count": result.count,
                "files": list(result.files)
            }
        else:
            return {
                "size": -1,
                "count": 0,
                "files": []
            } 
