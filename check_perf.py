import json

with open("CourseApp/src/data/storyboard-contract.json", encoding="utf-8") as f:
    d = json.load(f)

for slide in d["slides"][:2]:
    print(f"=== {slide['slideId']} ===")
    specs = slide.get("performanceSpecs", [])
    print(f"  performanceSpecs count: {len(specs)}")
    for spec in specs:
        cue_id = spec.get("cueId", "??")
        typ = spec.get("type", "??")
        tr = spec.get("timeRange", "MISSING")
        demo = spec.get("demo", "N/A")
        print(f"  cueId={cue_id} type={typ} timeRange={tr} demo={demo}")
    print()
