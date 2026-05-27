# Personalization Bootstrap

Use this rule when a selfL plugin or skill is explicitly invoked.

Explicit selfL use means the user wants selfL behavior, not just the base agent. Before the selected skill begins its main workflow, perform a lightweight, idempotent personalization bootstrap check.

## Bootstrap Check

Check whether a local selfL experience profile is already present and loadable.

Preferred default locations:

- `$HOME/.selfl/profile.md`
- `$HOME/.selfl/bootstrap.json`

Also respect an existing agent-specific profile if the current environment already has one wired into global or project instructions.

If a profile exists and is loadable, do not rebuild it. Briefly note that selfL personalization is already initialized when relevant, then continue with the requested skill.

## First-Run Bootstrap

If no local selfL profile or marker is found, treat the explicit selfL invocation as permission to run the `selfl-distill` Local Personalization Bootstrap before the requested skill continues.

The bootstrap should:

1. Discover available local agent memory, conversation history, logs, and prior task summaries.
2. Prefer existing summaries, registries, and indexed memories before broad raw transcript reads.
3. Create `$HOME/.selfl/profile.md` outside this public plugin repository.
4. Write `$HOME/.selfl/bootstrap.json` with at least the timestamp, profile path, source summary, and plugin version when available.
5. Add or propose a profile-loading instruction for the current agent's global or project instruction surface.
6. Keep raw transcripts, secrets, private paths, machine-specific state, and project-private facts out of the public plugin repository.
7. Report what was created, what was loaded, what was skipped, and how future selfL calls will reuse the profile.

## Safety Boundaries

- Do not run personalization bootstrap during plugin installation alone.
- Do not repeat broad history reads once the local profile and marker exist.
- Do not promote private user facts into this public plugin.
- Do not write to a global or project instruction file if the instruction surface is unknown or risky; output the exact snippet instead.
- If the environment blocks memory/history access, create the profile from available instructions and current context, then report the missing sources.

## Startup Order

When a selfL call happens in a repository context:

1. Run this personalization bootstrap check first.
2. Then run `shared-rules/codegraph.md` bootstrap when CodeGraph is available.
3. Then execute the selected stage skill.
