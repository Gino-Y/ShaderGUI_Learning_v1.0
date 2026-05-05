# Current Project State

## DAG State

Latest verified state: DEPLOY_READY after repairing WorkBuddy flow-engine regressions.

## Active Module

Module_01

## Current Focus

ADPMCP 平行 DAG 节点已创建完成。Sidebar 移动端悬浮按钮已重构。course.json 已修复（添加所有 4 个模块）。

## Recent Changes

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
