"""
Device discovery and management layer.

Responsible for:
- Discovering devices on the local network
- Wrapping devices in brand-specific adapters
- Providing a generic interface for retrieving devices
"""

from kasa import Discover
from devices.tp_link.kasa_light import KasaLight
from devices.tp_link.kasa_plug import KasaPlug


class DeviceManager:

    def __init__(self):
        """Initialises the device storage as a name -> adapter dictionary."""
        self.devices = {}

    def get_device(self, device_id: str):
        """Returns the device adapter by name, or None if not found."""
        return self.devices.get(device_id)

    def get_devices(self, type: str):
        """Returns all devices matching the given type (e.g. Light, TV)."""
        devices = []
        for device in self.devices.values():
            if isinstance(device, type):
                devices.append(device.to_dict())
        return devices

    async def find_tp_devices(self):
        """Discovers TP-Link devices on the network using the kasa library, wraps raw objects in the appropriate tp_link adapter."""
        found_devices = await Discover.discover()
        # print("Found raw tp_link devices:", found_devices)
        for device in found_devices.values():
            # print(device.device_type)
            if device.device_type.name == "Bulb":
                adapter = KasaLight(device)
            elif device.device_type.name == "Plug":
                adapter = KasaPlug(device)
            else:
                continue  # add more TP-Link devices later
            self.devices[device.alias] = adapter
            # print(self.devices)

    async def discover_devices(self):
        """Runs discovery across all supported brands"""
        await self.find_tp_devices()
