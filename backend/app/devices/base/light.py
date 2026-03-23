from abc import ABC, abstractmethod
from devices.base.device import Device


# Abstract Light base class
class Light(Device, ABC):

    def __init__(self, id: str, name: str, vendor: str):
        super().__init__(id=id, name=name, device_type="light", vendor=vendor)

    # Turn on
    @abstractmethod
    async def turn_on(self):
        pass

    # Turn off
    @abstractmethod
    async def turn_off(self):
        pass

    # Brightness
    @abstractmethod
    async def set_brightness(self, level):
        pass

    # Status
    @abstractmethod
    async def get_state(self):
        pass
