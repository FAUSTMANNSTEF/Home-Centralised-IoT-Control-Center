Frontend (UI)
   ↓ HTTP / WebSocket
Backend API (FastAPI)
   ↓
Device Abstraction Layer  ←── kasa lives here
   ↓
Actual devices (TP-Link lamp, relays, etc.)

Not Does
❌ Expose kasa directly to the frontend
❌ Write backend routes that depend on kasa everywhere
❌ Let device-specific logic leak into your API

Your backend becomes a home automation platform, not a TP-Link script. Generalize , using dynamic lnks 

Adapter Pattern

kasa → LightDevice

Factory / Registry

Map ID → device instance

Dependency inversion

API depends on interfaces, not brands