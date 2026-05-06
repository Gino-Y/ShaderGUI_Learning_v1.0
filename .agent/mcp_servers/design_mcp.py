from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class DesignMCP:
    """Prepare a visual design contract from the course slide manifest.

    This node creates a provider-neutral design specification that defines
    layout, color scheme, and component list for each slide. It includes
    self-validation loops for contract integrity and visual reference quality.
    """

    PROVIDER = "design-v0-translated-spec"

    # Module-level color schemes (dark engineering theme)
    COLOR_SCHEMES = {
        "default": {
            "bg": "#0f172a",
            "surface": "#1e293b",  # 修复：Slate-800
            "textPrimary": "#f8fafc",
            "textSecondary": "#94a3b8",
            "accent": "#38bdf8",
            "accentSecondary": "#818cf8",
            "codeBg": "#0d1117",
            "codeKeyword": "#ff7b72",
            "codeString": "#a5d6ff",
            "codeComment": "#8b949e",
        },
    }

    # Layout templates by slide kind
    LAYOUT_TEMPLATES = {
        "concept": {
            "template": "title-body",
            "grid": "grid-cols-1",
            "spacing": "gap-6",
            "typography": {
                "title": "text-3xl font-bold",
                "subtitle": "text-lg text-slate-400",
                "body": "text-base leading-relaxed",
                "caption": "text-sm text-slate-500",
            },
        },
        "code": {
            "template": "title-code",
            "grid": "grid-cols-1",
            "spacing": "gap-4",
            "typography": {
                "title": "text-2xl font-bold",
                "body": "text-base leading-relaxed",
                "code": "text-sm font-mono",
                "annotation": "text-xs text-slate-400",
            },
        },
    }

    # Component lists by slide kind + features
    COMPONENT_SETS = {
        "concept_base": ["SlideTitle", "PointList", "SlideNav"],
        "concept_diagram": ["SlideTitle", "PointList", "DiagramPlaceholder", "SlideNav"],
        "code_base": ["SlideTitle", "CodeBlock", "PointList", "SlideNav"],
        "code_full": ["SlideTitle", "CodeBlock", "AnnotationOverlay", "PointList", "SlideNav"],
    }

    @staticmethod
    def prepare_design_contract(workspace: Path, module: str, accumulate: bool = False) -> dict:
        app = workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        if not slides_file.exists():
            return {"status": "failed", "message": "slides.json is required before design contract"}

        try:
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"invalid slides.json: {exc}"}

        storyboard_file = app / "src" / "data" / "storyboard-contract.json"
        storyboard_by_slide = {}
        storyboard_interactive_screens = []
        if storyboard_file.exists():
            try:
                storyboard = json.loads(storyboard_file.read_text(encoding="utf-8"))
                storyboard_by_slide = {
                    item.get("slideId"): item
                    for item in storyboard.get("slides", [])
                    if item.get("moduleId") == module
                }
                storyboard_interactive_screens = [
                    item
                    for item in storyboard.get("interactiveScreens", [])
                    if item.get("moduleId") == module
                ]
            except json.JSONDecodeError as exc:
                return {"status": "failed", "message": f"invalid storyboard-contract.json: {exc}"}

        v0_file = workspace / ".agent" / "v0" / module / "react-prototype.json"
        v0_handoff = {}
        if v0_file.exists():
            try:
                v0_handoff = json.loads(v0_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                return {"status": "failed", "message": f"invalid v0 react-prototype.json: {exc}"}

        module_slides = [slide for slide in slides if slide.get("moduleId") == module]
        if not module_slides:
            return {"status": "failed", "message": f"no slides found for {module}"}

        design_slides = []
        for slide in module_slides:
            slide_id = slide.get("slideId")
            title = slide.get("title", "")
            points = slide.get("points", [])
            kind = slide.get("kind", "concept")
            storyboard_slide = storyboard_by_slide.get(slide_id, {})
            # Prefer storyboard visualComposition when deriving layoutSpec.
            visual_comp = storyboard_slide.get("visualComposition") or {}
            if visual_comp:
                layout_spec = {
                    "template": "title-body" if kind == "concept" else "title-code",
                    "grid": visual_comp.get("frameGrid", {}).get("columns", "grid-cols-1"),
                    "spacing": "gap-6",
                    "typography": DesignMCP._infer_typography(visual_comp),
                    "_source": "storyboard.visualComposition",
                }
            else:
                template = DesignMCP.LAYOUT_TEMPLATES.get(kind, DesignMCP.LAYOUT_TEMPLATES["concept"])
                layout_spec = dict(template)
            # Derive colorScheme from storyboard paletteIntent when available.
            palette = storyboard_slide.get("paletteIntent") or {}
            if palette:
                color_scheme = DesignMCP._infer_color_scheme(palette)
            else:
                color_scheme = dict(DesignMCP.COLOR_SCHEMES["default"])
            # Combine storyboard motion cues and slide kind into a component list.
            motion_cues = storyboard_slide.get("motionCues", [])
            has_performance = any(
                cue.get("type") == "demo" for cue in motion_cues
            )
            if has_performance:
                component_list = list(DesignMCP.COMPONENT_SETS["concept_diagram"])
            elif kind == "code":
                src_code = ""
                if len(points) > 0:
                    # Keep current code-size heuristic until code extraction is needed.
                    pass
                if len(src_code) > 100:
                    component_list = list(DesignMCP.COMPONENT_SETS["code_full"])
                else:
                    component_list = list(DesignMCP.COMPONENT_SETS["code_base"])
            else:
                search_text = title + " " + " ".join(points)
                diagram_keywords = [
                    "图",
                    "架构",
                    "路线",
                    "流程",
                    "层级",
                    "结构",
                    "diagram",
                    "architecture",
                    "flow",
                ]
                has_diagram = any(keyword in search_text for keyword in diagram_keywords)
                if has_diagram:
                    component_list = list(DesignMCP.COMPONENT_SETS["concept_diagram"])
                else:
                    component_list = list(DesignMCP.COMPONENT_SETS["concept_base"])
            design_slides.append(
                {
                    "moduleId": module,
                    "slideId": slide_id,
                    "route": slide.get("route"),
                    "title": title,
                    "kind": kind,
                    "screenType": "course-slide-player",
                    "visualPrompt": DesignMCP._visual_prompt(title, points, storyboard_slide),
                    "v0PrototypeRef": {
                        "source": str(v0_file.relative_to(workspace)).replace("\\", "/") if v0_handoff else None,
                        "chatUrl": v0_handoff.get("chat", {}).get("url"),
                        "translationMode": "extract-layout-interaction-visual-rules-to-vue-tailwind",
                        "designRules": v0_handoff.get("extractedDesignRules", {}),
                    },
                    "storyboardRef": {
                        "source": "CourseApp/src/data/storyboard-contract.json",
                        "storyPurpose": storyboard_slide.get("storyPurpose"),
                        "layoutIntent": storyboard_slide.get("layoutIntent"),
                        "visualComposition": visual_comp,
                        "paletteIntent": palette,
                        "motionCueCount": len(motion_cues),
                    },
                    "animationHandoff": storyboard_slide.get("animationHandoff"),
                    "motionCues": storyboard_slide.get("motionCues", []),
                    "contentConstraints": [
                        "Only show ShaderGUI course content in the slide canvas.",
                        "Do not render full transcript text as a panel.",
                        "Subtitles must appear only as audio-time events.",
                        "Keep player controls outside the slide canvas.",
                        "Follow storyboard layout, palette, and motion intent before inventing new visual behavior.",
                        "Translate v0 React prototype rules into Vue and Tailwind; do not copy React/shadcn code directly.",
                    ],
                    "implementationTarget": {
                        "framework": "Vue 3",
                        "router": "Vue Router",
                        "styling": "Tailwind CSS",
                    },
                    "layoutSpec": layout_spec,
                    "colorScheme": color_scheme,
                    "componentList": component_list,
                }
            )

        design_interactive_screens = [
            DesignMCP._interactive_screen_design(module, screen, v0_file, v0_handoff)
            for screen in storyboard_interactive_screens
        ]
        out_dir = workspace / ".agent" / "design" / module
        out_dir.mkdir(parents=True, exist_ok=True)
        brief_file = out_dir / "design-brief.md"
        design_file = app / "src" / "data" / "design-contract.json"

        contract = {
            "provider": DesignMCP.PROVIDER,
            "status": "design_ready",
            "module": module,
            "generatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "source": {
                "slides": "CourseApp/src/data/slides.json",
                "storyboard": "CourseApp/src/data/storyboard-contract.json",
                "v0Prototype": str(v0_file.relative_to(workspace)).replace("\\", "/") if v0_handoff else None,
            },
            "handoffBrief": str(brief_file.relative_to(workspace)).replace("\\", "/"),
            "slides": design_slides,
            "interactiveScreens": design_interactive_screens,
            "_validation": {
                "lastContractCheck": None,
                "lastVisualRefCheck": None,
                "contractCheckAttempts": 0,
                "visualRefCheckAttempts": 0,
            },
        }
        if accumulate:
            contract = DesignMCP._merge_contract(design_file, contract, module)

        design_file.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        brief_file.write_text(DesignMCP._brief(contract), encoding="utf-8")

        return {
            "status": "success",
            "provider": DesignMCP.PROVIDER,
            "design_file": str(design_file),
            "brief_file": str(brief_file),
            "slide_count": len(design_slides),
        }

    @staticmethod
    def _merge_contract(design_file: Path, contract: dict, module: str) -> dict:
        if not design_file.exists():
            contract["module"] = "ADP_ACCUMULATED"
            return contract
        try:
            existing = json.loads(design_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            contract["module"] = "ADP_ACCUMULATED"
            return contract
        existing_slides = [
            item for item in existing.get("slides", [])
            if item.get("moduleId") != module
        ]
        existing_screens = [
            item for item in existing.get("interactiveScreens", [])
            if item.get("moduleId") != module
        ]
        contract["slides"] = sorted(
            [*existing_slides, *contract.get("slides", [])],
            key=lambda item: (item.get("moduleId", ""), item.get("slideId", "")),
        )
        contract["interactiveScreens"] = sorted(
            [*existing_screens, *contract.get("interactiveScreens", [])],
            key=lambda item: (item.get("moduleId", ""), item.get("screenId", "")),
        )
        contract["module"] = "ADP_ACCUMULATED"
        return contract

    @staticmethod
    def _infer_typography(visual_comp: dict) -> dict:
        """Derive stable Tailwind typography tokens from storyboard composition."""
        typography = {
            "title": "text-3xl font-bold",
            "subtitle": "text-lg text-slate-400",
            "body": "text-base leading-relaxed",
            "caption": "text-sm text-slate-500",
        }
        if not isinstance(visual_comp, dict) or not visual_comp:
            return typography

        frame_grid = visual_comp.get("frameGrid") if isinstance(visual_comp.get("frameGrid"), dict) else {}
        hierarchy = visual_comp.get("visualHierarchy") if isinstance(visual_comp.get("visualHierarchy"), dict) else {}
        primary = " ".join(
            str(value)
            for value in (
                visual_comp.get("primarySubject"),
                visual_comp.get("dominantZone"),
                frame_grid.get("emphasis"),
                hierarchy.get("primary"),
            )
            if value
        ).lower()

        if any(token in primary for token in ("hero", "focus", "title", "lead")):
            typography["title"] = "text-4xl font-bold"
        if any(token in primary for token in ("code", "terminal", "snippet")):
            typography["code"] = "text-sm font-mono"
            typography["annotation"] = "text-xs text-slate-400"
        return typography

    @staticmethod
    def _infer_color_scheme(palette: dict) -> dict:
        """Map storyboard palette intent onto the app's design contract colors."""
        scheme = dict(DesignMCP.COLOR_SCHEMES["default"])
        if not isinstance(palette, dict) or not palette:
            return scheme

        accent = palette.get("accent") or palette.get("accentColor") or palette.get("primaryAccent")
        secondary = palette.get("accentSecondary") or palette.get("secondaryAccent")
        bg = palette.get("bg") or palette.get("background") or palette.get("backgroundColor")
        surface = palette.get("surface") or palette.get("panel") or palette.get("panelColor")
        text = palette.get("textPrimary") or palette.get("foreground")
        muted = palette.get("textSecondary") or palette.get("muted")

        if isinstance(accent, str) and accent.startswith("#"):
            scheme["accent"] = accent
        if isinstance(secondary, str) and secondary.startswith("#"):
            scheme["accentSecondary"] = secondary
        if isinstance(bg, str) and bg.startswith("#"):
            scheme["bg"] = bg
        if isinstance(surface, str) and surface.startswith("#"):
            scheme["surface"] = surface
        if isinstance(text, str) and text.startswith("#"):
            scheme["textPrimary"] = text
        if isinstance(muted, str) and muted.startswith("#"):
            scheme["textSecondary"] = muted

        mood = str(palette.get("mood") or palette.get("tone") or "").lower()
        if "warm" in mood:
            scheme["accentSecondary"] = "#f59e0b"
        elif "calm" in mood or "focus" in mood:
            scheme["accentSecondary"] = "#22d3ee"
        return scheme

    @staticmethod
    def validate_design_contract(
        workspace: Path, module: str, design_file: str | None, accumulate: bool = False
    ) -> dict:
        """Validate the design contract structure and field coverage."""
        if not design_file:
            return {"status": "failed", "message": "design_file is None", "errors": []}

        df = Path(design_file)
        if not df.exists():
            return {"status": "failed", "message": f"{df} not found", "errors": []}

        try:
            contract = json.loads(df.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"JSON parse error: {exc}", "errors": []}

        errors = []

        # Check status
        if contract.get("status") != "design_ready":
            errors.append({
                "field": "status",
                "issue": f"expected 'design_ready', got '{contract.get('status')}'",
                "severity": "error",
            })

        # Check provider
        if not contract.get("provider"):
            errors.append({
                "field": "provider",
                "issue": "provider is empty",
                "severity": "error",
            })

        # Check slides
        slides = contract.get("slides", [])
        if not slides:
            errors.append({
                "field": "slides",
                "issue": "slides array is empty",
                "severity": "error",
            })
        else:
            for slide in slides:
                sid = slide.get("slideId", "?")
                for req_field in ("moduleId", "slideId", "visualPrompt", "contentConstraints", "implementationTarget", "storyboardRef", "motionCues", "v0PrototypeRef"):
                    if not slide.get(req_field):
                        errors.append({
                            "slideId": sid,
                            "field": req_field,
                            "issue": "missing or empty",
                            "severity": "error",
                        })
                if not slide.get("storyboardRef", {}).get("visualComposition"):
                    errors.append({
                        "slideId": sid,
                        "field": "storyboardRef.visualComposition",
                        "issue": "missing storyboard composition guidance",
                        "severity": "error",
                    })
                # Check visualPrompt length
                vp = slide.get("visualPrompt", "")
                if vp and len(vp) <= 20:
                    errors.append({
                        "slideId": sid,
                        "field": "visualPrompt",
                        "issue": f"too short ({len(vp)} chars, expected > 20)",
                        "severity": "error",
                    })
                # Check contentConstraints is non-empty array
                cc = slide.get("contentConstraints")
                if cc is not None and (not isinstance(cc, list) or len(cc) == 0):
                    errors.append({
                        "slideId": sid,
                        "field": "contentConstraints",
                        "issue": "should be a non-empty array",
                        "severity": "error",
                    })

        interactive_screens = contract.get("interactiveScreens", [])
        if not interactive_screens:
            errors.append({
                "field": "interactiveScreens",
                "issue": "interactive screen design contract is missing",
                "severity": "error",
            })
        for screen in interactive_screens:
            screen_id = screen.get("screenId", "?")
            for req_field in (
                "moduleId",
                "screenId",
                "route",
                "screenType",
                "visualPrompt",
                "storyboardRef",
                "realtimeInteractionCues",
                "runtimeGuidance",
                "componentList",
                "contentConstraints",
            ):
                if not screen.get(req_field):
                    errors.append({
                        "screenId": screen_id,
                        "field": req_field,
                        "issue": "missing or empty",
                        "severity": "error",
                    })
            if not screen.get("storyboardRef", {}).get("visualComposition"):
                errors.append({
                    "screenId": screen_id,
                    "field": "storyboardRef.visualComposition",
                    "issue": "missing storyboard composition guidance",
                    "severity": "error",
                })
            cue_actions = {cue.get("action") for cue in screen.get("realtimeInteractionCues", [])}
            if screen.get("screenType") == "course-quiz-runtime":
                for action in ("shuffle-question-bank", "shuffle-options", "select-answer", "submit-answer", "show-score"):
                    if action not in cue_actions:
                        errors.append({
                            "screenId": screen_id,
                            "field": "realtimeInteractionCues",
                            "issue": f"missing storyboard-guided action: {action}",
                            "severity": "error",
                        })
            elif screen.get("screenType") == "course-exploration-subpage":
                for action in ("load-exploration-contract", "manipulate-variable", "return-to-parent-slide"):
                    if action not in cue_actions:
                        errors.append({
                            "screenId": screen_id,
                            "field": "realtimeInteractionCues",
                            "issue": f"missing exploration action: {action}",
                            "severity": "error",
                        })

        # Check coverage against slides.json
        app = workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        if slides_file.exists():
            try:
                source_slides = json.loads(slides_file.read_text(encoding="utf-8"))
                source_ids = {
                    (s.get("moduleId"), s.get("slideId"))
                    for s in source_slides
                    if s.get("moduleId") == module and s.get("slideId")
                }
                contract_ids = {
                    (s.get("moduleId"), s.get("slideId"))
                    for s in slides
                    if s.get("moduleId") == module and s.get("slideId")
                }
                missing = source_ids - contract_ids
                extra = contract_ids - source_ids
                if missing:
                    errors.append({
                        "field": "slides.coverage",
                        "issue": f"missing slideIds: {DesignMCP._format_slide_ids(missing)}",
                        "severity": "error",
                    })
                if extra:
                    errors.append({
                        "field": "slides.coverage",
                        "issue": f"extra slideIds not in slides.json: {DesignMCP._format_slide_ids(extra)}",
                        "severity": "warning",
                    })
                if accumulate:
                    all_source_ids = {
                        (s.get("moduleId"), s.get("slideId"))
                        for s in source_slides
                        if s.get("moduleId") and s.get("slideId")
                    }
                    all_contract_ids = {
                        (s.get("moduleId"), s.get("slideId"))
                        for s in slides
                        if s.get("moduleId") and s.get("slideId")
                    }
                    accumulated_missing = all_source_ids - all_contract_ids
                    if accumulated_missing:
                        errors.append({
                            "field": "slides.accumulatedCoverage",
                            "issue": f"missing accumulated slideIds: {DesignMCP._format_slide_ids(accumulated_missing)}",
                            "severity": "error",
                        })
            except json.JSONDecodeError:
                pass  # slides.json parse error is not this method's responsibility

        fatal_errors = [error for error in errors if error.get("severity") != "warning"]
        if fatal_errors:
            return {
                "status": "failed",
                "message": f"{len(fatal_errors)} check(s) failed",
                "errors": errors,
            }
        return {"status": "success", "message": "contract validation passed", "errors": errors}

    @staticmethod
    def _format_slide_ids(ids: set[tuple[str | None, str | None]]) -> list[str]:
        return [f"{module}/{slide}" for module, slide in sorted(ids)]

    @staticmethod
    def auto_fix_design_contract(
        workspace: Path, module: str, design_file: str | None, errors: list
    ) -> dict:
        """Attempt to auto-fix fixable issues in the design contract."""
        if not design_file:
            return {"status": "success", "fixed": [], "unfixable": [e for e in errors]}

        df = Path(design_file)
        if not df.exists():
            return {"status": "success", "fixed": [], "unfixable": [e for e in errors]}

        try:
            contract = json.loads(df.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"status": "success", "fixed": [], "unfixable": [e for e in errors]}

        # Load source slides.json for reference
        app = workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        source_slides = []
        if slides_file.exists():
            try:
                source_slides = json.loads(slides_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass

        source_map = {
            s.get("slideId"): s
            for s in source_slides
            if s.get("moduleId") == module
        }

        fixed = []
        unfixable = []
        needs_rewrite = False

        for err in errors:
            severity = err.get("severity", "error")
            field = err.get("field", "")
            slide_id = err.get("slideId")

            # Fixable: missing visualPrompt
            if slide_id and field == "visualPrompt" and slide_id in source_map:
                src = source_map[slide_id]
                for slide in contract.get("slides", []):
                    if slide.get("slideId") == slide_id:
                        slide["visualPrompt"] = DesignMCP._visual_prompt(
                            src.get("title", ""), src.get("points", [])
                        )
                        fixed.append(f"{slide_id}.visualPrompt")
                        needs_rewrite = True
                        break
                continue

            # Fixable: missing contentConstraints
            if slide_id and field == "contentConstraints" and slide_id in source_map:
                for slide in contract.get("slides", []):
                    if slide.get("slideId") == slide_id:
                        slide["contentConstraints"] = [
                            "Only show ShaderGUI course content in the slide canvas.",
                            "Do not render full transcript text as a panel.",
                            "Subtitles must appear only as audio-time events.",
                            "Keep player controls outside the slide canvas.",
                            "Follow storyboard layout, palette, and motion intent before inventing new visual behavior.",
                        ]
                        fixed.append(f"{slide_id}.contentConstraints")
                        needs_rewrite = True
                        break
                continue

            # Fixable: missing slideIds (coverage gap)
            if field == "slides.coverage" and "missing" in err.get("issue", ""):
                missing_ids = source_map.keys() - {
                    s.get("slideId") for s in contract.get("slides", [])
                }
                for sid in sorted(missing_ids):
                    if sid in source_map:
                        src = source_map[sid]
                        contract["slides"].append({
                            "moduleId": module,
                            "slideId": sid,
                            "route": src.get("route"),
                            "title": src.get("title", ""),
                            "kind": src.get("kind", "concept"),
                            "screenType": "course-slide-player",
                            "visualPrompt": DesignMCP._visual_prompt(
                                src.get("title", ""), src.get("points", [])
                            ),
                            "v0PrototypeRef": {},
                            "storyboardRef": {},
                            "animationHandoff": None,
                            "motionCues": [],
                            "contentConstraints": [
                                "Only show ShaderGUI course content in the slide canvas.",
                                "Do not render full transcript text as a panel.",
                                "Subtitles must appear only as audio-time events.",
                                "Keep player controls outside the slide canvas.",
                                "Follow storyboard layout, palette, and motion intent before inventing new visual behavior.",
                            ],
                            "implementationTarget": {
                                "framework": "Vue 3",
                                "router": "Vue Router",
                                "styling": "Tailwind CSS",
                            },
                            "layoutSpec": None,
                            "colorScheme": None,
                            "componentList": None,
                        })
                        fixed.append(f"{sid} (added)")
                        needs_rewrite = True
                continue

            # Fixable: status wrong
            if field == "status":
                contract["status"] = "design_ready"
                fixed.append("status")
                needs_rewrite = True
                continue

            # Not fixable
            unfixable.append(err)

        if needs_rewrite:
            contract["_validation"]["lastContractCheck"] = (
                datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
            )
            df.write_text(
                json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        return {"status": "success", "fixed": fixed, "unfixable": unfixable}

    @staticmethod
    def generate_visual_refs(
        workspace: Path, module: str, design_file: str | None
    ) -> dict:
        """Generate visual reference specs (layout, color, components) for each slide."""
        if not design_file:
            return {"status": "failed", "message": "design_file is None", "errors": []}

        df = Path(design_file)
        if not df.exists():
            return {"status": "failed", "message": f"{df} not found", "errors": []}

        try:
            contract = json.loads(df.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"JSON parse error: {exc}", "errors": []}

        slides = contract.get("slides", [])
        if not slides:
            return {"status": "failed", "message": "slides array is empty", "errors": []}

        color_scheme = DesignMCP.COLOR_SCHEMES.get("default", DesignMCP.COLOR_SCHEMES["default"])
        errors = []
        generated = 0

        for slide in slides:
            sid = slide.get("slideId", "?")
            kind = slide.get("kind", "concept")
            has_code = bool(slide.get("visualPrompt", "") and "code" in slide.get("visualPrompt", "").lower()) or kind == "code"

            # Generate layoutSpec
            template = DesignMCP.LAYOUT_TEMPLATES.get(kind, DesignMCP.LAYOUT_TEMPLATES["concept"])
            slide["layoutSpec"] = dict(template)

            # Generate colorScheme (module-level, shared across all slides)
            slide["colorScheme"] = dict(color_scheme)

            # Generate componentList
            if kind == "concept":
                points = slide.get("title", "")
                has_diagram_keywords = any(
                    kw in points
                    for kw in ("图", "架构", "路线", "流程", "层级", "结构", "支柱", "diagram", "architecture", "flow")
                )
                if has_diagram_keywords:
                    slide["componentList"] = list(DesignMCP.COMPONENT_SETS["concept_diagram"])
                else:
                    slide["componentList"] = list(DesignMCP.COMPONENT_SETS["concept_base"])
            elif kind == "code":
                src_code = ""
                # Try to get code from slides.json
                app = workspace / "CourseApp"
                slides_file = app / "src" / "data" / "slides.json"
                if slides_file.exists():
                    try:
                        source_slides = json.loads(slides_file.read_text(encoding="utf-8"))
                        for s in source_slides:
                            if s.get("slideId") == sid and s.get("moduleId") == module:
                                src_code = s.get("code", "")
                                break
                    except json.JSONDecodeError:
                        pass

                if len(src_code) > 100:
                    slide["componentList"] = list(DesignMCP.COMPONENT_SETS["code_full"])
                else:
                    slide["componentList"] = list(DesignMCP.COMPONENT_SETS["code_base"])
            else:
                slide["componentList"] = list(DesignMCP.COMPONENT_SETS["concept_base"])

            generated += 1

        # Update validation metadata
        now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        if "_validation" not in contract:
            contract["_validation"] = {}
        contract["_validation"]["lastVisualRefCheck"] = now

        df.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        return {
            "status": "success",
            "generated": generated,
            "errors": errors,
        }

    @staticmethod
    def validate_visual_refs(
        workspace: Path, module: str, design_file: str | None
    ) -> dict:
        """Validate the visual reference specs for quality and completeness."""
        if not design_file:
            return {"status": "failed", "message": "design_file is None", "errors": []}

        df = Path(design_file)
        if not df.exists():
            return {"status": "failed", "message": f"{df} not found", "errors": []}

        try:
            contract = json.loads(df.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"JSON parse error: {exc}", "errors": []}

        slides = contract.get("slides", [])
        errors = []

        for slide in slides:
            sid = slide.get("slideId", "?")

            # Check layoutSpec
            ls = slide.get("layoutSpec")
            if ls is None:
                errors.append({
                    "slideId": sid,
                    "field": "layoutSpec",
                    "issue": "is null",
                    "severity": "error",
                })
            elif not isinstance(ls, dict):
                errors.append({
                    "slideId": sid,
                    "field": "layoutSpec",
                    "issue": "should be an object",
                    "severity": "error",
                })
            elif not all(k in ls for k in ("template", "grid", "spacing", "typography")):
                missing = [k for k in ("template", "grid", "spacing", "typography") if k not in ls]
                errors.append({
                    "slideId": sid,
                    "field": "layoutSpec",
                    "issue": f"missing keys: {missing}",
                    "severity": "error",
                })

            # Check colorScheme
            cs = slide.get("colorScheme")
            if cs is None:
                errors.append({
                    "slideId": sid,
                    "field": "colorScheme",
                    "issue": "is null",
                    "severity": "error",
                })
            elif not isinstance(cs, dict):
                errors.append({
                    "slideId": sid,
                    "field": "colorScheme",
                    "issue": "should be an object",
                    "severity": "error",
                })
            elif not all(k in cs for k in ("bg", "textPrimary", "accent")):
                missing = [k for k in ("bg", "textPrimary", "accent") if k not in cs]
                errors.append({
                    "slideId": sid,
                    "field": "colorScheme",
                    "issue": f"missing required keys: {missing}",
                    "severity": "error",
                })

            # Check componentList
            cl = slide.get("componentList")
            if cl is None:
                errors.append({
                    "slideId": sid,
                    "field": "componentList",
                    "issue": "is null",
                    "severity": "error",
                })
            elif not isinstance(cl, list) or len(cl) == 0:
                errors.append({
                    "slideId": sid,
                    "field": "componentList",
                    "issue": "should be a non-empty array of strings",
                    "severity": "error",
                })
            elif not all(isinstance(item, str) for item in cl):
                errors.append({
                    "slideId": sid,
                    "field": "componentList",
                    "issue": "all items must be strings",
                    "severity": "error",
                })

        # Update validation metadata
        now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        if "_validation" in contract:
            contract["_validation"]["lastVisualRefCheck"] = now
            df.write_text(
                json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        if errors:
            return {
                "status": "failed",
                "message": f"{len(errors)} visual ref check(s) failed",
                "errors": errors,
            }
        return {"status": "success", "message": "visual ref validation passed", "errors": []}

    @staticmethod
    def generate_diagnostic_report(
        workspace: Path,
        module: str,
        check_type: str,
        errors: list,
        retries: int,
        max_retries: int = 3,
    ) -> str:
        """Generate a diagnostic report for failed self-checks."""
        out_dir = workspace / ".agent" / "design" / module
        out_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        report_file = out_dir / f"diagnostic-report-{check_type}.md"

        check_label = {
            "contract": "contract integrity",
            "visual_ref": "visual reference",
        }.get(check_type, check_type)

        lines = [
            f"# Design Self-Check Diagnostic Report - {check_label}",
            "",
            f"- Module: {module}",
            f"- Check type: {check_label}",
            f"- Retry count: {retries}/{max_retries}",
            f"- Time: {now}",
            "",
            "## Failed Items",
            "",
            "| Slide | Field | Issue | Severity |",
            "|-------|-------|-------|----------|",
        ]

        for err in errors:
            sid = err.get("slideId", "-")
            field = err.get("field", "-")
            issue = err.get("issue", "-")
            severity = err.get("severity", "error")
            lines.append(f"| {sid} | {field} | {issue} | {severity} |")

        lines.extend([
            "",
            "## Suggested Fixes",
            "",
        ])

        if check_type == "contract":
            lines.extend([
                "1. Check that slides.json is complete and every slide has title and points.",
                "2. Re-run the design stage through flow_engine.",
                "3. If slides.json is invalid, return to the MANIFEST_READY stage.",
            ])
        elif check_type == "visual_ref":
            lines.extend([
                "1. Re-run the design stage through flow_engine.",
                "2. Check that every slide has a valid kind field: concept or code.",
                "3. If the issue persists, inspect DesignMCP templates and storyboard inputs.",
            ])

        lines.extend([
            "",
            "## Diagnostic Path",
            "",
            f"- Report: `{report_file.relative_to(workspace).as_posix()}`",
        ])

        report_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(report_file)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _visual_prompt(title: str, points: list[str], storyboard: dict | None = None) -> str:
        point_text = " / ".join(points)
        storyboard_text = ""
        if storyboard:
            layout = storyboard.get("layoutIntent", {}).get("primaryFocus")
            composition = storyboard.get("visualComposition", {})
            palette = storyboard.get("paletteIntent", {}).get("mood")
            cues = len(storyboard.get("motionCues", []))
            storyboard_text = (
                f" Storyboard intent: layout focus={layout}; palette mood={palette}; "
                f"composition={composition.get('shotType')} / {composition.get('readingDirection')}; "
                f"foreground={composition.get('foreground', {}).get('position')}; "
                f"midground={composition.get('midground', {}).get('position')}; "
                f"negative space={composition.get('negativeSpace')}; "
                f"subtitle-triggered motion cues={cues}."
            )
        return (
            "Design a focused Chinese technical course slide for Unity ShaderGUI. "
            f"Title: {title}. Key points: {point_text}. "
            f"{storyboard_text} "
            "Use the v0 React prototype as design inspiration only, translating its layout, interaction and visual rules into Vue + Tailwind. "
            "The visual should feel like a professional engineering training player: "
            "clear hierarchy, restrained controls, readable subtitles, and no internal workflow text."
        )

    @staticmethod
    def _interactive_screen_design(module: str, screen: dict, v0_file: Path, v0_handoff: dict) -> dict:
        cues = screen.get("realtimeInteractionCues", [])
        actions = ", ".join(cue.get("action", "") for cue in cues)
        if screen.get("screenType") == "exploration-subpage":
            return {
                "moduleId": module,
                "screenId": screen.get("screenId"),
                "route": screen.get("route"),
                "title": screen.get("title"),
                "screenType": "course-exploration-subpage",
                "visualPrompt": (
                    "Design the exploration as a child page of the current lesson, not as a numbered slide. "
                    "The layout must foreground manipulable controls, linked visible feedback, and a clear return path to the parent lesson. "
                    f"Realtime storyboard actions to preserve: {actions}."
                ),
                "v0PrototypeRef": {
                    "source": str(v0_file.relative_to(v0_file.parents[3])).replace("\\", "/") if v0_handoff else None,
                    "chatUrl": v0_handoff.get("chat", {}).get("url"),
                    "translationMode": "extract-exploration-subpage-rules-to-vue-tailwind",
                    "designRules": v0_handoff.get("extractedDesignRules", {}),
                },
                "storyboardRef": {
                    "source": "CourseApp/src/data/storyboard-contract.json",
                    "storyPurpose": screen.get("storyPurpose"),
                    "layoutIntent": screen.get("layoutIntent"),
                    "visualComposition": screen.get("visualComposition"),
                    "paletteIntent": screen.get("paletteIntent"),
                    "realtimeCueCount": len(cues),
                    "parentSlideId": screen.get("parentSlideId"),
                },
                "realtimeInteractionCues": cues,
                "runtimeGuidance": {
                    "target": "CourseApp/src/views/ExplorationView.vue",
                    "stateModel": screen.get("interactionHandoff", {}).get("stateModel", []),
                    "eventHandlers": screen.get("interactionHandoff", {}).get("eventHandlers", []),
                    "mustRenderFromStoryboard": True,
                },
                "componentList": [
                    "ExplorationShell",
                    "PropertyGroupingLab",
                    "LinkedFeedbackPanel",
                    "ReturnToParentSlide",
                ],
                "contentConstraints": [
                    "Exploration must not appear in slides.json and must not consume a pxx number.",
                    "The route must be a child of the parent slide route.",
                    "Interaction exists only because interaction-necessity-gate decided insert.",
                    "Provide an obvious return path to the parent lesson.",
                ],
                "implementationTarget": {
                    "framework": "Vue 3",
                    "router": "Vue Router",
                    "styling": "Tailwind CSS",
                    "data": "CourseApp/src/data/explorations.json",
                },
            }
        return {
            "moduleId": module,
            "screenId": screen.get("screenId"),
            "route": screen.get("route"),
            "title": screen.get("title", "Quiz"),
            "screenType": "course-quiz-runtime",
            "visualPrompt": (
                "Design the quiz page as a live assessment workspace. "
                "The layout must foreground the question bank table, then answer cards, then immediate result feedback. "
                f"Realtime storyboard actions to preserve: {actions}. "
                "Interactions must feel immediate and data-driven, with no page reload after answer selection, option swapping, submission, or reset."
            ),
            "v0PrototypeRef": {
                "source": str(v0_file.relative_to(v0_file.parents[3])).replace("\\", "/") if v0_handoff else None,
                "chatUrl": v0_handoff.get("chat", {}).get("url"),
                "translationMode": "extract-live-quiz-interaction-rules-to-vue-tailwind",
                "designRules": v0_handoff.get("extractedDesignRules", {}),
            },
            "storyboardRef": {
                "source": "CourseApp/src/data/storyboard-contract.json",
                "storyPurpose": screen.get("storyPurpose"),
                "layoutIntent": screen.get("layoutIntent"),
                "visualComposition": screen.get("visualComposition"),
                "paletteIntent": screen.get("paletteIntent"),
                "realtimeCueCount": len(cues),
            },
            "realtimeInteractionCues": cues,
            "runtimeGuidance": {
                "target": "CourseApp/src/views/QuizView.vue",
                "stateModel": screen.get("interactionHandoff", {}).get("stateModel", []),
                "eventHandlers": screen.get("interactionHandoff", {}).get("eventHandlers", []),
                "mustRenderFromStoryboard": True,
            },
            "componentList": [
                "QuestionBankTable",
                "QuizQuestionCard",
                "SingleChoiceInput",
                "MultipleChoiceInput",
                "OptionSwapControls",
                "SubmitAnswerButton",
                "ResultFeedback",
            ],
            "contentConstraints": [
                "Use learner-facing quiz terminology in the UI.",
                "Render storyboard realtime cues as visible guidance or behavior.",
                "Do not hard-code question rows outside quizzes.json.",
                "Keep answer identity tied to option id when options are reordered.",
                "Submission feedback must be immediate and visible.",
            ],
            "implementationTarget": {
                "framework": "Vue 3",
                "router": "Vue Router",
                "styling": "Tailwind CSS",
                "data": "CourseApp/src/data/quizzes.json",
            },
        }

    @staticmethod
    def _brief(contract: dict) -> str:
        lines = [
            "# Design Brief",
            "",
            f"- Provider mode: `{contract['provider']}`",
            f"- Module: `{contract['module']}`",
            f"- Source: `{contract['source']}`",
            "- Goal: Generate or refine high-fidelity course-player UI screens for the Vue SPA.",
            "- Storyboard source: `CourseApp/src/data/storyboard-contract.json`.",
            "- v0 source: `.agent/v0/<module>/react-prototype.json`; translate design rules, do not copy React code directly.",
            "- Hard rule: Course production workflow text must not appear inside course slides.",
            "- Hard rule: Full transcripts are production material only; the runtime shows subtitles from audio events.",
            "- Hard rule: Motion cues are described for the future web animation module and triggered from subtitle events.",
            "",
            "## Screens",
            "",
        ]
        for slide in contract["slides"]:
            lines.extend(
                [
                    f"### {slide['moduleId']} / {slide['slideId']}",
                    "",
                    f"- Route: `{slide['route']}`",
                    f"- Title: {slide['title']}",
                    f"- Kind: {slide.get('kind', 'concept')}",
                    f"- Prompt: {slide['visualPrompt']}",
                    f"- v0 chat: {slide.get('v0PrototypeRef', {}).get('chatUrl')}",
                    f"- Story purpose: {slide.get('storyboardRef', {}).get('storyPurpose')}",
                    f"- Motion cues: {len(slide.get('motionCues', []))}",
                    "- Constraints:",
                ]
            )
            lines.extend([f"  - {item}" for item in slide["contentConstraints"]])

            layout = slide.get("layoutSpec")
            if layout:
                lines.extend([
                    "",
                    "- Layout:",
                    f"  - Template: {layout.get('template')}",
                    f"  - Grid: {layout.get('grid')}",
                    f"  - Spacing: {layout.get('spacing')}",
                ])

            components = slide.get("componentList")
            if components:
                lines.extend([
                    "",
                    f"- Components: {', '.join(components)}",
                ])

            lines.append("")

        if contract.get("interactiveScreens"):
            lines.extend(["## Interactive Screens", ""])
            for screen in contract["interactiveScreens"]:
                lines.extend(
                    [
                        f"### {screen['screenId']} - {screen['title']}",
                        "",
                        f"- Route: `{screen['route']}`",
                        f"- Prompt: {screen['visualPrompt']}",
                        f"- Story purpose: {screen.get('storyboardRef', {}).get('storyPurpose')}",
                        f"- Realtime cues: {len(screen.get('realtimeInteractionCues', []))}",
                        f"- Runtime target: `{screen.get('runtimeGuidance', {}).get('target')}`",
                        f"- Components: {', '.join(screen.get('componentList', []))}",
                        "- Constraints:",
                    ]
                )
                lines.extend([f"  - {item}" for item in screen.get("contentConstraints", [])])
                lines.append("")

        validation = contract.get("_validation", {})
        if validation:
            lines.extend([
                "## Validation History",
                "",
                f"- Last contract check: {validation.get('lastContractCheck', 'N/A')}",
                f"- Last visual ref check: {validation.get('lastVisualRefCheck', 'N/A')}",
                f"- Contract check attempts: {validation.get('contractCheckAttempts', 0)}",
                f"- Visual ref check attempts: {validation.get('visualRefCheckAttempts', 0)}",
                "",
            ])

        return "\n".join(lines)
