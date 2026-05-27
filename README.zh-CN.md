# Codex 自学习 Skills

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-switch-2563eb?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-%E5%BD%93%E5%89%8D-111827?style=for-the-badge"></a>
</p>

一组面向 Codex 的自学习技能模板，用来把开发过程拆成可研究、可判断、可设计、可调试、可交付、可复盘的工程闭环。

## 设计目标

- 让 Codex 能把每次开发中的经验、错误、偏好和验证方式沉淀成可复用技能，而不是每次从零开始。
- 保持内容通用，不包含个人记忆、本机路径、项目私有规则或密钥。
- 按工程阶段拆分技能，避免一个巨大的全局提示吞掉所有上下文。
- 让每个阶段都围绕证据、结果契约和验证方式运行。

## 工作流

推荐顺序：

```text
codex-learn -> codex-think -> codex-design -> implementation -> codex-debug -> codex-ship -> codex-distill
```

| 阶段 | Skill | 用途 |
|---|---|---|
| 学习 | `codex-learn` | 研究陌生领域、消化材料、建立事实底座。 |
| 思考 | `codex-think` | 做产品或架构判断、范围裁剪和执行计划。 |
| 设计 | `codex-design` | 处理产品方向、交互原则、UI 结构和视觉验证。 |
| 实施 | Codex implementation | 由 Codex 原生工程能力直接实现。 |
| 调试 | `codex-debug` | 复现问题、定位根因、最小修复、验证回归。 |
| 交付 | `codex-ship` | 做预交付审查、验收、发布和 PR/issue 收尾。 |
| 沉淀 | `codex-distill` | 从结果中提炼可复用规则并更新技能。 |

## Skills

| Skill | 用途 |
|---|---|
| `codex-learn` | 在决策前研究陌生领域并结构化材料。 |
| `codex-think` | 把粗略想法变成带取舍和风险的可执行计划。 |
| `codex-design` | 定义产品、交互和 UI 执行规则。 |
| `codex-debug` | 用可复现证据诊断故障并做最小修复。 |
| `codex-ship` | 审查交付准备、验收、发布和交付收尾。 |
| `codex-distill` | 从已完成工作中提炼可复用经验并更新规则。 |

## 安装方法

### 1. 克隆仓库

如果仓库是私有仓库，先确保当前 GitHub 账号有访问权限。

```bash
git clone https://github.com/sssstwee/codex-self-learning-skills.git
cd codex-self-learning-skills
```

### 2. 确认 Codex skills 目录

默认安装目录通常是：

```bash
mkdir -p "$HOME/.codex/skills"
```

### 3. 安装全部 skills

推荐使用 symlink，方便后续 `git pull` 更新后自动生效。

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

### 4. 只安装单个 skill

```bash
ln -s "$PWD/skills/codex-debug" "$HOME/.codex/skills/codex-debug"
```

### 5. 验证安装

重新打开 Codex 后，在输入框中尝试输入：

```text
/codex
```

你应该能看到 `Codex Learn`、`Codex Think`、`Codex Design`、`Codex Debug`、`Codex Ship`、`Codex Distill`。

### 6. 更新

```bash
cd /path/to/codex-self-learning-skills
git pull
```

如果使用 symlink 安装，通常不需要重新复制文件；重启 Codex 或刷新 skills 后即可读取更新。

### 7. 卸载

```bash
for skill in codex-learn codex-think codex-design codex-debug codex-ship codex-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## 目录结构

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

## 发布前检查

运行安全扫描，避免把私有信息、机器路径、密钥或不该进入 skill 内容的来源标识发布出去。

```bash
bash scripts/scan-public-safety.sh
```

当前策略：

- `README.md` 和 `README.zh-CN.md` 可以包含来源说明和致谢。
- `skills/` 内容保持通用，不包含个人数据、机器路径或来源品牌标识。

## 致谢

本项目的阶段化技能设计思想来源于 [Waza](https://github.com/tw93/Waza)，并在此基础上针对 Codex 的自学习闭环做了优化：更强调工程阶段拆分、可验证执行、交付前检查、以及从真实任务中持续提炼规则。
