# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_03`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_03 / p00

- Route: `/module/Module_03/slide/p00`
- Title: 像搭积木一样构建材质面板
- Purpose: Use this scene to make learners understand '像搭积木一样构建材质面板' through the content beats: 模块化思维 / 静态功能类设计 / DrawProperties 静态方法.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (模块化思维); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 模块化思维
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“模块化思维”，弱化其他内容；旁白：模块化思维。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (静态功能类设计); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 静态功能类设计
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静态功能类设计”，弱化其他内容；旁白：静态功能类设计。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (DrawProperties 静态方法); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: DrawProperties 静态方法
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“DrawProperties 静态方法”，弱化其他内容；旁白：DrawProperties 静态方法。

### Module_03 / p01

- Route: `/module/Module_03/slide/p01`
- Title: Managed Properties：面板的行政管理
- Purpose: Use this scene to make learners understand 'Managed Properties：面板的行政管理' through the content beats: 注册机制与自动补位 / 确保不漏掉参数 / 不重复绘制.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (注册机制与自动补位); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 注册机制与自动补位
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“注册机制与自动补位”，弱化其他内容；旁白：注册机制与自动补位。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (确保不漏掉参数); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 确保不漏掉参数
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“确保不漏掉参数”，弱化其他内容；旁白：确保不漏掉参数。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (不重复绘制); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 不重复绘制
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“不重复绘制”，弱化其他内容；旁白：不重复绘制。

## Interactive Screens

### explore-p00-modular-assembly - 模块化组装实验

- Route: `/module/Module_03/slide/p00/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_03/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
