import asyncio
from datetime import timedelta

import logbook
from fastapi import APIRouter

from ..logics.tasks import tasks, start, stop

logger = logbook.Logger(__name__)

scheduling_router = APIRouter()


@scheduling_router.get("/tasks")
async def get_tasks():
    return {task: {'running': bool(tasks[task].task), 'period': tasks[task].period} for task in tasks}


@scheduling_router.post("/resume")
async def resume(task: str):
    logger.debug('Resuming: {}', task)
    await start(task)
    return {"status": "started"}


@scheduling_router.post("/pause")
async def pause(task: str):
    logger.debug('Pausing: {}', task)
    await stop(task)
    return {"status": "pause"}
