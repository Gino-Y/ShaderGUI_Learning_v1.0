# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_01`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不仅仅是换个皮
- Purpose: Use this scene to make learners understand 'ShaderGUI：不仅仅是换个皮' through the content beats: ShaderGUI 是 Shader 参数系统的前端工程层 / 不是简单的 UI 美化.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:09.56 segment 0: reveal-focus -> content-beat (ShaderGUI 是 Shader 参数系统的前端工程层); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 当我们谈论 ShaderGUI 时，先不要把它理解成给 Inspector 换一层皮。
    - Shot: 0.00s-9.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“ShaderGUI 是 Shader 参数系统的前端工程层”，弱化其他内容；旁白：当我们谈论 ShaderGUI 时，先不要把它理解成给 Inspector 换一层皮。
  - `cue-02` 00:09.56-00:15.56 segment 1: reveal-focus -> content-beat (不是简单的 UI 美化); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 更准确地说，它是 Shader 参数系统的前端工程层。
    - Shot: 9.56s-15.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“不是简单的 UI 美化”，弱化其他内容；旁白：更准确地说，它是 Shader 参数系统的前端工程层。

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 编写第一个自定义材质面板
- Purpose: Use this scene to make learners understand '编写第一个自定义材质面板' through the content beats: 继承 ShaderGUI / 重写 OnGUI / 通过 CustomEditor 绑定.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:05.56 segment 0: reveal-focus -> content-beat (继承 ShaderGUI); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 自定义 ShaderGUI 的最小架构其实很直接。
    - Shot: 0.00s-5.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“继承 ShaderGUI”，弱化其他内容；旁白：自定义 ShaderGUI 的最小架构其实很直接。
  - `cue-02` 00:05.56-00:14.67 segment 1: reveal-focus -> content-beat (重写 OnGUI); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: C Sharp 侧创建一个类，继承 ShaderGUI，并重写 OnGUI 方法。
    - Shot: 5.56s-14.67s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“重写 OnGUI”，弱化其他内容；旁白：C Sharp 侧创建一个类，继承 ShaderGUI，并重写 OnGUI 方法。
  - `cue-03` 00:14.67-00:22.22 segment 2: reveal-focus -> content-beat (通过 CustomEditor 绑定); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: Shader 侧在文件底部用 CustomEditor 绑定这个类。
    - Shot: 14.67s-22.22s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“通过 CustomEditor 绑定”，弱化其他内容；旁白：Shader 侧在文件底部用 CustomEditor 绑定这个类。

### Module_01 / p02

- Route: `/module/Module_01/slide/p02`
- Title: 如何安全地获取参数？
- Purpose: Use this scene to make learners understand '如何安全地获取参数？' through the content beats: Required 模式的风险 / Safe 模式的安全获取 / 封装 FindPropertySafe 工具函数.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:04.89 segment 0: reveal-focus -> content-beat (Required 模式的风险); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 在实际工程中，我们推荐使用 Safe 模式。
    - Shot: 0.00s-4.89s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Required 模式的风险”，弱化其他内容；旁白：在实际工程中，我们推荐使用 Safe 模式。
  - `cue-02` 00:04.89-00:06.09 segment 1: reveal-focus -> content-beat (Safe 模式的安全获取); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 为什么？
    - Shot: 4.89s-6.09s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Safe 模式的安全获取”，弱化其他内容；旁白：为什么。
  - `cue-03` 00:06.09-00:09.20 segment 2: reveal-focus -> content-beat (封装 FindPropertySafe 工具函数); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 因为 Shader 会迭代。
    - Shot: 6.09s-9.20s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“封装 FindPropertySafe 工具函数”，弱化其他内容；旁白：因为 Shader 会迭代。

## Interactive Screens

### explore-p01-property-grouping - 探索页

- Route: `/module/Module_01/slide/p01/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### explore-p02-property-grouping - 属性查找实战

- Route: `/module/Module_01/slide/p02/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_01/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
