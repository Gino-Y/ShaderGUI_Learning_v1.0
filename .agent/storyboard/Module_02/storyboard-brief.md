# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_02`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_02 / p00

- Route: `/module/Module_02/slide/p00`
- Title: 告别参数地狱：逻辑化的分组设计
- Purpose: Use this scene to make learners understand '告别参数地狱：逻辑化的分组设计' through the content beats: 信息架构设计 / BeginVertical 创建视觉边界 / 按渲染逻辑排列参数.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:11.78 segment 0: reveal-focus -> content-beat (信息架构设计); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 告别参数地狱：逻辑化的分组设计 —— 逐字稿 参数多是 ShaderGUI 的常态，但"多"不等于"乱"。
    - Shot: 0.00s-11.78s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“信息架构设计”，弱化其他内容；旁白：告别参数地狱：逻辑化的分组设计 —— 逐字稿 参数多是 ShaderGUI 的常态，但"多"不等于"乱"。
  - `cue-02` 00:11.78-00:17.33 segment 1: reveal-focus -> content-beat (BeginVertical 创建视觉边界); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 本节课教你用信息架构思维，把一堆属性变成有序面板。
    - Shot: 11.78s-17.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“BeginVertical 创建视觉边界”，弱化其他内容；旁白：本节课教你用信息架构思维，把一堆属性变成有序面板。
  - `cue-03` 00:17.33-00:45.33 segment 2: reveal-focus -> content-beat (按渲染逻辑排列参数); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 核心观点 问题：Shader 属性多了，默认面板是一维长列表，美术不知道什么是什么 思路：按渲染逻辑分组，用 UI 边界（Vertical/Horizontal）建立视觉层次 金句："好的 GUI 不是把参数都摆出来，而是让美术知道先填什么、后填什么。
    - Shot: 17.33s-45.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“按渲染逻辑排列参数”，弱化其他内容；旁白：核心观点 问题：Shader 属性多了，默认面板是一维长列表，美术不知道什么是什么 思路：按渲染逻辑分组，用 UI 边界（Vertical/Horizontal）建立视觉层次 金句："好的 GUI 不是把参数都摆出来，而是让美术知道先填什么、后填什么。

### Module_02 / p01

- Route: `/module/Module_02/slide/p01`
- Title: 只给用户他需要的：智能 UI 联动
- Purpose: Use this scene to make learners understand '只给用户他需要的：智能 UI 联动' through the content beats: 条件显示技术 / Toggle/Enum 控制参数组显隐 / EditorGUI.DisabledScope 应用.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:13.56 segment 0: reveal-focus -> content-beat (条件显示技术); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 只给用户他需要的：智能 UI 联动 —— 逐字稿 好的面板不是"能改所有参数"，而是"在当前配置下，只展示有意义的参数"。
    - Shot: 0.00s-13.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“条件显示技术”，弱化其他内容；旁白：只给用户他需要的：智能 UI 联动 —— 逐字稿 好的面板不是"能改所有参数"，而是"在当前配置下，只展示有意义的参数"。
  - `cue-02` 00:13.56-00:16.67 segment 1: reveal-focus -> content-beat (Toggle/Enum 控制参数组显隐); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 条件显示是专业感的核心来源。
    - Shot: 13.56s-16.67s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“Toggle/Enum 控制参数组显隐”，弱化其他内容；旁白：条件显示是专业感的核心来源。
  - `cue-03` 00:16.67-00:34.22 segment 2: reveal-focus -> content-beat (EditorGUI.DisabledScope 应用); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 核心观点 问题：枚举切换后，某些参数对当前配置无意义，但还显示着，干扰判断 思路：监听关键属性（Toggle/Enum），用 EditorGUILayout.
    - Shot: 16.67s-34.22s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“EditorGUI.DisabledScope 应用”，弱化其他内容；旁白：核心观点 问题：枚举切换后，某些参数对当前配置无意义，但还显示着，干扰判断 思路：监听关键属性（Toggle/Enum），用 EditorGUILayout。

### Module_02 / p02

- Route: `/module/Module_02/slide/p02`
- Title: 拒绝代码重复：打造 ShaderGUI 工具箱
- Purpose: Use this scene to make learners understand '拒绝代码重复：打造 ShaderGUI 工具箱' through the content beats: 封装 DrawProp / DrawTex / BeginGroup 工具类 / 提高编写效率 / 视觉统一性.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:16.89 segment 0: reveal-focus -> content-beat (封装 DrawProp / DrawTex / BeginGroup 工具类); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 阶段6：封装工具类（Refactoring Utility）—— 逐字稿 如果我们每个 ShaderGUI 都手写一遍 EditorGUILayout.
    - Shot: 0.00s-16.89s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“封装 DrawProp / DrawTex / BeginGroup 工具类”，弱化其他内容；旁白：阶段6：封装工具类（Refactoring Utility）—— 逐字稿 如果我们每个 ShaderGUI 都手写一遍 EditorGUILayout。
  - `cue-02` 00:16.89-00:24.44 segment 1: reveal-focus -> content-beat (提高编写效率); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: BeginVertical("box")，代码会变得冗长且难以维护。
    - Shot: 16.89s-24.44s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“提高编写效率”，弱化其他内容；旁白：BeginVertical("box")，代码会变得冗长且难以维护。
  - `cue-03` 00:24.44-00:27.56 segment 2: reveal-focus -> content-beat (视觉统一性); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 作为开发者，我们要学会抽象。
    - Shot: 24.44s-27.56s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“视觉统一性”，弱化其他内容；旁白：作为开发者，我们要学会抽象。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_02/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
