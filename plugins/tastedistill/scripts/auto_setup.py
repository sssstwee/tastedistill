#!/usr/bin/env python3
"""Idempotently install TasteDistill host adapters after plugin updates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def plugin_version(root: Path, state: dict[str, Any] | None = None) -> str:
    for rel in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        path = root / rel
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        value = payload.get("version")
        if isinstance(value, str) and value:
            return value
    if state and isinstance(state.get("lastEnsuredPluginVersion"), str):
        return state["lastEnsuredPluginVersion"]
    return "unknown"


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def write_state(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--force", action="store_true", help="Run even if this plugin version was already ensured.")
    parser.add_argument("--quiet", action="store_true", help="Only print when changes were made.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    root = plugin_root()
    tasted_home = home / ".tastedistill"
    state_path = tasted_home / "adapter-state.json"
    state = load_state(state_path)
    version = plugin_version(root, state)
    install_script = Path(__file__).resolve().parent / "install_adapters.py"

    if not args.force and state.get("lastEnsuredPluginVersion") == version:
        if not args.quiet:
            print(f"adapter_current={version}")
        return 0

    command = [sys.executable, str(install_script), "--home", str(home), "--write-host", "--quiet"]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return result.returncode

    changed_lines = [line for line in result.stdout.splitlines() if line and not line.startswith("changed=")]
    state.update({
        "schemaVersion": 1,
        "lastEnsuredAt": now_iso(),
        "lastEnsuredPluginVersion": version,
        "lastEnsuredPluginRoot": str(root),
        "lastChangedFiles": changed_lines,
    })
    write_state(state_path, state)

    if changed_lines or not args.quiet:
        print(f"adapter_ensured={version}")
        for line in changed_lines:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
