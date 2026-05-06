# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_04`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_04 / p00

- Route: `/module/Module_04/slide/p00`
- Title: 渲染状态同步：让 GUI 替人思考
- Purpose: Use this scene to make learners understand '渲染状态同步：让 GUI 替人思考' through the content beats: 在 OnGUI 末尾检测属性变化 / 自动同步 Blend、ZWrite、RenderQueue.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (在 OnGUI 末尾检测属性变化); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 在 OnGUI 末尾检测属性变化
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“在 OnGUI 末尾检测属性变化”，弱化其他内容；旁白：在 OnGUI 末尾检测属性变化。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (自动同步 Blend、ZWrite、RenderQueue); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 自动同步 Blend、ZWrite、RenderQueue
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“自动同步 Blend、ZWrite、RenderQueue”，弱化其他内容；旁白：自动同步 Blend、ZWrite、RenderQueue。

### Module_04 / p01

- Route: `/module/Module_04/slide/p01`
- Title: 版本迁移：如何让旧资产不碎掉？
- Purpose: Use this scene to make learners understand '版本迁移：如何让旧资产不碎掉？' through the content beats: 属性名 Fallback / 语义映射 / 静默升级策略.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (属性名 Fallback); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 属性名 Fallback
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“属性名 Fallback”，弱化其他内容；旁白：属性名 Fallback。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (语义映射); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 语义映射
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“语义映射”，弱化其他内容；旁白：语义映射。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (静默升级策略); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 静默升级策略
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静默升级策略”，弱化其他内容；旁白：静默升级策略。

### Module_04 / p02

- Route: `/module/Module_04/slide/p02`
- Title: 最终实战：构建专业级描边材质面板
- Purpose: Use this scene to make learners understand '最终实战：构建专业级描边材质面板' through the content beats: 分组清晰 / 安全可靠 / 美术友好.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (分组清晰); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 分组清晰
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“分组清晰”，弱化其他内容；旁白：分组清晰。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (安全可靠); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 安全可靠
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“安全可靠”，弱化其他内容；旁白：安全可靠。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (美术友好); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 美术友好
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“美术友好”，弱化其他内容；旁白：美术友好。
  - `cue-04` 00:00.00-00:01.80 segment 3: reveal-focus -> content-beat (性能同步); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 性能同步
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“性能同步”，弱化其他内容；旁白：性能同步。

### Module_04 / p03

- Route: `/module/Module_04/slide/p03`
- Title: ShaderGUI 进阶思维路线图
- Purpose: Use this scene to make learners understand 'ShaderGUI 进阶思维路线图' through the content beats: 解构阶段 / 重构阶段 / 进化阶段.
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:
  - `cue-01` 00:00.00-00:01.80 segment 0: reveal-focus -> content-beat (解构阶段); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 解构阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“解构阶段”，弱化其他内容；旁白：解构阶段。
  - `cue-02` 00:00.00-00:01.80 segment 1: reveal-focus -> content-beat (重构阶段); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 重构阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“重构阶段”，弱化其他内容；旁白：重构阶段。
  - `cue-03` 00:00.00-00:01.80 segment 2: reveal-focus -> content-beat (进化阶段); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 进化阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“进化阶段”，弱化其他内容；旁白：进化阶段。
  - `cue-04` 00:00.00-00:01.80 segment 3: reveal-focus -> content-beat (治理阶段); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 治理阶段
    - Shot: 0.00s-1.80s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“治理阶段”，弱化其他内容；旁白：治理阶段。

## Interactive Screens

### explore-p02-render-state-playground - 渲染状态调试试验场

- Route: `/module/Module_04/slide/p02/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_04/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
