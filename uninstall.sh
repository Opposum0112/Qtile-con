#!/usr/bin/env bash
set -euo pipefail
target="$HOME/.config/qtile"
[[ -d "$target" ]] || { echo "No ~/.config/qtile found."; exit 0; }
read -r -p "Move $target out of the way? [y/N] " answer
[[ "$answer" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 0; }
backup="$HOME/.config/qtile.removed.$(date +%Y%m%d-%H%M%S)"
mv "$target" "$backup"
echo "Configuration moved to $backup. Packages and wallpapers were not removed."
