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
- Title: OnGUI 是唯一的入口
- Kind: concept
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: OnGUI 是唯一的入口. Key points: ShaderGUI 是材质面板的真正控制器 / OnGUI 每帧调用，负责绘制所有属性 / FindProperty 按名称取出属性引用.  Storyboard intent: layout focus=concept hierarchy and mental model; palette mood=clear, instructional, confident; composition=wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement; foreground=left-center hero area; midground=right-center, staggered stack; negative space=leave a quiet diagonal corridor from title to focus card for eye travel; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand 'OnGUI 是唯一的入口' through the content beats: ShaderGUI 是材质面板的真正控制器 / OnGUI 每帧调用，负责绘制所有属性 / FindProperty 按名称取出属性引用.
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
- Title: 参数分组与布局
- Kind: code
- Prompt: Design a focused Chinese technical course slide for Unity ShaderGUI. Title: 参数分组与布局. Key points: editor.LabelField 绘制分组标题 / editor.ShaderProperty 绘制单个属性 / GUILayout.Space 控制间距.  Storyboard intent: layout focus=code structure and callout annotations; palette mood=precise, technical, focused; composition=medium-wide technical board shot / upper-left title -> left point stack -> right active code fragment -> bottom takeaway; foreground=right-center, inside high-contrast code panel; midground=left-center stacked vertical rhythm; negative space=reserve quiet space between left cards and right code so callout motion has room; subtitle-triggered motion cues=3. Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. The visual should feel like a professional engineering training player: clear hierarchy, restrained controls, readable subtitles, and no internal workflow text.
- v0 chat: None
- Story purpose: Use this scene to make learners understand '参数分组与布局' through the content beats: editor.LabelField 绘制分组标题 / editor.ShaderProperty 绘制单个属性 / GUILayout.Space 控制间距.
- Motion cues: 3
- Constraints:
  - Only show ShaderGUI course content in the slide canvas.
  - Do not render full transcript text as a panel.
  - Subtitles must appear only as audio-time events.
  - Keep player controls outside the slide canvas.
  - Follow storyboard layout, palette, and motion intent before inventing new visual behavior.
  - Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.

- Layout:
  - Template: title-code
  - Grid: left 48% teaching beats, right 52% code panel
  - Spacing: gap-6

- Components: SlideTitle, CodeBlock, PointList, SlideNav

## Interactive Screens

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
