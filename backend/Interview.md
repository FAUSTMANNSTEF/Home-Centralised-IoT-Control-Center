## what is encapsulation inheritance polymorhism

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
