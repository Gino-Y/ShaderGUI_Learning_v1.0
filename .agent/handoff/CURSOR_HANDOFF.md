# Cursor Handoff

## Current Goal

代码示例、做题页、探索页数据已填充。动效暂缓（仅 Module_04 有 storyboard-contract）。探索页 Lab 组件待创建。

## Completed Work

- **2026-05-06 (代码示例 + 做题页 + 探索页数据填充)**:
  - **修改文件**：
    - `CourseContent/Module_01/slides.json`（添加 p01 手写代码 + p02 codeBlocks）
    - `CourseContent/Module_02/slides.json`（添加 p00/p01/p02 codeBlocks + p01 explore 入口）
    - `CourseContent/Module_03/slides.json`（添加 p00/p01 codeBlocks + p00 explore 入口）
    - `CourseContent/Module_04/slides.json`（添加 p00 2个 codeBlocks + p01 2个 + p02 + p03 + p02 explore 入口）
    - `CourseContent/Module_02/quizzes.json`（格式转换：扁平→嵌套 questions[]）
    - `CourseContent/Module_03/quizzes.json`（格式转换）
    - `CourseContent/Module_04/quizzes.json`（格式转换）
    - `CourseContent/Module_02/explorations.json`（添加 SmartUILinkageLab 探索）
    - `CourseContent/Module_03/explorations.json`（添加 ModularAssemblyLab 探索）
    - `CourseContent/Module_04/explorations.json`（添加 RenderStatePlayground 探索）
  - **DAG 影响**：无。仅 CourseContent/ 源数据变更
  - **验证**：`npm run build` ✅，`verify_course.py` 报 storyboard 覆盖不全（已知遗留）
  - **待办**：创建 SmartUILinkageLab、ModularAssemblyLab、RenderStatePlayground 组件

- **2026-05-06 (clean_text H1 标题泄露修复)**:
  - **根因**：`generate_audio.py` 的 `clean_text()` 只移除 `#` 符号，H1 文档标题行（如 `# Managed Properties：面板的行政管理 —— 逐字稿`）被 TTS 朗读
  - **修复**：`clean_text()` 开头新增正则移除匹配 `—— 逐字稿` 的 H1 元数据标题行
  - **影响范围**：全部 4 模块（12 个音频 + 12 个字幕）已重新生成
  - **DAG 影响**：无。仅修改模板脚本的文本预处理逻辑，不涉及 DAG 节点、流程或产物契约
  - **验证**：`verify_course.py` ✅
  - **提交**：`f818dab`
  - **状态**：音频/字幕不再泄露文档标题

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

## 2026-05-06 flow_engine ADP CLI guard
- `flow_engine.py` test cleanup is now mode-aware for `--adp --stage mvp`: it calls `ADPMCP._clean_adp_products()` and prints cleanup stage `adp`.
- This closes the remaining accidental MVP cleanup path at the CLI entrypoint.
- Verified with `python -m py_compile .agent\flow_engine.py .agent\run_guard.py .agent\mcp_servers\adp_mcp.py .agent\mcp_servers\mvp_mcp.py .agent\mcp_servers\v0_mcp.py .agent\mcp_servers\design_mcp.py` and `python .agent\platform_violation_guard.py --basedir .`.
- Full product verification/build was intentionally not rerun during this lightweight engine audit.

## 2026-05-06 ADP root cause / verify gap
- ADP imperfection is not explained by MVP success: ADPMCP writes full global `slides.json`, while storyboard/design/stitch still write current-module-only data into global files.
- Confirmed current generated data: slides cover Module_01~04, but storyboard/design/stitch manifests only cover Module_04; Module_01~03 lack contract coverage.
- Updated `scripts/verify_course.py` and `.agent/templates/scripts/verify_course.py` to fail when storyboard/design/stitch do not cover all generated slides.
- Next fix should make StoryboardMCP/DesignMCP/StitchMCP either aggregate all modules in ADP mode or emit per-module contract files that runtime resolves by module.

## 2026-05-06 ADP as MVP dispatcher
- DAG upgraded: ADP is now a command/dispatcher, not a second generator.
- `python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp` reads `.agent/adp-scope.json` and runs the normal MVPMCP full-module pipeline for each module.
- `ADPMCP.generate_products()` now returns an error explaining it is deprecated, preventing accidental old full-writer use.
- `.agent/mvp-scope.json` now contains complete module slide ranges.
- workbuddy/Cursor/Codex may execute MVP or ADP commands only; all rules/handoff/memory remain in `.agent/`, no `.workbuddy/` source directory.
- Verified: `python -m py_compile ...` passed; platform guard passed; ADP target expansion returns Module_01~Module_04.
- Current product verification still fails until regenerated: existing products are old mixed ADP state, and `verify_course.py` correctly blocks missing storyboard/design/stitch coverage.

## 2026-05-06 Runtime role switching
- Rules updated: role is not hard-bound to platform. Explicit user phrase `你是 <role>` switches the active executor immediately.
- Supported layers: workflow/DAG/工作流层, product/执行层/workbuddy, review/检查层.
- Workflow layer changes rules/DAG/MCP/templates/verification/handoff; product layer runs MVP/ADP and product-facing checks via DAG path; review layer reports only unless repair is requested.
