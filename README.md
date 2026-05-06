# ShaderGUI Learning v1.0

> **AI 驱动的课程生成与学习平台** — 基于 `.agent/` 流水线自动生成交互式 ShaderGUI 编程课程

> **在线访问：** [https://gino-y.github.io/ShaderGUI_Learning_v1.0/](https://gino-y.github.io/ShaderGUI_Learning_v1.0/)

---

## 项目简介

**ShaderGUI Learning** 使用 **AI 驱动的课程生成流水线** 自动生成结构化的编程学习课程，专注于 **Unity ShaderGUI 编程教学**。

### 核心特性

- **AI 流水线生成**：Prereq → Storyboard → v0 Design → Design Contract → Audio → Stitch → Verify → Build，全自动
- **ADP 全量调度**：`--adp` 模式一次执行全部模块，渐进式累加产物（不丢失前序模块）
- **交互式学习**：Vue 3 SPA，支持音频讲解、代码高亮、动效、做题页、探索实验室
- **双模式生成**：单模块 MVP（clean-first）+ 全量 ADP（accumulate），互不干扰
- **多 AI 平台协作**：`.agent/` 为唯一可信源，Cursor、WorkBuddy 等平台均作为执行器
- **完整验证链**：`verify_course.py` + `npm run build` + 浏览器验证

---

## 当前状态

| 模块 | 状态 | 内容 |
|------|------|------|
| Module_01 | DEPLOY_READY | OnGUI 基础、属性查找、手写 ShaderGUI |
| Module_02 | DEPLOY_READY | Managed Properties、智能 UI 联动、封装工具类 |
| Module_03 | DEPLOY_READY | 自定义 Inspector、模块化组装 |
| Module_04 | DEPLOY_READY | 渲染状态调试、透明/镂空/叠加光效 |

全部 4 模块已完成 ADP dispatcher 全量执行，`verify_course.py` 通过，`npm run build` 通过。

---

## 技术栈

### 课程生成流水线

- **Python 3.12+**
- **流水线引擎**：`.agent/flow_engine.py`
- **MCP 节点**：PrereqMCP → StoryboardMCP → V0MCP → DesignMCP → VoiceMCP → StitchMCP
- **AI 接口**：v0.dev API（React 原型 + 设计规则）

### 前端（CourseApp）

- **框架**：Vue 3（Composition API）
- **构建**：Vite 8
- **样式**：Tailwind CSS
- **路由**：Vue Router 4

### 内容格式

- **课程数据**：JSON（`course.json`、`slides.json`、`storyboard-contract.json`、`design-contract.json`、`stitch-manifest.json`）
- **音频**：MP3（TTS 生成）
- **字幕**：JSON

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Gino-Y/ShaderGUI_Learning_v1.0.git
cd ShaderGUI_Learning_v1.0
```

### 2. 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# Node.js 依赖
npm --prefix CourseApp install
```

### 3. 生成课程

**单模块 MVP**（clean-first，生成单个模块）：

```bash
python .agent/flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
```

**全量 ADP**（accumulate，一次生成全部模块）：

```bash
python .agent/flow_engine.py --mode production --scope all-content --basedir . --max-retries 5 --adp
```

**流水线阶段**：Prereq → Storyboard → v0 Design → Design Contract → Audio → Stitch → Verify → Build → Audit

### 4. 启动开发服务器

```bash
npm --prefix CourseApp run dev
```

访问 **http://localhost:5173/**

### 5. 构建生产版本

```bash
npm --prefix CourseApp run build
```

构建产物在 `CourseApp/dist/`。

---

## 项目结构

```
ShaderGUI_Learning_v1.0/
├── .agent/                              # AI 流水线核心（唯一可信源）
│   ├── flow_engine.py                   #   流水线入口（MVP + ADP）
│   ├── rules.md                         #   AI 行为规则（强制）
│   ├── SKILL.md                         #   Skill 定义
│   ├── STATE.md                         #   项目状态
│   ├── adp-scope.json                   #   ADP 模块范围
│   ├── mvp-scope.json                   #   MVP 模块范围
│   ├── adp-execution-scope.json         #   ADP 清理范围
│   ├── mcp_servers/                     #   MCP 服务器
│   │   ├── mvp_mcp.py                   #     MVP 生成（单模块）
│   │   ├── adp_mcp.py                   #     ADP 调度（全量）
│   │   ├── storyboard_mcp.py            #     故事板契约
│   │   ├── design_mcp.py                #     设计契约
│   │   ├── v0_mcp.py                    #     v0 原型生成
│   │   ├── voice_mcp.py                 #     音频生成
│   │   └── stitch_mcp.py                #     运行时缝合
│   ├── templates/                       #   课程模板（源头发）
│   │   ├── course-app/                  #     CourseApp 模板
│   │   └── scripts/                     #     生成脚本模板
│   ├── handoff/                         #   平台交接文档
│   ├── memory/                          #   AI 工作记忆
│   ├── design/                          #   模块设计简报
│   ├── storyboard/                      #   模块故事板简报
│   └── reports/                         #   验证/违规报告
│
├── CourseApp/                           # Vue 3 前端应用（产物）
│   ├── src/
│   │   ├── components/                  #   Vue 组件
│   │   │   └── labs/                    #     探索实验室组件
│   │   │       ├── PropertyGroupingLab.vue
│   │   │       ├── SmartUILinkageLab.vue
│   │   │       ├── ModularAssemblyLab.vue
│   │   │       └── RenderStatePlayground.vue
│   │   ├── data/                        #   课程数据（JSON）
│   │   ├── views/                       #   页面视图
│   │   └── router/                      #   路由配置
│   └── public/
│       ├── audio/                       #   模块音频（MP3）
│       ├── subtitles/                   #   字幕文件（JSON）
│       └── transcripts/                 #   逐字稿（Markdown）
│
├── CourseContent/                       # 课程源材料
│   ├── Module_01/                       #   Module_01：OnGUI 基础
│   ├── Module_02/                       #   Module_02：Managed Properties
│   ├── Module_03/                       #   Module_03：自定义 Inspector
│   └── Module_04/                       #   Module_04：渲染状态调试
│
├── docs/                                # 项目文档
│   ├── Skill_Chain_DAG.md               #   Skill 链 DAG 定义
│   ├── MVP_Execution_Contract.md        #   MVP 执行契约
│   ├── ADP_Execution_Contract.md        #   ADP 执行契约
│   ├── Data_Artifact_Boundary.md        #   数据/产物边界定义
│   └── ShaderGUI_Teaching_Plan.md       #   ShaderGUI 教学计划
│
├── scripts/                             # 验证和工具脚本
│   ├── verify_course.py                 #   课程验证
│   └── generate_audio.py                #   音频生成
│
└── README.md
```

---

## 验证

```bash
# 课程内容验证
python scripts/verify_course.py

# 前端构建验证
npm --prefix CourseApp run build

# 浏览器验证（启动服务后访问）
npm --prefix CourseApp run dev
# → http://localhost:5173/
```

---

## 核心文档

| 文档 | 说明 |
|------|------|
| [`.agent/rules.md`](.agent/rules.md) | AI 行为规则（强制） |
| [`.agent/STATE.md`](.agent/STATE.md) | 项目当前状态 |
| [`docs/Skill_Chain_DAG.md`](docs/Skill_Chain_DAG.md) | Skill 链 DAG 定义 |
| [`docs/MVP_Execution_Contract.md`](docs/MVP_Execution_Contract.md) | MVP 执行契约 |
| [`docs/ADP_Execution_Contract.md`](docs/ADP_Execution_Contract.md) | ADP 执行契约 |

---

## 许可证

MIT License

---

## 贡献者

- **Gino-Y** — 项目创建者
- **AI 协作平台** — Cursor、WorkBuddy

---

**最后更新：** 2026-05-06
**版本：** v1.0.0（全部 4 模块 DEPLOY_READY）
