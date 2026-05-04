"""
App MCP: verify the Vue course application.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class AppMCP:
    @staticmethod
    def verify_course(root_workspace: Path) -> dict:
        script = root_workspace / "scripts" / "verify_course.py"
        if not script.exists():
            return {"status": "error", "message": f"缺少验证脚本：{script}"}
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(root_workspace),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stdout.strip() + "\n" + result.stderr.strip()}
        return {"status": "success", "log": result.stdout.strip()}


