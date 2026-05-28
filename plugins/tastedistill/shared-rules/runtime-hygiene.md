# Runtime Hygiene

Use this rule when TasteDistill runs commands, browser checks, generated-artifact checks, or helper scripts.

TasteDistill should leave the user's project and host environment in a clearly explained state. Verification artifacts are useful only when their location and cleanup status are explicit.

## Helper Resolution

- Prefer tools and scripts that belong to the current project or the loaded TasteDistill skill.
- Resolve skill helper paths relative to the `SKILL.md` file that was actually opened.
- Do not guess host skill install paths such as `$HOME/.codex/skills/<skill>/scripts`.
- If a helper is missing, say which expected path was missing and continue with an equivalent manual check when feasible.
- On explicit TasteD/TasteDistill use, run `../../scripts/auto_setup.py --quiet` when present before the main skill workflow. This setup is idempotent and only maintains TasteDistill adapter marker sections and `~/.tastedistill/bin`; it must not sync host memory.
- TasteDistill memory helpers live at `../../scripts/` relative to `skills/tasted-distill/SKILL.md` and `claude-skills/distill/SKILL.md`.
- For cross-agent memory work, prefer `refresh_host_memory.py`, `sync_profile.py`, and `doctor.py` before hand-editing generated TasteDistill store files.

## Browser Tooling

- Follow the user's host preference when it is known. For local Codex sessions, prefer the current Chrome or host-provided browser plugin when the task needs a browser and that tool is available.
- If the preferred browser path fails, state the failure briefly before falling back to another browser tool.
- Close tabs or pages opened only for verification when the check is complete.
- Do not claim browser cleanup is complete if persistent MCP/browser service processes are still running; distinguish closed tabs, stopped app servers, and remaining tool service processes.

## Generated Artifacts

- Avoid leaving screenshots, snapshots, traces, coverage, or temporary reports in the project root unless the user asked for those files.
- Prefer a temporary directory or `$HOME/.tastedistill/runs/<timestamp>/` for TasteDistill-owned verification artifacts.
- If a tool necessarily writes into the project, report the exact paths and whether they were kept or removed.
- Do not describe a project as unchanged without qualifying generated verification artifacts.

## Local Servers

- Stop local servers started only for verification before final response unless the user asked to keep them running.
- Report server state separately from browser state and process/service state.
