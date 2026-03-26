from devices.base.light import Light


# KasaLight class wraper for tp_link SDK
class KasaLight(Light):

    def __init__(self, device):
        super().__init__(
            id=device.alias,  # id is the Name of the Lamp in the network
            name=device.alias,
            vendor="tp-link",
        )
        self.device = device

    async def turn_on(self):
        await self.device.turn_on()

    async def turn_off(self):
        await self.device.turn_off()

    async def set_brightness(self, level):
        await self.device.set_brightness(level)

    async def get_state(self):
        await self.device.update()
        return {
            "on": self.device.is_on,
            "brightness": self.device.brightness,
            "reachable": True,
        }
