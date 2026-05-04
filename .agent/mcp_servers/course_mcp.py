"""Course MCP: source material and manifest checks."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CourseRequest:
    module: str
    page: str


class CourseMCP:
    @staticmethod
    def check_source_material(root_workspace: Path) -> dict:
        required = [
            root_workspace / "docs" / "ShaderGUI_Teaching_Plan.md",
            root_workspace / "docs" / "Skill_Chain_DAG.md",
            root_workspace / ".agent" / "SKILL.md",
            root_workspace / ".agent" / "rules.md",
        ]
        missing = [str(path) for path in required if not path.exists()]
        if missing:
            return {"status": "error", "message": "missing source material: " + "; ".join(missing)}
        return {"status": "success", "files": [str(path) for path in required]}

    @staticmethod
    def ensure_course_manifest(root_workspace: Path) -> dict:
        course_file = root_workspace / "CourseApp" / "src" / "data" / "course.json"
        slides_file = root_workspace / "CourseApp" / "src" / "data" / "slides.json"
        if not course_file.exists():
            return {"status": "error", "message": f"missing course manifest: {course_file}"}
        if not slides_file.exists():
            return {"status": "error", "message": f"missing slide manifest: {slides_file}"}

        try:
            course = json.loads(course_file.read_text(encoding="utf-8"))
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "error", "message": f"manifest is not valid JSON: {exc}"}

        if not course.get("modules"):
            return {"status": "error", "message": "course.json missing modules"}
        if not slides:
            return {"status": "error", "message": "slides.json is empty"}

        return {
            "status": "success",
            "course_file": str(course_file),
            "slides_file": str(slides_file),
            "slide_count": len(slides),
        }

    @staticmethod
    def ensure_transcripts(root_workspace: Path) -> dict:
        slides_file = root_workspace / "CourseApp" / "src" / "data" / "slides.json"
        if not slides_file.exists():
            return {"status": "error", "message": f"missing slide manifest: {slides_file}"}

        slides = json.loads(slides_file.read_text(encoding="utf-8"))
        missing = []
        checked = 0
        for slide in slides:
            if slide.get("kind") == "interactive" or slide.get("interactive"):
                continue

            transcript_ref = slide.get("transcript")
            if not transcript_ref:
                missing.append(f"{slide.get('moduleId')}/{slide.get('slideId')} missing transcript contract")
                continue

            checked += 1
            transcript = root_workspace / "CourseApp" / "public" / transcript_ref.lstrip("/")
            if not transcript.exists():
                missing.append(str(transcript))
            elif not transcript.read_text(encoding="utf-8").strip():
                missing.append(str(transcript) + " (empty file)")

        if missing:
            return {"status": "error", "message": "missing transcripts: " + "; ".join(missing)}
        return {"status": "success", "transcript_count": checked}
