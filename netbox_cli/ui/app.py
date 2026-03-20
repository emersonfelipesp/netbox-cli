from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.css.query import NoMatches
from textual.screen import ModalScreen
from textual.theme import Theme
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, ListItem, ListView, Static, TabbedContent, TabPane, Tree

# NetBox dark mode palette mapped to Textual semantic tokens.
# Source: reference/design/NETBOX-DARK-PATTERNS.md (higher priority)
NETBOX_DARK = Theme(
    name="netbox-dark",
    dark=True,
    primary="#00F2D4",       # bright-teal — links, active nav, focus rings
    secondary="#00857D",     # dark-teal — secondary accent
    warning="#F59F00",       # NetBox warning
    error="#D63939",         # NetBox danger/error
    success="#2FB344",       # NetBox success/connected
    accent="#00F2D4",        # same as primary
    background="#001423",    # rich-black — outermost: html, navbar, cards
    surface="#081B2A",       # rich-black-light — page content area
    panel="#18212F",         # surface-tertiary — card headers, nested panels
    boost="#1F2937",         # gray-800 — elevated surfaces, dropdowns
    variables={
        # NetBox status badge colors (text on dark bg)
        "nb-success-text":   "#82D18E",
        "nb-info-text":      "#8DC1ED",
        "nb-warning-text":   "#F9C566",
        "nb-danger-text":    "#E68888",
        "nb-secondary-text": "#A6AAB2",
        # NetBox subtle status backgrounds
        "nb-success-bg":     "#09230D",
        "nb-info-bg":        "#0D1E2D",
        "nb-warning-bg":     "#311F00",
        "nb-danger-bg":      "#2B0B0B",
        "nb-secondary-bg":   "#151720",
        # NetBox border tones
        "nb-border":         "#2D3C51",
        "nb-border-subtle":  "#374151",
    },
)

from netbox_cli.api import NetBoxApiClient
from netbox_cli.schema import SchemaIndex

from .formatting import (
    humanize_field,
    humanize_group,
    humanize_resource,
    order_field_names,
    parse_response_rows,
    semantic_cell,
)
from .navigation import build_navigation_menus
from .panels import ObjectAttributesPanel
from .state import TuiState, ViewState, load_tui_state, save_tui_state


class FilterFieldItem(ListItem):
    def __init__(self, field_name: str, field_label: str):
        super().__init__(Label(field_label))
        self.field_name = field_name


class FilterModal(ModalScreen[tuple[str, str] | None]):
    BINDINGS = [Binding("escape", "cancel", "Cancel", show=False)]

    def __init__(self, default_key: str = ""):
        super().__init__()
        self.default_key = default_key

    def compose(self) -> ComposeResult:
        with Vertical(id="filter_dialog"):
            yield Static("Apply Filter", classes="panel-title")
            yield Input(value=self.default_key, placeholder="Field (example: name)", id="filter_key")
            yield Input(placeholder="Value", id="filter_value")
            with Horizontal(id="filter_buttons"):
                yield Button("Apply", id="apply", variant="primary")
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#filter_value", Input).focus()

    @on(Button.Pressed, "#apply")
    def on_apply(self) -> None:
        key = self.query_one("#filter_key", Input).value.strip()
        value = self.query_one("#filter_value", Input).value.strip()
        if not key:
            self.app.notify("Field is required", severity="warning")
            return
        self.dismiss((key, value))

    @on(Button.Pressed, "#cancel")
    def on_cancel_button(self) -> None:
        self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class NetBoxTuiApp(App[None]):
    TITLE = "NetBox CLI"
    SUB_TITLE = "NetBox UI-style shell for terminal"
    CSS_PATH = "../tui.tcss"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("/", "focus_search", "Search"),
        Binding("g", "focus_navigation", "Navigation"),
        Binding("s", "focus_results", "Results"),
        Binding("r", "refresh", "Refresh"),
        Binding("f", "filter_modal", "Filter"),
        Binding("space", "toggle_select", "Toggle Row"),
        Binding("a", "toggle_select_all", "Select All"),
        Binding("d", "show_details", "Details"),
    ]

    def __init__(self, client: NetBoxApiClient, index: SchemaIndex):
        super().__init__()
        self.client = client
        self.index = index
        self.state: TuiState = load_tui_state()

        self.current_group: str | None = self.state.last_view.group
        self.current_resource: str | None = self.state.last_view.resource
        self.current_rows: list[dict[str, Any]] = []
        self.selected_row_ids: set[str] = set()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="topbar"):
            yield Input(
                value=self.state.last_view.query_text,
                id="global_search",
                placeholder="Quick search: plain text -> q=<text>, or key=value",
            )
            yield Static("Context: <none>", id="context_line")
            yield Button("Close", id="close_tui_button")

        with Horizontal(id="shell"):
            with Vertical(id="sidebar"):
                yield Static("Navigation", id="nav_title")
                yield Tree("NetBox", id="nav_tree")
                yield Static("/ search | g nav | s results | f filter | d details", id="nav_help")

            with Vertical(id="main"):
                with TabbedContent(id="main_tabs"):
                    with TabPane("Results", id="results_tab"):
                        yield Static("Select a resource from Navigation", id="results_controls")
                        table = DataTable(id="results_table")
                        table.cursor_type = "row"
                        table.add_columns("sel", "result")
                        table.add_row("", "No data loaded")
                        yield table
                        yield Static("Ready", id="results_status")

                    with TabPane("Details", id="details_tab"):
                        yield ObjectAttributesPanel(panel_id="detail_panel")

                    with TabPane("Filters", id="filters_tab"):
                        yield Static("Select a field and press Enter to apply a filter", id="filters_help")
                        yield ListView(id="filters_list")

        yield Footer()

    def on_load(self) -> None:
        self.register_theme(NETBOX_DARK)
        self.theme = "netbox-dark"

    def on_mount(self) -> None:
        self._build_navigation_tree()
        self._update_context_line()
        self._sync_search_input()
        self.query_one("#nav_tree", Tree).focus()
        self._restore_last_view_if_any()

    def on_unmount(self) -> None:
        query_text = self.state.last_view.query_text
        try:
            query_text = self.query_one("#global_search", Input).value.strip()
        except NoMatches:
            # During teardown the widget tree may already be gone.
            pass
        self.state.last_view = ViewState(
            group=self.current_group,
            resource=self.current_resource,
            query_text=query_text,
            details_expanded=False,
        )
        save_tui_state(self.state)

    def action_focus_search(self) -> None:
        self.query_one("#global_search", Input).focus()

    def action_focus_navigation(self) -> None:
        self.query_one("#nav_tree", Tree).focus()

    def action_focus_results(self) -> None:
        self.query_one("#results_table", DataTable).focus()

    def action_refresh(self) -> None:
        if self.current_group and self.current_resource:
            self._load_rows(self.current_group, self.current_resource)

    def action_filter_modal(self) -> None:
        default_key = ""
        focused = self.query_one("#filters_list", ListView).highlighted_child
        if isinstance(focused, FilterFieldItem):
            default_key = focused.field_name

        self._open_filter_modal(default_key)

    def action_show_details(self) -> None:
        tabs = self.query_one("#main_tabs", TabbedContent)
        tabs.active = "details_tab"

    def action_toggle_select(self) -> None:
        table = self.query_one("#results_table", DataTable)
        row_index = table.cursor_row
        if row_index is None or row_index < 0 or row_index >= len(self.current_rows):
            return

        row_id = self._row_identity(self.current_rows[row_index], row_index)
        if row_id in self.selected_row_ids:
            self.selected_row_ids.remove(row_id)
        else:
            self.selected_row_ids.add(row_id)

        self._render_results_table(self.current_rows)
        self._set_status(f"Selected {len(self.selected_row_ids)} row(s)")

    def action_toggle_select_all(self) -> None:
        if not self.current_rows:
            return
        all_ids = {self._row_identity(row, idx) for idx, row in enumerate(self.current_rows)}
        if self.selected_row_ids == all_ids:
            self.selected_row_ids.clear()
        else:
            self.selected_row_ids = set(all_ids)

        self._render_results_table(self.current_rows)
        self._set_status(f"Selected {len(self.selected_row_ids)} row(s)")

    @on(Input.Submitted, "#global_search")
    def on_search_submit(self) -> None:
        if self.current_group and self.current_resource:
            self._load_rows(self.current_group, self.current_resource)

    @on(Button.Pressed, "#close_tui_button")
    def on_close_pressed(self) -> None:
        self.exit()

    @on(Tree.NodeSelected, "#nav_tree")
    def on_nav_selected(self, event: Tree.NodeSelected[tuple[str, str] | None]) -> None:
        if event.node.data is None:
            if not event.node.children:
                self._set_status("No API endpoint is available for this menu item in TUI")
            return

        group, resource = event.node.data
        self.current_group = group
        self.current_resource = resource
        self.selected_row_ids.clear()
        self._update_context_line()
        self._set_controls(f"Resource: {humanize_group(group)} / {humanize_resource(resource)}")
        self._load_rows(group, resource)

    @on(DataTable.RowSelected, "#results_table")
    def on_row_selected(self) -> None:
        table = self.query_one("#results_table", DataTable)
        row_index = table.cursor_row
        if row_index is None or row_index < 0 or row_index >= len(self.current_rows):
            self.query_one("#detail_panel", ObjectAttributesPanel).set_object(None)
            return

        selected = self.current_rows[row_index]
        self._load_object_details(selected)
        self._refresh_filter_fields(selected.keys())
        tabs = self.query_one("#main_tabs", TabbedContent)
        tabs.active = "details_tab"

    @on(ListView.Selected, "#filters_list")
    def on_filter_field_selected(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, FilterFieldItem):
            return
        self._open_filter_modal(event.item.field_name)

    def _open_filter_modal(self, default_key: str) -> None:
        self.push_screen(FilterModal(default_key=default_key), self._on_filter_modal_result)

    def _on_filter_modal_result(self, result: tuple[str, str] | None) -> None:
        if not result:
            return
        key, value = result
        self.query_one("#global_search", Input).value = f"{key}={value}"
        if self.current_group and self.current_resource:
            self._load_rows(self.current_group, self.current_resource)

    @work(group="list_refresh", exclusive=True, thread=False)
    async def _load_rows(self, group: str, resource: str) -> None:
        paths = self.index.resource_paths(group, resource)
        if paths is None or paths.list_path is None:
            self.current_rows = []
            self._render_results_table([])
            self._set_status("List endpoint unavailable for this resource")
            return

        query = self._query_from_search(self.query_one("#global_search", Input).value.strip())
        self._set_status(f"Loading {group}/{resource}...")

        try:
            response = await self.client.request("GET", paths.list_path, query=query)
        except Exception as exc:  # noqa: BLE001
            self.current_rows = []
            self._render_results_table([])
            self._set_status(f"Request failed: {exc}")
            return

        rows = parse_response_rows(response.text)
        self.current_rows = rows
        self._prune_selection()
        self._render_results_table(rows)

        if rows:
            self._load_object_details(rows[0])
            self._refresh_filter_fields(rows[0].keys())
        else:
            self.query_one("#detail_panel", ObjectAttributesPanel).set_object(None)
            self._refresh_filter_fields([])

        if response.status >= 400:
            self.notify(f"HTTP {response.status}", severity="error")
            self._set_status(f"HTTP {response.status}")
        else:
            self._set_status(f"Loaded {len(rows)} row(s) - HTTP {response.status}")

    @work(group="detail_refresh", exclusive=True, thread=False)
    async def _load_object_details(self, row: dict[str, Any]) -> None:
        panel = self.query_one("#detail_panel", ObjectAttributesPanel)
        panel.set_loading("Loading object details...")

        group = self.current_group
        resource = self.current_resource
        if not group or not resource:
            panel.set_object(row)
            return

        object_id = row.get("id")
        if object_id is None:
            panel.set_object(row)
            return

        paths = self.index.resource_paths(group, resource)
        if paths is None or paths.detail_path is None:
            panel.set_object(row)
            return

        detail_path = paths.detail_path.replace("{id}", str(object_id))
        try:
            response = await self.client.request("GET", detail_path)
        except Exception as exc:  # noqa: BLE001
            panel.set_object(row)
            self.notify(f"Detail request failed: {exc}", severity="error")
            return

        if response.status >= 400:
            panel.set_object(row)
            self.notify(f"HTTP {response.status} while loading details", severity="warning")
            return

        parsed = parse_response_rows(response.text)
        if not parsed:
            panel.set_object(row)
            return

        # detail endpoint returns one object; keep first object entry
        panel.set_object(parsed[0])

    def _build_navigation_tree(self) -> None:
        tree = self.query_one("#nav_tree", Tree)
        tree.clear()
        root = tree.root
        root.expand()
        for menu in build_navigation_menus(self.index):
            menu_node = root.add(menu.label)
            menu_node.expand()
            for group in menu.groups:
                group_node = menu_node.add(group.label)
                group_node.expand()
                for item in group.items:
                    data = (item.group, item.resource) if item.group and item.resource else None
                    group_node.add_leaf(item.label, data=data)

    def _restore_last_view_if_any(self) -> None:
        group = self.state.last_view.group
        resource = self.state.last_view.resource
        if not group or not resource:
            return
        if resource not in self.index.resources(group):
            return

        self.current_group = group
        self.current_resource = resource
        self._update_context_line()
        self._set_controls(f"Resource: {humanize_group(group)} / {humanize_resource(resource)}")
        self._load_rows(group, resource)

    def _sync_search_input(self) -> None:
        self.query_one("#global_search", Input).value = self.state.last_view.query_text

    def _update_context_line(self) -> None:
        target = self.query_one("#context_line", Static)
        if self.current_group and self.current_resource:
            target.update(
                f"Context: {humanize_group(self.current_group)} / {humanize_resource(self.current_resource)}"
            )
        else:
            target.update("Context: <none>")

    def _set_controls(self, text: str) -> None:
        self.query_one("#results_controls", Static).update(text)

    def _set_status(self, text: str) -> None:
        self.query_one("#results_status", Static).update(text)

    def _query_from_search(self, raw: str) -> dict[str, str]:
        raw = raw.strip()
        if not raw:
            return {}

        parsed: dict[str, str] = {}
        if "=" not in raw:
            return {"q": raw}

        chunks = [part.strip() for part in raw.split(",") if part.strip()]
        for chunk in chunks:
            if "=" not in chunk:
                return {"q": raw}
            key, value = chunk.split("=", 1)
            key = key.strip()
            if not key:
                continue
            parsed[key] = value

        return parsed or {"q": raw}

    def _prune_selection(self) -> None:
        valid_ids = {self._row_identity(row, idx) for idx, row in enumerate(self.current_rows)}
        self.selected_row_ids &= valid_ids

    def _render_results_table(self, rows: list[dict[str, Any]]) -> None:
        table = self.query_one("#results_table", DataTable)
        table.clear(columns=True)

        if not rows:
            table.add_columns("sel", "result")
            table.add_row("", "No results")
            return

        columns = ["sel"]
        discovered: list[str] = []
        for row in rows:
            for key in row:
                name = str(key)
                if name not in discovered:
                    discovered.append(name)
        discovered = order_field_names(discovered)
        columns.extend(humanize_field(name) for name in discovered)

        table.add_columns(*columns)

        for idx, row in enumerate(rows):
            row_id = self._row_identity(row, idx)
            marker = "●" if row_id in self.selected_row_ids else ""
            values = [marker]
            values.extend(semantic_cell(col, row.get(col)) for col in discovered)
            table.add_row(*values)

    def _row_identity(self, row: dict[str, Any], index: int) -> str:
        if "id" in row and row["id"] is not None:
            return str(row["id"])
        return f"row:{index}"

    def _refresh_filter_fields(self, fields: Iterable[str]) -> None:
        list_view = self.query_one("#filters_list", ListView)
        list_view.clear()

        seen: set[str] = set()
        for name in fields:
            key = str(name)
            if key in seen:
                continue
            seen.add(key)
        for key in order_field_names(list(seen)):
            list_view.append(FilterFieldItem(key, humanize_field(key)))


def run_tui(client: NetBoxApiClient, index: SchemaIndex) -> None:
    NetBoxTuiApp(client=client, index=index).run()
