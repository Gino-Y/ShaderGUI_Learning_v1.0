from __future__ import annotations

import itertools
import json
import re
from datetime import datetime
from pathlib import Path

# Import visual spec builder


class StoryboardMCP:
    """Create the narrative storyboard contract before visual design.

    The storyboard is the film-industry layer of the course DAG: it defines
    scene intent, layout emphasis, palette intent, and subtitle-driven motion
    cues before DesignMCP turns those choices into concrete visual specs.
    """

    PROVIDER = "storyboard-local-spec"

    @staticmethod
    def prepare_storyboard_contract(workspace: Path, module: str) -> dict:
        app = workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        explorations_file = app / "src" / "data" / "explorations.json"
        quizzes_file = app / "src" / "data" / "quizzes.json"
        if not slides_file.exists():
            return {"status": "failed", "message": "slides.json is required before storyboard contract"}

        try:
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
            explorations = json.loads(explorations_file.read_text(encoding="utf-8")) if explorations_file.exists() else []
            quizzes = json.loads(quizzes_file.read_text(encoding="utf-8")) if quizzes_file.exists() else []
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"invalid storyboard source JSON: {exc}"}

        module_slides = [slide for slide in slides if slide.get("moduleId") == module]
        if not module_slides:
            return {"status": "failed", "message": f"no slides found for {module}"}

        storyboard_slides = []
        for index, slide in enumerate(module_slides):
            slide_id = slide.get("slideId")
            title = slide.get("title", "")
            points = slide.get("points", [])
            kind = slide.get("kind", "concept")
            subtitle_path = slide.get("subtitles")
            
            storyboard_slides.append(
                {
                    "moduleId": module,
                    "slideId": slide_id,
                    "route": slide.get("route"),
                    "title": title,
                    "kind": kind,
                    "sceneIndex": index,
                    "storyPurpose": StoryboardMCP._story_purpose(title, points),
                    "layoutIntent": StoryboardMCP._layout_intent(kind, points),
                    "visualComposition": StoryboardMCP._visual_composition(kind, title, points, index),
                    "paletteIntent": StoryboardMCP._palette_intent(kind),
                    "motionCues": motion_cues,
                    "animationHandoff": {
                        "target": "future-web-animation-module",
                        "triggerSource": "subtitle-events",
                        "subtitleEventPath": subtitle_path,
                        "bindingMode": "subtitle-time-range-with-knowledge-alignment",
                        "notes": [
                            "Each cue binds to a concrete subtitle start/end range when subtitle events exist.",
                            "Knowledge points are aligned to the closest subtitle segment by keyword overlap, with ordered fallback.",
                        ],
                    },
                    "designDirectives": [
                        "Storyboard intent must guide layout hierarchy, color emphasis, and motion pacing.",
                        "Course production workflow text must not appear in the learner-facing slide canvas.",
                        "Animations must serve comprehension of teaching content, not decorative spectacle.",
                    ],
                }
            )

        embedded_explorations = []
        for slide in module_slides:
            explore = slide.get("explore")
            if not explore:
                continue
            embedded_explorations.append(
                {
                    "moduleId": module,
                    "parentSlideId": slide.get("slideId"),
                    "explorationId": explore.get("id") or explore.get("component", "explore"),
                    "route": explore.get("route"),
                    "title": explore.get("title"),
                    "component": explore.get("component"),
                    "points": slide.get("points", []),
                }
            )
        exploration_items = StoryboardMCP._dedupe_explorations([*explorations, *embedded_explorations])
        interactive_screens = StoryboardMCP._interactive_screens(module, quizzes, exploration_items)
        out_dir = workspace / ".agent" / "storyboard" / module
        out_dir.mkdir(parents=True, exist_ok=True)
        brief_file = out_dir / "storyboard-brief.md"
        storyboard_file = app / "src" / "data" / "storyboard-contract.json"

        contract = {
            "provider": StoryboardMCP.PROVIDER,
            "status": "storyboard_ready",
            "module": module,
            "generatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "source": {
                "slides": "CourseApp/src/data/slides.json",
                "explorations": "CourseApp/src/data/explorations.json" if explorations_file.exists() else None,
                "quizzes": "CourseApp/src/data/quizzes.json" if quizzes_file.exists() else None,
            },
            "handoffBrief": str(brief_file.relative_to(workspace)).replace("\\", "/"),
            "slides": storyboard_slides,
            "interactiveScreens": interactive_screens,
            "_validation": {
                "lastStoryboardCheck": None,
                "cueBindingPolicy": "subtitle segment indexes bind to concrete timecodes after audio generation",
                "realtimeInteractionPolicy": "user actions and state changes bind to concrete Vue event handlers in QuizView",
            },
        }

        storyboard_file.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        brief_file.write_text(StoryboardMCP._brief(contract), encoding="utf-8")

        return {
            "status": "success",
            "provider": StoryboardMCP.PROVIDER,
            "storyboard_file": str(storyboard_file),
            "brief_file": str(brief_file),
            "slide_count": len(storyboard_slides),
            "interactive_screen_count": len(interactive_screens),
        }

    @staticmethod
    def _dedupe_explorations(explorations: list[dict]) -> list[dict]:
        deduped = []
        seen = set()
        for item in explorations:
            key = (
                item.get("moduleId"),
                item.get("parentSlideId"),
                item.get("route"),
                item.get("explorationId") or item.get("id") or item.get("component"),
            )
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
        return deduped

    @staticmethod
    def validate_storyboard_contract(workspace: Path, module: str, storyboard_file: str | None) -> dict:
        if not storyboard_file:
            return {"status": "failed", "message": "storyboard_file is None", "errors": []}

        sf = Path(storyboard_file)
        if not sf.exists():
            return {"status": "failed", "message": f"{sf} not found", "errors": []}

        try:
            contract = json.loads(sf.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "failed", "message": f"JSON parse error: {exc}", "errors": []}

        errors = []
        if contract.get("status") != "storyboard_ready":
            errors.append({"field": "status", "issue": "expected storyboard_ready", "severity": "error"})
        if not contract.get("provider"):
            errors.append({"field": "provider", "issue": "provider is empty", "severity": "error"})

        slides = contract.get("slides", [])
        interactive_screens = contract.get("interactiveScreens", [])
        if not slides:
            errors.append({"field": "slides", "issue": "slides array is empty", "severity": "error"})
        for slide in slides:
            sid = slide.get("slideId", "?")
            for req_field in (
                "moduleId",
                "slideId",
                "storyPurpose",
                "layoutIntent",
                "paletteIntent",
                "visualComposition",
                "motionCues",
                "animationHandoff",
                "designDirectives",
            ):
                if not slide.get(req_field):
                    errors.append({"slideId": sid, "field": req_field, "issue": "missing or empty", "severity": "error"})
            if slide.get("visualGuidance"):
                errors.append({
                    "slideId": sid,
                    "field": "visualGuidance",
                    "issue": "deprecated: use slides.json mentalModel + motionCues for emphasis",
                    "severity": "error",
                })
            composition = slide.get("visualComposition", {})
            for req_field in ("aspectRatio", "shotType", "frameGrid", "foreground", "midground", "background", "negativeSpace", "readingDirection", "safeArea", "cameraPlan"):
                if not composition.get(req_field):
                    errors.append({"slideId": sid, "field": f"visualComposition.{req_field}", "issue": "missing or empty", "severity": "error"})
            last_start = -1.0
            for cue in slide.get("motionCues", []):
                for req_field in (
                    "cueId",
                    "trigger",
                    "timeRange",
                    "target",
                    "contentBeat",
                    "sourceSubtitleText",
                    "knowledgeFocus",
                    "animation",
                    "dynamicGuidance",
                    "compositionBeat",
                    "shotInstruction",
                    "focusInstruction",
                    "implementationHint",
                    "purpose",
                ):
                    if not cue.get(req_field):
                        errors.append({
                            "slideId": sid,
                            "field": f"motionCues.{req_field}",
                            "issue": "missing or empty",
                            "severity": "error",
                        })
                trigger = cue.get("trigger", {})
                if trigger.get("type") != "subtitle-segment":
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.trigger.type",
                        "issue": "must be subtitle-segment",
                        "severity": "error",
                    })
                if trigger.get("timecode") is None:
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.trigger.timecode",
                        "issue": "must bind to a concrete subtitle start time",
                        "severity": "error",
                    })
                time_range = cue.get("timeRange", {})
                start = time_range.get("start")
                end = time_range.get("end")
                duration_ms = time_range.get("durationMs")
                if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end <= start:
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.timeRange",
                        "issue": "must define numeric start/end with end > start",
                        "severity": "error",
                    })
                elif start < last_start:
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.timeRange",
                        "issue": "cue start times must be monotonically increasing",
                        "severity": "error",
                    })
                else:
                    last_start = float(start)
                if not isinstance(duration_ms, int) or duration_ms <= 0:
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.timeRange.durationMs",
                        "issue": "must be a positive integer",
                        "severity": "error",
                    })
                knowledge = cue.get("knowledgeFocus", {})
                if not knowledge.get("label") or not knowledge.get("learnerTakeaway"):
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.knowledgeFocus",
                        "issue": "must bind cue to current knowledge point and learner takeaway",
                        "severity": "error",
                    })
                guidance = cue.get("dynamicGuidance", {})
                if guidance.get("primaryEffect") not in {"knowledge-highlight", "code-highlight"}:
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.dynamicGuidance.primaryEffect",
                        "issue": "must define a supported highlight effect",
                        "severity": "error",
                    })
                if not guidance.get("attentionPattern") or not guidance.get("highlightTarget"):
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.dynamicGuidance",
                        "issue": "must define attention pattern and highlight target",
                        "severity": "error",
                    })
                composition_beat = cue.get("compositionBeat", {})
                for req_field in ("frameZone", "subject", "cameraAction", "spatialChange", "continuityRule"):
                    if not composition_beat.get(req_field):
                        errors.append({
                            "slideId": sid,
                            "field": f"motionCues.compositionBeat.{req_field}",
                            "issue": "must define concrete composition guidance per cue",
                            "severity": "error",
                        })
                timing = guidance.get("timing", {})
                if not all(isinstance(timing.get(key), (int, float)) for key in ("start", "peak", "settle")):
                    errors.append({
                        "slideId": sid,
                        "field": "motionCues.dynamicGuidance.timing",
                        "issue": "must define numeric start, peak, and settle values",
                        "severity": "error",
                    })
                if slide.get("kind") == "code" and guidance.get("primaryEffect") == "code-highlight":
                    cht = guidance.get("codeHighlightTokens")
                    if not isinstance(cht, list) or len(cht) == 0:
                        errors.append({
                            "slideId": sid,
                            "field": "motionCues.dynamicGuidance.codeHighlightTokens",
                            "issue": "code slides must list non-empty codeHighlightTokens per code-highlight cue",
                            "severity": "error",
                        })
                    elif not all(isinstance(t, str) and t.strip() for t in cht):
                        errors.append({
                            "slideId": sid,
                            "field": "motionCues.dynamicGuidance.codeHighlightTokens",
                            "issue": "codeHighlightTokens must be non-empty strings",
                            "severity": "error",
                        })

        if not interactive_screens:
            errors.append({"field": "interactiveScreens", "issue": "做题页实时互动故事板缺失", "severity": "error"})
        for screen in interactive_screens:
            screen_id = screen.get("screenId", "?")
            for req_field in (
                "moduleId",
                "screenId",
                "route",
                "screenType",
                "storyPurpose",
                "layoutIntent",
                "paletteIntent",
                "visualComposition",
                "realtimeInteractionCues",
                "interactionHandoff",
                "designDirectives",
            ):
                if not screen.get(req_field):
                    errors.append({"screenId": screen_id, "field": req_field, "issue": "missing or empty", "severity": "error"})
            composition = screen.get("visualComposition", {})
            for req_field in ("aspectRatio", "shotType", "frameGrid", "foreground", "midground", "background", "negativeSpace", "readingDirection", "safeArea", "cameraPlan"):
                if not composition.get(req_field):
                    errors.append({"screenId": screen_id, "field": f"visualComposition.{req_field}", "issue": "missing or empty", "severity": "error"})
            cue_actions = {cue.get("action") for cue in screen.get("realtimeInteractionCues", [])}
            if screen.get("screenType") == "realtime-quiz":
                for action in ("shuffle-question-bank", "shuffle-options", "select-answer", "submit-answer", "show-score"):
                    if action not in cue_actions:
                        errors.append({"screenId": screen_id, "field": "realtimeInteractionCues", "issue": f"missing action: {action}", "severity": "error"})
            elif screen.get("screenType") == "exploration-subpage":
                for action in ("load-exploration-contract", "manipulate-variable", "return-to-parent-slide"):
                    if action not in cue_actions:
                        errors.append({"screenId": screen_id, "field": "realtimeInteractionCues", "issue": f"missing action: {action}", "severity": "error"})
            for cue in screen.get("realtimeInteractionCues", []):
                trigger = cue.get("trigger", {})
                if trigger.get("type") not in {"page-load", "user-action", "state-change"}:
                    errors.append({"screenId": screen_id, "field": "realtimeInteractionCues.trigger.type", "issue": "invalid realtime trigger", "severity": "error"})

        slides_file = workspace / "CourseApp" / "src" / "data" / "slides.json"
        if slides_file.exists():
            try:
                source_slides = json.loads(slides_file.read_text(encoding="utf-8"))
                source_ids = {s.get("slideId") for s in source_slides if s.get("moduleId") == module}
                storyboard_ids = {s.get("slideId") for s in slides}
                missing = source_ids - storyboard_ids
                extra = storyboard_ids - source_ids
                if missing:
                    errors.append({"field": "slides.coverage", "issue": f"missing slideIds: {sorted(missing)}", "severity": "error"})
                if extra:
                    errors.append({"field": "slides.coverage", "issue": f"extra slideIds: {sorted(extra)}", "severity": "warning"})
            except json.JSONDecodeError:
                pass

        if "_validation" in contract:
            contract["_validation"]["lastStoryboardCheck"] = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
            sf.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if errors:
            return {"status": "failed", "message": f"{len(errors)} storyboard check(s) failed", "errors": errors}
        return {"status": "success", "message": "storyboard validation passed", "errors": []}

    @staticmethod
    def _story_purpose(title: str, points: list[str]) -> str:
        point_text = " / ".join(points[:3])
        return f"Use this scene to make learners understand '{title}' through the content beats: {point_text}."

    @staticmethod
    def _layout_intent(kind: str, points: list[str]) -> dict:
        if kind == "code":
            return {
                "primaryFocus": "code structure and callout annotations",
                "readingPath": "title -> code block -> highlighted risk or principle -> supporting bullets",
                "density": "medium",
                "emphasis": points[:2],
            }
        return {
            "primaryFocus": "concept hierarchy and mental model",
            "readingPath": "title -> core idea -> three supporting beats",
            "density": "low-to-medium",
            "emphasis": points[:3],
        }

    @staticmethod
    def _visual_composition(kind: str, title: str, points: list[str], scene_index: int) -> dict:
        if kind == "code":
            return {
                "aspectRatio": "16:9 responsive canvas, preserve 7% outer safe margin",
                "shotType": "medium-wide technical board shot",
                "frameGrid": {
                    "columns": "left 48% teaching beats, right 52% code panel",
                    "rows": "top title band, middle explanation/code body, bottom learner focus strip",
                    "anchor": "code panel occupies the right visual weight; title anchors upper-left",
                },
                "foreground": {
                    "subject": "current code fragment and active callout",
                    "position": "right-center, inside high-contrast code panel",
                    "scale": "dominant but not full-screen; code remains readable at laptop viewport",
                },
                "midground": {
                    "subject": "three principle cards or point cards",
                    "position": "left-center stacked vertical rhythm",
                    "role": "support the code fragment with conceptual labels",
                },
                "background": {
                    "subject": "subtle dark engineering surface and radial accent glow",
                    "position": "full frame, lowest contrast",
                    "role": "create depth without competing with code",
                },
                "negativeSpace": "reserve quiet space between left cards and right code so callout motion has room",
                "readingDirection": "upper-left title -> left point stack -> right active code fragment -> bottom takeaway",
                "safeArea": "keep subtitles and player controls outside the slide canvas composition",
                "cameraPlan": {
                    "base": "locked camera, no scene-wide zoom",
                    "beatMotion": "micro-pan attention from left point to right code callout",
                    "avoid": ["whole-card bouncing", "large decorative camera moves", "text crossing subtitle area"],
                },
            }
        return {
            "aspectRatio": "16:9 responsive canvas, preserve 7% outer safe margin",
            "shotType": "wide instructional concept board",
            "frameGrid": {
                "columns": "left 56% hero concept and explanation, right 44% supporting cards",
                "rows": "top metadata band, center concept body, bottom learner focus",
                "anchor": "hero concept anchors upper-left; supporting beats form right-side vertical rhythm",
            },
            "foreground": {
                "subject": points[0] if points else title,
                "position": "left-center hero area",
                "scale": "largest text block after title; primary learner attention",
            },
            "midground": {
                "subject": "secondary point cards",
                "position": "right-center, staggered stack",
                "role": "show the sequence of supporting ideas",
            },
            "background": {
                "subject": "soft radial highlights and dark glass panels",
                "position": "corners and far background",
                "role": "separate layers without becoming content",
            },
            "negativeSpace": "leave a quiet diagonal corridor from title to focus card for eye travel",
            "readingDirection": "upper-left title -> left hero concept -> right supporting cards -> bottom focus statement",
            "safeArea": "keep subtitle overlay and player controls outside the composed slide frame",
            "cameraPlan": {
                "base": "locked camera with stable slide geometry",
                "beatMotion": "progressive emphasis on the current point card only",
                "avoid": ["layout reflow during narration", "large parallax shifts", "decorative motion unrelated to current knowledge point"],
            },
        }

    @staticmethod
    def _palette_intent(kind: str) -> dict:
        if kind == "code":
            return {
                "mood": "precise, technical, focused",
                "contrastRole": "use accent color only for the currently explained code fragment",
                "avoid": ["decorative gradients", "high-saturation backgrounds", "workflow labels"],
            }
        return {
            "mood": "clear, instructional, confident",
            "contrastRole": "use accent color to separate principle, example, and learner takeaway",
            "avoid": ["monochrome sameness", "presentation decoration", "workflow labels"],
        }

    @staticmethod
    def _code_highlight_tokens(kind: str, index: int) -> list[str]:
        """Per-beat substring tokens for token-level code emphasis (longest match first for the runtime splitter)."""
        if kind != "code":
            return []
        by_index: dict[int, list[str]] = {
            0: [
                "MaterialProperty",
                "ShaderProperty",
                "MaterialEditor",
                "FindProperty",
                "ShaderGUI",
                "OnGUI",
                "override",
            ],
            1: [
                "CustomEditor",
                "Properties",
                "_BaseColor",
                "MyShader",
                "Shader",
            ],
            2: [
                "ShaderProperty",
                "MaterialProperty",
                "FindProperty",
                "MaterialEditor",
                "OnGUI",
                "editor",
            ],
        }
        tokens = list(by_index.get(index, []))
        tokens.sort(key=len, reverse=True)
        return tokens

    @staticmethod
    def _motion_cues(workspace: Path, kind: str, points: list[str], subtitle_path: str | None) -> list[dict]:
        subtitle_events = StoryboardMCP._load_subtitle_events(workspace, subtitle_path)
        alignments = StoryboardMCP._align_points_to_subtitles(points[:4], subtitle_events)
        cues = []
        for index, point in enumerate(points[:4]):
            event = alignments[index] if index < len(alignments) else None
            start = float(event.get("start", 0.0)) if event else 0.0
            end = float(event.get("end", start + 1.8)) if event else start + 1.8
            duration_ms = max(1, int(round((end - start) * 1000)))
            source_text = event.get("text", "") if event else point
            focus_id = f"knowledge-{index + 1:02d}"
            highlight_target = "code-callout" if kind == "code" else "point-card"
            primary_effect = "code-highlight" if kind == "code" else "knowledge-highlight"
            animation = {
                "name": "reveal-focus" if kind != "code" else "code-callout-focus",
                "durationMs": 420 if index == 0 else 360,
                "easing": "ease-out",
                "parameters": {
                    "opacity": [0, 1],
                    "translateY": [12, 0],
                    "highlight": kind == "code",
                },
            }
            code_tokens = StoryboardMCP._code_highlight_tokens(kind, index)
            dynamic_guidance: dict = {
                "primaryEffect": primary_effect,
                "attentionPattern": "pulse-once-then-hold" if index == 0 else "soft-blink-then-hold",
                "highlightTarget": highlight_target,
                "highlightText": point,
                "deEmphasizeOthers": True,
                "timing": {
                    "start": round(start, 2),
                    "peak": round(start + (end - start) * 0.4, 2),
                    "settle": round(end, 2),
                    "policy": "start at subtitle segment start, peak in first 40%, settle at segment end",
                },
                "visualTreatment": {
                    "accent": "emerald" if kind == "code" else "cyan",
                    "glow": True,
                    "blink": index > 0,
                    "outline": True,
                },
            }
            if code_tokens:
                dynamic_guidance["codeHighlightTokens"] = code_tokens
            cues.append(
                {
                    "cueId": f"cue-{index + 1:02d}",
                    "trigger": {
                        "type": "subtitle-segment",
                        "segmentIndex": event.get("segmentIndex", index) if event else index,
                        "subtitleEventPath": subtitle_path,
                        "subtitleEventId": event.get("id") if event else None,
                        "timecode": start,
                    },
                    "timeRange": {
                        "start": round(start, 2),
                        "end": round(end, 2),
                        "durationMs": duration_ms,
                    },
                    "target": "code-callout" if kind == "code" else "content-beat",
                    "contentBeat": point,
                    "sourceSubtitleText": source_text,
                    "knowledgeFocus": {
                        "id": focus_id,
                        "label": point,
                        "source": "slide.points",
                        "semanticRole": "code-step" if kind == "code" else "concept-beat",
                        "learnerTakeaway": f"当前应聚焦理解：{point}",
                    },
                    "animation": animation,
                    "dynamicGuidance": dynamic_guidance,
                    "compositionBeat": StoryboardMCP._composition_beat(kind, index, point, highlight_target),
                    "shotInstruction": StoryboardMCP._shot_instruction(kind, point, source_text, start, end),
                    "focusInstruction": {
                        "focus": point,
                        "deEmphasize": "other point cards and non-current code callouts",
                        "learnerAction": "follow the highlighted knowledge point while the matching narration plays",
                    },
                    "implementationHint": {
                        "componentRegion": "SlideCanvas",
                        "targetSelector": highlight_target,
                        "binding": "subtitle timeRange drives visual emphasis and compositionBeat drives frame-zone emphasis",
                        "runtimeStatus": "implemented-by-SlideCanvas-activeCue-and-visualComposition",
                    },
                    "purpose": "Synchronize visual emphasis with the spoken teaching beat.",
                }
            )
        return cues

    @staticmethod
    def _load_subtitle_events(workspace: Path, subtitle_path: str | None) -> list[dict]:
        if not subtitle_path:
            return []
        path = workspace / "CourseApp" / "public" / subtitle_path.lstrip("/")
        if not path.exists():
            return []
        try:
            events = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        normalized = []
        for index, event in enumerate(events if isinstance(events, list) else []):
            try:
                start = float(event.get("start"))
                end = float(event.get("end"))
            except (TypeError, ValueError):
                continue
            if end <= start:
                continue
            normalized.append(
                {
                    "id": event.get("id", f"s{index:02d}"),
                    "segmentIndex": index,
                    "start": start,
                    "end": end,
                    "text": str(event.get("text", "")),
                }
            )
        return normalized

    @staticmethod
    def _align_points_to_subtitles(points: list[str], subtitle_events: list[dict]) -> list[dict | None]:
        if not points:
            return []
        if not subtitle_events:
            return [None for _ in points]
        if len(subtitle_events) < len(points):
            return [subtitle_events[min(index, len(subtitle_events) - 1)] for index, _ in enumerate(points)]

        best_combo = None
        best_score = -1.0
        for combo in itertools.combinations(range(len(subtitle_events)), len(points)):
            score = sum(
                StoryboardMCP._text_match_score(point, subtitle_events[event_index].get("text", ""))
                for point, event_index in zip(points, combo)
            )
            # Prefer earlier, stable matches when scores are equal.
            score -= sum(combo) * 0.001
            if score > best_score:
                best_score = score
                best_combo = combo
        return [subtitle_events[index] for index in (best_combo or range(len(points)))]

    @staticmethod
    def _text_match_score(point: str, subtitle_text: str) -> float:
        point_tokens = StoryboardMCP._keywords(point)
        subtitle_tokens = StoryboardMCP._keywords(subtitle_text)
        if not point_tokens or not subtitle_tokens:
            return 0.0
        overlap = point_tokens & subtitle_tokens
        char_overlap = set(point) & set(subtitle_text)
        return (len(overlap) * 3.0) + (len(char_overlap) / max(1, len(set(point))))

    @staticmethod
    def _keywords(text: str) -> set[str]:
        latin = {item.lower() for item in re.findall(r"[A-Za-z][A-Za-z0-9_#]*", text)}
        chinese = re.findall(r"[\u4e00-\u9fff]{2,}", text)
        tokens = set(latin)
        for chunk in chinese:
            tokens.add(chunk)
            tokens.update(chunk[index : index + 2] for index in range(max(0, len(chunk) - 1)))
            tokens.update(chunk[index : index + 3] for index in range(max(0, len(chunk) - 2)))
        return tokens

    @staticmethod
    def _composition_beat(kind: str, index: int, point: str, highlight_target: str) -> dict:
        if kind == "code":
            zones = ["right code panel upper third", "right code panel middle third", "right code panel lower third", "left principle stack"]
            return {
                "frameZone": zones[index % len(zones)],
                "subject": point,
                "cameraAction": "locked frame; move only callout glow and local code highlight",
                "spatialChange": f"shift visual weight toward {highlight_target} while keeping title and navigation static",
                "continuityRule": "do not reflow code; preserve code panel position across all beats",
            }
        zones = ["left hero concept", "right support card top", "right support card middle", "right support card bottom"]
        return {
            "frameZone": zones[index % len(zones)],
            "subject": point,
            "cameraAction": "locked frame; reveal or pulse the current card in place",
            "spatialChange": f"raise contrast on {highlight_target} and dim sibling cards",
            "continuityRule": "keep hero title, card stack, and background fixed so learners perceive a stable board",
        }

    @staticmethod
    def _shot_instruction(kind: str, point: str, subtitle_text: str, start: float, end: float) -> str:
        target = "代码标注区域" if kind == "code" else "知识点卡片"
        clean_subtitle = subtitle_text.rstrip("。！？.!?")
        narration = f"旁白：{clean_subtitle}" if clean_subtitle else "旁白段落未解析"
        return (
            f"{start:.2f}s-{end:.2f}s 保持标题和主体结构稳定，"
            f"将{target}切到当前焦点“{point}”，弱化其他内容；{narration}。"
        )

    @staticmethod
    def _interactive_screens(module: str, quizzes: list[dict], explorations: list[dict] | None = None) -> list[dict]:
        screens = []
        for exploration in explorations or []:
            if exploration.get("moduleId") != module:
                continue
            screen_id = f"explore-{exploration.get('parentSlideId')}-{exploration.get('explorationId')}"
            screens.append(
                {
                    "moduleId": module,
                    "screenId": screen_id,
                    "route": exploration.get("route"),
                    "title": exploration.get("title"),
                    "screenType": "exploration-subpage",
                    "parentSlideId": exploration.get("parentSlideId"),
                    "storyPurpose": "Let learners manipulate ShaderGUI property grouping variables as a subpage of the current lesson, without consuming a main slide number.",
                    "layoutIntent": {
                        "primaryFocus": "interactive property grouping lab",
                        "readingPath": "parent lesson -> exploration controls -> linked feedback -> return to lesson",
                        "density": "medium",
                        "emphasis": exploration.get("points", []),
                    },
                    "visualComposition": {
                        "aspectRatio": "full viewport lab surface with 7% safe margin",
                        "shotType": "wide interactive workbench",
                        "frameGrid": {
                            "columns": "left controls 36%, right live material-panel feedback 64%",
                            "rows": "breadcrumb/header, interactive body, return affordance",
                            "anchor": "live feedback panel is the visual center; controls stay left",
                        },
                        "foreground": {"subject": "active lab controls", "position": "left-center", "scale": "touch-friendly controls"},
                        "midground": {"subject": "material panel preview and code snippet", "position": "right-center", "role": "show immediate consequence"},
                        "background": {"subject": "dark neutral lab shell", "position": "full frame", "role": "keep focus on interactive cause/effect"},
                        "negativeSpace": "space between controls and feedback prevents the lab from feeling like a form",
                        "readingDirection": "breadcrumb -> controls -> live feedback -> return to lesson",
                        "safeArea": "no content under footer/player controls; keep return path visible",
                        "cameraPlan": {"base": "locked wide frame", "beatMotion": "feedback regions update in place", "avoid": ["modal overlays", "hidden return navigation"]},
                    },
                    "paletteIntent": {
                        "mood": "focused, experimental, immediate",
                        "contrastRole": "use emerald for active controls and cyan for linked feedback",
                        "avoid": ["standalone slide numbering", "audio transcript panel", "decorative-only interaction"],
                    },
                    "realtimeInteractionCues": [
                        {
                            "cueId": "explore-cue-01",
                            "trigger": {"type": "page-load", "event": "exploration-mounted"},
                            "action": "load-exploration-contract",
                            "target": exploration.get("component"),
                        "runtimeBinding": "slides.json explore + concept-model.json",
                            "feedback": "Render the lab as a child route of the parent lesson.",
                            "purpose": "Keep exploration outside the pxx slide sequence.",
                        },
                        {
                            "cueId": "explore-cue-02",
                            "trigger": {"type": "user-action", "event": "input"},
                            "action": "manipulate-variable",
                            "target": "lab-controls",
                            "runtimeBinding": "PropertyGroupingLab local state",
                            "feedback": "Visible properties, risk level, explanation, and code snippet update immediately.",
                            "purpose": "Show why grouping and conditional display reduce cognitive load.",
                        },
                        {
                            "cueId": "explore-cue-03",
                            "trigger": {"type": "user-action", "event": "click"},
                            "action": "return-to-parent-slide",
                        "target": "PageNav return link",
                            "runtimeBinding": f"/module/{module}/slide/{exploration.get('parentSlideId')}",
                            "feedback": "Learner returns to the current lesson without changing the slide range.",
                            "purpose": "Preserve pxx as the main course spine.",
                        },
                    ],
                    "interactionHandoff": {
                        "target": "CourseApp/src/views/ExploreView.vue",
                        "stateModel": ["explore", "labControls", "linkedFeedback"],
                        "eventHandlers": ["resolveParentSlide", "updateLabState", "returnToParentSlide"],
                        "bindingMode": "parent-slide-subroute-to-vue-lab-component",
                    },
                    "designDirectives": [
                        "Exploration pages are child routes of parent slides and must not appear in slides.json.",
                        "Use interaction-necessity-gate evidence before adding the exploration route.",
                        "The exploration must provide a clear return path to its parent lesson.",
                    ],
                }
            )

        module_questions = [question for question in quizzes if question.get("moduleId") == module]
        if not module_questions:
            return screens
        screens.append(
            {
                "moduleId": module,
                "screenId": "quiz",
                "route": f"/module/{module}/quiz",
                "title": "做题页",
                "screenType": "realtime-quiz",
                "storyPurpose": "Let learners answer one focused question at a time, with randomized question order, randomized options, automatic progression, and a final score review.",
                "questionBank": {
                    "source": "CourseApp/src/data/quizzes.json",
                    "questionCount": len(module_questions),
                    "requiredTypes": sorted({question.get("type") for question in module_questions}),
                },
                "layoutIntent": {
                    "primaryFocus": "single active question card",
                    "readingPath": "navigation -> current question -> answer controls -> submit -> next question or score card",
                    "density": "medium",
                    "emphasis": ["单题卡片", "随机题库", "随机选项", "提交后自动下一题", "成绩复盘"],
                },
                "visualComposition": {
                    "aspectRatio": "centered full viewport assessment screen",
                    "shotType": "medium close assessment card",
                    "frameGrid": {
                        "columns": "single centered card, max readable width",
                        "rows": "breadcrumb, question header, answer list, action row, score review",
                        "anchor": "current question card anchors the center; score card replaces it after completion",
                    },
                    "foreground": {"subject": "current question and selected options", "position": "center", "scale": "dominant single-task card"},
                    "midground": {"subject": "submit/reset actions and progress count", "position": "inside card edges", "role": "support decision flow"},
                    "background": {"subject": "quiet dark course shell", "position": "full viewport", "role": "reduce distraction during assessment"},
                    "negativeSpace": "generous margins around the card keep the learner focused on one decision",
                    "readingDirection": "breadcrumb -> question type/progress -> question stem -> options -> submit",
                    "safeArea": "keep all answer controls above fold on common laptop viewport",
                    "cameraPlan": {"base": "locked centered card", "beatMotion": "card content changes, frame remains stable", "avoid": ["table-like all-question layout", "competing sidebars"]},
                },
                "paletteIntent": {
                    "mood": "focused, responsive, assessment-oriented",
                    "contrastRole": "use emerald for active choices and correct feedback, rose for remediation feedback",
                    "avoid": ["question bank table", "question-number navigation", "internal production guidance"],
                },
                "realtimeInteractionCues": [
                    {
                        "cueId": "quiz-cue-01",
                        "trigger": {"type": "page-load", "event": "quiz-mounted"},
                        "action": "shuffle-question-bank",
                        "target": "questionOrder",
                        "runtimeBinding": "restartQuiz()",
                        "feedback": "Question order is randomized when entering or restarting the quiz.",
                        "purpose": "Prevent answer memorization by fixed order.",
                    },
                    {
                        "cueId": "quiz-cue-02",
                        "trigger": {"type": "user-action", "event": "change"},
                        "action": "shuffle-options",
                        "target": "optionOrder[currentQuestion.id]",
                        "runtimeBinding": "shuffle(question.options)",
                        "feedback": "Each visible question renders options in a randomized order.",
                        "purpose": "Keep option display data-driven while preserving answer identity by id.",
                    },
                    {
                        "cueId": "quiz-cue-03",
                        "trigger": {"type": "user-action", "event": "click"},
                        "action": "select-answer",
                        "target": "radio-or-checkbox-inputs",
                        "runtimeBinding": "toggleAnswer(question, option.id)",
                        "feedback": "Selected options update local answer state without page reload.",
                        "purpose": "Single and multiple choice interactions stay visibly responsive.",
                    },
                    {
                        "cueId": "quiz-cue-04",
                        "trigger": {"type": "user-action", "event": "click"},
                        "action": "submit-answer",
                        "target": "submit-button",
                        "runtimeBinding": "submitAnswer(question)",
                        "feedback": "Compute correctness and advance to the next question automatically.",
                        "purpose": "Keep the quiz focused on one decision at a time.",
                    },
                    {
                        "cueId": "quiz-cue-05",
                        "trigger": {"type": "state-change", "event": "results-updated"},
                        "action": "show-score",
                        "target": "score-card",
                        "runtimeBinding": "finished + scoreCount",
                        "feedback": "Show final score, review states, restart, practice, and navigation actions.",
                        "purpose": "Close the assessment loop after all questions are answered.",
                    },
                ],
                "interactionHandoff": {
                    "target": "CourseApp/src/views/QuizView.vue",
                    "stateModel": ["questionOrder", "answers", "results", "optionOrder", "currentIndex"],
                    "eventHandlers": ["restartQuiz", "continuePractice", "toggleAnswer", "submitAnswer", "resetAnswer"],
                    "bindingMode": "storyboard-cue-to-vue-handler",
                },
                "designDirectives": [
                    "The 做题页 UI must show one active question card at a time.",
                    "Question and option order must be randomized without changing answer identity.",
                    "Submission advances automatically to the next question.",
                    "The score card must provide restart, practice, and return navigation.",
                ],
            }
        )
        return screens

    @staticmethod
    def _brief(contract: dict) -> str:
        lines = [
            "# Storyboard Brief",
            "",
            f"- Provider mode: `{contract['provider']}`",
            f"- Module: `{contract['module']}`",
            f"- Source: `{contract['source']}`",
            "- Role: Film-style storyboard layer before visual design.",
            "- Goal: Guide layout, palette, and subtitle-triggered motion for teaching expression.",
            "",
            "## Scenes",
            "",
        ]
        for slide in contract["slides"]:
            lines.extend(
                [
                    f"### {slide['moduleId']} / {slide['slideId']}",
                    "",
                    f"- Route: `{slide['route']}`",
                    f"- Title: {slide['title']}",
                    f"- Purpose: {slide['storyPurpose']}",
                    f"- Layout: {slide['layoutIntent'].get('primaryFocus')}",
                    f"- Composition: {slide.get('visualComposition', {}).get('shotType')} / {slide.get('visualComposition', {}).get('readingDirection')}",
                    f"- Frame grid: {slide.get('visualComposition', {}).get('frameGrid')}",
                    f"- Palette: {slide['paletteIntent'].get('mood')}",
                    "- Emphasis: motionCues bind subtitles to knowledgeFocus; optional slide `mentalModel` in slides.json (teaching layer).",
                    "- Motion cues:",
                ]
            )
            for cue in slide["motionCues"]:
                trigger = cue["trigger"]
                guidance = cue.get("dynamicGuidance", {})
                time_range = cue.get("timeRange", {})
                start = StoryboardMCP._format_time(float(time_range.get("start", 0)))
                end = StoryboardMCP._format_time(float(time_range.get("end", 0)))
                lines.append(
                    f"  - `{cue['cueId']}` {start}-{end} segment {trigger.get('segmentIndex')}: "
                    f"{cue['animation']['name']} -> {cue['target']} ({cue['contentBeat']}); "
                    f"focus `{cue.get('knowledgeFocus', {}).get('id')}` with {guidance.get('attentionPattern')} / {guidance.get('primaryEffect')}; "
                    f"target `{guidance.get('highlightTarget')}`; source subtitle: {cue.get('sourceSubtitleText')}"
                )
                lines.append(f"    - Shot: {cue.get('shotInstruction')}")
            lines.append("")
        lines.extend(["## Interactive Screens", ""])
        for screen in contract.get("interactiveScreens", []):
            lines.extend(
                [
                    f"### {screen.get('screenId')} - {screen.get('title')}",
                    "",
                    f"- Route: `{screen.get('route')}`",
                    f"- Purpose: {screen.get('storyPurpose')}",
                    f"- Layout: {screen.get('layoutIntent', {}).get('primaryFocus')}",
                    f"- Composition: {screen.get('visualComposition', {}).get('shotType')} / {screen.get('visualComposition', {}).get('readingDirection')}",
                    f"- Realtime cues: {len(screen.get('realtimeInteractionCues', []))}",
                    f"- Handoff target: `{screen.get('interactionHandoff', {}).get('target')}`",
                    "",
                ]
            )
        return "\n".join(lines)

    @staticmethod
    def _format_time(seconds: float) -> str:
        safe = max(0.0, seconds)
        minutes = int(safe // 60)
        remainder = safe - minutes * 60
        return f"{minutes:02d}:{remainder:05.2f}"
