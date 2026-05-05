"""重新生成 Module_01 的 storyboard 合约"""
import sys
import json
from pathlib import Path
import importlib.util

def load_module_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    code = open(filepath, encoding="utf-8-sig").read()
    exec(compile(code, filepath, "exec"), module.__dict__)
    return module

# 加载 storyboard_mcp
mcp_path = Path(__file__).parent / ".agent" / "mcp_servers" / "storyboard_mcp.py"
StoryboardMCP = load_module_from_file("storyboard_mcp", mcp_path).StoryboardMCP

workspace = Path(__file__).parent
module = "Module_01"

print(f"正在为 {module} 生成 storyboard 合约...")
result = StoryboardMCP.prepare_storyboard_contract(workspace, module)
print(f"状态: {result.get('status')}")
print(f"Slide 数量: {result.get('slide_count', 0)}")
if result.get('message'):
    print(f"消息: {result['message'][:200]}")

# 验证 mood 传递
contract_path = workspace / "CourseApp" / "src" / "data" / "storyboard-contract.json"
if contract_path.exists():
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    print(f"\n验证 mood 传递:")
    for slide in contract["slides"][:2]:
        slide_id = slide["slideId"]
        mood = slide.get("paletteIntent", {}).get("mood", "")
        print(f"\n{slide_id}: paletteIntent.mood = {mood!r}")
        for spec in slide.get("performanceSpecs", []):
            if spec.get("type") == "decoration":
                p = spec.get("payload", {})
                print(f"  decoration: payload.mood = {p.get('mood')!r}")
                print(f"  decoration: payload.colors = {p.get('colors')}")
else:
    print("\n❌ storyboard-contract.json 未生成")
