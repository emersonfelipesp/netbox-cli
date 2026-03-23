# NetBox CLI and TUI

## Contents

- [Quick Test with NetBox Demo Instance](#quick-test-with-netbox-demo-instance)
- [Install](#install)
  - [Install `nbx` Globally (bash + zsh)](#install-nbx-globally-bash--zsh)
- [Configure](#configure)
- [Command Modes](#command-modes)
  - [1) Dynamic mode (OpenAPI app/resource/action)](#1-dynamic-mode-openapi-appresourceaction)
  - [2) Explicit HTTP mode](#2-explicit-http-mode)
  - [3) Discovery helpers](#3-discovery-helpers)
  - [4) Developer / workbench mode](#4-developer--workbench-mode)
  - [5) Application logs](#5-application-logs)
  - [6) Documentation capture](#6-documentation-capture)
  - [7) TUI mode](#7-tui-mode)
  - [Custom Themes (JSON)](#custom-themes-json)
- [Project Layout](#project-layout)
- [Notes](#notes)

---

`netbox-cli` is an API-first NetBox client that supports both:

- direct command execution (`nbx dcim devices get --id 1`)
- interactive Textual TUI (`nbx tui`)

The project is bootstrapped from `CLAUDE.md` requirements:

- API-only integration with NetBox (no model access)
- async HTTP via `aiohttp`
- shared backend logic for CLI and TUI
- OpenAPI-driven command/resource discovery
- automatic TUI discovery for plugin REST resources under `/api/plugins/`

## Quick Test with NetBox Demo Instance

The fastest way to try `netbox-cli` — one command installs everything and connects to the public [demo.netbox.dev](https://demo.netbox.dev) instance.

**Install:**

```bash
# Debian/Ubuntu — install curl if not present
sudo apt-get update && sudo apt-get install -y curl

curl -fsSL https://raw.githubusercontent.com/emersonfelipesp/netbox-cli/main/install.sh | bash
```

The script installs [`uv`](https://github.com/astral-sh/uv) if not present, fetches `netbox-cli` directly from this GitHub repository, and sets up Playwright Chromium for the demo login flow.

**Reload your shell after install** (the installer runs in a subshell, so PATH changes need to be applied):

```bash
source ~/.bashrc   # bash
source ~/.zshrc    # zsh
```

If `nbx` is still not found, run it directly by full path as a fallback:

```bash
~/.local/bin/nbx --help
```

**Authenticate with the demo instance:**

```bash
nbx demo init
# enter your demo.netbox.dev username and password when prompted
```

Or non-interactively (CI / scripted):

```bash
nbx demo init --username <your-demo-user> --password <your-demo-password>
```

**Run CLI commands against demo.netbox.dev:**

```bash
nbx demo dcim devices list
nbx demo dcim sites list
nbx demo ipam prefixes list
nbx demo circuits circuit-terminations get --id 15 --trace-only
```

**Launch the interactive TUI:**

```bash
nbx demo tui
```

Use `/` to search, `g` to focus the nav tree, `q` to quit. All commands that work under `nbx demo …` are available inside the TUI with the same demo profile.

If your NetBox instance has plugins with a full REST API implementation, the TUI can discover their `/api/plugins/...` resources automatically and render them in navigation without extra configuration.

---

## Install

```bash
cd <path-to-netbox-cli>
uv tool install --force .
```

## Install `nbx` Globally (bash + zsh)

Preferred (`uv tool`):

```bash
uv tool install --force <path-to-netbox-cli>
nbx --help
```

If `nbx` is not found, ensure your shell PATH includes `~/.local/bin`.

For **bash**:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
nbx --help
```

For **zsh**:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
nbx --help
```

Alternative (repo-local maintenance environment):

```bash
cd <path-to-netbox-cli>
uv sync --dev
uv run nbx --help
```

This keeps a project-managed environment for development tasks. The main end-user install path remains `uv tool install`.

Contributor standard:

```bash
cd <path-to-netbox-cli>
uv sync --dev
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
uv run pre-commit run --all-files
```

Commits and pushes should go through `pre-commit`, which runs Ruff linting and formatting locally and in GitHub Actions.

## Configure

```bash
nbx init
# prompts for base URL, token key, token secret, timeout
```

If configuration is missing, `nbx` will prompt for host/token credentials automatically before executing commands (including `nbx tui`).

Demo profile bootstrap:

```bash
nbx demo init
```

This always targets `https://demo.netbox.dev/`, opens the NetBox login flow in Playwright, prompts for demo username/password in the terminal, creates a fresh API token, and stores that token in the separate `demo` profile.

Install the Playwright browser first if you want browser-based demo bootstrap:

```bash
uv tool run --from playwright playwright install chromium --with-deps
```

If you already have a demo API token, you can skip Playwright entirely:

```bash
nbx demo --token-key <key> --token-secret <secret>
```

The normal `nbx` profile and the `nbx demo` profile are stored separately in the same config file.

Stored config path:

- `$XDG_CONFIG_HOME/netbox-cli/config.json`
- or `~/.config/netbox-cli/config.json`

Environment overrides:

- `NETBOX_URL`
- `NETBOX_TOKEN_KEY`
- `NETBOX_TOKEN_SECRET`

Authentication uses v2 token format sent as:

- `Authorization: Bearer nbt_<KEY>.<TOKEN>`

If a v2 token request returns 403, the client automatically retries using the v1 `Token <token>` format.

## Command Modes

### 1) Dynamic mode (OpenAPI app/resource/action)

```bash
nbx dcim devices list
nbx dcim devices get --id 1
nbx ipam ip-addresses create --body-json '{"address":"192.0.2.10/24","status":"active"}'
nbx dcim devices list -q name=switch01
```

This path is now fully registered as real Typer subcommands generated from OpenAPI, so `--help` works at each level:

```bash
nbx dcim --help
nbx dcim devices --help
nbx dcim devices get --help
```

Demo mode uses the same command tree against `https://demo.netbox.dev/`:

```bash
nbx demo dcim devices list
nbx demo ipam prefixes list
nbx demo tui
nbx demo config         # show the active demo profile
nbx demo reset          # remove saved demo credentials
```

Supported action aliases:

- `list -> GET`
- `get -> GET` (requires `--id`)
- `create -> POST`
- `update -> PUT` (requires `--id`)
- `patch -> PATCH` (requires `--id`)
- `delete -> DELETE` (requires `--id`)

### 2) Explicit HTTP mode

```bash
nbx call GET /api/status/
nbx call POST /api/ipam/ip-addresses/ --body-file ./payload.json
```

### 3) Discovery helpers

```bash
nbx groups
nbx resources dcim
nbx ops dcim devices
```

### 4) Developer / workbench mode

```bash
nbx dev tui             # interactive request workbench (inspect requests, responses, timing)
nbx dev http GET /api/dcim/devices/
```

Demo profile variant:

```bash
nbx demo dev tui
```

### 5) Application logs

```bash
nbx logs                # view structured JSON application logs in a TUI log viewer
```

Logs are written to `~/.config/netbox-cli/logs/netbox-cli.log`.

### 6) Documentation capture

```bash
nbx docs generate-capture   # re-generate docs/generated/ from live CLI output
```

### 7) TUI mode

```bash
nbx tui
```

Theme options:

```bash
nbx tui --theme          # list available themes
nbx tui --theme dracula  # start with Dracula
nbx tui --theme netbox-light
```

You can also switch theme live from the top-left `Theme` dropdown in the TUI.

Theme contract:

- every Textual widget and subcomponent must inherit its visual styling from the active theme
- always inspect nested Textual internals recursively, not only the outer widget selector
- theme audits must include framework-owned component classes and wrappers such as `ContentTab`, `SelectCurrent` label/arrow, `SelectOverlay`, `.input--*`, `.option-list--*`, `.tree--*`, `.datatable--*`, `.text-area--*`, footer internals, and toast internals like `ToastRack`, `ToastHolder`, `Toast`, and `.toast--title`
- never hardcode runtime colors in Python or TCSS outside `netbox_cli/themes/*.json`
- do not opt into builtin Textual widget palettes when they override the repo theme tokens
- if a widget needs a custom state, express it with semantic variables and theme-backed component classes
- when a custom widget composes other Textual widgets internally, pass theme-aware intent through to those children and verify their rendered focus, hover, active, overlay, and ANSI states after a runtime theme switch

Textual composition contract:

- use React-style composition for Textual UI work: small reusable widgets, explicit constructor props, nested `compose()` trees
- prefer composition over inheritance for layout reuse
- extract shared primitives into `netbox_cli/ui/widgets.py`
- standard reusable controls should expose semantic arguments instead of ad-hoc class combinations
- pass theme-aware styling intent through semantic props such as `tone`, `surface`, and `size`

### Custom Themes (JSON)

Themes are loaded dynamically from:

- `netbox_cli/themes/`

Built-ins:

- `netbox_cli/themes/netbox-dark.json`
- `netbox_cli/themes/dracula.json`
- `netbox_cli/themes/netbox-light.json`

To add a custom theme, place `<theme>.json` in that folder. It will be auto-discovered.

Strict validation rules:

- required top-level keys: `name`, `label`, `dark`, `colors`
- optional keys: `variables`, `aliases`
- `colors` must define: `primary`, `secondary`, `warning`, `error`, `success`, `accent`, `background`, `surface`, `panel`, `boost`
- all color values must be `#RRGGBB`
- unknown keys, malformed colors, duplicate names, and alias conflicts fail fast with clear errors

TUI behavior (initial bootstrap):

- shell layout inspired by NetBox web UI:
  - top quick-search bar
  - left navigation tree (group -> resource)
  - main tabbed workspace (`Results`, `Details`) plus filter dialogs
  - footer status/help
- results view with incremental async refresh and row selection tracking
- details view rendered as panelized object attributes
- filters view with field picker + filter modal
- persisted last context/filter in local TUI state

Useful TUI keys:

- `/`: focus search
- `g`: focus navigation
- `s`: focus results table
- `r`: refresh current resource
- `f`: open filter modal
- `space`: toggle row selection
- `a`: toggle select all visible rows
- `d`: jump to details tab
- `q`: quit
- `Ctrl+G`: clear log viewer

## Project Layout

Core shared layer:

- `netbox_cli/config.py`: profile management + env overrides
- `netbox_cli/schema.py`: OpenAPI loading and indexing
- `netbox_cli/api.py`: async `aiohttp` client with token fallback
- `netbox_cli/http_cache.py`: filesystem HTTP cache (60 s fresh, 300 s stale-if-error)
- `netbox_cli/services.py`: request resolution and action mapping
- `netbox_cli/theme_registry.py`: JSON theme discovery and strict validation
- `netbox_cli/output_safety.py`: ANSI-escape and control-char sanitization
- `netbox_cli/trace_ascii.py`: cable trace ASCII renderer
- `netbox_cli/demo_auth.py`: Playwright-based demo.netbox.dev auth flow
- `netbox_cli/logging_runtime.py`: structured JSON logging setup
- `netbox_cli/docgen_capture.py` / `docgen_specs.py`: CLI-to-Markdown documentation pipeline

CLI subpackage (`netbox_cli/cli/`):

- `__init__.py`: root Typer app, static commands (`init`, `config`, `groups`, `resources`, `ops`, `call`, `logs`), subcommand wiring
- `runtime.py`: runtime config cache and async client factories
- `support.py`: Rich console output, table rendering, theme resolution
- `demo.py`: `nbx demo` profile management via Playwright
- `dev.py`: developer tools and request-workbench commands
- `dynamic.py`: OpenAPI-driven resource command routing

TUI subpackage (`netbox_cli/ui/`):

- `app.py`: main `NetBoxTuiApp` Textual application
- `dev_app.py`: request-workbench Textual app
- `chrome.py`: shared theme dropdown, logo, connection badge
- `navigation.py`: dynamic nav tree built from OpenAPI schema
- `nav_blueprint.py`: static NetBox navigation menu structure
- `panels.py`: `ObjectAttributesPanel` detail view with cable trace
- `filter_overlay.py`: filter modal mixin
- `formatting.py`: field humanization and semantic Rich Text styling
- `widgets.py`: shared composition primitives (buttons, headers, etc.)
- `state.py`: TUI state persistence (`~/.config/netbox-cli/tui_state.json`)
- `dev_state.py`: dev TUI state and request history
- `dev_rendering.py`: stateless Rich Text rendering for the dev TUI

Stylesheets:

- `netbox_cli/tui.tcss` / `netbox_cli/dev_tui.tcss`: app-level TCSS entry points
- `netbox_cli/ui_common.tcss`: shared visual design layer

Compatibility shims:

- `netbox_cli/tui.py`: re-export shim for `ui/app.py`
- `netbox_cli/dev_tui.py`: re-export shim for `ui/dev_app.py`

## Notes

`netbox-cli` mirrors NetBox UI workflows over a pure API layer, keeping CLI and TUI parity on top of the same shared execution layer. The CLI subpackage (`netbox_cli/cli/`) and TUI subpackage (`netbox_cli/ui/`) both consume the same `api.py` client and `schema.py` index — no model access, no direct DB connections.
