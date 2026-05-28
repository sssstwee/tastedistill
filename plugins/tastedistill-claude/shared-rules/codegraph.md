# CodeGraph

Use this rule when a TasteD/TasteDistill plugin or skill is explicitly invoked in a repository context, and when CodeGraph MCP tools are available in the current agent session.

In v1, the Codex plugin ships with CodeGraph MCP registration. CodeGraph itself is not Codex-specific: when the current host exposes compatible `codegraph_*` tools, TasteDistill may follow the same bootstrap and usage rules.

On explicit TasteD or TasteDistill use, perform the Index Bootstrap check before broad repository work. The user should not need to ask for CodeGraph initialization separately.

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

When a TasteD/TasteDistill plugin or skill is explicitly invoked in a host session where CodeGraph tools are available, treat that explicit use as permission to bootstrap CodeGraph for the current repository.

Before broad repository work, first check whether the current directory is inside a Git worktree with `git rev-parse --show-toplevel`. If that fails, skip CodeGraph status and initialization, then fall back to normal search and targeted file reads. Report that the current directory is not a Git repository.

If the current directory is inside a Git worktree, call `codegraph_status` for that repository root when available. If CodeGraph reports that the current project is not initialized, or if `codegraph_*` tools are available but cannot serve the current repository because the local index is missing:

1. Run `npx -y @colbymchenry/codegraph init -i` from that repository root.
2. Keep the generated index local by adding `.codegraph/` to `.git/info/exclude` if the repository has a `.git` directory and the entry is not already present.
3. Re-check `codegraph_status` or retry the intended `codegraph_*` lookup.
4. Report that CodeGraph was initialized for the current repository.

This bootstrap is idempotent: if the repository is already initialized, continue without running init again.

Do not initialize unrelated repositories, home directories, or parent folders. If the current directory is not a repository or the initialization command fails, fall back to normal search and targeted file reads, then report the fallback.

## Fallbacks

- If `codegraph_*` tools are not available, use normal repository search and targeted file reads.
- If the user did not explicitly invoke TasteD or TasteDistill and the project is not initialized, ask before running `npx -y @colbymchenry/codegraph init -i`.
- If CodeGraph reports stale or pending files, inspect `codegraph_status` and read the named files directly before editing.
- For a precise user-provided file and line, read that file directly; CodeGraph is optional context, not a replacement.

## Editing Rule

Use CodeGraph to locate structure and impact, but read the current target file before making edits. Do not treat index output as a substitute for tests, builds, runtime checks, artifact checks, or release verification.
