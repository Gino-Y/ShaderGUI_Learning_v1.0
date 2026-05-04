# ShaderGUI_Learning_v1.0 — 长期记忆

## 项目概述

**工程名**：ShaderGUI_Learning_v1.0  
**目标**：Unity ShaderGUI 专家成长体系，从工具使用者到工具定义者  
**核心理念**：ShaderGUI 是 Shader 的"交互契约"，不是 UI 装饰，是前端工程层  

---

## 四大教学模块

| 模块 | 课题 | 状态 |
| :--- | :--- | :--- |
| 模块一：解构 | 最小可行架构 + 属性契约 | ✅ 文档完成 |
| 模块二：重构 | 分组布局 + 条件显示 | ✅ 文档完成 |
| 模块三：进化 | 模块化复用 + Managed Properties | ✅ 文档完成 |
| 模块四：治理 | 渲染状态同步 + 版本迁移 | ✅ 文档完成 |
| 实战验收 | M_Outline_Fitting_h01 | 🔲 待开发 |

---

## 项目文件结构

```
D:\Works\Web\ShaderGUI_Learning_v1.0\
├── docs/
│   ├── ShaderGUI_Teaching_Plan.md
│   └── Skill_Chain_DAG.md
├── .agent/
│   ├── SKILL.md
│   ├── rules.md
│   └── memory/
│       ├── MEMORY.md
│       └── 2026-04-29.md
├── CourseApp/
├── CourseContent/
└── scripts/
```

AI 资产统一维护在 `.agent/` 下；禁止新增 `.workbuddy/`、`.cursor/` 等平台专属目录。

---

## 核心代码规范（已确立）

- **属性查找**：必须使用 `FindPropertySafe`，禁止强绑定 `FindProperty`
- **null 检查**：访问属性值前必须 guard
- **分组结构**：Shape → Clip → Motion → Color（角色描边材质标准）
- **模块化**：功能模块为独立静态类，签名：`DrawProperties(editor, props, managedProps)`
- **Managed Properties**：多模块协作时使用 HashSet 注册已绘制属性，防漏防重
- **渲染状态**：统一通过 `SyncRenderingStates` 自动同步，不暴露给美术手调

---

## 用户偏好（已观察）

- 中文交流，简洁直接
- 要求 AI 主动追问上下文后再生成代码
- 偏好完整的"❌ 反例 vs ✅ 正例"对比式代码示范
- 教学内容需要有"金句"（可记忆的工程原则）
- 拒绝半成品，要求一步到位交付可用内容

---

## 当前生成态补充（2026-04-29）

- Module_01 已扩展为 12 页：`p00` 到 `p11`。
- 旧 `stitch-ai-design.json` 已泛化为 `design-contract.json`。
- `DesignMCP` 是当前设计契约节点，负责生成 `CourseApp/src/data/design-contract.json` 与 `.agent/design/Module_01/design-brief.md`，并执行契约完整性与视觉参考双层循环自检。
- `CourseApp/`、`CourseContent/`、`scripts/`、音频、字幕、构建目录都属于可再生产物；`.agent/` 与 `docs/` 是当前保留的工作流与规则源。
- AI 资产只允许维护在 `.agent/`，`.workbuddy/`、`.cursor/` 等平台目录一律视为违规回流。

*最后更新：2026-04-29（归并 .workbuddy 记忆并清理平台目录）*
