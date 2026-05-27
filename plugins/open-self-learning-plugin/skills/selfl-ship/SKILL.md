---
name: selfl-ship
description: Review implemented work, verify acceptance criteria, prepare delivery, inspect release readiness, handle PR or issue follow-through, and confirm shipped state. Use when work is ready for review, merge, release, publish, push, or handoff. Not for root-cause debugging.
---

# Ship: Verify Before Delivery

Use this skill when an artifact exists and needs a delivery decision.

## Outcome Contract

- Outcome: a delivery decision grounded in current evidence.
- Done when: review findings, acceptance state, release state, or blockers are stated with proof.
- Evidence: worktree status, diff, tests, CI, manifests, docs, release artifacts, package contents, and remote state.

## Worktree Safety

Before review, release, or destructive repository action:

```bash
git status --short --branch -uall
```

Treat modified, staged, and untracked files as user work. Do not reset, clean, stash, switch branches, or overwrite files unless the user explicitly asks for that operation.

## Workflow

1. Extract the delivery surface: diff, PR, release candidate, issue queue, package, or generated artifact.
2. Read public project context: README, agent instructions, manifests, test config, CI, release docs, and changed files.
3. Identify correctness, safety, compatibility, UX, and release risks.
4. Run the narrowest meaningful verification first, then broader checks when needed.
5. Fix only small, clearly scoped issues when the user authorized implementation.
6. For release or publish actions, verify artifact contents and remote state before claiming success.

## Coding Guardrails

For review and delivery, apply `../../shared-rules/coding-guardrails.md`:

- Think before coding: identify any hidden assumptions in the diff or release path.
- Simplicity first: flag unnecessary abstraction, dependencies, or configuration surface.
- Surgical changes: every changed line should connect to the requested outcome; flag drive-by refactors separately.
- Goal-driven execution: acceptance should be tied to explicit checks, artifacts, or remote state.

## CodeGraph

For review and delivery, apply `../../shared-rules/codegraph.md` when `codegraph_*` tools are available. Use `codegraph_impact`, callers/callees, or trace output as risk evidence for non-trivial diffs, not as a substitute for tests, artifacts, CI, or remote-state checks.

## Review Output

Lead with findings ordered by severity. If there are no findings, say so and name remaining test gaps.

## Do Not

- Treat source tests as release proof when artifacts or registry state matter.
- Close issues, publish packages, push commits, or tag releases without explicit current-turn authorization.
- Promote project-specific commands into reusable rules.
- Treat a large diff as acceptable when unrelated changes are mixed into the requested work.
