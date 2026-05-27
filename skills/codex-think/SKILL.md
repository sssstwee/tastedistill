---
name: codex-think
description: Turn rough ideas, product questions, architecture choices, implementation options, and tradeoffs into decision-ready plans. Use when the user asks what to build, whether an approach is worth it, how to structure a solution, or what plan Codex should execute. Not for debugging an already broken behavior.
---

# Think: Decide Before Building

Use this skill when the main work is judgment, scope, or plan design.

## Outcome Contract

- Outcome: a decision, rationale, risks, and an executable plan.
- Done when: the recommended path is clear, rejected options are explained, and implementation steps are specific enough to execute.
- Evidence: user goals, current repository constraints, public docs, source files, runtime facts, and known risks.

## Workflow

1. Restate the decision to be made.
2. List constraints that materially affect the answer.
3. Compare viable options with tradeoffs.
4. Pick one recommendation and explain why it fits the current goal.
5. Write an implementation plan with verification steps.
6. Name assumptions that must be checked before or during execution.

## Output Shape

```text
Recommendation:
Why:
Rejected options:
Implementation plan:
Verification:
Risks:
```

## Do Not

- Hide major tradeoffs.
- Invent requirements.
- Expand scope beyond the user's goal.
- Turn a debugging symptom into a planning exercise.

