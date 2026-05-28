#!/usr/bin/env python3
"""Create a TasteDistill effective-memory snapshot from host memory sources."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any


CORRECTION_MARKERS = (
    "correction",
    "supersede",
    "do not infer",
    "wrong behavior",
    "correct behavior",
    "default",
    "已移除",
    "以后不要",
    "不要",
    "纠正",
)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, role: str, loaded: bool) -> dict[str, Any]:
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        "path": str(path),
        "role": role,
        "exists": exists,
        "loaded": loaded and exists,
        "bytes": stat.st_size if stat else None,
        "mtime": dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).astimezone().isoformat(timespec="seconds") if stat else None,
        "sha256": sha256_file(path) if exists else None,
    }


def read_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n\n[truncated by TasteDistill refresh_host_memory]\n"
    return text


def markers_for(text: str) -> list[str]:
    lower = text.lower()
    return [marker for marker in CORRECTION_MARKERS if marker.lower() in lower]


def title_for(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if stripped:
            return stripped[:120]
    return path.stem


def extract_rule_lines(text: str) -> list[str]:
    lines: list[str] = []
    capture_next = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        lower = line.lower()
        if lower.rstrip(":") in {"correct behavior", "correct interpretation", "keep valid when independently supported", "trigger", "supersede"}:
            capture_next = True
            continue
        if capture_next and line.startswith("-"):
            lines.append(line.lstrip("- ").strip())
            continue
        if capture_next and not line.startswith("-"):
            capture_next = False
        if any(marker.lower() in lower for marker in ("do not", "must not", "should never", "不要", "不能", "以后不要")):
            lines.append(line.lstrip("- ").strip())
    return lines[:12]


def overlay_from_path(path: Path, role: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    text = read_text(path)
    marker_hits = markers_for(text)
    overlay_id = hashlib.sha256(str(path).encode("utf-8") + b"\0" + (sha256_file(path) or "").encode("utf-8")).hexdigest()[:16]
    overlay = {
        "id": overlay_id,
        "path": str(path),
        "role": role,
        "title": title_for(path, text),
        "mtime": file_record(path, role, True)["mtime"],
        "markers": marker_hits,
        "sha256": sha256_file(path),
        "excerpt": text[:2000],
    }
    rules: list[dict[str, Any]] = []
    for index, rule in enumerate(extract_rule_lines(text), start=1):
        rules.append({
            "id": f"{overlay_id}-{index}",
            "sourceOverlayId": overlay_id,
            "sourcePath": str(path),
            "rule": rule,
            "markers": marker_hits,
        })
    return overlay, rules


def codex_sources(home: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    codex = home / ".codex"
    memories = codex / "memories"
    summary = memories / "memory_summary.md"
    registry = memories / "MEMORY.md"
    notes_dir = memories / "extensions" / "ad_hoc" / "notes"

    sources = [
        file_record(codex / "instructions" / "codex-experience-review.md", "host-experience-document", False),
        file_record(summary, "host-memory-summary", False),
        file_record(registry, "host-memory-registry", False),
    ]

    overlays: list[dict[str, Any]] = []
    resolved_rules: list[dict[str, Any]] = []

    if notes_dir.exists():
        note_paths = sorted(notes_dir.glob("*.md"), key=lambda item: item.stat().st_mtime)
        for path in note_paths:
            marker_hits = markers_for(read_text(path))
            role = "host-correction-overlay" if marker_hits else "host-ad-hoc-note"
            sources.append(file_record(path, role, True))
            overlay, rules = overlay_from_path(path, role)
            overlays.append(overlay)
            resolved_rules.extend(rules)
    else:
        sources.append(file_record(notes_dir, "host-correction-overlay-directory", False))

    return sources, overlays, resolved_rules


def claude_sources(home: Path, project_root: Path | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: list[tuple[Path, str]] = [
        (home / ".claude" / "CLAUDE.md", "claude-global-memory"),
    ]
    if project_root is not None:
        root = project_root.expanduser().resolve()
        candidates.extend([
            (root / "CLAUDE.md", "claude-project-memory"),
            (root / ".claude" / "CLAUDE.md", "claude-project-memory"),
        ])

    sources: list[dict[str, Any]] = []
    overlays: list[dict[str, Any]] = []
    resolved_rules: list[dict[str, Any]] = []
    for path, role in candidates:
        exists = path.exists()
        sources.append(file_record(path, role, exists))
        if not exists or not path.is_file():
            continue
        overlay, rules = overlay_from_path(path, role)
        overlays.append(overlay)
        resolved_rules.extend(rules)
    return sources, overlays, resolved_rules


def write_sources(tasted_home: Path, generated_at: str, host: str, sources: list[dict[str, Any]]) -> None:
    path = tasted_home / "sources.json"
    payload = {
        "schemaVersion": 2,
        "updatedAt": generated_at,
        "hosts": {
            host: {
                "sources": sources,
            }
        },
    }
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(old, dict):
                payload.update({k: v for k, v in old.items() if k not in {"schemaVersion", "updatedAt", "hosts"}})
                hosts = old.get("hosts") if isinstance(old.get("hosts"), dict) else {}
                hosts[host] = {"sources": sources}
                payload["hosts"] = hosts
        except json.JSONDecodeError:
            pass
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, host: str, generated_at: str, sources: list[dict[str, Any]], overlays: list[dict[str, Any]], resolved_rules: list[dict[str, Any]]) -> None:
    lines = [
        f"# {host.title()} Effective Memory",
        "",
        f"Generated: {generated_at}",
        "",
        "## Sources",
        "",
    ]
    for source in sources:
        state = "loaded" if source.get("loaded") else "inventoried" if source.get("exists") else "missing"
        lines.append(f"- {state}: `{source['path']}` ({source['role']})")
    lines.extend(["", "## Correction Overlays", ""])
    for overlay in overlays:
        markers = ", ".join(overlay["markers"]) if overlay["markers"] else "none"
        lines.append(f"- `{overlay['id']}` {overlay['title']} ({markers})")
    lines.extend(["", "## Resolved Rule Candidates", ""])
    for rule in resolved_rules:
        lines.append(f"- `{rule['id']}` {rule['rule']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="codex", choices=["codex", "claude"], help="Host memory adapter to refresh.")
    parser.add_argument("--home", default=str(Path.home()), help="Home directory to inspect.")
    parser.add_argument("--out", default=None, help="TasteDistill home directory. Defaults to ~/.tastedistill.")
    parser.add_argument("--project-root", default=None, help="Project root for project-local host memory such as CLAUDE.md.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    tasted_home = Path(args.out).expanduser().resolve() if args.out else home / ".tastedistill"
    imports_dir = tasted_home / "imports" / args.host
    imports_dir.mkdir(parents=True, exist_ok=True)
    tasted_home.mkdir(parents=True, exist_ok=True)

    generated_at = now_iso()
    if args.host == "codex":
        sources, overlays, resolved_rules = codex_sources(home)
    else:
        project_root = Path(args.project_root) if args.project_root else Path.cwd()
        sources, overlays, resolved_rules = claude_sources(home, project_root)
    payload = {
        "schemaVersion": 1,
        "host": args.host,
        "generatedAt": generated_at,
        "sources": sources,
        "overlays": overlays,
        "resolvedRules": resolved_rules,
    }
    json_path = imports_dir / "effective-memory.json"
    md_path = imports_dir / "effective-memory.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(md_path, args.host, generated_at, sources, overlays, resolved_rules)
    write_sources(tasted_home, generated_at, args.host, sources)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"overlays={len(overlays)} resolved_rules={len(resolved_rules)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
