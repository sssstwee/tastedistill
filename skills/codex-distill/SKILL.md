---
name: codex-distill
description: Extract reusable lessons from completed work, failed attempts, user corrections, logs, diffs, tests, and project outcomes, then update durable skills or rules. Use when asked to learn from experience, improve skills, refine agent behavior, audit skill health, or turn repeated mistakes into guidance.
---

# Distill: Turn Experience Into Rules

Use this skill after meaningful work has produced a lesson.

## Outcome Contract

- Outcome: reusable guidance with scope, trigger, evidence, and destination.
- Done when: each lesson is classified as update now, keep candidate, or discard.
- Evidence: user corrections, failed attempts, verified fixes, tests, command output, diffs, logs, and stable project conventions.

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

