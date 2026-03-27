# NetBox SDK

`netbox_sdk` is a standalone Python library for connecting to NetBox over its REST API. It is the shared core used by both the CLI and the TUI, but it can also be imported independently in any Python project.

The SDK exposes two layers:

- `NetBoxApiClient` for low-level async request control
- `api()` / `Api` for a higher-level async facade with PyNetBox-style workflows

## Modules

| Module | Responsibility |
|---|---|
| `netbox_sdk.config` | Config model, profile persistence, auth header construction |
| `netbox_sdk.client` | Async HTTP client and connection probe |
| `netbox_sdk.facade` | Async convenience API for apps, endpoints, records, and detail routes |
| `netbox_sdk.http_cache` | Filesystem cache with TTL/stale-if-error support |
| `netbox_sdk.schema` | OpenAPI schema loading and indexing |
| `netbox_sdk.services` | Dynamic request resolution |
| `netbox_sdk.plugin_discovery` | Runtime plugin API discovery |

## Installation

```bash
pip install netbox-sdk
```

## Quick start

```python
import asyncio
from netbox_sdk import api


async def main():
    nb = api("https://netbox.example.com", token="your-token")

    device = await nb.dcim.devices.get(42)
    if device is not None:
        print(device.name)

asyncio.run(main())
```

If you want raw HTTP control instead of the facade, use `NetBoxApiClient` directly.
