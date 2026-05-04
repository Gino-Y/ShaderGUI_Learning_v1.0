# ShaderGUI 课程交互化改造路线图

## 决策

当前项目采用 Web 交互式内容 Skill 库方案：

```text
web-interactive-content-builder
→ skill-router
→ chapter-lab-skill
→ explorable-mini-skill
```

默认组合：

- `chapter-lab-skill` 管课程结构、章节实验、路由、进度、测验与数据契约。
- `explorable-mini-skill` 管每节课的小型交互实验。

## 目标

把当前以幻灯片、音频、字幕和测验为主的课程播放器，升级为“章节课程 + 小型交互实验”的学习系统。

交互实验不替代讲解内容，而是让学习者直接操作 ShaderGUI 的关键变量，观察 UI、属性契约、状态同步和代码结构之间的关系。

## 阶段路线

### P0：Skill 规范落地

产物：

- `.agent/skills/web-interactive-content-builder/SKILL.md`
- `.agent/skills/skill-router/SKILL.md`
- `.agent/skills/chapter-lab-skill/SKILL.md`
- `.agent/skills/explorable-mini-skill/SKILL.md`

通过标准：

- 总 Skill 能说明何时调用子 Skill。
- `skill-router` 能根据场景选择方案。
- `chapter-lab-skill` 能约束课程数据结构。
- `explorable-mini-skill` 能约束单节实验结构。

### P1：交互内容契约

新增目录：

```text
.agent/interactive-content/
└── Module_01/
    ├── chapter-plan.md
    ├── chapter-contract.json
    └── p01/
        └── explore/
        ├── interaction-brief.md
        ├── concept-model.json
        ├── storyboard.json
        ├── component-spec.md
        └── validation-report.md
```

建议先为 `Module_01 / p01` 增加一个子探索页：

```text
Module_01 / p01 / explore
主题：属性分组如何降低调参负担
Skill：explorable-mini-skill
目标：让学习者切换功能开关，观察 ShaderGUI 分组、可见属性和代码片段如何联动。
```

### P2：CourseApp 数据接入

建议在父 slide 上扩展 `explore` 字段：

```json
{
  "slideId": "p01",
  "explore": {
    "route": "/module/Module_01/slide/p01/explore",
    "skill": "explorable-mini-skill",
    "component": "PropertyGroupingLab",
    "contract": ".agent/interactive-content/Module_01/p01/explore/concept-model.json"
  }
}
```

接入点：

- `CourseApp/src/data/slides.json`
- `CourseApp/src/views/SlideView.vue`
- `CourseApp/src/components/SlideCanvas.vue`
- `CourseApp/src/components/labs/`

通过标准：

- 普通幻灯片仍按现有逻辑渲染。
- `kind: "interactive"` 的页面能加载实验组件。
- 实验组件可重置，有默认状态，有即时反馈。

### P3：第一个小实验

建议组件：

```text
CourseApp/src/components/labs/PropertyGroupingLab.vue
```

实验变量：

- 是否启用描边。
- 是否启用溶解。
- 描边宽度。
- 当前材质使用场景。

联动反馈：

- 左侧：模拟材质面板分组。
- 中间：当前可见属性列表。
- 右侧：对应 ShaderGUI 代码片段高亮。
- 底部：一句解释当前状态为什么更易用或更危险。

通过标准：

- 任意控件变化都能立即改变至少一个反馈区域。
- 默认状态可以说明“分组降低认知负担”。
- 错误或危险状态有解释，而不是静默失败。

### P4：验证脚本扩展

建议扩展 `scripts/verify_course.py`：

- 检查 `kind: "interactive"` 时必须存在 `interactive.skill`、`interactive.component`、`interactive.contract`。
- 检查引用的交互契约文件存在。
- 检查实验组件文件存在。
- 检查 `slideCount` 与模块幻灯片数量一致。

通过标准：

```text
python scripts/verify_course.py
```

输出 `[OK] course verification passed`。

## 后续扩展

当单节实验变复杂时，再引入其他子 Skill：

- 多参数组合、训练或运行过程：`parameter-playground-skill`
- 用户需要制作和导出结果：`creative-workbench-skill`
- 依赖连续动画理解：`animated-lesson-skill`
- 深度技术长文：`interactive-article-skill`

当前阶段不需要提前实现这些子 Skill，只保留路由入口。
