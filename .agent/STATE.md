# Current Project State

## CURRENT ADP TRUTH - READ FIRST

This section supersedes older ADP state notes below.

- ADP is now a dispatcher command, not an ADPMCP full-writer.
- `--adp` reads `.agent/adp-scope.json` for module order and runs the standard `MVPMCP` complete-module pipeline for each module.
- ADP intentionally uses MVP generation semantics with accumulation: one initial ADP cleanup, then `MVPMCP.generate_products(accumulate=True, clean=False, scope_file_name="adp-scope.json")` per module.
- `ADPMCP.generate_products()` is deprecated/fail-fast. Do not restore the old full-scan/full-write path.
- Any older text saying ADP is full-scan/full-write or should call ADP-specific cleanup is historical only.
- ADP must accumulate CourseApp data, storyboard, design, and stitch manifests across modules. Ordinary single-module MVP keeps its original cleanup and scoped output behavior.

## DAG State

Latest verified state: **全部 4 模块 DEPLOY_READY**（ADP dispatcher 模式全量通过）。

## Active Module

全部模块（Module_01 ~ Module_04）已完成 ADP dispatcher 全量执行。

## Current Focus

代码示例、做题页、探索页数据已填充完成。三个 Lab 组件已创建并接入 ExploreView。动效（storyboard-contract）仅覆盖 Module_04，其余模块暂缓。

## 2026-05-06 Course Home Module Progress State

- Workflow-layer decision: course home module cards must expose optional local learner progress states: `看过 -> 学过 -> 已做题 -> 掌握`.
- The state is an ordered dependency chain. Selecting a later state implies earlier states; broken states such as mastered without practiced are invalid.
- Persistence lives in browser `localStorage` (`shadergui-module-progress-v1`) and must not be written into course source or generated data contracts.
- Implementation source is `.agent/templates/course-app/src/views/CourseHome.vue`; generated CourseApp should be updated by rerunning MVP/ADP, not by direct product edits.
- Verification was expanded in `scripts/verify_course.py` and `.agent/templates/scripts/verify_course.py`.

## 2026-05-06 ADP Storyboard Validation Fix

- Execution-layer ADP report proved Module_03 was failing in Storyboard validation before Voice/Design/Stitch.
- Root cause: accumulated storyboard validation compared bare `slideId` values, so another module's `p02` could be treated as an extra slide for Module_03. Warning-level findings were also treated as fatal.
- Workflow fix: `flow_engine.py` passes ADP mode into storyboard validation; `StoryboardMCP.validate_storyboard_contract()` compares `(moduleId, slideId)`, checks accumulated coverage, and only fails on non-warning errors.
- Product artifacts still need a fresh ADP execution by the execution layer.
## Recent Changes

- **2026-05-06 (Lab 组件创建 + ADP 全量通过)**:
  - **根因**：Module_02/03/04 的 explorations.json 引用了不存在的 Lab 组件，导致 StitchMCP 失败
  - **修复**：
    1. 创建 SmartUILinkageLab.vue（Module_02/p01 智能UI联动实验）
    2. 创建 ModularAssemblyLab.vue（Module_03/p00 模块化组装实验）
    3. 创建 RenderStatePlayground.vue（Module_04/p02 渲染状态调试试验场）
    4. 同步到 `.agent/templates/course-app/src/components/labs/`
    5. 更新模板 ExploreView.vue 注册新组件
  - **DAG 影响**：无。仅添加模板组件，未修改 DAG 节点/流程/规则
  - **验证**：ADP 全量 4 模块 DEPLOY_READY ✅，`verify_course.py` ✅，`npm run build` ✅（537ms）
  - **提交**：`f9d42e2`
  - **状态**：探索页 Lab 组件完整可用

- **2026-05-06 (代码示例 + 做题页 + 探索页数据填充)**:
  - **根因**：CourseContent/ 源数据缺失 codeBlocks、quizzes 格式不兼容、explorations 为空
  - **修复**：
    1. 4 个模块 slides.json 添加 codeBlocks（12 个代码块，从 doc/*.md 提取）
    2. Module_02/03/04 quizzes.json 转换为嵌套格式（匹配 QuizView schema）
    3. Module_02/03/04 explorations.json 添加探索记录 + slides.json 添加 explore 入口
  - **DAG 影响**：无。仅修改 CourseContent/ 源数据，不涉及 DAG 节点/流程
  - **验证**：`npm run build` ✅（verify_course.py 报 storyboard 覆盖不全，属已知遗留问题）
  - **待办**：Module_02/03/04 的 SmartUILinkageLab、ModularAssemblyLab、RenderStatePlayground 组件尚未创建，探索页显示"探索组件未找到"占位
  - **提交**：pending

- **2026-05-06 (clean_text H1 标题泄露修复)**:
  - **根因**：`generate_audio.py` 的 `clean_text()` 只移除 `#` 符号，H1 文档标题行（如 `# Managed Properties：面板的行政管理 —— 逐字稿`）被 TTS 朗读
  - **修复**：在 clean_text 开头新增正则，移除匹配 `—— 逐字稿` 的 H1 元数据标题行
  - **范围**：全部 4 模块（12 个音频文件）已重新生成
  - **验证**：`verify_course.py` ✅，字幕第一条直接从正文开始
  - **提交**：`f818dab`（Snapshot）
  - **状态**：音频/字幕不再泄露文档标题

- **2026-05-06 (ADP 全量写入架构重构)**:
  - **根因**：ADP 逐模块运行时，`_write_course_app` 跨运行合并依赖上一次的 `course.json`，但 `flow_engine.py` 的 `clear_stage_outputs("mvp", ...)` 删除整个 CourseApp/ 导致合并源消失
  - **修复（3 处）**：
    1. `adp_mcp.py`：`_write_course_app` 改为全量扫描写入（不依赖合并），新增 `_copy_all_course_content()`
    2. `flow_engine.py`：ADP 模式使用 `ADPMCP._clean_adp_products()` 而非 `clear_stage_outputs("mvp", ...)`，避免删除所有模块音频
    3. `adp-execution-scope.json`：从 clean allow 移除 audio/subtitles/transcripts（增量资产不可清理）
  - **同步**：`docs/Skill_Chain_DAG.md` 已更新（新增 ADP 模式说明、清理边界、全量写入架构）
  - **验证**：4 模块全部 DEPLOY_READY，`verify_course.py` ✅，`npm run build` ✅
  - **提交**：`407039a` → `225f262`（共 14 commits）
  - **状态**：ADP 管线稳定，可重复执行

- **2026-05-05 (generate_audio.py clean_text 修复)**:
  - **根因**：`clean_text()` 只清理了代码块和标题符号，未清理粗体/斜体/链接/引用/列表等 Markdown 符号，也未移除内部指导字段（`shotInstruction` 等），导致 TTS 生成 MP3 时会读出这些符号和文字
  - **修复**：修改 `.agent/templates/scripts/generate_audio.py` 的 `clean_text()` 函数，新增：移除粗体/斜体符号、链接/图片语法、引用符号、水平线、列表符号、表格语法、内部指导字段
  - **验证**：重新运行 DAG（所有 4 个模块），`verify_course.py` ✅ 通过
  - **提交**：`b19f42a`（fix: templates/generate_audio.py）
  - **状态**：所有模块的音频已用修复后的 `clean_text()` 重新生成

- **2026-05-05 (course.json 修复)**:
  - **根因**：`course.json` 只配置了 Module_01，导致首页只显示一个模块
  - **修复**：更新 `course.json`，添加所有 4 个模块（Module_01/02/03/04）
  - **验证**：`npm run build` ✅ 通过
  - **提交**：`5a86a75`
  - **状态**：首页现在应该显示所有 4 个模块

- **2026-05-05 (Sidebar 移动端悬浮按钮重构)**:
  - **目标**：将移动端导航从底部标签栏改为悬浮按钮 + 侧边栏
  - **修改**：`CourseApp/src/components/Sidebar.jsx`，`CourseApp/src/App.jsx`
  - **验证**：`npm run build` ✅ 通过
  - **提交**：`000bd14` + `bc883ef` + `8bd0a6a`
  - **状态**：移动端导航已重构

- **2026-05-05 (CURSOR_HANDOFF.md 修复)**:
  - **根因**：之前更新 `CURSOR_HANDOFF.md` 失败，未成功插入新条目
  - **修复**：直接编辑 `CURSOR_HANDOFF.md`，添加 Sidebar 重构条目
  - **提交**：`39f6e93`
  - **状态**：`CURSOR_HANDOFF.md` 已更新

- **2026-05-05 (ADP DAG node)**:
  - 创建新文件 `.agent/mcp_servers/adp_mcp.py`（平行节点）
  - 更新 `flow_engine.py` 支持 `--adp` 标志
  - 创建 `.agent/adp-scope.json`（完整 slideIds）
  - 更新 4 个模块的 `slides.json`，补充缺失的 slides
  - 新增 4 个逐字稿文件
  - 验证：`verify_course.py` ✅ 通过，`npm run build` ✅ 通过
  - 提交：`bb36efa` + `d0e322c`

- **2026-05-05 (ADP scope fix)**:
  - **根因**：`adp_mcp.py` 复用了 `MVPMCP` 的清理函数
  - **修复**：新建 `.agent/adp-execution-scope.json`，修改 `adp_mcp.py`
  - **验证**：`verify_course.py` ✅ 通过
  - 提交：`3308675` + `c945fdc`

## 2026-05-06 ADP Dispatcher State

Current DAG focus: ADP has been changed from a full-writer node into a dispatcher command that runs the normal complete-module MVP pipeline per module.

Commands:

```powershell
python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

Current product status: generated products still need rerun. `verify_course.py` intentionally fails on the old mixed ADP product state until MVP/ADP is executed again.
