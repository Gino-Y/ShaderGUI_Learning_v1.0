# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_01`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不只是换一层皮
- Purpose: Use this scene to make learners understand 'ShaderGUI：不只是换一层皮' through the content beats: ShaderGUI 是 Shader 参数系统的前端工程层 / 核心目标是降低美术调参时的认知负担 / 职责是组织参数、解释含义、同步状态.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (ShaderGUI 是 Shader 参数系统的前端工程层); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: ShaderGUI 是 Shader 参数系统的前端工程层
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“ShaderGUI 是 Shader 参数系统的前端工程层”，弱化其他内容；旁白：ShaderGUI 是 Shader 参数系统的前端工程层。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (核心目标是降低美术调参时的认知负担); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 核心目标是降低美术调参时的认知负担
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“核心目标是降低美术调参时的认知负担”，弱化其他内容；旁白：核心目标是降低美术调参时的认知负担。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (职责是组织参数、解释含义、同步状态); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 职责是组织参数、解释含义、同步状态
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“职责是组织参数、解释含义、同步状态”，弱化其他内容；旁白：职责是组织参数、解释含义、同步状态。

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 最小可行架构
- Purpose: Use this scene to make learners understand '最小可行架构' through the content beats: C Sharp 侧继承 ShaderGUI 并重写 OnGUI / Shader 侧通过 CustomEditor 绑定自定义面板 / 所有高级面板能力都从控制 OnGUI 开始.
- Layout: code structure and callout annotations
- Composition: medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway
- Frame grid: {'columns': 'left 48% teaching beats, right 52% code panel', 'rows': 'top title band, middle explanation/code body, bottom learner focus strip', 'anchor': 'code panel occupies the right visual weight; title anchors upper-left'}
- Palette: precise, technical, focused
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: code-callout-focus -> code-callout (C Sharp 侧继承 ShaderGUI 并重写 OnGUI); focus `knowledge-01` with pulse-once-then-hold / code-highlight; target `code-callout`; source subtitle: C Sharp 侧继承 ShaderGUI 并重写 OnGUI
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“C Sharp 侧继承 ShaderGUI 并重写 OnGUI”，弱化其他内容；旁白：C Sharp 侧继承 ShaderGUI 并重写 OnGUI。
  - `cue-02` 00:00.00-00:01.80 segment 1: code-callout-focus -> code-callout (Shader 侧通过 CustomEditor 绑定自定义面板); focus `knowledge-02` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: Shader 侧通过 CustomEditor 绑定自定义面板
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“Shader 侧通过 CustomEditor 绑定自定义面板”，弱化其他内容；旁白：Shader 侧通过 CustomEditor 绑定自定义面板。
  - `cue-03` 00:00.00-00:01.80 segment 2: code-callout-focus -> code-callout (所有高级面板能力都从控制 OnGUI 开始); focus `knowledge-03` with soft-blink-then-hold / code-highlight; target `code-callout`; source subtitle: 所有高级面板能力都从控制 OnGUI 开始
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将代码标注区域切到当前焦点“所有高级面板能力都从控制 OnGUI 开始”，弱化其他内容；旁白：所有高级面板能力都从控制 OnGUI 开始。

## Interactive Screens

### explore-p01-property-grouping - 探索页

- Route: `/module/Module_01/slide/p01/explore`
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
