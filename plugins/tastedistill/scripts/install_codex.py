#!/usr/bin/env python3
"""Install or repair TasteD for Codex via the implicit personal marketplace."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PLUGIN_NAME = "tasted"
MARKETPLACE_SOURCE_PATH = "./plugins/tasted"


def resolve_plugin_root(home: Path, explicit: str | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.extend([
        Path(__file__).resolve().parents[1],
        home / "plugins" / PLUGIN_NAME,
    ])
    cache_root = home / ".codex" / "plugins" / "cache"
    if cache_root.exists():
        candidates.extend(path.parent.parent for path in cache_root.glob(f"*/{PLUGIN_NAME}/*/.codex-plugin/plugin.json"))

    for candidate in candidates:
        root = candidate.resolve()
        if (root / ".codex-plugin" / "plugin.json").exists() and is_tasted_plugin(root):
            return root
    raise RuntimeError("could not locate a TasteD Codex plugin root; pass --plugin-root")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"failed to parse {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"expected JSON object in {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def codex_manifest(root: Path) -> dict[str, Any]:
    path = root / ".codex-plugin" / "plugin.json"
    payload = load_json(path)
    if payload.get("name") != PLUGIN_NAME:
        raise RuntimeError(f"{path} is not a TasteD Codex plugin manifest")
    return payload


def is_tasted_plugin(path: Path) -> bool:
    manifest = path / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        return False
    try:
        return load_json(manifest).get("name") == PLUGIN_NAME
    except RuntimeError:
        return False


def ignore_noise(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {".DS_Store", "__pycache__"} or name.endswith(".pyc")}


def copy_plugin_source(source: Path, target: Path, force: bool) -> bool:
    if source.resolve() == target.resolve():
        return False
    if target.exists() and not is_tasted_plugin(target) and not force:
        raise RuntimeError(f"{target} exists and is not a TasteD plugin; pass --force to replace it")

    source_manifest = codex_manifest(source)
    target_manifest = (load_json(target / ".codex-plugin" / "plugin.json") if is_tasted_plugin(target) else {})
    if target.exists() and target_manifest.get("version") == source_manifest.get("version") and not force:
        return False

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tasted-codex-install-", dir=str(target.parent)) as tmp:
        staged = Path(tmp) / PLUGIN_NAME
        shutil.copytree(source, staged, ignore=ignore_noise)
        if target.exists():
            shutil.rmtree(target)
        staged.rename(target)
    return True


def install_repair_script(home: Path) -> bool:
    source = Path(__file__).resolve()
    target = home / ".tastedistill" / "bin" / source.name
    old = target.read_text(encoding="utf-8") if target.exists() else None
    new = source.read_text(encoding="utf-8")
    if old == new:
        target.chmod(0o755)
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    target.chmod(0o755)
    return True


def ensure_personal_marketplace(home: Path) -> tuple[str, Path, bool]:
    path = home / ".agents" / "plugins" / "marketplace.json"
    payload = load_json(path) if path.exists() else {
        "name": "personal",
        "interface": {"displayName": "Personal"},
        "plugins": [],
    }

    if not isinstance(payload.get("name"), str) or not payload["name"]:
        payload["name"] = "personal"
    payload.setdefault("interface", {"displayName": "Personal"})
    plugins = payload.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise RuntimeError(f"{path} has non-array plugins")

    entry = {
        "name": PLUGIN_NAME,
        "source": {"source": "local", "path": MARKETPLACE_SOURCE_PATH},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
        "category": "Coding",
    }
    for index, existing in enumerate(plugins):
        if isinstance(existing, dict) and existing.get("name") == PLUGIN_NAME:
            if existing == entry:
                return payload["name"], path, False
            plugins[index] = entry
            return payload["name"], path, write_json(path, payload)

    plugins.append(entry)
    return payload["name"], path, write_json(path, payload)


def find_codex(explicit: str | None) -> str | None:
    candidates = [
        explicit,
        os.environ.get("CODEX_CLI_PATH"),
        shutil.which("codex"),
        "/Applications/Codex.app/Contents/Resources/codex",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def run_codex_add(codex: str, home: Path, marketplace_name: str) -> tuple[bool, str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env.setdefault("CODEX_HOME", str(home / ".codex"))
    Path(env["CODEX_HOME"]).expanduser().mkdir(parents=True, exist_ok=True)
    command = [codex, "plugin", "add", f"{PLUGIN_NAME}@{marketplace_name}"]
    result = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def codex_plugin_list(codex: str, home: Path) -> str:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env.setdefault("CODEX_HOME", str(home / ".codex"))
    Path(env["CODEX_HOME"]).expanduser().mkdir(parents=True, exist_ok=True)
    result = subprocess.run([codex, "plugin", "list"], check=False, capture_output=True, text=True, env=env)
    return (result.stdout + result.stderr).strip()


def codex_desktop_running() -> bool:
    result = subprocess.run(["pgrep", "-fl", "Codex"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return False
    return any("Codex.app" in line or "Codex Desktop" in line for line in result.stdout.splitlines())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--codex", default=None, help="Path to the Codex CLI.")
    parser.add_argument("--plugin-root", default=None, help="Existing TasteD plugin root to install from.")
    parser.add_argument("--no-plugin-add", action="store_true", help="Only install the personal marketplace source.")
    parser.add_argument("--force", action="store_true", help="Replace an existing ~/plugins/tasted directory.")
    parser.add_argument("--quiet", action="store_true", help="Only print warnings or failures.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    source = resolve_plugin_root(home, args.plugin_root)
    target = home / "plugins" / PLUGIN_NAME
    changed: list[str] = []
    warnings: list[str] = []

    if copy_plugin_source(source, target, args.force):
        changed.append(f"plugin_source={target}")
    if install_repair_script(home):
        changed.append(f"repair_script={home / '.tastedistill' / 'bin' / 'install_codex.py'}")
    marketplace_name, marketplace_path, marketplace_changed = ensure_personal_marketplace(home)
    if marketplace_changed:
        changed.append(f"personal_marketplace={marketplace_path}")

    codex = find_codex(args.codex)
    if args.no_plugin_add:
        warnings.append("codex_plugin_add_skipped=true")
    elif not codex:
        warnings.append("codex_cli_missing=true")
    else:
        ok, output = run_codex_add(codex, home, marketplace_name)
        if not ok:
            warnings.append(f"codex_plugin_add_failed={output}")
        else:
            changed.append(f"codex_plugin=tasted@{marketplace_name}")
            listing = codex_plugin_list(codex, home)
            if f"{PLUGIN_NAME}@{marketplace_name}" not in listing or "installed, enabled" not in listing:
                warnings.append("codex_plugin_verify_failed=true")

    if codex_desktop_running():
        warnings.append("codex_desktop_running=restart Codex Desktop or start a new thread after installing")

    if not args.quiet:
        print(f"marketplace={marketplace_name}")
        print(f"plugin_source={target}")
        print(f"marketplace_file={marketplace_path}")
    for line in changed:
        if not args.quiet:
            print("changed=" + line)
    for line in warnings:
        print("warning=" + line, file=sys.stderr)
    return 1 if any(line.startswith("codex_plugin_add_failed=") for line in warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
