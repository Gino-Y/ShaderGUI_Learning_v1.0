"""
Validate visual specifications.

Replaces validate_lottie.py with visualSpec validation.
"""

from __future__ import annotations

import json
from pathlib import Path
from visual_spec_schema import validate_visual_spec


def validate_visual_file(file_path: str | Path) -> dict:
    """
    Validate a JSON file containing visualSpec.
    
    Args:
        file_path: Path to JSON file with visualSpec
        
    Returns:
        dict: Validation result
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return {"status": "error", "message": f"File not found: {file_path}"}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    errors = []
    
    # Check if data is a dict of cueId -> visualSpec
    if isinstance(data, dict):
        for cue_id, spec in data.items():
            result = validate_visual_spec(spec)
            if result["status"] == "error":
                for error in result.get("errors", []):
                    errors.append(f"{cue_id}: {error}")
    
    # Check if data is a single visualSpec
    elif isinstance(data, dict) and "animation" in data:
        result = validate_visual_spec(data)
        if result["status"] == "error":
            errors.extend(result.get("errors", []))
    
    else:
        errors.append("Invalid format: expected dict of cueId->visualSpec or single visualSpec")
    
    if errors:
        return {
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }
    
    return {"status": "success", "message": "All visualSpec validations passed"}


def validate_storyboard_visuals(storyboard_path: str | Path) -> dict:
    """
    Validate visualSpec in storyboard cues.
    
    Args:
        storyboard_path: Path to storyboard JSON file
        
    Returns:
        dict: Validation result
    """
    storyboard_path = Path(storyboard_path)
    if not storyboard_path.exists():
        return {"status": "error", "message": f"Storyboard not found: {storyboard_path}"}
    
    with open(storyboard_path, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)
    
    errors = []
    warnings = []
    
    for cue in storyboard.get("cues", []):
        cue_id = cue.get("cueId", "unknown")
        visual_spec = cue.get("visualSpec")
        
        if not visual_spec:
            warnings.append(f"{cue_id}: No visualSpec found")
            continue
        
        result = validate_visual_spec(visual_spec)
        if result["status"] == "error":
            for error in result.get("errors", []):
                errors.append(f"{cue_id}: {error}")
    
    result = {
        "status": "success" if not errors else "error",
        "errors": errors,
        "warnings": warnings
    }
    
    if errors:
        result["message"] = f"Validation failed: {len(errors)} error(s)"
    else:
        result["message"] = "All visualSpec validations passed"
    
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate_visual.py <file.json>  # Validate single file")
        print("  python validate_visual.py --storyboard <storyboard.json>  # Validate storyboard")
        sys.exit(1)
    
    if sys.argv[1] == "--storyboard":
        storyboard_path = sys.argv[2]
        result = validate_storyboard_visuals(storyboard_path)
    else:
        file_path = sys.argv[1]
        result = validate_visual_file(file_path)
    
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    if result.get("errors"):
        print("\nErrors:")
        for error in result["errors"]:
            print(f"  - {error}")
    
    if result.get("warnings"):
        print("\nWarnings:")
        for warning in result["warnings"]:
            print(f"  - {warning}")
    
    sys.exit(0 if result["status"] == "success" else 1)
