# ShaderGUI Learning v1.0

> **AI 驱动的课程生成与学习平台** — 基于 `.agent/` 流水线自动生成交互式 ShaderGUI 编程课程

---

## 📖 项目简介

**ShaderGUI Learning** 是一个创新的教育技术项目，使用 **AI 驱动的课程生成流水线（MVP）** 自动生成结构化的编程学习课程。

本项目专注于 **Unity ShaderGUI 编程教学**，通过 AI 生成课程内容、交互式练习和可视化演示，帮助学习者掌握 ShaderGUI 的核心概念。

### 🎯 核心特性

- ✅ **AI 驱动内容生成**：通过 `.agent/flow_engine.py` 自动生成课程内容
- ✅ **交互式学习页面**：Vue 3 + Vite 驱动的 SPA，支持动画、代码高亮、音频讲解
- ✅ **模块化课程结构**：支持多模块、多课时，易于扩展
- ✅ **多平台 AI 协作规范**：通过 `.agent/` 作为唯一可信源，支持 Cursor、WorkBuddy 等 AI 平台协作
- ✅ **完整验证体系**：`verify_course.py` + `npm run build` 双重验证

---

## 🛠 技术栈

### 课程生成流水线（MVP）
- **Python 3.12+**
- **AI 平台接口**：v0.dev API
- **流水线引擎**：`.agent/flow_engine.py`
- **内容生成**：StoryboardMCP → DesignMCP → AudioMCP → StitchMCP

### 前端（CourseApp）
- **框架**：Vue 3（Composition API）
- **构建工具**：Vite 8
- **样式**：Tailwind CSS
- **路由**：Vue Router 4
- **状态管理**：Pinia（按需）

### 内容格式
- **课程数据**：JSON（`CourseApp/src/data/*.json`）
- **音频**：MP3（TTS 生成）
- **字幕**：JSON（SRT 格式转换）

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Gino-Y/ShaderGUI_Learning_v1.0.git
cd ShaderGUI_Learning_v1.0
```

### 2. 安装依赖

```bash
# Python 依赖（用于 MVP 流水线）
pip install -r requirements.txt  # TODO: 创建 requirements.txt

# Node.js 依赖（用于前端）
npm --prefix CourseApp install
```

### 3. 运行 MVP 生成课程

```bash
# 生成 Module_01 的课程内容
python .agent/flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5
```

**执行阶段：**
1. ✅ Prereq 检查（源材料、v0 API、清理旧产物）
2. ✅ Storyboard 生成（叙事故事板契约）
3. ✅ v0 Design（React 原型与设计规则）
4. ✅ Design 契约（完整性自检、视觉参考自检）
5. ✅ 音频生成（逐字稿 → TTS → MP3）
6. ✅ Stitch（音频、字幕、播放器运行时绑定）
7. ✅ Verify（课程内容验证）
8. ✅ Build（Vue SPA 构建）
9. ✅ Audit（npm audit）

### 4. 启动开发服务器

```bash
npm --prefix CourseApp run dev
```

访问 **http://localhost:5173/** 查看课程。

（如果端口被占用，Vite 会自动切换到 5174 或其他端口）

### 5. 构建生产版本

```bash
npm --prefix CourseApp run build
```

构建产物在 `CourseApp/dist/`。

---

## 📂 项目结构

```
ShaderGUI_Learning_v1.0/
├── .agent/                          # AI 流水线核心（唯一可信源）
│   ├── flow_engine.py               # MVP 流水线入口
│   ├── rules.md                    # AI 行为规则（强制）
│   ├── SKILL.md                    # Skill 定义
│   ├── memory/                     # AI 工作记忆
│   ├── mcp_servers/               # MCP 服务器（StoryboardMCP、DesignMCP 等）
│   ├── templates/                  # 课程模板
│   └── reports/                   # 验证报告、违规报告
│
├── CourseApp/                      # Vue 3 前端应用
│   ├── src/
│   │   ├── components/            # Vue 组件（SlideCanvas、 nodes/* 等）
│   │   ├── data/                 # 课程数据（JSON）
│   │   ├── router/               # Vue Router 配置
│   │   └── App.vue               # 根组件
│   ├── public/
│   │   ├── audio/                # 课程音频（MP3）
│   │   └── subtitles/            # 字幕文件（JSON）
│   └── package.json
│
├── CourseContent/                  # 课程源材料
│   └── Module_01/                # 模块 01 内容
│
├── docs/                          # 项目文档
│   ├── Skill_Chain_DAG.md        # Skill 链 DAG 定义
│   └── MVP_Execution_Contract.md # MVP 执行契约
│
├── scripts/                       # 验证和工具脚本
│   ├── verify_course.py          # 课程验证脚本
│   └── platform_violation_guard.py # 平台违规检测
│
├── .gitignore
└── README.md                     # 本文件
```

---

## 📋 Git 工作流规范

本项目遵循严格的 **Git 协作工作流规范**（详见 [`.agent/rules.md`](.agent/rules.md)）：

### ✅ Pull 拉取规则（必须强制执行）
- **首次克隆后**：`git pull origin main`
- **每天开始前**：`git pull origin main`
- **每个大阶段开始前**（P0/P1/P2/P3/P4）：`git pull origin main`

### ✅ 原子提交快照（开发中）
```bash
# 提交命名规范
git commit -m "feat: Module_01 - 完成 P0 阶段 Lottie 白名单集成"
git commit -m "fix: SlideCanvas - 修复音频播放器崩溃问题"
git commit -m "Snapshot: Pre-P1 - 创建 P1 阶段前快照"
```

### ✅ Push 推送规则（阶段完成时）
- **每个大阶段完成后**：`git push origin main`
- **每天工作结束时**：`git push origin main`

---

## 🧪 验证与测试

### 课程验证

```bash
# 运行完整验证
python scripts/verify_course.py
```

**验证内容：**
- ✅ `.agent/` 规则一致性
- ✅ 课程 JSON 格式正确性
- ✅ 音频文件完整性
- ✅ 路由配置正确性

### 前端构建验证

```bash
npm --prefix CourseApp run build
```

**构建成功标准：**
- ✅ 无 TypeScript 类型错误
- ✅ 无 ESLint 警告
- ✅ 构建产物生成成功

---

## 📄 核心文档

| 文档 | 说明 |
|------|------|
| [`.agent/rules.md`](.agent/rules.md) | **AI 行为规则（强制）** — 所有 AI 平台必须遵循 |
| [`docs/Skill_Chain_DAG.md`](docs/Skill_Chain_DAG.md) | Skill 链 DAG 定义 — 课程生成流程 |
| [`docs/MVP_Execution_Contract.md`](docs/MVP_Execution_Contract.md) | MVP 执行契约 — 流水线执行规范 |
| [`.agent/flow_engine.py`](.agent/flow_engine.py) | MVP 流水线入口 — 执行课程生成 |

---

## 🔧 常见问题

### Q1：MVP 执行失败怎么办？

**A：** 按照以下步骤排查：
1. 检查 Python 版本（需要 3.12+）
2. 验证 v0 API Key 是否有效（`.agent/mcp_servers/v0_mcp.py`）
3. 检查端口占用（5173/5174）
4. 查看 `.agent/reports/` 中的错误报告

### Q2：如何添加新的课程模块？

**A：** 按照以下步骤：
1. 在 `CourseContent/` 中创建新模块目录（如 `Module_02/`）
2. 更新 `.agent/mvp-scope.json`，添加新模块
3. 运行 MVP 生成：`python .agent/flow_engine.py --mode production --scope module --module Module_02 --basedir .`

### Q3：如何自定义课程样式？

**A：** 修改以下文件：
- `CourseApp/tailwind.config.js` — Tailwind 主题配置
- `CourseApp/src/components/SlideCanvas.vue` — 画布组件样式
- `.agent/templates/` — 课程模板

---

## 📜 许可证

**MIT License**（待确认）

---

## 👥 贡献者

- **Gino-Y**（项目创建者）
- **AI 协作平台**：Cursor、WorkBuddy

---

## 📞 联系方式

- **GitHub Issues**：[https://github.com/Gino-Y/ShaderGUI_Learning_v1.0/issues](https://github.com/Gino-Y/ShaderGUI_Learning_v1.0/issues)
- **Discussions**：[https://github.com/Gino-Y/ShaderGUI_Learning_v1.0/discussions](https://github.com/Gino-Y/ShaderGUI_Learning_v1.0/discussions)

---

## ✨ 致谢

- **v0.dev** — AI 原型生成平台
- **Vue 3** — 渐进式 JavaScript 框架
- **Vite** — 新一代前端构建工具
- **Tailwind CSS** — 实用优先的 CSS 框架

---

**最后更新：** 2026-05-04  
**版本：** v0.1.0 (Module_01 DEPLOY_READY)
