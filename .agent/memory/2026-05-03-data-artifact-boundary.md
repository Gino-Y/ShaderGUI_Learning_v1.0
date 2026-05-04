# Data Artifact Boundary Refactor

- User decision: AI skill DAG must stay generic; data artifact instantiation must not live in DAG or MCP servers.
- Judgment: This changes DAG/node responsibility, MVP source boundaries, cleanup rules, and verification.
- Changes: rewrote `.agent/mcp_servers/mvp_mcp.py` to read `CourseContent/<module-id>/` source files; added `CourseContent/Module_01/course.json`, `quizzes.json`, and `explorations.json`; removed `CourseContent/` from MVP cleanup in `.agent/mvp-execution-scope.json` and `.agent/run_guard.py`; added `docs/Data_Artifact_Boundary.md` and `.agent/data_artifact_boundary.md`.
- Regression guard: `scripts/verify_course.py` and the MVPMCP-generated verifier now scan `.agent/mcp_servers/*.py` against source transcript snippets to prevent course prose re-entering MCP literals.
- Verification: direct `MVPMCP.generate_products(..., "Module_01")` passed; `python scripts/verify_course.py` passed; `npm run build` in `CourseApp` passed; static search found no previous transcript literals, `DEFAULT_MVP_SLIDE_IDS`, `if module != "Module_01"`, or `CourseContent/Module_01` in MCP servers.
- Follow-up: user asked why full production DAG was not run. Reran `python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir .`.
- First full run failed at Stitch because `StitchMCP` still required `ExploreView.vue` even when `explorations.json` was empty. Fixed `StitchMCP` to require exploration runtime only when exploration source data exists.
- Full run also required generic audio output; restored generated TTS WAV creation and changed MVPMCP slide audio paths to `.wav`.
- Final full production DAG reached `DEPLOY_READY`; v0 chat id `hmvzWw3eC28`; post-run `python scripts\verify_course.py` and `npm run build` passed.
