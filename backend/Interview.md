## what is encapsulation inheritance polymorhism Dependency Inversion

“I separated abstractions, vendor adapters, and orchestration so that adding a new device type or brand never impacts the API or existing logic.”

### In Device why not add functionality methods ? because this is to see how i want to show stuff to the front end , not all devices share the same functionality

## Used a Dictionary in device.py

## Problem: Dynamic Device Availability

In a home IoT system, devices can go offline or be added at any time:

- A bulb may be unplugged or powered off → backend thinks it’s still available
- New devices may be added after startup → backend doesn’t know about them
- Commands sent to offline devices may fail (KasaException)

---

## Solutions Considered

### 1. Per-command online check (`is_online()`)

- Before sending any command, ping the device  
  **Pros:** Accurate, prevents sending commands to offline devices  
  **Cons:** Adds network overhead for every command

### 2. Periodic background discovery

- Backend scans network at intervals to refresh device list  
  **Pros:** Automatically keeps list up-to-date  
  **Cons:** Adds complexity, still can fail between scans

### 3. Manual refresh endpoint

- Frontend or user triggers `/devices/refresh` to update device list  
  **Pros:** Simple, low overhead, works well in home setups  
  **Cons:** Relies on user to refresh after changes

### 4. Safe command wrapper / try-catch

- Wrap all hardware commands in `try/except` to catch offline errors  
  **Pros:** Backend never crashes, provides meaningful HTTP errors  
  **Cons:** Doesn’t proactively know offline devices

What is Uvicorn

Regarding Github action pipeline
flake & ruff for linting
What is requirements.txt i used pipreqs for it when should i use it
requirements.txt vs requirements-dev.txt

.github file what does it do, Yaml files what do they do , how is this a pipeline
