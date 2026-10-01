#!/usr/bin/env python3
"""Map pywal's generated palette to Qtile's semantic color names."""
import json
from pathlib import Path

source = Path.home() / ".cache/wal/colors.json"
target = Path.home() / ".config/qtile/qtile_config/colors.py"
if not source.exists():
    raise SystemExit("pywal colors.json not found")
raw = json.loads(source.read_text()).get("colors", {})
def get(key, fallback):
    value = raw.get(key, fallback)
    return value if isinstance(value, str) and value.startswith("#") else fallback
colors = {
    "base": get("color0", "#1e1e2e"), "mantle": get("color0", "#181825"),
    "crust": get("color0", "#11111b"), "text": get("color7", "#cdd6f4"),
    "subtext": get("color7", "#a6adc8"), "overlay": get("color8", "#6c7086"),
    "surface0": get("color1", "#313244"), "surface1": get("color8", "#45475a"),
    "surface2": get("color7", "#585b70"), "mauve": get("color5", "#cba6f7"),
    "blue": get("color4", "#89b4fa"), "teal": get("color6", "#94e2d5"),
    "green": get("color2", "#a6e3a1"), "red": get("color1", "#f38ba8"),
    "peach": get("color3", "#fab387"), "yellow": get("color3", "#f9e2af"),
    "pink": get("color5", "#f5c2e7"), "lavender": get("color4", "#b4befe"),
    "rosewater": get("color7", "#f5e0dc"), "flamingo": get("color7", "#f2cdcd"),
    "maroon": get("color1", "#eba0ac"), "sky": get("color6", "#89dceb"),
    "sapphire": get("color4", "#74c7ec"),
}
target.write_text('"""Generated from wallpaper via pywal."""\nCOLORS = ' + repr(colors) + '\nBG = COLORS["base"]\nFG = COLORS["text"]\nACCENT = COLORS["mauve"]\nMUTED = COLORS["overlay"]\n')
