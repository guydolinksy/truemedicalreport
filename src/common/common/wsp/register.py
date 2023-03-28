import asyncio
from datetime import timedelta

import logbook

from .routes import router
from .logics.tasks import start, tasks, ScheduledTask

logger = logbook.Logger(__name__)


def register(period: timedelta, start_immediately=False):
    def _decorator(func):
        tasks[func.__name__] = ScheduledTask(code=func, task=None, period=period)

        if start_immediately:
            @router.on_event('startup')
            async def run():
                await start(func.__name__)

        return func

    return _decorator
