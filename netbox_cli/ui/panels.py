from __future__ import annotations

from typing import Any

from textual.containers import Vertical
from textual.timer import Timer
from textual.widgets import DataTable, Static

from .formatting import humanize_field, order_field_names, semantic_cell


class PanelCard(Vertical):
    """Simple card-like container with title and optional subtitle."""

    def __init__(self, title: str, subtitle: str = "", *, panel_id: str | None = None):
        super().__init__(id=panel_id)
        self._title_text = title
        self._subtitle_text = subtitle

    def compose(self):
        yield Static(self._title_text, classes="panel-title")
        if self._subtitle_text:
            yield Static(self._subtitle_text, classes="panel-subtitle")


def render_cable_trace_ascii(trace_payload: Any) -> str | None:
    if not isinstance(trace_payload, list) or not trace_payload:
        return None

    segments: list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for raw_segment in trace_payload:
        if not (
            isinstance(raw_segment, list)
            and len(raw_segment) == 3
            and isinstance(raw_segment[0], list)
            and isinstance(raw_segment[2], list)
            and raw_segment[0]
            and raw_segment[2]
            and isinstance(raw_segment[0][0], dict)
            and isinstance(raw_segment[1], dict)
            and isinstance(raw_segment[2][0], dict)
        ):
            continue
        segments.append((raw_segment[0][0], raw_segment[1], raw_segment[2][0]))

    if not segments:
        return None

    def _endpoint_lines(endpoint: dict[str, Any], *, device_first: bool) -> list[str]:
        device = endpoint.get("device")
        device_label = (
            str(device.get("display") or device.get("name"))
            if isinstance(device, dict)
            else ""
        )
        port_label = str(endpoint.get("display") or endpoint.get("name") or "Endpoint")
        if device_first:
            return [line for line in [device_label, port_label] if line]
        return [line for line in [port_label, device_label] if line]

    def _box(lines: list[str], width: int = 38) -> list[str]:
        inner_width = width - 2
        rendered = ["┌" + "─" * inner_width + "┐"]
        for line in lines:
            rendered.append(
                "│" + line.center(inner_width)[:inner_width].ljust(inner_width) + "│"
            )
        rendered.append("└" + "─" * inner_width + "┘")
        return rendered

    result: list[str] = []
    first_near, _, _ = segments[0]
    result.extend(_box(_endpoint_lines(first_near, device_first=True)))

    for index, (near, cable, far) in enumerate(segments):
        if index > 0:
            result.extend(_box(_endpoint_lines(near, device_first=False)))
        cable_label = str(cable.get("display") or cable.get("label") or "Cable")
        cable_status = str(cable.get("status") or "connected").title()
        center = " " * 16
        result.extend(
            [
                center + "│",
                center + f"│  {cable_label}",
                center + f"│  {cable_status}",
                center + "│",
            ]
        )
        result.extend(_box(_endpoint_lines(far, device_first=False)))

    result.append("")
    result.append(f"Trace Completed - {len(segments)} segment(s)")
    return "\n".join(result)


class ObjectAttributesPanel(PanelCard):
    """Render selected row data as key/value attributes."""

    def __init__(self, *, panel_id: str = "detail_panel"):
        super().__init__(
            "Object Attributes", "NetBox detail-style panel", panel_id=panel_id
        )
        self._spinner_frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self._spinner_index = 0
        self._spinner_timer: Timer | None = None
        self._row_values: list[tuple[str, Any]] = []

    def compose(self):
        yield from super().compose()
        yield Static("Ready", id="detail_status")
        table = DataTable(id="detail_table")
        table.cursor_type = "cell"
        table.add_columns("Field", "Value")
        table.add_row("status", "Select a row in Results tab")
        yield table
        yield Static("Cable Trace", id="detail_trace_title", classes="hidden")
        yield Static("", id="detail_trace", classes="hidden")

    def _set_status(self, text: str) -> None:
        self.query_one("#detail_status", Static).update(text)

    def _stop_spinner(self) -> None:
        if self._spinner_timer is not None:
            self._spinner_timer.stop()
            self._spinner_timer = None

    def _spinner_tick(self, label: str) -> None:
        frame = self._spinner_frames[self._spinner_index % len(self._spinner_frames)]
        self._spinner_index += 1
        self._set_status(f"{frame} {label}")

    def set_loading(self, label: str = "Loading object details...") -> None:
        self._stop_spinner()
        self._spinner_index = 0
        self._row_values = []
        self._spinner_tick(label)
        self._spinner_timer = self.set_interval(0.12, lambda: self._spinner_tick(label))
        self.add_class("-loading")  # CSS state machine: drives teal status color

        table = self.query_one("#detail_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Field", "Value")
        table.add_row("status", "Loading...")
        self.set_trace(None)

    def set_object(self, obj: dict[str, Any] | None) -> None:
        self._stop_spinner()
        self.remove_class("-loading")  # Clear CSS loading state
        self._row_values = []
        table = self.query_one("#detail_table", DataTable)
        table.clear(columns=True)
        table.add_columns("Field", "Value")

        if not obj:
            self._set_status("No object selected")
            table.add_row("status", "No object selected")
            self.set_trace(None)
            return

        self._set_status("Loaded")
        ordered = order_field_names([str(key) for key in obj.keys()])
        for key in ordered:
            raw_value = obj.get(key)
            field = humanize_field(str(key))
            self._row_values.append((field, raw_value))
            table.add_row(field, semantic_cell(str(key), raw_value, max_len=500))

    def set_trace(self, trace_payload: Any | None) -> None:
        title = self.query_one("#detail_trace_title", Static)
        trace = self.query_one("#detail_trace", Static)
        if trace_payload is None:
            title.add_class("hidden")
            trace.add_class("hidden")
            trace.update("")
            return

        rendered = (
            trace_payload
            if isinstance(trace_payload, str)
            else render_cable_trace_ascii(trace_payload)
        )
        if not rendered:
            title.add_class("hidden")
            trace.add_class("hidden")
            trace.update("")
            return

        title.remove_class("hidden")
        trace.remove_class("hidden")
        trace.update(rendered)

    def detail_value_at(self, row_index: int) -> Any | None:
        if row_index < 0 or row_index >= len(self._row_values):
            return None
        return self._row_values[row_index][1]
