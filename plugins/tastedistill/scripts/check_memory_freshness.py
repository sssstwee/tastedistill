#!/usr/bin/env python3
"""Detect whether host memory sources are newer than TasteDistill rules."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


HOSTS = ("codex", "claude")
HOST_LABELS = {
    "codex": "Codex",
    "claude": "Claude Code",
}


def fmt_ts(value: float) -> str:
    if not value:
        return "missing"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def newest(paths: list[Path]) -> tuple[Path | None, float]:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return None, 0.0
    latest = max(existing, key=lambda path: path.stat().st_mtime)
    return latest, latest.stat().st_mtime


def collect_codex_sources(home: Path, project_root: Path | None = None) -> list[Path]:
    memories = home / ".codex" / "memories"
    paths = [
        home / ".codex" / "instructions" / "codex-experience-review.md",
        memories / "memory_summary.md",
        memories / "MEMORY.md",
    ]
    notes_dir = memories / "extensions" / "ad_hoc" / "notes"
    if notes_dir.exists():
        paths.extend(sorted(notes_dir.glob("*.md")))
    return paths


def collect_claude_sources(home: Path, project_root: Path | None = None) -> list[Path]:
    paths = [home / ".claude" / "CLAUDE.md"]
    root = project_root or Path.cwd()
    paths.extend([root / "CLAUDE.md", root / ".claude" / "CLAUDE.md"])
    return paths


def host_sources(host: str, home: Path, project_root: Path) -> list[Path]:
    if host == "codex":
        return collect_codex_sources(home, project_root)
    if host == "claude":
        return collect_claude_sources(home, project_root)
    raise ValueError(f"unsupported host: {host}")


def sync_commands(tasted_home: Path, host: str, project_root: Path) -> list[str]:
    bin_dir = tasted_home / "bin"
    refresh = bin_dir / "refresh_host_memory.py"
    sync = bin_dir / "sync_profile.py"
    commands = [f"{refresh} --host {host}"]
    if host == "claude":
        commands[0] += f" --project-root {project_root}"
    commands.append(f"{sync} --host {host}")
    return commands


def format_stale_hosts(statuses: list[dict[str, Any]]) -> str:
    names = [HOST_LABELS.get(status["host"], status["host"]) for status in statuses]
    if len(names) <= 1:
        return names[0] if names else "host"
    return "、".join(names[:-1]) + " 和 " + names[-1]


def sync_prompt(statuses: list[dict[str, Any]]) -> str:
    return f"发现 {format_stale_hosts(statuses)} 的 memory 比 TasteD rules 更新，是否同步？"


def host_status(host: str, home: Path, tasted_home: Path, project_root: Path) -> dict[str, Any]:
    rules = tasted_home / "rules.jsonl"
    rules_ts = rules.stat().st_mtime if rules.exists() else 0.0
    newest_source, newest_source_ts = newest(host_sources(host, home, project_root))
    return {
        "host": host,
        "stale": bool(newest_source and newest_source_ts > rules_ts),
        "rulesPath": str(rules),
        "rulesMtime": fmt_ts(rules_ts),
        "newestSource": str(newest_source) if newest_source else None,
        "newestSourceMtime": fmt_ts(newest_source_ts),
        "commands": sync_commands(tasted_home, host, project_root),
    }


def print_human(statuses: list[dict[str, Any]]) -> None:
    stale = [status for status in statuses if status["stale"]]
    if not stale:
        print("OK TasteDistill rules are current for checked host memory sources.")
        for status in statuses:
            print(f"- {status['host']}: newest={status['newestSource'] or 'missing'} ({status['newestSourceMtime']}), rules={status['rulesMtime']}")
        return

    print("SYNC_NEEDED")
    print(sync_prompt(stale))
    for status in stale:
        print(f"- {status['host']}: newest={status['newestSource']} ({status['newestSourceMtime']}), rules={status['rulesMtime']}")
    print("")
    print("If the user confirms, run:")
    for status in stale:
        for command in status["commands"]:
            print(f"  {command}")
    print("")
    print("Do not run these sync commands without user confirmation.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", action="append", choices=HOSTS, help="Host to check. May be passed more than once. Defaults to both.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--tasted-home", default=None, help="TasteDistill home directory. Defaults to ~/.tastedistill.")
    parser.add_argument("--project-root", default=None, help="Project root for project-local host memory.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable status.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    tasted_home = Path(args.tasted_home).expanduser().resolve() if args.tasted_home else home / ".tastedistill"
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else Path.cwd().resolve()
    hosts = args.host or list(HOSTS)
    statuses = [host_status(host, home, tasted_home, project_root) for host in hosts]

    if args.json:
        print(json.dumps({"schemaVersion": 1, "statuses": statuses}, ensure_ascii=False, indent=2))
    else:
        print_human(statuses)
    return 2 if any(status["stale"] for status in statuses) else 0


if __name__ == "__main__":
    raise SystemExit(main())
