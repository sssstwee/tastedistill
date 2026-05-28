# Coding Guardrails

Use these rules for coding, refactoring, debugging, review, and implementation handoff.

## Think Before Coding

Do not silently choose an interpretation when the task has meaningful ambiguity.

- State assumptions that affect scope, behavior, cost, user-visible output, or rollback.
- Ask before editing when two valid interpretations would lead to different implementations.
- For simple, low-risk tasks, state the assumption briefly and proceed.

## Simplicity First

Solve the current problem with the smallest design that works.

- Prefer existing project patterns, helpers, and dependencies.
- Do not add abstraction, configuration, compatibility layers, or new runtime dependencies unless the current requirement proves they are needed.
- Necessary edge handling is not overengineering; speculative flexibility is.

## Surgical Changes

Keep the diff tied to the user's request.

- Every changed line should have a reason connected to the task.
- Do not perform drive-by refactors, formatting churn, renames, or comment rewrites.
- If the smallest correct fix reveals the same bug shape elsewhere, search and report the blast radius; fix siblings only when they share the same root cause and stay inside scope.

## Goal-Driven Execution

Turn the task into a pass/fail target before claiming success.

- Define what observable behavior should change.
- Prefer reproducible checks: tests, commands, logs, rendered UI, generated artifacts, or remote state.
- Report what was verified and what remains unverified.
