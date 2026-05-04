"""
Build MCP: build the Vue course application.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class BuildMCP:
    @staticmethod
    def build_app(root_workspace: Path) -> dict:
        app_dir = root_workspace / "CourseApp"
        if not app_dir.exists():
            return {"status": "error", "message": f"缺少 CourseApp：{app_dir}"}
        result = subprocess.run(
            ["npm.cmd", "run", "build"],
            cwd=str(app_dir),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stdout.strip() + "\n" + result.stderr.strip()}
        return {"status": "success", "log": result.stdout.strip()}
