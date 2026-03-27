from devices.base.light import Light


class KasaLight(Light):
    """TP-Link Kasa adapter for a smart bulb."""

    def __init__(self, device):
        """Initialises the adapter using the device alias as both id and name."""
        super().__init__(
            id=device.alias,
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
