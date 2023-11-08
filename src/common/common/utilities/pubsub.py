import asyncio
import json
from asyncio import Task
from collections import defaultdict
try:
    from types import NoneType
except ImportError:
    NoneType = type(None)
from typing import Callable, Any, TypeVar, Union, List, Dict, Awaitable, Optional

import logbook
from broadcaster import Broadcast
from fastapi import APIRouter

logger = logbook.Logger(__name__)

T = TypeVar("T")

_JSON_TYPE = Union[NoneType, Dict, List, str, int, float]
_SUBSCRIBER_HANDLER_TYPE = Callable[[_JSON_TYPE], Awaitable[T]]
_SUBSCRIBER_DECORATOR_TYPE = Callable[[_SUBSCRIBER_HANDLER_TYPE], _SUBSCRIBER_HANDLER_TYPE]
CHANNEL = "updates"


def _register_broadcaster(router: APIRouter, broadcast_backing: str) -> Broadcast:
    broadcaster = Broadcast(broadcast_backing)

    @router.on_event("startup")
    async def on_startup() -> None:
        await broadcaster.connect()

    @router.on_event("shutdown")
    async def on_shutdown() -> None:
        await broadcaster.disconnect()

    return broadcaster


def create_publisher(router: APIRouter, broadcast_backing: str) -> Callable[[str, Optional], Awaitable[NoneType]]:
    broadcaster = _register_broadcaster(router, broadcast_backing)

    async def publish(key: str, value: Any = None) -> None:
        await broadcaster.publish(channel=CHANNEL, message=json.dumps((key, value)))

    return publish


def create_subscriber(router: APIRouter, broadcast_backing: str) -> Callable[[str], _SUBSCRIBER_DECORATOR_TYPE]:
    broadcaster = _register_broadcaster(router, broadcast_backing)

    listener_task: Optional[Task] = None
    handlers: Dict[str, List[Callable[[_JSON_TYPE], Awaitable[NoneType]]]] = defaultdict(list)

    async def listen() -> None:
        async with broadcaster.subscribe(channel=CHANNEL) as subscriber:
            async for event in subscriber:
                try:
                    key, value = json.loads(event.message)
                except ValueError:
                    logger.error(f"Invalid message: {event}")
                    continue

                await asyncio.gather(*[h(value) for h in handlers[key]])

    @router.on_event("startup")
    async def on_startup() -> None:
        nonlocal listener_task
        listener_task = asyncio.create_task(listen())

    @router.on_event("shutdown")
    async def on_shutdown() -> None:
        nonlocal listener_task
        if listener_task:
            listener_task.cancel()
            listener_task = None

    def subscribe(key: str) -> _SUBSCRIBER_DECORATOR_TYPE:
        def decorator(f: _SUBSCRIBER_HANDLER_TYPE) -> _SUBSCRIBER_HANDLER_TYPE:
            async def handler(value: _JSON_TYPE) -> None:
                with logger.catch_exceptions():
                    await f(value)

            handlers[key].append(handler)
            return f

        return decorator

    return subscribe
