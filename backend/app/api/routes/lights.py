from fastapi import APIRouter, HTTPException, Request


router = APIRouter(prefix="/lights", tags=["lights"])


# Turns Light with specific light_id on
@router.post("/{light_id}/on")
async def turn_light_on(light_id: str, request: Request):
    manager = request.app.state.device_manager
    light = manager.get_device(light_id)
    if light:
        await light.turn_on()

    else:
        raise HTTPException(
            status_code=404, detail=f"Light with id:{light_id} not found"
        )

    return {"id": light_id, "status": "Turned on"}


# Turns Light with specific light_id off
@router.post("/{light_id}/off")
async def turn_light_off(light_id: str, request: Request):
    manager = request.app.state.device_manager
    light = manager.get_device(light_id)
    if light:
        await light.turn_off()

    else:
        raise HTTPException(
            status_code=404, detail=f"Light with id:{light_id} not found"
        )

    return {"id": light_id, "status": "Turned off"}


# Adjusts brightness of a light with specific light_id
@router.post("/{light_id}/brightness/{level}")
async def set_brightness(light_id: str, level: int, request: Request):
    manager = request.app.state.device_manager
    light = manager.get_device(light_id)
    if light:
        await light.set_brightness(level)

    else:
        raise HTTPException(
            status_code=404, detail=f"Light with id:{light_id} not found"
        )

    return {"id": light_id, "status": f"Set Brightness to: {level}"}


# Adjusts brightness of a light with specific light_id
@router.get("/{light_id}/state")
async def get_state(light_id: str, request: Request):
    manager = request.app.state.device_manager
    light = manager.get_device(light_id)
    if light:
        state = await light.get_state()

    else:
        raise HTTPException(
            status_code=404, detail=f"Light with id:{light_id} not found"
        )

    return {"id": light_id, "state": state}
