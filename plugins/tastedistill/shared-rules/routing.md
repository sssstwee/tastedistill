# Skill Routing

Use the narrowest skill that matches the task.

| Trigger | Skill |
|---|---|
| unfamiliar domain, source synthesis, research memo | `tasted-learn` |
| product judgment, architecture tradeoff, plan | `tasted-think` |
| UI, interaction, product surface, visual quality | `tasted-design` |
| error, crash, regression, failing test, broken behavior | `tasted-debug` |
| review, merge, release, publish, PR, issue follow-through | `tasted-ship` |
| extract lessons, update rules, audit skill health | `tasted-distill` |

Use `shared-rules/taste-distillation-loop.md` after meaningful work produces a reusable lesson.
Use `shared-rules/personalization.md` at the start of every explicit TasteD/TasteDistill plugin or skill invocation.
Use `shared-rules/host-compatibility.md` before writing host agent memory, identity, config, or project instruction files.
Use `shared-rules/portable-profile.md` when creating, loading, or updating `~/.tastedistill` global or project profiles.
Use `shared-rules/coding-guardrails.md` for coding, refactoring, debugging, review, and implementation handoff.
Use `shared-rules/codegraph.md` for Git repositories. Local index creation is handled by `scripts/auto_setup.py`; when `codegraph_*` tools are available, use them for architecture lookup, call flow, impact analysis, or large-repo exploration.
Use `shared-rules/runtime-hygiene.md` when running commands, helper scripts, browser checks, local servers, or generated-artifact verification.

When two skills match, prefer the one closest to the user's starting point:

- symptom first -> debug
- artifact first -> ship
- decision first -> think
- visual surface first -> design
- experience mining first -> distill
