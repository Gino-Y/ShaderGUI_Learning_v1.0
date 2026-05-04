# 2026-05-04 Platform Violation Guard

## Feedback

User asked for a mechanism that reminds Cursor when it violates the `.agent/` boundary, without relying on the user to manually remind Cursor.

## Mechanism Added

- Added `.agent/platform_violation_guard.py`.
- Integrated the guard into `.agent/run_guard.py` through `assert_workspace()`.
- Updated `.agent/rules.md` with `Cursor 自动提醒 / 阻断机制`.

## Behavior

Every `.agent/flow_engine.py` run now performs a preflight scan of `.cursor/` and `.workbuddy/`.

If platform-private AI assets are detected:

- The run fails fast with `CURSOR_PLATFORM_VIOLATION`.
- A human-readable report is written to `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.md`.
- A machine-readable report is written to `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.json`.
- The correction command is available:

```powershell
python .agent/platform_violation_guard.py --basedir . --fix
```

The fix command quarantines violating files under `.agent/reports/cleanup/quarantine/`.
