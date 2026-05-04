# Design Brief

- Provider mode: `design-v0-translated-spec`
- Module: `Module_01`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'storyboard': 'CourseApp/src/data/storyboard-contract.json', 'v0Prototype': '.agent/v0/Module_01/react-prototype.json'}`
- Goal: Generate or refine high-fidelity course-player UI screens for the Vue SPA.
- Storyboard source: `CourseApp/src/data/storyboard-contract.json`.
- v0 source: `.agent/v0/<module>/react-prototype.json`; translate design rules, do not copy React code directly.
- Hard rule: Course production workflow text must not appear inside course slides.
- Hard rule: Full transcripts are production material only; the runtime shows subtitles from audio events.
- Hard rule: Motion cues are described for the future web animation module and triggered from subtitle events.

## Screens

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不只是换一层皮
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: ShaderGUI：不只是换一层皮. Key points: ShaderGUI 是 Shader 参数系统的前端工程层 / 核心目标是降低美术调参时的认知负担 / 职责是组织参数、解释含义、同步状态.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: https://v0.app/chat/qAnaC7HeGO9
- Story purpose: Use this scene to make learners understand 'ShaderGUI：不只是换一层皮' through the content beats: ShaderGUI 是 Shader 参数系统的前端工程层 / 核心目标是降低美术调参时的认知负担 / 职责是组织参数、解释含义、同步状态.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 最小可行架构
- Kind: code
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 最小可行架构. Key points: C Sharp 侧继承 ShaderGUI 并重写 OnGUI / Shader 侧通过 CustomEditor 绑定自定义面板 / 所有高级面板能力都从控制 OnGUI 开始.  Storyboard intent: layout focus=code structure and callout annotations; palette mood=precise, technical, focused; composition=medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway; foreground=right-center, inside high-contrast code panel; midground=left-center stacked vertical rhythm; negative space=reserve quiet space between left cards and right code so callout motion has room; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: https://v0.app/chat/qAnaC7HeGO9
- Story purpose: Use this scene to make learners understand '最小可行架构' through the content beats: C Sharp 侧继承 ShaderGUI 并重写 OnGUI / Shader 侧通过 CustomEditor 绑定自定义面板 / 所有高级面板能力都从控制 OnGUI 开始.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

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

### quiz - 做题页

- Route: `/module/Module_01/quiz`
- Prompt: Design the 做题页 as a live assessment workspace. The layout must foreground the question bank table, then answer cards, then immediate result feedback. Realtime storyboard actions to preserve: shuffle-question-bank, shuffle-options, select-answer, submit-answer, show-score. Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset.
- Story purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Realtime cues: 5
- Runtime target: `CourseApp/src/views/QuizView.vue`
- Components: QuestionBankTable, QuizQuestionCard, SingleChoiceInput, MultipleChoiceInput, OptionSwapControls, SubmitAnswerButton, ResultFeedback
- Constraints:
  - Use 做题页 terminology in learner-facing UI.
  - Render storyboard realtime cues as visible guidance or behavior.
  - Do not hard-code question rows outside quizzes.json.
  - Keep answer identity tied to option id when options are reordered.
  - Submission feedback must be immediate and visible.

## Validation History

- Last contract check: None
- Last visual ref check: None
- Contract check attempts: 0
- Visual ref check attempts: 0
