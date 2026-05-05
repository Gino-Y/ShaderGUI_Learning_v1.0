from __future__ import annotations

import fnmatch
import json
import shutil
import subprocess
import sys
from pathlib import Path


class MVPMCP:
    """Generate the course MVP from explicit source artifacts.

    This MCP is intentionally content-agnostic. Course/module/slide/quiz text
    must live under CourseContent/<module>/ or another upstream source file,
    never inside this server.
    """

    @staticmethod
    @staticmethod
    def generate_products(workspace: Path, module: str) -> dict:
        try:
            source = MVPMCP._load_module_source(workspace, module)
            slide_ids = MVPMCP._resolve_mvp_slide_ids(workspace, module, source["slides"])
            source["slides"] = [slide for slide in source["slides"] if slide["slideId"] in slide_ids]
            cleaned = MVPMCP._clean_mvp_products(workspace, module)
            MVPMCP._write_course_app(workspace, module, source)
            MVPMCP._copy_course_content(workspace, module, source["slides"])
            MVPMCP._write_scripts(workspace)
            install = subprocess.run(
                ["npm.cmd", "install"],
                cwd=str(workspace / "CourseApp"),
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
            )
            if install.returncode != 0:
                return {"status": "error", "message": install.stdout.strip() + "\n" + install.stderr.strip()}
            # 加固：MVP 后自动检查并生成音频（不调用 storyboard，由 flow engine 调度）
            audio_result = MVPMCP._ensure_audio(workspace, module)
            if audio_result["status"] != "success":
                print(f"[MVP Harden] Audio generation failed: {audio_result.get('message')}")
        except Exception as exc:
            return {"status": "error", "message": f"MVP generation failed: {exc}"}
        return {
            "status": "success",
            "module": module,
            "app": str(workspace / "CourseApp"),
            "content": str(workspace / "CourseContent" / module),
            "scripts": str(workspace / "scripts"),
            "slide_ids": slide_ids,
            "slide_count": len(slide_ids),
            "cleaned": cleaned,
        }
    @staticmethod
    def _load_json(path: Path, fallback=None):
        if not path.exists():
            if fallback is not None:
                return fallback
            raise ValueError(f"missing source file: {path}")
        return json.loads(path.read_text(encoding="utf-8-sig"))

    @staticmethod
    def _load_module_source(workspace: Path, module: str) -> dict:
        root = workspace / "CourseContent" / module
        course_source = MVPMCP._load_json(root / "course.json")
        slides = MVPMCP._load_json(root / "slides.json")
        quizzes = MVPMCP._load_json(root / "quizzes.json", [])
        explorations = MVPMCP._load_json(root / "explorations.json", [])
        if not isinstance(slides, list) or not slides:
            raise ValueError(f"{root / 'slides.json'} must contain a non-empty array")
        normalized_slides = []
        for index, slide in enumerate(slides):
            if not isinstance(slide, dict):
                raise ValueError("each slide source item must be an object")
            slide_id = slide.get("slideId")
            if not isinstance(slide_id, str) or not slide_id:
                raise ValueError("each slide source item must contain slideId")
            normalized = {
                **slide,
                "moduleId": slide.get("moduleId") or module,
                "order": slide.get("order", index),
                "route": f"/module/{module}/slide/{slide_id}",
                "audio": f"/audio/{module}/{slide_id}.mp3",
                "subtitles": f"/subtitles/{module}/{slide_id}.json",
            }
            transcript = MVPMCP._find_transcript(root, module, slide_id)
            if transcript:
                normalized["transcript"] = f"/transcripts/{module}/{transcript.name}"
            normalized_slides.append(normalized)
        scope_explorations = MVPMCP._scope_explorations(workspace, module)
        explorations = MVPMCP._normalize_explorations(module, explorations or scope_explorations)
        by_slide = {slide["slideId"]: slide for slide in normalized_slides}
        for exploration in explorations:
            parent_id = exploration.get("parentSlideId")
            parent = by_slide.get(parent_id)
            if parent:
                parent["explore"] = {
                    "id": exploration.get("explorationId"),
                    "route": exploration.get("route"),
                    "title": exploration.get("title"),
                    "component": exploration.get("component"),
                }
        return {
            "course": course_source,
            "slides": sorted(normalized_slides, key=lambda item: item["order"]),
            "quizzes": quizzes,
            "explorations": explorations,
        }

    @staticmethod
    def _scope_explorations(workspace: Path, module: str) -> list[dict]:
        scope_file = workspace / ".agent" / "mvp-scope.json"
        if not scope_file.exists():
            return []
        scope = json.loads(scope_file.read_text(encoding="utf-8-sig"))
        if scope.get("module", module) != module:
            return []
        return scope.get("explorations") or []

    @staticmethod
    def _component_name(exploration_id: str | None) -> str:
        raw = exploration_id or "exploration"
        return "".join(part.capitalize() for part in raw.replace("_", "-").split("-") if part) + "Lab"

    @staticmethod
    def _normalize_explorations(module: str, explorations: list[dict]) -> list[dict]:
        normalized = []
        seen = set()
        for item in explorations:
            parent_id = item.get("parentSlideId")
            exploration_id = item.get("explorationId") or item.get("id") or "exploration"
            if not parent_id:
                continue
            route = item.get("route") or f"/module/{module}/slide/{parent_id}/explore"
            key = (module, parent_id, route)
            if key in seen:
                continue
            seen.add(key)
            normalized.append({
                "moduleId": item.get("moduleId") or module,
                "parentSlideId": parent_id,
                "explorationId": exploration_id,
                "route": route,
                "title": item.get("title") or "探索页",
                "component": item.get("component") or MVPMCP._component_name(exploration_id),
                "gateDecision": item.get("gateDecision") or {
                    "status": "inserted",
                    "gate": "interaction-necessity-gate",
                    "reason": "MVP scope requested this parent-slide child exploration.",
                },
            })
        return normalized

    @staticmethod
    def _find_transcript(root: Path, module: str, slide_id: str) -> Path | None:
        doc_root = root / "doc"
        matches = sorted(doc_root.glob(f"{module}-{slide_id}-*.md"))
        return matches[0] if matches else None

    @staticmethod
    def _resolve_mvp_slide_ids(workspace: Path, module: str, slides: list[dict]) -> list[str]:
        source_ids = [slide["slideId"] for slide in slides]
        scope_file = workspace / ".agent" / "mvp-scope.json"
        if not scope_file.exists():
            return source_ids
        scope = json.loads(scope_file.read_text(encoding="utf-8"))
        if scope.get("module", module) != module:
            return source_ids
        slide_ids = scope.get("slideIds") or scope.get("slides") or source_ids
        if not isinstance(slide_ids, list) or not all(isinstance(item, str) for item in slide_ids):
            raise ValueError(".agent/mvp-scope.json must contain slideIds: string[]")
        unknown = [slide_id for slide_id in slide_ids if slide_id not in source_ids]
        if unknown:
            raise ValueError(f".agent/mvp-scope.json references unknown slides: {unknown}")
        return list(dict.fromkeys(slide_ids))

    @staticmethod
    def _clean_mvp_products(workspace: Path, module: str) -> list[str]:
        scope_file = workspace / ".agent" / "mvp-execution-scope.json"
        contract_file = workspace / "docs" / "MVP_Execution_Contract.md"
        if not scope_file.exists():
            raise ValueError("missing .agent/mvp-execution-scope.json")
        if not contract_file.exists():
            raise ValueError("missing docs/MVP_Execution_Contract.md")
        scope = json.loads(scope_file.read_text(encoding="utf-8"))
        allow = scope.get("clean", {}).get("allow", [])
        deny = scope.get("clean", {}).get("deny", [])
        cleaned = []
        for item in allow:
            rel = item.replace("{module}", module).replace("\\", "/").strip("/")
            if not rel or rel.startswith("../") or "/../" in rel or Path(rel).is_absolute():
                raise ValueError(f"unsafe clean path: {item}")
            blocked_segments = {".agent", "node_modules"}
            if any(segment in blocked_segments for segment in rel.split("/")):
                raise ValueError(f"clean path is denied by execution scope: {rel}")
            if rel.startswith("CourseContent/"):
                raise ValueError("CourseContent is source input and cannot be cleaned by MVPMCP")
            for pattern in deny:
                normalized_pattern = pattern.replace("\\", "/").strip("/")
                if fnmatch.fnmatch(rel, normalized_pattern) or rel == normalized_pattern.removesuffix("/**"):
                    raise ValueError(f"clean path is denied by execution scope: {rel}")
            target = workspace / Path(*rel.split("/"))
            if not target.exists():
                continue
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            cleaned.append(str(target.relative_to(workspace)).replace("\\", "/"))
        return cleaned

    @staticmethod
    def _write_json(path: Path, data) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


    @staticmethod
    def _template_root(workspace: Path) -> Path:
        root = workspace / ".agent" / "templates"
        if not root.exists():
            raise ValueError(f"missing template root: {root}")
        return root

    @staticmethod
    def _copy_template_tree(template_dir: Path, target_dir: Path) -> None:
        if not template_dir.exists():
            raise ValueError(f"missing template directory: {template_dir}")
        for src in sorted(template_dir.rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(template_dir)
            dst = target_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                continue  # 不覆盖已存在的文件（防止节点漂移）
            shutil.copy2(src, dst)

    @staticmethod
    def _write_course_app(workspace: Path, module: str, source: dict) -> None:
        app = workspace / "CourseApp"
        MVPMCP._copy_template_tree(MVPMCP._template_root(workspace) / "course-app", app)

        course_source = source["course"]
        module_source = course_source.get("module") or {}
        course = {
            "title": course_source.get("title", "Course"),
            "subtitle": course_source.get("subtitle", ""),
            "modules": [
                {
                    "id": module_source.get("id", module),
                    "title": module_source.get("title", module),
                    "summary": module_source.get("summary", ""),
                    "slideCount": len(source["slides"]),
                }
            ],
        }
        MVPMCP._write_json(app / "src" / "data" / "course.json", course)
        MVPMCP._write_json(app / "src" / "data" / "slides.json", source["slides"])
        MVPMCP._write_json(app / "src" / "data" / "quizzes.json", source["quizzes"])
        MVPMCP._write_json(app / "src" / "data" / "explorations.json", source["explorations"])
        # 加固：只在文件不存在时才写占位符，避免覆盖已有真实数据
        contract_path = app / "src" / "data" / "storyboard-contract.json"
        if not contract_path.exists():
            MVPMCP._write_json(contract_path, {
                "provider": "storyboard-placeholder",
                "status": "storyboard_pending",
                "module": module,
                "slides": [],
                "interactiveScreens": [],
            })
            print(f"[MVP Harden] storyboard-contract.json placeholder written (first run)")
        else:
            # 文件已存在，检查是否已有真实数据
            try:
                existing = json.loads(contract_path.read_text(encoding="utf-8"))
                if existing.get("status") == "storyboard_ready" and existing.get("slides"):
                    print(f"[MVP Harden] Skipping storyboard-contract.json (has real data: {len(existing.get('slides'))} slides)")
                else:
                    print(f"[MVP Harden] storyboard-contract.json exists but not ready (status={existing.get('status')}), leaving for storyboard step")
            except Exception as ex:
                print(f"[MVP Harden] storyboard-contract.json exists but unreadable: {ex}")

    @staticmethod
    def _copy_course_content(workspace: Path, module: str, slides: list[dict]) -> None:
        transcript_root = workspace / "CourseApp" / "public" / "transcripts" / module
        transcript_root.mkdir(parents=True, exist_ok=True)
        for slide in slides:
            transcript = MVPMCP._find_transcript(workspace / "CourseContent" / module, module, slide["slideId"])
            if transcript:
                shutil.copy2(transcript, transcript_root / transcript.name)

    @staticmethod
    def _write_scripts(workspace: Path) -> None:
        MVPMCP._copy_template_tree(MVPMCP._template_root(workspace) / "scripts", workspace / "scripts")
