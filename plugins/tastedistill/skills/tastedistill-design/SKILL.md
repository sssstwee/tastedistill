---
name: tasted-design
description: Define product direction, interaction principles, UI structure, visual execution rules, and screenshot-based polish before or during frontend implementation. Use when the task involves UI, product design, interaction behavior, visual quality, or design-system consistency. Not for backend-only logic.
---

# Design: Make The Interface Intentional

Use this skill for UI and product-facing work.

Prefix your first response line with ✦ inline, not as its own paragraph.

Before the workflow, apply `../../shared-rules/personalization.md` for explicit TasteD/TasteDistill invocations.

## Outcome Contract

- Outcome: a usable interface direction or concrete UI change with clear interaction behavior.
- Done when: layout, information hierarchy, states, responsiveness, and visual consistency have been considered and verified when possible.
- Evidence: screenshots, rendered UI, existing components, design tokens, accessibility constraints, and user goals.

## Workflow

1. Identify the user workflow and the primary decision on the screen.
2. Inspect existing UI patterns, tokens, components, and states before adding new ones.
3. Choose a visual direction in concrete terms, not generic adjectives.
4. Design the required states: empty, loading, error, disabled, selected, hover, focus, and success.
5. Implement with the existing design system where available.
6. Verify in a real browser or rendered output when the task changes visible UI.

## Product Principles

- Prefer clear hierarchy over decoration.
- Make high-frequency tools compact and scannable.
- Keep controls predictable and stateful.
- Disabled controls should explain their dependency when possible.
- Do not introduce a second visual system unless the project requires it.

## Do Not

- Ship UI based only on compilation.
- Add decorative surfaces that do not support the workflow.
- Hide unavailable actions when disabled-with-explanation is clearer.
- Ignore responsive text fitting and layout overlap.
