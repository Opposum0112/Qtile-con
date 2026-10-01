#!/usr/bin/env python3
"""Convert a Catppuccin palette JSON into qtile_config/colors.py."""
import json
import pathlib
import sys

source = pathlib.Path(sys.argv[1]).expanduser()
target = pathlib.Path.home() / ".config/qtile/qtile_config/colors.py"
data = json.loads(source.read_text())
colors = data.get("colors", data)
# Accept simple {name: '#hex'} palettes only.
colors = {str(k): str(v) for k, v in colors.items() if isinstance(v, str) and v.startswith("#")}
required = {"base", "text", "mauve", "overlay", "surface0"}
if not required.issubset(colors):
    raise SystemExit(f"Palette missing required keys: {', '.join(sorted(required - colors.keys()))}")
lines = ['"""Generated palette; edit themes/*.json instead."""', f"COLORS = {colors!r}", 'BG = COLORS["base"]', 'FG = COLORS["text"]', 'ACCENT = COLORS["mauve"]', 'MUTED = COLORS["overlay"]', '']
target.write_text("\n".join(lines))
print(f"Updated {target}. Restart Qtile (Super+Ctrl+R) to reload the palette.")
