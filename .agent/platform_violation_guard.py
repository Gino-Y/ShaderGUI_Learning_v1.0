from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


PLATFORM_DIRS = [".cursor", ".workbuddy"]
AI_ASSET_NAME_MARKERS = [
    "agent",
    "canvas",
    "cursor",
    "dag",
    "handoff",
    "memory",
    "mvp",
    "prompt",
    "rule",
    "skill",
    "workflow",
]
AI_ASSET_EXTENSIONS = {".md", ".mdc", ".json", ".yaml", ".yml", ".txt", ".tsx", ".ts"}


def _is_ai_asset(path: Path) -> bool:
    lowered = path.name.lower()
    if any(marker in lowered for marker in AI_ASSET_NAME_MARKERS):
        return True
    if path.suffix.lower() not in AI_ASSET_EXTENSIONS:
        return False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:4096].lower()
    except OSError:
        return False
    return any(
        marker in text
        for marker in [
            ".agent",
            "skill",
            "workflow",
            "dag",
            "mvp",
            "cursor",
            "workbuddy",
            "storyboard",
            "design contract",
            "stitch",
        ]
    )


def _is_pointer_file(path: Path) -> bool:
    """检查是否是指针文件（指向 .agent/ 的不算违规）"""
    lowered_name = path.name.lower()
    if "pointer" in lowered_name:
        return True
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:500].lower()
        if ".agent/" in text and ("pointer" in text or "指向" in text or "point to" in text):
            return True
    except OSError:
        pass
    return False


def scan_platform_violations(workspace: Path) -> list[Path]:
    violations: list[Path] = []
    for dirname in PLATFORM_DIRS:
        root = workspace / dirname
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            # 指针文件不算违规（它只指向 .agent/ 中的正规路径）
            if _is_pointer_file(path):
                continue
            if _is_ai_asset(path):
                violations.append(path)
    return sorted(violations)


def _relative(workspace: Path, path: Path) -> str:
    return str(path.relative_to(workspace)).replace("\\", "/")


def write_violation_report(workspace: Path, violations: list[Path], action: str) -> Path:
    report_dir = workspace / ".agent" / "reports" / "cleanup"
    report_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report = report_dir / f"platform-violation-{stamp}.md"
    lines = [
        "# Platform Asset Boundary Violation",
        "",
        f"- Detected At: `{datetime.now().isoformat(timespec='seconds')}`",
        f"- Action: `{action}`",
        f"- Violation Count: `{len(violations)}`",
        "",
        "## Files",
        "",
    ]
    for path in violations:
        lines.append(f"- `{_relative(workspace, path)}`")
    lines.extend(
        [
            "",
            "## Required Correction",
            "",
            "Cursor/Codex must not use platform-private AI assets as rule, workflow, DAG, Skill, prompt, or MVP sources.",
            "Move valuable content into `.agent/`, delete duplicates, then rerun the MVP entrypoint.",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    latest = report_dir / "LATEST_PLATFORM_VIOLATION.md"
    latest.write_text(report.read_text(encoding="utf-8"), encoding="utf-8")
    machine = report_dir / "LATEST_PLATFORM_VIOLATION.json"
    machine.write_text(
        json.dumps(
            {
                "status": "failed",
                "action": action,
                "report": _relative(workspace, report),
                "violations": [_relative(workspace, path) for path in violations],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return latest


def quarantine_platform_violations(workspace: Path, violations: list[Path]) -> list[str]:
    quarantine_root = workspace / ".agent" / "reports" / "cleanup" / "quarantine"
    moved: list[str] = []
    for path in violations:
        rel = path.relative_to(workspace)
        target = quarantine_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(target))
        moved.append(str(target.relative_to(workspace)).replace("\\", "/"))
    return moved


def enforce_platform_boundary(workspace: Path, *, fix: bool = False) -> None:
    root = workspace.resolve()
    violations = scan_platform_violations(root)
    if not violations:
        return
    action = "quarantined" if fix else "blocked"
    if fix:
        quarantine_platform_violations(root, violations)
    report = write_violation_report(root, violations, action)
    raise RuntimeError(
        "CURSOR_PLATFORM_VIOLATION: platform-private AI assets detected. "
        f"See {report.relative_to(root)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect platform-private AI assets that violate the .agent boundary.")
    parser.add_argument("--basedir", default=".")
    parser.add_argument("--fix", action="store_true", help="Quarantine violating files under .agent/reports/cleanup/quarantine.")
    args = parser.parse_args()
    workspace = Path(args.basedir).resolve()
    try:
        enforce_platform_boundary(workspace, fix=args.fix)
    except RuntimeError as exc:
        print(str(exc))
        return 1
    print("[OK] no platform-private AI asset violations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
