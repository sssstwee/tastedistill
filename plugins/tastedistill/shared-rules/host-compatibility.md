# Host Compatibility

Use this rule whenever TasteDistill runs inside, or prepares instructions for, a host coding agent.

TasteDistill is a portable engineering profile and harness layer. The host agent remains the execution runtime. TasteDistill must not replace the host's memory system, identity file, permission model, tool policy, or native routing.

## Supported Hosts In v1

| Host | Native surface | TasteDistill behavior |
|---|---|---|
| Codex | `AGENTS.md`, Codex skills, MCP servers, sandbox and approval policy | Plugin adapter. Explicit TasteD or TasteDistill use may initialize `~/.tastedistill`, the current project profile, and the current repo CodeGraph index when inside a Git repository and CodeGraph tools are available. Do not rewrite Codex instruction files by default. |
| Claude Code | `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`, Claude auto memory | Reference adapter. Generate snippets that import or reference TasteDistill. Do not write Claude memory files unless the user explicitly asks. |

## Non-Override Rules

- Do not automatically write host global memory files such as `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`.
- Do not automatically write project instruction files such as `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, or repository docs.
- Do not copy raw host memory, raw transcripts, secrets, `.env` content, tokens, or private logs into TasteDistill.
- Do not duplicate the full TasteDistill profile into host memory. Host files should reference TasteDistill or contain a short adapter snippet.
- Do not bypass the host agent's sandbox, approval policy, or permission model.
- Do not treat TasteDistill as active unless the user explicitly invokes the TasteD/TasteDistill plugin or a `tasted-*` skill.
- Do not treat host-private skills named in project instructions as part of TasteDistill. If `AGENTS.md`, `CLAUDE.md`, or another host instruction references private or legacy skills, the host decides whether those skills are installed and routable before TasteDistill runs. TasteDistill must not search for, load, or preserve fallback behavior for unavailable host skills.
- Do not execute helper scripts from a guessed host skill path such as `$HOME/.codex/skills/<skill>/scripts/...`. If a helper is needed, resolve it relative to the actual `SKILL.md` file that was loaded. If that path is missing, report the missing helper and continue with a manual check.

## Host Detection

Prefer explicit host signals over guessing:

1. Current plugin or skill namespace when available.
2. Known instruction surfaces in the current agent session.
3. Environment-specific home directories or config paths.
4. User wording such as Codex or Claude Code.

If the host is unclear, follow the safest common path: load or create `~/.tastedistill` only, do not write host files, and report the adapter snippet instead of applying it.

## Adapter Snippets

### Codex

Codex may load TasteDistill through the plugin and skills. If the user asks for manual wiring, propose a short instruction instead of rewriting existing files automatically:

```text
At the start of ordinary work, lightly read ~/.tastedistill/profile.md, ~/.tastedistill/harness.md, and ~/.tastedistill/rules.jsonl when present. Use them as distilled cross-agent preferences and rules.

Do not read raw Codex/Claude histories during ordinary work. Only refresh host memory when the user asks to sync, refresh, import, or distill memory.

For project work, if a matching ~/.tastedistill/projects/<project-id>/project.md exists, load it lightly. Do not bulk-read lessons.jsonl unless the task needs project history.
```

### Claude Code

Generate this snippet unless the user asks to write it:

```md
# TasteDistill

At the start of ordinary work, lightly read @~/.tastedistill/profile.md, @~/.tastedistill/harness.md, and @~/.tastedistill/rules.jsonl when present. Use them as distilled cross-agent preferences and rules.

Do not read raw Codex/Claude histories during ordinary work. Only refresh host memory when the user asks to sync, refresh, import, or distill memory.

For project work, if a matching ~/.tastedistill/projects/<project-id>/project.md exists, load it lightly. Do not bulk-read lessons.jsonl unless the task needs project history.
Do not copy raw TasteDistill content into CLAUDE.md.
```

## Safety Response

When a requested integration would modify host memory, identity, config, or project instructions, state the target file and risk first. Proceed only after the user explicitly asks for that write.

## Host Instruction Boundaries

Project instruction files may mention the user's older or private workflow skills. Treat those mentions as host context, not as TasteDistill dependencies.

- Use project instructions for user preferences, boundaries, and local workflow expectations.
- Do not load or invoke unrelated host-private skills merely because they are listed as a recommended sequence.
- Do not ask TasteDistill to adjudicate removed, unavailable, or host-owned skill routing. That is a host-agent responsibility.
- If a TasteD/TasteDistill call has reached this rule, the host has already selected TasteDistill; use the native `tasted-*` skill for the requested stage.
- When you do inspect a host-private skill for compatibility, keep all file, script, and asset paths anchored to the actual file path you opened.
