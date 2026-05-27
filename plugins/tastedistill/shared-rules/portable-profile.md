# Portable Profile

Use this rule when TasteDistill initializes, loads, updates, or explains the local portable engineering profile.

TasteDistill stores portable user and project experience in `~/.tastedistill`. This directory is the TasteDistill source of truth across supported host agents. Host memory systems may reference it, but should not receive full copies by default.

## Directory Layout

```text
~/.tastedistill/
  manifest.json
  profile.md
  profile.json
  harness.md
  bootstrap.json
  sources.json
  adapters/
    codex.md
    claude.md
    hermes.md
  projects/
    <repo-id>/
      project.md
      project.json
      lessons.jsonl
      sources.json
```

## File Roles

| File | Role |
|---|---|
| `manifest.json` | TasteDistill schema version, created/updated timestamps, and supported hosts. |
| `profile.md` | Human-readable global engineering profile: communication, product taste, execution habits, validation preferences, durable personal rules. |
| `profile.json` | Machine-readable summary/index for the global profile. |
| `harness.md` | Runtime contract: context loading, tool preferences, permission boundaries, verification, delivery, and distillation rules. |
| `bootstrap.json` | Idempotence marker: initialization time, sources used, sources skipped, plugin version, and host adapter state. |
| `sources.json` | Discovered host sources and import status. |
| `adapters/*.md` | Host-specific reference snippets. These are generated locally and are not automatically written into host memory. |
| `projects/<repo-id>/project.md` | Human-readable project harness: repo identity, stack, entry points, commands, boundaries, validation surfaces. |
| `projects/<repo-id>/project.json` | Machine-readable project index. |
| `projects/<repo-id>/lessons.jsonl` | Append-only project lessons backed by evidence. |
| `projects/<repo-id>/sources.json` | Project source inventory such as package manifests, instruction files, and docs. |

## repo-id

When inside a Git repository, derive the project id from the repository root:

```text
repo-id = safe-slug(repo-name) + "-" + first 10 hex chars of sha256(realpath(repo-root))
```

Use a stable hash so same-named repositories do not collide and the full local path is not exposed in the directory name.

If hashing is not available, use a conservative safe slug and record the full path only inside local `project.json` if needed. Do not put full local paths in public plugin files.

## Initialization Policy

- Plugin installation alone must not scan history or create user/project profiles.
- Explicit TasteDistill plugin or `tastedistill-*` skill use may create `~/.tastedistill`.
- Explicit TasteDistill use may perform local bootstrap automatically across supported hosts while respecting each host's write boundaries.
- Claude Code and Hermes use reference adapters by default. Generate snippets and local adapter files; do not write host memory unless explicitly requested.
- Project profiles may be created automatically when TasteDistill is explicitly used inside a Git repository, but the first profile should be thin: stack, entry points, commands, instruction surfaces, known validation entry points, and boundaries.
- Deep project lessons should be added by `tastedistill-distill` only when backed by task evidence.

## Existing Host Sources

If existing host-specific experience files are found, treat them as sources, not as targets to overwrite.

Examples:

- Codex: `~/.codex/instructions/codex-experience-review.md`, `~/.codex/memories/MEMORY.md`, `~/.codex/memories/memory_summary.md`
- Claude Code: `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`
- Hermes: `~/.hermes/SOUL.md`, `~/.hermes/memories/MEMORY.md`, `~/.hermes/memories/USER.md`

When an existing host profile already contains durable user preferences, merge or summarize it into `~/.tastedistill/profile.md` and record the source in `sources.json` and `bootstrap.json`. Do not re-run broad raw transcript sweeps just because the TasteDistill marker did not previously exist.

## Write Boundaries

- Write automatically only under `~/.tastedistill` and, when CodeGraph bootstrap runs, the current repository's `.codegraph/` plus `.git/info/exclude`.
- Do not write raw transcripts, secrets, local credentials, `.env` files, or token material.
- Do not write public shared rules with private user facts or project-private details.
- Prefer references over copies when integrating with host memory.
