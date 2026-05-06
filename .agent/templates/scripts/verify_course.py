from __future__ import annotations
import ast
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "CourseApp"
CONTENT = ROOT / "CourseContent"
TODAY_MEMORY = ROOT / ".agent" / "memory" / f"{date.today().isoformat()}.md"

def load_json(path: Path, errors: list[str]):
    if not path.exists():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid json: {path.relative_to(ROOT)}: {exc}")
        return None

def source_snippets() -> list[str]:
    snippets = []
    for path in CONTENT.glob("*/doc/*.md"):
        text = path.read_text(encoding="utf-8-sig")
        for sentence in re.split("[\u3002\uff01\uff1f\uff1b\\n]", text):
            sentence = sentence.strip()
            if len(sentence) >= 18:
                snippets.append(sentence)
    return snippets

def check_mcp_content_boundary(errors: list[str]) -> None:
    snippets = source_snippets()
    for path in (ROOT / ".agent" / "mcp_servers").glob("*.py"):
        text = path.read_text(encoding="utf-8-sig")
        for snippet in snippets:
            if snippet in text:
                errors.append(f"MCP contains course instance prose: {path.relative_to(ROOT)}")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if any(snippet in node.value for snippet in snippets):
                    errors.append(f"MCP contains long prose literal: {path.relative_to(ROOT)}")
                    break

MOJIBAKE_MARKERS = [
    "\u951b", "\u9359", "\u6d63", "\u93c9", "\u7487", "\u9428", "\u9286", "\u9225", "\u95c8", "\u5bee",
    "\u93c8", "\u59af", "\u7481", "\u9a9e", "\u935a", "\u93c4", "\u701b", "\u6fb6", "\u9983", "\ufffd",
]

def check_utf8_and_mojibake(errors: list[str]) -> None:
    roots = [ROOT / ".agent", ROOT / "CourseContent", ROOT / "CourseApp" / "src", ROOT / "docs", ROOT / "scripts"]
    suffixes = {".md", ".json", ".py", ".js", ".vue", ".css", ".html", ".yml", ".yaml", ".txt", ".ts", ".tsx"}
    ignored_parts = {"__pycache__", "node_modules", "dist"}
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            if any(part in ignored_parts for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                errors.append(f"text file is not valid UTF-8: {path.relative_to(ROOT)}: {exc}")
                continue
            for index, line in enumerate(text.splitlines(), 1):
                if any(marker in line for marker in MOJIBAKE_MARKERS):
                    errors.append(f"possible mojibake in {path.relative_to(ROOT)}:{index}")
                    break

def main() -> int:
    errors = []
    for path in [
        APP / "package.json",
        APP / "src" / "router" / "index.js",
        APP / "src" / "data" / "course.json",
        APP / "src" / "data" / "slides.json",
        APP / "src" / "data" / "quizzes.json",
        APP / "src" / "data" / "storyboard-contract.json",
        APP / "src" / "data" / "design-contract.json",
        APP / "src" / "data" / "stitch-manifest.json",
        APP / "src" / "views" / "QuizView.vue",
        APP / "src" / "components" / "CoursePlayer.vue",
        APP / "src" / "components" / "SlideNav.vue",
        ROOT / ".agent" / "STATE.md",
        ROOT / ".agent" / "handoff" / "HANDOFF_PROTOCOL.md",
        ROOT / ".agent" / "handoff" / "CURSOR_HANDOFF.md",
        TODAY_MEMORY,
        ROOT / ".agent" / "templates" / "course-app" / "package.json",
        ROOT / ".agent" / "templates" / "course-app" / "src" / "components" / "CoursePlayer.vue",
        ROOT / ".agent" / "templates" / "course-app" / "src" / "components" / "SlideCanvas.vue",
        ROOT / ".agent" / "templates" / "course-app" / "src" / "views" / "CourseHome.vue",
        ROOT / ".agent" / "templates" / "course-app" / "src" / "views" / "QuizView.vue",
        ROOT / ".agent" / "templates" / "scripts" / "generate_audio.py",
        ROOT / ".agent" / "templates" / "scripts" / "verify_course.py",
        ROOT / "docs" / "MVP_Execution_Contract.md",
        ROOT / ".agent" / "mvp-execution-scope.json",
    ]:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
    rules_text = (ROOT / ".agent" / "rules.md").read_text(encoding="utf-8-sig") if (ROOT / ".agent" / "rules.md").exists() else ""
    if "[COMPLETION_GATE_FILE_DRIVEN]" not in rules_text:
        errors.append("missing proactive completion gate: .agent/rules.md [COMPLETION_GATE_FILE_DRIVEN]")
    course = load_json(APP / "src" / "data" / "course.json", errors)
    slides = load_json(APP / "src" / "data" / "slides.json", errors) or []
    source_slides = []
    if course:
        modules = course.get("modules", [])
        for module in modules:
            module_id = module.get("id")
            count = len([slide for slide in slides if slide.get("moduleId") == module_id])
            if module.get("slideCount") != count:
                errors.append(f"slideCount mismatch for {module_id}")
            source_root = CONTENT / module_id
            for source_name in ["course.json", "slides.json", "quizzes.json"]:
                if not (source_root / source_name).exists():
                    errors.append(f"missing source artifact: {source_root / source_name}")
            source_slides.extend(load_json(source_root / "slides.json", errors) or [])
    for slide in slides:
        for key in ["moduleId", "slideId", "route", "title", "audio", "subtitles"]:
            if not slide.get(key):
                errors.append(f"slide missing {key}: {slide}")
    public_root = APP / "public"
    for slide in slides:
        sid = slide.get("slideId", "?")
        for field in ("audio", "subtitles"):
            url = slide.get(field)
            if not isinstance(url, str) or not url.startswith("/"):
                continue
            rel = url.lstrip("/").replace("\\", "/")
            target = public_root.joinpath(*rel.split("/"))
            if not target.is_file():
                errors.append(f"missing public {field} for slide {sid}: {target.relative_to(ROOT)}")
    router = APP / "src" / "router" / "index.js"
    if router.exists():
        text = router.read_text(encoding="utf-8")
        for marker in ["/module/:moduleId/slide/:slideId", "/module/:moduleId/quiz"]:
            if marker not in text:
                errors.append(f"missing route marker: {marker}")
        if '{ path: "/module/:moduleId", redirect: "/" }' not in text:
            errors.append("module route must redirect to unified menu")
        if "component: ModuleHome" in text:
            errors.append("ModuleHome must not be used as a routed second-level menu")

    course_home = APP / "src" / "views" / "CourseHome.vue"
    if course_home.exists():
        text = course_home.read_text(encoding="utf-8")
        for marker in [
            "slidesForModule",
            "进入做题页",
            "slide.explore.route",
            "sm:grid-cols-[2.75rem_minmax(0,1fr)_5rem_8rem]",
            "shadergui-module-progress-v1",
            "progressSteps",
            "看过",
            "学过",
            "已做题",
            "掌握",
            "localStorage",
        ]:
            if marker not in text:
                errors.append(f"CourseHome missing unified menu marker: {marker}")

    course_home_template = ROOT / ".agent" / "templates" / "course-app" / "src" / "views" / "CourseHome.vue"
    if course_home_template.exists():
        text = course_home_template.read_text(encoding="utf-8")
        for marker in [
            "shadergui-module-progress-v1",
            "progressSteps",
            "setModuleProgress",
            "isStepReached",
            "localStorage",
            "看过",
            "学过",
            "已做题",
            "掌握",
        ]:
            if marker not in text:
                errors.append(f"CourseHome template missing module progress marker: {marker}")
    storyboard = load_json(APP / "src" / "data" / "storyboard-contract.json", errors)
    if storyboard and storyboard.get("status") != "storyboard_ready":
        errors.append("storyboard-contract.json must be storyboard_ready")
    if storyboard:
        for slide in storyboard.get("slides", []):
            if slide.get("visualGuidance"):
                errors.append(
                    f"storyboard must not use deprecated visualGuidance (use slides mentalModel + motionCues): "
                    f"{slide.get('moduleId')}/{slide.get('slideId')}",
                )
            if slide.get("kind") == "code":
                sid = f"{slide.get('moduleId')}/{slide.get('slideId')}"
                for cue in slide.get("motionCues") or []:
                    dg = cue.get("dynamicGuidance") or {}
                    if dg.get("primaryEffect") == "code-highlight":
                        toks = dg.get("codeHighlightTokens")
                        if not isinstance(toks, list) or not toks or not all(isinstance(t, str) and t.strip() for t in toks):
                            errors.append(
                                f"code slide motionCue must define codeHighlightTokens for code-highlight: {sid} {cue.get('cueId')}",
                            )
    design = load_json(APP / "src" / "data" / "design-contract.json", errors)
    stitch = load_json(APP / "src" / "data" / "stitch-manifest.json", errors)

    def check_contract_slide_coverage(name: str, contract: dict | None) -> None:
        if not contract:
            return
        contract_ids = {
            (slide.get("moduleId"), slide.get("slideId"))
            for slide in contract.get("slides", [])
            if slide.get("moduleId") and slide.get("slideId")
        }
        source_ids = {
            (slide.get("moduleId"), slide.get("slideId"))
            for slide in slides
            if slide.get("moduleId") and slide.get("slideId")
        }
        missing = sorted(source_ids - contract_ids)
        if missing:
            preview = ", ".join(f"{module}/{slide}" for module, slide in missing[:12])
            if len(missing) > 12:
                preview += f", ... (+{len(missing) - 12})"
            errors.append(f"{name} does not cover all generated slides: {preview}")

    check_contract_slide_coverage("storyboard-contract.json", storyboard)
    check_contract_slide_coverage("design-contract.json", design)
    check_contract_slide_coverage("stitch-manifest.json", stitch)

    for component, markers in {
        APP / "src" / "components" / "CoursePlayer.vue": [
            "storyboard-contract.json",
            "motionCues",
            "activeCue",
        ],
        APP / "src" / "components" / "SlideCanvas.vue": [
            "composition",
            "compositionBeat",
            "activeCodeFields",
            "codeHighlightTokens",
            "codeBlocks",
            "codeBlockCueClass(block)",
            "props.slide.mentalModel",
            "storyboardEmphasisText",
            "data-composition-zone",
        ],
        APP / "src" / "components" / "SlideNav.vue": [
            "subtitle-index-change",
            "activeIndex",
            'data-player-icon="pause"',
            'data-player-icon="play"',
            "目录",
            "sm:grid-cols-[1fr_auto_1fr]",
        ],
        APP / "src" / "views" / "QuizView.vue": [
            "continuePractice",
            "下一课",
            "回到菜单",
            "currentCourseRoute",
        ],
    }.items():
        if component.exists():
            text = component.read_text(encoding="utf-8")
            for marker in markers:
                if marker not in text:
                    errors.append(f"missing runtime marker in {component.relative_to(ROOT)}: {marker}")
    slide_canvas = APP / "src" / "components" / "SlideCanvas.vue"
    if slide_canvas.exists():
        text = slide_canvas.read_text(encoding="utf-8")
        for forbidden in ["bg-[#f7f6f0]", "v-if=\"slide.code\"", "compositionBeat = computed"]:
            if forbidden in text:
                errors.append(f"SlideCanvas contains regressed marker: {forbidden}")
        for forbidden in [
            "shotInstruction",
            "focusInstruction",
            "implementationHint",
            "learnerTakeaway",
            "Now focusing",
            "Mental model",
            "Learner focus",
            "先看面板职责",
        ]:
            if forbidden in text:
                errors.append(f"SlideCanvas exposes internal guidance: {forbidden}")

    for slide in [*slides, *source_slides]:
        if slide.get("kind") == "code" and any("CustomEditor" in point for point in slide.get("points", [])):
            blocks = slide.get("codeBlocks", [])
            if len(blocks) < 2:
                errors.append(f"code slide must use split codeBlocks: {slide.get('slideId')}")
            csharp_blocks = [block for block in blocks if block.get("language") == "csharp"]
            shader_blocks = [block for block in blocks if block.get("language") == "shaderlab"]
            if not csharp_blocks or not shader_blocks:
                errors.append(f"code slide must include csharp and shaderlab blocks: {slide.get('slideId')}")
            if any("CustomEditor" in block.get("code", "") for block in csharp_blocks):
                errors.append(f"C# code block must not contain CustomEditor: {slide.get('slideId')}")
            if not any("CustomEditor" in block.get("code", "") for block in shader_blocks):
                errors.append(f"ShaderLab code block must contain CustomEditor: {slide.get('slideId')}")

    mvp_mcp = ROOT / ".agent" / "mcp_servers" / "mvp_mcp.py"
    if mvp_mcp.exists():
        text = mvp_mcp.read_text(encoding="utf-8")
        for marker in [
            "<template>",
            "MVPMCP._write(app",
            "MVPMCP._write(scripts",
            "generate_audio.py\", \"\"\"",
            "verify_course.py\", \"\"\"",
        ]:
            if marker in text:
                errors.append(f"MVPMCP must assemble templates, not embed template content: {marker}")
        for marker in [".agent", "templates", "_copy_template_tree"]:
            if marker not in text:
                errors.append(f"MVPMCP missing template assembly marker: {marker}")

    for path in [
        ROOT / ".agent" / "handoff" / "HANDOFF_PROTOCOL.md",
        ROOT / ".agent" / "rules.md",
        ROOT / ".agent" / "SKILL.md",
        ROOT / "docs" / "Skill_Chain_DAG.md",
    ]:
        if path.exists() and "Small Fix Ownership" not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"missing Small Fix Ownership rule: {path.relative_to(ROOT)}")

    alignment_markers = [
        "对齐约束（必读）",
        "[AGENT_SINGLE_SOURCE]",
        "[MVP_EXECUTION_CONTRACT]",
        "[NO_INTERNAL_GUIDANCE_UI]",
        "[TOKEN_LEVEL_ANIMATION]",
        "[COURSE_HOME_ALIGNMENT_GRID]",
        "[SYNC_RULES_DAG_VERIFY]",
        "[REVERIFY_BUILD_BROWSER]",
        "[COMPLETION_GATE_FILE_DRIVEN]",
        "docs/MVP_Execution_Contract.md",
        ".agent/mvp-execution-scope.json",
        "shotInstruction",
        "focusInstruction",
        "implementationHint",
        "learnerTakeaway",
        "Now focusing",
        "verify_course.py",
        "npm run build",
    ]
    for path in [
        ROOT / ".agent" / "handoff" / "HANDOFF_PROTOCOL.md",
        ROOT / ".agent" / "rules.md",
        ROOT / ".agent" / "SKILL.md",
        ROOT / "docs" / "Skill_Chain_DAG.md",
    ]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig")
        for marker in alignment_markers:
            if marker not in text:
                errors.append(f"missing alignment constraint marker in {path.relative_to(ROOT)}: {marker}")

    check_utf8_and_mojibake(errors)
    check_mcp_content_boundary(errors)
    if errors:
        print("[FAIL] course verification failed")
        for error in errors:
            print(f" - {error}")
        return 1
    print("[OK] course verification passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
