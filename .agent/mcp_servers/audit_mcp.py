"""
Audit MCP: audit the Vue course application dependencies.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class AuditMCP:
    @staticmethod
    def audit_app(root_workspace: Path) -> dict:
        app_dir = root_workspace / "CourseApp"
        result = subprocess.run(
            ["npm.cmd", "audit", "--audit-level=moderate"],
            cwd=str(app_dir),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stdout.strip() + "\n" + result.stderr.strip()}
        return {"status": "success", "log": result.stdout.strip()}
