# Platform Asset Boundary Violation

- Detected At: `2026-05-04T15:45:24`
- Action: `blocked`
- Violation Count: `1`

## Files

- `.workbuddy/memory/2026-05-04.md`

## Required Correction

Cursor/Codex must not use platform-private AI assets as rule, workflow, DAG, Skill, prompt, or MVP sources.
Move valuable content into `.agent/`, delete duplicates, then rerun the MVP entrypoint.
