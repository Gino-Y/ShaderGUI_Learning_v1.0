from pathlib import Path
import sys
import json

sys.path.insert(0, '.agent/mcp_servers')
import storyboard_mcp

workspace = Path('.')

# 测试 p01
print("=== Testing p01 ===")
subtitle_path = '/subtitles/Module_01/p01.json'

# 模拟 p01 的 points (从 slides.json 读取)
slides_path = Path('CourseApp/src/data/slides.json')
slides_data = json.loads(slides_path.read_text(encoding='utf-8'))
# slides.json 是列表
p01 = next((s for s in slides_data if s['slideId'] == 'p01'), None)
if p01:
    points = p01.get('points', [])
    print(f"p01 points ({len(points)}):")
    for i, p in enumerate(points):
        print(f"  [{i}] {p[:50]}")
    
    # 测试 _load_subtitle_events
    subtitle_events = storyboard_mcp.StoryboardMCP._load_subtitle_events(workspace, subtitle_path)
    print(f"\nSubtitle events ({len(subtitle_events)}):")
    for e in subtitle_events[:5]:
        print(f"  [{e['segmentIndex']}] {e['start']}-{e['end']} | {e['text'][:30]}")
    
    # 测试 _align_points_to_subtitles
    alignments = storyboard_mcp.StoryboardMCP._align_points_to_subtitles(points, subtitle_events)
    print(f"\nAlignments ({len(alignments)}):")
    for i, a in enumerate(alignments):
        if a:
            print(f"  point[{i}] -> event[{a['segmentIndex']}]: start={a['start']}, end={a['end']}")
        else:
            print(f"  point[{i}] -> None")
    
    # 测试 _motion_cues
    print(f"\nMotion cues:")
    cues = storyboard_mcp.StoryboardMCP._motion_cues(workspace, 'concept', points, subtitle_path)
    for c in cues:
        print(f"  {c['cueId']}: timeRange={c['timeRange']}")
else:
    print("p01 not found in slides.json")
