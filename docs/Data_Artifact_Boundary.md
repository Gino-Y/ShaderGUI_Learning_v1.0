# Data Artifact Instantiation Boundary

This document is an authoritative supplement to `docs/Skill_Chain_DAG.md`, `.agent/rules.md`, and `.agent/SKILL.md`.

## Rule

- The DAG describes generic workflow, node responsibility, input/output contracts, validation rules, and failure backflow only.
- The DAG must not carry concrete lesson prose, transcript prose, quiz prompts, answers, explanations, exploration copy, or module-specific data instances as contract content.
- MCP servers implement capabilities only: read source inputs, transform data, generate files, and validate outputs.
- MCP servers must not hard-code course prose, transcript prose, quiz banks, answers, exploration content, or a single supported module/page sequence.
- Course instance data must come from explicit source artifacts such as `docs/`, `CourseContent/<module-id>/course.json`, `CourseContent/<module-id>/slides.json`, `CourseContent/<module-id>/quizzes.json`, `CourseContent/<module-id>/explorations.json`, and `CourseContent/<module-id>/doc/*.md`.
- `CourseContent/` is source input. MVP cleanup must not delete it.
- `MVPMCP.generate_products` must read from `CourseContent/<module-id>/` and generate runtime artifacts under `CourseApp/` and `scripts/`.

## Verification

`scripts/verify_course.py` must scan `.agent/mcp_servers/*.py` for known course prose and block regressions where lesson data is reintroduced into MCP capability nodes.
