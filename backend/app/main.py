from fastapi import FastAPI
from api.routes.lights import router as lights_router
from api.routes.plugs import router as plugs_router
from manager.device_manager import DeviceManager


app = FastAPI()
app.include_router(lights_router)
app.include_router(plugs_router)


@app.on_event("startup")
async def startup():
    """Mounts the DeviceManager on the startup and discovers smart devices on the network."""
    app.state.device_manager = DeviceManager()
    await app.state.device_manager.discover_devices()
