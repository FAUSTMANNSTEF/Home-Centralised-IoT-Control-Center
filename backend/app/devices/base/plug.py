from abc import ABC, abstractmethod
from devices.base.device import Device


class Plug(Device, ABC):
    """Abstract base class for all smart plugs. Any brand-specific plug must implement these methods."""

    def __init__(self, id: str, name: str, vendor: str):
        super().__init__(id=id, name=name, device_type="plug", vendor=vendor)

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def get_energy_usage(self):
        pass

    @abstractmethod
    async def get_state(self):
        pass
