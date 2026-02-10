# Central Point for discovering devices in a network
from kasa import Discover
from devices.tp_link.kasa_light import KasaLight
from devices.phillips_hue.phillips_hue import HueLight

"""
Device discovery and management layer.

Responsible for:
- Discovering devices on the local network
- Wrapping devices in brand-specific adapters
- Providing a generic interface for retrieving devices
"""


class DeviceManager:

    def __init__(self):
        self.devices = {}

    # Checks if device exists withing my network and returns it if it does
    def get_device(self, device_id: str):
        return self.devices.get(device_id)

    # finds tp devices and wraps them in appropriate adapter
    async def find_tp_devices(self):
        found_devices = await Discover.discover()
        print("Found raw tp_link devices:", found_devices)
        for device in found_devices.values():
            print(device.device_type)
            if device.device_type.name == "Bulb":
                adapter = KasaLight(device)
            else:
                continue  # add more TP-Link devices later
            self.devices[device.alias] = adapter
            print(self.devices)

    # finds Hue Lights and wraps them in appropriate adapter
    async def find_hue_lights(self, bridge_ip, username):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://{bridge_ip}/api/{username}/lights")
            lights = resp.json()
            for light_id, info in lights.items():
                adapter = HueLight(bridge_ip, username, light_id)
                self.devices[info["name"]] = adapter

    async def discover_devices(self):
        await self.find_tp_devices()
        await self.find_hue_lights()
