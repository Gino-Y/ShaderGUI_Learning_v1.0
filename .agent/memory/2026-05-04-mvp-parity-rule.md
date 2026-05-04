# 2026-05-04 MVP Cross-Platform Parity Rule

## Feedback

User required a directly actionable solution instead of advisory text for keeping Cursor MVP execution aligned with Codex MVP execution.

## Decision

Cursor, Codex, and any other AI platform must use `.agent/flow_engine.py` as the only MVP execution entrypoint. Platform-specific context is forbidden as an asset source.

## Rule Update

Updated `.agent/rules.md` with `MVP Cross-Platform Execution Parity Rule`.

The rule defines:

- `.agent/` as the only trusted source.
- Cursor/Codex as execution-only actors for MVP.
- The exact MVP command.
- The fixed Cursor prompt allowed for MVP execution.
- Required verification after execution.
- Allowed differences limited to external-service randomness.
- Any drift must be fixed in `.agent/`, not in platform-private context.
