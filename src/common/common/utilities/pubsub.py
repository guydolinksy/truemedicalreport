import asyncio
import json
from collections import defaultdict
from types import NoneType
from typing import Callable, Any, TypeVar, Union, List, Dict, Awaitable, Optional

from fastapi import APIRouter
from broadcaster import Broadcast
import logbook


logger = logbook.Logger(__name__)

T = TypeVar("T")
_JSON_TYPE = Union[NoneType, Dict, List, str, int, float]
_SUBSCRIBER_HANDLER_TYPE = Callable[[_JSON_TYPE], Awaitable[T]]

CHANNEL = "updates"



def create_publisher(
    router: APIRouter, broadcast_backing: str, channel: str = CHANNEL
) -> Callable[[str, Optional], Awaitable[NoneType]]:
    broadcaster = Broadcast(broadcast_backing)

    @router.on_event("startup")
    async def on_startup() -> None:
        await broadcaster.connect()

    @router.on_event("shutdown")
    async def on_shutdown() -> None:
        await broadcaster.disconnect()

    async def publish(key: str, value: Any = None) -> None:
        await broadcaster.publish(channel=channel, message=json.dumps((key, value)))

    return publish


def create_subscriber(
    router: APIRouter, broadcast_backing: str, channel: str = CHANNEL
) -> Callable[[str], Callable[[_SUBSCRIBER_HANDLER_TYPE], _SUBSCRIBER_HANDLER_TYPE]]:

    broadcaster = Broadcast(broadcast_backing)
    tasks = []

    handlers: Dict[str, List[Callable[[_JSON_TYPE], Awaitable[NoneType]]]] = defaultdict(list)

    async def listen():
        async with broadcaster.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                try:
                    key, value = json.loads(event.message)
                except ValueError:
                    logger.error(f"Invalid message: {event}")
                    continue

                await asyncio.gather(*[h(value) for h in handlers[key]])

    @router.on_event("startup")
    async def on_startup() -> None:
        await broadcaster.connect()
        tasks.append(asyncio.create_task(listen()))

    @router.on_event("shutdown")
    async def on_shutdown() -> None:
        for task in tasks:
            task.cancel()

        await broadcaster.disconnect()

    def subscribe(key: str) -> Callable[[_SUBSCRIBER_HANDLER_TYPE], _SUBSCRIBER_HANDLER_TYPE]:
        def decorator(f: _SUBSCRIBER_HANDLER_TYPE) -> _SUBSCRIBER_HANDLER_TYPE:
            async def handler(value: _JSON_TYPE) -> None:
                with logger.catch_exceptions():
                    await f(value)

            handlers[key].append(handler)
            return f

        return decorator

    return subscribe
