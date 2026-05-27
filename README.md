# Codex Self-Learning Skills

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-111827?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-2563eb?style=for-the-badge"></a>
</p>

A self-learning skill set for Codex. It turns repeated development work into a reusable engineering loop: research, decide, design, implement, debug, ship, and distill.

## Goals

- Help Codex convert repeated development lessons, mistakes, preferences, and verification habits into reusable skills.
- Keep the repository generic, without personal memory, machine-specific paths, project-private rules, or credentials.
- Split behavior by engineering stage instead of relying on one oversized global prompt.
- Make every stage evidence-oriented, with clear outcome contracts and validation expectations.

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
| `codex-distill` | Extract reusable lessons from completed work and update durable rules. |

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
scripts/
  scan-public-safety.sh
```

## Pre-Publish Check

Run the safety scan before publishing changes:

```bash
bash scripts/scan-public-safety.sh
```

Current policy:

- `README.md` and `README.zh-CN.md` may contain attribution and acknowledgements.
- `skills/` stays generic and should not contain personal data, machine-specific paths, or source-brand markers.

## Acknowledgements

The staged skill design is inspired by [Waza](https://github.com/tw93/Waza). This repository adapts and optimizes that idea for a Codex self-learning loop, with stronger emphasis on engineering stages, verifiable execution, delivery preflight, and continuous rule distillation from real work.
