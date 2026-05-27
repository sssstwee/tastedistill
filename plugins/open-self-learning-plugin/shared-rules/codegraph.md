# CodeGraph

Use this rule when a selfL plugin or skill is explicitly invoked in a repository context, and when CodeGraph MCP tools are available in the current agent session.

In v1, automatic CodeGraph bootstrap is part of the Codex adapter. For Claude Code and Hermes, do not initialize CodeGraph by default unless equivalent tools are available and the user explicitly asks for that integration.

On explicit selfL use, perform the Index Bootstrap check before broad repository work. The user should not need to ask for CodeGraph initialization separately.

## When To Use

- Unfamiliar repository or module exploration.
- Architecture questions that need entry points, related symbols, or existing patterns.
- Root-cause analysis that needs callers, callees, request flow, state flow, or symbol trace.
- Review or delivery work that needs impact radius before approving a non-trivial change.
- Large repositories where broad `rg` / file-read exploration would be noisy.

## Tool Routing

| Need | Prefer |
|---|---|
| Map an area or task | `codegraph_context` |
| Explore several related symbols together | `codegraph_explore` |
| Find a symbol by name | `codegraph_search` |
| Trace "how does X reach Y" | `codegraph_trace` |
| Inspect one-hop flow | `codegraph_callers` / `codegraph_callees` |
| Estimate affected code before editing | `codegraph_impact` |
| Check index health or staleness | `codegraph_status` |

## Index Bootstrap

When a selfL plugin or skill is explicitly invoked through Codex, treat that explicit selfL use as permission to bootstrap CodeGraph for the current repository.

Before broad repository work, call `codegraph_status` when available. If CodeGraph reports that the current project is not initialized, or if `codegraph_*` tools are available but cannot serve the current repository because the local index is missing:

1. Resolve the current repository root with `git rev-parse --show-toplevel` when inside a Git worktree.
2. Run `npx -y @colbymchenry/codegraph init -i` from that repository root.
3. Keep the generated index local by adding `.codegraph/` to `.git/info/exclude` if the repository has a `.git` directory and the entry is not already present.
4. Re-check `codegraph_status` or retry the intended `codegraph_*` lookup.
5. Report that CodeGraph was initialized for the current repository.

This bootstrap is idempotent: if the repository is already initialized, continue without running init again.

Do not initialize unrelated repositories, home directories, or parent folders. If the current directory is not a repository or the initialization command fails, fall back to normal search and targeted file reads, then report the fallback.

## Fallbacks

- If `codegraph_*` tools are not available, use normal repository search and targeted file reads.
- If the user did not explicitly invoke selfL and the project is not initialized, ask before running `npx -y @colbymchenry/codegraph init -i`.
- If CodeGraph reports stale or pending files, inspect `codegraph_status` and read the named files directly before editing.
- For a precise user-provided file and line, read that file directly; CodeGraph is optional context, not a replacement.

## Editing Rule

Use CodeGraph to locate structure and impact, but read the current target file before making edits. Do not treat index output as a substitute for tests, builds, runtime checks, artifact checks, or release verification.
