from abc import ABC, abstractmethod


# Abstract Light base class
class Light(ABC):

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
