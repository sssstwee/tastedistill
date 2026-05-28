# Personalization Bootstrap

Use this rule when a TasteD/TasteDistill plugin or skill is explicitly invoked.

Explicit TasteD or TasteDistill use means the user wants TasteDistill behavior, not just the base agent. Before the selected skill begins its main workflow, perform a lightweight, idempotent personalization bootstrap check.

Apply `host-compatibility.md` and `portable-profile.md` with this rule. TasteDistill is the portable profile source of truth; the host agent remains the execution runtime.

## Supported Hosts

v1 supports two host agents:

| Host | Bootstrap behavior |
|---|---|
| Codex | Plugin adapter. Explicit TasteD or TasteDistill use may create or update `~/.tastedistill`, create or update the current project profile, and initialize the current repo CodeGraph index through `codegraph.md` when CodeGraph tools are available. |
| Claude Code | Reference adapter. Generate `~/.tastedistill/adapters/claude.md` and a snippet the user can add to Claude memory. Do not write `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`, or Claude auto memory unless explicitly requested. |

If the host is unknown, use the safest common path: create or load `~/.tastedistill`, generate adapter snippets, and do not write host memory.

## Bootstrap Check

Check whether a local TasteDistill portable profile is already present and loadable.

Preferred default locations:

- `$HOME/.tastedistill/profile.md`
- `$HOME/.tastedistill/harness.md`
- `$HOME/.tastedistill/bootstrap.json`

Also discover existing host-specific profiles, such as Codex experience instructions or Claude user memory. Treat those files as sources, not as targets to overwrite.

If `profile.md`, `harness.md`, and `bootstrap.json` exist and are loadable, do not rebuild the global profile. Briefly note that TasteDistill personalization is already initialized when relevant, then continue with project bootstrap and the requested skill. Existing TasteDistill files are a cache of distilled preferences, not proof that newer host memory corrections have already been imported.

## Host Effective Memory View

When the host has its own memory system, let the host form the effective memory view before TasteDistill runs. TasteDistill may import or summarize that view, but must not replace the host's precedence rules.

For Codex, the effective memory view is:

1. `$HOME/.codex/memories/memory_summary.md` for the current summary.
2. `$HOME/.codex/memories/MEMORY.md` for the main registry and indexed lessons.
3. `$HOME/.codex/memories/extensions/ad_hoc/notes/*.md` for explicit corrections, overrides, and newly captured rules.
4. Targeted rollout summaries only when referenced by the registry or needed as evidence.

Codex ad-hoc notes are a correction layer. Newer notes with wording such as `correction`, `supersede`, `do not infer`, `default`, or `wrong behavior` should override older inferred rules when they conflict. Do not treat an older TasteDistill profile as authoritative against a newer host correction.

For Claude Code, the effective memory view is:

1. `$HOME/.claude/CLAUDE.md` for global Claude guidance.
2. Project `CLAUDE.md` for project guidance.
3. Project `.claude/CLAUDE.md` for project-local Claude guidance.
4. Current-session user corrections supplied by the host.

Claude project guidance should remain project-scoped unless the user explicitly asks to promote a rule globally or the rule is clearly portable.

If a TasteD/TasteDistill invocation only needs current-task behavior, use the host-provided effective context and continue. If the user asks to initialize, refresh, import, or distill memory, import the effective host memory view into TasteDistill-owned files and record the exact source set in `sources.json` and `bootstrap.json`.

## First-Run Bootstrap

If no local TasteDistill profile or marker is found, treat the explicit TasteD/TasteDistill invocation as permission to run the `tasted-distill` Local Personalization Bootstrap before the requested skill continues.

The bootstrap should:

1. Discover available local agent memory, conversation history, logs, and prior task summaries.
2. Prefer existing summaries, registries, and indexed memories before broad raw transcript reads.
3. Detect the current host as Codex, Claude Code, or unknown.
4. For Codex, run [Codex Source Synthesis](#codex-source-synthesis) when needed.
5. Create the portable profile under `$HOME/.tastedistill` according to `portable-profile.md`.
6. Write `$HOME/.tastedistill/bootstrap.json` with at least timestamp, profile path, harness path, source summary, plugin version when available, and host adapter status.
7. Generate host adapter files under `$HOME/.tastedistill/adapters/`.
8. Automatic local TasteDistill bootstrap is allowed after explicit TasteD/TasteDistill use. For host memory integration, output or save adapter snippets but do not write host memory unless explicitly requested.
9. Keep raw transcripts, secrets, private paths, machine-specific state, and project-private facts out of the public plugin repository.
10. Report what was created, what was loaded, what was skipped, and how future TasteD/TasteDistill calls will reuse the profile.

Use the real current timestamp for generated metadata. Do not use placeholder dates such as midnight on the current day. If the host exposes a current date but not a precise clock, run a local time command or record that the timestamp is approximate.

## Existing Host Sources

If a host-specific experience document already exists, do not behave as if the user has no prior context.

Examples:

- Codex: `$HOME/.codex/instructions/codex-experience-review.md`
- Claude Code: `$HOME/.claude/CLAUDE.md`, project `CLAUDE.md`, project `.claude/CLAUDE.md`

Use those sources to seed or update `~/.tastedistill/profile.md` and `~/.tastedistill/harness.md`, then record them in `~/.tastedistill/sources.json` and `~/.tastedistill/bootstrap.json`. Prefer summary and rule extraction over raw copying.

Do not re-run a broad raw transcript sweep only because `~/.tastedistill/bootstrap.json` is missing when a durable host-specific profile already exists.

## Codex Source Synthesis

Codex may or may not have a user-created experience document. Treat `$HOME/.codex/instructions/codex-experience-review.md` as an optional accelerator, not as a required prerequisite.

When the host is Codex, use this order:

1. If `$HOME/.codex/instructions/codex-experience-review.md` exists, read it as the highest-signal Codex experience source.
2. Always inventory Codex memory summary and registry sources when available, even if the experience document is already sufficient:
   - `$HOME/.codex/memories/memory_summary.md`
   - `$HOME/.codex/memories/MEMORY.md`
   - `$HOME/.codex/memories/extensions/ad_hoc/notes/*.md`
   - targeted files under `$HOME/.codex/memories/rollout_summaries/` only when referenced by the registry or needed for evidence.
3. If the experience document is missing or too thin, or if newer Codex correction notes materially change the current profile, synthesize or refresh a TasteDistill-owned digest from the effective Codex memory view:
   - `$HOME/.tastedistill/imports/codex/source-digest.md`
   - `$HOME/.tastedistill/imports/codex/source-digest.json`
4. Record all discovered, loaded, skipped, and missing Codex sources in `$HOME/.tastedistill/sources.json` and `$HOME/.tastedistill/bootstrap.json`.

If a source is only inventoried and not fully read, record that distinction explicitly. A lightweight bootstrap may avoid broad history scans, but it should not make the source inventory look narrower than it was.

The Codex digest should extract durable communication preferences, execution habits, product taste, validation habits, reusable project boundaries, and anti-patterns. It must not copy raw transcripts, secrets, token material, private logs, or large project-private facts.

Do not automatically create or overwrite `$HOME/.codex/instructions/codex-experience-review.md`. If the user asks for a Codex-native experience document, state the target file and ask before writing host instructions.

Raw Codex history is opt-in or bounded fallback. Read `$HOME/.codex/sessions/**/*.jsonl`, `$HOME/.codex/logs_2.sqlite`, or broad state databases only when summaries and registries are insufficient, or when the user explicitly asks for a deep scan. In that case, follow [Bounded Codex History Scan](#bounded-codex-history-scan) and keep the result distilled into TasteDistill files.

## Codex Source Precedence

The normal Codex source strategy and bounded history scan must not compete.

Use this precedence order:

1. Host-provided effective current context: respect the host's already-resolved memory, instruction, and routing decisions for the current turn.
2. Existing TasteDistill profile and bootstrap marker: load and reuse by default, but treat it as a cache that can be stale relative to newer host corrections.
3. Existing host experience document: use `$HOME/.codex/instructions/codex-experience-review.md` as a high-signal source when present.
4. Codex summaries, registries, and correction layers: use `memory_summary.md`, `MEMORY.md`, `extensions/ad_hoc/notes/*.md`, and targeted rollout summaries as the default synthesis layer.
5. Bounded history scan: use only to fill gaps, resolve contradictions, or satisfy an explicit deeper-import request.

Bounded scan results may enrich missing evidence, add candidate lessons, or mark contradictions for review. They must not silently override profile rules derived from higher-precedence sources. If bounded evidence contradicts an existing profile rule, record the conflict in `sources.json` or `bootstrap.json` and keep the existing rule unless the newer evidence is clearly repeated, durable, and relevant. If a newer host correction contradicts the existing TasteDistill profile, do not let the stale profile win; either refresh the profile when requested or report that a newer host correction is being used for this run.

## Bounded Codex History Scan

Use this only as a fallback when Codex summaries, registries, and targeted rollout summaries are not enough to build a useful profile, or when the user explicitly asks for deeper import.

Default order:

1. Read metadata and indexes before full content. Prefer `$HOME/.codex/state_5.sqlite` metadata, `$HOME/.codex/session_index.jsonl` when present, and file names/timestamps over full session bodies.
2. Build a small evidence set before reading raw records:
   - recent sessions, default max 30
   - highest-frequency `cwd` groups, default max 10
   - sessions referenced by `MEMORY.md` or rollout summaries
   - sessions with failures, fixes, user corrections, validation outcomes, or repeated project rules
3. Before reading raw session or log content, report the intended scope:
   - source paths
   - maximum item count
   - time range when known
   - whether full transcript bodies will be read
   - explicit secret exclusions
4. Do not read `.env`, auth files, token stores, unrelated private project files, or raw browser/profile stores.
5. Distill only durable preferences, habits, validation rules, project boundaries, and anti-patterns. Do not copy raw messages or logs into TasteDistill.

Example scope report:

```text
I will read Codex metadata and up to 30 recent session summaries across the top 10 cwd groups. I will not read .env files, auth files, token stores, or unrelated private project files. Full transcript bodies will only be opened if the summaries do not provide enough evidence.
```

## Project Bootstrap

When a TasteD or TasteDistill call happens inside a local project directory, compute a stable project id as defined in `portable-profile.md`.

Use the Git repository root when available. If the current directory is not inside a Git repository, use the current working directory as a directory-backed project root. Non-Git project profiles are still created; only Git-specific features are skipped.

Create or load:

- `$HOME/.tastedistill/projects/<project-id>/project.md`
- `$HOME/.tastedistill/projects/<project-id>/project.json`
- `$HOME/.tastedistill/projects/<project-id>/lessons.jsonl`
- `$HOME/.tastedistill/projects/<project-id>/sources.json`

The first project profile should be thin and evidence-based: repository or directory identity, stack, likely entry points, known commands, instruction surfaces, validation surfaces, and boundaries. Do not turn a first-run orientation into a large project memory dump.

After project profile bootstrap, apply `codegraph.md` only when the current project root is a Git repository and CodeGraph tools are available. If the current project is not a Git repository, report that project-level TasteDistill data was created or loaded but CodeGraph was skipped.

## Safety Boundaries

- Do not run personalization bootstrap during plugin installation alone.
- Do not repeat broad history reads once the local profile and marker exist.
- Do not promote private user facts into this public plugin.
- Do not write to host global memory, host project memory, host identity files, or project instruction files unless the user explicitly requests that write.
- If the environment blocks memory/history access, create the profile from available instructions and current context, then report the missing sources.
- Do not read `.env` files or any secrets source during bootstrap.

## Startup Order

When a TasteD or TasteDistill call happens in a project context:

1. Run `host-compatibility.md`.
2. Run this personalization bootstrap check.
3. Run `portable-profile.md` project profile bootstrap for the current Git repository or non-Git project directory.
4. Run `shared-rules/codegraph.md` bootstrap only when the current project root is a Git repository and CodeGraph tools are available.
5. Then execute the selected stage skill.
