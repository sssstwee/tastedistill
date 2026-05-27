# Skill Routing

Use the narrowest skill that matches the task.

| Trigger | Skill |
|---|---|
| unfamiliar domain, source synthesis, research memo | `selfl-learn` |
| product judgment, architecture tradeoff, plan | `selfl-think` |
| UI, interaction, product surface, visual quality | `selfl-design` |
| error, crash, regression, failing test, broken behavior | `selfl-debug` |
| review, merge, release, publish, PR, issue follow-through | `selfl-ship` |
| extract lessons, update rules, audit skill health | `selfl-distill` |

Use `shared-rules/self-learning-loop.md` after meaningful work produces a reusable lesson.
Use `shared-rules/coding-guardrails.md` for coding, refactoring, debugging, review, and implementation handoff.
Use `shared-rules/codegraph.md` when `codegraph_*` tools are available and the task involves architecture lookup, call flow, impact analysis, or large-repo exploration.

When two skills match, prefer the one closest to the user's starting point:

- symptom first -> debug
- artifact first -> ship
- decision first -> think
- visual surface first -> design
- experience mining first -> distill
