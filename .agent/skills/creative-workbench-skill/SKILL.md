---
name: creative-workbench-skill
description: Designs Teachable Machine-style task workbenches. Use when learners create, train, test, export, or otherwise produce a concrete artifact through a guided workflow.
---

# Creative Workbench Skill

## Purpose

Use this skill when the learning goal is a completed artifact or tool, not only conceptual understanding. The experience should guide learners through a task loop with clear state and recovery.

## Best Fit

- User gathers examples, configures inputs, trains, tests, or exports.
- Device capabilities, files, privacy, or permissions matter.
- The workflow has stages and validation gates.
- The result is a model, asset, tool, or reusable configuration.

## Workflow

1. Define the artifact and success criteria.
2. Break the task into stages: collect, configure, run, test, export.
3. Define state, validation, error recovery, and reset behavior.
4. Identify sensitive operations and required user confirmations.
5. Design progress feedback and result inspection.
6. Validate the workflow with missing/invalid input states.

## Output Contract

```text
.agent/interactive-content/<module-id>/<workbench-id>/
├── interaction-brief.md
├── workflow-contract.json
├── storyboard.json
├── component-spec.md
└── validation-report.md
```

## Quality Bar

- Each stage must have a clear completion condition.
- Do not request sensitive permissions unless they are essential.
- Errors must be recoverable.
- Export or output behavior must be explicit.
