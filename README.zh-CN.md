# selfL：自学习插件

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-switch-2563eb?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-%E5%BD%93%E5%89%8D-111827?style=for-the-badge"></a>
</p>

selfL 是一套面向 coding agent 的可移植自学习 harness，用来把重复开发过程沉淀成可跨 Codex、Claude Code、Hermes 复用的行为：研究、判断、设计、实施、调试、交付、复盘。

## 设计目标

- 让 coding agent 更稳定地结合你的本地记忆、个人偏好、项目上下文和当前任务证据来完成后续工作。
- 让你的个人工程档案能在 Codex、Claude Code、Hermes 之间复用，而不是被锁在某一个 agent 的 memory 里。
- 把重复出现的开发经验、错误、偏好和验证方式沉淀成可复用的 skill 行为。
- 按工程阶段拆分技能，避免一个巨大的全局提示吞掉所有上下文。
- 让每个阶段都围绕证据、结果契约和验证方式运行。

## 可移植 Harness

selfL 不替代宿主 agent。Codex、Claude Code、Hermes 仍然是实际执行任务的运行时；selfL 提供一层本地、可移植的个人工程档案和 harness，让这些 agent 可以引用同一套偏好、规则和项目经验。

```text
selfL 是 source of truth
宿主 agent 是 execution runtime
adapter 只负责让宿主读取 selfL
```

默认本地档案结构：

```text
$HOME/.selfl/
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

- `profile.md` 保存跨 agent 的个人工程偏好：沟通方式、产品审美、执行习惯、验证习惯。
- `harness.md` 保存运行契约：上下文加载、工具偏好、权限边界、验证、交付和复盘规则。
- `adapters/*.md` 保存宿主 agent 的最小接入片段；默认不会自动写入宿主 memory。
- `projects/<repo-id>/` 保存项目级 harness，位于业务仓库之外。

## 宿主兼容

selfL v1 支持 Codex、Claude Code、Hermes，三者采用不同接入策略。

| 宿主 | 行为 | 默认写入策略 |
|---|---|---|
| Codex | 完整 adapter。明确调用 `@selfL` 或 `selfl-*` 后，可以创建 `~/.selfl`、创建项目档案，并为当前 Git 仓库初始化 CodeGraph。 | 可以写入 `~/.selfl`、当前仓库 `.codegraph/` 和 `.git/info/exclude`；默认不改 `AGENTS.md`。 |
| Claude Code | 引用 adapter。selfL 生成可引用 `~/.selfl/profile.md` 和 `~/.selfl/harness.md` 的片段。 | 默认不写 `~/.claude/CLAUDE.md`、项目 `CLAUDE.md`、`.claude/CLAUDE.md` 或 Claude auto memory。 |
| Hermes | 外部 profile adapter。selfL 生成把 `~/.selfl` 作为外部工程偏好来源的片段。 | 默认不写 `~/.hermes/SOUL.md`、`~/.hermes/memories/*`、`~/.hermes/skills/*`、config 或 `.env`。 |

这样可以避免主要集成冲突：

- 不自动写宿主 memory
- 不替换宿主 identity 或系统规则
- 不把 selfL profile 完整复制到每个宿主里
- 不绕过宿主权限、sandbox 或审批模型

## Agent 原生方向

本仓库围绕一个反馈闭环设计：

```text
work -> evidence -> lesson -> durable rule -> better next run
```

每个 skill 都刻意保持小而清晰：定义阶段契约、所需证据和失败边界。运行时，它们应该与你本地的 agent memory、项目 instructions、仓库文件、日志、测试、浏览器状态和当前任务上下文一起工作。真正的代码实施仍由当前 coding agent 完成；skills 负责约束什么时候研究、什么时候判断、什么时候验证、什么时候把经验更新为未来可复用行为。

完成一次有价值的任务后，可以使用 `selfl-distill`。它会帮助你把用户纠正、失败尝试、日志、diff 和验证结果提炼成后续 agent 可复用的规则。个人记忆和私有项目事实可以继续保留在本地，而可复用的行为模式再沉淀进 skills 或 shared rules。

## 个性化初始化

安装这些 skills 不会自动读取、复制或总结你已有的 Codex、Claude Code、Hermes 或其他 agent 对话记录和记忆。第一次明确呼叫 `@selfL` 或任意 `selfl-*` skill 时，会先做一次幂等的个性化 bootstrap 检查。如果本机还没有 selfL profile，selfL 会先运行 `selfl-distill` bootstrap，再继续执行用户请求的 skill。

默认私有档案保存在仓库之外：

```text
$HOME/.selfl/profile.md
$HOME/.selfl/harness.md
$HOME/.selfl/bootstrap.json
```

如果你已经有稳定的宿主经验文档，selfL 会把它当作来源，而不是覆盖目标。例如已有 Codex 经验文档时，可以用它初始化 selfL profile，而不是重新做一次大范围原始对话扫描。

也可以直接运行 bootstrap：

```text
使用 $selfl-distill 初始化我的本地 selfL profile。阅读并整理我当前可用的本地 agent memory、对话记录、日志和历史任务结果。请在 ~/.selfl 下创建一份私有、可移植的工程档案，总结我的执行偏好、产品审美、验证习惯、可复用规则和反模式，并生成 Codex、Claude Code、Hermes adapter 片段。读取大范围个人历史或修改宿主 instructions 文件前先确认。
```

bootstrap 应该处理：

- 发现当前可用的本地 memory / history 来源
- 在仓库之外创建私有经验档案和 harness
- 生成宿主 adapter 片段，但不默认覆盖宿主 memory
- 报告读取了哪些来源、跳过了哪些来源、档案保存在哪里

后续完成重要任务后，可以继续沉淀：

```text
使用 $selfl-distill 从这次已完成任务中提炼可复用经验，并更新我的本地 selfL profile 或项目 harness。
```

## 内置 CodeGraph MCP

对于较大的代码仓库，Codex plugin 已内置 [CodeGraph](https://github.com/colbymchenry/codegraph) MCP 注册，让 agent 可以使用本地代码知识图谱来理解架构、追踪调用链和分析影响面。

当本仓库以 Codex plugin 方式安装时，CodeGraph 会在需要 MCP server 时通过 `npx` 启动。用户不需要在安装 plugin 之前先全局安装 CodeGraph。

每个代码仓库仍然需要一份本地图谱索引。当你在 Git 仓库内明确呼叫 selfL 插件或任意 selfL skill 时，selfL 会先对当前仓库做一次幂等的 CodeGraph bootstrap 检查。如果索引不存在，会在开始大范围仓库工作前自动初始化。

也可以手动初始化：

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

当当前 Codex 客户端能看到 `codegraph_*` MCP tools 时，这些 skills 会优先用 CodeGraph 做仓库探索、排障和影响面分析。如果当前仓库还没有 CodeGraph 索引，明确使用 selfL 会被视为允许只初始化当前仓库，并通过 `.git/info/exclude` 让 `.codegraph/` 保持本地化。如果你只安装 skills、在 Git 仓库外运行 selfL，或 CodeGraph 不可用，则回退到普通文件搜索和定向读取。

## 工作流

推荐顺序：

```text
selfl-learn -> selfl-think -> selfl-design -> implementation -> selfl-debug -> selfl-ship -> selfl-distill
```

| 阶段 | Skill | 用途 |
|---|---|---|
| 学习 | `selfl-learn` | 研究陌生领域、消化材料、建立事实底座。 |
| 思考 | `selfl-think` | 做产品或架构判断、范围裁剪和执行计划。 |
| 设计 | `selfl-design` | 处理产品方向、交互原则、UI 结构和视觉验证。 |
| 实施 | Agent implementation | 由当前 coding agent 的工程能力直接实现。 |
| 调试 | `selfl-debug` | 复现问题、定位根因、最小修复、验证回归。 |
| 交付 | `selfl-ship` | 做预交付审查、验收、发布和 PR/issue 收尾。 |
| 沉淀 | `selfl-distill` | 从结果中提炼可复用规则并更新技能。 |

## Skills

| Skill | 用途 |
|---|---|
| `selfl-learn` | 在决策前研究陌生领域并结构化材料。 |
| `selfl-think` | 把粗略想法变成带取舍和风险的可执行计划。 |
| `selfl-design` | 定义产品、交互和 UI 执行规则。 |
| `selfl-debug` | 用可复现证据诊断故障并做最小修复。 |
| `selfl-ship` | 审查交付准备、验收、发布和交付收尾。 |
| `selfl-distill` | 将已完成工作转化为可复用规则，让后续 agent 执行持续变好。 |

## 安装方法

### 方案 A：作为 Codex Plugin 安装

如果你希望 skills 和 CodeGraph MCP 一起生效，优先使用 plugin 安装方式。Plugin 会通过 `npx` 注册本地 CodeGraph MCP server，因此用户不需要在安装本项目之前先全局安装 CodeGraph。

在 Codex Desktop 中，把这个仓库添加为插件市场：

```text
来源：sssstwee/open-self-learning-plugin
Git 引用：main
稀疏路径：留空
```

然后从该 marketplace 中安装 `selfL`。

安装 plugin 后，重启 Codex。每个需要代码图谱能力的仓库，只要明确呼叫一次 `@selfL` 或某个 `selfl-*` skill，selfL 就会检查本地索引并在需要时初始化。你也可以手动初始化：

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

当 `codegraph_*` MCP tools 可用时，Codex 会使用 CodeGraph。若当前项目还没有初始化，并且你明确调用了 selfL，skills 可以为当前仓库创建 `.codegraph/`，并通过 `.git/info/exclude` 避免把它提交进 Git。

### 方案 B：只安装 Skills

如果你只想安装 skills，不希望 plugin 注册 MCP tools，可以使用这个方式。

```bash
git clone https://github.com/sssstwee/open-self-learning-plugin.git
cd open-self-learning-plugin
```

#### 1. 确认 Codex skills 目录

默认安装目录通常是：

```bash
mkdir -p "$HOME/.codex/skills"
```

#### 2. 安装全部 skills

推荐使用 symlink，方便后续 `git pull` 更新后自动生效。

```bash
for skill in selfl-learn selfl-think selfl-design selfl-debug selfl-ship selfl-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/plugins/open-self-learning-plugin/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

#### 3. 只安装单个 skill

```bash
ln -s "$PWD/plugins/open-self-learning-plugin/skills/selfl-debug" "$HOME/.codex/skills/selfl-debug"
```

#### 4. 验证安装

重新打开 Codex 后，在输入框中尝试输入：

```text
/selfl
```

你应该能看到 `selfL Learn`、`selfL Think`、`selfL Design`、`selfL Debug`、`selfL Ship`、`selfL Distill`。

#### 5. 更新

```bash
cd /path/to/open-self-learning-plugin
git pull
```

如果使用 symlink 安装，通常不需要重新复制文件；重启 Codex 或刷新 skills 后即可读取更新。

#### 6. 卸载

```bash
for skill in selfl-learn selfl-think selfl-design selfl-debug selfl-ship selfl-distill; do
  rm -f "$HOME/.codex/skills/$skill"
done
```

## 目录结构

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
      host-compatibility.md
      personalization.md
      portable-profile.md
      routing.md
      self-learning-loop.md
```

## 致谢

感谢：

- [Waza](https://github.com/tw93/Waza) 提供阶段化技能设计思想启发。
- [Andrej Karpathy](https://github.com/karpathy) 关于实用 coding agent 行为的公开写作与经验启发。
- [CodeGraph](https://github.com/colbymchenry/codegraph) 提供本地代码知识图谱的思路与工具支持。
