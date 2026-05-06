# Cursor / Codex Handoff Protocol

## Purpose

Keep Cursor, Codex, and any other executor aligned on the same `.agent/` source of truth. This protocol is mandatory for implementation, refactor, verification, MVP execution, workflow updates, and recovery after context loss.

## 对齐约束（必读）

- [AGENT_SINGLE_SOURCE] `.agent` is the only authoritative rules and asset root.
- [MVP_EXECUTION_CONTRACT] MVP runs must follow `docs/MVP_Execution_Contract.md` and `.agent/mvp-execution-scope.json`.
- [NO_INTERNAL_GUIDANCE_UI] Learner-facing pages must not show `shotInstruction`, `focusInstruction`, `implementationHint`, `learnerTakeaway`, or `Now focusing`.
- [TOKEN_LEVEL_ANIMATION] Code-slide motion must target code tokens and fields, not whole cards or whole code blocks.
- [COURSE_HOME_ALIGNMENT_GRID] The course home and module entry must use the unified single-level menu.
- [SYNC_RULES_DAG_VERIFY] Rule, DAG, Skill, verification, and template changes must stay synchronized.
- [REVERIFY_BUILD_BROWSER] Run `verify_course.py`, `npm run build`, and browser checks when relevant.
- [COMPLETION_GATE_FILE_DRIVEN] Completion must be proven by repository files, not conversation memory.

## Required Read Order

Before modifying the project, read:

1. `.agent/STATE.md`
2. `.agent/handoff/CURSOR_HANDOFF.md`
3. `.agent/memory/YYYY-MM-DD*.md`
4. `docs/Skill_Chain_DAG.md`
5. `.agent/rules.md`
6. `.agent/SKILL.md`

## Mandatory Handoff Fields

Every handoff update must include:

- Current goal.
- Completed work.
- Modified files.
- Verification commands.
- Verification results.
- DAG impact: yes or no.
- Unfinished work or blockers.
- Next recommended step.

## Completion Gate

A task is not complete until:

- Required files are updated.
- DAG impact is assessed.
- Rules, Skill, DAG, templates, and verification scripts are synchronized when needed.
- `python scripts\verify_course.py` has run.
- `npm --prefix CourseApp run build` has run when frontend code or templates changed.
- `.agent/STATE.md`, `.agent/handoff/CURSOR_HANDOFF.md`, and `.agent/memory/` are updated.

## Platform Boundary

- `.agent/` is the only trusted AI asset root.
- `.cursor/` and `.workbuddy/` must not provide project rules, workflow, Skill, prompt, DAG, or MVP assets.
- If platform-private AI assets appear, execute the platform violation correction flow and record it in memory.

## UTF-8 Requirement

All handoff, memory, rules, DAG, Skill, scripts, templates, data contracts, and generated text artifacts must be UTF-8. Encoding violations block delivery.

## Small Fix Ownership

Small, deterministic consistency problems must be fixed by the current executor without asking the user to do manual cleanup. Examples include stale paths, missing handoff updates, obvious typos, validation drift, and UTF-8/mojibake cleanup.

## MVP / ADP Execution Role

- MVP executes one module through the normal complete module pipeline.
- ADP is a dispatcher command that runs MVP module-by-module from `.agent/adp-scope.json`.
- The current platform assigned to the execution layer may execute MVP/ADP commands, but must not be used as a source of rules, prompts, workflow, DAG, or generated assets.
- Do not create `.workbuddy/` or `.cursor/` project knowledge directories; record all cross-agent state in `.agent/handoff/` and `.agent/memory/`.

## Runtime Role Switching

Roles are runtime responsibilities, not platform identities. If the user says `你是 <role>`, the active executor immediately switches to that role.

- workflow/DAG/工作流层: workflow assets only (`.agent/`, docs, MCP orchestration, templates, verification, handoff, memory, rules).
- product/执行层/产物层: execute MVP/ADP and handle product-facing output through the DAG/template/MCP path.
- review/检查层: inspect and report unless repair is explicitly requested.

Do not store durable role instructions in `.cursor/` or `.workbuddy/`; write all persistent coordination under `.agent/`.

## Course Home Module Progress State

- Course home module cards include local learner status: `看过 -> 学过 -> 已做题 -> 掌握`.
- This is generated from `.agent/templates/course-app/src/views/CourseHome.vue`.
- The state is persisted in browser `localStorage` under `shadergui-module-progress-v1`.
- Do not write learner progress into course source JSON or DAG contracts.
- If the current generated `CourseApp` lacks this UI, rerun MVP/ADP from the execution layer instead of hand-editing the product file.

## ADP Storyboard Validation

- ADP storyboard coverage must compare `(moduleId, slideId)`.
- Do not treat bare slide ids such as `p02` as globally unique across modules.
- Storyboard `severity: warning` findings are non-blocking; only non-warning errors fail the node.
- If ADP fails at Module_03 Storyboard with only an extra-slide warning, the workflow implementation is stale.
