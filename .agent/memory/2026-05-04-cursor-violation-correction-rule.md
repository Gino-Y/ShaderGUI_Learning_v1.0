# 2026-05-04 Cursor Violation Correction Rule

## Feedback

User required that if Cursor violates the `.agent/` asset boundary again, the agent must execute cleanup, cut/move, or other correction procedures.

## Rule Update

Updated `.agent/rules.md` under `MVP Cross-Platform Execution Parity Rule`.

## New P0 Behavior

When Cursor or another AI platform writes AI assets into `.cursor/`, `.workbuddy/`, or other platform-specific directories:

- Identify violating assets.
- Move valuable content into `.agent/`.
- Delete duplicate platform-specific copies.
- Quarantine summaries for obsolete or conflicting files under `.agent/reports/cleanup/`.
- Update `.agent` rules, Skill, MCP, DAG, or verification scripts if the content changes contracts.
- Rescan platform-specific directories.
- Record the correction in `.agent/memory/`.
- Rerun MVP or the smallest relevant verification if the correction touches the MVP chain.

This is now a P0 action and does not require a second confirmation unless the user explicitly asks to preserve platform-specific files.
