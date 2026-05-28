#!/usr/bin/env python3
"""Sync host effective-memory overlays into TasteDistill rules.jsonl."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            ids.add(item["id"])
    return ids


def append_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        return
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def stable_rule_id(host: str, source_path: str, rule: str) -> str:
    digest = hashlib.sha256(f"{host}\0{source_path}\0{rule}".encode("utf-8")).hexdigest()[:16]
    slug = Path(source_path).stem[:48].replace(" ", "-")
    return f"{host}-{slug}-{digest}"


def update_profile_json(path: Path, synced_at: str, added: int) -> None:
    payload: dict[str, Any] = {}
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
    payload.setdefault("schemaVersion", 1)
    payload["lastMemorySyncAt"] = synced_at
    payload["lastMemorySyncAddedRules"] = added
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="codex", choices=["codex", "claude"], help="Host effective-memory adapter to sync.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--tasted-home", default=None, help="TasteDistill home directory. Defaults to ~/.tastedistill.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    tasted_home = Path(args.tasted_home).expanduser().resolve() if args.tasted_home else home / ".tastedistill"
    effective_path = tasted_home / "imports" / args.host / "effective-memory.json"
    if not effective_path.exists():
        raise SystemExit(f"missing {effective_path}; run refresh_host_memory.py first")

    effective = load_json(effective_path)
    rules_path = tasted_home / "rules.jsonl"
    conflicts_path = tasted_home / "conflicts.jsonl"
    tasted_home.mkdir(parents=True, exist_ok=True)

    existing = read_jsonl_ids(rules_path)
    synced_at = now_iso()
    new_rules: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []

    for item in effective.get("resolvedRules", []):
        if not isinstance(item, dict) or not item.get("rule"):
            continue
        rule_id = stable_rule_id(args.host, str(item.get("sourcePath", "")), str(item["rule"]))
        if rule_id in existing:
            continue
        markers = item.get("markers") if isinstance(item.get("markers"), list) else []
        new_rules.append({
            "id": rule_id,
            "schemaVersion": 1,
            "scope": "global",
            "host": args.host,
            "trigger": "host effective memory correction overlay",
            "rule": item["rule"],
            "sourcePath": item.get("sourcePath"),
            "sourceOverlayId": item.get("sourceOverlayId"),
            "markers": markers,
            "createdAt": synced_at,
        })
        if any(str(marker).lower() in {"correction", "supersede", "do not infer", "wrong behavior", "纠正"} for marker in markers):
            conflicts.append({
                "id": f"conflict-{rule_id}",
                "schemaVersion": 1,
                "host": args.host,
                "sourcePath": item.get("sourcePath"),
                "ruleId": rule_id,
                "resolution": "host correction overlay supersedes older inferred or cached rules when conflicting",
                "createdAt": synced_at,
            })

    append_jsonl(rules_path, new_rules)
    append_jsonl(conflicts_path, conflicts)
    update_profile_json(tasted_home / "profile.json", synced_at, len(new_rules))
    print(f"rules_added={len(new_rules)} conflicts_recorded={len(conflicts)}")
    print(f"rules={rules_path}")
    print(f"conflicts={conflicts_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
