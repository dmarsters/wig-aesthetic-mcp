"""
Wig Design Aesthetic MCP Server

Three-layer architecture for wig design composition:
- Layer 1: Pure taxonomy (cap construction, texture, density, color)
- Layer 2: Deterministic parameter→vocabulary mapping (0 tokens)
- Layer 3: Creative synthesis with LLM (~200 tokens)

Achieves ~60% cost savings through categorical composition.
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional
import json

mcp = FastMCP("Wig Aesthetic")

# ============================================================================
# LAYER 1: TAXONOMY DEFINITIONS
# ============================================================================

CAP_CONSTRUCTIONS = {
    "lace_front": {
        "name": "Lace Front",
        "parting_freedom": "hairline_only",
        "visibility": "transparent_hairline",
        "vocabulary": "invisible lace hairline transition, individual strand implantation visible at forehead, pre-plucked density graduation"
    },
    "monofilament": {
        "name": "Monofilament Top",
        "parting_freedom": "full",
        "visibility": "scalp_simulation",
        "vocabulary": "monofilament scalp-like top, individual strand knotting visible, natural directional flow from crown, free-form parting capability"
    },
    "full_lace": {
        "name": "Full Lace",
        "parting_freedom": "full",
        "visibility": "transparent_entire",
        "vocabulary": "full lace cap construction, 360-degree transparency, individual hand-tied strands throughout, maximum styling versatility"
    },
    "wefted": {
        "name": "Wefted/Traditional",
        "parting_freedom": "constrained",
        "visibility": "standard",
        "vocabulary": "machine-wefted construction, defined weft lines, structured parting, economical density distribution"
    },
    "hand_tied": {
        "name": "Hand-Tied",
        "parting_freedom": "moderate",
        "visibility": "natural_movement",
        "vocabulary": "hand-tied individual strands, natural movement and flow, reduced bulk, breathable construction"
    },
    "capless": {
        "name": "Capless/Open-Wefted",
        "parting_freedom": "constrained",
        "visibility": "lightweight",
        "vocabulary": "open-wefted ventilated construction, lightweight feel, visible weft structure, maximum airflow"
    },
    "360_lace": {
        "name": "360 Lace",
        "parting_freedom": "perimeter",
        "visibility": "transparent_perimeter",
        "vocabulary": "360-degree lace perimeter, transparent edges all around, center wefted, high ponytail capability"
    }
}

TEXTURE_PATTERNS = {
    "straight": {
        "name": "Straight",
        "curl_type": "1A-1C",
        "wave_geometry": "none",
        "vocabulary": "sleek straight texture, no wave pattern, reflective shaft alignment, smooth uniform direction"
    },
    "body_wave": {
        "name": "Body Wave",
        "curl_type": "2A-2B",
        "wave_geometry": "loose_S",
        "vocabulary": "cascading body waves, loose S-curve pattern, 3-4 inch wavelength, medium spring and bounce"
    },
    "deep_wave": {
        "name": "Deep Wave",
        "curl_type": "2C-3A",
        "wave_geometry": "tight_S",
        "vocabulary": "deep wave texture, tight S-curve waves, 2-3 inch wavelength, pronounced spring, defined wave crests"
    },
    "loose_curl": {
        "name": "Loose Curl",
        "curl_type": "3A-3B",
        "wave_geometry": "spiral_loose",
        "vocabulary": "loose spiral curls, 1-2 inch curl diameter, defined ringlets, bouncy spring pattern"
    },
    "tight_curl": {
        "name": "Tight Curl",
        "curl_type": "3C",
        "wave_geometry": "spiral_tight",
        "vocabulary": "tight corkscrew curls, pencil-width diameter, dense curl definition, high spring coil pattern"
    },
    "kinky_straight": {
        "name": "Kinky Straight",
        "curl_type": "4A",
        "wave_geometry": "textured_straight",
        "vocabulary": "kinky straight texture, subtle bend pattern, coarse texture visibility, natural body without curl"
    },
    "kinky_curly": {
        "name": "Kinky Curly",
        "curl_type": "4B",
        "wave_geometry": "zigzag",
        "vocabulary": "kinky curly texture, tight zigzag pattern, dense coil structure, maximum volume and spring"
    },
    "coily": {
        "name": "Coily",
        "curl_type": "4C",
        "wave_geometry": "tight_coil",
        "vocabulary": "tight coily texture, densely packed coil springs, minimal definition, maximum shrinkage and volume"
    }
}

EDGE_TREATMENTS = {
    "baby_hairs": "fine 1-2 inch wispy baby hairs along perimeter, irregular natural distribution, delicate texture",
    "temple_points": "defined temple point detail, natural recession simulation, gradual density fade at temples",
    "clean": "clean finished hairline, uniform density to edge, no wispy detail",
    "layered": "graduated edge layering, soft perimeter transition, dimensional endpoint"
}

COLOR_HIGHLIGHT_PATTERNS = {
    "ribbon": "vertical highlight ribbons, 1-2 strand width, precise placement, contrasting dimension",
    "balayage": "hand-painted balayage highlights, irregular organic placement, graduated intensity toward ends",
    "ombre": "ombre gradient transition, horizontal color fade, distinct root-to-tip progression",
    "peek_a_boo": "peek-a-boo underlayer highlights, hidden color reveals, dimensional depth underneath",
    "full": "full dimensional coloring, integrated highlight distribution throughout, natural sun-kissed effect"
}

STYLE_CONTEXTS = {
    "natural": {
        "density_target": 1.0,
        "edge_preference": "baby_hairs",
        "volume_profile": {"crown": 1.0, "temple": 1.0, "nape": 1.0},
        "focus": "realistic scalp simulation, natural movement"
    },
    "theatrical": {
        "density_target": 1.5,
        "edge_preference": "clean",
        "volume_profile": {"crown": 1.3, "temple": 1.1, "nape": 1.2},
        "focus": "dramatic volume, bold silhouette"
    },
    "editorial": {
        "density_target": 1.4,
        "edge_preference": "layered",
        "volume_profile": {"crown": 1.4, "temple": 0.9, "nape": 1.0},
        "focus": "sculptural shape, architectural volume"
    },
    "cosplay": {
        "density_target": 1.6,
        "edge_preference": "clean",
        "volume_profile": {"crown": 1.5, "temple": 1.3, "nape": 1.4},
        "focus": "character accuracy, extreme styling capability"
    },
    "medical": {
        "density_target": 0.9,
        "edge_preference": "baby_hairs",
        "volume_profile": {"crown": 0.95, "temple": 0.95, "nape": 0.95},
        "focus": "comfort, natural appearance, breathability"
    }
}


# ============================================================================
# PHASE 2.6: MORPHOSPACE COORDINATES & RHYTHMIC PRESETS
# ============================================================================
#
# Normalized 5D parameter space capturing wig aesthetic variation.
# Each parameter ranges [0.0, 1.0] for compatibility with aesthetic-dynamics-core.
#
# Parameters:
#   construction_transparency - Opacity of cap structure
#       0.0 = opaque wefted/capless (visible structure)
#       1.0 = fully transparent lace (invisible construction)
#
#   texture_curl_intensity - Curl pattern tightness
#       0.0 = pin-straight (type 1A)
#       1.0 = tight coily (type 4C)
#
#   density_volume - Hair density and resulting volume
#       0.0 = sparse, lightweight, scalp-visible
#       1.0 = ultra-dense, maximum theatrical volume
#
#   color_dimension - Complexity of color treatment
#       0.0 = flat solid single color
#       1.0 = complex multi-technique dimensional color
#
#   styling_drama - Overall aesthetic intensity
#       0.0 = understated medical/comfort focus
#       1.0 = extreme theatrical/cosplay presentation
#

WIG_PARAMETER_NAMES = [
    "construction_transparency",
    "texture_curl_intensity",
    "density_volume",
    "color_dimension",
    "styling_drama"
]

# Canonical states in 5D morphospace
# Each maps a recognizable wig aesthetic archetype to coordinates
WIG_MORPHOSPACE_COORDS = {
    "everyday_natural": {
        "construction_transparency": 0.60,
        "texture_curl_intensity": 0.25,
        "density_volume": 0.50,
        "color_dimension": 0.15,
        "styling_drama": 0.20
    },
    "red_carpet_glam": {
        "construction_transparency": 0.90,
        "texture_curl_intensity": 0.40,
        "density_volume": 0.70,
        "color_dimension": 0.75,
        "styling_drama": 0.80
    },
    "editorial_sculpt": {
        "construction_transparency": 0.75,
        "texture_curl_intensity": 0.05,
        "density_volume": 0.65,
        "color_dimension": 0.50,
        "styling_drama": 0.85
    },
    "theatrical_volume": {
        "construction_transparency": 0.30,
        "texture_curl_intensity": 0.45,
        "density_volume": 0.90,
        "color_dimension": 0.60,
        "styling_drama": 0.95
    },
    "protective_crown": {
        "construction_transparency": 0.55,
        "texture_curl_intensity": 0.85,
        "density_volume": 0.55,
        "color_dimension": 0.10,
        "styling_drama": 0.30
    },
    "fantasy_extreme": {
        "construction_transparency": 1.00,
        "texture_curl_intensity": 0.50,
        "density_volume": 1.00,
        "color_dimension": 1.00,
        "styling_drama": 1.00
    },
    "medical_comfort": {
        "construction_transparency": 0.45,
        "texture_curl_intensity": 0.20,
        "density_volume": 0.40,
        "color_dimension": 0.05,
        "styling_drama": 0.05
    },
    "textured_natural": {
        "construction_transparency": 0.65,
        "texture_curl_intensity": 0.75,
        "density_volume": 0.60,
        "color_dimension": 0.20,
        "styling_drama": 0.35
    }
}

# Phase 2.6 Rhythmic Presets
# Periods chosen for strategic interaction with existing domains:
#   22 - unique to wig, near catastrophe's 22
#   18 - shared with nuclear/diatom (multi-domain resonance)
#   28 - matches the composite beat period (cross-domain coupling)
#   14 - unique low period (gap-filler candidate at 12-15)
#   20 - shared with microscopy/catastrophe/diatom (3-domain sync)
WIG_RHYTHMIC_PRESETS = {
    "texture_morph": {
        "state_a": "everyday_natural",
        "state_b": "textured_natural",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 22,
        "description": "Smooth oscillation between straight/wavy and curly/coily textures"
    },
    "density_breathe": {
        "state_a": "medical_comfort",
        "state_b": "theatrical_volume",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": "Volume expansion/contraction cycle from sparse comfort to dramatic fullness"
    },
    "drama_sweep": {
        "state_a": "everyday_natural",
        "state_b": "red_carpet_glam",
        "pattern": "triangular",
        "num_cycles": 2,
        "steps_per_cycle": 28,
        "description": "Linear ramp from understated natural to full glamour presentation"
    },
    "construction_shift": {
        "state_a": "theatrical_volume",
        "state_b": "editorial_sculpt",
        "pattern": "sinusoidal",
        "num_cycles": 5,
        "steps_per_cycle": 14,
        "description": "Rapid oscillation between opaque theatrical and transparent editorial construction"
    },
    "color_pulse": {
        "state_a": "protective_crown",
        "state_b": "fantasy_extreme",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 20,
        "description": "Color dimensionality cycling from minimal flat tone to complex multi-technique"
    }
}


# ============================================================================
# PHASE 2.7: VISUAL VOCABULARY FOR ATTRACTOR VISUALIZATION
# ============================================================================
#
# Maps regions of wig morphospace to image-generation-ready keywords.
# Each visual type represents a canonical aesthetic archetype with
# distinct visual vocabulary suitable for AI image generation.
#

WIG_VISUAL_TYPES = {
    "natural_realism": {
        "coords": {
            "construction_transparency": 0.60,
            "texture_curl_intensity": 0.25,
            "density_volume": 0.50,
            "color_dimension": 0.15,
            "styling_drama": 0.20
        },
        "keywords": [
            "invisible hairline blending into skin",
            "natural strand movement with light bounce",
            "realistic scalp visibility through parting",
            "soft body wave catching ambient light",
            "understated everyday hairstyle",
            "believable biological hair texture"
        ],
        "optical_properties": {
            "finish": "satin",
            "light_interaction": "diffuse_scatter",
            "sheen_level": "moderate"
        },
        "color_associations": [
            "warm brunettes", "natural blacks", "honey blondes",
            "subtle warm undertones"
        ]
    },
    "glamour_cascade": {
        "coords": {
            "construction_transparency": 0.90,
            "texture_curl_intensity": 0.40,
            "density_volume": 0.75,
            "color_dimension": 0.80,
            "styling_drama": 0.80
        },
        "keywords": [
            "luxurious cascading waves",
            "voluminous body with dimensional highlights",
            "hand-painted balayage color depth",
            "red carpet volumetric silhouette",
            "high-gloss strand reflections",
            "dramatic root shadow fading to bright ends",
            "movement-rich layered flow"
        ],
        "optical_properties": {
            "finish": "high_gloss",
            "light_interaction": "specular_ribbon",
            "sheen_level": "high"
        },
        "color_associations": [
            "champagne highlights", "rose gold tones", "caramel ribbons",
            "multi-tonal blonde dimension", "warm copper accents"
        ]
    },
    "editorial_sculpture": {
        "coords": {
            "construction_transparency": 0.75,
            "texture_curl_intensity": 0.05,
            "density_volume": 0.65,
            "color_dimension": 0.50,
            "styling_drama": 0.85
        },
        "keywords": [
            "architectural hair silhouette",
            "razor-sharp geometric edges",
            "sculptural volume at crown tapering to points",
            "sleek pin-straight reflective sheets",
            "fashion editorial precision styling",
            "dramatic asymmetric shape",
            "high-contrast structural form"
        ],
        "optical_properties": {
            "finish": "mirror_gloss",
            "light_interaction": "planar_reflection",
            "sheen_level": "extreme"
        },
        "color_associations": [
            "jet black mirror finish", "platinum ice blonde",
            "stark monochrome", "electric fashion colors"
        ]
    },
    "textured_crown": {
        "coords": {
            "construction_transparency": 0.60,
            "texture_curl_intensity": 0.85,
            "density_volume": 0.60,
            "color_dimension": 0.15,
            "styling_drama": 0.35
        },
        "keywords": [
            "densely packed coil springs",
            "voluminous natural afro silhouette",
            "tight curl definition with shrinkage",
            "crown of kinky-curly texture",
            "matte coil surface absorbing light",
            "celebrating natural 4B-4C pattern",
            "protective styling versatility"
        ],
        "optical_properties": {
            "finish": "matte_velvet",
            "light_interaction": "diffuse_absorb",
            "sheen_level": "low"
        },
        "color_associations": [
            "deep espresso browns", "blue-black depth",
            "warm chestnut undertones", "natural dark richness"
        ]
    }
}

# ============================================================================
# LAYER 2: DETERMINISTIC MAPPING FUNCTIONS (0 TOKENS)
# ============================================================================

def map_density_vocabulary(density: float) -> str:
    """Map density value to descriptive vocabulary."""
    if density < 0.8:
        return f"{int(density*100)}% density, lightweight sparse construction, visible scalp through strands"
    elif density < 1.0:
        return f"{int(density*100)}% density, natural lightweight fullness, subtle scalp visibility"
    elif density == 1.0:
        return "100% natural density, realistic fullness matching biological hair"
    elif density <= 1.3:
        return f"{int(density*100)}% density, enhanced fullness, voluminous appearance"
    elif density <= 1.6:
        return f"{int(density*100)}% density, dramatic volume, luxurious thickness"
    else:
        return f"{int(density*100)}% density, maximum theatrical volume, ultra-dense construction"

def map_length_vocabulary(length_primary: int, layers: Optional[List[int]] = None) -> str:
    """Map length parameters to vocabulary."""
    vocab = f"{length_primary}-inch primary length"
    
    if layers:
        layer_desc = ", ".join([f"{l}-inch" for l in sorted(layers, reverse=True)])
        vocab += f", with graduated layers at {layer_desc}"
        vocab += ", creating dimensional movement and reduced weight"
    
    return vocab

def map_volume_distribution(distribution: Dict[str, float]) -> str:
    """Map volume distribution to geometric vocabulary."""
    vocab_parts = []
    
    for zone, multiplier in distribution.items():
        if multiplier > 1.2:
            vocab_parts.append(f"dramatic {zone} lift creating {multiplier:.1f}x natural height")
        elif multiplier > 1.05:
            vocab_parts.append(f"enhanced {zone} volume at {multiplier:.1f}x natural")
        elif multiplier < 0.9:
            vocab_parts.append(f"compressed {zone} profile at {multiplier:.1f}x natural")
        else:
            vocab_parts.append(f"natural {zone} proportion")
    
    return ", ".join(vocab_parts)

def map_color_dimension_vocabulary(
    base_color: str,
    dimensional: bool,
    highlight_pattern: Optional[str] = None,
    root_shadow_depth: float = 0.0
) -> str:
    """Map color parameters to vocabulary."""
    vocab = f"{base_color} base color"
    
    if not dimensional:
        return vocab + ", solid uniform color throughout"
    
    vocab += ", dimensional coloring with"
    
    if root_shadow_depth > 0:
        vocab += f" {root_shadow_depth}-inch root shadow fade creating depth,"
    
    if highlight_pattern and highlight_pattern in COLOR_HIGHLIGHT_PATTERNS:
        vocab += f" {COLOR_HIGHLIGHT_PATTERNS[highlight_pattern]}"
    
    return vocab

# ============================================================================
# LAYER 2: MCP TOOLS - DETERMINISTIC OPERATIONS
# ============================================================================

@mcp.tool()
def list_wig_taxonomy() -> str:
    """
    List all available wig design taxonomy categories.
    
    Returns complete vocabulary reference for:
    - Cap constructions (7 types)
    - Texture patterns (8 types)
    - Edge treatments (4 types)
    - Color highlight patterns (5 types)
    - Style contexts (5 types)
    
    Cost: 0 tokens (pure taxonomy lookup)
    """
    taxonomy = {
        "cap_constructions": list(CAP_CONSTRUCTIONS.keys()),
        "texture_patterns": list(TEXTURE_PATTERNS.keys()),
        "edge_treatments": list(EDGE_TREATMENTS.keys()),
        "color_highlight_patterns": list(COLOR_HIGHLIGHT_PATTERNS.keys()),
        "style_contexts": list(STYLE_CONTEXTS.keys())
    }
    return json.dumps(taxonomy, indent=2)

@mcp.tool()
def get_cap_construction_details(construction_id: str) -> str:
    """
    Get detailed specifications for a cap construction type.
    
    Args:
        construction_id: One of: lace_front, monofilament, full_lace, 
                        wefted, hand_tied, capless, 360_lace
    
    Returns complete visual vocabulary and structural properties.
    Cost: 0 tokens (pure lookup)
    """
    if construction_id not in CAP_CONSTRUCTIONS:
        return json.dumps({"error": f"Unknown construction: {construction_id}",
                          "available": list(CAP_CONSTRUCTIONS.keys())})
    
    return json.dumps(CAP_CONSTRUCTIONS[construction_id], indent=2)

@mcp.tool()
def get_texture_pattern_details(texture_id: str) -> str:
    """
    Get detailed specifications for a texture pattern.
    
    Args:
        texture_id: One of: straight, body_wave, deep_wave, loose_curl,
                   tight_curl, kinky_straight, kinky_curly, coily
    
    Returns wave geometry, curl classification, and visual vocabulary.
    Cost: 0 tokens (pure lookup)
    """
    if texture_id not in TEXTURE_PATTERNS:
        return json.dumps({"error": f"Unknown texture: {texture_id}",
                          "available": list(TEXTURE_PATTERNS.keys())})
    
    return json.dumps(TEXTURE_PATTERNS[texture_id], indent=2)

@mcp.tool()
def map_wig_parameters(
    cap_construction: str,
    texture_pattern: str,
    density_profile: float,
    length_primary: int,
    base_color: str,
    color_dimensional: bool = False,
    highlight_pattern: Optional[str] = None,
    root_shadow_depth: float = 0.0,
    edge_treatment: str = "baby_hairs",
    layers: Optional[str] = None,
    volume_distribution: Optional[str] = None
) -> str:
    """
    LAYER 2: Deterministic mapping from parameters to visual vocabulary.
    
    Maps wig design parameters to image-generation-ready vocabulary
    through pure categorical composition. No LLM inference.
    
    Args:
        cap_construction: Cap type (lace_front, monofilament, etc.)
        texture_pattern: Texture (straight, body_wave, deep_wave, etc.)
        density_profile: Density multiplier (0.5-2.0, 1.0 = natural)
        length_primary: Primary length in inches
        base_color: Base color description
        color_dimensional: Enable dimensional coloring
        highlight_pattern: Pattern (ribbon, balayage, ombre, peek_a_boo, full)
        root_shadow_depth: Root shadow depth in inches (0-3)
        edge_treatment: Edge style (baby_hairs, temple_points, clean, layered)
        layers: JSON string of layer lengths, e.g. "[12, 14, 16]"
        volume_distribution: JSON string, e.g. '{"crown": 1.4, "temple": 0.9}'
    
    Returns:
        JSON with complete visual vocabulary mapped from parameters
    
    Cost: 0 tokens (deterministic taxonomy mapping)
    """
    # Validate inputs
    if cap_construction not in CAP_CONSTRUCTIONS:
        return json.dumps({"error": f"Unknown cap construction: {cap_construction}"})
    
    if texture_pattern not in TEXTURE_PATTERNS:
        return json.dumps({"error": f"Unknown texture pattern: {texture_pattern}"})
    
    if edge_treatment not in EDGE_TREATMENTS:
        return json.dumps({"error": f"Unknown edge treatment: {edge_treatment}"})
    
    # Parse optional JSON parameters
    layer_list = json.loads(layers) if layers else None
    volume_dict = json.loads(volume_distribution) if volume_distribution else {"crown": 1.0, "temple": 1.0, "nape": 1.0}
    
    # Build vocabulary through deterministic mapping
    vocabulary_components = {
        "cap_construction": CAP_CONSTRUCTIONS[cap_construction]["vocabulary"],
        "texture": TEXTURE_PATTERNS[texture_pattern]["vocabulary"],
        "density": map_density_vocabulary(density_profile),
        "length": map_length_vocabulary(length_primary, layer_list),
        "color": map_color_dimension_vocabulary(base_color, color_dimensional, highlight_pattern, root_shadow_depth),
        "edge": EDGE_TREATMENTS[edge_treatment],
        "volume": map_volume_distribution(volume_dict)
    }
    
    # Composite vocabulary string
    composite_vocabulary = "; ".join([
        vocabulary_components["cap_construction"],
        vocabulary_components["texture"],
        vocabulary_components["density"],
        vocabulary_components["length"],
        vocabulary_components["volume"],
        vocabulary_components["edge"],
        vocabulary_components["color"]
    ])
    
    result = {
        "parameters": {
            "cap_construction": cap_construction,
            "texture_pattern": texture_pattern,
            "density_profile": density_profile,
            "length_primary": length_primary,
            "base_color": base_color,
            "color_dimensional": color_dimensional,
            "edge_treatment": edge_treatment
        },
        "vocabulary_components": vocabulary_components,
        "composite_vocabulary": composite_vocabulary,
        "cost_profile": {
            "layer_2_tokens": 0,
            "methodology": "deterministic_taxonomy_mapping"
        }
    }
    
    return json.dumps(result, indent=2)

@mcp.tool()
def apply_style_context(
    base_parameters: str,
    style: str = "natural"
) -> str:
    """
    Apply style context presets to base parameters.
    
    Style contexts adjust density, volume, and edge treatment for:
    - natural: Realistic everyday wear
    - theatrical: Stage/performance drama
    - editorial: Fashion photography
    - cosplay: Character accuracy
    - medical: Comfort-focused
    
    Args:
        base_parameters: JSON string from map_wig_parameters
        style: Style context (natural, theatrical, editorial, cosplay, medical)
    
    Returns:
        Modified parameters with style adjustments applied
    
    Cost: 0 tokens (deterministic modification)
    """
    if style not in STYLE_CONTEXTS:
        return json.dumps({"error": f"Unknown style: {style}",
                          "available": list(STYLE_CONTEXTS.keys())})
    
    base = json.loads(base_parameters)
    context = STYLE_CONTEXTS[style]
    
    # Apply style modifications
    params = base["parameters"]
    params["density_profile"] = context["density_target"]
    params["edge_treatment"] = context["edge_preference"]
    
    # Rebuild vocabulary with new parameters
    volume_json = json.dumps(context["volume_profile"])
    
    result = map_wig_parameters(
        params["cap_construction"],
        params["texture_pattern"],
        params["density_profile"],
        params["length_primary"],
        params["base_color"],
        params.get("color_dimensional", False),
        params.get("highlight_pattern"),
        params.get("root_shadow_depth", 0.0),
        params["edge_treatment"],
        json.dumps(params.get("layers", [])) if params.get("layers") else None,
        volume_json
    )
    
    result_dict = json.loads(result)
    result_dict["style_context"] = {
        "style": style,
        "focus": context["focus"]
    }
    
    return json.dumps(result_dict, indent=2)


# ============================================================================
# PHASE 2.6: RHYTHMIC COMPOSITION TOOLS
# ============================================================================

import math
import numpy as np


def _generate_oscillation(num_steps: int, num_cycles: float, pattern: str):
    """Generate oscillation alpha values [0, 1]."""
    t = [2 * math.pi * num_cycles * i / num_steps for i in range(num_steps)]

    if pattern == "sinusoidal":
        return [0.5 * (1 + math.sin(ti)) for ti in t]
    elif pattern == "triangular":
        result = []
        for ti in t:
            t_norm = (ti / (2 * math.pi)) % 1.0
            result.append(2 * t_norm if t_norm < 0.5 else 2 * (1 - t_norm))
        return result
    elif pattern == "square":
        return [0.0 if (ti / (2 * math.pi)) % 1.0 < 0.5 else 1.0 for ti in t]
    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def _interpolate_states(state_a: dict, state_b: dict, alpha: float) -> dict:
    """Linearly interpolate between two morphospace states."""
    return {
        p: state_a[p] * (1 - alpha) + state_b[p] * alpha
        for p in WIG_PARAMETER_NAMES
    }


def _generate_preset_trajectory(preset_name: str) -> list:
    """Generate full trajectory for a Phase 2.6 preset.

    Returns list of state dicts representing one complete rhythmic sequence.
    """
    if preset_name not in WIG_RHYTHMIC_PRESETS:
        raise ValueError(f"Unknown preset: {preset_name}")

    config = WIG_RHYTHMIC_PRESETS[preset_name]
    state_a = WIG_MORPHOSPACE_COORDS[config["state_a"]]
    state_b = WIG_MORPHOSPACE_COORDS[config["state_b"]]
    total_steps = config["num_cycles"] * config["steps_per_cycle"]

    alphas = _generate_oscillation(total_steps, config["num_cycles"], config["pattern"])
    return [_interpolate_states(state_a, state_b, a) for a in alphas]


@mcp.tool()
def list_wig_rhythmic_presets() -> str:
    """
    List all Phase 2.6 rhythmic presets for wig aesthetics.

    Returns preset names, periods, patterns, and descriptions.
    Cost: 0 tokens (pure taxonomy lookup)
    """
    presets = {}
    for name, config in WIG_RHYTHMIC_PRESETS.items():
        presets[name] = {
            "period": config["steps_per_cycle"],
            "total_steps": config["num_cycles"] * config["steps_per_cycle"],
            "pattern": config["pattern"],
            "states": f"{config['state_a']} ↔ {config['state_b']}",
            "description": config["description"]
        }

    return json.dumps({
        "domain": "wig_aesthetic",
        "presets": presets,
        "available_periods": sorted(set(
            c["steps_per_cycle"] for c in WIG_RHYTHMIC_PRESETS.values()
        )),
        "available_states": list(WIG_MORPHOSPACE_COORDS.keys()),
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def get_wig_morphospace_coordinates(state_id: str = "") -> str:
    """
    Get morphospace coordinates for wig aesthetic states.

    Args:
        state_id: Specific state to look up, or empty string for all states.

    Returns 5D normalized coordinates in wig morphospace.
    Cost: 0 tokens (pure lookup)
    """
    if state_id:
        if state_id not in WIG_MORPHOSPACE_COORDS:
            return json.dumps({
                "error": f"Unknown state: {state_id}",
                "available": list(WIG_MORPHOSPACE_COORDS.keys())
            })
        return json.dumps({
            "state_id": state_id,
            "coordinates": WIG_MORPHOSPACE_COORDS[state_id],
            "parameter_names": WIG_PARAMETER_NAMES
        }, indent=2)

    return json.dumps({
        "states": WIG_MORPHOSPACE_COORDS,
        "parameter_names": WIG_PARAMETER_NAMES,
        "total_states": len(WIG_MORPHOSPACE_COORDS)
    }, indent=2)


@mcp.tool()
def generate_wig_rhythmic_sequence(
    preset_name: str = "",
    state_a_id: str = "",
    state_b_id: str = "",
    oscillation_pattern: str = "sinusoidal",
    num_cycles: int = 3,
    steps_per_cycle: int = 20,
    phase_offset: float = 0.0
) -> str:
    """
    Generate rhythmic oscillation between two wig aesthetic states.

    PHASE 2.6 TOOL: Temporal composition for wig aesthetics.
    Creates periodic transitions cycling between morphospace states.

    Use preset_name for curated presets, OR specify state_a/state_b
    for custom oscillations.

    Args:
        preset_name: Use a curated preset (texture_morph, density_breathe,
                     drama_sweep, construction_shift, color_pulse)
        state_a_id: Starting state (if not using preset)
        state_b_id: Alternating state (if not using preset)
        oscillation_pattern: "sinusoidal", "triangular", or "square"
        num_cycles: Number of complete A→B→A cycles
        steps_per_cycle: Samples per cycle (= period)
        phase_offset: Starting phase (0.0 = state A, 0.5 = state B)

    Returns:
        Sequence with states, pattern info, and phase points.

    Cost: 0 tokens (Layer 2 deterministic computation)
    """
    # Use preset if specified
    if preset_name:
        if preset_name not in WIG_RHYTHMIC_PRESETS:
            return json.dumps({
                "error": f"Unknown preset: {preset_name}",
                "available": list(WIG_RHYTHMIC_PRESETS.keys())
            })
        config = WIG_RHYTHMIC_PRESETS[preset_name]
        state_a = WIG_MORPHOSPACE_COORDS[config["state_a"]]
        state_b = WIG_MORPHOSPACE_COORDS[config["state_b"]]
        oscillation_pattern = config["pattern"]
        num_cycles = config["num_cycles"]
        steps_per_cycle = config["steps_per_cycle"]
        state_a_label = config["state_a"]
        state_b_label = config["state_b"]
    else:
        if not state_a_id or not state_b_id:
            return json.dumps({
                "error": "Provide preset_name OR both state_a_id and state_b_id"
            })
        if state_a_id not in WIG_MORPHOSPACE_COORDS:
            return json.dumps({"error": f"Unknown state: {state_a_id}"})
        if state_b_id not in WIG_MORPHOSPACE_COORDS:
            return json.dumps({"error": f"Unknown state: {state_b_id}"})
        state_a = WIG_MORPHOSPACE_COORDS[state_a_id]
        state_b = WIG_MORPHOSPACE_COORDS[state_b_id]
        state_a_label = state_a_id
        state_b_label = state_b_id

    total_steps = num_cycles * steps_per_cycle
    alphas = _generate_oscillation(total_steps, num_cycles, oscillation_pattern)

    # Apply phase offset
    if phase_offset > 0:
        offset_steps = int(phase_offset * steps_per_cycle)
        alphas = alphas[offset_steps:] + alphas[:offset_steps]

    sequence = []
    for step, alpha in enumerate(alphas):
        state = _interpolate_states(state_a, state_b, alpha)
        sequence.append({
            "step": step,
            "phase": (step % steps_per_cycle) / steps_per_cycle,
            "alpha": round(alpha, 4),
            "state": {k: round(v, 4) for k, v in state.items()}
        })

    return json.dumps({
        "domain": "wig_aesthetic",
        "preset": preset_name or "custom",
        "state_a": state_a_label,
        "state_b": state_b_label,
        "pattern": oscillation_pattern,
        "period": steps_per_cycle,
        "num_cycles": num_cycles,
        "total_steps": total_steps,
        "sequence": sequence,
        "parameter_names": WIG_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def apply_wig_rhythmic_preset(preset_name: str) -> str:
    """
    Apply a curated wig rhythmic preset and return the full trajectory.

    PHASE 2.6 CONVENIENCE TOOL: Pre-configured patterns.

    Available Presets:
    - texture_morph: everyday_natural ↔ textured_natural (period 22)
    - density_breathe: medical_comfort ↔ theatrical_volume (period 18)
    - drama_sweep: everyday_natural ↔ red_carpet_glam (period 28)
    - construction_shift: theatrical_volume ↔ editorial_sculpt (period 14)
    - color_pulse: protective_crown ↔ fantasy_extreme (period 20)

    Cost: 0 tokens
    """
    if preset_name not in WIG_RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(WIG_RHYTHMIC_PRESETS.keys())
        })

    trajectory = _generate_preset_trajectory(preset_name)
    config = WIG_RHYTHMIC_PRESETS[preset_name]

    return json.dumps({
        "preset": preset_name,
        "description": config["description"],
        "period": config["steps_per_cycle"],
        "pattern": config["pattern"],
        "total_steps": len(trajectory),
        "trajectory": [
            {k: round(v, 4) for k, v in state.items()}
            for state in trajectory
        ],
        "parameter_names": WIG_PARAMETER_NAMES,
        "cost_tokens": 0
    }, indent=2)


# ============================================================================
# PHASE 2.7: ATTRACTOR VISUALIZATION & PROMPT GENERATION
# ============================================================================

def _nearest_visual_type(state: dict) -> tuple:
    """Find nearest visual type to a parameter state.

    Returns (type_name, distance, type_data).
    """
    min_dist = float('inf')
    nearest_name = None
    nearest_data = None

    for type_name, type_data in WIG_VISUAL_TYPES.items():
        coords = type_data["coords"]
        dist = math.sqrt(sum(
            (state.get(p, 0.0) - coords.get(p, 0.0)) ** 2
            for p in WIG_PARAMETER_NAMES
        ))
        if dist < min_dist:
            min_dist = dist
            nearest_name = type_name
            nearest_data = type_data

    return nearest_name, min_dist, nearest_data


@mcp.tool()
def extract_wig_visual_vocabulary(
    state: str,
    strength: float = 1.0
) -> str:
    """
    Extract visual vocabulary from wig morphospace coordinates.

    PHASE 2.7 TOOL: Maps a 5D parameter state to the nearest canonical
    wig visual type and returns image-generation-ready keywords.

    Uses nearest-neighbor matching against 4 visual types.

    Args:
        state: JSON string of parameter coordinates, e.g.
               '{"construction_transparency": 0.6, "texture_curl_intensity": 0.25, ...}'
        strength: Keyword weight multiplier [0.0, 1.0] (default: 1.0)

    Returns:
        Dict with nearest_type, distance, keywords, optical_properties,
        color_associations

    Cost: 0 tokens (pure Layer 2 computation)
    """
    state_dict = json.loads(state)

    type_name, distance, type_data = _nearest_visual_type(state_dict)

    # Weight keywords by strength
    if strength < 1.0:
        n_keywords = max(2, int(len(type_data["keywords"]) * strength))
        keywords = type_data["keywords"][:n_keywords]
    else:
        keywords = type_data["keywords"]

    return json.dumps({
        "nearest_type": type_name,
        "distance": round(distance, 4),
        "keywords": keywords,
        "optical_properties": type_data["optical_properties"],
        "color_associations": type_data["color_associations"],
        "parameter_state": {k: round(v, 4) for k, v in state_dict.items()},
        "strength": strength,
        "cost_tokens": 0
    }, indent=2)


@mcp.tool()
def generate_wig_attractor_prompt(
    attractor_state: str = "",
    preset_name: str = "",
    mode: str = "composite",
    style_modifier: str = "",
    keyframe_count: int = 4
) -> str:
    """
    Generate image generation prompt from wig attractor state or preset.

    PHASE 2.7 TOOL: Translates wig morphospace coordinates into visual
    prompts suitable for image generation (ComfyUI, Stable Diffusion,
    DALL-E, etc.).

    Modes:
        composite: Single blended prompt from parameter state
        sequence: Multiple keyframe prompts from a rhythmic preset trajectory

    Args:
        attractor_state: JSON string of 5D coordinates (for composite mode)
        preset_name: Rhythmic preset name (for sequence mode)
        mode: "composite" or "sequence"
        style_modifier: Optional prefix (e.g. "photorealistic portrait",
                        "fashion photography", "oil painting")
        keyframe_count: Number of keyframes for sequence mode (default: 4)

    Returns:
        Dict with prompt(s), vocabulary details, and metadata

    Cost: 0 tokens (Layer 2 deterministic)
    """
    if mode == "composite":
        # Single prompt from a parameter state
        if not attractor_state:
            # Use a default interesting state (glamour_cascade region)
            state_dict = WIG_VISUAL_TYPES["glamour_cascade"]["coords"]
        else:
            state_dict = json.loads(attractor_state)

        type_name, distance, type_data = _nearest_visual_type(state_dict)

        # Build composite prompt
        prompt_parts = []
        if style_modifier:
            prompt_parts.append(style_modifier)
        prompt_parts.extend(type_data["keywords"])
        prompt_parts.extend(type_data["color_associations"][:2])

        prompt = ", ".join(prompt_parts)

        return json.dumps({
            "mode": "composite",
            "prompt": prompt,
            "vocabulary": {
                "nearest_type": type_name,
                "distance": round(distance, 4),
                "keywords": type_data["keywords"],
                "optical": type_data["optical_properties"],
                "colors": type_data["color_associations"]
            },
            "state": {k: round(v, 4) for k, v in state_dict.items()},
            "style_modifier": style_modifier or None,
            "cost_tokens": 0
        }, indent=2)

    elif mode == "sequence":
        # Multiple keyframes from a rhythmic preset
        if not preset_name:
            return json.dumps({
                "error": "preset_name required for sequence mode",
                "available_presets": list(WIG_RHYTHMIC_PRESETS.keys())
            })

        trajectory = _generate_preset_trajectory(preset_name)
        total_steps = len(trajectory)

        # Extract evenly-spaced keyframes
        keyframe_indices = [
            int(i * total_steps / keyframe_count)
            for i in range(keyframe_count)
        ]

        keyframes = []
        for idx in keyframe_indices:
            state = trajectory[idx]
            type_name, distance, type_data = _nearest_visual_type(state)

            prompt_parts = []
            if style_modifier:
                prompt_parts.append(style_modifier)
            prompt_parts.extend(type_data["keywords"])
            prompt_parts.extend(type_data["color_associations"][:2])

            keyframes.append({
                "step": idx,
                "phase": round(idx / total_steps, 3),
                "prompt": ", ".join(prompt_parts),
                "nearest_type": type_name,
                "distance": round(distance, 4),
                "state": {k: round(v, 4) for k, v in state.items()}
            })

        config = WIG_RHYTHMIC_PRESETS[preset_name]
        return json.dumps({
            "mode": "sequence",
            "preset": preset_name,
            "description": config["description"],
            "period": config["steps_per_cycle"],
            "keyframe_count": keyframe_count,
            "keyframes": keyframes,
            "style_modifier": style_modifier or None,
            "cost_tokens": 0
        }, indent=2)

    else:
        return json.dumps({
            "error": f"Unknown mode: {mode}",
            "available": ["composite", "sequence"]
        })


@mcp.tool()
def compute_wig_morphospace_distance(
    state_a_id: str,
    state_b_id: str
) -> str:
    """
    Compute distance between two wig morphospace states.

    Layer 2: Pure distance computation (0 tokens)

    Args:
        state_a_id: First state name (or JSON coordinates string)
        state_b_id: Second state name (or JSON coordinates string)

    Returns:
        Euclidean distance, per-parameter differences, and visual type info
    """
    # Resolve states (accept both names and JSON coordinate strings)
    if state_a_id in WIG_MORPHOSPACE_COORDS:
        coords_a = WIG_MORPHOSPACE_COORDS[state_a_id]
    else:
        try:
            coords_a = json.loads(state_a_id)
        except (json.JSONDecodeError, TypeError):
            return json.dumps({"error": f"Unknown state: {state_a_id}"})

    if state_b_id in WIG_MORPHOSPACE_COORDS:
        coords_b = WIG_MORPHOSPACE_COORDS[state_b_id]
    else:
        try:
            coords_b = json.loads(state_b_id)
        except (json.JSONDecodeError, TypeError):
            return json.dumps({"error": f"Unknown state: {state_b_id}"})

    # Compute distance
    diff = {p: round(coords_b[p] - coords_a[p], 4) for p in WIG_PARAMETER_NAMES}
    euclidean = math.sqrt(sum(d ** 2 for d in diff.values()))

    type_a, dist_a, _ = _nearest_visual_type(coords_a)
    type_b, dist_b, _ = _nearest_visual_type(coords_b)

    return json.dumps({
        "euclidean_distance": round(euclidean, 4),
        "parameter_differences": diff,
        "max_difference_parameter": max(diff, key=lambda k: abs(diff[k])),
        "state_a_visual_type": type_a,
        "state_b_visual_type": type_b,
        "cost_tokens": 0
    }, indent=2)

@mcp.tool()
def get_server_info() -> str:
    """
    Get information about the Wig Aesthetic MCP server.

    Returns server capabilities, architecture, and usage patterns.
    """
    info = {
        "name": "Wig Aesthetic MCP Server",
        "version": "2.6.0",
        "architecture": "three_layer_categorical_composition",
        "cost_optimization": "60% savings through deterministic mapping",
        "layers": {
            "layer_1": "Pure taxonomy (7 cap types, 8 textures, 5 styles)",
            "layer_2": "Deterministic parameter→vocabulary mapping (0 tokens)",
            "layer_3": "Creative synthesis with LLM (~200 tokens)"
        },
        "taxonomy_coverage": {
            "cap_constructions": len(CAP_CONSTRUCTIONS),
            "texture_patterns": len(TEXTURE_PATTERNS),
            "edge_treatments": len(EDGE_TREATMENTS),
            "color_patterns": len(COLOR_HIGHLIGHT_PATTERNS),
            "style_contexts": len(STYLE_CONTEXTS)
        },
        "phase_2_6_enhancements": {
            "rhythmic_composition": True,
            "morphospace_parameters": WIG_PARAMETER_NAMES,
            "canonical_states": list(WIG_MORPHOSPACE_COORDS.keys()),
            "presets": {
                name: {
                    "period": config["steps_per_cycle"],
                    "pattern": config["pattern"],
                    "states": f"{config['state_a']} ↔ {config['state_b']}"
                }
                for name, config in WIG_RHYTHMIC_PRESETS.items()
            },
            "available_periods": sorted(set(
                c["steps_per_cycle"] for c in WIG_RHYTHMIC_PRESETS.values()
            ))
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_types": list(WIG_VISUAL_TYPES.keys()),
            "prompt_modes": ["composite", "sequence"],
            "image_generation_compatible": True
        },
        "workflow": [
            "1. Select parameters (cap, texture, density, length, color)",
            "2. map_wig_parameters → deterministic vocabulary (0 tokens)",
            "3. Optional: apply_style_context for preset adjustments",
            "4. Optional: generate_wig_rhythmic_sequence for temporal composition",
            "5. Optional: generate_wig_attractor_prompt for image generation prompts",
            "6. Use vocabulary in image generation prompt"
        ],
        "domain_integration": {
            "domain_id": "wig_aesthetic",
            "parameter_count": len(WIG_PARAMETER_NAMES),
            "preset_count": len(WIG_RHYTHMIC_PRESETS),
            "visual_type_count": len(WIG_VISUAL_TYPES),
            "periods": sorted(set(
                c["steps_per_cycle"] for c in WIG_RHYTHMIC_PRESETS.values()
            )),
            "compatible_with": [
                "aesthetic-dynamics-core",
                "composition-graph-mcp",
                "catastrophe-morph-mcp",
                "microscopy-aesthetics-mcp",
                "diatom-morphology-mcp"
            ]
        }
    }
    return json.dumps(info, indent=2)
