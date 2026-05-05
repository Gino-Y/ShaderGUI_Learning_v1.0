#!/usr/bin/env python3
"""
修复 storyboard-contract.json 中的 timeRange 错误。
问题：motionCues 和 performanceSpecs 的 timeRange 全是 {start: 0.0, end: 1.8}
修复：从字幕文件读取正确的时间并替换。
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTRACT_PATH = BASE_DIR / "CourseApp/src/data/storyboard-contract.json"

def fix_contract():
    if not CONTRACT_PATH.exists():
        print(f"契约文件不存在: {CONTRACT_PATH}")
        return False
    
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    fixed_count = 0
    
    for slide in contract.get("slides", []):
        module_id = slide.get("moduleId", "")
        slide_id = slide.get("slideId", "")
        subtitle_path = slide.get("subtitles", "")
        
        if not subtitle_path:
            print(f"  {slide_id}: 无字幕路径，跳过")
            continue
            
        # 加载字幕事件
        subtitle_file = BASE_DIR / "CourseApp/public" / subtitle_path.lstrip("/")
        if not subtitle_file.exists():
            print(f"  {slide_id}: 字幕文件不存在 {subtitle_file}")
            continue
            
        events = json.loads(subtitle_file.read_text(encoding="utf-8"))
        print(f"  {slide_id}: 找到 {len(events)} 个字幕事件")
        
        # 修复 motionCues 的 timeRange
        motion_cues = slide.get("motionCues", [])
        for i, cue in enumerate(motion_cues):
            if i < len(events):
                event = events[i]
                old_range = dict(cue.get("timeRange", {}))
                cue["timeRange"] = {
                    "start": round(event["start"], 2),
                    "end": round(event["end"], 2),
                    "durationMs": int(round((event["end"] - event["start"]) * 1000)),
                }
                print(f"    motionCues[{i}]: {old_range} -> {cue['timeRange']}")
                fixed_count += 1
        
        # 修复 performanceSpecs 的 timeRange
        perf_specs = slide.get("performanceSpecs", [])
        # 构建 cueId -> timeRange 的映射，供 decoration 对齐
        cue_time_map = {}
        for cue in motion_cues:
            cue_time_map[cue["cueId"]] = cue["timeRange"]
        
        for spec in perf_specs:
            spec_cue_id = spec.get("cueId", "")
            # perf-cue-xx -> cue-xx; deco-cue-xx -> cue-xx
            m = re.search(r"(cue-\d+)", spec_cue_id)
            if m:
                target_cue_id = m.group(1)
                if target_cue_id in cue_time_map:
                    old_range = dict(spec.get("timeRange", {}))
                    spec["timeRange"] = dict(cue_time_map[target_cue_id])
                    print(f"    {spec_cue_id} ({spec.get('type','?')}): {old_range} -> {spec['timeRange']}")
                    fixed_count += 1
                elif spec.get("type") == "demo" and events:
                    # demo 找不到对应 cue，用最后一个 event
                    event = events[-1]
                    old_range = dict(spec.get("timeRange", {}))
                    spec["timeRange"] = {
                        "start": round(event["start"], 2),
                        "end": round(event["end"], 2),
                        "durationMs": int(round((event["end"] - event["start"]) * 1000)),
                    }
                    print(f"    {spec_cue_id} (demo,fallback): {old_range} -> {spec['timeRange']}")
                    fixed_count += 1
    
    # 保存修复后的契约
    CONTRACT_PATH.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 修复完成！共修复 {fixed_count} 个 timeRange")
    return True

if __name__ == "__main__":
    print("=== 修复 storyboard-contract.json timeRange ===")
    fix_contract()
