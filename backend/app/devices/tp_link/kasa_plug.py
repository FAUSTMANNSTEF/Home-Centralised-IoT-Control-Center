from devices.base.plug import Plug


class KasaPlug(Plug):
    """TP-Link Kasa adapter for a smart plug — wraps the raw kasa SDK device."""

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

    async def get_energy_usage(self):
        await self.device.update()
        emeter = self.device.emeter_realtime
        return {
            "power_w": emeter.get("power"),
            "voltage_v": emeter.get("voltage"),
            "current_a": emeter.get("current"),
        }

    async def get_state(self):
        await self.device.update()
        return {
            "on": self.device.is_on,
            "reachable": True,
        }