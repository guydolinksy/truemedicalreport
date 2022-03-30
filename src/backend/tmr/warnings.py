import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Coroutine

import websockets

from tmr.routes.websocket import notify

logger = logging.getLogger(__name__)


@dataclass
class WebSocketSubscriber:
    # **Note** that this implementation does not currently support multiple subscriptions for the same key!

    websocket_url: str
    tasks: dict[str, asyncio.Task] = field(default_factory=dict)

    def subscribe(self, key: str):
        def wrapper(callback: Callable[[str], Coroutine]):
            self.tasks.setdefault(
                key,
                asyncio.create_task(
                    _connect_to_websocket_and_wait_for_updates(key, callback, self.websocket_url)
                )
            )
        return wrapper

    def unsubscribe(self, key: str):
        if key not in self.tasks:
            return
        self.tasks.pop(key).cancel()


async def _connect_to_websocket_and_wait_for_updates(
        key: str,
        callback: Callable[[str], Coroutine],
        websocket_url: str):
    async for ws in websockets.connect(f"{websocket_url}?key={key}"):
        try:
            await _wait_for_updates(ws, key, callback)

        except websockets.ConnectionClosedOK:
            logger.debug("Connection to web-socket closed properly. Disconnecting.")
            break

        except websockets.ConnectionClosedError:
            logger.warning("Connection to web-socket closed abruptly. Reconnecting")
            continue


async def _wait_for_updates(websocket, key, callback):
    await websocket.send()
    while True:
        message = await websocket.recv()
        try:
            await callback(message)
        except Exception:
            logger.exception(f"Error calling callback for {key}")


subscriber = WebSocketSubscriber(websocket_url="ws://medical_dal/ws")


@subscriber.subscribe(key="patient")
def patient_handler(message):
    notify(f"/patient/id/{message}")

