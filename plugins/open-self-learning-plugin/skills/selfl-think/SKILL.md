---
name: selfl-think
description: Turn rough ideas, product questions, architecture choices, implementation options, and tradeoffs into decision-ready plans. Use when the user asks what to build, whether an approach is worth it, how to structure a solution, or what plan the agent should execute. Not for debugging an already broken behavior.
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

## Coding Guardrails

For implementation plans, apply `../../shared-rules/coding-guardrails.md`:

- Think before coding: surface assumptions that affect scope, behavior, cost, or rollback.
- Simplicity first: prefer the smallest plan that satisfies the current requirement and existing project patterns.
- Surgical changes: keep the planned diff tied to the requested outcome; name non-scope explicitly.
- Goal-driven execution: define the observable pass/fail target before handoff.

## CodeGraph

For plans that change existing code, apply `../../shared-rules/codegraph.md` when `codegraph_*` tools are available. Use `codegraph_context` to inspect current patterns and `codegraph_impact` for symbols likely to change before recommending architecture, file targets, or risk level.

## Output Shape

```text
Recommendation:
Why:
Rejected options:
Implementation plan:
Verification:
Risks:
Assumptions:
Non-scope:
```

## Do Not

- Hide major tradeoffs.
- Invent requirements.
- Expand scope beyond the user's goal.
- Turn a debugging symptom into a planning exercise.
- Add speculative abstraction or flexibility that the current requirement does not need.
