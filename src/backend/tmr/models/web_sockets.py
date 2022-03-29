from asyncio import Future

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.futures = {}

    async def wait(self, url: str):
        print('wait')
        return self.futures.setdefault(url, Future())

    async def broadcast_url(self):
        print('b')
        for f in self.futures:
            # f.set_result()
            break
