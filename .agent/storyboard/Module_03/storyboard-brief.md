# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_03`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_03 / p00

- Route: `/module/Module_03/slide/p00`
- Title: OnGUI 是唯一的入口
- Purpose: Use this scene to make learners understand 'OnGUI 是唯一的入口' through the content beats: ShaderGUI 是材质面板的真正控制器 / OnGUI 每帧调用，负责绘制所有属性 / FindProperty 按名称取出属性引用.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (ShaderGUI 是材质面板的真正控制器); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: ShaderGUI 是材质面板的真正控制器
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“ShaderGUI 是材质面板的真正控制器”，弱化其他内容；旁白：ShaderGUI 是材质面板的真正控制器。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (OnGUI 每帧调用，负责绘制所有属性); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: OnGUI 每帧调用，负责绘制所有属性
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“OnGUI 每帧调用，负责绘制所有属性”，弱化其他内容；旁白：OnGUI 每帧调用，负责绘制所有属性。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (FindProperty 按名称取出属性引用); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: FindProperty 按名称取出属性引用
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“FindProperty 按名称取出属性引用”，弱化其他内容；旁白：FindProperty 按名称取出属性引用。

### Module_03 / p01

- Route: `/module/Module_03/slide/p01`
- Title: 参数分组与布局
- Purpose: Use this scene to make learners understand '参数分组与布局' through the content beats: editor.LabelField 绘制分组标题 / editor.ShaderProperty 绘制单个属性 / GUILayout.Space 控制间距.
- Layout: code structure and callout annotations
- Composition: medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway
- Frame grid: {'columns': 'left 48% teaching beats, right 52% code panel', 'rows': 'top title band, middle explanation/code body, bottom learner focus strip', 'anchor': 'code panel occupies the right visual weight; title anchors upper-left'}
- Palette: precise, technical, focused
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: code-callout-focus -> code-callout (editor.LabelField 绘制分组标题); focus `knowledge-01` with pulse-once-then-hold / code-highlight; target `code-callout`; source subtitle: editor.LabelField 绘制分组标题
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“editor.LabelField 绘制分组标题”，弱化其他内容；旁白：editor.LabelField 绘制分组标题。
  - `cue-02` 00:00.00-00:01.80 segment 1: code-callout-focus -> code-callout (editor.ShaderProperty 绘制单个属性); focus `knowledge-02` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: editor.ShaderProperty 绘制单个属性
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“editor.ShaderProperty 绘制单个属性”，弱化其他内容；旁白：editor.ShaderProperty 绘制单个属性。
  - `cue-03` 00:00.00-00:01.80 segment 2: code-callout-focus -> code-callout (GUILayout.Space 控制间距); focus `knowledge-03` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: GUILayout.Space 控制间距
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“GUILayout.Space 控制间距”，弱化其他内容；旁白：GUILayout.Space 控制间距。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_03/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
