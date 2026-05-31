#!/usr/bin/env python3
"""Check TasteDistill local memory health and host-source freshness."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0


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


def status_line(ok: bool, label: str, detail: str) -> str:
    return f"{'OK' if ok else 'WARN'} {label}: {detail}"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def personal_marketplace_has_tasted(home: Path) -> bool:
    payload = read_json(home / ".agents" / "plugins" / "marketplace.json")
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        return False
    for entry in plugins:
        if not isinstance(entry, dict) or entry.get("name") != "tasted":
            continue
        source = entry.get("source")
        return isinstance(source, dict) and source.get("source") == "local" and source.get("path") == "./plugins/tasted"
    return False


def codex_config_has_tasted(home: Path) -> bool:
    config = home / ".codex" / "config.toml"
    if not config.exists():
        return False
    text = config.read_text(encoding="utf-8")
    return "[plugins.\"tasted@" in text or "[plugins.'tasted@" in text


def codex_plugin_source_ok(home: Path) -> bool:
    manifest = read_json(home / "plugins" / "tasted" / ".codex-plugin" / "plugin.json")
    return manifest.get("name") == "tasted"


def codex_cache_has_tasted(home: Path) -> bool:
    cache = home / ".codex" / "plugins" / "cache"
    return any(cache.glob("*/tasted/*/.codex-plugin/plugin.json")) if cache.exists() else False


def collect_codex_plugin_status(home: Path) -> list[str]:
    marketplace_ok = personal_marketplace_has_tasted(home)
    source_ok = codex_plugin_source_ok(home)
    config_ok = codex_config_has_tasted(home)
    cache_ok = codex_cache_has_tasted(home)
    lines = [
        status_line(marketplace_ok, "codex-personal-marketplace", str(home / ".agents" / "plugins" / "marketplace.json")),
        status_line(source_ok, "codex-personal-plugin-source", str(home / "plugins" / "tasted")),
        status_line(config_ok, "codex-plugin-config", str(home / ".codex" / "config.toml")),
    ]
    if cache_ok and not config_ok:
        lines.append("ACTION run python3 ~/.tastedistill/bin/install_codex.py to repair a stale Codex plugin config")
    elif not marketplace_ok or not source_ok:
        lines.append("ACTION run plugins/tastedistill/scripts/install_codex.py from the TasteDistill repo")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="codex", choices=["codex", "claude"], help="Host adapter to check.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--tasted-home", default=None, help="TasteDistill home directory. Defaults to ~/.tastedistill.")
    parser.add_argument("--project-root", default=None, help="Project root for project-local host memory.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    tasted_home = Path(args.tasted_home).expanduser().resolve() if args.tasted_home else home / ".tastedistill"
    profile = tasted_home / "profile.md"
    harness = tasted_home / "harness.md"
    bootstrap = tasted_home / "bootstrap.json"
    rules = tasted_home / "rules.jsonl"
    effective = tasted_home / "imports" / args.host / "effective-memory.json"
    adapter = tasted_home / "adapters" / ("claude.md" if args.host == "claude" else "codex.md")
    preflight = tasted_home / "bin" / "check_memory_freshness.py"
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else Path.cwd()
    sources = collect_codex_sources(home, project_root) if args.host == "codex" else collect_claude_sources(home, project_root)
    newest_source, newest_source_ts = newest(sources)
    effective_ts = mtime(effective)
    profile_ts = mtime(profile)
    rules_ts = mtime(rules)

    lines = [
        status_line(profile.exists(), "profile", str(profile)),
        status_line(harness.exists(), "harness", str(harness)),
        status_line(bootstrap.exists(), "bootstrap", str(bootstrap)),
        status_line(effective.exists(), "effective-memory", f"{effective} ({fmt_ts(effective_ts)})"),
        status_line(rules.exists(), "rules", f"{rules} ({fmt_ts(rules_ts)})"),
        status_line(adapter.exists(), "adapter", str(adapter)),
        status_line(preflight.exists(), "preflight", str(preflight)),
    ]
    if args.host == "codex":
        lines.extend(collect_codex_plugin_status(home))

    if newest_source:
        stale_effective = newest_source_ts > effective_ts
        stale_profile = newest_source_ts > max(profile_ts, rules_ts)
        lines.append(status_line(not stale_effective, "host-source freshness", f"newest={newest_source} ({fmt_ts(newest_source_ts)})"))
        if stale_effective:
            lines.append(f"ACTION run scripts/refresh_host_memory.py --host {args.host}")
        if stale_profile:
            lines.append(f"PROMPT 发现 {args.host.title()} memory 比 TasteD rules 更新，是否同步？")
            lines.append(f"ACTION run scripts/sync_profile.py --host {args.host} after refresh")
    else:
        lines.append(status_line(False, "host sources", "no host memory sources found"))

    print("\n".join(lines))
    return 1 if any(line.startswith("WARN") for line in lines) else 0


if __name__ == "__main__":
    raise SystemExit(main())
