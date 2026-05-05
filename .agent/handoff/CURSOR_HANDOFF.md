# Cursor Handoff

## Current Goal

ADPMCP 平行 DAG 节点已创建完成，支持完整生产模式（非 MVP 裁剪）。

## Completed Work

- **2026-05-05 (ADP scope fix)**:
  - **根因**：`adp_mcp.py` 复用了 `MVPMCP` 的清理函数 `_clean_mvp_products()`，读取的是 `mvp-execution-scope.json`，语义不对
  - **修复**：
    - 新建 `.agent/adp-execution-scope.json`（ADP 独立清理范围）
    - 新建 `docs/ADP_Execution_Contract.md`（ADP 执行契约）
    - 修改 `.agent/mcp_servers/adp_mcp.py`：
      - `_clean_mvp_products` → `_clean_adp_products`
      - 读取 `adp-execution-scope.json`（不再复用 MVP 的）
      - 检查 `docs/ADP_Execution_Contract.md`（不再检查 MVP 的）
  - **验证**：`verify_course.py` ✅ 通过，语法检查 ✅ 通过
  - **提交**：`3308675`（快照）+ `c945fdc`（feat: ADP scope fix）
  - **状态**：ADPMCP 现在有自己的清理配置，不再依赖 MVP 的 scope 文件

- **2026-05-05 (ADP DAG node)**:
  - 创建新文件 `.agent/mcp_servers/adp_mcp.py`（平行节点，不修改 `mvp_mcp.py`）
  - 更新 `flow_engine.py` 支持 `--adp` 标志，在 pipeline 中根据 mode 选择调用 `ADPMCP` 或 `MVPMCP`
  - 创建 `.agent/adp-scope.json`（包含所有模块的完整 slideIds，非 MVP 裁剪）
  - 更新 4 个模块的 `slides.json`，补充缺失的 slides（Module_01 p02, Module_02 p02, Module_04 p02/p03）
  - 新增逐字稿文件（Module_01-p02, Module_02-p02, Module_04-p02/p03）
  - 验证：`verify_course.py` ✅ 通过，`npm run build` ✅ 通过
  - 提交：`bb36efa`（快照）+ `d0e322c`（feat: ADP）
  - 状态：ADPMCP 节点已就绪

- **2026-05-05 (Sidebar 移动端悬浮按钮重构)**:
  - **目标**：将移动端导航从底部标签栏（`BottomTabBar`）改为悬浮按钮 + 侧边栏
  - **修改文件**：
    - `CourseApp/src/components/Sidebar.jsx`（新增移动端悬浮按钮 + 侧边栏逻辑）
    - `CourseApp/src/App.jsx`（移除 `BottomTabBar` 组件）
  - **实现细节**：
    - 桌面端（≥1024px）：维持原侧边栏行为
    - 移动端（<1024px）：
      - 悬浮按钮（固定定位，左上角，z-50）
      - 点击按钮 → 显示侧边栏（绝对定位，覆盖全高）
      - 点击遮罩层 → 关闭侧边栏
      - 点击导航项 → 跳转 + 关闭侧边栏
  - **验证**：`npm run build` ✅ 通过
  - **提交**：`000bd14`（快照）+ `bc883ef`（feat: Sidebar 移动端悬浮按钮）+ `8bd0a6a`（fix: 移除 BottomTabBar）
  - **状态**：移动端导航已重构为悬浮按钮 + 侧边栏

- **2026-05-05 (earlier work - already in previous handoff)**:
  - Fixed `storyboard_mcp.py` scale field and color data
  - Fixed performance animation field name inconsistencies
  - Fixed MVP template not overwriting issue
  - Hardened `v0_mcp.py` with timeout and local fallback

## Modified Files

- `.agent/mcp_servers/adp_mcp.py` (新增 + 修改：独立化清理配置)
- `.agent/flow_engine.py` (修改：支持 --adp 标志)
- `.agent/adp-scope.json` (新增)
- `.agent/adp-execution-scope.json` (新增：ADP 独立清理范围)
- `docs/ADP_Execution_Contract.md` (新增：ADP 执行契约)
- `CourseContent/Module_01/slides.json` (修改：补充 p02)
- `CourseContent/Module_02/slides.json` (修改：补充 p02)
- `CourseContent/Module_03/slides.json` (修改：维持 p00/p01)
- `CourseContent/Module_04/slides.json` (修改：补充 p02/p03)
- `CourseContent/Module_01/doc/Module_01-p02-属性查找的工程策略.md` (新增)
- `CourseContent/Module_02/doc/Module_02-p02-封装工具类.md` (新增)
- `CourseContent/Module_04/doc/Module_04-p02-实战验收.md` (新增)
- `CourseContent/Module_04/doc/Module_04-p03-元认知总结.md` (新增)
- `.agent/STATE.md` (更新)
- `.agent/handoff/CURSOR_HANDOFF.md` (更新)

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
