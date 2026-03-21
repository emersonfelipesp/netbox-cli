# reference — Design and Framework References

Read-only reference material for guiding TUI visual design and Textual framework usage. **No code lives here.** These files are consulted before making any UI/styling changes.

## Contents

### `design/` — Visual Design Guides

| File | Priority | Purpose |
|---|---|---|
| `NETBOX-DARK-PATTERNS.md` | **1 (highest)** | NetBox dark mode color palette, layer hierarchy, component styles, status colors |
| `TOAD-DESIGN-GUIDE.md` | 2 | Textual idiomatic design patterns (TCSS patterns, spacing, borders, states, animations) |

**Rule:** When these two guides conflict on the same visual aspect, `NETBOX-DARK-PATTERNS.md` wins.

**When to consult:**
- Before any change to `tui.tcss`
- Before adding new widgets or changing widget borders/colors/spacing
- When implementing new status indicators, badges, or state colors
- When choosing layout primitives (`layout: grid` vs `layout: stream` etc.)

### `textual/` — Textual App References

Annotated source / documentation extracts from real-world Textual apps, used to understand idiomatic Textual patterns:

| File | Source |
|---|---|
| `TEXTUAL.md` | Official Textual framework documentation |
| `TOAD.md` | Toad — most advanced idiomatic Textual app |
| `DOLPHIE.md` | Dolphie — MySQL TUI |
| `MEMRAY.md` | Memray — memory profiling TUI |
| `POSTING.md` | Posting — HTTP client TUI |
| `TOOLONG.md` | Toolong — log viewer TUI |
| `NMS-CLI.md` | nms-cli — prior art for this project |
| `CLAUDE.md` | Claude-specific Textual guidance |

**When to consult:** Before implementing new Textual patterns, especially: `@work` usage, `Pilot` testing, reactive attributes, CSS selectors, `on_*` message handlers, `compose()` patterns.

### `openapi/` — NetBox OpenAPI Schema (symlink / copy)

These may be copies of or symlinks to `netbox_cli/reference/openapi/`. The canonical bundled schema used at runtime is in `netbox_cli/reference/openapi/`. See [`netbox_cli/reference/CLAUDE.md`](../netbox_cli/reference/CLAUDE.md) for details.
