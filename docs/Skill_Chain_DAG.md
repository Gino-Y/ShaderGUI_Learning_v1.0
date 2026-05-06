# ShaderGUI_Learning_v1.0 Skill 链 DAG 设计

本文描述本工程从教学计划到 Vue 课程播放器的生产 DAG。DAG 的目标是让课程内容、分镜头、音频、字幕、设计契约、探索页、做题页和验证脚本形成可重复执行的闭环。

## 对齐约束（必读）

- [AGENT_SINGLE_SOURCE] `.agent` 是唯一可信源；Cursor/Codex/其它平台只能作为执行器，禁止使用 `.cursor`/`.workbuddy` 作为规则/资产来源。
- [MVP_EXECUTION_CONTRACT] 执行 MVP 必须遵循 `docs/MVP_Execution_Contract.md` 和 `.agent/mvp-execution-scope.json`；禁止清理 `.agent`、`node_modules` 等禁区。
- [NO_INTERNAL_GUIDANCE_UI] 前端学习页面不得展示内部生产指导：`shotInstruction`、`focusInstruction`、`implementationHint`、`learnerTakeaway`、`Now focusing` 一律禁止展示。
- [TOKEN_LEVEL_ANIMATION] 代码类页面动效必须细化到代码字段/token，例如 `ShaderGUI`、`OnGUI`、`CustomEditor`、`FindProperty`、`ShaderProperty`；不得退化为整卡片或整块代码动画。
- [COURSE_HOME_ALIGNMENT_GRID] 首页和模块入口必须使用统一单层菜单。
- [SYNC_RULES_DAG_VERIFY] 任何影响规则/DAG/验收标准的改动必须同步更新 `docs/Skill_Chain_DAG.md`、`.agent/rules.md`、`.agent/SKILL.md` 和 `scripts/verify_course.py`。
- [REVERIFY_BUILD_BROWSER] 需循环自检直至交付：`verify_course.py`、`npm run build` 和必要的浏览器验证。
- [COMPLETION_GATE_FILE_DRIVEN] 任务完成必须以仓库文件、handoff、memory 和验证结果为准。

## DAG 总览

```mermaid
flowchart TD
  A["教学计划 docs/ShaderGUI_Teaching_Plan.md"] --> B["CourseMCP: 源材料与规则检查"]
  B --> B2["V0MCP: API Key 验证"]
  B2 --> C0{"运行模式"}
  C0 -->|"MVP (--max-retries)"| C1["clear_stage_outputs(mvp)"]
  C0 -->|"ADP (--adp)"| C2["ADPMCP._clean_adp_products()"]
  C1 --> C["MVPMCP: 生成 CourseApp / scripts（scope 裁剪）"]
  C2 --> C3["ADPMCP: 全量扫描写入 CourseApp / scripts"]
  C --> D["StoryboardMCP: 分镜头契约"]
  C3 --> D
  D --> E["V0MCP: v0 React 原型与设计规则"]
  E --> F["DesignMCP: Vue 设计契约"]
  F --> G["VoiceMCP: MP3 与字幕事件"]
  G --> H["StitchMCP: 运行时绑定"]
  H --> I["Verify: 课程契约验证"]
  I --> J["Build: Vue SPA 构建"]
  J --> K["Audit: 依赖审计"]
  K --> L["DEPLOY_READY"]
```

## MVP 与 ADP 模式

| 维度 | MVP 模式 | ADP 模式 |
| :--- | :--- | :--- |
| 触发 | `--max-retries N` | `--adp` 标志 |
| 生成节点 | `MVPMCP` | `ADPMCP` |
| 清理策略 | `clear_stage_outputs("mvp")` 删除整个 CourseApp/（除 node_modules） | `ADPMCP._clean_adp_products()` 只清理 scope 允许的路径 |
| 写入策略 | 模板覆盖 + scope 裁剪 | **全量扫描**所有模块源文件，一次性写全量 `course.json` / `slides.json` / `quizzes.json` / `explorations.json` |
| 音频/字幕 | 清理后由 flow engine Dev 步骤生成 | **不清理**音频/字幕/逐字稿（增量资产），由 flow engine Dev 步骤生成 |
| scope 文件 | `.agent/mvp-scope.json` + `.agent/mvp-execution-scope.json` | `.agent/adp-scope.json` + `.agent/adp-execution-scope.json` |

### ADP 清理边界

`adp-execution-scope.json` 的 `clean.allow` **不包含** `CourseApp/public/audio/`、`subtitles/`、`transcripts/`。这些是跨模块增量资产，ADP 全量写入模式下不可清理。

### ADP 全量写入

`ADPMCP._write_course_app()` 不依赖跨运行合并：
1. `_copy_all_course_content()` — 复制所有模块逐字稿到 `CourseApp/public/transcripts/`
2. 扫描所有 `CourseContent/Module_*/` 目录
3. 一次性写全量 `course.json`（含所有模块）、`slides.json`（含所有 slide）、`quizzes.json`、`explorations.json`

## 2026-05-06 ADP Dispatcher Override

ADP is no longer a parallel full-writer node. `--adp` is now a dispatcher command:

```text
ADP = for each module declared in .agent/adp-scope.json:
        run the normal MVP pipeline for that module's complete module scope
```

This supersedes the older ADPMCP full-scan/full-write design. The reason is structural: `slides.json` was written as all-module data while `storyboard-contract.json`, `design-contract.json`, and `stitch-manifest.json` stayed current-module-only global files. That made the last module overwrite earlier module contracts. The stable boundary is now:

- `MVPMCP`: owns one complete module production run.
- `ADP command`: owns module scheduling only; it must not produce a second CourseApp writing model.
- The current platform assigned to the execution layer may execute MVP or ADP commands, but must read rules and handoff only from `.agent/`.

Current ADP command:

```powershell
python .agent\flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

Single-module full MVP command:

```powershell
python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
```

## MVP Scope

当前 MVP scope 由 `.agent/mvp-scope.json` 控制：

- 正式课时：`p00`、`p01`。
- 探索页：`p01` 的子页面 `/module/Module_01/slide/p01/explore`。
- 做题页：`/module/Module_01/quiz`。

探索页不是 `pXX`，不计入 `slideCount`，不得作为 `kind=interactive` slide 出现在 `slides.json`。

## 节点职责

| 节点 | 输入 | 输出 | 验收 |
| :--- | :--- | :--- | :--- |
| `CourseMCP` | docs、`.agent` 规则 | 源材料检查结果 | 必须确认 `.agent` 单一可信源 |
| `MVPMCP` | `CourseContent/<module>`、scope、templates | Vue SPA、数据、脚本 | 只生成 scope 内产物 |
| `ADPMCP` | `CourseContent/Module_*/`（全量扫描）、scope、templates | Vue SPA（全量数据）、脚本 | 全量写入所有模块数据 |
| `StoryboardMCP` | slides、subtitles、explorations、quizzes | `storyboard-contract.json` | motion cues 与交互屏完整 |
| `V0MCP` | storyboard | `.agent/v0/<module>/react-prototype.json` | v0 引用落到 `.agent/v0/` |
| `DesignMCP` | storyboard、v0 handoff | `design-contract.json` | 设计契约承接 storyboard 与 v0 |
| `VoiceMCP` | transcripts | MP3、subtitle JSON | 音频不是占位音 |
| `StitchMCP` | slides、audio、subtitles、storyboard、design | `stitch-manifest.json` | 课程页、探索页、做题页绑定完整 |
| `verify_course.py` | 全部产物 | 验证报告 | 失败即阻断 |
| `BuildMCP` | CourseApp | `dist/` | `npm run build` 通过 |
| `AuditMCP` | npm 依赖 | audit 结果 | 无 P0/P1 漏洞 |

## Skill Registry

方案技能库由 `.agent/skills/` 维护：

- `web-interactive-content-builder`：顶层总控 Skill。
- `skill-router`：根据内容特征选择或组合子 Skill。
- `interactive-article-skill`：长文交互解释。
- `explorable-mini-skill`：短篇可探索解释器。
- `parameter-playground-skill`：参数沙盒。
- `creative-workbench-skill`：任务工作台。
- `animated-lesson-skill`：动画课件。
- `chapter-lab-skill`：章节实验课程。

ShaderGUI 当前默认组合为 `chapter-lab-skill + explorable-mini-skill`。

## Interaction Necessity Gate

探索页必须先通过必要性闸门。只有满足以下条件时才允许插入：

- 静态讲解和做题页不足以达成学习目标。
- 存在可操纵的概念变量。
- 用户操作能产生即时反馈。
- 交互结果可以帮助迁移到真实 ShaderGUI 工程判断。
- 探索页不破坏主课程序列。

闸门产物应写入 `.agent/interactive-content/<module>/<slide>/explore/necessity-gate.json` 或同等 `.agent` 契约。

## 运行时契约

- `CoursePlayer.vue` 必须读取 `storyboard-contract.json` 并向 `SlideCanvas.vue` 传入 `activeCue`、`visualComposition`、`motionCues`。
- `SlideCanvas.vue` 必须按 cue 高亮知识点和代码 token。
- `SlideNav.vue` 必须提供播放、暂停、进度条、上一页、下一页、探索入口、模块入口。
- `ExploreView.vue` 必须作为父课时子路由。
- `QuizView.vue` 必须只展示当前题卡，完成后展示成绩页。

## UTF-8 Contract

所有文本产物必须是 UTF-8，包括：

- `.agent` 规则、Skill、MCP、memory、handoff、reports、templates。
- `CourseContent` 源数据与逐字稿。
- `CourseApp/src/data` 契约数据。
- `docs` 文档。
- `scripts` 脚本。

任何乱码、mojibake 或非 UTF-8 文本都是交付阻塞项。

## 平台违规闸门

`platform_violation_guard.py` 在 `flow_engine.py` 入口前扫描 `.cursor/` 和 `.workbuddy/`。发现平台私有 AI 资产时：

- DAG fail-fast。
- 报告写入 `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.md`。
- 机器报告写入 `.agent/reports/cleanup/LATEST_PLATFORM_VIOLATION.json`。
- 可执行 `python .agent/platform_violation_guard.py --basedir . --fix` 隔离违规文件。

## 验证闭环

最小验证：

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

触及前端体验时还必须验证：

- `/`
- `/module/Module_01/slide/p00`
- `/module/Module_01/slide/p01`
- `/module/Module_01/slide/p01/explore`
- `/module/Module_01/quiz`
- `/audio/Module_01/p00.mp3`
- `/audio/Module_01/p01.mp3`

## 反馈同步规则

每次用户反馈后必须判断是否影响 DAG。影响时同步更新：

- `docs/Skill_Chain_DAG.md`
- `.agent/rules.md`
- `.agent/SKILL.md`
- `scripts/verify_course.py`
- 相关 `.agent/mcp_servers/` 或 templates
- `.agent/memory/`
- `.agent/handoff/`

不影响 DAG 时也要记录判断理由。

## Small Fix Ownership

小而确定、低风险的一致性问题由当前执行方直接修复，不得要求用户手动处理。包括路径不一致、编码问题、handoff/memory/STATE 漏写、验证脚本漂移和明显笔误。

## ADP Accumulation Update

ADP dispatcher now accumulates module products instead of replacing prior module output. This supersedes earlier dispatcher notes that implied cleanup/generation happened independently inside every module run.

## Course Home Module Progress State

课程首页新增学习者本地状态层，不改变课程内容 DAG 的源数据契约：

```text
CourseContent/course metadata
  -> MVPMCP template assembly
  -> CourseHome.vue module cards
  -> localStorage learner progress state
```

- 状态集合为 `看过 -> 学过 -> 已做题 -> 掌握`。
- 后一级依赖前一级，运行时使用单一等级值表达阶梯进度，避免状态断裂。
- 状态是学习者本地交互数据，不进入 `CourseContent/`、`course.json`、`slides.json`、`storyboard-contract.json`、`design-contract.json` 或 `stitch-manifest.json`。
- 验收由 `scripts/verify_course.py` 检查模板和生成首页中的 `localStorage` key、四个状态标签和阶梯状态函数标记。

## ADP Storyboard Validation Update

ADP 累加模式下，StoryboardMCP 校验属于跨模块全局契约校验：

- 覆盖关系必须使用 `(moduleId, slideId)`，不能只看 `slideId`。
- `Module_01/p02` 不应在校验 `Module_03` 时被误判为当前模块的 extra slide。
- `severity: warning` 是诊断信息，不阻断 DAG；只有非 warning 错误阻断节点。
- ADP 校验还要确认累计 storyboard 覆盖当前生成的全部 slide，防止后续模块覆盖前序模块。

## ADP Design Validation Update

ADP 累加模式下，DesignMCP 校验同样属于跨模块全局契约校验：

- 覆盖关系必须使用 `(moduleId, slideId)`，不能只看 `slideId`。
- `Module_01/p02` 不应在校验 `Module_03` 时被误判为当前模块的 extra slide。
- `severity: warning` 是诊断信息，不阻断 DAG；只有非 warning 错误阻断节点。
- ADP 校验还要确认累计 design 契约覆盖当前生成的全部 slide，防止后续模块覆盖前序模块。

## Transcript Narration Quality Gate

逐字稿进入语音与字幕前必须经过叙述面清洗：

```text
CourseContent/Module_XX/doc/*.md
  -> generate_audio.py clean_text()
  -> subtitles JSON + TTS MP3
  -> verify_course.py narration-label gate
```

- 清洗必须移除元数据标题、二级结构标题、Markdown 表格和列表结构标签。
- `核心观点`、`问题：`、`思路：`、`金句：`、`结论：` 等文档编辑标签不得出现在生成字幕或语音朗读文本中。
- 此类问题不得通过手改 `CourseApp/public/audio` 或 `CourseApp/public/subtitles` 修复，必须改 `.agent/templates/scripts/generate_audio.py` 与验证门闸后重新生成。
