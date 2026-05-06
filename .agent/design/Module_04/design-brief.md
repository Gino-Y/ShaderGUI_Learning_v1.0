# Design Brief

- Provider mode: `design-v0-translated-spec`
- Module: `ADP_ACCUMULATED`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'storyboard': 'CourseApp/src/data/storyboard-contract.json', 'v0Prototype': '.agent/v0/Module_04/react-prototype.json'}`
- Goal: Generate or refine high-fidelity course-player UI screens for the Vue SPA.
- Storyboard source: `CourseApp/src/data/storyboard-contract.json`.
- v0 source: `.agent/v0/<module>/react-prototype.json`; translate design rules, do not copy React code directly.
- Hard rule: Course production workflow text must not appear inside course slides.
- Hard rule: Full transcripts are production material only; the runtime shows subtitles from audio events.
- Hard rule: Motion cues are described for the future web animation module and triggered from subtitle events.

## Screens

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不仅仅是换个皮
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: ShaderGUI：不仅仅是换个皮. Key points: ShaderGUI 是 Shader 参数系统的前端工程层 / 不是简单的 UI 美化.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=2. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand 'ShaderGUI：不仅仅是换个皮' through the content beats: ShaderGUI 是 Shader 参数系统的前端工程层 / 不是简单的 UI 美化.
- Motion cues: 2
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 编写第一个自定义材质面板
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 编写第一个自定义材质面板. Key points: 继承 ShaderGUI / 重写 OnGUI / 通过 CustomEditor 绑定.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '编写第一个自定义材质面板' through the content beats: 继承 ShaderGUI / 重写 OnGUI / 通过 CustomEditor 绑定.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_01 / p02

- Route: `/module/Module_01/slide/p02`
- Title: 如何安全地获取参数？
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 如何安全地获取参数？. Key points: Required 模式的风险 / Safe 模式的安全获取 / 封装 FindPropertySafe 工具函数.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '如何安全地获取参数？' through the content beats: Required 模式的风险 / Safe 模式的安全获取 / 封装 FindPropertySafe 工具函数.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_02 / p00

- Route: `/module/Module_02/slide/p00`
- Title: 告别参数地狱：逻辑化的分组设计
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 告别参数地狱：逻辑化的分组设计. Key points: 信息架构设计 / BeginVertical 创建视觉边界 / 按渲染逻辑排列参数.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '告别参数地狱：逻辑化的分组设计' through the content beats: 信息架构设计 / BeginVertical 创建视觉边界 / 按渲染逻辑排列参数.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_02 / p01

- Route: `/module/Module_02/slide/p01`
- Title: 只给用户他需要的：智能 UI 联动
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 只给用户他需要的：智能 UI 联动. Key points: 条件显示技术 / Toggle/Enum 控制参数组显隐 / EditorGUI.DisabledScope 应用.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '只给用户他需要的：智能 UI 联动' through the content beats: 条件显示技术 / Toggle/Enum 控制参数组显隐 / EditorGUI.DisabledScope 应用.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_02 / p02

- Route: `/module/Module_02/slide/p02`
- Title: 拒绝代码重复：打造 ShaderGUI 工具箱
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 拒绝代码重复：打造 ShaderGUI 工具箱. Key points: 封装 DrawProp / DrawTex / BeginGroup 工具类 / 提高编写效率 / 视觉统一性.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '拒绝代码重复：打造 ShaderGUI 工具箱' through the content beats: 封装 DrawProp / DrawTex / BeginGroup 工具类 / 提高编写效率 / 视觉统一性.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_03 / p00

- Route: `/module/Module_03/slide/p00`
- Title: 像搭积木一样构建材质面板
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 像搭积木一样构建材质面板. Key points: 模块化思维 / 静态功能类设计 / DrawProperties 静态方法.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '像搭积木一样构建材质面板' through the content beats: 模块化思维 / 静态功能类设计 / DrawProperties 静态方法.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_03 / p01

- Route: `/module/Module_03/slide/p01`
- Title: Managed Properties：面板的行政管理
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: Managed Properties：面板的行政管理. Key points: 注册机制与自动补位 / 确保不漏掉参数 / 不重复绘制.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand 'Managed Properties：面板的行政管理' through the content beats: 注册机制与自动补位 / 确保不漏掉参数 / 不重复绘制.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: grid-cols-1
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_04 / p00

- Route: `/module/Module_04/slide/p00`
- Title: 渲染状态同步：让 GUI 替人思考
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 渲染状态同步：让 GUI 替人思考. Key points: 在 OnGUI 末尾检测属性变化 / 自动同步 Blend、ZWrite、RenderQueue.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=2. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '渲染状态同步：让 GUI 替人思考' through the content beats: 在 OnGUI 末尾检测属性变化 / 自动同步 Blend、ZWrite、RenderQueue.
- Motion cues: 2
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_04 / p01

- Route: `/module/Module_04/slide/p01`
- Title: 版本迁移：如何让旧资产不碎掉？
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 版本迁移：如何让旧资产不碎掉？. Key points: 属性名 Fallback / 语义映射 / 静默升级策略.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '版本迁移：如何让旧资产不碎掉？' through the content beats: 属性名 Fallback / 语义映射 / 静默升级策略.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_04 / p02

- Route: `/module/Module_04/slide/p02`
- Title: 最终实战：构建专业级描边材质面板
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 最终实战：构建专业级描边材质面板. Key points: 分组清晰 / 安全可靠 / 美术友好 / 性能同步.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=4. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '最终实战：构建专业级描边材质面板' through the content beats: 分组清晰 / 安全可靠 / 美术友好.
- Motion cues: 4
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

### Module_04 / p03

- Route: `/module/Module_04/slide/p03`
- Title: ShaderGUI 进阶思维路线图
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: ShaderGUI 进阶思维路线图. Key points: 解构阶段 / 重构阶段 / 进化阶段 / 治理阶段.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=4. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand 'ShaderGUI 进阶思维路线图' through the content beats: 解构阶段 / 重构阶段 / 进化阶段.
- Motion cues: 4
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-body
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, DiagramPlaceholder, SlideNav

## Interactive Screens

### explore-p01-property-grouping - 探索页

- Route: `/module/Module_01/slide/p01/explore`
- Prompt: Design the exploration as a child page of the current lesson, not as a numbered slide. The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. Realtime storyboard actions to preserve: load-exploration-contract, manipulate-variable, return-to-parent-slide.
- Story purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Realtime cues: 3
- Runtime target: `CourseApp/src/views/ExplorationView.vue`
- Components: ExplorationShell, PropertyGroupingLab, LinkedFeedbackPanel, ReturnToParentSlide
- Constraints:
  - Exploration must not appear in slides.json and must not consume a pxx number.
  - The route must be a child of the parent slide route.
  - Interaction exists only because interaction-necessity-gate decided insert.
  - Provide an obvious return path to the parent lesson.

### explore-p02-property-grouping - 属性查找实战

- Route: `/module/Module_01/slide/p02/explore`
- Prompt: Design the exploration as a child page of the current lesson, not as a numbered slide. The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. Realtime storyboard actions to preserve: load-exploration-contract, manipulate-variable, return-to-parent-slide.
- Story purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Realtime cues: 3
- Runtime target: `CourseApp/src/views/ExplorationView.vue`
- Components: ExplorationShell, PropertyGroupingLab, LinkedFeedbackPanel, ReturnToParentSlide
- Constraints:
  - Exploration must not appear in slides.json and must not consume a pxx number.
  - The route must be a child of the parent slide route.
  - Interaction exists only because interaction-necessity-gate decided insert.
  - Provide an obvious return path to the parent lesson.

### quiz - 做题页

- Route: `/module/Module_01/quiz`
- Prompt: Design the quiz page as a live assessment workspace. The layout must foreground the question bank table, then answer cards, then immediate result feedback. Realtime storyboard actions to preserve: shuffle-question-bank, shuffle-options, select-answer, submit-answer, show-score. Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset.
- Story purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Realtime cues: 5
- Runtime target: `CourseApp/src/views/QuizView.vue`
- Components: QuestionBankTable, QuizQuestionCard, SingleChoiceInput, MultipleChoiceInput, OptionSwapControls, SubmitAnswerButton, ResultFeedback
- Constraints:
  - Use learner-facing quiz terminology in the UI.
  - Render storyboard realtime cues as visible guidance or behavior.
  - Do not hard-code question rows outside quizzes.json.
  - Keep answer identity tied to option id when options are reordered.
  - Submission feedback must be immediate and visible.

### explore-p01-smart-ui-linkage - 智能 UI 联动实验

- Route: `/module/Module_02/slide/p01/explore`
- Prompt: Design the exploration as a child page of the current lesson, not as a numbered slide. The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. Realtime storyboard actions to preserve: load-exploration-contract, manipulate-variable, return-to-parent-slide.
- Story purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Realtime cues: 3
- Runtime target: `CourseApp/src/views/ExplorationView.vue`
- Components: ExplorationShell, PropertyGroupingLab, LinkedFeedbackPanel, ReturnToParentSlide
- Constraints:
  - Exploration must not appear in slides.json and must not consume a pxx number.
  - The route must be a child of the parent slide route.
  - Interaction exists only because interaction-necessity-gate decided insert.
  - Provide an obvious return path to the parent lesson.

### quiz - 做题页

- Route: `/module/Module_02/quiz`
- Prompt: Design the quiz page as a live assessment workspace. The layout must foreground the question bank table, then answer cards, then immediate result feedback. Realtime storyboard actions to preserve: shuffle-question-bank, shuffle-options, select-answer, submit-answer, show-score. Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset.
- Story purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Realtime cues: 5
- Runtime target: `CourseApp/src/views/QuizView.vue`
- Components: QuestionBankTable, QuizQuestionCard, SingleChoiceInput, MultipleChoiceInput, OptionSwapControls, SubmitAnswerButton, ResultFeedback
- Constraints:
  - Use learner-facing quiz terminology in the UI.
  - Render storyboard realtime cues as visible guidance or behavior.
  - Do not hard-code question rows outside quizzes.json.
  - Keep answer identity tied to option id when options are reordered.
  - Submission feedback must be immediate and visible.

### explore-p00-modular-assembly - 模块化组装实验

- Route: `/module/Module_03/slide/p00/explore`
- Prompt: Design the exploration as a child page of the current lesson, not as a numbered slide. The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. Realtime storyboard actions to preserve: load-exploration-contract, manipulate-variable, return-to-parent-slide.
- Story purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Realtime cues: 3
- Runtime target: `CourseApp/src/views/ExplorationView.vue`
- Components: ExplorationShell, PropertyGroupingLab, LinkedFeedbackPanel, ReturnToParentSlide
- Constraints:
  - Exploration must not appear in slides.json and must not consume a pxx number.
  - The route must be a child of the parent slide route.
  - Interaction exists only because interaction-necessity-gate decided insert.
  - Provide an obvious return path to the parent lesson.

### quiz - 做题页

- Route: `/module/Module_03/quiz`
- Prompt: Design the quiz page as a live assessment workspace. The layout must foreground the question bank table, then answer cards, then immediate result feedback. Realtime storyboard actions to preserve: shuffle-question-bank, shuffle-options, select-answer, submit-answer, show-score. Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset.
- Story purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Realtime cues: 5
- Runtime target: `CourseApp/src/views/QuizView.vue`
- Components: QuestionBankTable, QuizQuestionCard, SingleChoiceInput, MultipleChoiceInput, OptionSwapControls, SubmitAnswerButton, ResultFeedback
- Constraints:
  - Use learner-facing quiz terminology in the UI.
  - Render storyboard realtime cues as visible guidance or behavior.
  - Do not hard-code question rows outside quizzes.json.
  - Keep answer identity tied to option id when options are reordered.
  - Submission feedback must be immediate and visible.

### explore-p02-render-state-playground - 渲染状态调试试验场

- Route: `/module/Module_04/slide/p02/explore`
- Prompt: Design the exploration as a child page of the current lesson, not as a numbered slide. The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. Realtime storyboard actions to preserve: load-exploration-contract, manipulate-variable, return-to-parent-slide.
- Story purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Realtime cues: 3
- Runtime target: `CourseApp/src/views/ExplorationView.vue`
- Components: ExplorationShell, PropertyGroupingLab, LinkedFeedbackPanel, ReturnToParentSlide
- Constraints:
  - Exploration must not appear in slides.json and must not consume a pxx number.
  - The route must be a child of the parent slide route.
  - Interaction exists only because interaction-necessity-gate decided insert.
  - Provide an obvious return path to the parent lesson.

### quiz - 做题页

- Route: `/module/Module_04/quiz`
- Prompt: Design the quiz page as a live assessment workspace. The layout must foreground the question bank table, then answer cards, then immediate result feedback. Realtime storyboard actions to preserve: shuffle-question-bank, shuffle-options, select-answer, submit-answer, show-score. Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset.
- Story purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Realtime cues: 5
- Runtime target: `CourseApp/src/views/QuizView.vue`
- Components: QuestionBankTable, QuizQuestionCard, SingleChoiceInput, MultipleChoiceInput, OptionSwapControls, SubmitAnswerButton, ResultFeedback
- Constraints:
  - Use learner-facing quiz terminology in the UI.
  - Render storyboard realtime cues as visible guidance or behavior.
  - Do not hard-code question rows outside quizzes.json.
  - Keep answer identity tied to option id when options are reordered.
  - Submission feedback must be immediate and visible.

## Validation History

- Last contract check: None
- Last visual ref check: None
- Contract check attempts: 0
- Visual ref check attempts: 0
