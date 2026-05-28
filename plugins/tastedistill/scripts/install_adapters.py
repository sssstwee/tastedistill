#!/usr/bin/env python3
"""Install TasteDistill adapter snippets for host agents."""

from __future__ import annotations

import argparse
from pathlib import Path


CODEX_SNIPPET = """# TasteDistill

At the start of ordinary work, lightly read these files when present:
- ~/.tastedistill/profile.md
- ~/.tastedistill/harness.md
- ~/.tastedistill/rules.jsonl

Use them as distilled cross-agent preferences and rules. Do not read raw Codex/Claude histories during ordinary work. Only refresh host memory when the user asks to sync, refresh, import, or distill memory.

For project work, if a matching ~/.tastedistill/projects/<project-id>/project.md exists, load it lightly. Do not bulk-read lessons.jsonl unless the task needs project history.
"""


CLAUDE_SNIPPET = """# TasteDistill

At the start of ordinary work, lightly read these files when present:
- ~/.tastedistill/profile.md
- ~/.tastedistill/harness.md
- ~/.tastedistill/rules.jsonl

Use them as distilled cross-agent preferences and rules. Do not read raw Codex/Claude histories during ordinary work. Only refresh host memory when the user asks to sync, refresh, import, or distill memory.

For project work, if a matching ~/.tastedistill/projects/<project-id>/project.md exists, load it lightly. Do not bulk-read lessons.jsonl unless the task needs project history.
Do not copy raw TasteDistill content into CLAUDE.md.
"""


def write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def replace_section(path: Path, title: str, snippet: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    start = f"<!-- BEGIN {title} -->"
    end = f"<!-- END {title} -->"
    block = f"{start}\n{snippet.rstrip()}\n{end}\n"
    if start in old and end in old:
        before, rest = old.split(start, 1)
        _, after = rest.split(end, 1)
        new = before.rstrip() + "\n\n" + block + after.lstrip()
    else:
        new = old.rstrip() + ("\n\n" if old.strip() else "") + block
    if new == old:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()), help="Home directory.")
    parser.add_argument("--write-host", action="store_true", help="Also install snippets into host global instruction files.")
    args = parser.parse_args()

    home = Path(args.home).expanduser().resolve()
    tasted_home = home / ".tastedistill"
    changed = []
    if write_if_changed(tasted_home / "adapters" / "codex.md", CODEX_SNIPPET):
        changed.append(str(tasted_home / "adapters" / "codex.md"))
    if write_if_changed(tasted_home / "adapters" / "claude.md", CLAUDE_SNIPPET):
        changed.append(str(tasted_home / "adapters" / "claude.md"))
    if args.write_host:
        if replace_section(home / ".codex" / "AGENTS.md", "TasteDistill", CODEX_SNIPPET):
            changed.append(str(home / ".codex" / "AGENTS.md"))
        if replace_section(home / ".claude" / "CLAUDE.md", "TasteDistill", CLAUDE_SNIPPET):
            changed.append(str(home / ".claude" / "CLAUDE.md"))
    print("changed=" + str(len(changed)))
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
