# 2026-05-04 Storyboard Runtime Restore

## Feedback

User reported that the newly developed screen regressed to the old state and asked for an urgent fix.

## Decision

The MVP generator must always bind storyboard contracts into the Vue runtime. Runtime pages cannot depend on hand-edited Vue files that are lost during clean-first MVP execution.

## Changes

- `MVPMCP` now injects scoped exploration metadata into generated slide data and keeps exploration pages as parent-slide child routes.
- `MVPMCP` now writes the storyboard-aware runtime shell after the base Vue files:
  - `CoursePlayer.vue` imports `storyboard-contract.json`.
  - `CoursePlayer.vue` binds `activeCue`, `visualComposition`, subtitle indexes, and audio time updates into `SlideCanvas.vue`.
  - `SlideCanvas.vue` renders storyboard composition and cue-driven visual emphasis.
  - `ExploreView.vue`, `BreadcrumbNav.vue`, `PropertyGroupingLab.vue`, and the upgraded `QuizView.vue` are regenerated on every MVP run.
- `StoryboardMCP` deduplicates exploration entries when both `explorations.json` and slide-level `explore` metadata describe the same child page.
- `StitchMCP` also deduplicates the same child exploration before writing `stitch-manifest.json`.

## Verification

- Full DAG runner reached `DEPLOY_READY` for `Module_01`.
- Vue production build passed.
- `storyboard-contract.json`, `design-contract.json`, and `stitch-manifest.json` now each contain one `explore-p01-property-grouping` entry plus `quiz`.
- Dev server restarted on `http://127.0.0.1:5173`.
- Verified routes:
  - `/`
  - `/module/Module_01/slide/p00`
  - `/module/Module_01/slide/p01`
  - `/module/Module_01/slide/p01/explore`
  - `/module/Module_01/quiz`
  - `/audio/Module_01/p00.mp3`
  - `/audio/Module_01/p01.mp3`
