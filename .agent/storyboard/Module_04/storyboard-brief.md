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
  - `cue-01` 00:00.00-00:21.78 segment 0: reveal-focus -> content-beat (在 OnGUI 末尾检测属性变化); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 渲染状态同步：让 GUI 替人思考 —— 逐字稿 你有没有遇到过这种情况：美术在面板里把混合模式从 Alpha 混合改成了加法混合，结果渲染出来颜色完全不对，一查才发现是 Blend 状态没同步。
    - Shot: 0.00s-21.78s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“在 OnGUI 末尾检测属性变化”，弱化其他内容；旁白：渲染状态同步：让 GUI 替人思考 —— 逐字稿 你有没有遇到过这种情况：美术在面板里把混合模式从 Alpha 混合改成了加法混合，结果渲染出来颜色完全不对，一查才发现是 Blend 状态没同步。
  - `cue-02` 00:21.78-00:31.33 segment 1: reveal-focus -> content-beat (自动同步 Blend、ZWrite、RenderQueue); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 更糟糕的是，这种错误往往不会报错，只会在画面上留下难以察觉的瑕疵，直到上线前才被发现。
    - Shot: 21.78s-31.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“自动同步 Blend、ZWrite、RenderQueue”，弱化其他内容；旁白：更糟糕的是，这种错误往往不会报错，只会在画面上留下难以察觉的瑕疵，直到上线前才被发现。

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
  - `cue-01` 00:00.00-00:03.33 segment 0: reveal-focus -> content-beat (属性名 Fallback); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 版本迁移：如何让旧资产不碎掉？
    - Shot: 0.00s-3.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“属性名 Fallback”，弱化其他内容；旁白：版本迁移：如何让旧资产不碎掉。
  - `cue-02` 00:03.33-00:09.78 segment 1: reveal-focus -> content-beat (语义映射); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: —— 逐字稿 在实际工程中，Shader 是会不断迭代的。
    - Shot: 3.33s-9.78s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“语义映射”，弱化其他内容；旁白：—— 逐字稿 在实际工程中，Shader 是会不断迭代的。
  - `cue-03` 00:09.78-00:26.00 segment 2: reveal-focus -> content-beat (静默升级策略); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 我见过太多团队遇到这样的噩梦：某天改了 Shader 的一个属性名，结果整个项目几百个材质球全部报错，美术同学打开材质面板看到一片空白，直接崩溃。
    - Shot: 9.78s-26.00s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“静默升级策略”，弱化其他内容；旁白：我见过太多团队遇到这样的噩梦：某天改了 Shader 的一个属性名，结果整个项目几百个材质球全部报错，美术同学打开材质面板看到一片空白，直接崩溃。

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
  - `cue-01` 00:00.00-00:17.11 segment 0: reveal-focus -> content-beat (分组清晰); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 阶段11：实战验收：MOutlineFittingh01 —— 逐字稿 最后，我们将所有的知识点汇聚到 MOutlineFittingh01 这个案例中。
    - Shot: 0.00s-17.11s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“分组清晰”，弱化其他内容；旁白：阶段11：实战验收：MOutlineFittingh01 —— 逐字稿 最后，我们将所有的知识点汇聚到 MOutlineFittingh01 这个案例中。
  - `cue-02` 00:17.11-00:25.33 segment 1: reveal-focus -> content-beat (安全可靠); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 这不再是一个简单的 Shader 练习，而是一个符合工业化标准的材质工具。
    - Shot: 17.11s-25.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“安全可靠”，弱化其他内容；旁白：这不再是一个简单的 Shader 练习，而是一个符合工业化标准的材质工具。
  - `cue-03` 00:25.33-00:34.22 segment 2: reveal-focus -> content-beat (美术友好); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 从这一刻起，你不再只是在"写 Shader"，你是在为团队定义一套"创作标准"。
    - Shot: 25.33s-34.22s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“美术友好”，弱化其他内容；旁白：从这一刻起，你不再只是在"写 Shader"，你是在为团队定义一套"创作标准"。
  - `cue-04` 00:34.22-00:41.33 segment 3: reveal-focus -> content-beat (性能同步); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 当我们把这份 GUI 交付给美术同学时，我们交付的是效率和信心。
    - Shot: 34.22s-41.33s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“性能同步”，弱化其他内容；旁白：当我们把这份 GUI 交付给美术同学时，我们交付的是效率和信心。

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
  - `cue-01` 00:00.00-00:16.44 segment 0: reveal-focus -> content-beat (解构阶段); focus `knowledge-01` with pulse-once-then-hold / knowledge-highlight; target `point-card`; source subtitle: 阶段12：ShaderGUI 进阶思维路线图 —— 逐字稿 学习 ShaderGUI 的过程，本质上是学习如何处理"人、机器、资产"三者关系的过程。
    - Shot: 0.00s-16.44s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“解构阶段”，弱化其他内容；旁白：阶段12：ShaderGUI 进阶思维路线图 —— 逐字稿 学习 ShaderGUI 的过程，本质上是学习如何处理"人、机器、资产"三者关系的过程。
  - `cue-02` 00:16.44-00:19.78 segment 1: reveal-focus -> content-beat (重构阶段); focus `knowledge-02` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 代码是死的，但交互逻辑是活的。
    - Shot: 16.44s-19.78s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“重构阶段”，弱化其他内容；旁白：代码是死的，但交互逻辑是活的。
  - `cue-03` 00:19.78-00:32.00 segment 2: reveal-focus -> content-beat (进化阶段); focus `knowledge-03` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 希望这门课能帮你开启"工程化开发"的大门，让你在 TA 的道路上不仅能做出绚丽的特效，更能搭建出稳健的流水线。
    - Shot: 19.78s-32.00s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“进化阶段”，弱化其他内容；旁白：希望这门课能帮你开启"工程化开发"的大门，让你在 TA 的道路上不仅能做出绚丽的特效，更能搭建出稳健的流水线。
  - `cue-04` 00:32.00-00:33.20 segment 3: reveal-focus -> content-beat (治理阶段); focus `knowledge-04` with soft-blink-then-hold / knowledge-highlight; target `point-card`; source subtitle: 谢谢大家！
    - Shot: 32.00s-33.20s 保持标题和主体结构稳定，将知识点卡片切到当前焦点“治理阶段”，弱化其他内容；旁白：谢谢大家。

## Interactive Screens

### quiz - 做题页

- Route: `/module/Module_04/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
