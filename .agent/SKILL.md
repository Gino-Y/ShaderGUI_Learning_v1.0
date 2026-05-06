---
name: shadergui-expert
description: "Unity ShaderGUI 专家级开发 Skill。用于 ShaderGUI 工程化课程、Vue 课程播放器、MVP DAG、音频字幕、分镜头运行时和交互式学习内容的生成、验证与修复。"
version: "1.3.0"
project: ShaderGUI_Learning_v1.0
allowed-tools: Read, Edit, Bash
---

# ShaderGUI Expert Skill

## 对齐约束（必读）

- [AGENT_SINGLE_SOURCE] `.agent` 是唯一可信源；Cursor/Codex/其它平台只能作为执行器，禁止使用 `.cursor`/`.workbuddy` 作为规则/资产来源。
- [MVP_EXECUTION_CONTRACT] 执行 MVP 必须遵循 `docs/MVP_Execution_Contract.md` 和 `.agent/mvp-execution-scope.json`；禁止清理 `.agent`、`node_modules` 等禁区。
- [NO_INTERNAL_GUIDANCE_UI] 前端学习页面不得展示内部生产指导：`shotInstruction`、`focusInstruction`、`implementationHint`、`learnerTakeaway`、`Now focusing` 一律禁止展示。
- [TOKEN_LEVEL_ANIMATION] 代码类页面动效必须细化到代码字段/token，例如 `ShaderGUI`、`OnGUI`、`CustomEditor`、`FindProperty`、`ShaderProperty`；不得退化为整卡片或整块代码动画。
- [COURSE_HOME_ALIGNMENT_GRID] 首页与模块入口必须统一为单层菜单。
- [SYNC_RULES_DAG_VERIFY] 任何影响规则/DAG/验收标准的改动必须同步更新 `docs/Skill_Chain_DAG.md`、`.agent/rules.md`、`.agent/SKILL.md` 和 `scripts/verify_course.py`。
- [REVERIFY_BUILD_BROWSER] 修改后必须循环自检：`verify_course.py`、`npm run build` 和必要浏览器验证。
- [COMPLETION_GATE_FILE_DRIVEN] 任务完成必须以仓库文件和验证结果为准，不得只靠对话记忆。
- [NO_DIRECT_EDIT_OUTPUT] **禁止直接修改产物文件**；只能通过修改 `.agent/` 中的 MCP 节点或模板后重新生成的方式修改。`CourseApp/`、`CourseApp/dist/`、`CourseApp/src/data/` 均为产物，不得直接编辑。
  - **MVP清理例外**：执行 MVP 前允许直接移除产物文件（清理操作），但重新生成后不得手动修改产物。
  - **测试型修改**：允许为快速验证而直接修改产物文件，但测试结果确认后，必须立即将改动同步回对应的 DAG 节点（MCP Server 或模板），确保 MVP 和正式生产时的一致性。未同步前不得视为完成。

## 角色定位

本 Skill 把 AI 定位为 ShaderGUI 课程工程的技术负责人：既要理解 Unity ShaderGUI 的工程实践，也要维护课程生产 DAG、Vue 运行时、音频字幕、分镜头契约、探索页和做题页的可交付状态。

## 强制规则

- 所有文本资产必须是 UTF-8。
- `.agent/` 是唯一规则源和 Skill 源。
- Cursor 或其它平台出现私有资产回流时，必须执行平台违规校正程序。
- 每次用户反馈都要判断 DAG 是否受影响。
- 修改课程运行时代码时，同步模板、验证脚本和 memory。
- 修复不能只停在源码，必须跑到可验证结果。

## MVP 工作流

唯一 MVP 入口：

```powershell
python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
```

节点顺序：

1. `CourseMCP` 检查源材料、规则和执行边界。
2. `MVPMCP` 清理可再生产物并生成 Vue SPA、课程数据、脚本。
3. `StoryboardMCP` 生成分镜头契约和 motion cues。
4. `V0MCP` 生成 React 原型和设计规则引用。
5. `DesignMCP` 生成 Vue 转译设计契约。
6. `VoiceMCP` 生成 MP3 和字幕事件。
7. `StitchMCP` 绑定幻灯片、音频、字幕、探索页、做题页和运行时组件。
8. `BuildMCP` 执行 Vue 构建。
9. `AuditMCP` 执行安全审计。

## 前端运行时

- Vue 3 + Vue Router + Tailwind CSS。
- `CoursePlayer.vue` 必须绑定 `storyboard-contract.json`、`activeCue`、`visualComposition`、`motionCues` 和音频时间事件。
- `SlideCanvas.vue` 必须消费分镜头契约，不得退回静态 PPT 画布。
- `SlideNav.vue` 负责播放、进度条、翻页、探索入口、模块入口。
- `SubtitleOverlay.vue` 只显示音频事件驱动的字幕。

## 探索页与做题页

- 探索页只能作为父课时 `/explore` 子页面，不占用 `pXX`。
- 探索页必须经过 `interaction-necessity-gate`。
- 做题页路由固定为 `/module/:moduleId/quiz`。
- 做题页只显示当前题卡和统一导航，提交后自动推进，最后展示成绩页。
- 选项和题目顺序必须可随机化。

## Web 交互式内容 Skill 链

- `web-interactive-content-builder` 是总控 Skill。
- `skill-router` 根据概念特征选择子 Skill。
- 子 Skill 包括 `interactive-article-skill`、`explorable-mini-skill`、`parameter-playground-skill`、`creative-workbench-skill`、`animated-lesson-skill`、`chapter-lab-skill`。
- ShaderGUI 课程默认组合：`chapter-lab-skill` 管课程结构，`explorable-mini-skill` 管单节探索实验。

## 验证

最小验证：

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

涉及浏览器行为时，还要验证：

- `/`
- `/module/Module_01/slide/p00`
- `/module/Module_01/slide/p01`
- `/module/Module_01/slide/p01/explore`
- `/module/Module_01/quiz`
- `/audio/Module_01/p00.mp3`
- `/audio/Module_01/p01.mp3`

## 交付

最终回复必须说明：

- DAG 是否受影响。
- 修改了哪些关键区域。
- 运行了哪些验证。
- 本地 URL 是否可访问。
- 仍有哪些风险或阻塞。

## Small Fix Ownership

小而确定、低风险的一致性问题由当前执行方直接修复，不再要求用户手动处理。若 Cursor 或其它工具正在同一文件/同一任务范围内执行，当前执行方不直接抢改，必须给用户一段可复制给 Cursor 的明确指令，写清文件、改法和验证命令。只有当问题涉及产品行为、DAG 契约、运行时代码、数据语义或设计取舍时，才向用户确认。

## ADP 工作流

ADP 是调度命令，不是独立产物生成器：

```powershell
python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

- `--adp` 读取 `.agent/adp-scope.json` 的模块列表。
- 每个模块按完整模块范围运行同一条 MVP pipeline。
- ADP 不再使用全量写入式 `ADPMCP.generate_products()`。
- 当前被用户指定为执行层的平台只是执行器；规则、DAG、handoff、memory 仍只来自 `.agent/`。

## Runtime Role Switching

Roles are not permanently bound to platforms. When the user says `你是 <role>`, the current platform immediately follows that role until the user switches again or the task ends.

- workflow/DAG/工作流层: edit `.agent/`, docs, DAG contracts, MCP orchestration, templates, verification gates, handoff, memory, and rules. Avoid direct product edits.
- product/执行层/产物层: execute MVP/ADP, inspect generated output, and fix product-facing defects through the approved DAG/template/MCP path. Do not create workflow rules or private platform assets.
- review/检查层: inspect and report only unless the user explicitly asks for repair.

This is a role switch, not platform binding. Codex, Cursor, and any other executor can serve any role when the user explicitly assigns it.

## ADP Accumulation Semantics

`--adp` performs one initial cleanup, then accumulates module outputs across the normal MVP pipeline. Course data, storyboard, design, and stitch manifests must merge by `moduleId`; ordinary MVP remains single-module and clean-first.
