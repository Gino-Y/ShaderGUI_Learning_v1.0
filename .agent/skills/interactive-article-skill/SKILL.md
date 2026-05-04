---
name: interactive-article-skill
description: Designs Distill-style long-form interactive articles. Use when a deep technical topic needs article structure, progressive explanation, embedded interactive figures, citations, and linked views.
---

# Interactive Article Skill

## Purpose

Use this skill when the article is the main learning surface and interactions are embedded to support a long explanation. It is best for research-style or deep technical content where learners need a progressive evidence chain.

## Best Fit

- Complex concept or research explanation.
- Multiple sections, citations, diagrams, and code notes.
- Interactions clarify paragraphs rather than becoming a standalone playground.
- Learner benefits from scroll-linked anchors and linked visual views.

## Workflow

1. Define the article thesis and reader promise.
2. Split the explanation into sections with one interaction per major idea.
3. Build concept models for embedded figures.
4. Specify linked views: text, diagram, table, formula, code, result.
5. Plan progressive disclosure from intuition to formal model.
6. Validate that every interaction supports a paragraph-level claim.

## Output Contract

```text
.agent/interactive-content/<module-id>/<article-id>/
├── interaction-brief.md
├── article-outline.md
├── concept-model.json
├── storyboard.json
├── component-spec.md
└── validation-report.md
```

## Quality Bar

- The article must remain readable without interaction.
- Interactions must be placed where they prove or clarify a claim.
- Avoid decorative charts.
- Provide accessible fallback text for each figure.
