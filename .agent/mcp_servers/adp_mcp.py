from __future__ import annotations

import fnmatch
import json
import shutil
import subprocess
import sys
from pathlib import Path


class ADPMCP:
    """Generate ALL course slides for production (full ADP, not MVP).

    This is a parallel DAG node to MVPMCP.
    Reads from adp-scope.json and generates all slides for each module.
    """

    @staticmethod
    def generate_products(workspace: Path, module: str) -> dict:
        try:
            source = ADPMCP._load_module_source(workspace, module)
            slide_ids = ADPMCP._resolve_adp_slide_ids(workspace, module, source["slides"])
            source["slides"] = [slide for slide in source["slides"] if slide["slideId"] in slide_ids]
            cleaned = ADPMCP._clean_adp_products(workspace, module)
            ADPMCP._write_course_app(workspace, module, source)
            ADPMCP._copy_course_content(workspace, module, source["slides"])
            ADPMCP._write_scripts(workspace)
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
            audio_result = ADPMCP._ensure_audio(workspace, module)
            if audio_result["status"] != "success":
                print(f"[ADP] Audio: {audio_result.get('message')}")
        except Exception as exc:
            return {"status": "error", "message": f"ADP generation failed: {exc}"}
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
        course_source = ADPMCP._load_json(root / "course.json")
        slides = ADPMCP._load_json(root / "slides.json")
        quizzes = ADPMCP._load_json(root / "quizzes.json", [])
        explorations = ADPMCP._load_json(root / "explorations.json", [])
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
            transcript = ADPMCP._find_transcript(root, module, slide_id)
            if transcript:
                normalized["transcript"] = f"/transcripts/{module}/{transcript.name}"
            normalized_slides.append(normalized)
        scope_explorations = ADPMCP._scope_explorations(workspace, module)
        explorations = ADPMCP._normalize_explorations(module, explorations or scope_explorations)
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
        scope_file = workspace / ".agent" / "adp-scope.json"
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
                "component": item.get("component") or ADPMCP._component_name(exploration_id),
                "gateDecision": item.get("gateDecision") or {
                    "status": "inserted",
                    "gate": "interaction-necessity-gate",
                    "reason": "ADP scope requested this parent-slide child exploration.",
                },
            })
        return normalized

    @staticmethod
    def _find_transcript(root: Path, module: str, slide_id: str) -> Path | None:
        doc_root = root / "doc"
        matches = sorted(doc_root.glob(f"{module}-{slide_id}-*.md"))
        return matches[0] if matches else None

    @staticmethod
    def _resolve_adp_slide_ids(workspace: Path, module: str, slides: list[dict]) -> list[str]:
        source_ids = [slide["slideId"] for slide in slides]
        scope_file = workspace / ".agent" / "adp-scope.json"
        if not scope_file.exists():
            return source_ids
        scope = json.loads(scope_file.read_text(encoding="utf-8"))
        if scope.get("module", module) != module:
            return source_ids
        # adp-scope.json can have multiple modules
        for mod_entry in scope.get("modules", []):
            if mod_entry.get("module") == module:
                slide_ids = mod_entry.get("slideIds") or mod_entry.get("slides") or source_ids
                if not isinstance(slide_ids, list) or not all(isinstance(item, str) for item in slide_ids):
                    raise ValueError(".agent/adp-scope.json must contain slideIds: string[]")
                unknown = [slide_id for slide_id in slide_ids if slide_id not in source_ids]
                if unknown:
                    raise ValueError(f".agent/adp-scope.json references unknown slides: {unknown}")
                return list(dict.fromkeys(slide_ids))
        return source_ids

    @staticmethod
    def _clean_adp_products(workspace: Path, module: str) -> list[str]:
        scope_file = workspace / ".agent" / "adp-execution-scope.json"
        contract_file = workspace / "docs" / "ADP_Execution_Contract.md"
        if not scope_file.exists():
            raise ValueError("missing .agent/adp-execution-scope.json")
        if not contract_file.exists():
            raise ValueError("missing docs/ADP_Execution_Contract.md")
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
                raise ValueError("CourseContent is source input and cannot be cleaned by ADPMCP")
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
            cleaned.append(str(target.relative_to(workspace)).replace("\\", "/")
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
    def _write_course_app(workspace: Path, module: str, source: dict) -> None:
        """不依赖跨运行合并——扫描所有模块源文件，一次性写全量产物。"""
        app = workspace / "CourseApp"
        ADPMCP._copy_template_tree(ADPMCP._template_root(workspace) / "course-app", app)

        all_modules = []
        all_slides = []
        all_quizzes = []
        all_explorations = []

        for mod_dir in sorted(workspace.glob("CourseContent/Module_*")):
            if not mod_dir.is_dir():
                continue
            mod_name = mod_dir.name
            try:
                c = json.loads((mod_dir / "course.json").read_text(encoding="utf-8-sig"))
                s = json.loads((mod_dir / "slides.json").read_text(encoding="utf-8-sig"))
                q = json.loads((mod_dir / "quizzes.json").read_text(encoding="utf-8-sig")) if (mod_dir / "quizzes.json").exists() else []
                e = json.loads((mod_dir / "explorations.json").read_text(encoding="utf-8-sig")) if (mod_dir / "explorations.json").exists() else []
            except Exception as ex:
                print(f"[ADP] 跳过 {mod_name}（读源文件失败: {ex}）")
                continue

            norm_slides = ADPMCP._normalize_slides(mod_dir, mod_name, s)

            # course.json 格式：{ "title": "...", "modules": [{ "id": "...", ...}] }
            mod_entry = {}
            if isinstance(c, dict):
                modules_list = c.get("modules", [])
                if modules_list and isinstance(modules_list, list):
                    mod_entry = modules_list[0]

            all_modules.append({
                "id": mod_entry.get("id", mod_name),
                "title": mod_entry.get("title", mod_name),
                "summary": mod_entry.get("summary", ""),
                "slideCount": len(norm_slides),
            })
            all_slides.extend(norm_slides)
            all_quizzes.extend(q)
            all_explorations.extend(ADPMCP._normalize_explorations(mod_name, e))

        course_out = {
            "title": source["course"].get("title", "Course"),
            "subtitle": source["course"].get("subtitle", ""),
            "modules": all_modules,
        }
        ADPMCP._write_json(app / "src" / "data" / "course.json", course_out)
        ADPMCP._write_json(app / "src" / "data" / "slides.json", all_slides)
        ADPMCP._write_json(app / "src" / "data" / "quizzes.json", all_quizzes)
        ADPMCP._write_json(app / "src" / "data" / "explorations.json", all_explorations)
        print(f"[ADP] 已写入全量产物：{len(all_modules)} 模块，{len(all_slides)} slides")

    @staticmethod
    def _normalize_slides(mod_dir: Path, mod_name: str, slides: list) -> list:
        """给 slides 添加 route/audio/subtitles/transcript 字段。"""
        result = []
        for slide in slides:
            if not isinstance(slide, dict):
                continue
            slide_id = slide.get("slideId", "")
            norm = {
                **slide,
                "moduleId": slide.get("moduleId", mod_name),
                "route": f"/module/{mod_name}/slide/{slide_id}",
                "audio": f"/audio/{mod_name}/{slide_id}.mp3",
                "subtitles": f"/subtitles/{mod_name}/{slide_id}.json",
            }
            transcript = ADPMCP._find_transcript(mod_dir, mod_name, slide_id)
            if transcript:
                norm["transcript"] = f"/transcripts/{mod_name}/{transcript.name}"
            result.append(norm)
        return result

    @staticmethod
    def _copy_course_content(workspace: Path, module: str, slides: list[dict]) -> None:
        transcript_root = workspace / "CourseApp" / "public" / "transcripts" / module
        transcript_root.mkdir(parents=True, exist_ok=True)
        for slide in slides:
            transcript = ADPMCP._find_transcript(workspace / "CourseContent" / module, module, slide["slideId"])
            if transcript:
                shutil.copy2(transcript, transcript_root / transcript.name)

    @staticmethod
    def _write_scripts(workspace: Path) -> None:
        ADPMCP._copy_template_tree(ADPMCP._template_root(workspace) / "scripts", workspace / "scripts")

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
