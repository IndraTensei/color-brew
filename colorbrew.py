#!/usr/bin/env python3
"""
color-brew - Generate beautiful color palettes from a single color or keyword.

A CLI tool that creates harmonious color palettes and exports them in
multiple formats. Perfect for designers, developers, and anyone who
needs colors for a project, presentation, or creative work.

Version: 1.4.0

Usage:
    color-brew <color> [options]

Examples:
    color-brew "#FF6B6B"
    color-brew blue --scheme analogous
    color-brew "#2C3E50" --all
    color-brew coral --export css --output palette.css
    color-brew "#E74C3C" --scheme triadic --preview
"""

import argparse
import colorsys
import datetime
import json
import math
import os
import random
import re
import sys
from typing import List, Tuple, Optional, Dict


# ─── Named Colors (subset of CSS named colors) ───────────────────────────────

NAMED_COLORS: Dict[str, str] = {
    "aliceblue": "#F0F8FF", "antiquewhite": "#FAEBD7", "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4", "azure": "#F0FFFF", "beige": "#F5F5DC",
    "bisque": "#FFE4C4", "black": "#000000", "blanchedalmond": "#FFEBCD",
    "blue": "#0000FF", "blueviolet": "#8A2BE2", "brown": "#A52A2A",
    "burlywood": "#DEB887", "cadetblue": "#5F9EA0", "chartreuse": "#7FFF00",
    "chocolate": "#D2691E", "coral": "#FF7F50", "cornflowerblue": "#6495ED",
    "cornsilk": "#FFF8DC", "crimson": "#DC143C", "cyan": "#00FFFF",
    "darkblue": "#00008B", "darkcyan": "#008B8B", "darkgoldenrod": "#B8860B",
    "darkgray": "#A9A9A9", "darkgreen": "#006400", "darkkhaki": "#BDB76B",
    "darkmagenta": "#8B008B", "darkolivegreen": "#556B2F", "darkorange": "#FF8C00",
    "darkorchid": "#9932CC", "darkred": "#8B0000", "darksalmon": "#E9967A",
    "darkseagreen": "#8FBC8F", "darkslateblue": "#483D8B", "darkslategray": "#2F4F4F",
    "darkturquoise": "#00CED1", "darkviolet": "#9400D3", "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF", "dimgray": "#696969", "dodgerblue": "#1E90FF",
    "firebrick": "#B22222", "floralwhite": "#FFFAF0", "forestgreen": "#228B22",
    "fuchsia": "#FF00FF", "gainsboro": "#DCDCDC", "ghostwhite": "#F8F8FF",
    "gold": "#FFD700", "goldenrod": "#DAA520", "gray": "#808080",
    "green": "#008000", "greenyellow": "#ADFF2F", "honeydew": "#F0FFF0",
    "hotpink": "#FF69B4", "indianred": "#CD5C5C", "indigo": "#4B0082",
    "ivory": "#FFFFF0", "khaki": "#F0E68C", "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5", "lawngreen": "#7CFC00", "lemonchiffon": "#FFFACD",
    "lightblue": "#ADD8E6", "lightcoral": "#F08080", "lightcyan": "#E0FFFF",
    "lightgoldenrodyellow": "#FAFAD2", "lightgray": "#D3D3D3", "lightgreen": "#90EE90",
    "lightpink": "#FFB6C1", "lightsalmon": "#FFA07A", "lightseagreen": "#20B2AA",
    "lightskyblue": "#87CEFA", "lightslategray": "#778899", "lightsteelblue": "#B0C4DE",
    "lightyellow": "#FFFFE0", "lime": "#00FF00", "limegreen": "#32CD32",
    "linen": "#FAF0E6", "magenta": "#FF00FF", "maroon": "#800000",
    "mediumaquamarine": "#66CDAA", "mediumblue": "#0000CD", "mediumorchid": "#BA55D3",
    "mediumpurple": "#9370DB", "mediumseagreen": "#3CB371", "mediumslateblue": "#7B68EE",
    "mediumspringgreen": "#00FA9A", "mediumturquoise": "#48D1CC", "mediumvioletred": "#C71585",
    "midnightblue": "#191970", "mintcream": "#F5FFFA", "mistyrose": "#FFE4E1",
    "moccasin": "#FFE4B5", "navajowhite": "#FFDEAD", "navy": "#000080",
    "oldlace": "#FDF5E6", "olive": "#808000", "olivedrab": "#6B8E23",
    "orange": "#FFA500", "orangered": "#FF4500", "orchid": "#DA70D6",
    "palegoldenrod": "#EEE8AA", "palegreen": "#98FB98", "paleturquoise": "#AFEEEE",
    "palevioletred": "#DB7093", "papayawhip": "#FFEFD5", "peachpuff": "#FFDAB9",
    "peru": "#CD853F", "pink": "#FFC0CB", "plum": "#DDA0DD",
    "powderblue": "#B0E0E6", "purple": "#800080", "rebeccapurple": "#663399",
    "red": "#FF0000", "rosybrown": "#BC8F8F", "royalblue": "#4169E1",
    "saddlebrown": "#8B4513", "salmon": "#FA8072", "sandybrown": "#F4A460",
    "seagreen": "#2E8B57", "seashell": "#FFF5EE", "sienna": "#A0522D",
    "silver": "#C0C0C0", "skyblue": "#87CEEB", "slateblue": "#6A5ACD",
    "slategray": "#708090", "snow": "#FFFAFA", "springgreen": "#00FF7F",
    "steelblue": "#4682B4", "tan": "#D2B48C", "teal": "#008080",
    "thistle": "#D8BFD8", "tomato": "#FF6347", "turquoise": "#40E0D0",
    "violet": "#EE82EE", "wheat": "#F5DEB3", "white": "#FFFFFF",
    "whitesmoke": "#F5F5F5", "yellow": "#FFFF00", "yellowgreen": "#9ACD32",
}


# ─── Color Conversion Utilities ──────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex string."""
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to HSL. Returns (h: 0-360, s: 0-100, l: 0-100)."""
    r1, g1, b1 = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r1, g1, b1)
    return (h * 360, s * 100, l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL to RGB. Takes (h: 0-360, s: 0-100, l: 0-100)."""
    h1 = h / 360.0
    s1 = s / 100.0
    l1 = l / 100.0
    r, g, b = colorsys.hls_to_rgb(h1, l1, s1)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[float, float, float, float]:
    """Convert RGB to CMYK. Returns values 0-100."""
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    r1, g1, b1 = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r1, g1, b1)
    c = (1 - r1 - k) / (1 - k) * 100
    m = (1 - g1 - k) / (1 - k) * 100
    y = (1 - b1 - k) / (1 - k) * 100
    return (c, m, y, k * 100)


def parse_color(color_str: str) -> Tuple[int, int, int]:
    """Parse a color from hex, rgb(), or named color."""
    color_str = color_str.strip().lower()

    # Try named color
    if color_str in NAMED_COLORS:
        return hex_to_rgb(NAMED_COLORS[color_str])

    # Try hex
    if color_str.startswith('#') or re.match(r'^[0-9a-f]{3,6}$', color_str):
        return hex_to_rgb(color_str)

    # Try rgb(r, g, b)
    rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str)
    if rgb_match:
        return (int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3)))

    # Try hsl(h, s%, l%)
    hsl_match = re.match(r'hsl\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*\)', color_str)
    if hsl_match:
        return hsl_to_rgb(float(hsl_match.group(1)), float(hsl_match.group(2)), float(hsl_match.group(3)))

    raise ValueError(f"Cannot parse color: '{color_str}'. Use hex (#FF6B6B), rgb(255,107,107), hsl(0,71,71), or a named color.")


def get_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.0."""
    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def get_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = get_luminance(*rgb1)
    l2 = get_luminance(*rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def get_text_color(bg_rgb: Tuple[int, int, int]) -> str:
    """Return black or white depending on which contrasts better with bg."""
    white_contrast = get_contrast_ratio(bg_rgb, (255, 255, 255))
    black_contrast = get_contrast_ratio(bg_rgb, (0, 0, 0))
    return "#FFFFFF" if white_contrast > black_contrast else "#000000"


# ─── Color Name Detection (Reverse Lookup) ────────────────────────────────────

def color_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """Calculate weighted Euclidean distance between two colors (human-perception-aware)."""
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    # Weighted Euclidean distance (human eyes are most sensitive to green)
    return math.sqrt(2 * (r1 - r2) ** 2 + 4 * (g1 - g2) ** 2 + 3 * (b1 - b2) ** 2)


def find_closest_color_name(rgb: Tuple[int, int, int]) -> Tuple[str, str, float]:
    """Find the closest named CSS color. Returns (name, hex, distance)."""
    min_dist = float('inf')
    closest_name = "unknown"
    closest_hex = rgb_to_hex(*rgb)
    for name, hex_val in NAMED_COLORS.items():
        dist = color_distance(rgb, hex_to_rgb(hex_val))
        if dist < min_dist:
            min_dist = dist
            closest_name = name
            closest_hex = hex_val
    return (closest_name, closest_hex, min_dist)


def print_color_identity(rgb: Tuple[int, int, int]):
    """Print detailed identity info for a color."""
    hex_str = rgb_to_hex(*rgb)
    h, s, l = rgb_to_hsl(*rgb)
    c, m, y, k = rgb_to_cmyk(*rgb)
    closest_name, closest_hex, dist = find_closest_color_name(rgb)

    print(f"\n  Color Identity for {hex_str}")
    print(f"  {'─' * 45}")
    print(f"  HEX: {hex_str}")
    print(f"  RGB: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
    print(f"  HSL: hsl({h:.1f}, {s:.1f}%, {l:.1f}%)")
    print(f"  CMYK: cmyk({c:.0f}%, {m:.0f}%, {y:.0f}%, {k:.0f}%)")
    if closest_name != "unknown":
        exact = " (exact match)" if dist < 1 else f" (distance: {dist:.1f})"
        print(f"  Name: {closest_name}{exact}")
    print()


# ─── Palette History & Favorites ──────────────────────────────────────────────

HISTORY_DIR = os.path.expanduser("~/.color-brew")
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.json")


def _ensure_history_dir():
    os.makedirs(HISTORY_DIR, exist_ok=True)


def load_history() -> List[dict]:
    """Load palette history from disk."""
    _ensure_history_dir()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_palette_to_history(scheme: str, base_color: str, palette: List[Tuple[int, int, int]]):
    """Save a generated palette to history."""
    _ensure_history_dir()
    history = load_history()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "scheme": scheme,
        "base_color": base_color,
        "colors": [rgb_to_hex(*c) for c in palette],
    }
    history.insert(0, entry)
    # Keep last 200 entries
    history = history[:200]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    return entry


def print_history(count: int = 10):
    """Print palette history."""
    history = load_history()
    if not history:
        print("\n  No palette history yet. Generate some palettes!\n")
        return

    print(f"\n  Palette History (last {min(count, len(history))} of {len(history)})")
    print(f"  {'─' * 55}")
    for i, entry in enumerate(history[:count]):
        ts = entry.get("timestamp", "?")[:19]
        scheme = entry.get("scheme", "?")
        base = entry.get("base_color", "?")
        colors = entry.get("colors", [])
        color_str = " ".join(colors) if colors else "(empty)"
        swatches = ""
        if colors:
            for c in colors[:8]:
                try:
                    swatches += color_block(c, 2)
                except Exception:
                    pass
        print(f"  {i+1:3d}. [{ts}] {scheme:20s} from {base}")
        print(f"       {swatches}")
        print(f"       {color_str}")
        print()
    print()

def normalize_hue(h: float) -> float:
    """Normalize hue to 0-360 range."""
    return h % 360


# ─── Random Palette Generation ──────────────────────────────────────────────

# Mood-based hue ranges and saturation/lightness presets
MOOD_PRESETS: Dict[str, Dict] = {
    "warm": {"hue_range": (0, 60), "sat_range": (50, 90), "light_range": (40, 70)},
    "cool": {"hue_range": (180, 270), "sat_range": (40, 80), "light_range": (35, 65)},
    "calm": {"hue_range": (150, 240), "sat_range": (20, 50), "light_range": (55, 80)},
    "vibrant": {"hue_range": (0, 360), "sat_range": (75, 100), "light_range": (45, 65)},
    "pastel": {"hue_range": (0, 360), "sat_range": (30, 60), "light_range": (70, 90)},
    "dark": {"hue_range": (0, 360), "sat_range": (30, 80), "light_range": (10, 35)},
    "earthy": {"hue_range": (15, 55), "sat_range": (25, 55), "light_range": (25, 55)},
    "neon": {"hue_range": (0, 360), "sat_range": (90, 100), "light_range": (50, 65)},
    "sunset": {"hue_range": (340, 60), "sat_range": (60, 95), "light_range": (40, 70)},
    "ocean": {"hue_range": (170, 220), "sat_range": (40, 80), "light_range": (30, 65)},
    "forest": {"hue_range": (80, 160), "sat_range": (25, 60), "light_range": (20, 50)},
    "retro": {"hue_range": (0, 360), "sat_range": (50, 75), "light_range": (45, 60)},
}

SEASONS: Dict[str, List[str]] = {
    "spring": ["#FFB7C5", "#FFD1DC", "#B5EAD7", "#C7CEEA", "#E2F0CB"],
    "summer": ["#FF6B6B", "#FFE66D", "#4ECDC4", "#1A535C", "#F7FFF7"],
    "autumn": ["#D4A373", "#CCD5AE", "#E9EDC9", "#FEFAE0", "#FAEDCD"],
    "winter": ["#A8DADC", "#457B9D", "#1D3557", "#F1FAEE", "#E63946"],
}


def generate_random_color(mood: Optional[str] = None) -> Tuple[int, int, int]:
    """Generate a random base color, optionally constrained by a mood keyword."""
    if mood and mood.lower() in MOOD_PRESETS:
        preset = MOOD_PRESETS[mood.lower()]
        h_range = preset["hue_range"]
        # Handle wrap-around hue ranges (e.g., sunset: 340 to 60)
        if h_range[0] > h_range[1]:
            h = random.choice(
                list(range(h_range[0], 360)) + list(range(0, h_range[1] + 1))
            )
        else:
            h = random.uniform(h_range[0], h_range[1])
        s = random.uniform(preset["sat_range"][0], preset["sat_range"][1])
        l = random.uniform(preset["light_range"][0], preset["light_range"][1])
    else:
        h = random.uniform(0, 360)
        s = random.uniform(30, 90)
        l = random.uniform(30, 70)
    return hsl_to_rgb(h, s, l)


def generate_random_palette(
    scheme: str = "analogous",
    mood: Optional[str] = None,
    steps: int = 5,
) -> Tuple[Tuple[int, int, int], List[Tuple[int, int, int]]]:
    """Generate a random palette. Returns (base_rgb, palette)."""
    base_rgb = generate_random_color(mood)
    generator = SCHEMES.get(scheme, generate_analogous)
    if scheme in ("monochromatic", "shades", "tints"):
        palette = generator(base_rgb, steps)
    else:
        palette = generator(base_rgb)
    return base_rgb, palette


def generate_seasonal_palette(season: str) -> List[Tuple[int, int, int]]:
    """Generate a palette inspired by a season."""
    season = season.lower()
    if season not in SEASONS:
        raise ValueError(f"Unknown season '{season}'. Choose from: {', '.join(SEASONS.keys())}")
    hex_list = SEASONS[season]
    random.shuffle(hex_list)
    return [hex_to_rgb(h) for h in hex_list]


# ─── Palette Blending ───────────────────────────────────────────────────────

def blend_colors(
    rgb1: Tuple[int, int, int],
    rgb2: Tuple[int, int, int],
    ratio: float = 0.5,
) -> Tuple[int, int, int]:
    """Blend two colors together. ratio=0 gives rgb1, ratio=1 gives rgb2."""
    ratio = max(0.0, min(1.0, ratio))
    r = int(round(rgb1[0] * (1 - ratio) + rgb2[0] * ratio))
    g = int(round(rgb1[1] * (1 - ratio) + rgb2[1] * ratio))
    b = int(round(rgb1[2] * (1 - ratio) + rgb2[2] * ratio))
    return (r, g, b)


def blend_palettes(
    palette1: List[Tuple[int, int, int]],
    palette2: List[Tuple[int, int, int]],
    ratio: float = 0.5,
) -> List[Tuple[int, int, int]]:
    """Blend two palettes together. The longer palette is truncated to match."""
    min_len = min(len(palette1), len(palette2))
    result = []
    for i in range(min_len):
        result.append(blend_colors(palette1[i], palette2[i], ratio))
    return result


def interleave_palettes(
    palette1: List[Tuple[int, int, int]],
    palette2: List[Tuple[int, int, int]],
) -> List[Tuple[int, int, int]]:
    """Interleave colors from two palettes (alternating picks)."""
    result = []
    max_len = max(len(palette1), len(palette2))
    for i in range(max_len):
        if i < len(palette1):
            result.append(palette1[i])
        if i < len(palette2):
            result.append(palette2[i])
    return result


# ─── Favorites System ────────────────────────────────────────────────────────

FAVORITES_FILE = os.path.join(HISTORY_DIR, "favorites.json")


def load_favorites() -> List[dict]:
    """Load favorite palettes from disk."""
    _ensure_history_dir()
    if not os.path.exists(FAVORITES_FILE):
        return []
    try:
        with open(FAVORITES_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_to_favorites(name: str, scheme: str, base_color: str, palette: List[Tuple[int, int, int]]):
    """Save a palette to favorites with a given name."""
    _ensure_history_dir()
    favorites = load_favorites()
    entry = {
        "name": name,
        "scheme": scheme,
        "base_color": base_color,
        "colors": [rgb_to_hex(*c) for c in palette],
        "timestamp": datetime.datetime.now().isoformat(),
    }
    # Remove duplicate by name
    favorites = [f for f in favorites if f.get("name") != name]
    favorites.insert(0, entry)
    # Keep last 100 favorites
    favorites = favorites[:100]
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)
    return entry


def remove_favorite(name: str) -> bool:
    """Remove a favorite by name. Returns True if found and removed."""
    favorites = load_favorites()
    original_len = len(favorites)
    favorites = [f for f in favorites if f.get("name") != name]
    if len(favorites) < original_len:
        with open(FAVORITES_FILE, "w") as f:
            json.dump(favorites, f, indent=2)
        return True
    return False


def print_favorites():
    """Print all saved favorite palettes."""
    favorites = load_favorites()
    if not favorites:
        print("\n  No favorites saved yet. Use --favorite <name> to save a palette.\n")
        return

    print(f"\n  Saved Favorites ({len(favorites)})")
    print(f"  {'─' * 55}")
    for i, entry in enumerate(favorites):
        name = entry.get("name", "?")
        scheme = entry.get("scheme", "?")
        base = entry.get("base_color", "?")
        colors = entry.get("colors", [])
        ts = entry.get("timestamp", "")[:10]
        color_str = " ".join(colors) if colors else "(empty)"
        swatches = ""
        if colors:
            for c in colors[:8]:
                try:
                    swatches += color_block(c, 2)
                except Exception:
                    pass
        print(f"  {i+1:3d}. [{name}] ({scheme}) from {base}  ({ts})")
        print(f"       {swatches}")
        print(f"       {color_str}")
        print()
    print()


def generate_complementary(base_rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Generate complementary palette (2 colors)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [base_rgb, hsl_to_rgb(normalize_hue(h + 180), s, l)]


def generate_analogous(base_rgb: Tuple[int, int, int], spread: float = 30) -> List[Tuple[int, int, int]]:
    """Generate analogous palette (3 colors)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [
        hsl_to_rgb(normalize_hue(h - spread), s, l),
        base_rgb,
        hsl_to_rgb(normalize_hue(h + spread), s, l),
    ]


def generate_triadic(base_rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Generate triadic palette (3 colors, 120° apart)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [
        base_rgb,
        hsl_to_rgb(normalize_hue(h + 120), s, l),
        hsl_to_rgb(normalize_hue(h + 240), s, l),
    ]


def generate_split_complementary(base_rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Generate split-complementary palette (3 colors)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [
        base_rgb,
        hsl_to_rgb(normalize_hue(h + 150), s, l),
        hsl_to_rgb(normalize_hue(h + 210), s, l),
    ]


def generate_tetradic(base_rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Generate tetradic (rectangle) palette (4 colors)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [
        base_rgb,
        hsl_to_rgb(normalize_hue(h + 60), s, l),
        hsl_to_rgb(normalize_hue(h + 180), s, l),
        hsl_to_rgb(normalize_hue(h + 240), s, l),
    ]


def generate_square(base_rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """Generate square palette (4 colors, 90° apart)."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [
        base_rgb,
        hsl_to_rgb(normalize_hue(h + 90), s, l),
        hsl_to_rgb(normalize_hue(h + 180), s, l),
        hsl_to_rgb(normalize_hue(h + 270), s, l),
    ]


def generate_monochromatic(base_rgb: Tuple[int, int, int], steps: int = 5) -> List[Tuple[int, int, int]]:
    """Generate monochromatic palette with varying lightness."""
    h, s, l = rgb_to_hsl(*base_rgb)
    lightness_values = [max(10, l - 30), max(20, l - 15), base_rgb and l, min(85, l + 15), min(95, l + 30)]
    # Recalculate to get exact lightness steps
    result = []
    for i in range(steps):
        target_l = 10 + (80 * i / (steps - 1))
        result.append(hsl_to_rgb(h, s, target_l))
    return result


def generate_shades(base_rgb: Tuple[int, int, int], steps: int = 5) -> List[Tuple[int, int, int]]:
    """Generate shades from the base color to black."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [hsl_to_rgb(h, s, max(5, l * i / (steps - 1))) for i in range(steps)]


def generate_tints(base_rgb: Tuple[int, int, int], steps: int = 5) -> List[Tuple[int, int, int]]:
    """Generate tints from the base color to white."""
    h, s, l = rgb_to_hsl(*base_rgb)
    return [hsl_to_rgb(h, s, min(95, l + (100 - l) * i / (steps - 1))) for i in range(steps)]


def generate_gradient(base_rgb: Tuple[int, int, int], target_rgb: Tuple[int, int, int], steps: int = 6) -> List[Tuple[int, int, int]]:
    """Generate a smooth gradient between two colors."""
    r1, g1, b1 = base_rgb
    r2, g2, b2 = target_rgb
    return [
        (
            int(round(r1 + (r2 - r1) * i / (steps - 1))),
            int(round(g1 + (g2 - g1) * i / (steps - 1))),
            int(round(b1 + (b2 - b1) * i / (steps - 1))),
        )
        for i in range(steps)
    ]


SCHEMES = {
    "complementary": generate_complementary,
    "analogous": generate_analogous,
    "triadic": generate_triadic,
    "split-complementary": generate_split_complementary,
    "tetradic": generate_tetradic,
    "square": generate_square,
    "monochromatic": generate_monochromatic,
    "shades": generate_shades,
    "tints": generate_tints,
}


# ─── Terminal Display ────────────────────────────────────────────────────────

def color_block(hex_color: str, size: int = 2) -> str:
    """Return a colored block for terminal display using ANSI 24-bit color."""
    r, g, b = hex_to_rgb(hex_color)
    return f"\033[48;2;{r};{g};{b}m{'  ' * size}\033[0m"


def color_text(text: str, hex_color: str) -> str:
    """Return colored text for terminal display."""
    r, g, b = hex_to_rgb(hex_color)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def print_palette(palette: List[Tuple[int, int, int]], labels: Optional[List[str]] = None):
    """Print a color palette to the terminal with colored blocks."""
    hexes = [rgb_to_hex(*c) for c in palette]

    # Print color blocks
    print()
    for i, color in enumerate(palette):
        r, g, b = color
        text_color = get_text_color(color)
        label = labels[i] if labels and i < len(labels) else ""
        hex_str = rgb_to_hex(r, g, b)
        hsl = rgb_to_hsl(r, g, b)
        print(f"  {color_block(hex_str, 4)}  {color_text(hex_str, text_color)}  "
              f"rgb({r:3d},{g:3d},{b:3d})  hsl({hsl[0]:5.1f},{hsl[1]:4.1f}%,{hsl[2]:4.1f}%)  {label}")
    print()


def print_palette_bar(palette: List[Tuple[int, int, int]], width: int = 60):
    """Print a horizontal color bar."""
    print()
    bar = ""
    block_width = width // len(palette)
    for color in palette:
        hex_str = rgb_to_hex(*color)
        bar += color_block(hex_str, block_width // 2)
    print(f"  {bar}")
    print()


def print_smooth_bar(palette: List[Tuple[int, int, int]], width: int = 60):
    """Print a smooth gradient bar using Unicode half-block characters for finer resolution."""
    print()
    if len(palette) < 2:
        print_palette_bar(palette, width)
        return

    # Generate a smooth gradient by interpolating between palette colors
    total_steps = width
    colors_per_segment = max(1, total_steps // (len(palette) - 1))

    smooth_colors = []
    for i in range(len(palette) - 1):
        r1, g1, b1 = palette[i]
        r2, g2, b2 = palette[i + 1]
        for step in range(colors_per_segment):
            t = step / colors_per_segment
            r = int(round(r1 + (r2 - r1) * t))
            g = int(round(g1 + (g2 - g1) * t))
            b = int(round(b1 + (b2 - b1) * t))
            smooth_colors.append((r, g, b))

    # Add the last color
    smooth_colors.append(palette[-1])

    # Print using half-block characters (▀ and ▄) for double vertical resolution
    bar = ""
    for color in smooth_colors[:width]:
        hex_str = rgb_to_hex(*color)
        bar += color_block(hex_str, 1)
    print(f"  {bar}")
    print()


# ─── Export Formats ──────────────────────────────────────────────────────────

def export_css(palette: List[Tuple[int, int, int]], var_prefix: str = "color") -> str:
    """Export palette as CSS custom properties."""
    lines = [":root {"]
    for i, color in enumerate(palette):
        hex_str = rgb_to_hex(*color)
        lines.append(f"  --{var_prefix}-{i + 1}: {hex_str};")
    lines.append("}")
    return "\n".join(lines)


def export_scss(palette: List[Tuple[int, int, int]], var_prefix: str = "color") -> str:
    """Export palette as SCSS variables."""
    lines = []
    for i, color in enumerate(palette):
        hex_str = rgb_to_hex(*color)
        lines.append(f"${var_prefix}-{i + 1}: {hex_str};")
    return "\n".join(lines)


def export_tailwind(palette: List[Tuple[int, int, int]], name: str = "custom") -> str:
    """Export palette as Tailwind config extension."""
    lines = [f"  {name}: {{"]
    for i, color in enumerate(palette):
        hex_str = rgb_to_hex(*color)
        step = (i + 1) * 100
        lines.append(f"    '{step}': '{hex_str}',")
    lines.append("  },")
    return "\n".join(lines)


def export_json(palette: List[Tuple[int, int, int]]) -> str:
    """Export palette as JSON."""
    colors = []
    for color in palette:
        h, s, l = rgb_to_hsl(*color)
        colors.append({
            "hex": rgb_to_hex(*color),
            "rgb": {"r": color[0], "g": color[1], "b": color[2]},
            "hsl": {
                "h": round(h, 1),
                "s": round(s, 1),
                "l": round(l, 1),
            },
        })
    data = {"palette": colors}
    return json.dumps(data, indent=2)


def export_svg(palette: List[Tuple[int, int, int]], width: int = 500, height: int = 100) -> str:
    """Export palette as an SVG swatch image."""
    swatch_width = width / len(palette)
    rects = []
    for i, color in enumerate(palette):
        hex_str = rgb_to_hex(*color)
        x = i * swatch_width
        rects.append(
            f'  <rect x="{x}" y="0" width="{swatch_width}" height="{height}" fill="{hex_str}" />'
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{chr(10).join(rects)}
</svg>"""


def export_png(palette: List[Tuple[int, int, int]], output_path: str):
    """Export palette as a PNG image using Pillow if available, else SVG fallback."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        width = 600
        height = 150
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        swatch_width = width // len(palette)

        for i, color in enumerate(palette):
            x0 = i * swatch_width
            x1 = x0 + swatch_width
            draw.rectangle([x0, 0, x1, height - 30], fill=color)
            hex_str = rgb_to_hex(*color)
            # Try to add text
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
            except (IOError, OSError):
                font = ImageFont.load_default()
            text_color = get_text_color(color)
            text_x = x0 + (swatch_width - len(hex_str) * 6) // 2
            draw.text((text_x, height - 22), hex_str, fill=text_color, font=font)

        img.save(output_path, 'PNG')
    except ImportError:
        # Fallback: save as SVG
        svg_path = output_path.replace('.png', '.svg')
        with open(svg_path, 'w') as f:
            f.write(export_svg(palette))
        print(f"  Pillow not available. Saved SVG swatch to {svg_path} instead.")


# ─── Main CLI ────────────────────────────────────────────────────────────────

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="color-brew",
        description="Generate beautiful color palettes from a single color or keyword.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  color-brew "#FF6B6B"
  color-brew blue --scheme analogous
  color-brew coral --all
  color-brew "#2C3E50" --scheme triadic --preview
  color-brew "#E74C3C" --export css --output palette.css
  color-brew "#3498DB" --scheme monochromatic --steps 7
  color-brew "#FF6B6B" --gradient "#3498DB" --steps 8
  color-brew "#2ECC71" --contrast white black
        """,
    )

    parser.add_argument(
        "color",
        nargs="?",
        default=None,
        help="Input color: hex (#FF6B6B), rgb(255,107,107), hsl(0,71,71), or named color (coral)"
    )

    parser.add_argument(
        "-s", "--scheme",
        choices=list(SCHEMES.keys()),
        default="analogous",
        help="Color scheme to generate (default: analogous)",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all color schemes at once",
    )

    parser.add_argument(
        "-n", "--steps",
        type=int,
        default=5,
        help="Number of colors for monochromatic/shades/tints schemes (default: 5)",
    )

    parser.add_argument(
        "-p", "--preview",
        action="store_true",
        help="Show a large color bar preview",
    )

    parser.add_argument(
        "-e", "--export",
        choices=["css", "scss", "tailwind", "json", "svg", "png"],
        help="Export format",
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path for export",
    )

    parser.add_argument(
        "--gradient",
        metavar="COLOR",
        help="Generate a gradient from input color to this color",
    )

    parser.add_argument(
        "--contrast",
        nargs="+",
        metavar="COLOR",
        help="Show contrast ratios against specified colors (default: black, white)",
    )

    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy hex values to clipboard (requires xclip or pbcopy)",
    )

    parser.add_argument(
        "--name",
        help="Custom name/prefix for export variables (default: auto-detected)",
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Only output hex values, one per line",
    )

    parser.add_argument(
        "--identify",
        action="store_true",
        help="Identify the closest named CSS color and show full color identity",
    )

    parser.add_argument(
        "--history",
        action="store_true",
        help="Show palette generation history",
    )

    parser.add_argument(
        "--history-count",
        type=int,
        default=10,
        help="Number of history entries to show (default: 10)",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save generated palette to history",
    )

    parser.add_argument(
        "--bar-style",
        choices=["block", "smooth"],
        default="block",
        help="Color bar style: 'block' (default) or 'smooth' (gradient)",
    )

    parser.add_argument(
        "--random",
        nargs="?",
        const="any",
        default=None,
        metavar="MOOD",
        help="Generate a random palette. Optionally specify a mood: "
             + ", ".join(sorted(MOOD_PRESETS.keys())),
    )

    parser.add_argument(
        "--season",
        choices=list(SEASONS.keys()),
        help="Generate a palette inspired by a season (spring, summer, autumn, winter)",
    )

    parser.add_argument(
        "--blend",
        metavar="COLOR",
        help="Blend the generated palette with a palette from this second base color",
    )

    parser.add_argument(
        "--blend-mode",
        choices=["merge", "interleave"],
        default="merge",
        help="How to blend palettes: 'merge' (weighted average) or 'interleave' (alternate) (default: merge)",
    )

    parser.add_argument(
        "--blend-ratio",
        type=float,
        default=0.5,
        help="Blend ratio for merge mode (0.0=first palette, 1.0=second) (default: 0.5)",
    )

    parser.add_argument(
        "--favorite",
        metavar="NAME",
        help="Save the current palette to favorites with the given name",
    )

    parser.add_argument(
        "--favorites",
        action="store_true",
        help="List all saved favorite palettes",
    )

    parser.add_argument(
        "--unfavorite",
        metavar="NAME",
        help="Remove a palette from favorites by name",
    )

    return parser


def copy_to_clipboard(text: str):
    """Copy text to clipboard."""
    try:
        import subprocess
        # Try xclip (Linux)
        try:
            proc = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            proc.communicate(text.encode())
            return
        except FileNotFoundError:
            pass
        # Try pbcopy (macOS)
        try:
            proc = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            proc.communicate(text.encode())
            return
        except FileNotFoundError:
            pass
        # Try wl-copy (Wayland)
        try:
            proc = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
            proc.communicate(text.encode())
            return
        except FileNotFoundError:
            pass
        print("  Clipboard copy requires xclip, pbcopy, or wl-copy", file=sys.stderr)
    except Exception as e:
        print(f"  Clipboard copy failed: {e}", file=sys.stderr)


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Handle --history (no color needed)
    if args.history:
        print_history(args.history_count)
        return

    # Handle --favorites (no color needed)
    if args.favorites:
        print_favorites()
        return

    # Handle --unfavorite (no color needed)
    if args.unfavorite:
        if remove_favorite(args.unfavorite):
            print(f"\n  Removed '{args.unfavorite}' from favorites.\n")
        else:
            print(f"\n  Favorite '{args.unfavorite}' not found.\n")
        return

    # Handle --season (no base color needed)
    if args.season:
        try:
            palette = generate_seasonal_palette(args.season)
        except ValueError as e:
            print(f"  {e}", file=sys.stderr)
            sys.exit(1)

        if args.quiet:
            print(" ".join(rgb_to_hex(*c) for c in palette))
            return

        scheme_name = f"seasonal-{args.season}"
        hex_str = rgb_to_hex(*palette[0])

        print(f"\n  color-brew -- {args.season.upper()} seasonal palette")
        print(f"  {'─' * 50}")
        if args.bar_style == "smooth":
            print_smooth_bar(palette)
        else:
            print_palette_bar(palette)
        print_palette(palette)

        # Save to history
        if args.save:
            entry = save_palette_to_history(scheme_name, hex_str, palette)
            print(f"  Saved to history ({len(entry['colors'])} colors)")

        # Export
        if args.export:
            var_prefix = args.name or args.season
            _handle_export(palette, args, var_prefix)

        # Favorite
        if args.favorite:
            entry = save_to_favorites(args.favorite, scheme_name, hex_str, palette)
            print(f"  Saved to favorites as '{args.favorite}' ({len(entry['colors'])} colors)")

        # Copy to clipboard
        if args.copy:
            hex_values = " ".join(rgb_to_hex(*c) for c in palette)
            copy_to_clipboard(hex_values)
            print(f"  Copied to clipboard: {hex_values}")

        print()
        return

    # Handle --random (no base color needed)
    if args.random is not None:
        mood = args.random if args.random != "any" else None
        if mood and mood.lower() not in MOOD_PRESETS:
            print(f"  Unknown mood '{mood}'. Available moods: {', '.join(sorted(MOOD_PRESETS.keys()))}", file=sys.stderr)
            sys.exit(1)

        base_rgb, palette = generate_random_palette(
            scheme=args.scheme, mood=mood, steps=args.steps
        )
        scheme_name = args.scheme

        # Apply blend if requested
        if args.blend:
            try:
                blend_rgb = parse_color(args.blend)
            except ValueError as e:
                print(f"  {e}", file=sys.stderr)
                sys.exit(1)
            blend_gen = SCHEMES.get(args.scheme, generate_analogous)
            if args.scheme in ("monochromatic", "shades", "tints"):
                palette2 = blend_gen(blend_rgb, args.steps)
            else:
                palette2 = blend_gen(blend_rgb)
            if args.blend_mode == "interleave":
                palette = interleave_palettes(palette, palette2)
                scheme_name = f"{scheme_name}-interleaved"
            else:
                palette = blend_palettes(palette, palette2, args.blend_ratio)
                scheme_name = f"{scheme_name}-blended"

        if args.quiet:
            print(" ".join(rgb_to_hex(*c) for c in palette))
            return

        hex_str = rgb_to_hex(*base_rgb)
        h, s, l = rgb_to_hsl(*base_rgb)
        mood_label = f" ({mood})" if mood else ""
        print(f"\n  color-brew -- RANDOM{mood_label} {scheme_name.upper()} palette")
        print(f"  Base: {hex_str} HSL({h:.0f}, {s:.0f}%, {l:.0f}%)")
        print(f"  {'─' * 50}")

        if args.bar_style == "smooth":
            print_smooth_bar(palette)
        else:
            print_palette_bar(palette)
        print_palette(palette)

        # Save to history
        if args.save:
            entry = save_palette_to_history(scheme_name, hex_str, palette)
            print(f"  Saved to history ({len(entry['colors'])} colors)")

        # Export
        if args.export:
            var_prefix = args.name or "random"
            _handle_export(palette, args, var_prefix)

        # Favorite
        if args.favorite:
            entry = save_to_favorites(args.favorite, scheme_name, hex_str, palette)
            print(f"  Saved to favorites as '{args.favorite}' ({len(entry['colors'])} colors)")

        # Copy to clipboard
        if args.copy:
            hex_values = " ".join(rgb_to_hex(*c) for c in palette)
            copy_to_clipboard(hex_values)
            print(f"  Copied to clipboard: {hex_values}")

        print()
        return

    # Require color for all other operations
    if not args.color:
        parser.print_help()
        sys.exit(0)

    # Parse input color
    try:
        base_rgb = parse_color(args.color)
    except ValueError as e:
        print(f"  {e}", file=sys.stderr)
        sys.exit(1)

    # Handle --identify (color identity info)
    if args.identify:
        print_color_identity(base_rgb)
        return

    # Generate palette
    if args.gradient:
        try:
            target_rgb = parse_color(args.gradient)
        except ValueError as e:
            print(f"  {e}", file=sys.stderr)
            sys.exit(1)
        palette = generate_gradient(base_rgb, target_rgb, args.steps)
        scheme_name = "gradient"
    elif args.all:
        # Show all schemes
        if not args.quiet:
            hex_str = rgb_to_hex(*base_rgb)
            h, s, l = rgb_to_hsl(*base_rgb)
            print(f"\n  color-brew -- Palettes from {hex_str} "
                  f"(hsl({h:.0f}, {s:.0f}%, {l:.0f}%))")
            print(f"  {'─' * 56}")

        for scheme_name, generator in SCHEMES.items():
            if scheme_name in ("monochromatic", "shades", "tints"):
                palette = generator(base_rgb, args.steps)
            else:
                palette = generator(base_rgb)

            if args.quiet:
                print(" ".join(rgb_to_hex(*c) for c in palette))
            else:
                print(f"\n  {scheme_name} ({len(palette)} colors)")
                if args.bar_style == "smooth":
                    print_smooth_bar(palette)
                else:
                    print_palette_bar(palette)
                print_palette(palette)

        # Also show contrast info and color identity
        if not args.quiet:
            print(f"\n  Contrast Ratios")
            print(f"  {'─' * 40}")
            for label, ref in [("White", (255, 255, 255)), ("Black", (0, 0, 0))]:
                ratio = get_contrast_ratio(base_rgb, ref)
                wcag_aa = "AA" if ratio >= 4.5 else "fail AA"
                wcag_aaa = "AAA" if ratio >= 7.0 else "fail AAA"
                large_aa = "AA" if ratio >= 3.0 else "fail AA"
                print(f"  {label:6s}: {ratio:.2f}:1  Large: {large_aa}  Normal: {wcag_aa}  {wcag_aaa}")
            print()
            # Show closest named color
            closest_name, closest_hex, dist = find_closest_color_name(base_rgb)
            if closest_name != "unknown":
                exact = " (exact match)" if dist < 1 else f" (distance: {dist:.1f})"
                print(f"  Closest named color: {closest_name}{exact}")
            print()

        return
    else:
        generator = SCHEMES[args.scheme]
        if args.scheme in ("monochromatic", "shades", "tints"):
            palette = generator(base_rgb, args.steps)
        else:
            palette = generator(base_rgb)
        scheme_name = args.scheme

    # Apply blend if requested
    if args.blend:
        try:
            blend_rgb = parse_color(args.blend)
        except ValueError as e:
            print(f"  {e}", file=sys.stderr)
            sys.exit(1)
        blend_gen = SCHEMES.get(args.scheme, generate_analogous)
        if args.scheme in ("monochromatic", "shades", "tints"):
            palette2 = blend_gen(blend_rgb, args.steps)
        else:
            palette2 = blend_gen(blend_rgb)
        if args.blend_mode == "interleave":
            palette = interleave_palettes(palette, palette2)
            scheme_name = f"{scheme_name}-interleaved"
        else:
            palette = blend_palettes(palette, palette2, args.blend_ratio)
            scheme_name = f"{scheme_name}-blended"

    # Quiet mode
    if args.quiet:
        print(" ".join(rgb_to_hex(*c) for c in palette))
        return

    # Display header
    hex_str = rgb_to_hex(*base_rgb)
    h, s, l = rgb_to_hsl(*base_rgb)
    print(f"\n  color-brew -- {scheme_name.upper()} palette from {hex_str}")
    print(f"  HSL({h:.0f}, {s:.0f}%, {l:.0f}%)")
    print(f"  {'─' * 50}")

    # Display palette with chosen bar style
    if args.bar_style == "smooth":
        print_smooth_bar(palette)
    else:
        print_palette_bar(palette)
    print_palette(palette)

    # Contrast check
    if args.contrast:
        contrast_colors = []
        for c in args.contrast:
            try:
                contrast_colors.append(parse_color(c))
            except ValueError as e:
                print(f"  {e}", file=sys.stderr)

        print(f"  Contrast Ratios")
        print(f"  {'─' * 40}")
        for i, color in enumerate(palette):
            for ref_name, ref_color in [(f"vs {c}", rc) for c, rc in zip(args.contrast, contrast_colors)]:
                ratio = get_contrast_ratio(color, ref_color)
                status = "PASS" if ratio >= 4.5 else "WARN" if ratio >= 3.0 else "FAIL"
                print(f"  {rgb_to_hex(*color)} {ref_name}: {ratio:.2f}:1 {status}")
        print()

    # Export
    if args.export:
        var_prefix = args.name or "color"
        _handle_export(palette, args, var_prefix)

    # Save to history
    if args.save:
        entry = save_palette_to_history(scheme_name, hex_str, palette)
        print(f"  Saved to history ({len(entry['colors'])} colors)")

    # Save to favorites
    if args.favorite:
        entry = save_to_favorites(args.favorite, scheme_name, hex_str, palette)
        print(f"  Saved to favorites as '{args.favorite}' ({len(entry['colors'])} colors)")

    # Copy to clipboard
    if args.copy:
        hex_values = " ".join(rgb_to_hex(*c) for c in palette)
        copy_to_clipboard(hex_values)
        print(f"  Copied to clipboard: {hex_values}")

    print()


def _export_by_format(palette: List[Tuple[int, int, int]], args, var_prefix: str) -> str:
    """Generate export content based on the selected format."""
    if args.export == "css":
        return export_css(palette, var_prefix)
    elif args.export == "scss":
        return export_scss(palette, var_prefix)
    elif args.export == "tailwind":
        return export_tailwind(palette, var_prefix)
    elif args.export == "json":
        return export_json(palette)
    elif args.export == "svg":
        return export_svg(palette)
    return ""


def _handle_export(palette: List[Tuple[int, int, int]], args, var_prefix: str):
    """Handle export: write to file or print to stdout."""
    if args.export == "png":
        output_path = args.output or "palette.png"
        export_png(palette, output_path)
        print(f"  PNG exported to {output_path}")
        return
    content = _export_by_format(palette, args, var_prefix)
    if not content:
        return
    if args.output:
        with open(args.output, 'w') as f:
            f.write(content)
        print(f"  Exported to {args.output} ({args.export} format)")
    else:
        print(f"\n  {args.export.upper()} Output:")
        print(f"  {'─' * 40}")
        for line in content.split('\n'):
            print(f"  {line}")
        print()


if __name__ == "__main__":
    main()
