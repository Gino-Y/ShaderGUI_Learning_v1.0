"""
Build visual specification from storyboard cues.

Replaces build_lottie_from_spec.py with native Vue component approach.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
from visual_spec_schema import VisualSpec, AnimationType, validate_visual_spec


def build_visual_from_storyboard(storyboard_path: str | Path) -> dict:
    """
    Build visualSpec JSON from storyboard file.
    
    Args:
        storyboard_path: Path to storyboard JSON file
        
    Returns:
        dict: Mapping of cueId -> visualSpec
    """
    storyboard_path = Path(storyboard_path)
    if not storyboard_path.exists():
        return {"status": "error", "message": f"Storyboard not found: {storyboard_path}"}
    
    with open(storyboard_path, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)
    
    result = {"status": "success", "visual_specs": {}}
    
    for cue in storyboard.get("cues", []):
        cue_id = cue.get("cueId")
        if not cue_id:
            continue
        
        # Build visualSpec from cue
        visual_spec = build_visual_for_cue(cue)
        result["visual_specs"][cue_id] = visual_spec
    
    return result


def build_visual_for_cue(cue: dict) -> dict:
    """
    Build visualSpec for a single cue.
    
    This is where storyboard cues get translated into
    native Vue component specifications.
    """
    # Default: use neural-core for concept cues
    animation_type = "neural-core"
    
    # Map cue content to animation type
    content = cue.get("contentBeat", "").lower()
    knowledge = cue.get("knowledgeFocus", {}).get("label", "").lower()
    
    if "scan" in content or "system" in content:
        animation_type = "cyber-grid"
    elif "3d" in content or "structure" in content:
        animation_type = "data-prism"
    elif "energy" in content or "pulse" in content:
        animation_type = "pulse-wave"
    elif "particle" in content or "flow" in content:
        animation_type = "particle-vortex"
    elif "holographic" in content or "interface" in content:
        animation_type = "holographic-hud"
    elif "dna" in content or "genetic" in content:
        animation_type = "fractal-dna"
    elif "fluid" in content or "aurora" in content:
        animation_type = "aurora-fluid"
    elif "network" in content or "node" in content:
        animation_type = "floating-nodes"
    elif "quantum" in content or "orbit" in content:
        animation_type = "quantum-orbit"
    
    visual_spec = {
        "composition": {
            "frame_grid": "left 56% / right 44%",
            "foreground": {"position": "left", "zone": "hero"},
            "midground": {"position": "right", "zone": "animation-panel"}
        },
        "animation": {
            "type": animation_type,
            "config": {
                "color": "#22d3ee",
                "intensity": 0.8,
                "speed": 1.0,
                "loop": True
            }
        },
        "layout": {
            "padding": "2rem",
            "border_radius": "1.5rem",
            "background": "rgba(255,255,255,0.03)",
            "blur": "backdrop-blur-md",
            "border": "border-white/10"
        },
        "typography": {
            "emphasis": cue.get("cueId"),
            "de_emphasize_others": True,
            "blink": [],
            "pulse": []
        }
    }
    
    return visual_spec


def save_visual_specs(visual_specs: dict, output_path: str | Path) -> dict:
    """
    Save visualSpec mappings to JSON file.
    
    Args:
        visual_specs: Dict of cueId -> visualSpec
        output_path: Path to output JSON file
        
    Returns:
        dict: Status and output path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(visual_specs, f, indent=2, ensure_ascii=False)
    
    return {
        "status": "success",
        "output_path": str(output_path),
        "count": len(visual_specs)
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python build_visual_from_spec.py <storyboard.json> <output.json>")
        sys.exit(1)
    
    storyboard_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Build visual specs
    result = build_visual_from_storyboard(storyboard_path)
    
    if result["status"] == "error":
        print(f"Error: {result['message']}")
        sys.exit(1)
    
    # Save to output
    save_result = save_visual_specs(result["visual_specs"], output_path)
    
    print(f"✅ Generated {save_result['count']} visualSpecs")
    print(f"📁 Output: {save_result['output_path']}")
