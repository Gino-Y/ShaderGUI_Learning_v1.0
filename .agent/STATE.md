# Current Project State

## DAG State

Latest verified state: UTF8_TEXT_ASSETS_CLEANED.

## Active Module

Module_01

## Current Focus

All project text assets must be UTF-8. The previously garbled trusted documents have been replaced with clean UTF-8 text, and verification now blocks mojibake.

## Recent Changes

- Rewrote `.agent/rules.md` as clean UTF-8 Chinese.
- Rewrote `.agent/SKILL.md` as clean UTF-8 Chinese.
- Rewrote `docs/Skill_Chain_DAG.md` as clean UTF-8 Chinese.
- Rewrote `.agent/handoff/HANDOFF_PROTOCOL.md` as clean UTF-8.
- Fixed `SlideView.vue` fallback text in both runtime and template.
- Added UTF-8/mojibake checks to `scripts/verify_course.py` and `.agent/templates/scripts/verify_course.py`.
- Regenerated `Module_01` MP3 audio and subtitle JSON after verification found public audio artifacts missing.

## Known Issues

- Windows PowerShell may display UTF-8 Chinese incorrectly unless its output encoding is configured; the repository text files now validate as UTF-8.
- Windows `node_modules` cleanup can hit EPERM on native `.node` files; do not force-delete.

## Last Verified

- `python .agent\platform_violation_guard.py --basedir .` passed.
- `python scripts\verify_course.py` passed.
- `npm --prefix CourseApp run build` passed.

## Next Step

Refresh the local app if needed and continue visual QA on `p01`, `p01/explore`, and the quiz flow.
