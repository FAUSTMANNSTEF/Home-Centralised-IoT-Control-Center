# devices/hue/hue_light.py
import httpx
from devices.base.light import Light


# HueLight class wrapper for Phillips Hue Lamps utilizing a Hue Bridge
class HueLight(Light):
    """
    Args:
        bridge_ip (str): The local IP address of the Hue Bridge.
        username (str): The API username (token) for the Hue Bridge.
        light_id (str): The ID of the specific light on the bridge to control.
    """

    def __init__(self, bridge_ip: str, username: str, light_id: str):
        self.base_url = f"http://{bridge_ip}/api/{username}"
        self.light_id = light_id

    async def turn_on(self):
        async with httpx.AsyncClient() as client:
            await client.put(
                f"{self.base_url}/lights/{self.light_id}/state", json={"on": True}
            )

    async def turn_off(self):
        async with httpx.AsyncClient() as client:
            await client.put(
                f"{self.base_url}/lights/{self.light_id}/state", json={"on": False}
            )

    async def set_brightness(self, level: int):
        # Hue brightness is 0-254
        bri = max(0, min(254, int(level * 254 / 100)))
        async with httpx.AsyncClient() as client:
            await client.put(
                f"{self.base_url}/lights/{self.light_id}/state", json={"bri": bri}
            )

    async def get_state(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/lights/{self.light_id}")
            return resp.json()
