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
    def generate_products(
        workspace: Path,
        module: str,
        *,
        accumulate: bool = False,
        clean: bool = True,
        scope_file_name: str = "mvp-scope.json",
    ) -> dict:
        try:
            source = MVPMCP._load_module_source(workspace, module, scope_file_name=scope_file_name)
            slide_ids = MVPMCP._resolve_mvp_slide_ids(workspace, module, source["slides"], scope_file_name=scope_file_name)
            source["slides"] = [slide for slide in source["slides"] if slide["slideId"] in slide_ids]
            cleaned = MVPMCP._clean_mvp_products(workspace, module) if clean else []
            MVPMCP._write_course_app(workspace, module, source, accumulate=accumulate)
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
                print(f"[MVP Harden] Audio: {audio_result.get('message')}")
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
    def _load_module_source(workspace: Path, module: str, scope_file_name: str = "mvp-scope.json") -> dict:
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
        scope_explorations = MVPMCP._scope_explorations(workspace, module, scope_file_name=scope_file_name)
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
    def _scope_explorations(workspace: Path, module: str, scope_file_name: str = "mvp-scope.json") -> list[dict]:
        scope_file = workspace / ".agent" / scope_file_name
        if not scope_file.exists():
            return []
        scope = json.loads(scope_file.read_text(encoding="utf-8-sig"))
        for mod_entry in scope.get("modules", []):
            if isinstance(mod_entry, dict) and mod_entry.get("module") == module:
                return mod_entry.get("explorations") or []
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
    def _resolve_mvp_slide_ids(
        workspace: Path,
        module: str,
        slides: list[dict],
        scope_file_name: str = "mvp-scope.json",
    ) -> list[str]:
        source_ids = [slide["slideId"] for slide in slides]
        scope_file = workspace / ".agent" / scope_file_name
        if not scope_file.exists():
            return source_ids
        scope = json.loads(scope_file.read_text(encoding="utf-8"))
        for mod_entry in scope.get("modules", []):
            if isinstance(mod_entry, dict) and mod_entry.get("module") == module:
                slide_ids = mod_entry.get("slideIds") or mod_entry.get("slides") or source_ids
                if not isinstance(slide_ids, list) or not all(isinstance(item, str) for item in slide_ids):
                    raise ValueError(f".agent/{scope_file_name} module entries must contain slideIds: string[]")
                unknown = [slide_id for slide_id in slide_ids if slide_id not in source_ids]
                if unknown:
                    raise ValueError(f".agent/{scope_file_name} references unknown slides: {unknown}")
                return list(dict.fromkeys(slide_ids))
        if scope.get("module", module) != module:
            return source_ids
        slide_ids = scope.get("slideIds") or scope.get("slides") or source_ids
        if not isinstance(slide_ids, list) or not all(isinstance(item, str) for item in slide_ids):
            raise ValueError(f".agent/{scope_file_name} must contain slideIds: string[]")
        unknown = [slide_id for slide_id in slide_ids if slide_id not in source_ids]
        if unknown:
            raise ValueError(f".agent/{scope_file_name} references unknown slides: {unknown}")
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
            shutil.copy2(src, dst)

    @staticmethod
    def _write_course_app(workspace: Path, module: str, source: dict, accumulate: bool = False) -> None:
        app = workspace / "CourseApp"
        MVPMCP._copy_template_tree(MVPMCP._template_root(workspace) / "course-app", app)

        course_source = source["course"]
        module_source = MVPMCP._module_metadata(course_source, module)
        module_entry = {
            "id": module_source.get("id", module),
            "title": module_source.get("title", module),
            "summary": module_source.get("summary") or module_source.get("description", ""),
            "slideCount": len(source["slides"]),
        }
        if accumulate:
            course = MVPMCP._merge_course_data(app, course_source, module, module_entry)
            slides = MVPMCP._merge_module_items(app / "src" / "data" / "slides.json", source["slides"], module)
            quizzes = MVPMCP._merge_module_items(app / "src" / "data" / "quizzes.json", source["quizzes"], module)
            explorations = MVPMCP._merge_module_items(
                app / "src" / "data" / "explorations.json",
                source["explorations"],
                module,
            )
        else:
            course = {
                "title": course_source.get("title", "Course"),
                "subtitle": course_source.get("subtitle", ""),
                "modules": [module_entry],
            }
            slides = source["slides"]
            quizzes = source["quizzes"]
            explorations = source["explorations"]
        MVPMCP._write_json(app / "src" / "data" / "course.json", course)
        MVPMCP._write_json(app / "src" / "data" / "slides.json", slides)
        MVPMCP._write_json(app / "src" / "data" / "quizzes.json", quizzes)
        MVPMCP._write_json(app / "src" / "data" / "explorations.json", explorations)
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
    def _merge_course_data(app: Path, course_source: dict, module: str, module_entry: dict) -> dict:
        course_file = app / "src" / "data" / "course.json"
        if course_file.exists():
            try:
                course = json.loads(course_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                course = {}
        else:
            course = {}
        course["title"] = course.get("title") or course_source.get("title", "Course")
        course["subtitle"] = course.get("subtitle") or course_source.get("subtitle", "")
        modules = [item for item in course.get("modules", []) if item.get("id") != module]
        modules.append(module_entry)
        course["modules"] = sorted(modules, key=lambda item: item.get("id", ""))
        return course

    @staticmethod
    def _merge_module_items(path: Path, new_items: list, module: str) -> list:
        existing = []
        if path.exists():
            try:
                existing = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                existing = []
        existing = [item for item in existing if not isinstance(item, dict) or item.get("moduleId") != module]
        merged = [*existing, *new_items]
        return sorted(
            merged,
            key=lambda item: (
                item.get("moduleId", "") if isinstance(item, dict) else "",
                item.get("order", 999) if isinstance(item, dict) else 999,
                item.get("slideId", item.get("parentSlideId", "")) if isinstance(item, dict) else "",
            ),
        )

    @staticmethod
    def _module_metadata(course_source: dict, module: str) -> dict:
        module_source = course_source.get("module")
        if isinstance(module_source, dict):
            return module_source
        modules = course_source.get("modules")
        if isinstance(modules, list):
            for item in modules:
                if isinstance(item, dict) and item.get("id") == module:
                    return item
            if modules and isinstance(modules[0], dict):
                return modules[0]
        if course_source.get("moduleId") or course_source.get("title") or course_source.get("description"):
            return {
                "id": course_source.get("moduleId", module),
                "title": course_source.get("title", module),
                "summary": course_source.get("summary") or course_source.get("description", ""),
            }
        return {"id": module, "title": module, "summary": ""}

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

    @staticmethod
    def _ensure_audio(workspace: Path, module: str) -> dict:
        """检查音频文件是否存在（不生成音频，由 flow engine 调度）"""
        app = workspace / "CourseApp"
        slides_file = app / "src" / "data" / "slides.json"
        
        if not slides_file.exists():
            return {"status": "error", "message": "slides.json not found"}
        
        try:
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "error", "message": f"Failed to read slides.json: {exc}"}
        
        module_slides = [s for s in slides if s.get("moduleId") == module]
        missing_audio = []
        
        for slide in module_slides:
            audio_path = slide.get("audio")
            if not audio_path:
                continue
            full_path = app / "public" / audio_path.lstrip("/")
            if not full_path.exists():
                missing_audio.append(audio_path)
        
        if missing_audio:
            return {
                "status": "warning",
                "message": f"缺少 {len(missing_audio)} 个音频文件，将由 flow engine 生成",
                "missing": missing_audio,
            }
        
        return {"status": "success", "message": "所有音频文件已存在"}

    @staticmethod
    def _fix_timeRange(workspace: Path, module: str) -> dict:
        """后处理：修复 storyboard-contract.json 中的 timeRange 对齐问题"""
        fix_script = workspace / "fix_timeRange.py"
        if not fix_script.exists():
            return {"status": "skipped", "message": "fix_timeRange.py 不存在，跳过"}
        try:
            result = subprocess.run(
                [sys.executable, str(fix_script)],
                cwd=str(workspace),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": f"fix_timeRange.py 失败 (exit {result.returncode}): {result.stdout.strip()} {result.stderr.strip()}",
                }
            return {"status": "success", "message": result.stdout.strip()}
        except Exception as exc:
            return {"status": "error", "message": f"运行 fix_timeRange.py 异常: {exc}"}
