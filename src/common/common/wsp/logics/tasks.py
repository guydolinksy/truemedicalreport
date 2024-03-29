import asyncio
from asyncio import Task
from datetime import timedelta
from typing import Callable, Dict

import logbook
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool


class ScheduledTask(BaseModel):
    code: Callable
    task: Task | None
    period: timedelta

    class Config:
        arbitrary_types_allowed = True


tasks: Dict[str, ScheduledTask] = {}

logger = logbook.Logger(__name__)


async def start(function_name: str):
    if tasks[function_name].task:
        raise ValueError(f'Task {function_name} is already running!')

    async def runner():
        while True:
            logger.debug('Starting Scheduled Task: {}', function_name)
            if asyncio.iscoroutinefunction(tasks[function_name].code):
                await tasks[function_name].code()
            else:
                await run_in_threadpool(tasks[function_name].code)
            logger.debug('Finished Scheduled Task: {}', function_name)
            await asyncio.sleep(tasks[function_name].period.total_seconds())

    tasks[function_name].task = asyncio.create_task(runner())


async def stop(function_name: str):
    if not tasks[function_name].task:
        raise ValueError(f'Task {function_name} is already stopped!')

    logger.debug('res {}', tasks[function_name].task.cancel())
    tasks[function_name].task = None
