# Personalization Bootstrap

Use this rule when a TasteDistill plugin or skill is explicitly invoked.

Explicit TasteDistill use means the user wants TasteDistill behavior, not just the base agent. Before the selected skill begins its main workflow, perform a lightweight, idempotent personalization bootstrap check.

Apply `host-compatibility.md` and `portable-profile.md` with this rule. TasteDistill is the portable profile source of truth; the host agent remains the execution runtime.

## Supported Hosts

v1 supports three host agents:

| Host | Bootstrap behavior |
|---|---|
| Codex | Plugin adapter. Explicit TasteDistill use may create or update `~/.tastedistill`, create or update the current repo project profile, and initialize the current repo CodeGraph index through `codegraph.md` when CodeGraph tools are available. |
| Claude Code | Reference adapter. Generate `~/.tastedistill/adapters/claude.md` and a snippet the user can add to Claude memory. Do not write `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`, or Claude auto memory unless explicitly requested. |
| Hermes | External profile adapter. Generate `~/.tastedistill/adapters/hermes.md` and a snippet the user can add to Hermes guidance. Do not write `~/.hermes/SOUL.md`, `~/.hermes/memories/*`, `~/.hermes/skills/*`, `~/.hermes/config.yaml`, or `~/.hermes/.env` unless explicitly requested. |

If the host is unknown, use the safest common path: create or load `~/.tastedistill`, generate adapter snippets, and do not write host memory.

## Bootstrap Check

Check whether a local TasteDistill portable profile is already present and loadable.

Preferred default locations:

- `$HOME/.tastedistill/profile.md`
- `$HOME/.tastedistill/harness.md`
- `$HOME/.tastedistill/bootstrap.json`

Also discover existing host-specific profiles, such as Codex experience instructions, Claude user memory, or Hermes memory files. Treat those files as sources, not as targets to overwrite.

If `profile.md`, `harness.md`, and `bootstrap.json` exist and are loadable, do not rebuild the global profile. Briefly note that TasteDistill personalization is already initialized when relevant, then continue with project bootstrap and the requested skill.

## First-Run Bootstrap

If no local TasteDistill profile or marker is found, treat the explicit TasteDistill invocation as permission to run the `tastedistill-distill` Local Personalization Bootstrap before the requested skill continues.

The bootstrap should:

1. Discover available local agent memory, conversation history, logs, and prior task summaries.
2. Prefer existing summaries, registries, and indexed memories before broad raw transcript reads.
3. Detect the current host as Codex, Claude Code, Hermes, or unknown.
4. Create the portable profile under `$HOME/.tastedistill` according to `portable-profile.md`.
5. Write `$HOME/.tastedistill/bootstrap.json` with at least timestamp, profile path, harness path, source summary, plugin version when available, and host adapter status.
6. Generate host adapter files under `$HOME/.tastedistill/adapters/`.
7. Automatic local TasteDistill bootstrap is allowed after explicit TasteDistill use. For host memory integration, output or save adapter snippets but do not write host memory unless explicitly requested.
8. Keep raw transcripts, secrets, private paths, machine-specific state, and project-private facts out of the public plugin repository.
9. Report what was created, what was loaded, what was skipped, and how future TasteDistill calls will reuse the profile.

## Existing Host Sources

If a host-specific experience document already exists, do not behave as if the user has no prior context.

Examples:

- Codex: `$HOME/.codex/instructions/codex-experience-review.md`
- Claude Code: `$HOME/.claude/CLAUDE.md`
- Hermes: `$HOME/.hermes/memories/MEMORY.md` or `$HOME/.hermes/memories/USER.md`

Use those sources to seed or update `~/.tastedistill/profile.md` and `~/.tastedistill/harness.md`, then record them in `~/.tastedistill/sources.json` and `~/.tastedistill/bootstrap.json`. Prefer summary and rule extraction over raw copying.

Do not re-run a broad raw transcript sweep only because `~/.tastedistill/bootstrap.json` is missing when a durable host-specific profile already exists.

## Project Bootstrap

When a TasteDistill call happens inside a Git repository, compute a stable repo id as defined in `portable-profile.md`.

Create or load:

- `$HOME/.tastedistill/projects/<repo-id>/project.md`
- `$HOME/.tastedistill/projects/<repo-id>/project.json`
- `$HOME/.tastedistill/projects/<repo-id>/lessons.jsonl`
- `$HOME/.tastedistill/projects/<repo-id>/sources.json`

The first project profile should be thin and evidence-based: repository identity, stack, likely entry points, known commands, instruction surfaces, validation surfaces, and boundaries. Do not turn a first-run orientation into a large project memory dump.

After project profile bootstrap, apply `codegraph.md` when CodeGraph tools are available. If the current host does not expose CodeGraph tools, skip CodeGraph and continue with normal repository search.

## Safety Boundaries

- Do not run personalization bootstrap during plugin installation alone.
- Do not repeat broad history reads once the local profile and marker exist.
- Do not promote private user facts into this public plugin.
- Do not write to host global memory, host project memory, host identity files, or project instruction files unless the user explicitly requests that write.
- If the environment blocks memory/history access, create the profile from available instructions and current context, then report the missing sources.
- Do not read Hermes `.env` files or any secrets source during bootstrap.

## Startup Order

When a TasteDistill call happens in a repository context:

1. Run `host-compatibility.md`.
2. Run this personalization bootstrap check.
3. Run `portable-profile.md` project profile bootstrap when inside a Git repository.
4. Run `shared-rules/codegraph.md` bootstrap when CodeGraph tools are available.
5. Then execute the selected stage skill.
