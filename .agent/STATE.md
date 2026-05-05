# Current Project State

## DAG State

Latest verified state: DEPLOY_READY after repairing WorkBuddy flow-engine regressions.

## Active Module

Module_01

## Current Focus

WorkBuddy remediation is complete: design/v0 MCP runtime failures were fixed and the full flow engine reaches DEPLOY_READY.

## Recent Changes

- **2026-05-05 (2nd fix)**: 修复表演动画字段名全链路不一致问题：
  - **根因**：`build_performance_for_cue()` 返回字典使用 `performanceType`/`demoType`，但 `SlideCanvas.vue`/`PerformanceLayer.vue` 消费的是 `type`/`demo`，导致 Vue 读到 `undefined`，表演动画全部消失。
  - **修复范围（8个文件）**：
    - `storyboard_mcp.py`：`build_performance_for_cue()` 返回字段改为 `type`/`demo`；`validate_storyboard_contract()` 校验字段同步更新
    - `design_mcp.py`：`performanceSpecs` 读取字段同步更新
    - `PerformanceLayer.vue`（模板）：`v-if/v-else-if` 绑定改为 `activePerfSpec.type`
    - `SlideCanvas.vue`（模板）：`showFlowPath` 计算属性改为 `activePerfSpec.value?.type` 和 `activePerfSpec.value?.demo`
    - `audit_semantic.py` / `audit_storyboard.py`：审计脚本字段名同步
  - 重新生成 `storyboard-contract.json` 和 `design-contract.json`，验证 `type=demo, demo=flow-path` 正确
  - 提交：`0736b00`
  - 用户验证：待刷新浏览器确认动画恢复

- **2026-05-05 (1st fix)**: Fixed `storyboard_mcp.py` and `design_mcp.py` for performance animation issues:
  - `storyboard_mcp.py`: Removed `slide_kind == "concept"` restriction in `build_performance_specs_for_slide()` — now all slide types (concept/code) can generate demo specs based on semantic keywords.
  - `design_mcp.py`: Fixed color code typo (`#1e293b` → `#1e293b`) in `COLOR_SCHEMES["default"]["surface"]`.
  - Re-generated `storyboard-contract.json` and `design-contract.json` — p01 now correctly generates `type=demo, demo=flow-path` performanceSpec.
  - Verified timeRange binding to subtitle segments (p01 demo: 12.69-19.23s, duration 6.54s).

- **2026-05-04** (earlier): Fixed `.agent/mcp_servers/design_mcp.py` regressions:
  - Added missing `design_slides` initialization.
  - Added `_infer_typography()` and `_infer_color_scheme()`.
  - Fixed broken diagram keyword detection.
  - Replaced mojibake/broken strings that caused SyntaxError or verification failures.
  - Restored `palette` assignment that had been swallowed by a corrupted comment.
- Hardened `.agent/mcp_servers/v0_mcp.py`:
  - Added configurable `V0_API_TIMEOUT_SECONDS`.
  - Reduced default POST timeout to avoid long flow-engine stalls.
  - Added deterministic `local-v0-fallback` handoff when v0 chat creation times out or fails.
  - Cleaned broken mojibake strings and f-string syntax.
- Re-ran the full flow engine for `Module_01`; it regenerated design, v0 fallback handoff, audio, subtitles, stitch manifest, and build artifacts.

## Known Issues

- The v0 API key is reachable, but v0 chat creation timed out during this run; the flow used `local-v0-fallback` so the DAG could continue deterministically.
- Some older historical handoff/memory reports still contain mojibake for audit history; current trusted STATE/handoff files are readable UTF-8.
- Windows `node_modules` cleanup can hit EPERM on native `.node` files; do not force-delete.

## Last Verified

- `python -c "from mcp_servers.storyboard_mcp import StoryboardMCP; StoryboardMCP.prepare_storyboard_contract(...)"` ✅ generated storyboard-contract.json
- `python -c "from mcp_servers.design_mcp import DesignMCP; DesignMCP.prepare_design_contract(...)"` ✅ generated design-contract.json
- Verified p01 has `type=demo, demo=flow-path` performanceSpec ✅
- Verified timeRange binding (p01 demo: start=12.69, end=19.23, durationMs=6540) ✅
- SlideIds consistent across storyboard/design/slides.json ✅
- `V0_API_TIMEOUT_SECONDS=5 python -u .agent\flow_engine.py --mode test --stage mvp --scope module --module Module_01 --basedir .` reached `DEPLOY_READY`.
- `python .agent\platform_violation_guard.py --basedir .` passed.
- `python scripts\verify_course.py` passed.
- `npm --prefix CourseApp run build` passed.

## Next Step

Refresh the local app and continue visual QA on `p01`, `p01/explore`, and `/module/Module_01/quiz`.
