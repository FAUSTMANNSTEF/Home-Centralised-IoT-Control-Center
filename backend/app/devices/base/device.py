from abc import ABC
from typing import Dict


class Device(ABC):
    """
    Base contract for all devices regardless of brand or type.
    Enforces that every device has a common identity (id, name, device_type, vendor)

    Inheritance chain:
        Device → Light → KasaLight (or any other brand-specific implementation)
    """

    def __init__(
        self,
        *,
        id: str,
        name: str,
        device_type: str,
        vendor: str,
    ):
        self.id = id
        self.name = name
        self.device_type = device_type
        self.vendor = vendor

    def to_dict(self) -> Dict:
        """
        Convert device to a JSON-serializable dict for API responses.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.device_type,
            "vendor": self.vendor,
        }
