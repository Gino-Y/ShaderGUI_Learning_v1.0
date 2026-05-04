# 2026-05-03 探索页子路由与播放链闭环

- 用户反馈：探索页必须像做题页一样，不属于 `pXX` 范围，而是对应课时的子页面；当前正常课页无法播放；做题页和探索页缺少统一导航。
- 判断：这改变课程结构契约、MVP 验证规则、播放器链路和页面导航要求，必须更新 DAG、规则、Skill 与生成器。
- DAG：已更新 `docs/Skill_Chain_DAG.md`，明确当前 MVP 主线仅 `p00/p01`，探索页只能挂在 `/module/:moduleId/slide/:slideId/explore`，不得作为 `p02` 或 `kind=interactive` 进入 `slides.json`。
- 规则：已更新 `.agent/rules.md` 与 `.agent/SKILL.md`，固化探索页子路由、统一导航、TTS WAV 音频、播放链验证要求。
- 生成器：已重写 `.agent/mcp_servers/mvp_mcp.py` 的 MVP 输出，生成 `ExploreView.vue`、统一 `BreadcrumbNav.vue`、`SlideNav.vue` 探索入口、`QuizView.vue` 导航和 TTS WAV 音频脚本。
- 验证：`python .agent\flow_engine.py --mode production --scope module --module Module_01 --basedir . --max-retries 5` 已以 Windows System.Speech TTS WAV 方案跑通至 `DEPLOY_READY`。
- 运行：已重启 `http://localhost:5173/`，并验证 `/`、`/module/Module_01/slide/p00`、`/module/Module_01/slide/p01`、`/module/Module_01/slide/p01/explore`、`/module/Module_01/quiz` 和 `/audio/Module_01/p00.wav` 均返回 200。
