# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_04`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_04 / p00

- Route: `/module/Module_04/slide/p00`
- Title: 条件显示与高级布局
- Purpose: Use this scene to make learners understand '条件显示与高级布局' through the content beats: 根据属性值条件显示/隐藏其他属性 / 使用 EditorGUILayout 实现复杂布局 / 处理动画属性的时间轴绑定.
- Layout: code structure and callout annotations
- Composition: medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway
- Frame grid: {'columns': 'left 48% teaching beats, right 52% code panel', 'rows': 'top title band, middle explanation/code body, bottom learner focus strip', 'anchor': 'code panel occupies the right visual weight; title anchors upper-left'}
- Palette: precise, technical, focused
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: code-callout-focus -> code-callout (根据属性值条件显示/隐藏其他属性); focus `knowledge-01` with pulse-once-then-hold / code-highlight; target `code-callout`; source subtitle: 根据属性值条件显示/隐藏其他属性
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“根据属性值条件显示/隐藏其他属性”，弱化其他内容；旁白：根据属性值条件显示/隐藏其他属性。
  - `cue-02` 00:00.00-00:01.80 segment 1: code-callout-focus -> code-callout (使用 EditorGUILayout 实现复杂布局); focus `knowledge-02` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: 使用 EditorGUILayout 实现复杂布局
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“使用 EditorGUILayout 实现复杂布局”，弱化其他内容；旁白：使用 EditorGUILayout 实现复杂布局。
  - `cue-03` 00:00.00-00:01.80 segment 2: code-callout-focus -> code-callout (处理动画属性的时间轴绑定); focus `knowledge-03` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: 处理动画属性的时间轴绑定
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“处理动画属性的时间轴绑定”，弱化其他内容；旁白：处理动画属性的时间轴绑定。

### Module_04 / p01

- Route: `/module/Module_04/slide/p01`
- Title: 实战踩坑与性能优化
- Purpose: Use this scene to make learners understand '实战踩坑与性能优化' through the content beats: 避免在 OnGUI 中做耗时操作 / 材质属性变更触发重新序列化 / 使用 MaterialEditor.RegisterPropertyChangeUndo 支持撤销.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (避免在 OnGUI 中做耗时操作); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 避免在 OnGUI 中做耗时操作
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“避免在 OnGUI 中做耗时操作”，弱化其他内容；旁白：避免在 OnGUI 中做耗时操作。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (材质属性变更触发重新序列化); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 材质属性变更触发重新序列化
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“材质属性变更触发重新序列化”，弱化其他内容；旁白：材质属性变更触发重新序列化。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (使用 MaterialEditor.RegisterPropertyChangeUndo 支持撤销); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 使用 MaterialEditor.RegisterPropertyChangeUndo 支持撤销
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“使用 MaterialEditor.RegisterPropertyChangeUndo 支持撤销”，弱化其他内容；旁白：使用 MaterialEditor.RegisterPropertyChangeUndo 支持撤销。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_04/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
