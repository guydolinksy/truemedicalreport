from dataclasses import dataclass

import logbook
from motor.motor_asyncio import AsyncIOMotorDatabase as Database

logger = logbook.Logger(__name__)


@dataclass
class ApplicationDal:
    db: Database

    async def set_config(self, key, version, value):
        await self.db.config.update_one(
            {'key': key, 'version': version},
            {'$set': {'version': version, 'value': value}},
            upsert=True
        )

    async def get_config(self, key, default):
        async for res in self.db.config.find({'key': key}, {'value': 1, 'version': 1}).sort([('version', -1)]):
            return dict(version=res['version'], value=res['value'])
        return dict(version=None, value=default)