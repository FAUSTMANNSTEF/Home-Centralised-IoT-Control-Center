from fastapi import FastAPI
from api.routes.lights import router as lights_router
from manager.device_manager import DeviceManager


app = FastAPI()
app.include_router(lights_router)


@app.on_event("startup")
async def startup():
    app.state.device_manager = DeviceManager()
    await app.state.device_manager.discover_devices()
