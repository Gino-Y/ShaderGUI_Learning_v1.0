# ShaderGUI_Learning_v1.0 项目 AI 行为规则

本文件是项目 AI 协作、课程生成、MVP 验证和交付的强制规则源。所有平台只能把 `.agent/` 作为可信源，Cursor、Codex 或其它 AI 平台都只是执行器。

## 对齐约束（必读）

- [GIT_SNAPSHOT_BEFORE_MODIFY] **修改代码前必须创建Git快照**（详见第126行"Git快照与回滚规范"）；快照不是备份，是在重要节点创建的可回溯标记。
- [GIT_COMMIT_AFTER_TASK] **任务完成后必须提交Git**（详见第223行"Git协作工作流规范"）；不得积累大量未提交改动。
- [NO_CONTEXT_INFERENCE] **禁止通过上下文推测执行流程**：AI 不得从对话上下文、历史记录或推理中推断"应该做什么"或"下一步"。所有执行流程、触发条件、完成标准必须以文本形式写入规则文件（`rules.md`、`SKILL.md`、DAG、`STATE.md`、`CURSOR_HANDOFF.md`）。未写入规则文件的流程视为不存在，AI 不得自行假设执行。
- [AGENT_SINGLE_SOURCE] `.agent` 是唯一可信源；禁止使用 `.cursor`、`.workbuddy` 作为规则、资产、Skill、workflow 或 prompt 来源。
- [MVP_EXECUTION_CONTRACT] 执行 MVP 必须遵循 `docs/MVP_Execution_Contract.md` 和 `.agent/mvp-execution-scope.json`；禁止清理 `.agent`、`node_modules` 等禁区。
- [NO_INTERNAL_GUIDANCE_UI] 前端学习页面不得展示内部生产指导：`shotInstruction`、`focusInstruction`、`implementationHint`、`learnerTakeaway`、`Now focusing` 一律禁止展示。
- [TOKEN_LEVEL_ANIMATION] 代码类页面动效必须细化到代码字段/token，例如 `ShaderGUI`、`OnGUI`、`CustomEditor`、`FindProperty`、`ShaderProperty`；不得退化为整卡片或整块代码动画。
- [COURSE_HOME_ALIGNMENT_GRID] 首页和模块入口必须使用统一菜单结构，展示课程首页、模块信息、课时入口、探索入口和做题页入口，不得恢复二级菜单页。
- [DUAL_COMPLIANCE] **双规（双重合规）**：通过上下文（对话/推理）更改产物后，必须同时满足两条铁规，否则构成双重违规：
  - **铁规1 同步 DAG 节点**（`[SYNC_RULES_DAG_VERIFY]`）：任何影响规则、DAG、验收标准的改动必须同步更新 `docs/Skill_Chain_DAG.md`、`.agent/rules.md`、`.agent/SKILL.md` 和 `scripts/verify_course.py`，必要时同步 `.agent/mcp_servers/mvp_mcp.py`。
  - **铁规2 汇报 AI 交叉开发文档**（`[COMPLETION_GATE_FILE_DRIVEN]`）：禁止仅靠对话记忆收尾；凡触及 `CourseApp/`、`.agent/mcp_servers/`、`scripts/`、`.agent/templates/`、`CourseContent/`、`docs/Skill_Chain_DAG.md`、`.agent/handoff/` 或课程数据契约，必须更新 STATE、handoff、memory 并运行验证。
- [REVERIFY_BUILD_BROWSER] 需循环自检直至交付：`verify_course.py`、`npm run build`、启动开发服务器（`npm --prefix CourseApp run dev`）、输出 `http://localhost:5173/` URL，未通过不算完成。本地服务可用时，最终回复必须给出 URL。
- [NO_DIRECT_EDIT_OUTPUT] **禁止直接修改产物文件**；只能通过修改 `.agent/` 中的 MCP 节点或模板后重新生成的方式修改。`CourseApp/`、`CourseApp/dist/`、`CourseApp/src/data/` 均为产物，不得直接编辑。
  - **MVP清理例外**：执行 MVP 前允许直接移除产物文件（清理操作），但重新生成后不得手动修改产物。
  - **测试型修改**：允许为快速验证而直接修改产物文件，但测试结果确认后，必须立即将改动同步回对应的 DAG 节点（MCP Server 或模板），确保 MVP 和正式生产时的一致性。未同步前不得视为完成。
- [STOP_DEV_SERVER_BEFORE_MVP] **执行 MVP 前必须关闭开发服务器**；开发服务器会占用端口并锁定文件，导致 MVP 清理/重新生成失败。执行 `npm --prefix CourseApp run dev` 的进程必须先终止。

## 单一资产源

- 所有 AI 规则、Skill、DAG、MCP、memory、handoff、报告和模板必须维护在 `.agent/`。
- 发现 `.cursor/`、`.workbuddy/` 中出现规则、canvas、workflow、Skill、prompt、DAG、MVP 说明或课程生成逻辑时，必须执行违规校正程序。
- 有价值内容迁移到 `.agent/`；重复内容删除；过期或冲突内容隔离到 `.agent/reports/cleanup/` 后删除原件。
- 任何平台私有上下文不得作为工程源头参与 MVP 生成。

## UTF-8 编码标准

所有文本文件必须使用 `UTF-8`。这包括 `.md`、`.txt`、`.json`、`.js`、`.ts`、`.tsx`、`.vue`、`.css`、`.html`、`.py`、`.yml`、`.yaml`、`.csv`、`.env`、handoff、memory、rule、DAG、Skill 和所有生成文本产物。

- 新建文本文件必须写入 UTF-8。
- 被触碰的旧文本文件如果出现乱码、mojibake 或跨平台读取异常，必须规范化为 UTF-8。
- `.agent/` 资产永远不能漂移到 ANSI、GBK、UTF-16 或平台默认编码。
- 编码违规是交付阻塞项。
- 如果 Cursor 或其它平台写入非 UTF-8 文本，按平台违规校正程序处理。

## MVP 执行

唯一 MVP 入口：

```powershell
python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
```

- 当前 MVP scope 由 `.agent/mvp-scope.json` 声明，默认正式课程序列为 `p00/p01`。
- 探索页只能作为父课时子页面，例如 `/module/:moduleId/slide/:slideId/explore`，不得占用 `pXX` 编号，不得计入 `slideCount`。
- `MVPMCP` 只能装配 `.agent/templates/` 和课程源数据，不得在 MCP 内嵌大段 Vue、CSS、脚本或课程实例文本。
- MVP 清理范围必须以 `.agent/mvp-execution-scope.json` 为准。

## Cursor / Codex 一致性

Cursor、Codex 或任何其它 AI 平台执行 MVP 时，只能作为执行器，不能作为资产源、规则源或上下文源。

- 允许差异仅限 `generatedAt`、v0 chat id/url、音频二进制 hash、构建产物 hash。
- 不允许差异包括课程 scope、路由、`storyboard-contract.json`、`design-contract.json`、`stitch-manifest.json`、`CoursePlayer.vue` 的 storyboard 绑定、`SlideCanvas.vue` 的分镜头运行时绑定。
- 发现漂移时必须修 `.agent/` 链路，不得在平台私有上下文中补丁式修复。

## Cursor 自动提醒 / 阻断机制

- `platform_violation_guard.py` 扫描 `.cursor/`、`.workbuddy/` 中疑似规则、canvas、workflow、skill、prompt、DAG、MVP 或课程生成资产。
- `run_guard.assert_workspace()` 在每次执行 `.agent/flow_engine.py` 前自动调用平台违规守卫。
- 违规时必须以 `CURSOR_PLATFORM_VIOLATION` fail-fast。
- 人类可读报告写入 `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.md`。
- 机器可读报告写入 `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.json`。
- 可执行校正命令：`python .agent/platform_violation_guard.py --basedir . --fix`。

## DAG 与反馈

- 每次用户反馈后必须判断 DAG 是否受影响。
- 影响流程、节点职责、产物契约、验证标准、目录结构或交付定义时，必须更新 `docs/Skill_Chain_DAG.md`。
- 即使不影响 DAG，也要在 memory 或 handoff 中说明“不影响 DAG”的理由。
- 最终回复必须说明 DAG 是否已更新及更新位置。

## 课程前端

- 技术栈固定为 Vue 3、Vue Router、Tailwind CSS、Vite。
- 最终交付为 SPA，不允许恢复为多份独立 HTML。
- 路由必须包含 `/`、`/module/:moduleId/slide/:slideId`、`/module/:moduleId/slide/:slideId/explore`、`/module/:moduleId/quiz`。
- `/module/:moduleId` 只作为兼容入口，不得承载二级菜单页。
- 页面、音频、字幕和讲稿映射必须由 `CourseApp/src/data/*.json` 驱动。

## 分镜头与设计

- `StoryboardMCP` 位于 `DesignMCP` 之前，状态流为 `MANIFEST_READY -> STORYBOARD_READY -> DESIGN_READY`。
- `storyboard-contract.json` 是设计前置契约，不得由 `design-contract.json` 替代。
- 动效写入 `motionCues[]`，以 `subtitle-segment` 或音频事件作为触发。
- `SlideCanvas.vue` 必须消费 `activeCue`、`visualComposition`、`motionCues` 和 `codeHighlightTokens`。
- 学习页面不得展示故事板指令、设计契约说明、Skill 链说明或任何内部生产文档。

## v0 规则

- `V0MCP.validate_api_key` 只代表连通性，不代表画面已经由 v0 改造。
- `V0MCP.generate_react_prototype` 必须在 `StoryboardMCP` 后执行。
- v0 输出只作为 React 原型和设计规则来源，最终运行时代码必须转译为 Vue 3 + Tailwind。
- `DesignMCP` 必须通过 `v0PrototypeRef` 承接 v0 chat、原型文件和设计规则。

## 音频与字幕

- 课程音频必须由逐字稿通过 TTS 生成正式 MP3。
- 禁止蜂鸣、正弦波、静音轨或测试音频作为交付产物。
- `slides.json` 中音频路径必须指向 `/audio/Module_XX/pNN.mp3`。
- 字幕事件必须跟随真实音频播放推进，不得在静音 fallback 中伪推进。
- 自动播放被浏览器拦截时，必须等待用户点击页面或播放按钮解锁有声播放。

## 做题页

- 课程 quiz 统一称为“做题页”，路由为 `/module/:moduleId/quiz`。
- 做题页默认只展示当前题卡和统一导航，不展示题库表格、题号列表或全页题目流。
- 提交后自动进入下一题，全部答完后展示成绩页。
- 每次重新挑战或继续练习必须随机抽样题目并洗牌选项。
- 成绩页必须提供重新挑战、继续练习、回到当前课程、进入下一课、回到菜单的返回策略。
- 错题复盘在选项列表中标记正确答案和用户选择，下方只保留简短错因提示，不重复列出完整答案文本。

## 探索页

- 探索页必须先通过 `interaction-necessity-gate`。
- 探索页是父课时的子页面，不属于 `pXX` 范围。
- 探索入口由播放器导航或对应课时入口管理，不得塞入 PPT 内容画布。
- 探索页必须提供回到父课时、回到模块、去做题页等统一导航。
- 不得为了增加功能而增加探索页；只有静态讲解和做题不足以达成学习目标时才允许插入。

## Web 交互式内容 Skill

- 总控 Skill：`web-interactive-content-builder`。
- 路由 Skill：`skill-router`。
- 子 Skill：`interactive-article-skill`、`explorable-mini-skill`、`parameter-playground-skill`、`creative-workbench-skill`、`animated-lesson-skill`、`chapter-lab-skill`。
- ShaderGUI 课程默认组合：`chapter-lab-skill` 管课程结构，`explorable-mini-skill` 管单节小实验。

## Git 快照与回滚规范

### 目标

确保每次重要操作前都有 Git 快照，方案失败时可快速、准确地回滚到上一个稳定状态。

### 核心规则

1. **指令执行前必须创建 Git 快照**
   - 在任何 P0/P1/P2/P3/P4 阶段执行前
   - 在任何架构决策、方案切换前
   - 在任何可能影响现有功能的修改前

2. **快照命名规范**
   - 格式：`Snapshot: [阶段/决策] - [简短描述]`
   - 示例：
     - `Snapshot: Pre-Lottie - Before trying Lottie integration`
     - `Snapshot: Pre-Native-Node - Before switching to native performance nodes`
     - `Snapshot: Pre-DAG-Integration - Before modifying flow_engine.py`

3. **回滚优先级**
   - **首选**：Git 回滚 (`git reset --hard <commit-hash>`)
   - **次选**：手动还原（仅适用于未提交的小改动）
   - **禁止**：直接修改文件而不创建快照

4. **快照检查清单**
   - [ ] 工作区是否干净（无未提交改动）？
   - [ ] 是否所有重要文件都已提交？
   - [ ] 快照描述是否清晰、可回溯？

### 实施细节

**何时创建快照：**
- 阶段开始前（P0、P1、P2、P3、P4）
- 方案切换前（如从 Lottie 切换到原生组件）
- 重要决策前（如修改 DAG、更新 Schema）
- 用户明确要求快照时

**如何创建快照：**
```powershell
# 1. 检查工作区状态
git status

# 2. 添加所有改动
git add .

# 3. 创建快照（使用描述性 commit message）
git commit -m "Snapshot: [阶段/决策] - [描述]"
```

**如何回滚：**
```powershell
# 1. 查看 Git 日志，找到目标快照
git log --oneline

# 2. 回滚到指定快照
git reset --hard <commit-hash>

# 3. 如果已推送到远程，需要强制推送（谨慎！）
git push origin <branch> --force
```

### 示例

**示例 1：方案切换前创建快照**
```powershell
# 用户决定尝试 Lottie 方案
git add .
git commit -m "Snapshot: Pre-Lottie - Before trying Lottie integration"

# ... 执行 Lottie 集成 ...

# 用户宣布方案失败，回滚
git reset --hard <snapshot-hash>
```

**示例 2：阶段执行前创建快照**
```powershell
# P3 阶段开始前
git add .
git commit -m "Snapshot: Pre-P3 - Before integrating PerformanceNode into SlideCanvas"

# ... 执行 P3 ...

# 如果 P3 失败，回滚
git reset --hard HEAD~1
```

### 注意事项

- 快照不是备份，不要在其中包含敏感信息（如 API keys、密码）
- 如果工作区有未提交的改动，先提交或 stash，再创建快照
- 快照描述要清晰，便于后续回溯和恢复
- 不要过度创建快照（如每修改一行代码就创建一次），在重要节点创建即可

---

## Git 协作工作流规范

### 目标

确保本地开发与远程仓库保持同步，避免因不同步导致的冲突和代码丢失。

### 核心规则

#### 1. Pull 拉取规则（必须强制执行）

**何时必须 Pull：**
- **首次克隆后**：第一次从远程仓库克隆代码后，必须 pull 一次确保最新
- **每天开始前**：每天开发工作开始时，必须先 `git pull`
- **每个大阶段开始前**：P0/P1/P2/P3/P4 阶段开始前，必须先 `git pull`
- **切换分支前**：切换分支前必须先 pull 当前分支和目标分支
- **合并代码前**：合并分支前必须先 pull 目标分支

**Pull 命令规范：**
```powershell
# 开始工作前（推荐）
git pull origin main

# 如果本地有未提交改动（先暂存）
git stash
git pull origin main
git stash pop

# 如果本地有未提交改动（先提交）
git add .
git commit -m "WIP: 临时提交"
git pull origin main
```

**Pull 失败处理：**
```powershell
# 如果 pull 冲突，先查看冲突文件
git status

# 手动解决冲突后
git add .
git commit -m "Resolve merge conflicts"

# 如果无法解决冲突，回滚 pull
git merge --abort
```

#### 2. 原子提交快照规则（开发中）

**原子提交原则：**
- 每个提交只做一个逻辑修改（原子性）
- 提交信息必须清晰描述修改内容
- 禁止一次性提交大量不相关改动

**提交命名规范：**
```
格式：[类型] [范围/阶段] - [简短描述]

类型：
- feat: 新功能
- fix: 修复 bug
- refactor: 重构（不改变外部行为）
- docs: 文档更新
- style: 代码格式（不影响功能）
- test: 测试相关
- chore: 构建/工具/依赖更新

示例：
- feat: Module_01 - 完成 P0 阶段 Lottie 白名单集成
- fix: SlideCanvas - 修复音频播放器崩溃问题
- refactor: storyboard_mcp - 重构 motionCues 生成逻辑
- docs: rules.md - 更新 Git 工作流规范
- Snapshot: Pre-P1 - 创建 P1 阶段前快照
```

**提交检查清单：**
- [ ] 提交是否原子性（只做一个逻辑修改）？
- [ ] 提交信息是否清晰、可回溯？
- [ ] 是否所有相关文件都已提交？
- [ ] 是否通过了 `verify_course.py` 和 `npm run build`？

**提交命令规范：**
```powershell
# 1. 检查工作区状态
git status

# 2. 添加相关文件（不要盲目 git add .）
git add <specific-files>
# 或者分批次提交
git add .agent/mcp_servers/storyboard_mcp.py
git commit -m "fix: storyboard_mcp - 修复 motionCues 引用"

# 3. 推送前先 pull
git pull origin main

# 4. 解决冲突（如果有）后再推送
```

#### 3. Push 推送规则（阶段完成时）

**何时 Push：**
- **每个大阶段完成后**：P0/P1/P2/P3/P4 完成后必须 push
- **每天工作结束时**：当天工作结束前必须 push
- **重要功能完成后**：单个重要功能完成后建议 push
- **修复关键 bug 后**：修复关键 bug 后必须 push

**Push 命令规范：**
```powershell
# 1. 检查本地提交
git log --oneline -5

# 2. 推送前先 pull（确保远程无新提交）
git pull origin main --rebase

# 3. 推送到远程
git push origin main

# 4. 如果推送失败（远程有新提交），先 pull 再 push
git pull origin main
git push origin main
```

**Push 失败处理：**
```powershell
# 如果 push 被拒绝（远程有新提交）
git pull origin main --rebase
# 解决冲突（如果有）
git add .
git rebase --continue
git push origin main

# 如果 rebase 出错，中止 rebase
git rebase --abort
```

#### 4. 远程仓库维护规则

**分支管理：**
- **main 分支**：生产就绪代码，必须稳定
- **功能分支**：开发新功能时创建功能分支（如 `feature/lottie-integration`）
- **禁止直接 push 到 main**：如果仓库设置了保护规则

**标签管理：**
- 重要里程碑打标签（如 `v0.1.0-Module_01-DEPLOY_READY`）
- 标签命名规范：`v<major>.<minor>.<patch>-<milestone>`

```powershell
# 创建标签
git tag -a v0.1.0-Module_01-DEPLOY_READY -m "Module_01 MVP 完成，所有验证通过"
git push origin v0.1.0-Module_01-DEPLOY_READY
```

### 完整工作流示例

**示例 1：每天开始工作**
```powershell
# 1. 拉取最新代码
git pull origin main

# 2. 检查状态
git status
git log --oneline -3

# 3. 开始工作
# ... 开发中 ...

# 4. 原子提交
git add .agent/mcp_servers/storyboard_mcp.py
git commit -m "fix: storyboard_mcp - 修复 motionCues 引用"

# 5. 推送
git push origin main
```

**示例 2：大阶段开始前**
```powershell
# 1. 拉取最新代码
git pull origin main

# 2. 创建快照
git add .
git commit -m "Snapshot: Pre-P1 - Before starting P1 Lottie integration"

# 3. 开始 P1 阶段
# ... P1 开发中 ...

# 4. P1 完成，原子提交
git add .agent/ CourseApp/src/
git commit -m "feat: Module_01 P1 - 完成 Lottie 集成"

# 5. 推送
git push origin main
```

**示例 3：功能分支工作流**
```powershell
# 1. 从 main 创建功能分支
git checkout -b feature/lottie-integration

# 2. 开发中，原子提交
git add .
git commit -m "feat: lottie - 添加 LottieStage 组件"
git commit -m "feat: lottie - 更新 storyboard-contract.json"

# 3. 功能完成，合并到 main
git checkout main
git pull origin main
git merge feature/lottie-integration
git push origin main

# 4. 删除功能分支
git branch -d feature/lottie-integration
```

### 注意事项

- **禁止强制推送（git push --force）**：除非你确定要覆盖远程历史
- **禁止提交敏感信息**：API keys、密码、token 等
- **禁止提交大文件**：音频、视频、二进制文件等，使用 Git LFS
- **提交前必须验证**：`verify_course.py` 和 `npm run build` 必须通过
- **Push 前必须先 Pull**：避免冲突和代码丢失

---

## 循环自检

每次生成、修改、重构、排版或代码实现后必须执行闭环：

1. 生成可运行或可交付初版。
2. 对照 `.agent/rules.md`、`.agent/SKILL.md`、DAG 和用户目标自检。
3. 主动修复发现的问题。
4. 重新验证，直到达到交付标准。
5. 最终回复说明已交付内容、验证结果、风险或未完成项。

最小验证：

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

## Handoff Quality Gate

每轮结束必须更新：

- `.agent/STATE.md`
- `.agent/handoff/CURSOR_HANDOFF.md`
- `.agent/memory/YYYY-MM-DD*.md`

handoff 必须列出修改文件、验证命令、验证结果、DAG 是否受影响、未完成/阻塞和下一步。不能只写“已完成”。

## Small Fix Ownership

小而确定、低风险的一致性问题由当前执行方直接修复，不得要求用户手动处理。范围包括日期过期、路径不一致、遗漏 handoff/memory/STATE、验证模板漂移、规则短句重复、明显笔误和 UTF-8 编码问题。

如果其它工具已经在同一文件或同一任务范围内执行，当前执行方不得制造冲突；必须输出可直接交给该工具的清晰指令，包含文件、改法和验证命令。

## ADP 执行

[ADP_AS_MVP_DISPATCHER] ADP 不是第二套生成器。`--adp` 只负责按 `.agent/adp-scope.json` 调度模块列表；每个模块必须进入同一条 `MVPMCP` 完整模块 pipeline。

ADP 入口：

```powershell
python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

- ADP 不得调用全量写入式 `ADPMCP.generate_products()`。
- ADP 不得产出 all-module `slides.json` 搭配 current-module `storyboard/design/stitch` 的混合状态。
- 当前被用户指定为执行层的平台只能作为执行器运行 MVP/ADP 命令；不得创建或依赖 `.workbuddy/`、`.cursor/` 私有规则资产。
- 执行后必须以 `scripts/verify_course.py`、`npm --prefix CourseApp run build`、handoff 和 memory 作为完成依据。

## Runtime Role Switching

[ROLE_SWITCH_NOT_PLATFORM_BINDING] Roles are runtime responsibilities, not permanent platform bindings. Codex, Cursor, or any other executor is not inherently tied to one role. The user may switch the current platform role by saying `你是 <role>` or an equivalent explicit instruction.

Supported roles:

- `workflow` / `DAG` / `架构层` / `工作流层`: the current platform may edit only workflow-layer assets such as `.agent/`, `docs/`, DAG contracts, MCP orchestration, templates, verification gates, handoff, memory, and rules. It must not directly edit generated product files except for verification or clearly marked temporary inspection.
- `product` / `产物层` / `执行层`: the current platform may execute MVP/ADP commands, inspect generated output, and fix product-facing defects only through the approved DAG/template/MCP path. It must not invent new workflow rules, prompts, private assets, or hidden platform memory.
- `review` / `检查层`: the current platform only inspects, reports risks, and proposes or records fixes. It must not modify files unless the user then switches role or explicitly asks for repair.

Switching rules:

- The switch is immediate for the current platform after the user's explicit role sentence.
- The switch is not sticky across all future platforms; every executor must read `.agent/STATE.md`, `.agent/handoff/CURSOR_HANDOFF.md`, and this rules file before acting.
- If a requested action crosses role boundaries, the current platform must either stop and ask for a role switch or write a copyable instruction for the executor that should perform the other layer.
- No role may create `.cursor/` or `.workbuddy/` project knowledge directories. All durable coordination must be written under `.agent/`.
- Small deterministic consistency fixes inside the active role remain owned by the current executor and should be fixed directly.

## ADP Accumulation Semantics

ADP controls MVP in accumulation mode:

```text
ADP = one initial cleanup
    + for each module in .agent/adp-scope.json:
        MVPMCP.generate_products(accumulate=True, clean=False, scope_file_name="adp-scope.json")
        StoryboardMCP.prepare_storyboard_contract(accumulate=True)
        DesignMCP.prepare_design_contract(accumulate=True)
        StitchMCP.stitch_runtime(accumulate=True)
```

Ordinary single-module MVP keeps its original cleanup and scoped output behavior. ADP must not remove the previous module while progressing through later modules.
