---
name: skill-router
description: Selects the right interactive content child skill based on topic shape, learner goal, interaction complexity, and delivery target. Use inside web-interactive-content-builder before designing or implementing a web interaction.
---

# Skill Router

## Purpose

Use this skill to choose which interactive content skill should run for a given teaching task. It may select one primary skill and optional supporting skills. This is the routing layer between the top-level Skill Registry and child Skill executors.

## Routing Inputs

Collect or infer:

- `topic`: what concept is being taught.
- `learner_goal`: what the learner should do or understand.
- `concept_count`: single concept, chapter, or full course.
- `state_complexity`: low, medium, or high.
- `requires_user_artifact`: whether the learner must create/export something.
- `requires_animation`: whether continuous motion is essential.
- `delivery_target`: article, course chapter, slide, embedded lab, playground, or workbench.

## Decision Rules

Use the first strong match:

| Signal | Primary skill | Why |
| --- | --- | --- |
| Full course, module tree, repeated lessons | `chapter-lab-skill` | Needs navigation, data contracts, and reusable lesson template |
| One focused concept with few variables | `explorable-mini-skill` | Best for quick intuition and immediate feedback |
| Many linked parameters or a train/run loop | `parameter-playground-skill` | Needs presets, state serialization, and comparison |
| User must gather examples, train, test, or export | `creative-workbench-skill` | Needs task workflow and artifact lifecycle |
| Understanding depends on smooth spatial change | `animated-lesson-skill` | Needs keyframes, narration, and visual metaphor |
| Long-form research explanation | `interactive-article-skill` | Needs article structure with embedded interactive figures |

## Composition Rules

Skill selection is not always single-choice.

- Course structure plus per-lesson experiments: `chapter-lab-skill + explorable-mini-skill`.
- Course structure plus complex parameter exploration: `chapter-lab-skill + parameter-playground-skill`.
- Animated explanation plus short manipulation checkpoint: `animated-lesson-skill + explorable-mini-skill`.
- Long-form article with embedded sandbox: `interactive-article-skill + parameter-playground-skill`.

## Default Routing For ShaderGUI

For the current ShaderGUI course:

```text
chapter-lab-skill + explorable-mini-skill
```

Choose:

- `chapter-lab-skill` when changing modules, lessons, course navigation, progress, quizzes, or data contracts.
- `explorable-mini-skill` when creating one slide-level or lesson-level experiment, such as material property grouping, conditional display, render-state sync, or property binding.

## Router Output

Always write the routing result in this shape:

```json
{
  "primarySkill": "chapter-lab-skill",
  "supportingSkills": ["explorable-mini-skill"],
  "reason": "The request changes course structure and also requires per-lesson experiments.",
  "requiresNecessityGate": true,
  "deliveryTarget": "CourseApp",
  "expectedArtifacts": [
    ".agent/interactive-content/Module_XX/interaction-brief.md",
    "CourseApp/src/data/course.json",
    "CourseApp/src/data/slides.json"
  ]
}
```

## Validation

Before proceeding, verify:

- The chosen skill directly matches the user's requested deliverable.
- The chosen skill can produce concrete files, not only design notes.
- If multiple skills are selected, each has a clear boundary.
- The route does not conflict with `.agent/rules.md`.
- If any interactive or explorable page may be inserted, `interaction-necessity-gate` must pass before changing `slides.json`.

## Interaction Necessity Gate

The router must answer this before any child skill creates a new interactive page:

```text
Without this interaction, would the learner be meaningfully worse at understanding, judging, or transferring the concept?
```

Route to an interactive child skill only when the answer is supported by evidence such as manipulable variables, immediate feedback, static-explanation weakness, learner risk, expected learning gain, and verifiable outcome.
