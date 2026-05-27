# Codex 自学习 Skills

一组面向 Codex 的可复用技能模板，用于把开发过程拆成可沉淀、可验证、可迭代的工程阶段。

## Skill Flow

Recommended sequence:

```text
codex-learn -> codex-think -> codex-design -> implementation -> codex-debug -> codex-ship -> codex-distill
```

## Skills

| Skill | Purpose |
|---|---|
| `codex-learn` | Research unfamiliar domains and structure source material before decisions. |
| `codex-think` | Turn rough ideas into decision-ready plans with tradeoffs and risks. |
| `codex-design` | Define product, interaction, and UI execution rules before visual implementation. |
| `codex-debug` | Diagnose failures with reproducible evidence and minimal fixes. |
| `codex-ship` | Review readiness, acceptance, release, and delivery follow-through. |
| `codex-distill` | Extract reusable lessons from completed work and update durable rules. |

## Install

Copy or symlink the wanted folders under `skills/` into your Codex skills directory.

Example:

```bash
ln -s "$PWD/skills/codex-learn" "$HOME/.codex/skills/codex-learn"
```

## Safety

This repository is intentionally generic:

- no personal memory
- no machine-specific paths
- no secrets or credentials
- no project-specific release rituals
- no third-party framework branding copied from another skill set

Run the local scan before publishing changes:

```bash
bash scripts/scan-public-safety.sh
```

