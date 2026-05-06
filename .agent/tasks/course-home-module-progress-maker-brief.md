# Course Home Module Progress Maker Brief

## Role

You are `product / execution layer`.

## Goal

Regenerate and verify the course home module cards so the homepage presents real module metadata consistently and exposes local learner progress state.

## Required Reads

1. `.agent/rules.md`
2. `.agent/STATE.md`
3. `.agent/handoff/CURSOR_HANDOFF.md`
4. `.agent/design/course-home-progress-contract.json`

## Source Of Truth

- Home UI template: `.agent/templates/course-app/src/views/CourseHome.vue`
- Module metadata: `CourseContent/Module_*/course.json`
- Generation path: `MVPMCP` through MVP/ADP
- Verification: `scripts/verify_course.py` and `npm --prefix CourseApp run build`

## Hard Boundaries

- Do not hand-edit `CourseApp/src/views/CourseHome.vue` as the final solution.
- Do not hand-edit generated data JSON as the final solution.
- Do not create `.cursor/` or `.workbuddy/`.
- Do not invent Module_02/03/04 titles or summaries. Use only `CourseContent/Module_*/course.json`.
- Do not write learner progress into `CourseContent/`, `course.json`, `slides.json`, `storyboard-contract.json`, `design-contract.json`, or `stitch-manifest.json`.

## Homepage Requirements

1. Each real module card must use the same structure:
   - module id
   - semantic title
   - summary
   - quiz entry
   - slide entries
   - exploration entry when the slide has one
   - local progress controls
2. Fallback titles such as `Module_02` or `Module_03` are invalid when real metadata exists.
3. Progress controls must show:
   - `看过`
   - `学过`
   - `已做题`
   - `掌握`
4. Progress is an ordered level. Later states imply earlier states.
5. Persistence must use `localStorage` key `shadergui-module-progress-v1`.
6. UI must remain usable on desktop and mobile with no text overlap.

## Execution Path

1. Confirm `.agent/templates/course-app/src/views/CourseHome.vue` contains the progress controls and localStorage logic.
2. Confirm `CourseContent/Module_*/course.json` contains semantic module metadata.
3. Stop any running dev server.
4. Run ADP to regenerate all module products:

```powershell
python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

5. Run verification:

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

6. Start dev server and inspect the homepage:

```powershell
npm --prefix CourseApp run dev
```

Open `http://localhost:5173/`.

## Failure Handling

- If template markers are missing, stop and report to workflow layer.
- If module metadata is missing or falls back to `Module_XX`, stop and report the exact module/source file.
- If ADP fails, report failed module, failed stage, failed command, and key error. Do not modify DAG/rules from execution role.

## Completion Report

End with `[ROLE_COMPLETION_REPORT]`:

- Current role.
- What was regenerated or inspected.
- Commands and results.
- Homepage result.
- DAG/rules/product impact.
- Cross-role next steps, or explicitly state no cross-role handoff is needed.
