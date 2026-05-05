# Current Project State

## DAG State

Latest verified state: DEPLOY_READY after repairing WorkBuddy flow-engine regressions.

## Active Module

Module_01

## Current Focus

ADPMCP 平行 DAG 节点已创建完成。Sidebar 移动端悬浮按钮已重构。course.json 已修复（添加所有 4 个模块）。

## Recent Changes

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
