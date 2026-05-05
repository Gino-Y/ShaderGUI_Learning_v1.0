# Platform Asset Boundary Violation

- Detected At: `2026-05-05T16:59:42`
- Action: `blocked`
- Violation Count: `1`

## Files

- `.workbuddy/memory/2026-05-05.md`

## Required Correction

Cursor/Codex must not use platform-private AI assets as rule, workflow, DAG, Skill, prompt, or MVP sources.
Move valuable content into `.agent/`, delete duplicates, then rerun the MVP entrypoint.
