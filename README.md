# Home-Centralised IoT Control

A backend API for controlling smart home devices (TP-Link Kasa, with extensibility for other brands) running on a Raspberry Pi on the local network.

---

## Running the App

Requires Docker to be installed.

### Option 1: Local (recommended for development / device control)

Requires Python 3.11+ and a venv.

```bash
cd backend/app
source ../venv/bin/activate
uvicorn main:app --reload
```

Access at http://localhost:8000/docs

### Option 2: Docker — Linux / Raspberry Pi (required for device discovery)

```bash
docker build -t iot-app .
docker run --network host --restart always -d iot-app
```

`--network host` allows the container to broadcast on the local network and discover Kasa devices. Only works on Linux — use Option 1 on macOS during development.

### Option 3: Docker — macOS/Windows (no device discovery)

```bash
docker build -t iot-app .
docker run -p 8000:8000 iot-app
```

Access at http://localhost:8000/docs

> Note: Kasa device discovery will not work on macOS/Windows due to Docker networking limitations.

---

## Architecture

The project is structured in layers so that adding a new brand or device type never requires changes to the API or business logic.

```
+------------------+
|   HTTP Request   |  POST /lights/Lamp Dance/on
+------------------+
         |
         v
+------------------+
|    APIRouter     |  routes the request to the correct endpoint
+------------------+
         |
         v
+------------------+
|  DeviceManager   |  brand-agnostic, holds all discovered devices
+------------------+
         |
         v
+------------------+
|  Device Adapter  |  e.g. KasaLight, KasaPlug
+------------------+
         |
         v
+------------------+
|    Hardware      |  the physical device on the network
+------------------+
```

### Layer Breakdown

- **APIRouter** — each device type has its own route file (`lights.py`, `plugs.py`). Uses FastAPI dependency injection (`Depends`) to retrieve the DeviceManager from app state, keeping routes clean and testable.

- **DeviceManager** — discovers devices on the local network at startup, wraps each raw SDK object in the appropriate adapter, and stores them in a name-keyed dictionary. Brand-agnostic — the API never knows what vendor a device is.

- **Device Adapters** — vendor-specific wrappers (e.g. `KasaLight`, `KasaPlug`) that translate SDK calls into a common interface. Each adapter extends an abstract base class (`Light`, `Plug`) which extends `Device`.

- **Base Classes** — `Device` enforces a common structure (id, name, type, vendor) across all devices. `Light` and `Plug` define the abstract methods each device type must implement.

---

## What Was Built

- Layered architecture separating API, orchestration, and vendor adapters
- Abstract base classes (`Device`, `Light`, `Plug`) as contracts for all device types
- TP-Link Kasa support for smart bulbs (`KasaLight`) and smart plugs (`KasaPlug`)
- REST API endpoints for lights and plugs (on, off, brightness, state, energy usage)
- FastAPI dependency injection for clean, testable route handlers
- CI pipeline (ruff linting + Docker build) on every push
- CD pipeline that SSHs into the Raspberry Pi and deploys on merge to main
- Pytest integration tests with mocked dependencies for lights and plugs

---

## Future Improvements

- **Modular device managers** — move from a single `DeviceManager` to one manager per brand (e.g. `TPLinkManager`, `HueManager`) so adding a new brand is purely additive
- **Philips Hue support** — add `HueLight` adapter and `HueManager`
- **Auth** — protect the API with an API key (via FastAPI dependency) so only authorised clients can control devices
- **Scheduled triggers** — use APScheduler to turn everything off at a set time (e.g. midnight)
- **Refresh/discover endpoint** — `POST /devices/refresh` to detect new or removed devices without restarting the server
- **WebSockets** — replace polling with push-based device state updates to the frontend
- **Frontend** — React app with device cards, controlling lights and plugs from the UI
- **Container registry** — push built Docker image to GitHub Container Registry during CI so the Pi pulls a ready image instead of building it locally
- **Logging** — replace print statements with structured logging for monitoring device activity and failures
- **Tailscale** — VPN tunnel so the CD pipeline and frontend can reach the Pi from anywhere, not just the home network