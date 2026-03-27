from fastapi import APIRouter, HTTPException, Request, Depends
from devices.base.light import Light
from manager.device_manager import DeviceManager


router = APIRouter(prefix="/lights", tags=["lights"])


def get_manager(request: Request) -> DeviceManager:
    """Dependency that retrieves the DeviceManager from app state."""
    return request.app.state.device_manager


@router.post("/{light_id}/on")
async def turn_light_on(light_id: str, manager: DeviceManager = Depends(get_manager)):
    """Turns on the light with the given name. Returns 404 if not found."""
    light = manager.get_device(light_id)
    if light:
        await light.turn_on()
    else:
        raise HTTPException(status_code=404, detail=f"Light with id:{light_id} not found")
    return {"id": light_id, "status": "Turned on"}


@router.post("/{light_id}/off")
async def turn_light_off(light_id: str, manager: DeviceManager = Depends(get_manager)):
    """Turns off the light with the given name. Returns 404 if not found."""
    light = manager.get_device(light_id)
    if light:
        await light.turn_off()
    else:
        raise HTTPException(status_code=404, detail=f"Light with id:{light_id} not found")
    return {"id": light_id, "status": "Turned off"}


@router.post("/{light_id}/brightness/{level}")
async def set_brightness(light_id: str, level: int, manager: DeviceManager = Depends(get_manager)):
    """Sets the brightness of the light to the given level (0-100). Returns 404 if not found."""
    light = manager.get_device(light_id)
    if light:
        await light.set_brightness(level)
    else:
        raise HTTPException(status_code=404, detail=f"Light with id:{light_id} not found")
    return {"id": light_id, "status": f"Set Brightness to: {level}"}


@router.get("/{light_id}/state")
async def get_state(light_id: str, manager: DeviceManager = Depends(get_manager)):
    """Returns the current state of the light (on/off, brightness). Returns 404 if not found."""
    light = manager.get_device(light_id)
    if light:
        state = await light.get_state()
    else:
        raise HTTPException(status_code=404, detail=f"Light with id:{light_id} not found")
    return {"id": light_id, "state": state}


@router.get("")
async def get_lights(manager: DeviceManager = Depends(get_manager)):
    """Returns all lights currently discovered on the network."""
    lights = manager.get_devices(Light)
    if lights:
        return lights
    else:
        raise HTTPException(status_code=404, detail="No lights found")
