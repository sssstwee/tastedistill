# CodeGraph

Use this rule when CodeGraph MCP tools are available in the current agent session and the task involves repository understanding, architecture lookup, call-flow tracing, or impact analysis.

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

## Fallbacks

- If `codegraph_*` tools are not available, use normal repository search and targeted file reads.
- If the project is not initialized, ask before running `codegraph init -i`.
- If CodeGraph reports stale or pending files, inspect `codegraph_status` and read the named files directly before editing.
- For a precise user-provided file and line, read that file directly; CodeGraph is optional context, not a replacement.

## Editing Rule

Use CodeGraph to locate structure and impact, but read the current target file before making edits. Do not treat index output as a substitute for tests, builds, runtime checks, artifact checks, or release verification.
