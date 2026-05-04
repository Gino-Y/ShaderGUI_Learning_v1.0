# Platform Asset Boundary Violation

- Detected At: `2026-05-04T14:55:48`
- Action: `quarantined`
- Violation Count: `1`

## Files

- `.cursor/rules/dag-handoff-completion-gate.mdc`

## Required Correction

Cursor/Codex must not use platform-private AI assets as rule, workflow, DAG, Skill, prompt, or MVP sources.
Move valuable content into `.agent/`, delete duplicates, then rerun the MVP entrypoint.
