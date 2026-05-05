#!/usr/bin/env python3
"""
fix_timeRange.py — 后处理脚本
读取 storyboard-contract.json，根据每个 slide 的 subtitles 文件，
将 motionCues / visualSpecs / performanceSpecs 的 timeRange 对齐到真实的字幕时间段。

用法：python fix_timeRange.py  （在 workspace 根目录执行）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
CONTRACT_FILE = WORKSPACE / "CourseApp" / "src" / "data" / "storyboard-contract.json"


def load_subtitles(workspace: Path, subtitle_path: str) -> list[dict]:
    """加载字幕文件，返回 normalized 的 segment 列表"""
    if not subtitle_path:
        return []
    path = workspace / "CourseApp" / "public" / subtitle_path.lstrip("/")
    if not path.exists():
        print(f"[fix_timeRange] WARNING: subtitle file not found: {path}")
        return []
    try:
        events = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, Exception) as exc:
        print(f"[fix_timeRange] WARNING: failed to parse {path}: {exc}")
        return []
    result = []
    for idx, event in enumerate(events if isinstance(events, list) else []):
        try:
            start = float(event["start"])
            end = float(event["end"])
        except (TypeError, ValueError, KeyError):
            continue
        if end <= start:
            continue
        result.append({
            "segmentIndex": idx,
            "start": start,
            "end": end,
            "text": str(event.get("text", "")),
        })
    return result


def fix_time_range(obj: dict, subtitles: list[dict], field_name: str) -> int:
    """
    修复单个对象（cue 或 spec）的 timeRange。
    根据 trigger.segmentIndex 找到对应字幕段，写入正确的 start/end/durationMs。
    返回修复数量。
    """
    count = 0
    trigger = obj.get("trigger", {})
    seg_idx = trigger.get("segmentIndex")
    if seg_idx is None:
        return 0

    # 找到匹配的字幕段
    segment = None
    for s in subtitles:
        if s["segmentIndex"] == seg_idx:
            segment = s
            break
    if not segment:
        # 没有对应字幕段，保持原样
        return 0

    time_range = obj.get("timeRange", {})
    old_start = time_range.get("start")
    old_end = time_range.get("end")

    new_start = round(segment["start"], 2)
    new_end = round(segment["end"], 2)
    new_duration_ms = max(1, int(round((new_end - new_start) * 1000)))

    if old_start == new_start and old_end == new_end:
        return 0  # 已经正确

    time_range["start"] = new_start
    time_range["end"] = new_end
    time_range["durationMs"] = new_duration_ms
    obj["timeRange"] = time_range

    # 同时修正 trigger.timecode
    trigger["timecode"] = new_start
    obj["trigger"] = trigger

    count += 1
    if count <= 20:  # 避免刷屏
        print(f"  [fix] {field_name}: timeRange {old_start}-{old_end} → {new_start}-{new_end}")
    return count


def process_slide(slide: dict, workspace: Path) -> int:
    """处理单个 slide，返回修复总数"""
    subtitle_path = slide.get("subtitles")
    if not subtitle_path:
        return 0

    subtitles = load_subtitles(workspace, subtitle_path)
    if not subtitles:
        return 0

    total = 0
    print(f"\n[fix_timeRange] {slide['moduleId']}/{slide['slideId']}: {len(subtitles)} subtitle segments")

    # 修复 motionCues
    for cue in slide.get("motionCues", []):
        total += fix_time_range(cue, subtitles, f"motionCue {cue.get('cueId')}")

    # 修复 visualSpecs
    for spec in slide.get("visualSpecs", []):
        total += fix_time_range(spec, subtitles, f"visualSpec {spec.get('cueId')}")

    # 修复 performanceSpecs
    for spec in slide.get("performanceSpecs", []):
        total += fix_time_range(spec, subtitles, f"perfSpec {spec.get('cueId')}")

    return total


def main():
    if not CONTRACT_FILE.exists():
        print(f"[fix_timeRange] ERROR: {CONTRACT_FILE} not found")
        sys.exit(1)

    contract = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    slides = contract.get("slides", [])
    if not slides:
        print("[fix_timeRange] No slides found in contract")
        sys.exit(0)

    total_fixed = 0
    for slide in slides:
        total_fixed += process_slide(slide, WORKSPACE)

    if total_fixed > 0:
        CONTRACT_FILE.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\n[fix_timeRange] ✅ Fixed {total_fixed} timeRange entries, contract updated.")
    else:
        print("\n[fix_timeRange] ℹ️  All timeRange values already correct, no changes made.")


if __name__ == "__main__":
    main()
