"""
Runtime guard for ShaderGUI course flow execution.

The guard separates test and production execution:
- test mode may clear generated outputs for a declared stage.
- production mode never clears files automatically.
- every run must declare scope so execution is intentional.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from platform_violation_guard import enforce_platform_boundary

SCOPES = {"module", "all-content"}
TEST_STAGES = {"audio", "verify", "mvp", "storyboard", "design"}


def _remove_path(path: Path) -> bool:
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)
        return True
    except PermissionError:
        return False


def assert_workspace(path: Path) -> Path:
    root = path.resolve()
    if not (root / ".agent").exists():
        raise ValueError(f"不是有效项目根目录，缺少 .agent：{root}")
    enforce_platform_boundary(root, fix=False)
    return root


def expand_targets(workspace: Path, scope: str, module: str | None = None) -> list[str]:
    if scope not in SCOPES:
        raise ValueError(f"不支持的 scope：{scope}")
    if scope == "module":
        if not module:
            raise ValueError("module scope 必须提供 --module")
        return [module]

    audio_root = workspace / "CourseApp" / "public" / "transcripts"
    modules = sorted(path.name for path in audio_root.glob("Module_*") if path.is_dir())
    if not modules:
        raise ValueError(f"未找到任何模块逐字稿目录：{audio_root}")
    return modules


def clear_stage_outputs(workspace: Path, stage: str, module: str) -> list[str]:
    if stage not in TEST_STAGES:
        raise ValueError(f"不支持的 test stage：{stage}")
    deleted: list[str] = []

    if stage == "audio":
        audio_dir = workspace / "CourseApp" / "public" / "audio" / module
        if audio_dir.exists():
            for path in sorted(audio_dir.glob("*.mp3")):
                if _remove_path(path):
                    deleted.append(str(path))
    elif stage == "mvp":
        # 清理全部可再生产物，只保留工作流/规则源：.agent/、docs/、.env。
        targets = [
            workspace / "scripts",
            workspace / ".agent" / "storyboard" / module,
            workspace / ".agent" / "v0" / module,
            workspace / ".agent" / "design" / module,
        ]
        app = workspace / "CourseApp"
        if app.exists():
            deleted.append(str(app))
            for child in sorted(app.iterdir()):
                if child.name == "node_modules":
                    continue
                if _remove_path(child):
                    deleted.append(str(child))
        for base in targets:
            if base.exists():
                if _remove_path(base):
                    deleted.append(str(base))
    elif stage in {"storyboard", "design"}:
        storyboard_file = workspace / "CourseApp" / "src" / "data" / "storyboard-contract.json"
        if storyboard_file.exists():
            if _remove_path(storyboard_file):
                deleted.append(str(storyboard_file))
        storyboard_dir = workspace / ".agent" / "storyboard" / module
        if storyboard_dir.exists():
            for f in sorted(storyboard_dir.glob("*")):
                if f.is_file():
                    if _remove_path(f):
                        deleted.append(str(f))
        if stage == "storyboard":
            return deleted
        design_file = workspace / "CourseApp" / "src" / "data" / "design-contract.json"
        if design_file.exists():
            if _remove_path(design_file):
                deleted.append(str(design_file))
        brief_dir = workspace / ".agent" / "design" / module
        if brief_dir.exists():
            for f in sorted(brief_dir.glob("*")):
                if f.is_file():
                    if _remove_path(f):
                        deleted.append(str(f))
    return deleted
