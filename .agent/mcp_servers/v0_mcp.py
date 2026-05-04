from __future__ import annotations

import json
import time
from datetime import datetime
import urllib.error
import urllib.request
from pathlib import Path


class V0MCP:
    API_BASE = "https://api.v0.dev/v1"

    @staticmethod
    def _read_api_key(workspace: Path) -> str:
        env_file = workspace / ".env"
        if not env_file.exists():
            raise ValueError("缺少 .env，无法读取 V0_API_KEY")

        key = ""
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("V0_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
        if not key:
            raise ValueError(".env 中 V0_API_KEY 为空")
        return key

    @staticmethod
    def _request(workspace: Path, endpoint: str, method: str = "GET", payload: dict | None = None) -> dict:
        key = V0MCP._read_api_key(workspace)
        body = None
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        request = urllib.request.Request(
            f"{V0MCP.API_BASE}{endpoint}",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method=method,
        )
        timeout = 600 if method == "POST" else 30
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    @staticmethod
    def validate_api_key(workspace: Path) -> dict:
        try:
            payload = V0MCP._request(workspace, "/rate-limits")
        except ValueError as exc:
            return {"status": "error", "message": str(exc)}
        except urllib.error.HTTPError as exc:
            return {"status": "error", "message": f"v0 API 认证失败：HTTP {exc.code}"}
        except Exception as exc:
            return {"status": "error", "message": f"v0 API 探测失败：{exc}"}

        required = {"remaining", "reset", "limit"}
        missing = sorted(required - set(payload))
        if missing:
            return {"status": "error", "message": "v0 rate-limits 响应缺少字段：" + ", ".join(missing)}

        return {
            "status": "success",
            "endpoint": "https://api.v0.dev/v1/rate-limits",
            "remaining": payload.get("remaining"),
            "limit": payload.get("limit"),
        }

    @staticmethod
    def generate_react_prototype(workspace: Path, module: str) -> dict:
        """Create a v0 chat and persist the React prototype/design handoff.

        v0 is React-oriented, so this node treats its output as a design source.
        Vue code generation remains local and consumes the extracted rules.
        """
        slides_file = workspace / "CourseApp" / "src" / "data" / "slides.json"
        storyboard_file = workspace / "CourseApp" / "src" / "data" / "storyboard-contract.json"
        if not slides_file.exists():
            return {"status": "error", "message": "slides.json is required before v0 prototype generation"}
        if not storyboard_file.exists():
            return {"status": "error", "message": "storyboard-contract.json is required before v0 prototype generation"}

        try:
            slides = json.loads(slides_file.read_text(encoding="utf-8"))
            storyboard = json.loads(storyboard_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"status": "error", "message": f"v0 prototype input JSON invalid: {exc}"}

        module_slides = [item for item in slides if item.get("moduleId") == module]
        storyboard_slides = [
            item for item in storyboard.get("slides", []) if item.get("moduleId") == module
        ]
        storyboard_interactions = [
            item for item in storyboard.get("interactiveScreens", []) if item.get("moduleId") == module
        ]
        if not module_slides:
            return {"status": "error", "message": f"no slides found for {module}"}

        prompt = V0MCP._build_prototype_prompt(module, module_slides, storyboard_slides, storyboard_interactions)
        out_dir = workspace / ".agent" / "v0" / module
        out_dir.mkdir(parents=True, exist_ok=True)

        try:
            response = V0MCP._create_chat(workspace, prompt)
        except ValueError as exc:
            return {"status": "error", "message": str(exc)}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return {"status": "error", "message": f"v0 chat 创建失败：HTTP {exc.code}: {detail[:600]}"}
        except Exception as exc:
            return {"status": "error", "message": f"v0 chat 创建失败：{exc}"}

        handoff = V0MCP._extract_handoff(module, response, module_slides)
        prototype_file = out_dir / "react-prototype.json"
        brief_file = out_dir / "react-prototype-brief.md"
        prototype_file.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        brief_file.write_text(V0MCP._brief(handoff), encoding="utf-8")

        return {
            "status": "success",
            "provider": "v0",
            "chat_id": handoff.get("chat", {}).get("id"),
            "chat_url": handoff.get("chat", {}).get("url"),
            "prototype_file": str(prototype_file),
            "brief_file": str(brief_file),
            "slide_count": len(module_slides),
        }

    @staticmethod
    def _create_chat(workspace: Path, prompt: str) -> dict:
        payload = {
            "message": prompt,
            "modelConfiguration": {
                "thinking": False,
                "imageGenerations": False,
            },
            "metadata": {
                "project": "ShaderGUI_Learning_v1.0",
                "purpose": "course-player-ui-prototype",
            },
            "mcpServerIds": [],
        }
        last_error = None
        for attempt in range(1, 4):
            try:
                return V0MCP._request(workspace, "/chats", method="POST", payload=payload)
            except urllib.error.HTTPError as exc:
                if exc.code != 400:
                    raise
                fallback_payload = dict(payload)
                fallback_payload["initialMessage"] = fallback_payload.pop("message")
                return V0MCP._request(workspace, "/chats", method="POST", payload=fallback_payload)
            except (urllib.error.URLError, ConnectionError, TimeoutError) as exc:
                last_error = exc
                if attempt < 3:
                    time.sleep(2 * attempt)
                    continue
                raise
        raise RuntimeError(f"v0 chat request failed after retries: {last_error}")

    @staticmethod
    def _build_prototype_prompt(module: str, slides: list[dict], storyboard_slides: list[dict], storyboard_interactions: list[dict]) -> str:
        compact_slides = [
            {
                "slideId": slide.get("slideId"),
                "title": slide.get("title"),
                "kind": slide.get("kind"),
                "points": slide.get("points", []),
                "hasCode": bool(slide.get("code")),
            }
            for slide in slides
        ]
        compact_storyboard = {
            item.get("slideId"): {
                "layout": item.get("layoutIntent", {}).get("primaryFocus"),
                "palette": item.get("paletteIntent", {}).get("mood"),
                "motionCueCount": len(item.get("motionCues", [])),
            }
            for item in storyboard_slides
        }
        compact_interactions = [
            {
                "screenId": item.get("screenId"),
                "route": item.get("route"),
                "title": item.get("title"),
                "layout": item.get("layoutIntent", {}).get("primaryFocus"),
                "realtimeActions": [cue.get("action") for cue in item.get("realtimeInteractionCues", [])],
                "runtimeTarget": item.get("interactionHandoff", {}).get("target"),
            }
            for item in storyboard_interactions
        ]
        return (
            "Create one compact React + Tailwind prototype for a dark Chinese Unity ShaderGUI course player plus a 做题页 quiz screen. "
            "Use a large slide canvas, event subtitle area, compact bottom audio controls, tap-to-play, and vertical swipe navigation. "
            "The 做题页 must reflect storyboard realtime actions: question-bank scan, answer selection, option swapping, submit scoring, and feedback. "
            "Do not use shadcn imports, Next.js routing, transcript panels, or internal production workflow text. "
            "Return code plus concise design rules for translating the result to Vue 3 + Tailwind.\n"
            f"Module: {module}\n"
            f"Slides: {json.dumps(compact_slides, ensure_ascii=False)}\n"
            f"Storyboard: {json.dumps(compact_storyboard, ensure_ascii=False)}\n"
            f"Interactive screens: {json.dumps(compact_interactions, ensure_ascii=False)}\n"
        )

    @staticmethod
    def _extract_handoff(module: str, response: dict, slides: list[dict]) -> dict:
        files = V0MCP._collect_files(response)
        text_blocks = V0MCP._collect_strings(response)
        return {
            "provider": "v0",
            "status": "prototype_ready",
            "module": module,
            "generatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "chat": {
                "id": response.get("id") or response.get("chatId"),
                "url": response.get("url") or response.get("webUrl"),
                "apiUrl": response.get("apiUrl"),
            },
            "source": {
                "slides": "CourseApp/src/data/slides.json",
                "storyboard": "CourseApp/src/data/storyboard-contract.json",
            },
            "slides": [
                {
                    "moduleId": item.get("moduleId"),
                    "slideId": item.get("slideId"),
                    "title": item.get("title"),
                    "route": item.get("route"),
                }
                for item in slides
            ],
            "reactPrototype": {
                "files": files,
                "textBlocks": text_blocks[:12],
            },
            "extractedDesignRules": {
                "layout": [
                    "Dark full-screen course player shell with a luminous slide canvas centered above subtitles and controls.",
                    "Concept slides use a hero statement plus three progressive content cards.",
                    "Code slides use a split reading path: principle cards beside a high-contrast code panel.",
                ],
                "visual": [
                    "Use deep slate/neutral backgrounds, cyan or emerald accents, soft radial highlights, and glass-like cards.",
                    "Keep controls outside the learner-facing slide canvas.",
                    "Reserve strong accent treatments for the current teaching beat or code callout.",
                ],
                "interaction": [
                    "Bottom controls stay compact and touch-friendly.",
                    "Subtitles remain event-driven and visually separate from full transcripts.",
                    "Mobile surface tap toggles playback; vertical swipe navigates slides.",
                    "做题页 renders the question bank table first, then answer cards and immediate feedback.",
                    "Option swapping, answer selection, submission, reset, and scoring must remain live Vue state interactions.",
                ],
            },
            "rawResponseKeys": sorted(response.keys()),
        }

    @staticmethod
    def _collect_files(value) -> list[dict]:
        files = []

        def walk(node):
            if isinstance(node, dict):
                name = node.get("name") or node.get("fileName") or node.get("path")
                content = node.get("content") or node.get("source")
                if isinstance(name, str) and isinstance(content, str):
                    files.append({"name": name, "content": content[:12000]})
                for child in node.values():
                    walk(child)
            elif isinstance(node, list):
                for child in node:
                    walk(child)

        walk(value)
        return files[:20]

    @staticmethod
    def _collect_strings(value) -> list[str]:
        strings = []

        def walk(node):
            if isinstance(node, str) and len(node) > 120:
                strings.append(node[:4000])
            elif isinstance(node, dict):
                for child in node.values():
                    walk(child)
            elif isinstance(node, list):
                for child in node:
                    walk(child)

        walk(value)
        return strings

    @staticmethod
    def _brief(handoff: dict) -> str:
        chat = handoff.get("chat", {})
        rules = handoff.get("extractedDesignRules", {})
        lines = [
            "# v0 React Prototype Handoff",
            "",
            f"- Provider: `{handoff.get('provider')}`",
            f"- Status: `{handoff.get('status')}`",
            f"- Module: `{handoff.get('module')}`",
            f"- Chat ID: `{chat.get('id')}`",
            f"- Chat URL: `{chat.get('url')}`",
            "",
            "## Vue Translation Rules",
            "",
        ]
        for group, items in rules.items():
            lines.append(f"### {group}")
            lines.extend(f"- {item}" for item in items)
            lines.append("")
        lines.extend([
            "## React Prototype Files",
            "",
        ])
        for file in handoff.get("reactPrototype", {}).get("files", []):
            lines.append(f"- `{file.get('name')}`")
        if not handoff.get("reactPrototype", {}).get("files"):
            lines.append("- v0 response did not expose file payloads; text response is preserved in `react-prototype.json`.")
        return "\n".join(lines) + "\n"
