# Codex Self-Learning Skills

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-111827?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-2563eb?style=for-the-badge"></a>
</p>

A Codex-native self-learning loop for turning repeated development work into reusable agent behavior: research, decide, design, implement, debug, ship, and distill.

## Goals

- Help Codex use your accumulated memory, preferences, project context, and task evidence more consistently across future work.
- Turn repeated development lessons, mistakes, preferences, and verification habits into reusable skill behavior.
- Split behavior by engineering stage instead of relying on one oversized global prompt.
- Make every stage evidence-oriented, with clear outcome contracts and validation expectations.
- Treat external inspiration as attribution, while keeping the project identity focused on Codex self-learning and continuous evolution.

## Codex-Native Direction

This repository is designed around a feedback loop:

```text
work -> evidence -> lesson -> durable rule -> better next run
```

The skills are intentionally small. Each one defines a phase contract, expected evidence, and failure boundaries. At runtime, they are meant to work together with your local Codex memory, project instructions, repository files, logs, tests, browser state, and current task context. Codex still performs the implementation work directly; the skills shape when to research, when to decide, when to verify, and when to update future behavior.

`codex-distill` is the differentiating layer. It turns completed work, failed attempts, user corrections, logs, diffs, and verification results into durable rules. Personal memory and private project facts can remain local while reusable behavior is promoted into skills or shared rules.

## Workflow

Recommended sequence:

```text
codex-learn -> codex-think -> codex-design -> implementation -> codex-debug -> codex-ship -> codex-distill
```

| Stage | Skill | Purpose |
|---|---|---|
| Learn | `codex-learn` | Research unfamiliar domains, synthesize materials, and build a fact base. |
| Think | `codex-think` | Make product or architecture decisions, define scope, and produce an execution plan. |
| Design | `codex-design` | Handle product direction, interaction principles, UI structure, and visual verification. |
| Implement | Codex implementation | Use Codex's native engineering capability to build the change. |
| Debug | `codex-debug` | Reproduce issues, prove root cause, make minimal fixes, and verify regressions. |
| Ship | `codex-ship` | Review readiness, acceptance, release, and PR/issue follow-through. |
| Distill | `codex-distill` | Extract reusable rules from completed work and update durable guidance. |

## Skills

| Skill | Purpose |
|---|---|
| `codex-learn` | Research unfamiliar domains and structure source material before decisions. |
| `codex-think` | Turn rough ideas into decision-ready plans with tradeoffs and risks. |
| `codex-design` | Define product, interaction, and UI execution rules before visual implementation. |
| `codex-debug` | Diagnose failures with reproducible evidence and minimal fixes. |
| `codex-ship` | Review readiness, acceptance, release, and delivery follow-through. |
| `codex-distill` | Convert completed work into reusable rules that improve future Codex runs. |

## Installation

### 1. Clone

If this repository is private, make sure your GitHub account has access first.

```bash
git clone https://github.com/sssstwee/codex-self-learning-skills.git
cd codex-self-learning-skills
```

### 2. Check the Codex Skills Directory

The default install directory is usually:

```bash
mkdir -p "$HOME/.codex/skills"
```

### 3. Install All Skills

Symlinks are recommended so updates from `git pull` are picked up automatically.

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

### 4. Install One Skill

```bash
ln -s "$PWD/skills/codex-debug" "$HOME/.codex/skills/codex-debug"
```

### 5. Verify

After reopening Codex, type:

```text
/codex
```

You should see `Codex Learn`, `Codex Think`, `Codex Design`, `Codex Debug`, `Codex Ship`, and `Codex Distill`.

### 6. Update

```bash
cd /path/to/codex-self-learning-skills
git pull
```

If installed via symlinks, you usually do not need to copy files again. Restart Codex or reload skills to pick up changes.

### 7. Uninstall

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## Repository Layout

```text
skills/
  codex-learn/
  codex-think/
  codex-design/
  codex-debug/
  codex-ship/
  codex-distill/
  shared-rules/
    anti-patterns.md
    routing.md
    self-learning-loop.md
scripts/
  scan-public-safety.sh
```

## Pre-Publish Check

Run the safety scan before publishing changes. This protects the repository itself; it does not prevent users from combining the installed skills with their local Codex memory or private project instructions at runtime.

```bash
bash scripts/scan-public-safety.sh
```

Current policy:

- `README.md` and `README.zh-CN.md` may contain attribution and acknowledgements.
- The public `skills/` files should not contain personal data, machine-specific paths, private project facts, credentials, or source-brand markers.

## Acknowledgements

The staged skill design is inspired by [Waza](https://github.com/tw93/Waza). This repository adapts and evolves that idea for a Codex self-learning loop, with stronger emphasis on evidence-driven execution, delivery preflight, and continuous rule distillation from real work.
