# Home-Centralised IoT Control

## Instructions

- Navigate to app and run "uvicorn main:app --reload"
- Endpoints have been tested using Postman

---

## What I Did

- Added **specific API route paths** to make the backend scalable, avoiding having everything in `main`.
- Used **Adapters** to make it easy to support devices with different APIs (e.g., Kasa, Hue, etc.).
- Implemented a **DeviceManager** to handle network calls and wrap all discovered devices into their corresponding adapters.

---

## Architecture

The flow of an HTTP request for controlling a device:

+------------------+
| HTTP Request | -> POST /lights/livingroom/off
+------------------+
|
v
+------------------+
| APIRouter | -> knows which DeviceManager to ask
+------------------+
|
v
+------------------+
| DeviceManager | -> generic, brand-agnostic, holds all devices
+------------------+
|
v
+------------------+
| Device Adapter | -> e.g., KasaLight
+------------------+
|
v
+------------------+
| Hardware | -> the actual lamp
+------------------+

**Explanation of each layer:**

- **HTTP Request:** Frontend or external service sends a request to the API.
- **APIRouter:** Routes the request to the appropriate endpoint and interacts with the DeviceManager.
- **DeviceManager:** Maintains all devices in the network, independent of brand or type.
- **Device Adapter:** Wraps the vendor-specific SDK or API calls into a common interface.
- **Hardware:** The actual physical device being controlled.

---

## Future TODOs

- Test API endpoints using Postman
- Auth using an API Key in router dependencies or router params in the backend even though its local maybe my friends would want to mess around

## Future Possible Improvements

- Add **error handling** for unreachable/offline devices.
- Implement a **list all devices** endpoint (`GET /devices`) so the frontend can dynamically display all devices.
- Add a **refresh/discover endpoint** to detect and add new devices dynamically while the server is running.(kind of solves a big part of the error handling)
- Device authentication with IOTA
- Support **more device types** (e.g., plugs, sensors) using additional adapters and abstract base classes.
- Optional: implement **logging** and **metrics** to monitor device activity and failures.
- Implement LogIn
- At scheduled triggers example at 12:00 everything turns off etc
