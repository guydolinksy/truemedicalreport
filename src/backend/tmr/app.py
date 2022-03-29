from asyncio import Future

from fastapi import FastAPI, WebSocket

from tmr.routes.wing import wing_router
from tmr.routes.patient import patient_router
from tmr.routes.department import department_router
from tmr.models.web_sockets import ConnectionManager


def create_app() -> FastAPI:
    app_ = FastAPI(root_path='/api')
    app_.include_router(wing_router, prefix="/wing")
    app_.include_router(patient_router, prefix="/patient")
    app_.include_router(department_router, prefix="/department")

    return app_


app = create_app()

conn = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, url: str = None):
    if url:
        i = 0
        await websocket.accept()
        while await conn.wait(url):
            i += 1
            print('done')
            await websocket.send_text(str(i))


@app.route('/test_broadcast')
async def broadcast_url():
    await conn.broadcast_url()
