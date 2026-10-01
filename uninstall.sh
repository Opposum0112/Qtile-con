#!/usr/bin/env bash
# ==============================================================================
# Qtile-Con: Comprehensive Desktop Environment Uninstaller
#
# Purpose:
#   Cleanly and safely removes all configuration files, theme files, fonts,
#   standalone binaries, desktop session entries, and udev rules created by
#   Qtile-Con. If the '--purge' option is supplied, it also uninstalls all
#   system packages and pipx modules that were installed during the install phase.
#
# Usage:
#   ./uninstall.sh [OPTIONS]
#
# Options:
#   --dry-run       Preview all removal actions without altering the filesystem
#   --yes, -y       Skip interactive confirmation prompts
#   --purge         Uninstall all system dependencies that were installed by install.sh
#   --restore       Automatically restore previous ~/.config/qtile backup if available
#   -h, --help      Display this help message and exit
# ==============================================================================
set -Eeuo pipefail

DRY_RUN=0
ASSUME_YES=0
PURGE=0
RESTORE_BACKUP=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --purge|--all) PURGE=1 ;;
    --restore) RESTORE_BACKUP=1 ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --dry-run     Show items that would be removed without deleting anything"
      echo "  --yes, -y     Skip interactive confirmations"
      echo "  --purge       Completely remove configuration AND uninstall dependencies installed by install.sh"
      echo "  --restore     Automatically restore previous ~/.config/qtile backup if available"
      echo "  -h, --help    Show this help message and exit"
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/qtile"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/qtile-con"
MANIFEST_FILE=""

if [[ -f "$CONFIG_DIR/.install-manifest.json" ]]; then
  MANIFEST_FILE="$CONFIG_DIR/.install-manifest.json"
elif [[ -f "$DATA_DIR/install-manifest.json" ]]; then
  MANIFEST_FILE="$DATA_DIR/install-manifest.json"
fi

echo "================================================================="
echo " Qtile-Con: Desktop Environment Uninstaller"
echo "================================================================="

# ------------------------------------------------------------------------------
# 1. Parse Install Manifest (if available)
# ------------------------------------------------------------------------------
NEWLY_INSTALLED_PKGS=()
PIPX_PACKAGES=()
STANDALONE_BINS=()
INSTALLED_FONTS=()
CREATED_FILES=()
BACKUP_PATH=""
PM=""

if [[ -n "$MANIFEST_FILE" && -f "$MANIFEST_FILE" ]]; then
  echo "Found install manifest: $MANIFEST_FILE"
  eval "$(python3 -c "
import json
with open('$MANIFEST_FILE', 'r', encoding='utf-8') as f:
    data = json.load(f)

def bash_arr(name, lst):
    items = ' '.join(f'\"{x}\"' for x in lst)
    return f'{name}=({items})'

print(bash_arr('NEWLY_INSTALLED_PKGS', data.get('newly_installed_packages', [])))
print(bash_arr('PIPX_PACKAGES', data.get('pipx_packages', [])))
print(bash_arr('STANDALONE_BINS', data.get('standalone_binaries', [])))
print(bash_arr('INSTALLED_FONTS', data.get('installed_fonts', [])))
print(bash_arr('CREATED_FILES', data.get('created_files', [])))
print(f'BACKUP_PATH=\"{data.get(\"backup_path\", \"\")}\"')
print(f'PM=\"{data.get(\"package_manager\", \"\")}\"')
")"
else
  echo "Notice: No install manifest found. Standard file removal will be performed."
fi

# Fallback default created files to clean up even if manifest was absent
DEFAULT_FILES=(
  "$HOME/.config/libinput-gestures.conf"
  "$HOME/.config/alacritty/qtile-con-catppuccin-mocha.toml"
  "$HOME/.config/kitty/qtile-theme.conf"
  "$HOME/.config/kitty/kitty.conf"
  "$HOME/.config/helix/config.toml"
  "$HOME/.config/yazi/yazi.toml"
  "$HOME/.config/dunst/dunstrc"
  "$HOME/.config/micro/colorschemes/qtile-theme.micro"
  "/usr/share/xsessions/qtile.desktop"
  "/etc/X11/xorg.conf.d/40-libinput-touchpad.conf"
  "/etc/udev/rules.d/90-backlight.rules"
)
for df in "${DEFAULT_FILES[@]}"; do
  found=0
  for cf in "${CREATED_FILES[@]:-}"; do
    if [[ "$cf" == "$df" ]]; then found=1; break; fi
  done
  if [[ $found -eq 0 && -e "$df" ]]; then
    CREATED_FILES+=("$df")
  fi
done

echo ""
echo "Planned actions:"
echo "  • Remove Qtile configuration:  $CONFIG_DIR"
if [[ ${#CREATED_FILES[@]} -gt 0 ]]; then
  echo "  • Remove created files:        ${CREATED_FILES[*]}"
fi
if [[ ${#STANDALONE_BINS[@]} -gt 0 ]]; then
  echo "  • Remove standalone binaries:  ${STANDALONE_BINS[*]}"
fi
if [[ ${#INSTALLED_FONTS[@]} -gt 0 ]]; then
  echo "  • Remove installed font dirs:  ${INSTALLED_FONTS[*]}"
fi
if [[ "$PURGE" -eq 1 ]]; then
  if [[ ${#NEWLY_INSTALLED_PKGS[@]} -gt 0 ]]; then
    echo "  • Uninstall system packages:   ${NEWLY_INSTALLED_PKGS[*]}"
  fi
  if [[ ${#PIPX_PACKAGES[@]} -gt 0 ]]; then
    echo "  • Uninstall pipx packages:     ${PIPX_PACKAGES[*]}"
  fi
else
  echo "  • System packages:             PRESERVED (use --purge to uninstall packages installed by install.sh)"
fi

if [[ -n "$BACKUP_PATH" && -d "$BACKUP_PATH" ]]; then
  echo "  • Previous backup available:   $BACKUP_PATH"
fi
echo ""

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "--- DRY RUN COMPLETE: No changes were made ---"
  exit 0
fi

if [[ "$ASSUME_YES" -ne 1 ]]; then
  read -r -p "Proceed with uninstallation? [y/N] " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Uninstallation cancelled."; exit 0; }
fi

# ------------------------------------------------------------------------------
# 2. Stop and Disable Services (if purging)
# ------------------------------------------------------------------------------
if [[ "$PURGE" -eq 1 ]]; then
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl is-active --quiet cockpit.socket 2>/dev/null; then
      echo "Disabling cockpit.socket..."
      sudo systemctl disable --now cockpit.socket 2>/dev/null || true
    fi
  fi
fi

# ------------------------------------------------------------------------------
# 3. Uninstall System Packages via Host Package Manager (if purging)
# ------------------------------------------------------------------------------
if [[ "$PURGE" -eq 1 && -n "$PM" && ${#NEWLY_INSTALLED_PKGS[@]} -gt 0 ]]; then
  echo "Removing packages installed by Qtile-Con installer..."
  case "$PM" in
    apt)
      sudo apt-get remove --purge -y "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      sudo apt-get autoremove -y 2>/dev/null || true
      ;;
    pacman)
      sudo pacman -Rns --noconfirm "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    dnf)
      sudo dnf remove -y "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    zypper)
      sudo zypper remove -y "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    eopkg)
      sudo eopkg remove -y "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    xbps)
      sudo xbps-remove -Ry "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    emerge)
      sudo emerge --unmerge "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
    pkg)
      sudo pkg delete -y "${NEWLY_INSTALLED_PKGS[@]}" 2>/dev/null || true
      ;;
  esac
fi

# ------------------------------------------------------------------------------
# 4. Uninstall Pipx Packages (if purging)
# ------------------------------------------------------------------------------
if [[ "$PURGE" -eq 1 && ${#PIPX_PACKAGES[@]} -gt 0 ]]; then
  for pp in "${PIPX_PACKAGES[@]}"; do
    if command -v pipx >/dev/null 2>&1; then
      echo "Removing pipx package: $pp"
      pipx uninstall "$pp" 2>/dev/null || true
    fi
  done
fi

# ------------------------------------------------------------------------------
# 5. Remove Standalone Binaries (witr, fd symlink, etc.)
# ------------------------------------------------------------------------------
for sb in "${STANDALONE_BINS[@]:-}"; do
  if [[ -f "$sb" || -L "$sb" ]]; then
    echo "Removing binary: $sb"
    rm -f "$sb"
  fi
done

# ------------------------------------------------------------------------------
# 6. Remove Installed Fonts
# ------------------------------------------------------------------------------
for fdir in "${INSTALLED_FONTS[@]:-}"; do
  if [[ -d "$fdir" ]]; then
    echo "Removing font directory: $fdir"
    rm -rf "$fdir"
    if command -v fc-cache >/dev/null 2>&1; then
      fc-cache -f 2>/dev/null || true
    fi
  fi
done

# ------------------------------------------------------------------------------
# 7. Remove Created Files (Alacritty themes, Kitty, Dunst, Helix, Gestures, udev)
# ------------------------------------------------------------------------------
for cf in "${CREATED_FILES[@]:-}"; do
  if [[ -f "$cf" || -L "$cf" ]]; then
    echo "Removing created file: $cf"
    if [[ "$cf" =~ ^(/usr/|/etc/) ]]; then
      sudo rm -f "$cf" 2>/dev/null || rm -f "$cf" 2>/dev/null || true
    else
      rm -f "$cf"
    fi
  fi
done

# Reload udev rules if backlight rule was removed
if command -v udevadm >/dev/null 2>&1; then
  sudo udevadm control --reload-rules 2>/dev/null || true
fi

# ------------------------------------------------------------------------------
# 8. Clean Environment PATH lines in ~/.bashrc and ~/.profile
# ------------------------------------------------------------------------------
for pfile in "$HOME/.profile" "$HOME/.bashrc"; do
  if [[ -f "$pfile" ]]; then
    sed -i '/# Qtile-Con unified binary PATH/d' "$pfile" 2>/dev/null || true
    sed -i '/qtile\/scripts/d' "$pfile" 2>/dev/null || true
  fi
done

# ------------------------------------------------------------------------------
# 9. Remove or Archive Qtile Configuration Directory
# ------------------------------------------------------------------------------
if [[ -d "$CONFIG_DIR" ]]; then
  ARCHIVE_PATH="${CONFIG_DIR}.removed.$(date +%Y%m%d-%H%M%S)"
  mv "$CONFIG_DIR" "$ARCHIVE_PATH"
  echo "Qtile configuration moved to archive: $ARCHIVE_PATH"
fi

# Clean application runtime data directory
rm -rf "$DATA_DIR" 2>/dev/null || true

# ------------------------------------------------------------------------------
# 10. Restore Previous Backup (if requested)
# ------------------------------------------------------------------------------
if [[ "$RESTORE_BACKUP" -eq 1 && -n "$BACKUP_PATH" && -d "$BACKUP_PATH" ]]; then
  echo "Restoring previous backup from $BACKUP_PATH to $CONFIG_DIR..."
  cp -a "$BACKUP_PATH" "$CONFIG_DIR"
  echo "[OK] Previous configuration restored."
elif [[ -n "$BACKUP_PATH" && -d "$BACKUP_PATH" && "$ASSUME_YES" -ne 1 ]]; then
  read -r -p "A previous configuration backup was found ($BACKUP_PATH). Restore it? [y/N] " restore_confirm
  if [[ "$restore_confirm" =~ ^[Yy]$ ]]; then
    cp -a "$BACKUP_PATH" "$CONFIG_DIR"
    echo "[OK] Previous configuration restored."
  fi
fi

echo ""
echo "================================================================="
echo " Qtile-Con Uninstallation Complete!"
echo "================================================================="
