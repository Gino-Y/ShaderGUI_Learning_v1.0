---
name: explorable-mini-skill
description: Creates small explorable explanation labs for a single lesson or slide. Use when a concept can be taught through a few user-controlled variables with immediate visual, numeric, code, or explanation feedback.
---

# Explorable Mini Skill

## Purpose

Use this skill to create a focused interactive lab for one concept. The lab should make cause and effect visible through direct manipulation and immediate feedback.

## Best Fit

Use this skill when:

- The concept has 1 to 5 important variables.
- The learner can change a value and immediately see the consequence.
- A small simulation is enough; no long training loop or export flow is needed.
- The lab can be understood in 5 to 10 minutes.

ShaderGUI examples:

- Toggle a property group and see which material properties become visible.
- Drag outline width and see how UI grouping changes perceived control.
- Switch render mode and see which hidden render states must sync.
- Rename a shader property and see safe lookup vs hard lookup behavior.

## Required Model

Each lab must define:

```json
{
  "labId": "Module_01-p01-explore-property-grouping",
  "parentSlideId": "p01",
  "learningQuestion": "Why does grouping reduce material tuning burden?",
  "state": {
    "useOutline": true,
    "outlineWidth": 0.05,
    "useDissolve": false
  },
  "derived": {
    "visibleGroups": ["Shape", "Color"],
    "warnings": []
  },
  "interactions": [
    {
      "control": "toggle",
      "target": "useDissolve",
      "feedback": ["visibleGroups", "explanation", "codeHighlight"]
    }
  ]
}
```

## Workflow

0. Pass the interaction necessity gate.
   - Write `necessity-gate.json`.
   - Continue only when `decision` is `insert`.
   - Skip the explorable page when a normal explanation page plus quiz can teach the concept.

1. State the learning question.
   - One lab, one question.

2. Define manipulable state.
   - Keep controls few.
   - Use meaningful defaults.

3. Define derived feedback.
   - Visual diagram.
   - Numeric or status output.
   - Explanation text.
   - Optional code highlight.

4. Write the storyboard.
   - Initial state.
   - User actions.
   - Expected feedback.
   - Reset behavior.

5. Specify the Vue component.
   - Component name.
   - Props.
   - Internal state.
   - Events.
   - Tailwind layout notes.

6. Validate the lab.
   - The default state teaches something.
   - Each control has visible feedback.
   - Invalid states are either prevented or explained.
   - The lab works without relying on hover only.

## Output Contract

For each lab:

```text
.agent/interactive-content/<module-id>/<slide-id>/explore/
├── interaction-brief.md
├── necessity-gate.json
├── concept-model.json
├── storyboard.json
├── component-spec.md
└── validation-report.md
```

If implemented:

```text
CourseApp/src/components/labs/<ComponentName>.vue
```

## Quality Bar

- Prefer direct manipulation over form-heavy configuration.
- Show cause and effect in the same viewport when possible.
- Provide reset and at least one curated preset.
- Keep the lab bounded; do not turn every mini lab into a full playground.
- If code is shown, highlight the part affected by the current state.
- Never create a mini lab only to add variety; the necessity gate must show a concrete learning gain.
