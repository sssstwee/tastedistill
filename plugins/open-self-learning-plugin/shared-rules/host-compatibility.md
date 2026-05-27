# Host Compatibility

Use this rule whenever selfL runs inside, or prepares instructions for, a host coding agent.

selfL is a portable engineering profile and harness layer. The host agent remains the execution runtime. selfL must not replace the host's memory system, identity file, permission model, tool policy, or native routing.

## Supported Hosts In v1

| Host | Native surface | selfL behavior |
|---|---|---|
| Codex | `AGENTS.md`, Codex skills, MCP servers, sandbox and approval policy | Full v1 adapter. Explicit selfL use may initialize `~/.selfl`, the current repo project profile, and the current repo CodeGraph index. Do not rewrite Codex instruction files by default. |
| Claude Code | `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`, Claude auto memory | Reference adapter. Generate snippets that import or reference selfL. Do not write Claude memory files unless the user explicitly asks. |
| Hermes | `~/.hermes/SOUL.md`, `~/.hermes/memories/`, `~/.hermes/skills/`, `~/.hermes/config.yaml`, `~/.hermes/.env` | External profile adapter. Generate a selfL reference. Do not change Hermes identity, memories, skills, config, or secrets unless the user explicitly asks. |

## Non-Override Rules

- Do not automatically write host global memory files such as `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.hermes/SOUL.md`, or `~/.hermes/memories/*`.
- Do not automatically write project instruction files such as `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, or repository docs.
- Do not copy raw host memory, raw transcripts, secrets, `.env` content, tokens, or private logs into selfL.
- Do not duplicate the full selfL profile into host memory. Host files should reference selfL or contain a short adapter snippet.
- Do not bypass the host agent's sandbox, approval policy, or permission model.
- Do not treat selfL as active unless the user explicitly invokes the selfL plugin or a `selfl-*` skill.

## Host Detection

Prefer explicit host signals over guessing:

1. Current plugin or skill namespace when available.
2. Known instruction surfaces in the current agent session.
3. Environment-specific home directories or config paths.
4. User wording such as Codex, Claude Code, or Hermes.

If the host is unclear, follow the safest common path: load or create `~/.selfl` only, do not write host files, and report the adapter snippet instead of applying it.

## Adapter Snippets

### Codex

Codex may load selfL through the plugin and skills. If the user asks for manual wiring, propose a short instruction instead of rewriting existing files automatically:

```text
When selfL is explicitly invoked, load ~/.selfl/profile.md and ~/.selfl/harness.md. If working inside a Git repository and a matching selfL project profile exists, load that project profile before running the selected selfL workflow.
```

### Claude Code

Generate this snippet unless the user asks to write it:

```md
# selfL

When working with my projects, read @~/.selfl/profile.md and @~/.selfl/harness.md for my personal engineering preferences.

If inside a Git repository, ask before loading the matching selfL project profile from ~/.selfl/projects/.
Do not copy raw selfL content into CLAUDE.md.
```

### Hermes

Generate this snippet unless the user asks to write it:

```md
# selfL external profile

Use ~/.selfl/profile.md and ~/.selfl/harness.md as an external engineering preference source.
Do not import secrets, ~/.hermes/.env, or raw conversation logs.
Keep Hermes SOUL.md as the source of agent identity.
```

## Safety Response

When a requested integration would modify host memory, identity, config, or project instructions, state the target file and risk first. Proceed only after the user explicitly asks for that write.
