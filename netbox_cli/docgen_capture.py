"""Generate Markdown + JSON capturing ``nbx`` CLI invocations (Typer CliRunner).

Documentation guidelines (AGENTS):
- All captured output MUST come from demo.netbox.dev only.  Never use a
  production instance to generate docs — it will leak customer data.
- Commands documented without the ``demo`` prefix (e.g. ``nbx dcim devices
  list``) must still execute against the demo profile.
- Commands that fail with configuration errors (interactive prompts, aborted)
  are skipped and never included in final output.
- Each command gets tabs: Command, Output (human), JSON Output, YAML Output,
  Markdown Output.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import UTC, datetime
from inspect import signature
from pathlib import Path
from typing import Any, TextIO

from .docgen_specs import all_specs as _all_specs

# OpenAPI dynamic actions that render via ``print_response`` (tabular / Markdown-friendly).
_MARKDOWN_ACTIONS = frozenset({"list", "get", "create", "update", "patch", "delete"})
_OUTPUT_FORMAT_FLAGS = frozenset({"--json", "--yaml", "--markdown"})

# Strings that indicate a command failed because configuration is missing.
_CONFIG_ERROR_SIGNALS = (
    "NetBox endpoint configuration is required",
    "NetBox host (example:",
    "Aborted.",
)

# Header line prepended by ``print_response`` (stripped from format-variant captures).
_STATUS_HEADER_RE = re.compile(r"^Status:\s*\d+\s*\n?")


def argv_with_markdown_output(argv: list[str], *, enabled: bool) -> list[str]:
    """Return argv, appending ``--markdown`` when doc capture should use Markdown tables.

    Skips ``--help``, leaves argv unchanged when ``--json`` / ``--yaml`` / ``--markdown``
    is already present, and only targets ``call`` plus dynamic
    ``[<demo>] <group> <resource> <action>`` invocations.
    """
    if not enabled:
        return list(argv)
    if "--help" in argv:
        return list(argv)
    if any(t in _OUTPUT_FORMAT_FLAGS for t in argv):
        return list(argv)

    opt_idx = next((i for i, t in enumerate(argv) if t.startswith("-")), len(argv))
    pos = argv[:opt_idx]
    if not pos:
        return list(argv)

    if pos[0] == "call" and len(pos) >= 3:
        return [*argv, "--markdown"]

    body = pos[1:] if pos[0] == "demo" else pos
    if len(body) >= 3 and body[-1] in _MARKDOWN_ACTIONS:
        return [*argv, "--markdown"]

    return list(argv)


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_capture_paths(
    output: Path | None,
    raw_dir: Path | None,
) -> tuple[Path, Path]:
    """Default under ``<repo>/docs/generated/`` when the repo layout is present."""
    docs_dir = _repo_root() / "docs"
    default_out = docs_dir / "generated" / "nbx-command-capture.md"
    if not docs_dir.is_dir():
        if output is None or raw_dir is None:
            raise FileNotFoundError(
                "Cannot infer default paths: no docs/ directory next to netbox_cli. "
                "Run from the netbox-cli git checkout or pass --output and --raw-dir."
            )
        return output, raw_dir
    if output is None:
        output = default_out
    if raw_dir is None:
        raw_dir = output.parent / "raw"
    return output, raw_dir


def _inject_stub_config(profile: str) -> bool:
    """Ensure ``cli._RUNTIME_CONFIGS[profile]`` is populated before CliRunner invocations.

    If a complete config already exists on disk for this profile it is loaded into the
    in-process cache (so commands don't re-read disk on every spec) and ``False`` is
    returned — meaning the caller should *not* clear the cache afterwards.

    If no real config exists, a placeholder stub is injected so that live-API specs
    produce a 401/403 response instead of triggering interactive prompts.  ``True`` is
    returned so the caller knows to clear the injected entry after the invocation.
    """
    from netbox_cli import cli as cli_mod
    from netbox_cli.config import (
        DEMO_BASE_URL,
        Config,
        is_runtime_config_complete,
        load_profile_config,
        normalize_base_url,
    )

    existing = load_profile_config(profile)
    if is_runtime_config_complete(existing):
        cli_mod._RUNTIME_CONFIGS[profile] = existing
        return False  # real config loaded — caller must not clear it

    # No real config — inject a placeholder so live calls fail gracefully.
    if profile == "demo":
        base_url = DEMO_BASE_URL
    else:
        raw = os.environ.get("NETBOX_URL", "https://netbox.example.com").strip()
        base_url = normalize_base_url(raw)

    token_key = os.environ.get("NETBOX_TOKEN_KEY", "docgen-placeholder").strip()
    token_secret = os.environ.get("NETBOX_TOKEN_SECRET", "placeholder").strip()
    timeout = float(os.environ.get("NBX_DOC_CAPTURE_TIMEOUT", "30"))
    cli_mod._RUNTIME_CONFIGS[profile] = Config(
        base_url=base_url,
        token_key=token_key,
        token_secret=token_secret,
        timeout=timeout,
    )
    return True  # stub injected — caller must clear it afterwards


def _clear_stub_config(profile: str) -> None:
    from netbox_cli import cli as cli_mod

    cli_mod._RUNTIME_CONFIGS.pop(profile, None)


def _truncate(text: str, max_lines: int, max_chars: int) -> tuple[str, bool]:
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n… (truncated by character limit)\n"
        return text, True
    lines = text.splitlines()
    if len(lines) > max_lines:
        head = "\n".join(lines[:max_lines])
        return head + f"\n\n… ({len(lines) - max_lines} more lines truncated)\n", True
    return text, False


def _strip_status_header(text: str) -> str:
    """Remove the ``Status: NNN`` header line added by ``print_response``."""
    return _STATUS_HEADER_RE.sub("", text, count=1)


def _is_config_error(output: str) -> bool:
    """Return True if the captured output indicates a missing configuration."""
    return any(sig in output for sig in _CONFIG_ERROR_SIGNALS)


def _has_output_format_support(argv: list[str]) -> bool:
    """Return True if the command accepts ``--json``/``--yaml``/``--markdown`` flags.

    Help-only commands and schema-discovery commands do not benefit from
    format variants — only live API calls and dynamic commands do.
    """
    if "--help" in argv:
        return False
    if any(t in _OUTPUT_FORMAT_FLAGS for t in argv):
        return False
    # Static local commands (groups, resources, ops, config) are plain text.
    local_commands = {"groups", "resources", "ops", "config", "logs", "init"}
    if argv and argv[0] in local_commands:
        return False
    return True


def _inject_format_variant(argv: list[str], flag: str) -> list[str]:
    """Return a copy of *argv* with *flag* appended (or replacing an existing format flag)."""
    clean = [a for a in argv if a not in _OUTPUT_FORMAT_FLAGS]
    return [*clean, flag]


def _make_cli_runner() -> Any:
    from typer.testing import CliRunner

    if "mix_stderr" in signature(CliRunner).parameters:
        return CliRunner(mix_stderr=False)
    return CliRunner()


def _run_capture(
    argv: list[str],
    app: Any,
    *,
    profile: str,
    safe: bool,
) -> tuple[int, str, float]:
    was_stub = _inject_stub_config(profile)
    try:
        runner = _make_cli_runner()
        started = time.perf_counter()
        result = runner.invoke(
            app,
            argv,
            catch_exceptions=not safe,
            color=False,
        )
        elapsed = time.perf_counter() - started
        out = result.stdout or ""
        err = getattr(result, "stderr", "") or ""
        if err.strip():
            out = f"{out}\n--- stderr ---\n{err}" if out.strip() else f"--- stderr ---\n{err}"
        # Surface captured exceptions (catch_exceptions=True path) as readable text.
        if result.exception is not None and not isinstance(result.exception, SystemExit):
            import traceback

            tb = "".join(
                traceback.format_exception(
                    type(result.exception),
                    result.exception,
                    result.exception.__traceback__,
                )
            )
            out = f"{out}\n--- exception ---\n{tb}" if out.strip() else f"--- exception ---\n{tb}"
        return result.exit_code or 0, out, elapsed
    finally:
        if was_stub:
            _clear_stub_config(profile)


def generate_command_capture_docs(
    *,
    output: Path,
    raw_dir: Path,
    max_lines: int = 200,
    max_chars: int = 120_000,
    use_demo: bool = True,
    markdown_output: bool = True,
    log: TextIO | None = None,
) -> int:
    """Write capture Markdown and raw JSON artifacts. Returns 0 on success."""
    log = log or sys.stderr
    from netbox_cli.cli import app as cli_app
    from netbox_cli.config import DEFAULT_PROFILE, DEMO_PROFILE

    profile = DEMO_PROFILE if use_demo else DEFAULT_PROFILE

    output.parent.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Determine effective base_url for the chosen profile for metadata display.
    from netbox_cli.config import DEMO_BASE_URL, load_profile_config

    cfg = load_profile_config(profile)
    effective_url = cfg.base_url or (
        DEMO_BASE_URL if use_demo else os.environ.get("NETBOX_URL", "https://netbox.example.com")
    )
    token_configured = bool(cfg.token_key and cfg.token_secret)

    meta = {
        "generated_at": datetime.now(UTC).isoformat(),
        "profile": profile,
        "netbox_url": effective_url,
        "timeout": os.environ.get("NBX_DOC_CAPTURE_TIMEOUT", "30"),
        "token_configured": token_configured,
        "markdown_output": markdown_output,
    }

    profile_note = (
        "**demo profile** (`nbx demo …` commands → demo.netbox.dev)"
        if use_demo
        else "**default profile** (`nbx …` commands → your configured NetBox)"
    )

    lines: list[str] = [
        "# NetBox CLI — captured command input and output",
        "",
        "This file is **machine-generated**. Regenerate with:",
        "",
        "```bash",
        "cd /path/to/netbox-cli",
        "uv sync --group docs --group dev   # once",
        "uv run nbx docs generate-capture            # demo profile (default)",
        "uv run nbx docs generate-capture --live     # default profile (real NetBox)",
        "# or: uv run python docs/generate_command_docs.py",
        "```",
        "",
        "Run the capture **in the background** (log + pid):",
        "",
        "```bash",
        "./docs/run_capture_in_background.sh",
        "```",
        "",
        "## Generation metadata",
        "",
        f"- **UTC time:** `{meta['generated_at']}`",
        f"- **Profile used:** {profile_note}",
        f"- **Effective NetBox URL:** `{meta['netbox_url']}`",
        f"- **Effective timeout (s):** `{meta['timeout']}`",
        f"- **Token configured:** `{meta['token_configured']}`",
        "",
        (
            "> Live API calls reflect whatever is reachable at the configured URL. "
            "Connection errors and 401/403 responses are still useful documentation "
            "of real CLI behavior."
        ),
        "",
        (
            "> **Typer `CliRunner` quirk:** help banners may show `Usage: root` instead of "
            "`Usage: nbx`. The installed `nbx` script uses the correct name."
        ),
        "",
        "---",
        "",
    ]

    section_last = ""
    artifacts: list[dict] = []
    skipped: list[str] = []

    for spec in _all_specs(use_demo=use_demo):
        if spec.section != section_last:
            lines.append(f"## {spec.section}")
            lines.append("")
            section_last = spec.section

        run_argv = argv_with_markdown_output(spec.argv, enabled=markdown_output)
        cmd_display = "nbx " + " ".join(run_argv)
        code, out, elapsed = _run_capture(run_argv, cli_app, profile=profile, safe=spec.safe)

        # ── Skip commands that failed due to missing configuration ────────────
        if _is_config_error(out):
            skipped.append(spec.title)
            print(f"  SKIPPED (config error): {spec.title}", file=log)
            continue

        truncated, did_trunc = _truncate(out, max_lines, max_chars)
        slug = f"{spec.section}-{spec.title}"[:80].lower().replace(" ", "-").replace("/", "-")
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
        while "--" in slug:
            slug = slug.replace("--", "-")

        # ── Capture format variants (JSON, YAML, Markdown) ────────────────────
        # Check format support on the original spec.argv (before --markdown was appended).
        has_format_variants = _has_output_format_support(spec.argv)
        stdout_json: str | None = None
        stdout_yaml: str | None = None
        stdout_markdown: str | None = None

        if has_format_variants:
            # Re-run with --json and derive YAML + Markdown from it.
            json_argv = _inject_format_variant(run_argv, "--json")
            _, json_out, _ = _run_capture(json_argv, cli_app, profile=profile, safe=spec.safe)
            json_body = _strip_status_header(json_out).strip()

            # Verify the output is valid JSON before storing.
            try:
                parsed_json = json.loads(json_body)
            except json.JSONDecodeError:
                parsed_json = None

            if parsed_json is not None:
                stdout_json = json.dumps(parsed_json, indent=2, sort_keys=True)

                import yaml as _yaml  # noqa: PLC0415

                stdout_yaml = _yaml.dump(
                    parsed_json,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False,
                ).rstrip()

                from .markdown_output import render_markdown as _render_md  # noqa: PLC0415

                stdout_markdown = _render_md(parsed_json)

        art: dict[str, Any] = {
            "section": spec.section,
            "title": spec.title,
            "argv": run_argv,
            "exit_code": code,
            "elapsed_seconds": round(elapsed, 3),
            "truncated": did_trunc,
        }
        if stdout_json is not None:
            art["stdout_json"] = stdout_json
        if stdout_yaml is not None:
            art["stdout_yaml"] = stdout_yaml
        if stdout_markdown is not None:
            art["stdout_markdown"] = stdout_markdown

        artifacts.append(art)
        (raw_dir / f"{len(artifacts):03d}-{slug}.json").write_text(
            json.dumps({**art, "stdout_full": out}, indent=2),
            encoding="utf-8",
        )

        lines.append(f"### {spec.title}")
        lines.append("")
        lines.append("**Input:**")
        lines.append("")
        lines.append("```bash")
        lines.append(cmd_display)
        lines.append("```")
        lines.append("")
        if spec.notes:
            lines.append(f"*{spec.notes}*")
            lines.append("")
        lines.append(f"**Exit code:** `{code}`  ·  **Wall time (s):** `{elapsed:.3f}`")
        if did_trunc:
            lines.append("")
            lines.append(
                f"*Output truncated for this doc (max {max_lines} lines / {max_chars} chars).*"
            )
        lines.append("")
        lines.append("**Output:**")
        lines.append("")
        lines.append("```text")
        lines.append(truncated.rstrip() or "(empty)")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    (raw_dir / "index.json").write_text(
        json.dumps({"meta": meta, "runs": artifacts}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {output}", file=log)
    print(f"Wrote {len(artifacts)} raw JSON files under {raw_dir}", file=log)
    if skipped:
        print(f"Skipped {len(skipped)} commands (config errors): {skipped}", file=log)
    return 0
