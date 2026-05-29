---
name: debug
description: Diagnose failures, broken behavior, regressions, test failures, runtime errors, stale state, rendering bugs, and repeated failed fixes. Use when something does not work, used to work, crashes, fails tests, or needs root-cause proof. Not for product planning or release readiness.
---

# Debug: Prove The Cause

Use this skill when the task starts from a symptom.

Prefix your first response line with ⚗️ inline, not as its own paragraph.

Before the workflow, apply `../../shared-rules/personalization.md` for explicit TasteD/TasteDistill invocations.
Apply `../../shared-rules/runtime-hygiene.md` when debugging uses helper scripts, browser checks, local servers, screenshots, traces, or other generated artifacts.

## Outcome Contract

- Outcome: proven root cause, minimal fix or handoff, and verification evidence.
- Done when: every observed symptom fits the explanation and the fix is checked by a reproducible test or runtime observation.
- Evidence: repro steps, logs, traces, state, source paths, generated artifacts, tests, screenshots, and command output.

## Workflow

1. List the observed symptoms.
2. Reproduce the issue or define the missing evidence.
3. Trace from symptom to source.
4. State a one-sentence root-cause hypothesis with evidence.
5. Make the smallest fix that addresses the cause.
6. Run the narrow regression check.
7. Search for the same bug shape if the root cause is reusable.

## Coding Guardrails

For fixes, apply `../../shared-rules/coding-guardrails.md`:

- Think before coding: do not edit until the root-cause hypothesis is specific and evidence-backed.
- Simplicity first: fix the cause directly; avoid broad rewrites, new abstractions, or speculative compatibility.
- Surgical changes: keep the patch to the failure path; search siblings only for the same bug shape.
- Goal-driven execution: prove the original symptom changed with a reproducible check.

## CodeGraph

For root-cause analysis in a Git repository, `../../shared-rules/personalization.md` should already have ensured the local CodeGraph index. When `codegraph_*` tools are available, prefer `codegraph_trace` for "how does X reach Y", `codegraph_callers` / `codegraph_callees` for one-hop flow, and `codegraph_context` for nearby implementation context. Read target files directly before editing.

## Stop Rules

- Same symptom after a fix means the hypothesis failed.
- Do not stack patches without new evidence.
- Do not claim UI, native, or generated-artifact bugs are fixed from compile output alone.
- If the fix expands into a refactor, pause and name the scope change.

## Output Shape

```text
Root cause:
Fix:
Confirmed:
Tests:
Regression guard:
Remaining risk:
```
