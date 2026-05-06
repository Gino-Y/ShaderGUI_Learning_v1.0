# Visual Execution Optimization Plan

## Goal

Solve the current gap where storyboard/design contracts keep improving but the rendered course screens do not become visibly better.

The optimization target is not "more storyboard text". The target is a closed visual execution loop:

```text
storyboard/design intent
  -> visual tokens
  -> Vue renderer implementation
  -> screenshot verification
  -> visual acceptance report
```

## Current Diagnosis

The current DAG already has a strong production chain:

```text
CourseMCP -> MVPMCP -> StoryboardMCP -> V0MCP -> DesignMCP -> VoiceMCP -> StitchMCP -> Verify -> Build -> Audit
```

The weak point is visual execution:

- `StoryboardMCP` can produce rich visual intent.
- `DesignMCP` can produce design contracts.
- `SlideCanvas.vue` still relies heavily on hardcoded layout, color, and motion behavior.
- Existing verification checks structure and runtime markers, but not visual quality.
- The full MVP loop is too heavy for fast visual iteration.

## Proposed Architecture

Add a dedicated visual execution layer between `DesignMCP` and runtime rendering.

```text
StoryboardMCP
  -> DesignMCP
  -> VisualCompilerMCP
  -> visual-tokens.json
  -> SlideCanvas / PerformanceLayer / Lab renderer
  -> Playwright screenshots
  -> VisualAuditMCP
```

## Deliverables

### 1. Visual Token Contract

Create:

```text
CourseApp/src/data/visual-tokens.json
.agent/design/Module_01/visual-tokens-brief.md
```

The token file must be renderer-friendly and avoid vague natural language.

Required structure:

```json
{
  "module": "Module_01",
  "slides": [
    {
      "moduleId": "Module_01",
      "slideId": "p00",
      "theme": "technical-editorial",
      "layout": {
        "type": "concept-board",
        "columns": "56/44",
        "safeMargin": "7%"
      },
      "background": {
        "type": "layered-radial",
        "base": "#06111f",
        "accents": [
          {
            "position": "18% 24%",
            "color": "rgba(45, 212, 191, 0.18)",
            "size": "42rem"
          }
        ]
      },
      "surface": {
        "panel": "glass",
        "border": "rgba(255,255,255,0.14)",
        "shadow": "0 24px 80px rgba(0,0,0,0.34)"
      },
      "motion": {
        "activeScale": 1.035,
        "dimOpacity": 0.38,
        "durationMs": 680
      }
    }
  ]
}
```

Acceptance:

- No vague fields such as `"soft radial highlights"` without renderable values.
- Every current MVP slide has tokens.
- Tokens validate as UTF-8 JSON.

### 2. VisualCompilerMCP

Create:

```text
.agent/mcp_servers/visual_compiler_mcp.py
```

Responsibilities:

- Read `storyboard-contract.json`.
- Read `design-contract.json`.
- Compile visual intent into `visual-tokens.json`.
- Reject vague visual values that cannot be rendered.
- Emit a brief explaining how each slide's visual tokens were derived.

Pipeline position:

```text
DESIGN_READY -> VISUAL_TOKENS_READY -> TRANSCRIPTS_READY
```

Acceptance:

- Flow state includes `visual_tokens_file`.
- `verify_course.py` validates `visual-tokens.json`.
- `SlideCanvas.vue` imports and consumes `visual-tokens.json`.

### 3. Renderer Capability Matrix

Create:

```text
.agent/design/renderer-capability-matrix.md
```

Purpose:

Define what the renderer can actually draw. Storyboard/design output must stay inside this capability matrix unless a renderer upgrade is explicitly planned.

Initial capabilities:

- `layout.type`: `concept-board`, `code-board`, `lab-workbench`, `quiz-card`
- `background.type`: `layered-radial`, `grid-surface`, `quiet-paper`, `none`
- `surface.panel`: `glass`, `paper`, `code-terminal`
- `motion.primary`: `focus-pulse`, `code-token-highlight`, `card-reveal`
- `accent.role`: `concept`, `code`, `feedback`, `warning`

Acceptance:

- `VisualCompilerMCP` validates tokens against this matrix.
- If a storyboard asks for unsupported visuals, validation fails with a concrete missing capability.

### 4. SlideCanvas Visual Token Integration

Modify templates, not only generated runtime:

```text
.agent/templates/course-app/src/components/SlideCanvas.vue
.agent/templates/course-app/src/components/PerformanceLayer.vue
.agent/templates/course-app/src/components/ParticleDecoration.vue
```

Expected changes:

- `SlideCanvas.vue` receives or imports tokens by `moduleId + slideId`.
- Background, layout, panel style, accent colors, and motion intensity come from tokens.
- `ParticleDecoration.vue` reads token payload instead of hardcoded colors.
- Code token highlight intensity comes from tokens and cue state.

Acceptance:

- The same storyboard with different tokens produces visibly different screens.
- `p00` and `p01` no longer share the same generic dark-tech look.
- Runtime still hides internal production guidance.

### 5. Screenshot Visual Audit

Create:

```text
scripts/visual_audit.py
.agent/reports/visual-audit/Module_01/
```

Responsibilities:

- Open the local app routes with Playwright or an equivalent browser runner.
- Capture screenshots for:
  - `/`
  - `/module/Module_01/slide/p00`
  - `/module/Module_01/slide/p01`
  - `/module/Module_01/slide/p01/explore`
  - `/module/Module_01/quiz`
- Check basic visual failures:
  - blank screen
  - unreadable low contrast
  - text overflow
  - content overlap
  - missing slide canvas
  - missing navigation
  - identical-looking slide backgrounds when tokens differ

Acceptance:

- Screenshots are written to `.agent/reports/visual-audit/Module_01/`.
- Audit JSON contains pass/fail and reason.
- Failing visual audit blocks delivery when visual code changed.

### 6. Fast Visual Iteration Command

Add a lightweight test stage:

```powershell
python .agent\flow_engine.py --mode test --stage visual --scope module --module Module_01 --basedir .
```

This stage should run only:

```text
StoryboardMCP
DesignMCP
VisualCompilerMCP
template/runtime sync
verify_course.py
npm build
visual_audit.py
```

It must not regenerate MP3 unless transcript/audio changed.

Acceptance:

- Visual iteration completes much faster than full MVP.
- The command produces updated visual tokens and visual audit screenshots.

## Execution Phases

### Phase 1: Contract And Gate

Deliver:

- `visual-tokens.json` schema.
- `VisualCompilerMCP` minimal implementation.
- `verify_course.py` checks for token file presence and slide coverage.
- `renderer-capability-matrix.md`.

Definition of done:

- `python scripts\verify_course.py` fails if tokens are missing or incomplete.
- Existing app still builds.

### Phase 2: Renderer Consumption

Deliver:

- `SlideCanvas.vue` consumes tokens.
- `PerformanceLayer.vue` consumes tokenized visual payload.
- Runtime and template remain synchronized.

Definition of done:

- `p00` and `p01` have visibly different layout, background, and emphasis.
- `npm --prefix CourseApp run build` passes.

### Phase 3: Screenshot Audit

Deliver:

- `scripts/visual_audit.py`.
- `.agent/reports/visual-audit/Module_01/*.png`.
- `.agent/reports/visual-audit/Module_01/report.json`.

Definition of done:

- Visual audit can detect blank/overlap/low-contrast regressions.
- Audit report is referenced in handoff.

### Phase 4: Fast Visual Stage

Deliver:

- `visual` test stage in `.agent/run_guard.py`.
- `flow_engine.py` branch for visual-only iteration.

Definition of done:

- `python .agent\flow_engine.py --mode test --stage visual --scope module --module Module_01 --basedir .` runs without full audio regeneration.

## File Change Map

Expected files to add:

```text
.agent/mcp_servers/visual_compiler_mcp.py
.agent/design/renderer-capability-matrix.md
.agent/reports/visual-audit/Module_01/
scripts/visual_audit.py
CourseApp/src/data/visual-tokens.json
```

Expected files to modify:

```text
.agent/flow_engine.py
.agent/run_guard.py
.agent/rules.md
.agent/SKILL.md
docs/Skill_Chain_DAG.md
scripts/verify_course.py
.agent/templates/scripts/verify_course.py
.agent/templates/course-app/src/components/SlideCanvas.vue
.agent/templates/course-app/src/components/PerformanceLayer.vue
.agent/templates/course-app/src/components/ParticleDecoration.vue
```

## Verification Commands

Minimum after Phase 1:

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

Minimum after Phase 2:

```powershell
python scripts\verify_course.py
npm --prefix CourseApp run build
```

Minimum after Phase 3:

```powershell
python scripts\visual_audit.py --module Module_01 --base-url http://127.0.0.1:5173
```

Minimum after Phase 4:

```powershell
python .agent\flow_engine.py --mode test --stage visual --scope module --module Module_01 --basedir .
```

## Risks

- Visual tokens may become another document layer unless `SlideCanvas.vue` consumes them directly.
- Screenshot audit can catch structural failures but cannot fully judge taste.
- Too many token variants can make the renderer brittle; start with four layout types and three background types only.
- Full MVP remains necessary for final delivery; visual stage is only an iteration shortcut.

## Recommendation

Start with Phase 1 and Phase 2 only.

The most important first milestone is:

```text
storyboard/design -> visual-tokens.json -> SlideCanvas consumes tokens -> p00/p01 visibly diverge
```

Do not spend more effort upgrading storyboard prose until this milestone is working.
