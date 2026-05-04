"""
Visual Spec Schema for native performance nodes.

This schema replaces lottieSpec and extends storyboard
to drive composition, animation, layout, and typography.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
from enum import Enum


class AnimationType(str, Enum):
    NEURAL_CORE = "neural-core"
    CYBER_GRID = "cyber-grid"
    DATA_PRISM = "data-prism"
    PULSE_WAVE = "pulse-wave"
    PARTICLE_VORTEX = "particle-vortex"
    HOLOGRAPHIC_HUD = "holographic-hud"
    FRACTAL_DNA = "fractal-dna"
    AURORA_FLUID = "aurora-fluid"
    FLOATING_NODES = "floating-nodes"
    QUANTUM_ORBIT = "quantum-orbit"


class CompositionSpec:
    """Composition layout specification."""
    frame_grid: str = "left 56% / right 44%"  # CSS grid template
    foreground: dict = field(default_factory=lambda: {
        "position": "left",
        "zone": "hero"
    })
    midground: dict = field(default_factory=lambda: {
        "position": "right",
        "zone": "animation-panel"
    })


class AnimationSpec:
    """Animation node specification."""
    type: AnimationType
    config: dict = field(default_factory=lambda: {
        "color": "#22d3ee",
        "intensity": 0.8,
        "speed": 1.0,
        "loop": True
    })


class LayoutSpec:
    """Layout styling specification."""
    padding: str = "2rem"
    border_radius: str = "1.5rem"
    background: str = "rgba(255,255,255,0.03)"
    blur: str = "backdrop-blur-md"
    border: str = "border-white/10"


class TypographySpec:
    """Typography animation specification."""
    emphasis: Optional[str] = None
    de_emphasize_others: bool = False
    blink: list[str] = field(default_factory=list)
    pulse: list[str] = field(default_factory=list)


class VisualSpec:
    """Complete visual specification for a cue."""
    composition: CompositionSpec = field(default_factory=CompositionSpec)
    animation: Optional[AnimationSpec] = None
    layout: LayoutSpec = field(default_factory=LayoutSpec)
    typography: TypographySpec = field(default_factory=TypographySpec)


def validate_visual_spec(spec: dict) -> dict:
    """
    Validate visualSpec dict against schema.
    
    Returns:
        dict with 'status' and 'errors' (if any)
    """
    errors = []
    
    # Check required fields
    if not isinstance(spec, dict):
        return {"status": "error", "message": "visualSpec must be a dict"}
    
    # Validate animation.type if present
    if "animation" in spec and spec["animation"]:
        anim = spec["animation"]
        if "type" not in anim:
            errors.append("animation.type is required")
        elif anim["type"] not in [e.value for e in AnimationType]:
            errors.append(f"animation.type must be one of: {[e.value for e in AnimationType]}")
    
    # Validate composition.frame_grid if present
    if "composition" in spec:
        comp = spec["composition"]
        if "frame_grid" in comp:
            # Basic validation: should contain grid template
            if not isinstance(comp["frame_grid"], str):
                errors.append("composition.frame_grid must be a string")
    
    if errors:
        return {"status": "error", "errors": errors}
    
    return {"status": "success", "message": "visualSpec validation passed"}
