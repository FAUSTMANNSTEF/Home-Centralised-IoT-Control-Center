from devices.base.light import Light


# KasaLight class wraper for tp_link SDK
class KasaLight(Light):

    def __init__(self, device):
        self.device = device
        self.id = device.alias  # id is the Name of the Lamp in the network

    async def turn_on(self):
        await self.device.turn_on()

    async def turn_off(self):
        await self.device.turn_off()

    async def set_brightness(self, level):
        await self.device.set_brightness(level)

    async def get_state(self):
        state = await self.device.update()
        return state
