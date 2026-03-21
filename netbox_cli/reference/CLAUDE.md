# netbox_cli/reference — Bundled Reference Data

Static data files bundled with the package at install time (declared in `pyproject.toml` under `[tool.setuptools.package-data]`).

## Contents

| Path | Description |
|---|---|
| `openapi/netbox-openapi.json` | NetBox OpenAPI 3.0 schema (JSON) |
| `openapi/netbox-openapi.yaml` | NetBox OpenAPI 3.0 schema (YAML) |

## How It's Used

`netbox_cli/schema.py` loads `openapi/netbox-openapi.json` at startup via `importlib.resources` (or a path relative to `__file__`). The schema is loaded **once**, indexed into `SchemaIndex`, and reused for the entire process lifetime.

This schema drives:
- `nbx groups` — lists all API groups
- `nbx resources <group>` — lists resources per group
- `nbx ops <group> <resource>` — shows available HTTP operations
- Dynamic command routing — maps action names to correct HTTP methods and paths
- Filter parameter discovery — populates `--filter` options in the TUI

## Updating the Schema

When a new NetBox version is released, replace both files with the updated schema from the target NetBox instance:

```bash
curl https://<your-netbox>/api/schema/?format=json -o netbox_cli/reference/openapi/netbox-openapi.json
curl https://<your-netbox>/api/schema/?format=yaml -o netbox_cli/reference/openapi/netbox-openapi.yaml
```

Or download from the official NetBox GitHub releases.

> **Do not** reference the live NetBox API schema at runtime. The bundled file ensures the CLI works offline and pins the supported schema version.
