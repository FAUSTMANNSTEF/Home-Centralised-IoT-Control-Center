# Central Point for discovering devices in a network
from kasa import Discover
from devices.tp_link.kasa_light import KasaLight


class DeviceManager:

    def __init__(self):
        self.devices = {}

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

    async def discover_devices(self):
        await self.find_tp_devices()
