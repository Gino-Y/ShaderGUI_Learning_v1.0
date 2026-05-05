"""语义审计 storyboard-contract.json"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
contract_path = ROOT / "CourseApp" / "src" / "data" / "storyboard-contract.json"

with open(contract_path, encoding="utf-8") as f:
    c = json.load(f)

print(f"status: {c.get('status')}")
print(f"slides: {len(c.get('slides', []))}\n")

for s in c["slides"]:
    sid = s["slideId"]
    print(f"=== {sid} ===")
    print(f"  audio:     {s.get('audio', 'MISSING')}")
    print(f"  subtitles: {s.get('subtitles', 'MISSING')}")
    print(f"  transcript: {s.get('transcript', 'MISSING')}")
    print(f"  motionCues:      {len(s.get('motionCues', []))}")
    print(f"  visualSpecs:     {len(s.get('visualSpecs', []))}")
    print(f"  performanceSpecs: {len(s.get('performanceSpecs', []))}")

    # 检查 performanceSpecs 类型分布
    pts = {}
    for ps in s.get("performanceSpecs", []):
        pt = ps.get("type", "?")
        dt = ps.get("demo", "-")
        pts.setdefault(pt, []).append(dt)
    print(f"  performance types: {pts}")

    # 检查 timeRange 合理性
    for i, mc in enumerate(s.get("motionCues", [])):
        tr = mc.get("timeRange", {})
        start = tr.get("start")
        end = tr.get("end")
        if start is not None and end is not None and end <= start:
            print(f"  WARN: motionCues[{i}].timeRange end <= start ({start}~{end})")

    # 检查 visualSpecs 与 motionCues 数量是否一致
    if len(s.get("motionCues", [])) != len(s.get("visualSpecs", [])):
        print(f"  WARN: motionCues 与 visualSpecs 数量不一致")

    print()
