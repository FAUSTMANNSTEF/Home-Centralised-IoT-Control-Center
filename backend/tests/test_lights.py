import pytest
from fastapi.testclient import TestClient
from main import app
from api.routes.lights import get_manager


# Mocked the light class
class MockLight:
    async def turn_on(self):
        pass

    async def turn_off(self):
        pass

    async def set_brightness(self, level):
        pass

    async def get_state(self):
        return {"on": True, "brightness": 80, "reachable": True}

    def to_dict(self):
        return {
            "id": "Lamp Dance",
            "name": "Lamp Dance",
            "type": "light",
            "vendor": "tp-link",
        }


# Mocked the manager
class MockManager:
    def get_device(self, device_id):
        if device_id == "Lamp Dance":
            return MockLight()
        return None

    def get_devices(self, type):
        return [
            {
                "id": "Lamp Dance",
                "name": "Lamp Dance",
                "type": "light",
                "vendor": "tp-link",
            }
        ]


app.dependency_overrides[get_manager] = (
    lambda: MockManager()
)  # Replace actual manager with mocked one
client = TestClient(app)  # HTTP client testerß


def test_turn_on_existing_light():
    response = client.post("/lights/Lamp Dance/on")
    assert response.status_code == 200
    assert response.json()["status"] == "Turned on"


def test_turn_on_missing_light():
    response = client.post("/lights/Unknown/on")
    assert response.status_code == 404


def test_turn_off_existing_light():
    response = client.post("/lights/Lamp Dance/off")
    assert response.status_code == 200
    assert response.json()["status"] == "Turned off"


def test_turn_off_missing_light():
    response = client.post("/lights/Unknown/off")
    assert response.status_code == 404


def test_set_brightness_existing_light():
    response = client.post("/lights/Lamp Dance/brightness/50")
    assert response.status_code == 200
    assert response.json()["status"] == "Set Brightness to: 50"


def test_set_brightness_missing_light():
    response = client.post("/lights/Unknown/brightness/50")
    assert response.status_code == 404


def test_get_state_existing_light():
    response = client.get("/lights/Lamp Dance/state")
    assert response.status_code == 200
    assert response.json()["state"]["on"] is True


def test_get_state_missing_light():
    response = client.get("/lights/Unknown/state")
    assert response.status_code == 404


def test_get_all_lights():
    response = client.get("/lights")
    assert response.status_code == 200
    assert len(response.json()) > 0
