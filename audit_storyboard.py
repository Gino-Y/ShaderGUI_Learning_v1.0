"""审计 storyboard_mcp.py 生成质量 + 验证合约"""
import sys, json
from pathlib import Path

# 把项目根目录和 .agent 加到 sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / ".agent"))

from mcp_servers.storyboard_mcp import StoryboardMCP
from run_guard import assert_workspace

ws = assert_workspace(ROOT)
print(f"[Audit] workspace = {ws}")

# 1. 重新生成合约（确保是最新逻辑的产物）
print("\n[1] Re-generating storyboard contract...")
gen = StoryboardMCP.prepare_storyboard_contract(ws, "Module_01")
print(f"    generate result: {gen['status']} (slides={gen.get('slide_count')})")

# 2. 运行验证
print("\n[2] Validating storyboard contract...")
contract_path = ws / "CourseApp" / "src" / "data" / "storyboard-contract.json"
val = StoryboardMCP.validate_storyboard_contract(ws, "Module_01", str(contract_path))
print(f"    validate result: {val['status']}")
if val.get("errors"):
    print(f"    ERRORS ({len(val['errors'])}):")
    for err in val["errors"][:10]:
        print(f"      - {err}")
else:
    print("    No errors - contract is clean!")

# 3. 检查 performanceSpecs 是否包含 demo 类型
print("\n[3] Checking performanceSpecs types...")
contract = json.loads(contract_path.read_text(encoding="utf-8"))
for s in contract.get("slides", []):
    types = set(p.get("type") for p in s.get("performanceSpecs", []))
    demo_types = [p.get("demo") for p in s.get("performanceSpecs", []) if p.get("type") == "demo"]
    print(f"    {s['slideId']}: performanceTypes={types}, demoTypes={demo_types}")
