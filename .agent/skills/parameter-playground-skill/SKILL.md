---
name: parameter-playground-skill
description: Designs TensorFlow Playground-style parameter sandboxes. Use when learners need to adjust many linked parameters, compare presets, run a simulation or training loop, and inspect result changes.
---

# Parameter Playground Skill

## Purpose

Use this skill for multi-parameter systems where learning happens through controlled trial and comparison. The playground must make parameter causality visible without overwhelming the learner.

## Best Fit

- Many linked variables.
- Training, simulation, or repeated run loop.
- Presets and state comparison matter.
- The learner needs to share or reproduce a state.

## Workflow

1. Define the system model.
2. Separate editable parameters, derived metrics, and visual outputs.
3. Create safe presets before exposing free-form controls.
4. Define run, pause, reset, compare, and serialize behavior.
5. Design linked result views such as output, loss, warnings, and trace.
6. Validate performance and state reproducibility.

## Output Contract

```text
.agent/interactive-content/<module-id>/<playground-id>/
├── interaction-brief.md
├── concept-model.json
├── presets.json
├── storyboard.json
├── component-spec.md
└── validation-report.md
```

## Quality Bar

- Defaults must teach before any parameter changes.
- Every parameter needs a visible effect or an explanation why it is inactive.
- Presets are required.
- State must be resettable and, when useful, serializable.
