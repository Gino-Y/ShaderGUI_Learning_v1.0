"""
Stitch MCP: bind slides, audio, subtitle events, child exploration pages, and runtime components.
"""
from __future__ import annotations

import json
from pathlib import Path


class StitchMCP:
    @staticmethod
    def stitch_runtime(root_workspace: Path, module: str, accumulate: bool = False) -> dict:
        app = root_workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        explorations_file = app / "src" / "data" / "explorations.json"
        quizzes_file = app / "src" / "data" / "quizzes.json"
        storyboard_file = app / "src" / "data" / "storyboard-contract.json"
        design_file = app / "src" / "data" / "design-contract.json"
        player_file = app / "src" / "components" / "CoursePlayer.vue"
        nav_file = app / "src" / "components" / "SlideNav.vue"
        subtitle_file = app / "src" / "components" / "SubtitleOverlay.vue"
        exploration_file = app / "src" / "views" / "ExploreView.vue"
        quiz_file = app / "src" / "views" / "QuizView.vue"

        if not slides_file.exists():
            return {"status": "error", "message": f"missing slides.json: {slides_file}"}
        try:
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
            explorations = json.loads(explorations_file.read_text(encoding="utf-8")) if explorations_file.exists() else []
            quizzes = json.loads(quizzes_file.read_text(encoding="utf-8")) if quizzes_file.exists() else []
            storyboard = json.loads(storyboard_file.read_text(encoding="utf-8")) if storyboard_file.exists() else {}
            design = json.loads(design_file.read_text(encoding="utf-8")) if design_file.exists() else {}
        except json.JSONDecodeError as exc:
            return {"status": "error", "message": f"runtime contract JSON invalid: {exc}"}

        required_components = [player_file, nav_file, subtitle_file, quiz_file]
        if explorations or any(slide.get("explore") for slide in slides if slide.get("moduleId") == module):
            required_components.append(exploration_file)
        missing_components = [str(path) for path in required_components if not path.exists()]
        if missing_components:
            return {"status": "error", "message": "missing runtime components: " + "; ".join(missing_components)}

        stitched = []
        stitched_interactions = []
        errors = []

        for slide in [item for item in slides if item.get("moduleId") == module]:
            slide_id = slide.get("slideId")
            if slide.get("kind") == "interactive" or slide.get("interactive"):
                errors.append(f"{module}/{slide_id} exploration must be a child page, not a pxx slide")
                continue

            audio_path = app / "public" / slide.get("audio", "").lstrip("/")
            subtitle_path = app / "public" / slide.get("subtitles", "").lstrip("/")
            transcript_path = app / "public" / slide.get("transcript", "").lstrip("/")
            for label, path in {
                "audio": audio_path,
                "subtitles": subtitle_path,
                "transcript": transcript_path,
            }.items():
                if not path.exists():
                    errors.append(f"{module}/{slide_id} missing {label}: {path}")

            events = []
            if subtitle_path.exists():
                try:
                    events = json.loads(subtitle_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    errors.append(f"{module}/{slide_id} subtitle JSON invalid: {exc}")
                    events = []
                if not isinstance(events, list) or not events:
                    errors.append(f"{module}/{slide_id} subtitle events are empty")
                elif not all({"start", "end", "text"}.issubset(event) for event in events):
                    errors.append(f"{module}/{slide_id} subtitle event missing start/end/text")

            stitched.append({
                "moduleId": module,
                "slideId": slide_id,
                "route": slide.get("route"),
                "audio": slide.get("audio"),
                "subtitles": slide.get("subtitles"),
                "transcript": slide.get("transcript"),
                "subtitleEventCount": len(events),
                "interaction": None,
            })

        storyboard_screens = {
            item.get("screenId"): item
            for item in storyboard.get("interactiveScreens", [])
            if item.get("moduleId") == module
        }
        design_screens = {
            item.get("screenId"): item
            for item in design.get("interactiveScreens", [])
            if item.get("moduleId") == module
        }

        module_explorations = [item for item in explorations if item.get("moduleId") == module]
        for slide in [item for item in slides if item.get("moduleId") == module]:
            explore = slide.get("explore")
            if not explore:
                continue
            module_explorations.append({
                "moduleId": module,
                "parentSlideId": slide.get("slideId"),
                "explorationId": explore.get("id") or explore.get("component", "explore"),
                "route": explore.get("route"),
                "title": explore.get("title"),
                "component": explore.get("component"),
            })
        deduped_explorations = []
        seen_explorations = set()
        for exploration in module_explorations:
            key = (
                exploration.get("moduleId"),
                exploration.get("parentSlideId"),
                exploration.get("route"),
                exploration.get("explorationId"),
            )
            if key in seen_explorations:
                continue
            seen_explorations.add(key)
            deduped_explorations.append(exploration)
        for exploration in deduped_explorations:
            screen_id = f"explore-{exploration.get('parentSlideId')}-{exploration.get('explorationId')}"
            screen_storyboard = storyboard_screens.get(screen_id)
            screen_design = design_screens.get(screen_id)
            component = exploration.get("component")
            if component and not (app / "src" / "components" / "labs" / f"{component}.vue").exists():
                errors.append(f"{module}/{screen_id} missing exploration component: {component}")
            if not screen_storyboard:
                errors.append(f"{module}/{screen_id} missing exploration storyboard contract")
            if not screen_design:
                errors.append(f"{module}/{screen_id} missing exploration design contract")
            if screen_storyboard and screen_design:
                stitched_interactions.append({
                    "moduleId": module,
                    "screenId": screen_id,
                    "route": exploration.get("route"),
                    "runtime": "ExploreView.vue",
                    "parentSlideId": exploration.get("parentSlideId"),
                    "component": component,
                    "storyboardCueCount": len(screen_storyboard.get("realtimeInteractionCues", [])),
                    "designCueCount": len(screen_design.get("realtimeInteractionCues", [])),
                    "stateModel": screen_storyboard.get("interactionHandoff", {}).get("stateModel", []),
                    "eventHandlers": screen_storyboard.get("interactionHandoff", {}).get("eventHandlers", []),
                    "bindingMode": "parent-slide-subroute-exploration",
                })

        module_quizzes = [item for item in quizzes if item.get("moduleId") == module]
        quiz_storyboard = storyboard_screens.get("quiz")
        quiz_design = design_screens.get("quiz")
        if not module_quizzes:
            errors.append(f"{module}/quiz missing question data: {quizzes_file}")
        if not quiz_storyboard:
            errors.append(f"{module}/quiz missing storyboard contract: {storyboard_file}")
        if not quiz_design:
            errors.append(f"{module}/quiz missing design contract: {design_file}")
        if quiz_file.exists():
            quiz_text = quiz_file.read_text(encoding="utf-8")
            for marker in ["questions", "submitQuiz", "answers", "restartQuiz"]:
                if marker not in quiz_text:
                    errors.append(f"{module}/quiz missing runtime marker: {marker}")
        if quiz_storyboard and quiz_design:
            stitched_interactions.append({
                "moduleId": module,
                "screenId": "quiz",
                "route": quiz_storyboard.get("route"),
                "runtime": "QuizView.vue",
                "questionCount": len(module_quizzes),
                "storyboardCueCount": len(quiz_storyboard.get("realtimeInteractionCues", [])),
                "designCueCount": len(quiz_design.get("realtimeInteractionCues", [])),
                "stateModel": quiz_storyboard.get("interactionHandoff", {}).get("stateModel", []),
                "eventHandlers": quiz_storyboard.get("interactionHandoff", {}).get("eventHandlers", []),
                "bindingMode": "storyboard-and-design-guided-realtime-vue-state",
            })

        if not stitched:
            return {"status": "error", "message": f"slides.json has no slides for module: {module}"}
        if errors:
            return {"status": "error", "message": "; ".join(errors)}

        manifest = {
            "module": module,
            "player": "CoursePlayer.vue",
            "navigation": "SlideNav.vue",
            "subtitleOverlay": "SubtitleOverlay.vue",
            "slides": stitched,
            "interactiveScreens": stitched_interactions,
        }
        out_file = app / "src" / "data" / "stitch-manifest.json"
        if accumulate:
            manifest = StitchMCP._merge_manifest(out_file, manifest, module)
        out_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        return {"status": "success", "file": str(out_file), "slide_count": len(stitched)}

    @staticmethod
    def _merge_manifest(out_file: Path, manifest: dict, module: str) -> dict:
        if not out_file.exists():
            manifest["module"] = "ADP_ACCUMULATED"
            return manifest
        try:
            existing = json.loads(out_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest["module"] = "ADP_ACCUMULATED"
            return manifest
        existing_slides = [
            item for item in existing.get("slides", [])
            if item.get("moduleId") != module
        ]
        existing_screens = [
            item for item in existing.get("interactiveScreens", [])
            if item.get("moduleId") != module
        ]
        manifest["slides"] = sorted(
            [*existing_slides, *manifest.get("slides", [])],
            key=lambda item: (item.get("moduleId", ""), item.get("slideId", "")),
        )
        manifest["interactiveScreens"] = sorted(
            [*existing_screens, *manifest.get("interactiveScreens", [])],
            key=lambda item: (item.get("moduleId", ""), item.get("screenId", "")),
        )
        manifest["module"] = "ADP_ACCUMULATED"
        return manifest
