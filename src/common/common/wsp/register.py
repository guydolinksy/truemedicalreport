from datetime import timedelta

import logbook

from .logics.tasks import start, tasks, ScheduledTask
from .routes import router

logger = logbook.Logger(__name__)


def register(period: timedelta, start_immediately=True):
    def _decorator(func):
        tasks[func.__name__] = ScheduledTask(code=func, task=None, period=period)

        if start_immediately:
            @router.on_event('startup')
            async def run():
                await start(func.__name__)

        return func

    return _decorator
