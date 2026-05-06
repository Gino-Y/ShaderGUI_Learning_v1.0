# Design Brief

- Provider mode: `design-v0-translated-spec`
- Module: `Module_02`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'storyboard': 'CourseApp/src/data/storyboard-contract.json', 'v0Prototype': '.agent/v0/Module_02/react-prototype.json'}`
- Goal: Generate or refine high-fidelity course-player UI screens for the Vue SPA.
- Storyboard source: `CourseApp/src/data/storyboard-contract.json`.
- v0 source: `.agent/v0/<module>/react-prototype.json`; translate design rules, do not copy React code directly.
- Hard rule: Course production workflow text must not appear inside course slides.
- Hard rule: Full transcripts are production material only; the runtime shows subtitles from audio events.
- Hard rule: Motion cues are described for the future web animation module and triggered from subtitle events.

## Screens

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
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, DiagramPlaceholder, SlideNav

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
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
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
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

## Interactive Screens

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

## Validation History

- Last contract check: None
- Last visual ref check: None
- Contract check attempts: 0
- Visual ref check attempts: 0
