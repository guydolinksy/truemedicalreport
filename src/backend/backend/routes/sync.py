import asyncio
import copy
from typing import Optional, Any, Set, List, Collection

from fastapi import APIRouter
from logbook import Logger
from starlette.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import PayloadTooBig, WebSocketException, InvalidURI, ProtocolError

from common.data_models.admission import Admission
from common.data_models.patient import Patient
from common.utilities.pubsub import create_subscriber
from .. import config

logger = Logger(__name__)

sync_router = APIRouter()

subscribe = create_subscriber(sync_router, config.redis_connection)


@subscribe(Patient.__name__)
async def patient_handler(data: dict):
    patient_oid = data["oid"]
    if not (new := data.get("new")):
        return

    admission = Admission(**new['admission'])
    keys = {
        f"/api/departments/",
        f"/api/patients/{patient_oid}",
        f"/api/patients/{patient_oid}/info",
        f"/api/departments/{admission.department_id}",
    }
    if admission.wing_id:
        keys.add(f"/api/departments/{admission.department_id}/wings/{admission.wing_id}")

    await notify(keys)


@subscribe(f"{Patient.__name__}.admission")
async def admission_handler(data: dict) -> None:
    keys = set()

    for k in ["new", "old"]:
        if not data.get(k):
            continue

        admission = Admission(**data[k])
        keys.update({
            f"/api/departments/{admission.department_id}",
            f"/api/departments/{admission.department_id}/wings/{admission.wing_id}",
            f"/api/departments/{admission.department_id}/wings/{admission.wing_id}/beds/{admission.bed}",
        })

    await notify(keys)


class WebsocketsManager:
    def __init__(self):
        self._sockets = set()
        self._lock = asyncio.Lock()

    async def add(self, ws: WebSocket) -> None:
        async with self._lock:
            logger.debug(f"Gained socket from {ws.client.host}:{ws.client.port}")
            self._sockets.add(ws)

    async def remove(self, ws: WebSocket) -> None:
        async with self._lock:
            logger.debug(f"Lost socket from {ws.client.host}:{ws.client.port}")
            self._sockets.remove(ws)

    def all(self) -> Set[WebSocket]:
        # Shallow copy, so the function calling us won't be affected by subsequent addition/removals of sockets.
        return copy.copy(self._sockets)


_ws_manager = WebsocketsManager()


async def _echo_ws(ws: WebSocket) -> None:
    while True:
        msg = await ws.receive_json()
        logger.debug(msg)
        await ws.send_json(msg)


@sync_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    await _ws_manager.add(websocket)

    try:
        await _echo_ws(websocket)
    except WebSocketDisconnect:
        await _ws_manager.remove(websocket)


async def _notify_single(ws: WebSocket, data: Any) -> Optional[WebSocket]:
    try:
        await ws.send_json(data)
    except (PayloadTooBig, ProtocolError, InvalidURI):
        logger.exception("Failed to send to WS")
    except (WebSocketException, RuntimeError):
        return None

    return ws


_waiting_keys = set()


async def notify(keys: Collection[str]) -> None:
    _waiting_keys.update(keys)
    asyncio.create_task(_consolidated_notify())


async def _consolidated_notify() -> None:
    if len(_waiting_keys) < config.websocket_burst_threshold:
        await asyncio.sleep(config.websocket_consolidation_window_seconds)

    _keys = list(_waiting_keys)
    _waiting_keys.clear()
    await _notify_now(_keys)


async def _notify_now(keys: List[str]) -> None:
    if not keys:
        return

    websockets = _ws_manager.all()

    if not websockets:
        logger.debug(f"No websockets to notify")
        return

    data = {
        "length": len(keys),
        "keys": keys,
    }

    tasks = [asyncio.create_task(_notify_single(ws, data)) for ws in websockets]
    live_sockets = set([ws for ws in await asyncio.gather(*tasks) if ws])

    for dead_socket in websockets.difference(live_sockets):
        await _ws_manager.remove(dead_socket)


@sync_router.post('/test_broadcast')
async def test_broadcast(keys: List[str]):
    await notify(keys)
    return {}


@sync_router.post('/test_broadcast_now')
async def test_broadcast_now(keys: List[str]):
    await _notify_now(keys)
    return {}
