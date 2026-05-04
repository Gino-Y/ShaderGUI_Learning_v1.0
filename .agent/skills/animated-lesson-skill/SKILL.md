---
name: animated-lesson-skill
description: Designs 3Blue1Brown-style animated lessons. Use when the core concept depends on continuous visual transformation, spatial intuition, timing, or narration.
---

# Animated Lesson Skill

## Purpose

Use this skill when animation is the clearest way to build intuition. The output is a lesson plan and runtime spec for keyframes, transitions, narration rhythm, and optional checkpoints.

## Best Fit

- Abstract math, spatial transformation, or state transition.
- Learner needs to see continuity rather than only before/after states.
- Animation carries the explanation.
- Interactions are checkpoints, scrubbing, or small parameter changes.

## Workflow

1. Define the visual metaphor.
2. Write a scene list with learning intent per scene.
3. Define keyframes, transitions, and narration beats.
4. Specify learner controls such as play, pause, scrub, reset, and checkpoints.
5. Add optional quiz or reflection points.
6. Validate pacing, readability, and mobile behavior.

## Output Contract

```text
.agent/interactive-content/<module-id>/<lesson-id>/
├── interaction-brief.md
├── scene-script.md
├── keyframes.json
├── component-spec.md
└── validation-report.md
```

## Quality Bar

- Animation must explain a concept, not decorate a slide.
- Every scene needs a clear observation target.
- Provide pause or scrub controls for dense sequences.
- Text must not occlude the primary visual.
