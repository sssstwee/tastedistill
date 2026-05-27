---
name: codex-distill
description: Extract reusable lessons from completed work, failed attempts, user corrections, logs, diffs, tests, and project outcomes, then update durable skills or rules. Use when asked to learn from experience, improve skills, refine agent behavior, audit skill health, or turn repeated mistakes into guidance.
---

# Distill: Improve The Next Run

Use this skill after meaningful work has produced a lesson.

## Outcome Contract

- Outcome: current work improves future Codex behavior through reusable guidance with scope, trigger, evidence, and destination.
- Done when: each lesson is classified as update now, keep candidate, or discard, and the chosen destination is the narrowest useful one.
- Evidence: user corrections, failed attempts, verified fixes, tests, command output, diffs, logs, delivery results, and stable project conventions.

## Self-Learning Loop

```text
work -> evidence -> lesson -> durable rule -> better next run
```

Distillation is not a transcript summary. It turns repeated, verified behavior into future execution guidance. A lesson should explain when Codex should behave differently next time, what evidence supports the rule, and where the rule belongs.

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
| Current project docs | Repo-specific commands, release process, domain constraints, or local architecture rules. |
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

## Output Shape

```text
update now:
keep candidate:
discard:
files updated:
validation:
```
