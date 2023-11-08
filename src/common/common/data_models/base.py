import contextlib
import inspect
import re
from builtins import NotImplemented
from enum import Enum
from typing import Callable, Awaitable, Any, List, Optional, Tuple, ClassVar, Iterator, Dict, Type, TypeVar

import logbook
from bson import ObjectId
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from common.utilities.exceptions import MaxRetriesExceeded

logger = logbook.Logger(__name__)
connection = None


class Mode(int, Enum):
    mask_any = 0b00
    mask_old = 0b10
    mask_new = 0b01
    mask_all = 0b11

    created = 0b01
    updated = 0b11
    deleted = 0b10


class Run(object):
    def __init__(self, watcher, old, new):
        self.diff = set()
        self.watcher: Watcher = watcher
        self.old = old
        self.new = new

    def __aiter__(self):
        return self

    async def __anext__(self):
        for path, old_value, new_value in Diffable.diff(self.old, self.new):
            async for callback in self.watcher.match_handlers(
                    self.watcher.callbacks, path=path, old_value=old_value, new_value=new_value
            ):
                key = (path, _hash(old_value), _hash(new_value), callback)
                if key not in self.diff:
                    self.diff.add(key)
                    args = inspect.getfullargspec(callback)[0]
                    return callback(**{k: v for k, v in dict(
                        path=path,
                        old=self.old,
                        new=self.new,
                        old_value=old_value,
                        new_value=new_value
                    ).items() if k in args})
        else:
            raise StopAsyncIteration()


class Watcher(object):
    notifiers: List[
        Tuple[Tuple[str], bool, Mode, Mode, Callable[[List[str], 'AtomicUpdate', 'AtomicUpdate'], Any]]] = []
    callbacks: List[
        Tuple[Tuple[str], bool, Mode, Mode, Callable[[List[str], 'AtomicUpdate', 'AtomicUpdate'], Any]]] = []

    def callback(self, *path: str, exact=True, mask: Mode = Mode.mask_any,
                 mode: Mode = Mode.mask_old | Mode.mask_new):
        def callback_(func: Callable[[List[str], 'AtomicUpdate', 'AtomicUpdate'], Any]):
            self.callbacks.append((path, exact, mask, mode, func))
            return func

        return callback_

    def notify(self, *path: str, exact=True, mask: Mode = Mode.mask_any,
               mode: Mode = Mode.mask_old | Mode.mask_new):
        def notify_(func: Callable[[List[str], 'AtomicUpdate', 'AtomicUpdate'], Any]):
            self.notifiers.append((path, exact, mask, mode, func))
            return func

        return notify_

    @staticmethod
    async def match_handlers(handlers, path, old_value, new_value):
        for matchers, exact, mask, mode, watcher in handlers:
            if len(path) < len(matchers) or (len(path) > len(matchers) and exact):
                continue
            for matcher, part in zip(matchers, path):
                if not re.fullmatch(matcher, part):
                    break
            else:
                if mode & mask & Mode.mask_new and not new_value:
                    continue
                elif mode & mask & Mode.mask_old and not old_value:
                    continue
                else:
                    yield watcher

    async def run_recursive_diff(self, old, new):
        async for result in Run(self, old, new):
            await result

    async def run_notify(self, oid, old, new):
        for path, old_value, new_value in Diffable.diff(old, new):
            async for callback in self.match_handlers(
                    self.notifiers, path=path, old_value=old_value, new_value=new_value
            ):
                await callback(**{k: v for k, v in dict(
                    oid=str(oid), path=path, old=old, new=new, old_value=old_value, new_value=new_value
                ).items() if k in inspect.getfullargspec(callback)[0]})


class Diffable(BaseModel):
    @staticmethod
    def diff(old: Any, new: Any):
        yield from _diff((), old, new)

    def __hash__(self):
        return hash(((key, _hash(getattr(self, key))) for key in sorted(self.model_fields)))


def _hash(obj):
    if isinstance(obj, dict):
        return hash(((k, hash(obj[k])) for k in sorted(obj)))
    elif isinstance(obj, list):
        return hash(tuple(obj))
    else:
        return hash(obj)


def _diff(path: Tuple[str], old: Any, new: Any) -> Iterator[Tuple[Tuple[str], Any, Any]]:
    if old is None:
        if new is None:
            return
        else:
            yield from _flip(_diff(path, new, old))
    else:
        if isinstance(old, Diffable):
            yield from _diff_first(path, old, new, _diff_diffable)
        elif isinstance(old, dict):
            yield from _diff_first(path, old, new, _diff_dict)
        elif old != new:
            yield path, old, new


def _flip(iterator: Iterator[Tuple[Tuple[str], Any, Any]]) -> Iterator[Tuple[List[str], Any, Any]]:
    for path, old_value, new_value in iterator:
        yield path, new_value, old_value


def _diff_diffable(path: Tuple[str], old: 'Diffable', new: Optional['Diffable']) \
        -> Iterator[Tuple[Tuple[str], Any, Any]]:
    # logger.debug('{} {}', old, new)
    if not new:
        new = Diffable()
    for member in set(old.model_fields) - set(new.model_fields):
        yield from _diff(path + (member,), getattr(old, member), None)
    for member in set(old.model_fields) & set(new.model_fields):
        yield from _diff(path + (member,), getattr(old, member), getattr(new, member))
    for member in set(new.model_fields) - set(old.model_fields):
        yield from _diff(path + (member,), None, getattr(new, member))


def _diff_first(path: Tuple[str], old: Any, new: Any, differ):
    # logger.debug('FIRST {} {} {}', path, old, new)
    first = True
    for member in differ(path, old, new):
        if first:
            yield path, old, new
            first = False
        yield member


def _diff_dict(path: Tuple[str], old: Dict[str, Any], new: Optional[Dict[str, Any]]) \
        -> Iterator[Tuple[Tuple[str], Any, Any]]:
    if not new:
        new = {}
    for member in set(old) - set(new):
        yield from _diff(path + (member,), old.get(member), None)
    for member in set(old) & set(new):
        yield from _diff(path + (member,), old.get(member), new.get(member))
    for member in set(new) - set(old):
        yield from _diff(path + (member,), None, new.get(member))


class AtomicUpdate(Diffable):
    version: int

    collection: ClassVar[str] = NotImplemented
    watcher: ClassVar[Watcher] = NotImplemented
    not_found_exception: ClassVar[Type] = NotImplemented

    @classmethod
    async def atomic_update(
            cls,
            query: dict,
            update: Optional[Callable[['AtomicUpdate'], Awaitable[Any]]] = None,
            create: Optional[Callable[[], Awaitable['AtomicUpdate']]] = None,
            max_retries=10
    ) -> Optional[str]:
        for i in range(max_retries):
            oid, old = await cls.from_db(query)
            if oid:
                if update:
                    await update(new := old.model_copy(deep=True))
                    await cls.watcher.run_recursive_diff(old, new)
                    if not any(_diff((), old, new)):
                        return

                    update_result = await getattr(AtomicUpdate.get_connection().db, cls.collection).update_one(
                        {'_id': ObjectId(oid), 'version': old.version},
                        {"$set": dict(version=old.version + 1, **new.model_dump(exclude={'version': True}))}
                    )
                    if update_result.modified_count:
                        break
                else:
                    new = None
                    delete_result = await getattr(AtomicUpdate.get_connection().db, cls.collection).delete_one(
                        {'_id': ObjectId(oid), 'version': old.version}
                    )
                    if delete_result.deleted_count:
                        break
            elif create:
                if not (new := await create()):
                    return
                await cls.watcher.run_recursive_diff(old, new)
                try:
                    if oid := (await getattr(AtomicUpdate.get_connection().db, cls.collection).insert_one(
                            new.model_dump())).inserted_id:
                        break
                except DuplicateKeyError:
                    continue
            else:
                raise cls.not_found_exception()
        else:
            raise MaxRetriesExceeded(msg=f"{cls.__name__}({query})")
        await cls.watcher.run_notify(oid, old, new)
        return str(oid)

    @classmethod
    async def from_db(cls, patient_query):
        if res := await getattr(AtomicUpdate.get_connection().db, cls.collection).find_one(
                patient_query, {k: 1 for k in cls.model_fields}
        ):
            return str(res.pop('_id')), cls(**res)
        return None, None

    @staticmethod
    @contextlib.contextmanager
    def set_connection(new_connection):
        global connection

        old_connection, connection = connection, new_connection
        yield
        connection = old_connection

    @staticmethod
    def get_connection():
        return connection


class ParsableMixin:
    @classmethod
    def parse(cls, value) -> 'ParsableMixin':
        raise NotImplemented()
