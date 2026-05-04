# Data Artifact Instantiation Boundary

- DAG and MCP servers must not contain concrete lesson prose, transcript prose, quiz prompts, answers, explanations, exploration copy, or module-specific data instances.
- Course instance data must come from `docs/`, `CourseContent/<module-id>/`, or an explicit source manifest.
- `CourseContent/` is source input and must not be removed by MVP cleanup.
- `MVPMCP.generate_products` reads source artifacts and writes runtime artifacts. It must not instantiate course data from Python literals.
- Verification must scan `.agent/mcp_servers/*.py` for course prose regressions.
