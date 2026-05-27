# Codex 自学习 Skills

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-switch-2563eb?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-%E5%BD%93%E5%89%8D-111827?style=for-the-badge"></a>
</p>

一套 Codex-native 的自学习闭环，用来把重复开发过程沉淀成可复用的 agent 行为：研究、判断、设计、实施、调试、交付、复盘。

## 设计目标

- 让 Codex 更稳定地结合你的本地记忆、个人偏好、项目上下文和当前任务证据来完成后续工作。
- 把重复出现的开发经验、错误、偏好和验证方式沉淀成可复用的 skill 行为。
- 按工程阶段拆分技能，避免一个巨大的全局提示吞掉所有上下文。
- 让每个阶段都围绕证据、结果契约和验证方式运行。

## Codex 原生方向

本仓库围绕一个反馈闭环设计：

```text
work -> evidence -> lesson -> durable rule -> better next run
```

每个 skill 都刻意保持小而清晰：定义阶段契约、所需证据和失败边界。运行时，它们应该与你本地的 Codex memory、项目 instructions、仓库文件、日志、测试、浏览器状态和当前任务上下文一起工作。真正的代码实施仍由 Codex 原生工程能力完成；skills 负责约束什么时候研究、什么时候判断、什么时候验证、什么时候把经验更新为未来可复用行为。

完成一次有价值的任务后，可以使用 `codex-distill`。它会帮助你把用户纠正、失败尝试、日志、diff 和验证结果提炼成后续 Codex 可复用的规则。个人记忆和私有项目事实可以继续保留在本地，而可复用的行为模式再沉淀进 skills 或 shared rules。

## 个性化初始化

安装这些 skills 不会自动读取、复制或总结你已有的 Codex 对话记录和记忆。安装只是让工作流可用；读取个人历史和修改本地 instructions 应该发生在你明确运行 `codex-distill` 之后。

安装完成后，建议运行一次 `codex-distill`，让它完成初始化：

```text
使用 $codex-distill 初始化我的本地个性化配置。阅读并整理我当前可用的本地 Codex memory、对话记录、日志和历史任务结果。请在这个仓库之外创建一份私有经验档案，总结我的执行偏好、产品审美、验证习惯、可复用规则和反模式，并把它接入我的全局或项目 Codex instructions，让后续会话可以默认加载。读取大范围个人历史或修改 instructions 文件前先确认。
```

`codex-distill` 应该处理完整 bootstrap：

- 发现当前可用的本地 memory / history 来源
- 在仓库之外创建私有经验档案
- 添加或给出可加载该档案的 instructions 入口
- 报告读取了哪些来源、跳过了哪些来源、档案保存在哪里

后续完成重要任务后，可以继续沉淀：

```text
使用 $codex-distill 从这次已完成任务中提炼可复用经验，并更新我的本地经验档案。
```

## 可选增强：CodeGraph

对于较大的代码仓库，可以接入 [CodeGraph](https://github.com/colbymchenry/codegraph)，让 Codex 使用本地代码知识图谱来理解架构、追踪调用链和分析影响面。

单独安装 CodeGraph：

```bash
npx @colbymchenry/codegraph
```

初始化项目：

```bash
cd your-project
codegraph init -i
```

当当前 Codex 客户端能看到 `codegraph_*` MCP tools 时，这些 skills 会优先用 CodeGraph 做仓库探索、排障和影响面分析。若 CodeGraph 不可用，则回退到普通文件搜索和定向读取。

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
| `codex-distill` | 将已完成工作转化为可复用规则，让后续 Codex 执行持续变好。 |

## 安装方法

### 1. 克隆仓库

克隆仓库：

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
    anti-patterns.md
    codegraph.md
    coding-guardrails.md
    routing.md
    self-learning-loop.md
```

## 致谢

感谢：

- [Waza](https://github.com/tw93/Waza) 提供阶段化技能设计思想启发。
- [Andrej Karpathy](https://github.com/karpathy) 关于实用 coding agent 行为的公开写作与经验启发。
- [CodeGraph](https://github.com/colbymchenry/codegraph) 提供本地代码知识图谱的思路与工具支持。
