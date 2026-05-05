# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_02`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_02 / p00

- Route: `/module/Module_02/slide/p00`
- Title: Drawer 是什么
- Purpose: Use this scene to make learners understand 'Drawer 是什么' through the content beats: Drawer 控制材质属性在面板中的渲染方式 / 内置 Drawer：Toggle、Enum、PowerSlider / 自定义 Drawer 继承 MaterialPropertyDrawer.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (Drawer 控制材质属性在面板中的渲染方式); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: Drawer 控制材质属性在面板中的渲染方式
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Drawer 控制材质属性在面板中的渲染方式”，弱化其他内容；旁白：Drawer 控制材质属性在面板中的渲染方式。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (内置 Drawer：Toggle、Enum、PowerSlider); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 内置 Drawer：Toggle、Enum、PowerSlider
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“内置 Drawer：Toggle、Enum、PowerSlider”，弱化其他内容；旁白：内置 Drawer：Toggle、Enum、PowerSlider。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (自定义 Drawer 继承 MaterialPropertyDrawer); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 自定义 Drawer 继承 MaterialPropertyDrawer
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“自定义 Drawer 继承 MaterialPropertyDrawer”，弱化其他内容；旁白：自定义 Drawer 继承 MaterialPropertyDrawer。

### Module_02 / p01

- Route: `/module/Module_02/slide/p01`
- Title: 内置 Drawer 实战
- Purpose: Use this scene to make learners understand '内置 Drawer 实战' through the content beats: [Toggle] 控制布尔属性 / [Enum] 控制下拉选择 / [PowerSlider] 非线性滑块.
- Layout: code structure and callout annotations
- Composition: medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway
- Frame grid: {'columns': 'left 48% teaching beats, right 52% code panel', 'rows': 'top title band, middle explanation/code body, bottom learner focus strip', 'anchor': 'code panel occupies the right visual weight; title anchors upper-left'}
- Palette: precise, technical, focused
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: code-callout-focus -> code-callout ([Toggle] 控制布尔属性); focus `knowledge-01` with pulse-once-then-hold / code-highlight; target `code-callout`; source subtitle: [Toggle] 控制布尔属性
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“[Toggle] 控制布尔属性”，弱化其他内容；旁白：[Toggle] 控制布尔属性。
  - `cue-02` 00:00.00-00:01.80 segment 1: code-callout-focus -> code-callout ([Enum] 控制下拉选择); focus `knowledge-02` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: [Enum] 控制下拉选择
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“[Enum] 控制下拉选择”，弱化其他内容；旁白：[Enum] 控制下拉选择。
  - `cue-03` 00:00.00-00:01.80 segment 2: code-callout-focus -> code-callout ([PowerSlider] 非线性滑块); focus `knowledge-03` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: [PowerSlider] 非线性滑块
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“[PowerSlider] 非线性滑块”，弱化其他内容；旁白：[PowerSlider] 非线性滑块。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_02/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
