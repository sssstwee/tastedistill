# Self-Learning Loop

Use this rule when a completed task, failed attempt, user correction, or delivery result contains a reusable lesson.

## Loop

```text
work -> evidence -> lesson -> durable rule -> better next run
```

## Promotion Rules

Promote a lesson only when it has:

- a clear trigger
- a wrong behavior to avoid
- a correct behavior to repeat
- evidence from the current task or repeated prior tasks
- a narrow destination
- no secrets, personal paths, private project facts, or transient state

## Destination Rules

| Lesson type | Destination |
|---|---|
| Stage-specific behavior | The matching skill's `SKILL.md` |
| Cross-stage behavior | `skills/shared-rules/` |
| Repo-specific behavior | The target repo's own public docs or agent instructions |
| Useful but unproven behavior | Candidate note, not a shipped rule |
| Private context | Keep outside the public repository |

## Validation

After updating a skill or shared rule:

1. Confirm the rule has a trigger and an action.
2. Confirm it does not encode local private data.
3. Run the repository safety scan when available.
4. Report which files changed and which validation ran.
