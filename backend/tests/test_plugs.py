import pytest
from fastapi.testclient import TestClient
from main import app
from api.routes.lights import get_manager


# Mocked a plug
class MockPlug:
    async def turn_on(self):
        pass

    async def turn_off(self):
        pass

    async def get_energy_usage(self):
        return {"power_w": 60.0, "voltage_v": 230.0, "current_a": 0.26}

    async def get_state(self):
        return {"on": True, "reachable": True}

    def to_dict(self):
        return {
            "id": "Living Room Plug",
            "name": "Living Room Plug",
            "type": "plug",
            "vendor": "tp-link",
        }


# Mocked the manager
class MockManager:
    def get_device(self, device_id):
        if device_id == "Living Room Plug":
            return MockPlug()
        return None

    def get_devices(self, type):
        return [
            {
                "id": "Living Room Plug",
                "name": "Living Room Plug",
                "type": "plug",
                "vendor": "tp-link",
            }
        ]


# prevents test_lights.py MockManager from overwriting this one since both share the same app instance
@pytest.fixture(autouse=True)
def override_manager():
    app.dependency_overrides[get_manager] = lambda: MockManager()
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_turn_on_existing_plug():
    response = client.post("/plugs/Living Room Plug/on")
    assert response.status_code == 200
    assert response.json()["status"] == "Turned on"


def test_turn_on_missing_plug():
    response = client.post("/plugs/Unknown/on")
    assert response.status_code == 404


def test_turn_off_existing_plug():
    response = client.post("/plugs/Living Room Plug/off")
    assert response.status_code == 200
    assert response.json()["status"] == "Turned off"


def test_turn_off_missing_plug():
    response = client.post("/plugs/Unknown/off")
    assert response.status_code == 404


def test_get_energy_existing_plug():
    response = client.get("/plugs/Living Room Plug/energy")
    assert response.status_code == 200
    assert response.json()["energy"]["power_w"] == 60.0


def test_get_energy_missing_plug():
    response = client.get("/plugs/Unknown/energy")
    assert response.status_code == 404


def test_get_state_existing_plug():
    response = client.get("/plugs/Living Room Plug/state")
    assert response.status_code == 200
    assert response.json()["state"]["on"] is True


def test_get_state_missing_plug():
    response = client.get("/plugs/Unknown/state")
    assert response.status_code == 404


def test_get_all_plugs():
    response = client.get("/plugs")
    assert response.status_code == 200
    assert len(response.json()) > 0
