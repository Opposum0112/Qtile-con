#!/usr/bin/env bash
set -euo pipefail
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1
ROOT="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$HOME/.config/qtile"
if command -v apt-get >/dev/null 2>&1; then PM=apt; packages=(python3 git fuzzel foot grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq libnotify-bin)
elif command -v dnf >/dev/null 2>&1; then PM=dnf; packages=(python3 git fuzzel foot grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq libnotify)
elif command -v pacman >/dev/null 2>&1; then PM=pacman; packages=(python git fuzzel foot grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq libnotify)
elif command -v zypper >/dev/null 2>&1; then PM=zypper; packages=(python3 git fuzzel foot grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq libnotify)
elif command -v eopkg >/dev/null 2>&1; then PM=eopkg; packages=(python3 git fuzzel foot grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq libnotify)
else PM=manual; fi
echo "Qtile-Con installer"
if [[ "$PM" == manual ]]; then
 echo "Install dependencies manually: python3 fuzzel foot swww grim slurp wl-clipboard cliphist playerctl pamixer brightnessctl curl jq notify-send"
elif [[ "$DRY_RUN" == 1 ]]; then echo "Dry run: would install using $PM: ${packages[*]}"
else
 read -r -p "Install dependencies with $PM? [y/N] " answer
 if [[ "$answer" =~ ^[Yy]$ ]]; then
  case "$PM" in
   apt) sudo apt-get update && sudo apt-get install -y "${packages[@]}";;
   dnf) sudo dnf install -y "${packages[@]}";;
   pacman) sudo pacman -S --needed "${packages[@]}";;
   zypper) sudo zypper install -y "${packages[@]}";;
   eopkg) sudo eopkg install -y "${packages[@]}";;
  esac
 fi
fi
if [[ "$DRY_RUN" == 1 ]]; then echo "Dry run: would back up $CONFIG and install files."; exit 0; fi
if [[ -e "$CONFIG" ]]; then backup="${CONFIG}.backup.$(date +%Y%m%d-%H%M%S)"; mv "$CONFIG" "$backup"; echo "Backup: $backup"; fi
mkdir -p "$CONFIG"
cp -a "$ROOT/config.py" "$ROOT/config" "$ROOT/scripts" "$ROOT/themes" "$CONFIG/"
chmod +x "$CONFIG"/scripts/*
echo "Installed to $CONFIG. Ensure Qtile is installed with Wayland support."
echo "Validate with: qtile check -c ~/.config/qtile/config.py"
