---
name: distill
description: Extract reusable lessons from completed work, failed attempts, user corrections, logs, diffs, tests, project outcomes, local agent memory, and conversation history, then update durable skills or rules. Use when asked to learn from experience, personalize an agent from prior work, improve skills, refine agent behavior, audit skill health, or turn repeated mistakes into guidance.
---

# Distill: Improve The Next Run

Use this skill after meaningful work has produced a lesson.

Prefix your first response line with ⚗️ inline, not as its own paragraph.

Before the workflow, apply `../../shared-rules/host-compatibility.md`, `../../shared-rules/portable-profile.md`, and `../../shared-rules/personalization.md` for explicit TasteD/TasteDistill invocations. If this skill is already running the Local Personalization Bootstrap, use those shared rules only as host-safety, idempotence, and destination policy.
Apply `../../shared-rules/runtime-hygiene.md` when distillation reads logs, creates generated evidence, invokes helper scripts, or runs browser/runtime checks.

## Outcome Contract

- Outcome: current work improves future agent behavior through reusable guidance with scope, trigger, evidence, and destination.
- Done when: each lesson is classified as update now, keep candidate, or discard, and the chosen destination is the narrowest useful one.
- Evidence: user corrections, failed attempts, verified fixes, tests, command output, diffs, logs, delivery results, and stable project conventions.

## Taste Distillation Loop

```text
work -> evidence -> lesson -> durable rule -> better next run
```

Distillation is not a transcript summary. It turns repeated, verified behavior into future execution guidance. A lesson should explain when the agent should behave differently next time, what evidence supports the rule, and where the rule belongs.

## Local Personalization Bootstrap

Use this mode when the user asks to initialize these skills from their existing Codex or compatible agent memory, conversation history, logs, or prior task outcomes.

Do not assume those sources are already loaded. Installing a skill does not automatically import a user's historical conversations or memories. Explicitly invoking the TasteD/TasteDistill plugin or any `tasted-*` skill should perform a one-time bootstrap check through `../../shared-rules/personalization.md`. If no local TasteDistill profile exists, run this bootstrap before continuing with the requested skill.

v1 supports Codex, Claude Code, and Hermes. Codex can run as a full plugin adapter. Claude Code and Hermes use reference adapters by default: generate TasteDistill adapter snippets and local `~/.tastedistill/adapters/*.md` files, but do not write host memory or identity files unless the user explicitly asks.

Bootstrap flow:

1. Identify available local memory/history sources in the current agent environment.
2. Prefer existing summaries, registries, and indexed memories before broad raw transcript reads.
3. Detect the host agent when possible: Codex, Claude Code, Hermes, or unknown.
4. For Codex, treat `$HOME/.codex/instructions/codex-experience-review.md` as optional. If it is missing, synthesize a TasteDistill-owned Codex digest from available Codex summaries and registries.
5. Create the portable TasteDistill profile under `$HOME/.tastedistill` according to `../../shared-rules/portable-profile.md`.
6. Write `$HOME/.tastedistill/bootstrap.json` as the idempotence marker.
7. Summarize execution preferences, product taste, validation habits, reusable rules, project boundaries, and anti-patterns.
8. Generate host adapter snippets under `$HOME/.tastedistill/adapters/` when useful.
9. Automatic local TasteDistill bootstrap is allowed after explicit TasteD/TasteDistill use. For host memory integration, output the exact snippet to add unless the user explicitly requests host memory edits.
10. Report what was loaded, what was skipped, what was written, and how future sessions will load the profile.

Codex fallback flow:

1. Inventory these Codex sources when available:
   - `$HOME/.codex/instructions/codex-experience-review.md`
   - `$HOME/.codex/memories/memory_summary.md`
   - `$HOME/.codex/memories/MEMORY.md`
   - targeted `$HOME/.codex/memories/rollout_summaries/*` files referenced by the memory registry
   - `$HOME/.codex/config.toml` without copying secrets or volatile machine state
2. If `codex-experience-review.md` exists, use it as the highest-signal source.
3. If it is missing or incomplete, create:
   - `$HOME/.tastedistill/imports/codex/source-digest.md`
   - `$HOME/.tastedistill/imports/codex/source-digest.json`
4. Use the digest to seed `profile.md` and `harness.md`.
5. Record loaded, skipped, and missing sources in `sources.json` and `bootstrap.json`.
6. Do not automatically write `codex-experience-review.md` back into `$HOME/.codex/instructions/`.
7. Read raw Codex sessions, logs, or broad SQLite state only as an opt-in deep scan or bounded fallback when summary sources are insufficient. Follow `../../shared-rules/personalization.md#bounded-codex-history-scan`: metadata and indexes first, recent sessions default max 30, highest-frequency `cwd` groups default max 10, failures/fixes/user corrections prioritized, and scan scope reported before reading raw content.
8. Follow `../../shared-rules/personalization.md#codex-source-precedence`: bounded scan results can fill gaps or flag contradictions, but must not silently override an existing TasteDistill profile, Codex experience document, or Codex summary-derived rule.

Recommended output:

- a private experience profile saved outside this public skill repository, preferably `$HOME/.tastedistill/profile.md`
- a runtime contract saved at `$HOME/.tastedistill/harness.md`
- a bootstrap marker, preferably `$HOME/.tastedistill/bootstrap.json`
- a host source digest when needed, preferably `$HOME/.tastedistill/imports/<host>/source-digest.md`
- host adapter snippets, preferably under `$HOME/.tastedistill/adapters/`
- a host adapter file or a short instruction snippet the user can add to host instructions when automatic wiring is unavailable
- a summary of what was distilled: execution habits, preferences, project rules, validation habits, and anti-patterns
- a list of sources that were unavailable or intentionally skipped

Keep personal facts, private project details, raw transcripts, and machine-specific paths in the user's local profile or project profile. Promote only reusable behavior into this skill or shared rules.

## Workflow

1. Define the extraction scope: execution habit, design principle, debugging lesson, delivery rule, project invariant, or anti-pattern.
2. Gather a small amount of direct evidence.
3. Write each candidate lesson with:
   - trigger
   - wrong behavior
   - correct behavior
   - lesson
   - destination
   - evidence
4. Promote only durable behavior, not one-off state.
5. Write the rule into the narrowest useful destination.
6. Run a lightweight validation after editing skills or shared rules.
7. If the lesson exposes agent health risk, add or update a health check note before finishing.

## Destinations

| Destination | Use for |
|---|---|
| Global profile | Cross-agent user preferences, communication style, product taste, execution habits, and validation preferences. Write to `$HOME/.tastedistill/profile.md` and, when useful, `$HOME/.tastedistill/profile.json`. |
| Global harness | Cross-agent runtime contract: context loading, tool preference, permission boundaries, verification, delivery, and distillation policy. Write to `$HOME/.tastedistill/harness.md`. |
| Project profile | Repo-specific commands, release process, domain constraints, local architecture rules, validation surfaces, and recurring project lessons. Write under `$HOME/.tastedistill/projects/<repo-id>/`. |
| Host adapter | Short Codex, Claude Code, or Hermes loading guidance. Write under `$HOME/.tastedistill/adapters/` or output as a snippet. Do not edit host memory by default. |
| Current project docs | Only when the user explicitly wants repo docs updated, or when the repo's own instructions are the correct source of truth. |
| Skill instructions | Reusable behavior that applies whenever this phase is active. |
| Shared rules | Cross-skill anti-patterns, routing rules, or validation expectations. |
| Candidate note | Useful lessons that need more evidence before promotion. |
| Discard | One-off state, stale facts, secrets, private paths, or rules with no clear trigger. |

## Health Signals

During distillation, check whether the incident reveals one of these agent-health issues:

- missing verification surface
- stale or contradictory instructions
- unclear skill routing
- repeated retry without new evidence
- unsafe promotion of private or transient facts
- public-facing artifact not checked before delivery

If a health signal is present, add a concrete guardrail or note the gap as remaining risk.

## Rule Quality Gate

Promote a lesson only when it has a clear trigger, narrow scope, executable wording, and evidence. Do not promote secrets, local paths, transient release facts, one-off commands, raw transcripts, or private project details.

Never copy host memory files wholesale into TasteDistill. Distill them into short rules with provenance and destination.

Do not automatically write:

- `~/.codex/AGENTS.md`
- project `AGENTS.md`
- `~/.claude/CLAUDE.md`
- project `CLAUDE.md` or `.claude/CLAUDE.md`
- `~/.claude/projects/*/memory/*`
- `~/.hermes/SOUL.md`
- `~/.hermes/memories/*`
- `~/.hermes/.env`

Only write those host files when the user explicitly asks for that exact integration.

## Output Shape

```text
update now:
keep candidate:
discard:
files updated:
validation:
```
