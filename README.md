# TasteDistill

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-111827?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-2563eb?style=for-the-badge"></a>
</p>

TasteDistill is a portable taste distillation layer for coding agents. It turns your development experience, product taste, interaction principles, validation habits, and project rules into reusable behavior across Codex, Claude Code, and Hermes.

## Goals

- Help coding agents use your accumulated memory, preferences, project context, and task evidence more consistently across future work.
- Keep your personal engineering profile portable across Codex, Claude Code, and Hermes instead of locking it inside one agent's memory system.
- Turn repeated development lessons, mistakes, preferences, and verification habits into reusable skill behavior.
- Split behavior by engineering stage instead of relying on one oversized global prompt.
- Make every stage evidence-oriented, with clear outcome contracts and validation expectations.

## Portable Harness

TasteDistill does not replace your host agent. Codex, Claude Code, and Hermes remain the execution runtimes. TasteDistill provides a local, portable profile and harness layer that those agents can reference.

```text
TasteDistill is the source of truth
host agent is the execution runtime
adapter lets the host read TasteDistill
```

The default local profile layout is:

```text
$HOME/.tastedistill/
  manifest.json
  profile.md
  profile.json
  harness.md
  bootstrap.json
  sources.json
  adapters/
    codex.md
    claude.md
    hermes.md
  projects/
    <repo-id>/
      project.md
      project.json
      lessons.jsonl
      sources.json
```

- `profile.md` stores cross-agent personal engineering preferences: communication, product taste, execution habits, and verification habits.
- `harness.md` stores the runtime contract: context loading, tool preference, permission boundaries, verification, delivery, and distillation policy.
- `adapters/*.md` stores host-specific loading snippets. These snippets are not automatically written into host memory.
- `projects/<repo-id>/` stores project-specific harness notes outside the business repository.

## Host Compatibility

TasteDistill v1 supports Codex, Claude Code, and Hermes with different adapter behavior.

| Host | Behavior | Default write policy |
|---|---|---|
| Codex | Plugin adapter. Explicit `@TasteDistill` or `tastedistill-*` use can create `~/.tastedistill`, create project profiles, and initialize CodeGraph for the current Git repository when CodeGraph tools are available. | May write under `~/.tastedistill`, current repo `.codegraph/`, and `.git/info/exclude`. Does not rewrite `AGENTS.md` by default. |
| Claude Code | Reference adapter. TasteDistill generates a snippet that can import or reference `~/.tastedistill/profile.md` and `~/.tastedistill/harness.md`. | Does not write `~/.claude/CLAUDE.md`, project `CLAUDE.md`, `.claude/CLAUDE.md`, or Claude auto memory unless explicitly requested. |
| Hermes | External profile adapter. TasteDistill generates a snippet for using `~/.tastedistill` as an external engineering preference source. | Does not write `~/.hermes/SOUL.md`, `~/.hermes/memories/*`, `~/.hermes/skills/*`, config, or `.env` unless explicitly requested. |

This avoids the main integration conflicts:

- no automatic writes to host memory
- no replacement of host identity or system instructions
- no full-copy sync of the TasteDistill profile into every host
- no bypassing host permissions, sandboxing, or approval policy

## Agent-Native Direction

This repository is designed around a feedback loop:

```text
work -> evidence -> lesson -> durable rule -> better next run
```

The skills are intentionally small. Each one defines a phase contract, expected evidence, and failure boundaries. At runtime, they are meant to work together with local agent memory, project instructions, repository files, logs, tests, browser state, and current task context. The active coding agent still performs the implementation work directly; the skills shape when to research, when to decide, when to verify, and when to update future behavior.

Use `tastedistill-distill` after meaningful work is completed. It helps turn user corrections, failed attempts, logs, diffs, and verification results into reusable rules for future agent runs. Personal memory and private project facts can remain local while reusable behavior is promoted into skills or shared rules.

## Personalization

Installing these skills does not automatically read, copy, or summarize your existing Codex, Claude Code, Hermes, or other agent conversations and memory. The first explicit `@TasteDistill` or `tastedistill-*` invocation performs an idempotent personalization bootstrap check. If no local TasteDistill profile exists yet, TasteDistill runs the `tastedistill-distill` bootstrap before continuing with the requested skill.

The default private profile lives outside this repository:

```text
$HOME/.tastedistill/profile.md
$HOME/.tastedistill/harness.md
$HOME/.tastedistill/bootstrap.json
```

If you already have durable host-specific experience files, TasteDistill treats them as sources, not targets to overwrite. For example, a Codex experience document can seed the TasteDistill profile without forcing a new broad transcript sweep.

You can also run the bootstrap directly:

```text
Use $tastedistill-distill to initialize my local TasteDistill profile. Review my available local agent memory, conversation history, logs, and prior task outcomes. Create a private portable engineering profile under ~/.tastedistill, summarize my execution preferences, product taste, validation habits, reusable rules, and anti-patterns, then generate Codex, Claude Code, and Hermes adapter snippets. Ask before reading broad personal history or editing host instruction files.
```

The bootstrap should handle:

- find available local memory/history sources
- create the private experience profile and harness outside this repository
- generate host adapter snippets without overwriting host memory
- report what was loaded, what was skipped, and where the profile was saved

Then keep improving it over time:

```text
Use $tastedistill-distill to extract reusable lessons from this completed task and update my local TasteDistill profile or project harness.
```

## Built-In CodeGraph MCP

For larger repositories, TasteDistill can use [CodeGraph](https://github.com/colbymchenry/codegraph) as a local code knowledge graph for architecture lookup, call-flow tracing, and impact analysis.

When this repository is installed as a Codex plugin, CodeGraph is launched through `npx` when the MCP server is needed. Users do not need to install CodeGraph globally before installing the plugin. Other hosts can follow the same CodeGraph rules when they expose compatible MCP/tools.

Each repository still needs a local graph index. When you explicitly call the TasteDistill plugin or any TasteDistill skill from inside a Git repository, TasteDistill performs an idempotent CodeGraph bootstrap check for the current repository. If the index is missing, it initializes it automatically before broad repository work.

Manual initialization is also supported:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

When `codegraph_*` MCP tools are available in the current host, these skills will prefer CodeGraph for repository exploration, debugging, and impact analysis. If the current repository has no CodeGraph index yet, explicit TasteDistill use is treated as permission to initialize only that repository and keep `.codegraph/` local via `.git/info/exclude`. If you install the skills without the plugin, run TasteDistill outside a Git repository, or if CodeGraph is unavailable, the skills fall back to normal file search and targeted reads.

## Workflow

Recommended sequence:

```text
tastedistill-learn -> tastedistill-think -> tastedistill-design -> implementation -> tastedistill-debug -> tastedistill-ship -> tastedistill-distill
```

| Stage | Skill | Purpose |
|---|---|---|
| Learn | `tastedistill-learn` | Research unfamiliar domains, synthesize materials, and build a fact base. |
| Think | `tastedistill-think` | Make product or architecture decisions, define scope, and produce an execution plan. |
| Design | `tastedistill-design` | Handle product direction, interaction principles, UI structure, and visual verification. |
| Implement | Agent implementation | Use the active coding agent's engineering capability to build the change. |
| Debug | `tastedistill-debug` | Reproduce issues, prove root cause, make minimal fixes, and verify regressions. |
| Ship | `tastedistill-ship` | Review readiness, acceptance, release, and PR/issue follow-through. |
| Distill | `tastedistill-distill` | Extract reusable rules from completed work and update durable guidance. |

## Skills

| Skill | Purpose |
|---|---|
| `tastedistill-learn` | Research unfamiliar domains and structure source material before decisions. |
| `tastedistill-think` | Turn rough ideas into decision-ready plans with tradeoffs and risks. |
| `tastedistill-design` | Define product, interaction, and UI execution rules before visual implementation. |
| `tastedistill-debug` | Diagnose failures with reproducible evidence and minimal fixes. |
| `tastedistill-ship` | Review readiness, acceptance, release, and delivery follow-through. |
| `tastedistill-distill` | Convert completed work into reusable rules that improve future agent runs. |

## Installation

### Option A: Install As A Codex Plugin

Use the plugin install path when you want the skills and CodeGraph MCP support together in Codex. The plugin registers CodeGraph as a local MCP server through `npx`, so users do not need to install CodeGraph separately before installing this project.

In Codex Desktop, add this repository as a plugin marketplace:

```text
Source: sssstwee/tastedistill
Git ref: main
Sparse path: leave empty
```

Then install `TasteDistill` from that marketplace.

After installing the plugin, restart Codex. In each repository where you want graph-based code intelligence, explicitly call `@TasteDistill` or a `tastedistill-*` skill once. TasteDistill will check the local index and initialize it if needed. You can also initialize it manually:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

TasteDistill will use CodeGraph when `codegraph_*` MCP tools are available. If a project is not initialized yet and you explicitly invoked TasteDistill, the skills may create `.codegraph/` for the current repository and keep it out of Git via `.git/info/exclude`.

### Option B: Install Skills Only

Use this path when you only want the skills and do not want the plugin to register MCP tools.

```bash
git clone https://github.com/sssstwee/tastedistill.git
cd tastedistill
```

#### 1. Check the Codex Skills Directory

The default install directory is usually:

```bash
mkdir -p "$HOME/.codex/skills"
```

#### 2. Install All Skills

Symlinks are recommended so updates from `git pull` are picked up automatically.

```bash
for skill in tastedistill-learn tastedistill-think tastedistill-design tastedistill-debug tastedistill-ship tastedistill-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/plugins/tastedistill/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

#### 3. Install One Skill

```bash
ln -s "$PWD/plugins/tastedistill/skills/tastedistill-debug" "$HOME/.codex/skills/tastedistill-debug"
```

#### 4. Verify

After reopening Codex, type:

```text
/tastedistill
```

You should see `TasteDistill Learn`, `TasteDistill Think`, `TasteDistill Design`, `TasteDistill Debug`, `TasteDistill Ship`, and `TasteDistill Distill`.

#### 5. Update

```bash
cd /path/to/tastedistill
git pull
```

If installed via symlinks, you usually do not need to copy files again. Restart Codex or reload skills to pick up changes.

#### 6. Uninstall

```bash
for skill in tastedistill-learn tastedistill-think tastedistill-design tastedistill-debug tastedistill-ship tastedistill-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## Repository Layout

```text
.agents/
  plugins/
    marketplace.json
plugins/
  tastedistill/
    .codex-plugin/
      plugin.json
    .mcp.json
    skills/
      tastedistill-learn/
      tastedistill-think/
      tastedistill-design/
      tastedistill-debug/
      tastedistill-ship/
      tastedistill-distill/
    shared-rules/
      anti-patterns.md
      codegraph.md
      coding-guardrails.md
      host-compatibility.md
      personalization.md
      portable-profile.md
      routing.md
      taste-distillation-loop.md
```

## Acknowledgements

Thanks to:

- [Waza](https://github.com/tw93/Waza) for the staged skill design inspiration.
- [Andrej Karpathy](https://github.com/karpathy) for public writing and guidance on practical coding-agent behavior.
- [CodeGraph](https://github.com/colbymchenry/codegraph) for local code knowledge graph ideas and tooling.
