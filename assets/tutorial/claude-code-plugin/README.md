# Claude Code Plugin Tutorial Assets

This folder stores screenshots and notes for the Claude Code TasteD plugin installation tutorial.

## Marketplace Address

Use this in Claude Code:

```text
/plugin marketplace add sssstwee/tastedistill
```

Equivalent GitHub repository URL:

```text
https://github.com/sssstwee/tastedistill.git
```

Install the plugin after adding the marketplace:

```text
/plugin install tasted@tastedistill
```

After install or update, restart Claude Code and verify:

```bash
claude plugin details tasted@tastedistill | sed -n '1,40p'
```

Expected Claude Code commands:

```text
/tasted:learn
/tasted:think
/tasted:design
/tasted:debug
/tasted:ship
/tasted:distill
```

## Screenshot Inventory

Save tutorial screenshots under `screenshots/` with these names:

| File | Use |
| --- | --- |
| `01-plugin-marketplaces-tab.png` | Claude Code `/plugin` UI on the Marketplaces tab, showing existing marketplaces and the add marketplace entry. |
| `02-add-marketplace-source.png` | Add Marketplace dialog with `sssstwee/tastedistill` entered as the marketplace source. |
| `03-discover-tasted-v007.png` | Discover tab after adding the marketplace, showing TasteD `v0.0.7` as available. |
| `04-plugin-details-install-scope.png` | TasteD plugin details page, showing install scope choices before installation. |
| `05-installed-reload-plugins.png` | Successful install message: `Installed tasted. Run /reload-plugins to apply.` |
| `06-tasted-old-duplicate-autocomplete.png` | Historical regression example: `/tasted:tasted-think` duplicated command after tab completion. |
| `07-tasted-expected-autocomplete.png` | Expected final autocomplete after typing `/tasted`: relative commands such as `/think`, `/ship`, and `/distill`, with `(tasted)` shown as the plugin source. |
| `08-tasted-profile-harness-verification.png` | Verification output showing `~/.tastedistill/profile.md`, `harness.md`, and `bootstrap.json` were read. |

The screenshot attached in the conversation for the Marketplaces tab should be saved as:

```text
assets/tutorial/claude-code-plugin/screenshots/01-plugin-marketplaces-tab.png
```

The three installation screenshots attached in the conversation should be saved as:

```text
assets/tutorial/claude-code-plugin/screenshots/02-add-marketplace-source.png
assets/tutorial/claude-code-plugin/screenshots/03-discover-tasted-v007.png
assets/tutorial/claude-code-plugin/screenshots/04-plugin-details-install-scope.png
assets/tutorial/claude-code-plugin/screenshots/05-installed-reload-plugins.png
```

After the successful install screen, run this in Claude Code:

```text
/reload-plugins
```

Then type `/tasted` to verify command completion.

Claude Code displays plugin commands in two equivalent forms:

- In completion after typing `/tasted`, it may show relative commands such as `/think`, `/ship`, and `/distill`, with `(tasted)` in the source column.
- When inserted or executed, the command may be namespaced as `/tasted:think`.

Both forms are valid. The regression to avoid is duplicated names such as `/tasted:tasted-think`.

## Verified State

After installing `v0.0.7`, Claude Code should report exactly six skills:

```text
tasted 0.0.7
Skills (6)  debug, design, distill, learn, ship, think
```
