# Cursor Handoff

## Current Goal

ADP 全量写入架构已落地，全部 4 模块 DEPLOY_READY。MVP 模式与 ADP 模式已完全分离。

## Completed Work

- **2026-05-06 (ADP 全量写入架构重构)**:
  - **根因**：ADP 逐模块运行时，`_write_course_app` 跨运行合并依赖上一次的 `course.json`，但 `flow_engine.py` 的 `clear_stage_outputs("mvp", ...)` 删除整个 CourseApp/ 导致合并源消失
  - **修复（3 处）**：
    1. `.agent/mcp_servers/adp_mcp.py`：
       - `_write_course_app` 改为全量扫描写入（扫描所有 `CourseContent/Module_*/` 目录，一次性写全量产物）
       - 新增 `_copy_all_course_content()` 在写入前复制所有模块逐字稿
       - 新增 `_normalize_slides()` 辅助方法
       - `generate_products` 不再内部调用 `_clean_adp_products`（改由 flow_engine 统一管理）
    2. `.agent/flow_engine.py`：
       - V0_READY 阶段增加 `mode == "adp"` 判断
       - ADP 模式调用 `ADPMCP._clean_adp_products()` 而非 `clear_stage_outputs("mvp", ...)`
    3. `.agent/adp-execution-scope.json`：
       - 从 `clean.allow` 移除 `CourseApp/public/audio/{module}`、`subtitles/{module}`、`transcripts/{module}`
  - **DAG 同步**：`docs/Skill_Chain_DAG.md` 已更新（MVP/ADP 双模式说明、清理边界、全量写入架构、ADPMCP 节点职责）
  - **验证**：
    - Module_01/02/03/04 全部 DEPLOY_READY
    - `verify_course.py` ✅
    - `npm run build` ✅ (614ms)
    - 12 个音频文件完好无损
  - **提交**：`407039a` → `225f262`（14 commits 已 push）
  - **状态**：ADP 管线稳定

- **2026-05-05 (generate_audio.py clean_text 修复)**:
  - **根因**：`clean_text()` 只清理了代码块和标题符号，未清理粗体/斜体/链接/引用/列表等 Markdown 符号，也未移除内部指导字段（`shotInstruction` 等），导致 TTS 生成 MP3 时会读出这些符号和文字
  - **修复**：修改 `.agent/templates/scripts/generate_audio.py` 的 `clean_text()` 函数，新增：
    - 移除粗体/斜体符号（`**bold**` `*italic*`）
    - 移除链接/图片语法（`[text](url)` `![alt](url)`）
    - 移除引用符号（`>`）
    - 移除水平线（`---` `***` `___`）
    - 移除列表符号（`-` `*` `1.`）
    - 移除表格语法（`|`）
    - 移除内部指导字段（`shotInstruction|focusInstruction|implementationHint|learnerTakeaway|Now focusing`）
  - **验证**：重新运行 DAG（所有 4 个模块），`verify_course.py` ✅ 通过
  - **提交**：`b19f42a`（fix: templates/generate_audio.py）
  - **状态**：所有模块的音频已用修复后的 `clean_text()` 重新生成

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

- **2026-05-05 (course.json 修复)**:
  - **根因**：`course.json` 只配置了 Module_01，导致首页只显示一个模块
  - **修复**：更新 `course.json`，添加所有 4 个模块（Module_01/02/03/04）
  - **验证**：`npm run build` ✅ 通过
  - **提交**：`5a86a75`（fix: course.json - 添加所有 4 个模块）
  - **状态**：首页现在应该显示所有 4 个模块

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

## Modified Files (2026-05-06)

- `.agent/mcp_servers/adp_mcp.py` (重构：全量扫描写入、移除内部清理调用)
- `.agent/flow_engine.py` (修改：ADP 模式使用 ADP 专用清理)
- `.agent/adp-execution-scope.json` (修改：移除增量资产清理项)
- `docs/Skill_Chain_DAG.md` (更新：MVP/ADP 双模式说明)
- `.agent/STATE.md` (更新)
- `.agent/handoff/CURSOR_HANDOFF.md` (更新)

## DAG Impact

Yes. 2026-05-06 架构重构影响 DAG 清理策略和写入策略：

- **清理分离**：`flow_engine.py` 现在根据运行模式选择不同清理策略。MVP 用 `clear_stage_outputs("mvp")` 全量清理；ADP 用 `ADPMCP._clean_adp_products()` 只清理 scope 允许的路径。
- **全量写入**：`ADPMCP._write_course_app()` 不再依赖跨运行合并，改为每次全量扫描所有模块源文件，一次性写全量产物。
- **增量资产保护**：ADP 模式不清理音频、字幕、逐字稿等跨模块增量资产。
- DAG 节点顺序和产品契约不变。

## Unfinished / Blockers

- 无当前阻塞项。

## Verification

- `python scripts\verify_course.py` passed ✅
- `npm --prefix CourseApp run build` passed ✅
- 全部 4 模块 ADP DEPLOY_READY ✅
- 12 个音频文件完好无损 ✅

## Next Step

ADP 管线已稳定。可根据需要进行课程内容迭代或前端体验优化。
