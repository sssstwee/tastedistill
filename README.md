# selfL: Self-Learning Plugin

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-111827?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-2563eb?style=for-the-badge"></a>
</p>

selfL is an agent-oriented self-learning loop for turning repeated development work into reusable behavior: research, decide, design, implement, debug, ship, and distill.

## Goals

- Help coding agents use your accumulated memory, preferences, project context, and task evidence more consistently across future work.
- Turn repeated development lessons, mistakes, preferences, and verification habits into reusable skill behavior.
- Split behavior by engineering stage instead of relying on one oversized global prompt.
- Make every stage evidence-oriented, with clear outcome contracts and validation expectations.

## Agent-Native Direction

This repository is designed around a feedback loop:

```text
work -> evidence -> lesson -> durable rule -> better next run
```

The skills are intentionally small. Each one defines a phase contract, expected evidence, and failure boundaries. At runtime, they are meant to work together with local agent memory, project instructions, repository files, logs, tests, browser state, and current task context. The active coding agent still performs the implementation work directly; the skills shape when to research, when to decide, when to verify, and when to update future behavior.

Use `selfl-distill` after meaningful work is completed. It helps turn user corrections, failed attempts, logs, diffs, and verification results into reusable rules for future agent runs. Personal memory and private project facts can remain local while reusable behavior is promoted into skills or shared rules.

## Personalization

Installing these skills does not automatically read, copy, or summarize your existing Codex or agent conversations and memory. The first explicit `@selfL` or `selfl-*` invocation performs an idempotent personalization bootstrap check. If no local selfL profile exists yet, selfL runs the `selfl-distill` bootstrap before continuing with the requested skill.

The default private profile lives outside this repository:

```text
$HOME/.selfl/profile.md
$HOME/.selfl/bootstrap.json
```

You can also run the bootstrap directly:

```text
Use $selfl-distill to initialize my local personalization. Review my available local agent memory, conversation history, logs, and prior task outcomes. Create a private experience profile outside this repository, summarize my execution preferences, product taste, validation habits, reusable rules, and anti-patterns, then wire it into my global or project agent instructions so future sessions can load it by default. Ask before reading broad personal history or editing instruction files.
```

The bootstrap should handle:

- find available local memory/history sources
- create the private experience profile outside this repository
- add or propose the instruction entry that loads the profile in future sessions
- report what was loaded, what was skipped, and where the profile was saved

Then keep improving it over time:

```text
Use $selfl-distill to extract reusable lessons from this completed task and update my local experience profile.
```

## Built-In CodeGraph MCP

For larger repositories, the Codex plugin includes [CodeGraph](https://github.com/colbymchenry/codegraph) MCP registration so the agent can use a local code knowledge graph for architecture lookup, call-flow tracing, and impact analysis.

When this repository is installed as a Codex plugin, CodeGraph is launched through `npx` when the MCP server is needed. Users do not need to install CodeGraph globally before installing the plugin.

Each repository still needs a local graph index. When you explicitly call the selfL plugin or any selfL skill from inside a Git repository, selfL performs an idempotent CodeGraph bootstrap check for the current repository. If the index is missing, it initializes it automatically before broad repository work.

Manual initialization is also supported:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

When `codegraph_*` MCP tools are available in your current Codex client, these skills will prefer CodeGraph for repository exploration, debugging, and impact analysis. If the current repository has no CodeGraph index yet, explicit selfL use is treated as permission to initialize only that repository and keep `.codegraph/` local via `.git/info/exclude`. If you install the skills without the plugin, run selfL outside a Git repository, or if CodeGraph is unavailable, the skills fall back to normal file search and targeted reads.

## Workflow

Recommended sequence:

```text
selfl-learn -> selfl-think -> selfl-design -> implementation -> selfl-debug -> selfl-ship -> selfl-distill
```

| Stage | Skill | Purpose |
|---|---|---|
| Learn | `selfl-learn` | Research unfamiliar domains, synthesize materials, and build a fact base. |
| Think | `selfl-think` | Make product or architecture decisions, define scope, and produce an execution plan. |
| Design | `selfl-design` | Handle product direction, interaction principles, UI structure, and visual verification. |
| Implement | Agent implementation | Use the active coding agent's engineering capability to build the change. |
| Debug | `selfl-debug` | Reproduce issues, prove root cause, make minimal fixes, and verify regressions. |
| Ship | `selfl-ship` | Review readiness, acceptance, release, and PR/issue follow-through. |
| Distill | `selfl-distill` | Extract reusable rules from completed work and update durable guidance. |

## Skills

| Skill | Purpose |
|---|---|
| `selfl-learn` | Research unfamiliar domains and structure source material before decisions. |
| `selfl-think` | Turn rough ideas into decision-ready plans with tradeoffs and risks. |
| `selfl-design` | Define product, interaction, and UI execution rules before visual implementation. |
| `selfl-debug` | Diagnose failures with reproducible evidence and minimal fixes. |
| `selfl-ship` | Review readiness, acceptance, release, and delivery follow-through. |
| `selfl-distill` | Convert completed work into reusable rules that improve future agent runs. |

## Installation

### Option A: Install As A Codex Plugin

Use the plugin install path when you want the skills and CodeGraph MCP support together. The plugin registers CodeGraph as a local MCP server through `npx`, so users do not need to install CodeGraph separately before installing this project.

In Codex Desktop, add this repository as a plugin marketplace:

```text
Source: sssstwee/open-self-learning-plugin
Git ref: main
Sparse path: leave empty
```

Then install `selfL` from that marketplace.

After installing the plugin, restart Codex. In each repository where you want graph-based code intelligence, explicitly call `@selfL` or a `selfl-*` skill once. selfL will check the local index and initialize it if needed. You can also initialize it manually:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

Codex will use CodeGraph when `codegraph_*` MCP tools are available. If a project is not initialized yet and you explicitly invoked selfL, the skills may create `.codegraph/` for the current repository and keep it out of Git via `.git/info/exclude`.

### Option B: Install Skills Only

Use this path when you only want the skills and do not want the plugin to register MCP tools.

```bash
git clone https://github.com/sssstwee/open-self-learning-plugin.git
cd open-self-learning-plugin
```

#### 1. Check the Codex Skills Directory

The default install directory is usually:

```bash
mkdir -p "$HOME/.codex/skills"
```

#### 2. Install All Skills

Symlinks are recommended so updates from `git pull` are picked up automatically.

```bash
for skill in selfl-learn selfl-think selfl-design selfl-debug selfl-ship selfl-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/plugins/open-self-learning-plugin/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

#### 3. Install One Skill

```bash
ln -s "$PWD/plugins/open-self-learning-plugin/skills/selfl-debug" "$HOME/.codex/skills/selfl-debug"
```

#### 4. Verify

After reopening Codex, type:

```text
/selfl
```

You should see `selfL Learn`, `selfL Think`, `selfL Design`, `selfL Debug`, `selfL Ship`, and `selfL Distill`.

#### 5. Update

```bash
cd /path/to/open-self-learning-plugin
git pull
```

If installed via symlinks, you usually do not need to copy files again. Restart Codex or reload skills to pick up changes.

#### 6. Uninstall

```bash
for skill in selfl-learn selfl-think selfl-design selfl-debug selfl-ship selfl-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## Repository Layout

```text
.agents/
  plugins/
    marketplace.json
plugins/
  open-self-learning-plugin/
    .codex-plugin/
      plugin.json
    .mcp.json
    skills/
      selfl-learn/
      selfl-think/
      selfl-design/
      selfl-debug/
      selfl-ship/
      selfl-distill/
    shared-rules/
      anti-patterns.md
      codegraph.md
      coding-guardrails.md
      routing.md
      self-learning-loop.md
```

## Acknowledgements

Thanks to:

- [Waza](https://github.com/tw93/Waza) for the staged skill design inspiration.
- [Andrej Karpathy](https://github.com/karpathy) for public writing and guidance on practical coding-agent behavior.
- [CodeGraph](https://github.com/colbymchenry/codegraph) for local code knowledge graph ideas and tooling.
