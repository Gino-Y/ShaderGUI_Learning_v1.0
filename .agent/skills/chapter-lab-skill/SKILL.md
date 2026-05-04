---
name: chapter-lab-skill
description: Designs and maintains course-level interactive lab structure for CourseApp. Use when creating modules, chapters, lesson sequences, navigation, quizzes, progress gates, or data contracts for interactive course content.
---

# Chapter Lab Skill

## Purpose

Use this skill to manage the course structure around interactive labs. It owns module layout, lesson order, navigation, quiz/progress integration, and the data contracts that let `CourseApp` render the course.

## Responsibilities

- Define modules, lesson order, and learning outcomes.
- Decide which parent `pXX` owns each explore child page.
- Keep `course.json`, `slides.json`, and `quizzes.json` consistent.
- Preserve Vue Router paths used by the app.
- Coordinate lesson-level experiments produced by `explorable-mini-skill`.
- Keep quiz validation card-based: only the active question card is visible.
- Keep internal production guidance out of learner-facing pages.

## Course Data Contract

`CourseApp/src/data/course.json` should describe modules:

```json
{
  "id": "Module_01",
  "title": "模块一：解构",
  "summary": "理解 ShaderGUI 的定位，并完成最小自定义材质面板架构。",
  "slideCount": 2
}
```

`CourseApp/src/data/slides.json` should describe each lesson slide. Explore pages are child pages of a parent slide; they must not occupy their own `pXX` slide:

```json
{
  "moduleId": "Module_01",
  "slideId": "p01",
  "order": 1,
  "route": "/module/Module_01/slide/p01",
  "title": "最小可行性架构",
  "kind": "code",
  "explore": {
    "route": "/module/Module_01/slide/p01/explore",
    "title": "属性分组如何降低调参负担",
    "skill": "explorable-mini-skill",
    "component": "PropertyGroupingLab",
    "contract": ".agent/interactive-content/Module_01/p01/explore/concept-model.json",
    "necessityGate": ".agent/interactive-content/Module_01/p01/explore/necessity-gate.json"
  }
}
```

Keep new fields additive and explicit. Do not overload existing audio, subtitles, or transcript fields for interaction metadata. Do not use `kind: "interactive"` for formal slides.

## Workflow

1. Read existing course data.
   - `CourseApp/src/data/course.json`
   - `CourseApp/src/data/slides.json`
   - `CourseApp/src/data/quizzes.json`

2. Define chapter structure.
   - Module goal.
   - Lesson titles.
   - Required experiment per lesson.
   - Quiz coverage.

3. Assign interaction types.
   - Use `explorable-mini-skill` for each focused lab.
   - Reserve playground/workbench skills for larger tasks.

4. Update contracts.
   - Course data.
   - Slide data.
   - Quiz coverage.
   - `.agent/interactive-content/<module-id>/...` planning files.

5. Validate.
   - Every slide route matches `/module/:moduleId/slide/:slideId`.
   - `slideCount` equals the number of slides for the module.
   - Explore pages are nested under a parent slide and do not count toward `slideCount`.
   - No formal slide uses `kind: "interactive"`.
   - Every explore page references an existing component plan or component.
   - Quizzes test the module outcomes, not incidental UI details.
   - Quiz UI only shows the active question card, not a page header, return link, progress bar, table, question list, card navigation panel, or full-page question stream.
   - Submitting an answer automatically advances to the next question.
   - After the final question, the quiz shows only the score card.
   - Options are shuffled each time a question is displayed.
   - Question order is shuffled each time the learner restarts the quiz.
   - Learner-facing pages do not show storyboard guidance, design runtime guidance, Skill chain notes, or internal contract copy.

## Output

For a module update, produce:

```text
.agent/interactive-content/<module-id>/chapter-plan.md
.agent/interactive-content/<module-id>/chapter-contract.json
CourseApp/src/data/course.json
CourseApp/src/data/slides.json
CourseApp/src/data/quizzes.json
```

## Quality Bar

- A chapter must have a visible learning arc, not just a list of demos.
- Each lab must answer one concrete learner question.
- Progress and quiz gates must reflect understanding of ShaderGUI concepts.
- Course structure should remain data-driven and compatible with Vue Router.
