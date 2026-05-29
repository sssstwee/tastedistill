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


def git_root_for(path: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return Path(value).resolve() if value else None


def ensure_gitignore(repo_root: Path) -> bool:
    gitignore_path = repo_root / ".gitignore"
    old = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    lines = old.splitlines()
    if ".codegraph/" in lines:
        return False
    new = old
    if new and not new.endswith("\n"):
        new += "\n"
    new += ".codegraph/\n"
    gitignore_path.write_text(new, encoding="utf-8")
    return True


def untrack_codegraph(repo_root: Path) -> tuple[bool, str | None]:
    tracked = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "--", ".codegraph"],
        check=False,
        capture_output=True,
        text=True,
    )
    if tracked.returncode != 0 or not tracked.stdout.strip():
        return False, None
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rm", "-r", "--cached", "--", ".codegraph"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "unknown error").strip().splitlines()
        detail = message[-1] if message else "unknown error"
        return False, detail
    return True, None


def ensure_codegraph(project_root: Path) -> tuple[list[str], list[str], str | None]:
    repo_root = git_root_for(project_root)
    if not repo_root:
        return [], [], None
    changed = []
    warnings = []
    if ensure_gitignore(repo_root):
        changed.append(f"codegraph_gitignore_added={repo_root}")
    untracked, untrack_error = untrack_codegraph(repo_root)
    if untracked:
        changed.append(f"codegraph_untracked={repo_root}")
    elif untrack_error:
        warnings.append(f"codegraph_untrack_failed={repo_root}: {untrack_error}")
    if (repo_root / ".codegraph" / "codegraph.db").exists():
        return changed, warnings, str(repo_root)

    result = subprocess.run(
        ["npx", "-y", "@colbymchenry/codegraph", "init", "-i"],
        cwd=str(repo_root),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "unknown error").strip().splitlines()
        detail = message[-1] if message else "unknown error"
        warnings.append(f"codegraph_init_failed={repo_root}: {detail}")
        return changed, warnings, str(repo_root)

    changed.append(f"codegraph_initialized={repo_root}")
    return changed, warnings, str(repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--project-root", default=None, help="Current project root or working directory for CodeGraph setup.")
    parser.add_argument("--no-codegraph", action="store_true", help="Skip current-repository CodeGraph setup.")
    parser.add_argument("--force", action="store_true", help="Run even if this plugin version was already ensured.")
    parser.add_argument("--quiet", action="store_true", help="Only print when changes were made.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else Path.cwd().resolve()
    root = plugin_root()
    tasted_home = home / ".tastedistill"
    state_path = tasted_home / "adapter-state.json"
    state = load_state(state_path)
    version = plugin_version(root, state)
    install_script = Path(__file__).resolve().parent / "install_adapters.py"
    changed_lines: list[str] = []
    warning_lines: list[str] = []
    codegraph_repo_root: str | None = None

    if not args.no_codegraph:
        codegraph_changed, codegraph_warnings, codegraph_repo_root = ensure_codegraph(project_root)
        changed_lines.extend(codegraph_changed)
        warning_lines.extend(codegraph_warnings)

    adapter_current = not args.force and state.get("lastEnsuredPluginVersion") == version
    if not adapter_current:
        command = [sys.executable, str(install_script), "--home", str(home), "--write-host", "--quiet"]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            return result.returncode
        changed_lines.extend(line for line in result.stdout.splitlines() if line and not line.startswith("changed="))

    state.update({
        "schemaVersion": 1,
        "lastEnsuredAt": now_iso(),
        "lastEnsuredPluginVersion": version,
        "lastEnsuredPluginRoot": str(root),
        "lastCodeGraphProjectRoot": codegraph_repo_root,
        "lastChangedFiles": changed_lines,
        "lastWarnings": warning_lines,
    })
    write_state(state_path, state)

    if args.quiet:
        for line in warning_lines:
            print(line, file=sys.stderr)
        return 0

    print(f"adapter_ensured={version}")
    if adapter_current:
        print(f"adapter_current={version}")
    for line in changed_lines:
        print(line)
    for line in warning_lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
