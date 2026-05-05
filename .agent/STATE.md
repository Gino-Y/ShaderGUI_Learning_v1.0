# Current Project State

## DAG State

Latest verified state: **全部 4 模块 DEPLOY_READY**（ADP 全量写入架构）。

## Active Module

全部模块（Module_01 ~ Module_04）已完成 ADP 生产管线。

## Current Focus

ADP 全量写入架构已落地并验证通过。MVP 模式与 ADP 模式已分离，清理策略、写入策略各自独立。

## Recent Changes

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
