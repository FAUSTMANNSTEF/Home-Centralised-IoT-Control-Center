# Central Point for discovering devices in a network
from kasa import Discover
from devices.tp_link.kasa_light import KasaLight

"""
Device discovery and management layer.

Responsible for:
- Discovering devices on the local network
- Wrapping devices in brand-specific adapters
- Providing a generic interface for retrieving devices
"""


class DeviceManager:

    # devices acts as a dictionary with key(name) value(Adaptor Object) pairs
    def __init__(self):
        self.devices = {}

    # Checks if device exists withing my network and returns it if it does
    def get_device(self, device_id: str):
        return self.devices.get(device_id)

    # Gets all devices of a specific type (light,tv etc)
    def get_devices(self, type: str):
        devices = []
        for device in self.devices.values():
            if isinstance(device, type):
                devices.append(device.to_dict())
        return devices

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

    async def discover_devices(self):
        await self.find_tp_devices()
