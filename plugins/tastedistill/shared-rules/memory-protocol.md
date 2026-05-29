# Cross-Agent Memory Protocol

Use this rule when TasteDistill imports, refreshes, syncs, or checks host memory.

TasteDistill is a portable memory layer, not the owner of host-native memory. The host agent resolves its own instructions, routing, and current effective memory first. TasteDistill then imports the resolved view into a host-neutral local store.

## Store Files

```text
~/.tastedistill/
  profile.md
  profile.json
  harness.md
  rules.jsonl
  conflicts.jsonl
  sources.json
  imports/
    <host>/
      effective-memory.md
      effective-memory.json
```

## Default Read Policy

Host adapters should enable lightweight automatic reads for ordinary work:

1. Read `~/.tastedistill/profile.md` when present.
2. Read `~/.tastedistill/harness.md` when present.
3. Read `~/.tastedistill/rules.jsonl` when present.

Do not automatically read raw host histories, broad session logs, rollout summaries, or large project lesson logs during ordinary work. Those sources are refresh inputs, not default context.

Project memory is semi-automatic: read the matching `projects/<project-id>/project.md` when available, but only open `lessons.jsonl` when the task needs project history.

| File | Purpose |
|---|---|
| `imports/<host>/effective-memory.json` | Machine-readable host memory snapshot, source inventory, overlays, and resolved rules. |
| `imports/<host>/effective-memory.md` | Human-readable summary of the same snapshot. |
| `rules.jsonl` | Append-only host-neutral rules that other agents can consume. |
| `conflicts.jsonl` | Records of rules that were superseded, contradicted, or intentionally ignored. |
| `sources.json` | Source inventory with path, role, mtime, hash, and import status. |

## Effective Memory View

For Codex, the effective memory view is:

1. `$HOME/.codex/memories/memory_summary.md`
2. `$HOME/.codex/memories/MEMORY.md`
3. `$HOME/.codex/memories/extensions/ad_hoc/notes/*.md`
4. Targeted rollout summaries only when referenced or needed as evidence.

Ad-hoc notes are correction overlays, not low-quality history. Newer correction overlays can supersede older inferred rules.

For Claude Code, the effective memory view is:

1. `$HOME/.claude/CLAUDE.md`
2. Project `CLAUDE.md`
3. Project `.claude/CLAUDE.md`
4. Current-session user corrections supplied by the host.

Claude project memory is project-scoped. Import it into the host snapshot with its source path and role, but do not automatically copy it into global TasteDistill rules unless the rule is clearly portable beyond that project.

## Bidirectional Host Sync

Any supported host can refresh another host's memory sources when it has local filesystem access and the user requested cross-agent synchronization.

Examples:

```text
# Run inside Codex to make Claude Code memory available to Codex through TasteDistill.
scripts/refresh_host_memory.py --host claude --project-root /path/to/project
scripts/sync_profile.py --host claude

# Run inside Claude Code to make Codex memory available to Claude through TasteDistill.
scripts/refresh_host_memory.py --host codex
scripts/sync_profile.py --host codex
```

The result is always stored under `~/.tastedistill/imports/<host>/` plus host-neutral `rules.jsonl`. The consuming agent should read `profile.md`, `harness.md`, and `rules.jsonl`; it does not need to read the other host's raw memory files directly.

Cross-host import must stay read-only for the source host. Do not write `CLAUDE.md`, Codex memories, or project instructions unless the user explicitly asks for that exact host integration.

## Precedence

Use this order when rules conflict:

1. Current explicit user correction.
2. Newer host correction overlays such as Codex ad-hoc notes.
3. Current project instructions.
4. Existing TasteDistill rules/profile.
5. Host main memory registry.
6. Host summaries.
7. Targeted rollout summaries or bounded raw history.

Do not let an older TasteDistill profile override a newer host correction. If the profile is stale, report that the current run is using the newer host correction and ask for or run a refresh when appropriate.

## Commands

TasteDistill helper scripts implement three local operations:

| Operation | Script | Result |
|---|---|---|
| Refresh host memory | `scripts/refresh_host_memory.py` | Writes `imports/<host>/effective-memory.*` and updates `sources.json`. |
| Sync profile | `scripts/sync_profile.py` | Imports stable overlay rules into `rules.jsonl` and records conflicts. |
| Doctor | `scripts/doctor.py` | Checks whether profile, rules, imports, and host sources are stale or missing. |
| Preflight freshness check | `scripts/check_memory_freshness.py` | Compares host memory source mtimes with `rules.jsonl` and prints the user confirmation prompt when sync is needed. |
| Auto setup | `scripts/auto_setup.py` | Idempotently refreshes host adapter marker sections and `~/.tastedistill/bin`, and silently ensures the current Git repository's local CodeGraph index. |

Use `--host codex` inside Codex and `--host claude` inside Claude Code. For Claude project memory, pass `--project-root <path>` when the current working directory is not the project root.

Default host adapters may run only the preflight check during ordinary work. They must ask the specific confirmation prompt printed by the checker before running refresh/sync, for example:

```text
发现 Codex 的 memory 比 TasteD rules 更新，是否同步？
发现 Claude Code 的 memory 比 TasteD rules 更新，是否同步？
```

## Safety

- Do not read secrets, `.env` files, auth stores, token stores, browser stores, or raw transcript bodies during default refresh.
- Do not write host memory or project instruction files.
- Keep machine-specific source paths local under `~/.tastedistill`.
- Treat helper outputs as local private files, not public plugin artifacts.
