import asyncio
import logging
from dataclasses import dataclass, field
from typing import Callable, Coroutine

import websockets

from tmr.routes.websocket import notify

logger = logging.getLogger(__name__)


@dataclass
class WebSocketSubscriber:
    websocket_url: str

    def subscribe(self, key: str):
        def decorator(func: Callable[[str], Coroutine]):
            async def wrapper():
                async with websockets.connect(f"{self.websocket_url}?key={key}") as ws:
                    async for message in ws:
                        await func(message)
            return wrapper
        return decorator


subscriber = WebSocketSubscriber(websocket_url="ws://medical_dal/ws")


@subscriber.subscribe(key="patient")
async def patient_handler(message):
    notify(f"/patient/id/{message}")
