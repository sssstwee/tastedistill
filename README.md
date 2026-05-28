# TasteDistill

<p>
  <a href="./README.md"><strong>ENGLISH</strong></a>
  ·
  <a href="./README.zh-CN.md"><strong>中文</strong></a>
</p>

> Project About: TasteDistill lets Codex, Claude Code, and Hermes share local experience, preference memory, and engineering workflows.

![TasteDistill helps multiple coding agents share your working style](./assets/readme/hero-en.png)

TasteDistill is a small local notebook for your coding agents. It keeps your taste, habits, project lessons, and delivery rules in one place so Codex, Claude Code, and Hermes can work in a more consistent way.

| 🧠 What it stores | 🤖 Who can read it | 🔒 Where it lives |
|---|---|---|
| Your product taste, UI preferences, coding habits, and lessons | Codex, Claude Code, Hermes | On your machine, under `~/.tastedistill/` |

```mermaid
flowchart LR
    A["Your taste<br/>preferences<br/>lessons"] --> B["TasteDistill<br/>local profile"]
    B --> C["Codex"]
    B --> D["Claude Code"]
    B --> E["Hermes"]
```

## 🧩 Why Use It

| Without TasteDistill | With TasteDistill |
|---|---|
| 😵 You repeat the same preferences in every new chat. | ✅ Your preferences live in one local profile. |
| 🧩 One agent learns something, but another agent does not know it. | 🔁 Codex, Claude Code, and Hermes can read the same working style. |
| 🗂️ Useful lessons stay buried in old conversations. | ✨ Finished work can turn into reusable lessons. |
| 🧱 Big global prompts become messy. | 🛠️ Each task follows a small, clear workflow. |

## 🎯 What It Helps With

TasteDistill is useful when you want an agent to remember things like:

- "I prefer simple, polished UI instead of decorative dashboard clutter."
- "Before changing code, first understand the current project structure."
- "After fixing a bug, show the exact verification result."
- "Do not overwrite host memory or project instruction files unless I ask."
- "Keep private user taste and project lessons outside public repositories."

The profile stays on your own machine by default:

```text
~/.tastedistill/
  profile.md      # your personal taste and working preferences
  harness.md      # how agents should verify, deliver, and distill lessons
  adapters/       # Codex, Claude Code, Hermes loading notes
  projects/       # project-specific lessons outside the business repo
```

## 🔁 How It Works

![TasteDistill workflow: learn, think, design, debug, ship, distill](./assets/readme/workflow-en.png)

TasteDistill splits agent work into six easy stages:

| Stage | Use It When | What The Agent Should Do |
|---|---|---|
| Learn | The topic or repo is unfamiliar | Read sources, map facts, avoid guessing |
| Think | You need a plan or decision | Compare options, explain tradeoffs, choose a path |
| Design | UI, UX, product taste, or visual polish matters | Follow your taste, check real screens when needed |
| Debug | Something is broken | Reproduce, prove the root cause, fix the smallest thing |
| Ship | Work is almost done | Verify, check delivery details, prepare release or PR notes |
| Distill | A task taught something useful | Save the lesson for future runs |

## 🚀 First-Time Setup

After installing TasteDistill, use it normally in a project. The first explicit TasteD call also creates the local profile when needed.

```mermaid
flowchart LR
    A["Install TasteDistill"] --> B["Call TasteD in a project"]
    B --> C["Create<br/>~/.tastedistill"]
    C --> D["Generate setup notes"]
    D --> E["Use it in future tasks"]
```

Use the same everyday request you would normally ask an agent:

```text
Codex Desktop: @TasteD analyze this project
Codex CLI: tasted-think analyze this project
Claude Code: /tasted:think analyze this project
Hermes CLI: tasted:think analyze this project
```

TasteD can be called in different ways depending on the host. Codex Desktop supports an `@TasteD` mention, Codex CLI can call symlinked skills directly, Claude Code uses `/plugin` commands, and Hermes is managed from the command line.

| Host | Everyday call | Stage skill calls |
| --- | --- | --- |
| Codex Desktop | `@TasteD analyze this project` | `tasted-learn`, `tasted-think`, `tasted-design`, `tasted-debug`, `tasted-ship`, `tasted-distill` |
| Codex CLI | `tasted-think analyze this project` | `tasted-learn`, `tasted-think`, `tasted-design`, `tasted-debug`, `tasted-ship`, `tasted-distill` |
| Claude Code CLI or desktop | `/tasted:think analyze this project` | `/tasted:learn`, `/tasted:think`, `/tasted:design`, `/tasted:debug`, `/tasted:ship`, `/tasted:distill` |
| Hermes CLI | `tasted:think analyze this project` | `tasted:learn`, `tasted:think`, `tasted:design`, `tasted:debug`, `tasted:ship`, `tasted:distill` |

Just ask for the work you want done. On the first run, TasteD prepares your local profile automatically and then continues with that request.

TasteDistill will:

- look for existing local agent preferences and guidance
- when running in Codex, reuse your existing Codex preferences when available, or build a local TasteDistill summary from the safe records it can already see
- ask before reading broad personal history
- create `~/.tastedistill/profile.md`
- create `~/.tastedistill/harness.md`
- save a local summary of useful Codex context when needed
- generate setup notes for Codex, Claude Code, and Hermes
- report what it created and what it skipped

It will not silently rewrite your host agent memory.

You do not need to prepare any Codex preference file first. If Codex already has useful notes about how you like agents to work, TasteDistill will use them. If not, it will make its own local summary from the safe records it can already see. It will not quietly change Codex's own instructions or memories.

## 🧭 Choose An Install Path

```mermaid
flowchart TD
    A["Which host do you use?"] --> B["Codex Desktop"]
    A --> C["Codex CLI"]
    A --> D["Claude Code<br/>CLI or desktop"]
    A --> E["Hermes CLI"]
    B --> F["Install marketplace plugin"]
    C --> G["Symlink Codex skills"]
    D --> H["Use /plugin commands"]
    E --> I["Use hermes plugins install"]
```

## 🔄 Update To The Latest Version

If you installed from `main`, update TasteD from the same host where you use it:

| Host | Update command |
| --- | --- |
| Codex Desktop | Restart Codex Desktop so the installed marketplace plugin refreshes from `main`. |
| Codex CLI | Pull the Git repo you symlinked from, then restart Codex CLI or open a new session. |
| Claude Code CLI or desktop | Run `/plugin update tasted`, then restart Claude Code. |
| Hermes CLI | Run `hermes plugins update tasted`, then start a new Hermes session. |

Claude Code terminal equivalent:

```bash
claude plugin update tasted
```

Hermes terminal command:

```bash
hermes plugins update tasted
```

## <img src="./assets/icons/codex.png" width="24" height="24" alt="Codex"> Install In Codex Desktop

Use this if you want the easiest Codex experience with bundled skills and bundled CodeGraph MCP registration.

1. Open Codex Desktop.
2. Go to plugin marketplace management.
3. Add this repository as a marketplace:

```text
Source: sssstwee/tastedistill
Git ref: main
Sparse path: leave empty
```

4. Install `TasteD` (the plugin for the TasteDistill project).
5. Restart Codex.
6. In a project, call the plugin:

```text
@TasteD analyze this repo
```

You can also call an individual skill directly:

```text
tasted-learn
tasted-think
tasted-design
tasted-debug
tasted-ship
tasted-distill
```

## <img src="./assets/icons/claude-code.png" width="24" height="24" alt="Claude Code"> Install In Claude Code

Claude Code can be used from the terminal or from a desktop UI. Use the same plugin commands anywhere Claude Code exposes `/plugin`.

The Claude Code plugin also includes the bundled CodeGraph MCP config. Claude Code may ask you to trust or enable the MCP server before the `codegraph_*` tools appear.

Add the marketplace:

```text
/plugin marketplace add sssstwee/tastedistill
```

Install the plugin:

```text
/plugin install tasted@tastedistill
```

If your Claude Code version expects the plugin name directly, use:

```text
/plugin install tasted
```

Then call an individual TasteD skill:

```text
/tasted:learn
/tasted:think
/tasted:design
/tasted:debug
/tasted:ship
/tasted:distill
```

TasteDistill does not automatically edit `CLAUDE.md`. It can generate a small setup snippet, and you decide whether to add it.

## <img src="./assets/icons/hermes.png" width="24" height="24" alt="Hermes"> Install In Hermes CLI

Hermes is managed from the command line and installs plugins from a Git repository.

The Hermes plugin currently installs the TasteDistill workflow skills. It does not automatically register CodeGraph MCP. If your Hermes environment already exposes compatible `codegraph_*` tools, TasteDistill can still use them.

```bash
hermes plugins install sssstwee/tastedistill --enable
```

Restart Hermes after installing.

Call an individual TasteD skill under the plugin namespace:

```text
tasted:learn
tasted:think
tasted:design
tasted:debug
tasted:ship
tasted:distill
```

If you installed without `--enable`, enable it later:

```bash
hermes plugins enable tasted
```

TasteDistill does not automatically edit `SOUL.md`, Hermes memories, config files, or `.env`.

## 🧰 Install In Codex CLI Or Codex Skills Only

Use this for Codex CLI, or when you do not want the full Codex Desktop plugin and only want the skill files.

```bash
git clone https://github.com/sssstwee/tastedistill.git
cd tastedistill
mkdir -p "$HOME/.codex/skills"

for phase in learn think design debug ship distill; do
  rm -f "$HOME/.codex/skills/tasted-$phase"
  ln -s "$PWD/plugins/tastedistill/skills/tastedistill-$phase" "$HOME/.codex/skills/tasted-$phase"
done
```

Restart Codex and call the short skill names:

```text
tasted-learn
tasted-think
tasted-design
tasted-debug
tasted-ship
tasted-distill
```

## 🗺️ CodeGraph Support

TasteDistill can use [CodeGraph](https://github.com/colbymchenry/codegraph) to understand larger codebases faster.

In simple terms: CodeGraph is a local map of your repository. It helps the agent answer questions like:

- "Where is this feature implemented?"
- "What calls this function?"
- "What might break if we change this file?"

When you explicitly call TasteDistill inside a Git repository, it may initialize a local `.codegraph/` index for that repository and keep it out of Git.

| Host | Does the TasteDistill plugin include CodeGraph MCP registration? |
|---|---|
| Codex Desktop | ✅ Yes. The Codex plugin points to `plugins/tastedistill/.mcp.json`. |
| Codex CLI | ⚠️ Skills-only install does not register MCP automatically. Use CodeGraph only if the session already exposes compatible `codegraph_*` tools, or set MCP up manually. |
| Claude Code CLI or desktop | ✅ Yes. The Claude Code plugin also points to `plugins/tastedistill/.mcp.json`. |
| Hermes CLI | ⚠️ Not yet. The Hermes plugin installs skills; use CodeGraph only if the host/session already exposes compatible `codegraph_*` tools. |

So "CodeGraph support" means two different things:

- **Codex Desktop / Claude Code**: the plugin ships the MCP registration and can start CodeGraph through `npx` when the host enables it.
- **Codex CLI / Hermes CLI**: the plugin does not currently wire MCP automatically in these paths; TasteDistill falls back to normal repository search unless CodeGraph tools are already available.

Manual setup is also possible:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

## 🛡️ What TasteDistill Will Not Do By Default

TasteDistill is intentionally conservative.

It will not automatically:

- overwrite Codex `AGENTS.md`
- overwrite Claude `CLAUDE.md`
- overwrite Hermes `SOUL.md`
- copy raw private conversations into the repository
- read `.env` secrets
- publish or upload your personal profile

Your local profile is meant to stay local unless you choose otherwise.

## 🔄 Update

If you installed from Git:

```bash
cd /path/to/tastedistill
git pull
```

Then restart your host agent if it does not reload plugins automatically.

## 🙏 Acknowledgements

TasteDistill was inspired by useful ideas from:

- [Waza](https://github.com/tw93/Waza), especially the idea of small stage-based skills.
- [Andrej Karpathy](https://github.com/karpathy), for practical public notes about coding agents.
- [CodeGraph](https://github.com/colbymchenry/codegraph), for local code knowledge graph tooling.
