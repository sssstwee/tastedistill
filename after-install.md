# TasteD Hermes Usage

Use plugin-qualified skill names in Hermes:

```bash
hermes -s tasted:think -z "analyze this project"
hermes -s tasted:distill -z "summarize lessons from this work"
```

Available plugin skills:

- `tasted:learn`
- `tasted:think`
- `tasted:design`
- `tasted:debug`
- `tasted:ship`
- `tasted:distill`

Compatibility aliases such as `tasted:tasted-think` are also registered.

Avoid bare local names such as `hermes -s tasted-think` when a local skill exists under `~/.hermes/skills/`, because local skills can shadow plugin-provided skills.
