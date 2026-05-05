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
  - `cue-01` 00:00.00-00:16.67 segment 0: reveal-focus -> content-beat (模块化思维); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 像搭积木一样构建材质面板 —— 逐字稿 你有没有遇到过这种情况：一个 ShaderGUI 脚本写了上千行，所有属性的绘制逻辑全都堆在 OnGUI 里。
    - Shot: 0.00s-16.67s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“模块化思维”，弱化其他内容；旁白：像搭积木一样构建材质面板 —— 逐字稿 你有没有遇到过这种情况：一个 ShaderGUI 脚本写了上千行，所有属性的绘制逻辑全都堆在 OnGUI 里。
  - `cue-02` 00:16.67-00:20.22 segment 1: reveal-focus -> content-beat (静态功能类设计); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 改一个地方，整块面板都要跟着改。
    - Shot: 16.67s-20.22s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静态功能类设计”，弱化其他内容；旁白：改一个地方，整块面板都要跟着改。
  - `cue-03` 00:20.22-00:27.33 segment 2: reveal-focus -> content-beat (DrawProperties 静态方法); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 后期维护的时候，光是找到某段绘制代码藏在哪一行，就要花半天时间。
    - Shot: 20.22s-27.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“DrawProperties 静态方法”，弱化其他内容；旁白：后期维护的时候，光是找到某段绘制代码藏在哪一行，就要花半天时间。

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
  - `cue-01` 00:00.00-00:13.56 segment 0: reveal-focus -> content-beat (注册机制与自动补位); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: Managed Properties：面板的行政管理 —— 逐字稿 在前面两节课里，我们学会了如何查找属性、如何绘制控件。
    - Shot: 0.00s-13.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“注册机制与自动补位”，弱化其他内容；旁白：Managed Properties：面板的行政管理 —— 逐字稿 在前面两节课里，我们学会了如何查找属性、如何绘制控件。
  - `cue-02` 00:13.56-00:28.44 segment 1: reveal-focus -> content-beat (确保不漏掉参数); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 但当一个 ShaderGUI 代码变得越来越长，你有没有遇到过这种情况：某个属性明明在 Shader 里定义了，但面板里就是没画出来？
    - Shot: 13.56s-28.44s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“确保不漏掉参数”，弱化其他内容；旁白：但当一个 ShaderGUI 代码变得越来越长，你有没有遇到过这种情况：某个属性明明在 Shader 里定义了，但面板里就是没画出来。
  - `cue-03` 00:28.44-00:32.00 segment 2: reveal-focus -> content-beat (不重复绘制); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 或者更糟，同一个属性被画了两次？
    - Shot: 28.44s-32.00s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“不重复绘制”，弱化其他内容；旁白：或者更糟，同一个属性被画了两次。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_03/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
