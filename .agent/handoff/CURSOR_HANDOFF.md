# Cursor Handoff

## Current Goal

ADPMCP 平行 DAG 节点已创建完成，支持完整生产模式（非 MVP 裁剪）。

## Completed Work

- **2026-05-05 (ADP DAG node)**:
  - 创建新文件 `.agent/mcp_servers/adp_mcp.py`（平行节点，不修改 `mvp_mcp.py`）
  - 更新 `flow_engine.py` 支持 `--adp` 标志，在 pipeline 中根据 mode 选择调用 `ADPMCP` 或 `MVPMCP`
  - 创建 `.agent/adp-scope.json`（包含所有模块的完整 slideIds，非 MVP 裁剪）
  - 更新 4 个模块的 `slides.json`，补充缺失的 slides（Module_01 p02, Module_02 p02, Module_04 p02/p03）
  - 新增逐字稿文件（Module_01-p02, Module_02-p02, Module_04-p02/p03）
  - 验证：`verify_course.py` ✅ 通过，`npm run build` ✅ 通过
  - 提交：`bb36efa`（快照）+ `d0e322c`（feat: ADP）
  - 状态：ADPMCP 节点已就绪

- **2026-05-05 (earlier work - already in previous handoff)**:
  - Fixed `storyboard_mcp.py` scale field and color data
  - Fixed performance animation field name inconsistencies
  - Fixed MVP template not overwriting issue
  - Hardened `v0_mcp.py` with timeout and local fallback

## Modified Files

- `.agent/mcp_servers/adp_mcp.py` (新增)
- `.agent/flow_engine.py` (修改：支持 --adp 标志)
- `.agent/adp-scope.json` (新增)
- `CourseContent/Module_01/slides.json` (修改：补充 p02)
- `CourseContent/Module_02/slides.json` (修改：补充 p02)
- `CourseContent/Module_03/slides.json` (修改：维持 p00/p01)
- `CourseContent/Module_04/slides.json` (修改：补充 p02/p03)
- `CourseContent/Module_01/doc/Module_01-p02-属性查找的工程策略.md` (新增)
- `CourseContent/Module_02/doc/Module_02-p02-封装工具类.md` (新增)
- `CourseContent/Module_04/doc/Module_04-p02-实战验收.md` (新增)
- `CourseContent/Module_04/doc/Module_04-p03-元认知总结.md` (新增)
- `.agent/STATE.md` (更新)

## DAG Impact

Yes. Added `ADPMCP` as a parallel DAG node to `MVPMCP`:
- `MVPMCP`: MVP mode, reads from `mvp-scope.json`, generates only p00/p01
- `ADPMCP`: ADP mode (--adp flag), reads from `adp-scope.json`, generates ALL slides
- No change to existing DAG node order or product contracts
- Flow engine now supports `--adp` flag to switch between MVP and ADP modes

## Unfinished / Blockers

- No current blocker for ADP node creation.
- Need to test ADP mode: `python .agent\flow_engine.py --mode production --adp --scope module --module Module_01`

## Verification

- `python scripts\verify_course.py` passed ✅
- `npm --prefix CourseApp run build` passed ✅
- `python .agent\platform_violation_guard.py --basedir .` passed ✅
- Syntax check for `flow_engine.py` passed ✅

## Next Step

Test ADPMCP full production flow:
```powershell
python .agent\flow_engine.py --mode production --adp --scope module --module Module_01 --basedir . --max-retries 5
```

Verify ADPMCP correctly generates ALL slides (not just p00/p01).
