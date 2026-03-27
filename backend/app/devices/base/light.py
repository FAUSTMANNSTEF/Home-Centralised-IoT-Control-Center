from abc import ABC, abstractmethod
from devices.base.device import Device


class Light(Device, ABC):
    """Abstract base class for all light devices. Any brand-specific light must implement these methods."""

    def __init__(self, id: str, name: str, vendor: str):
        super().__init__(id=id, name=name, device_type="light", vendor=vendor)

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def set_brightness(self, level):
        pass

    @abstractmethod
    async def get_state(self):
        pass
