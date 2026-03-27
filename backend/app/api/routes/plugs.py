from fastapi import APIRouter, HTTPException, Depends
from devices.base.plug import Plug
from manager.device_manager import DeviceManager
from api.routes.lights import get_manager


router = APIRouter(prefix="/plugs", tags=["plugs"])


@router.post("/{plug_id}/on")
async def turn_plug_on(plug_id: str, manager: DeviceManager = Depends(get_manager)):
    """Turns on the plug with the given name. Returns 404 if not found."""
    plug = manager.get_device(plug_id)
    if plug:
        await plug.turn_on()
    else:
        raise HTTPException(status_code=404, detail=f"Plug with id:{plug_id} not found")
    return {"id": plug_id, "status": "Turned on"}


@router.post("/{plug_id}/off")
async def turn_plug_off(plug_id: str, manager: DeviceManager = Depends(get_manager)):
    """Turns off the plug with the given name. Returns 404 if not found."""
    plug = manager.get_device(plug_id)
    if plug:
        await plug.turn_off()
    else:
        raise HTTPException(status_code=404, detail=f"Plug with id:{plug_id} not found")
    return {"id": plug_id, "status": "Turned off"}


@router.get("/{plug_id}/energy")
async def get_energy_usage(plug_id: str, manager: DeviceManager = Depends(get_manager)):
    """Returns the current energy usage of the plug (power, voltage, current). Returns 404 if not found."""
    plug = manager.get_device(plug_id)
    if plug:
        usage = await plug.get_energy_usage()
    else:
        raise HTTPException(status_code=404, detail=f"Plug with id:{plug_id} not found")
    return {"id": plug_id, "energy": usage}


@router.get("/{plug_id}/state")
async def get_state(plug_id: str, manager: DeviceManager = Depends(get_manager)):
    """Returns the current state of the plug (on/off). Returns 404 if not found."""
    plug = manager.get_device(plug_id)
    if plug:
        state = await plug.get_state()
    else:
        raise HTTPException(status_code=404, detail=f"Plug with id:{plug_id} not found")
    return {"id": plug_id, "state": state}


@router.get("")
async def get_plugs(manager: DeviceManager = Depends(get_manager)):
    """Returns all plugs currently discovered on the network."""
    plugs = manager.get_devices(Plug)
    if plugs:
        return plugs
    else:
        raise HTTPException(status_code=404, detail="No plugs found")