# TasteDistill

<p>
  <a href="./README.md"><img alt="English" src="https://img.shields.io/badge/English-current-111827?style=for-the-badge"></a>
  <a href="./README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-switch-2563eb?style=for-the-badge"></a>
</p>

![TasteDistill helps multiple coding agents share your working style](./assets/readme/hero-en.png)

TasteDistill is a small local notebook for your coding agents.

You may use Codex today, Claude Code tomorrow, and Hermes next week. Each agent can be helpful, but they usually do not share what they learned about you: your product taste, UI preferences, delivery habits, common project rules, and the lessons from past mistakes.

TasteDistill gives those agents one shared place to read that long-term working style.

It does not replace Codex, Claude Code, or Hermes. It simply helps them work more like you.

## Why Use It

Without TasteDistill:

- You repeat the same preferences in every new chat.
- One agent learns something, but another agent does not know it.
- Useful lessons stay buried in old conversations.
- Big global prompts become messy and hard to maintain.

With TasteDistill:

- Your preferences live in one local profile.
- Codex, Claude Code, and Hermes can all read the same working style.
- Finished work can turn into reusable lessons.
- Each task follows a simple workflow: learn, think, design, debug, ship, distill.

## What It Helps With

TasteDistill is useful when you want an agent to remember things like:

- "I prefer simple, polished UI instead of decorative dashboard clutter."
- "Before changing code, first understand the current project structure."
- "After fixing a bug, show the exact verification result."
- "Do not overwrite host memory or project instruction files unless I ask."
- "Keep private user taste and project lessons outside public repositories."

The profile is stored on your own machine by default:

```text
~/.tastedistill/
  profile.md      # your personal taste and working preferences
  harness.md      # how agents should verify, deliver, and distill lessons
  adapters/       # Codex, Claude Code, Hermes loading notes
  projects/       # project-specific lessons outside the business repo
```

## How It Works

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

## First-Time Setup

After installing TasteDistill, run it once to create your local profile.

In Codex, you can say:

```text
@TasteDistill initialize my local profile
```

Or use the distill skill:

```text
Use tastedistill-distill to initialize my local TasteDistill profile.
```

On the first run, TasteDistill should:

- look for existing local agent memory or instruction files
- ask before reading broad personal history
- create `~/.tastedistill/profile.md`
- create `~/.tastedistill/harness.md`
- generate adapter notes for Codex, Claude Code, and Hermes
- report what it created and what it skipped

It should not silently rewrite your host agent memory.

## Install In Codex Desktop

Use this if you want the easiest Codex experience with bundled skills and CodeGraph support.

1. Open Codex Desktop.
2. Go to plugin marketplace management.
3. Add this repository as a marketplace:

```text
Source: sssstwee/tastedistill
Git ref: main
Sparse path: leave empty
```

4. Install `TasteDistill`.
5. Restart Codex.
6. In a project, call:

```text
@TasteDistill analyze this repo
```

You can also call the individual skills:

```text
tastedistill-learn
tastedistill-think
tastedistill-design
tastedistill-debug
tastedistill-ship
tastedistill-distill
```

## Install In Claude Code

Claude Code uses plugin marketplace commands.

Add the marketplace:

```text
/plugin marketplace add sssstwee/tastedistill
```

Install the plugin:

```text
/plugin install tastedistill@tastedistill
```

If your Claude Code version expects the plugin name directly, use:

```text
/plugin install tastedistill
```

Then use:

```text
/tastedistill:learn
/tastedistill:think
/tastedistill:design
/tastedistill:debug
/tastedistill:ship
/tastedistill:distill
```

TasteDistill does not automatically edit `CLAUDE.md`. It can generate a small adapter snippet, and you decide whether to add it.

## Install In Hermes

Hermes installs plugins from a Git repository.

```bash
hermes plugins install sssstwee/tastedistill --enable
```

Restart Hermes after installing.

The skills are available under the TasteDistill namespace:

```text
tastedistill:learn
tastedistill:think
tastedistill:design
tastedistill:debug
tastedistill:ship
tastedistill:distill
```

If you installed without `--enable`, enable it later:

```bash
hermes plugins enable tastedistill
```

TasteDistill does not automatically edit `SOUL.md`, Hermes memories, config files, or `.env`.

## Install Codex Skills Only

Use this only if you do not want the full Codex plugin and only want the skill files.

```bash
git clone https://github.com/sssstwee/tastedistill.git
cd tastedistill
mkdir -p "$HOME/.codex/skills"

for skill in tastedistill-learn tastedistill-think tastedistill-design tastedistill-debug tastedistill-ship tastedistill-distill; do
  rm -f "$HOME/.codex/skills/$skill"
  ln -s "$PWD/plugins/tastedistill/skills/$skill" "$HOME/.codex/skills/$skill"
done
```

Restart Codex and type:

```text
/tastedistill
```

## CodeGraph Support

TasteDistill can use [CodeGraph](https://github.com/colbymchenry/codegraph) to understand larger codebases faster.

In simple terms: CodeGraph is a local map of your repository. It helps the agent answer questions like:

- "Where is this feature implemented?"
- "What calls this function?"
- "What might break if we change this file?"

When you explicitly call TasteDistill inside a Git repository, it may initialize a local `.codegraph/` index for that repository and keep it out of Git.

Manual setup is also possible:

```bash
cd your-project
npx -y @colbymchenry/codegraph init -i
```

## What TasteDistill Will Not Do By Default

TasteDistill is intentionally conservative.

It will not automatically:

- overwrite Codex `AGENTS.md`
- overwrite Claude `CLAUDE.md`
- overwrite Hermes `SOUL.md`
- copy raw private conversations into the repository
- read `.env` secrets
- publish or upload your personal profile

Your local profile is meant to stay local unless you choose otherwise.

## Update

If you installed from Git:

```bash
cd /path/to/tastedistill
git pull
```

Then restart your host agent if it does not reload plugins automatically.

## Acknowledgements

TasteDistill was inspired by useful ideas from:

- [Waza](https://github.com/tw93/Waza), especially the idea of small stage-based skills.
- [Andrej Karpathy](https://github.com/karpathy), for practical public notes about coding agents.
- [CodeGraph](https://github.com/colbymchenry/codegraph), for local code knowledge graph tooling.
