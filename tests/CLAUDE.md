# tests — Test Suite

pytest + pytest-asyncio. All tests live here; there are no inline tests in the source package.

**Run all tests:**
```bash
pytest
```

**Async mode:** `asyncio_mode = "auto"` (set in `pyproject.toml`) — every `async def test_*` runs automatically under an event loop without needing `@pytest.mark.asyncio`.

---

## Test Files

| File | What it covers |
|---|---|
| `test_api_auth.py` | Authorization header generation, config completeness, URL validation, v2→v1 token fallback |
| `test_api_cache.py` | Cache TTL policies, stale-if-error, ETag/Last-Modified conditional requests |
| `test_cli_trace.py` | Cable trace ASCII rendering (Unicode boxes, endpoint labels, status, cable segments) |
| `test_cli_tui_theme.py` | TUI theme selection, live switching, persistence via `tui_state.json` |
| `test_config_profiles.py` | Profile save/load, legacy flat-config migration, file permissions (0o700/0o600) |
| `test_demo_auth.py` | Playwright demo.netbox.dev automation validation and token provisioning |
| `test_demo_cli.py` | Demo profile CLI commands; live API calls when `DEMO_USERNAME`/`DEMO_PASSWORD` are set |
| `test_no_hardcoded_colors.py` | Enforces that `tui.tcss` uses only CSS variables — **zero hex colors allowed** |
| `test_output_safety.py` | ANSI stripping, control character replacement, safe Rich Text rendering |
| `test_schema_index.py` | Group/resource extraction, list/detail path identification, trace path support |
| `test_services.py` | Request resolution from (group, resource, action, id) tuples, key-value arg parsing |
| `test_theme_registry.py` | Theme JSON loading, `#RRGGBB` format enforcement, required variable keys, alias conflicts |
| `test_tui_interaction.py` | Textual `Pilot` integration tests: navigation, filtering, detail panel, cable trace display |

---

## Patterns

### Mocking the API client
Most tests that touch `NetBoxApiClient` inject a mock via `monkeypatch` or a fixture that replaces `aiohttp.ClientSession`. Never mock at the HTTP level inside `test_tui_interaction.py` — use the `NetBoxApiClient` mock boundary instead.

### Live tests (skip if secrets absent)
`test_demo_cli.py` and `test_demo_auth.py` check for `DEMO_USERNAME` / `DEMO_PASSWORD` environment variables and skip gracefully when absent. CI sets these from repository secrets.

### Filesystem isolation
Tests that write to `~/.config/netbox-cli/` use `tmp_path` (pytest fixture) and patch the config directory to a temporary location so they never pollute the developer's real config.

### TCSS color test
`test_no_hardcoded_colors.py` reads `tui.tcss` as text and asserts no `#` hex literals appear — this enforces the semantic-variable-only rule from the design guide.
