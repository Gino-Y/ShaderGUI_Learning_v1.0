# Design Brief

- Provider mode: `design-v0-translated-spec`
- Module: `Module_03`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'storyboard': 'CourseApp/src/data/storyboard-contract.json', 'v0Prototype': '.agent/v0/Module_03/react-prototype.json'}`
- Goal: Generate or refine high-fidelity course-player UI screens for the Vue SPA.
- Storyboard source: `CourseApp/src/data/storyboard-contract.json`.
- v0 source: `.agent/v0/<module>/react-prototype.json`; translate design rules, do not copy React code directly.
- Hard rule: Course production workflow text must not appear inside course slides.
- Hard rule: Full transcripts are production material only; the runtime shows subtitles from audio events.
- Hard rule: Motion cues are described for the future web animation module and triggered from subtitle events.

## Screens

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
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
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
  - Grid: left 56% hero concept and explanation, right 44% supporting cards
  - Spacing: gap-6

- Components: SlideTitle, PointList, SlideNav

## Interactive Screens

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

## Validation History

- Last contract check: None
- Last visual ref check: None
- Contract check attempts: 0
- Visual ref check attempts: 0
