# Skill Routing

Use the narrowest skill that matches the task.

| Trigger | Skill |
|---|---|
| unfamiliar domain, source synthesis, research memo | `codex-learn` |
| product judgment, architecture tradeoff, plan | `codex-think` |
| UI, interaction, product surface, visual quality | `codex-design` |
| error, crash, regression, failing test, broken behavior | `codex-debug` |
| review, merge, release, publish, PR, issue follow-through | `codex-ship` |
| extract lessons, update rules, audit skill health | `codex-distill` |

When two skills match, prefer the one closest to the user's starting point:

- symptom first -> debug
- artifact first -> ship
- decision first -> think
- visual surface first -> design
- experience mining first -> distill

