"""
Voice MCP: generate narration audio from transcript files.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class VoiceMCP:
    @staticmethod
    def generate_audio(root_workspace: Path, module: str) -> dict:
        script = root_workspace / "scripts" / "generate_audio.py"
        if not script.exists():
            return {"status": "error", "message": f"缺少音频生成脚本：{script}"}

        result = subprocess.run(
            [sys.executable, str(script), module],
            cwd=str(root_workspace),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode != 0:
            return {
                "status": "error",
                "message": result.stderr.strip() or result.stdout.strip() or "音频生成失败",
            }
        return {"status": "success", "log": result.stdout.strip()}
