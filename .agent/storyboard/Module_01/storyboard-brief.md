# Storyboard Brief

- Provider mode: `storyboard-local-spec`
- Module: `Module_01`
- Source: `{'slides': 'CourseApp/src/data/slides.json', 'explorations': 'CourseApp/src/data/explorations.json', 'quizzes': 'CourseApp/src/data/quizzes.json'}`
- Role: Film-style storyboard layer before visual design.
- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.

## Scenes

### Module_01 / p00

- Route: `/module/Module_01/slide/p00`
- Title: ShaderGUI：不仅仅是换个皮
- Purpose: Use this scene to make learners understand 'ShaderGUI：不仅仅是换个皮' through the content beats: .
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:

### Module_01 / p01

- Route: `/module/Module_01/slide/p01`
- Title: 编写第一个自定义材质面板
- Purpose: Use this scene to make learners understand '编写第一个自定义材质面板' through the content beats: .
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:

### Module_01 / p02

- Route: `/module/Module_01/slide/p02`
- Title: 如何安全地获取参数？
- Purpose: Use this scene to make learners understand '如何安全地获取参数？' through the content beats: .
- Layout: concept hierarchy and mental model
- Composition: wide instructional concept board / upper-left title -> left hero concept -> right supporting cards -> bottom focus statement
- Frame grid: {'columns': 'left 56% hero concept and explanation, right 44% supporting cards', 'rows': 'top metadata band, center concept body, bottom learner focus', 'anchor': 'hero concept anchors upper-left; supporting beats form right-side vertical rhythm'}
- Palette: clear, instructional, confident
- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).
- Motion cues:

## Interactive Screens

### explore-p01-property-grouping - 探索页

- Route: `/module/Module_01/slide/p01/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### explore-p02-property-grouping - 属性查找实战

- Route: `/module/Module_01/slide/p02/explore`
- Purpose: Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.
- Layout: interactive property grouping lab
- Composition: wide interactive workbench / breadcrumb -> controls -> live feedback -> return to lesson
- Realtime cues: 3
- Handoff target: `CourseApp/src/views/ExploreView.vue`

### quiz - 做题页

- Route: `/module/Module_01/quiz`
- Purpose: Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.
- Layout: single active question card
- Composition: medium close assessment card / breadcrumb -> question type/progress -> question stem -> options -> submit
- Realtime cues: 5
- Handoff target: `CourseApp/src/views/QuizView.vue`
