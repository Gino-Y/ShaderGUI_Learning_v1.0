# 2026-05-04 UTF-8 Cleanup

## Feedback

User asked to execute the UTF-8 correction after confirming there were still garbled texts in the project.

## Actions

- Rewrote `.agent/rules.md` as clean UTF-8 Chinese.
- Rewrote `.agent/SKILL.md` as clean UTF-8 Chinese.
- Rewrote `docs/Skill_Chain_DAG.md` as clean UTF-8 Chinese.
- Rewrote `.agent/handoff/HANDOFF_PROTOCOL.md` as clean UTF-8.
- Fixed `SlideView.vue` fallback text in runtime and template.
- Added UTF-8 and mojibake validation to `scripts/verify_course.py`.
- Synchronized `.agent/templates/scripts/verify_course.py`.
- Regenerated missing `Module_01` audio and subtitle artifacts.

## DAG Impact

Yes. UTF-8 validation is now part of the verification gate.

## Verification

- `python .agent\platform_violation_guard.py --basedir .` passed.
- `python scripts\verify_course.py` passed.
- `npm --prefix CourseApp run build` passed.
