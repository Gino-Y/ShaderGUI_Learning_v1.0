---
name: web-interactive-content-builder
description: Builds web interactive learning content from teaching topics, formulas, data, or course copy. Use when creating explorable explanations, chapter labs, parameter playgrounds, animated lessons, or task workbenches for CourseApp.
---

# Web Interactive Content Builder

## Purpose

Use this skill to turn a teaching topic into a runnable Web interaction plan and implementation path. It is the top-level coordinator and Skill Registry entry point; it delegates scenario choice to `skill-router` and execution details to child skills.

## Skill Registry

Available child skills:

| Child Skill | Reference Pattern | Use When |
| --- | --- | --- |
| `interactive-article-skill` | Distill | Long-form technical explanation with embedded interactive figures |
| `explorable-mini-skill` | Setosa | One focused concept with a few variables and immediate feedback |
| `parameter-playground-skill` | TensorFlow Playground | Many linked parameters, presets, run loops, and comparison |
| `creative-workbench-skill` | Teachable Machine | Learner creates, trains, tests, exports, or completes an artifact |
| `animated-lesson-skill` | 3Blue1Brown | Continuous visual transformation or spatial intuition is central |
| `chapter-lab-skill` | Seeing Theory | Multi-lesson course structure and repeated lab grammar |

## Default For This Project

For ShaderGUI course work, default to:

```text
web-interactive-content-builder
-> skill-router
-> chapter-lab-skill for course structure
-> explorable-mini-skill for each lesson experiment
```

Use another child skill only when the topic clearly fits better:

- `interactive-article-skill`: long-form research or deep technical article.
- `parameter-playground-skill`: many interdependent parameters or training loops.
- `creative-workbench-skill`: user must produce/export a model, asset, or tool.
- `animated-lesson-skill`: the core concept depends on continuous spatial transformation.

## Workflow

1. Define the learning target.
   - Topic.
   - Target learner.
   - What the learner should be able to judge or do after the interaction.

2. Build a concept model.
   - Objects: data entities, UI entities, shader/material entities.
   - State variables: user-editable values.
   - Derived values: formulas, flags, visual states, validation results.
   - Constraints: legal ranges, invalid combinations, defaults.

3. Route the scenario.
   - Invoke `skill-router`.
   - Record selected child skills and why.

4. Run the interaction necessity gate.
   - Produce `necessity-gate.json` before adding an explore child page.
   - Prove the interaction has learning value beyond a normal explanation page and quiz.
   - If the gate decision is `skip`, do not add the explore page.

5. Produce the interaction contract.
   - `interaction-brief.md`
   - `necessity-gate.json`
   - `concept-model.json`
   - `storyboard.json`
   - `component-spec.md`
   - implementation target in `CourseApp`
   - validation checklist

6. Implement or hand off.
   - For course structure, use `chapter-lab-skill`.
   - For lesson-level experiments, use `explorable-mini-skill`.
   - Keep course data driven by `CourseApp/src/data`.

7. Validate.
   - Build succeeds.
   - Interaction has a useful default state.
   - User action changes at least one visible result immediately.
   - There is a reset path.
   - The learning target is testable.

## Output Contract

For each explore child page, produce:

```text
.agent/interactive-content/<module-id>/<slide-id>/explore/
├── interaction-brief.md
├── necessity-gate.json
├── concept-model.json
├── storyboard.json
├── component-spec.md
└── validation-report.md
```

## Interaction Necessity Gate

Do not add an explore page just because it is possible. Add it only when the gate proves the interaction improves learning. Explore pages are child pages of a parent `pXX` slide and must not occupy their own `pXX` slide number.

Required decision file:

```text
.agent/interactive-content/<module-id>/<slide-id>/explore/necessity-gate.json
```

Minimum schema:

```json
{
  "candidateSlide": "p01/explore",
  "parentSlideId": "p01",
  "learningQuestion": "Why does grouping reduce material tuning burden?",
  "manipulableVariables": ["groupingMode"],
  "feedbackTargets": ["visiblePropertyCount", "riskWarnings"],
  "staticExplanationWeakness": "Static text cannot show the comparison cost clearly.",
  "learnerRisk": "Learners may confuse ShaderGUI with cosmetic UI changes.",
  "expectedLearningGain": "Learners directly compare grouped and flat layouts.",
  "verifiableOutcome": "Learners can identify why grouped parameters reduce risk.",
  "decision": "insert",
  "requiredEvidenceCount": 3
}
```

For implemented Vue content, update:

```text
CourseApp/src/data/course.json
CourseApp/src/data/slides.json
CourseApp/src/data/quizzes.json
CourseApp/src/components/
CourseApp/src/views/
```

## Quality Bar

- The first screen must teach something before the learner touches controls.
- Controls must map to real concept variables, not decorative animation.
- One action should update multiple representations when useful: diagram, value, formula, explanation, or code.
- Prefer a small correct experiment over a broad but vague playground.
- Avoid hidden magic: show enough state for the learner to infer cause and effect.
