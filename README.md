# Codex 自学习 Skills

一组面向 Codex 的自学习技能模板，用来把开发过程拆成可研究、可判断、可设计、可调试、可交付、可复盘的工程闭环。

This repository provides a self-learning skill set for Codex. It turns repeated development work into a reusable loop: research, decide, design, implement, debug, ship, and distill.

## 设计目标 / Goals

- 中文：让 Codex 能把每次开发中的经验、错误、偏好和验证方式沉淀成可复用技能，而不是每次从零开始。
- English: Help Codex convert repeated development lessons, mistakes, preferences, and verification habits into reusable skills.
- 中文：保持内容通用，不包含个人记忆、本机路径、项目私有规则或密钥。
- English: Keep the repository generic, without personal memory, machine-specific paths, project-private rules, or credentials.
- 中文：按工程阶段拆分技能，避免一个巨大的全局提示吞掉所有上下文。
- English: Split behavior by engineering stage instead of relying on one oversized global prompt.

## 工作流 / Workflow

推荐顺序：

Recommended sequence:

```text
codex-learn -> codex-think -> codex-design -> implementation -> codex-debug -> codex-ship -> codex-distill
```

含义：

Meaning:

| 阶段 | Skill | 用途 |
|---|---|---|
| 学习 | `codex-learn` | 研究陌生领域、消化材料、建立事实底座 |
| 思考 | `codex-think` | 做方案判断、架构取舍、范围裁剪和执行计划 |
| 设计 | `codex-design` | 处理产品方向、交互原则、UI 结构和视觉验证 |
| 实施 | Codex implementation | 由 Codex 原生工程能力直接实现 |
| 调试 | `codex-debug` | 复现问题、定位根因、最小修复、验证回归 |
| 交付 | `codex-ship` | 做预交付审查、验收、发布和 PR/issue 收尾 |
| 沉淀 | `codex-distill` | 从结果中提炼可复用规则并更新技能 |

## Skills

| Skill | Purpose |
|---|---|
| `codex-learn` | Research unfamiliar domains and structure source material before decisions. |
| `codex-think` | Turn rough ideas into decision-ready plans with tradeoffs and risks. |
| `codex-design` | Define product, interaction, and UI execution rules before visual implementation. |
| `codex-debug` | Diagnose failures with reproducible evidence and minimal fixes. |
| `codex-ship` | Review readiness, acceptance, release, and delivery follow-through. |
| `codex-distill` | Extract reusable lessons from completed work and update durable rules. |

## 安装方法 / Installation

### 1. 克隆仓库 / Clone

如果仓库是私有仓库，先确保当前 GitHub 账号有访问权限。

If this repository is private, make sure your GitHub account has access first.

```bash
git clone https://github.com/sssstwee/codex-self-learning-skills.git
cd codex-self-learning-skills
```

### 2. 确认 Codex skills 目录 / Check Codex Skills Directory

默认安装目录通常是：

The default install directory is usually:

```bash
mkdir -p "$HOME/.codex/skills"
```

### 3. 安装全部 skills / Install All Skills

推荐使用 symlink，方便后续 `git pull` 更新后自动生效。

Symlinks are recommended so updates from `git pull` are picked up automatically.

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

### 4. 只安装单个 skill / Install One Skill

```bash
ln -s "$PWD/skills/codex-debug" "$HOME/.codex/skills/codex-debug"
```

### 5. 验证安装 / Verify

重新打开 Codex 后，在输入框中尝试输入：

After reopening Codex, type:

```text
/codex
```

你应该能看到 `Codex Learn`、`Codex Think`、`Codex Design`、`Codex Debug`、`Codex Ship`、`Codex Distill`。

You should see `Codex Learn`, `Codex Think`, `Codex Design`, `Codex Debug`, `Codex Ship`, and `Codex Distill`.

### 6. 更新 / Update

```bash
cd /path/to/codex-self-learning-skills
git pull
```

如果你使用 symlink 安装，通常不需要重新复制文件；重启 Codex 或刷新 skills 后即可读取更新。

If installed via symlinks, you usually do not need to copy files again. Restart Codex or reload skills to pick up changes.

### 7. 卸载 / Uninstall

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## 目录结构 / Repository Layout

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

## 发布前检查 / Pre-Publish Check

运行安全扫描，避免把私有信息、机器路径、密钥或不该进入 skill 内容的来源标识发布出去。

Run the safety scan before publishing changes:

```bash
bash scripts/scan-public-safety.sh
```

当前策略：

Current policy:

- `README.md` 可以包含来源说明和致谢。
- `README.md` may contain attribution and acknowledgements.
- `skills/` 内容保持通用，不包含个人数据、机器路径或来源品牌标识。
- `skills/` stays generic and should not contain personal data, machine-specific paths, or source-brand markers.

## 致谢 / Acknowledgements

本项目的阶段化技能设计思想来源于 [Waza](https://github.com/tw93/Waza)，并在此基础上针对 Codex 的自学习闭环做了优化：更强调工程阶段拆分、可验证执行、交付前检查、以及从真实任务中持续提炼规则。

The staged skill design is inspired by [Waza](https://github.com/tw93/Waza). This repository adapts and optimizes that idea for a Codex self-learning loop, with stronger emphasis on engineering stages, verifiable execution, delivery preflight, and continuous rule distillation from real work.

