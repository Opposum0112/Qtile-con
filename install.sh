#!/usr/bin/env bash
# ==============================================================================
# Qtile-Con: Modern Cohesive X11 Desktop Environment Installer
# 
# Purpose:
#   Automated, OS-aware, and idempotent installer for the Qtile-Con environment.
#   Detects the host operating system and package manager, validates and installs
#   core and optional packages, sets up fallback tooling, deploys configurations
#   across all supported utilities, and records a manifest for clean removal.
#
# Supported Operating Systems & Package Managers:
#   • Debian / Ubuntu / Parrot OS / Kali / Mint (apt)
#   • Arch Linux / Manjaro / EndeavourOS (pacman)
#   • Fedora / Red Hat / CentOS / Rocky (dnf)
#   • openSUSE Leap 16.1 / Tumbleweed (zypper)
#   • Solus Linux (eopkg)
#   • Void Linux (xbps)
#   • FreeBSD (pkg)
#
# Idempotence:
#   Re-running this script will safely inspect already installed packages,
#   preserve prior configuration files, update in-place, and maintain install history.
# ==============================================================================
set -Eeuo pipefail

# ------------------------------------------------------------------------------
# CLI Flags & Option Parsing
# ------------------------------------------------------------------------------
DRY_RUN=0
ASSUME_YES=0
NO_DEPS=0
NO_SYSADMIN=0
NO_SECONDARY=0
NO_FONTS=0
NO_AI=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    --no-deps) NO_DEPS=1 ;;
    --no-sysadmin) NO_SYSADMIN=1 ;;
    --no-secondary) NO_SECONDARY=1 ;;
    --no-fonts) NO_FONTS=1 ;;
    --no-ai) NO_AI=1 ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --dry-run         Show detected OS, package manager, and planned actions without making changes"
      echo "  --yes, -y         Non-interactive mode (automatically accept all default prompts)"
      echo "  --no-deps         Skip system package installation; only configure Qtile desktop files"
      echo "  --no-sysadmin     Opt-out: do not install Cockpit Web Console and Snapper Btrfs tools"
      echo "  --no-secondary    Opt-out: do not install secondary editors/terminals (Kitty, Micro, Helix, Yazi)"
      echo "  --no-fonts        Opt-out: do not download extra Nerd Fonts (use existing system fonts)"
      echo "  --no-ai           Opt-out: do not install background AI agent monitoring tools"
      echo "  -h, --help        Show this help message and exit"
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/qtile"
ALACRITTY_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/alacritty"
KITTY_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/kitty"
MICRO_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/micro"
HELIX_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/helix"
YAZI_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/yazi"
DUNST_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/dunst"
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/qtile-con"

# ------------------------------------------------------------------------------
# 1. Repository Integrity Validation
# Ensure all critical modules, scripts, themes, and configuration files exist.
# ------------------------------------------------------------------------------
REQUIRED_FILES=(
  "config.py"
  "qtile_config/__init__.py"
  "qtile_config/colors.py"
  "qtile_config/groups.py"
  "qtile_config/keys.py"
  "qtile_config/layouts.py"
  "qtile_config/scroller.py"
  "qtile_config/screens.py"
  "qtile_config/settings.py"
  "qtile_config/widgets.py"
  "scripts/check-config"
  "scripts/autostart"
  "scripts/qtile-action"
  "scripts/qtile-run"
  "scripts/keybindings-cheatsheet"
  "scripts/apply-global-theme"
  "scripts/theme_apply.py"
  "scripts/set-theme"
  "scripts/set-wallpaper"
  "scripts/logout-menu"
  "scripts/weather"
  "scripts/weather-forecast"
  "scripts/set-weather-location"
  "scripts/volume-status"
  "scripts/volume-menu"
  "scripts/volume-slider"
  "scripts/wifi-status"
  "scripts/wifi-menu"
  "scripts/process-info"
  "scripts/services-info"
  "scripts/battery-status"
  "scripts/critical-indicators"
  "scripts/sys-investigate"
  "scripts/clipboard-history"
  "scripts/man-lookup"
  "scripts/rofi-file-search"
  "scripts/rofi-content-search"
  "scripts/screenshot"
  "scripts/setup-gestures"
  "scripts/cockpit-info"
  "scripts/ai-agents-info"
  "scripts/snapper-info"
  "themes/catppuccin-mocha.json"
  "themes/catppuccin-mocha.rasi"
  "themes/catppuccin-mocha-grid.rasi"
  "themes/catppuccin-mocha-weather.rasi"
  "alacritty/alacritty.toml"
  "alacritty/catppuccin-mocha.toml"
  "kitty/kitty.conf"
  "helix/config.toml"
  "yazi/yazi.toml"
  "dunst/dunstrc"
  "gestures/libinput-gestures.conf"
  "udev/90-backlight.rules"
)

for req in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$ROOT/$req" ]]; then
    echo "ERROR: Required repository file is missing: $req" >&2
    exit 2
  fi
done

# ------------------------------------------------------------------------------
# 2. OS & Package Manager Detection
# Supports Linux distributions and BSD variants.
# ------------------------------------------------------------------------------
OS_ID="unknown"
OS_LIKE=""
OS_NAME="Unknown Linux"
PM=""
PM_FAMILY=""

if [[ "$(uname -s)" == "FreeBSD" ]]; then
  OS_ID="freebsd"
  OS_NAME="FreeBSD"
  PM=pkg
  PM_FAMILY=freebsd
elif [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  OS_ID="${ID:-unknown}"
  OS_LIKE="${ID_LIKE:-}"
  OS_NAME="${PRETTY_NAME:-$OS_ID}"
fi

if [[ -z "$PM" ]]; then
  case "$OS_ID" in
    debian|ubuntu|linuxmint|pop|parrot|kali|raspbian)
      PM=apt
      PM_FAMILY=debian
      ;;
    arch|manjaro|endeavouros|garuda|artix)
      PM=pacman
      PM_FAMILY=arch
      ;;
    fedora|nobara|rhel|centos|rocky|alma)
      PM=dnf
      PM_FAMILY=fedora
      ;;
    opensuse*|suse)
      PM=zypper
      PM_FAMILY=suse
      ;;
    solus)
      PM=eopkg
      PM_FAMILY=solus
      ;;
    void)
      PM=xbps
      PM_FAMILY=void
      ;;
    gentoo)
      PM=emerge
      PM_FAMILY=gentoo
      ;;
    freebsd)
      PM=pkg
      PM_FAMILY=freebsd
      ;;
    *)
      if [[ "$OS_LIKE" =~ (debian|ubuntu) ]]; then PM=apt; PM_FAMILY=debian;
      elif [[ "$OS_LIKE" =~ (arch) ]]; then PM=pacman; PM_FAMILY=arch;
      elif [[ "$OS_LIKE" =~ (fedora|rhel) ]]; then PM=dnf; PM_FAMILY=fedora;
      elif [[ "$OS_LIKE" =~ (suse) ]]; then PM=zypper; PM_FAMILY=suse;
      elif [[ "$OS_LIKE" =~ (void) ]]; then PM=xbps; PM_FAMILY=void;
      elif [[ "$OS_LIKE" =~ (gentoo) ]]; then PM=emerge; PM_FAMILY=gentoo;
      elif command -v apt-get >/dev/null 2>&1; then PM=apt; PM_FAMILY=debian;
      elif command -v pacman >/dev/null 2>&1; then PM=pacman; PM_FAMILY=arch;
      elif command -v dnf >/dev/null 2>&1; then PM=dnf; PM_FAMILY=fedora;
      elif command -v zypper >/dev/null 2>&1; then PM=zypper; PM_FAMILY=suse;
      elif command -v xbps-install >/dev/null 2>&1; then PM=xbps; PM_FAMILY=void;
      elif command -v emerge >/dev/null 2>&1; then PM=emerge; PM_FAMILY=gentoo;
      elif command -v eopkg >/dev/null 2>&1; then PM=eopkg; PM_FAMILY=solus;
      elif command -v pkg >/dev/null 2>&1; then PM=pkg; PM_FAMILY=freebsd;
      fi
      ;;
  esac
fi

# ------------------------------------------------------------------------------
# 3. Interactive Opt-Out Prompts (if not in unattended/dry-run mode)
# ------------------------------------------------------------------------------
if [[ "$ASSUME_YES" -ne 1 && "$DRY_RUN" -ne 1 ]]; then
  if [[ "$NO_SYSADMIN" -eq 0 ]]; then
    read -r -p "Install SysAdmin management tools (Cockpit Web Console & Snapper)? [Y/n] " prompt_sysadmin
    [[ "$prompt_sysadmin" =~ ^[Nn]$ ]] && NO_SYSADMIN=1
  fi
  if [[ "$NO_SECONDARY" -eq 0 ]]; then
    read -r -p "Install secondary editors & terminal (Kitty, Micro, Helix, Yazi)? [Y/n] " prompt_secondary
    [[ "$prompt_secondary" =~ ^[Nn]$ ]] && NO_SECONDARY=1
  fi
  if [[ "$NO_FONTS" -eq 0 ]]; then
    read -r -p "Download and install JetBrainsMono Nerd Font? [Y/n] " prompt_fonts
    [[ "$prompt_fonts" =~ ^[Nn]$ ]] && NO_FONTS=1
  fi
  if [[ "$NO_AI" -eq 0 ]]; then
    read -r -p "Enable background AI agent monitoring tools? [Y/n] " prompt_ai
    [[ "$prompt_ai" =~ ^[Nn]$ ]] && NO_AI=1
  fi
fi

# ------------------------------------------------------------------------------
# 4. OS-Specific Prerequisites Definition
# ------------------------------------------------------------------------------
BASE_PKGS=()
EXTRA_PKGS=()

case "$PM_FAMILY" in
  debian)
    BASE_PKGS=(
      python3 git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify-bin
      python3-pip pipx python3-cairocffi python3-xcffib python3-dbus python3-psutil python3-requests libpangocairo-1.0-0
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl network-manager-gnome i3lock micro kitty dunst xdotool
      libinput-tools man-db gcc make libx11-dev libxtst-dev fd-find ripgrep cockpit snapper
    )
    ;;
  arch)
    BASE_PKGS=(
      python git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify
      python-pip python-pipx python-cairocffi python-xcffib python-dbus python-psutil python-requests pango qtile
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl network-manager-applet nm-connection-editor i3lock micro kitty dunst xdotool
      libinput-gestures man-db gcc make libx11 libxtst fd ripgrep cockpit snapper
    )
    ;;
  fedora)
    BASE_PKGS=(
      python3 git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify
      python3-pip pipx python3-cairocffi python3-xcffib python3-dbus python3-psutil python3-requests pango qtile
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl NetworkManager-gnome i3lock micro kitty dunst xdotool
      libinput man-db gcc make libX11-devel libXtst-devel fd-find ripgrep cockpit snapper
    )
    ;;
  suse)
    BASE_PKGS=(
      python3 git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify-tools
      python3-pip python3-pipx python3-cairocffi python3-xcffib python3-dbus-python python3-psutil python3-requests pango qtile
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl NetworkManager-applet i3lock micro kitty dunst xdotool
      man-db gcc make libX11-devel libXtst-devel fd ripgrep cockpit snapper
    )
    ;;
  solus)
    BASE_PKGS=(
      python3 git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify pipx
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl nm-connection-editor network-manager-applet i3lock micro kitty dunst xdotool man-db gcc make fd ripgrep
    )
    ;;
  void)
    BASE_PKGS=(
      python3 git rofi alacritty feh maim xclip xsel playerctl curl jq libnotify
      python3-pip pipx python3-cairocffi python3-xcffib python3-dbus python3-psutil python3-requests pango qtile
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils brightnessctl NetworkManager i3lock micro kitty dunst xdotool
      libinput-gestures man-db gcc make libX11-devel libXtst-devel fd ripgrep cockpit snapper
    )
    ;;
  gentoo)
    BASE_PKGS=(
      dev-lang/python dev-vcs/git x11-misc/rofi x11-terms/alacritty media-gfx/feh media-gfx/maim x11-misc/xclip x11-misc/xsel
      media-sound/playerctl net-misc/curl app-misc/jq x11-libs/libnotify dev-python/pip dev-python/pipx dev-python/cairocffi
      dev-python/xcffib dev-python/dbus-python dev-python/psutil dev-python/requests x11-libs/pango x11-wm/qtile
    )
    EXTRA_PKGS=(
      sys-process/btop sys-process/htop media-sound/pamixer media-sound/pavucontrol media-sound/alsa-utils sys-power/brightnessctl
      net-misc/networkmanager x11-misc/i3lock app-editors/micro x11-terms/kitty x11-misc/dunst x11-misc/xdotool
      sys-apps/man-db sys-devel/gcc sys-devel/make x11-libs/libX11 x11-libs/libXtst sys-apps/fd sys-apps/ripgrep sys-apps/snapper
    )
    ;;
  freebsd)
    BASE_PKGS=(
      python3 git rofi alacritty feh playerctl curl jq libnotify
      py311-pip py311-cairocffi py311-xcffib py311-dbus py311-psutil py311-requests pango
    )
    EXTRA_PKGS=(
      btop htop pamixer pavucontrol alsa-utils i3lock micro kitty dunst xdotool
      man-db gcc gmake libX11 libXtst fd-find ripgrep
    )
    ;;
  *)
    BASE_PKGS=(python3 git rofi alacritty feh maim xclip xsel playerctl curl jq)
    EXTRA_PKGS=(btop htop pamixer pavucontrol brightnessctl i3lock micro kitty dunst xdotool gcc make fd-find ripgrep)
    ;;
esac

# Filter extra packages according to user opt-outs
FILTERED_EXTRA=()
for p in "${EXTRA_PKGS[@]}"; do
  if [[ "$NO_SYSADMIN" -eq 1 ]] && [[ "$p" =~ ^(cockpit|snapper) ]]; then
    continue
  fi
  if [[ "$NO_SECONDARY" -eq 1 ]] && [[ "$p" =~ ^(kitty|micro|helix|yazi) ]]; then
    continue
  fi
  FILTERED_EXTRA+=("$p")
done
EXTRA_PKGS=("${FILTERED_EXTRA[@]}")

echo "================================================================="
echo " Qtile-Con: Modern Cohesive X11 Desktop Environment Installer"
echo "================================================================="
echo "Operating System: $OS_NAME"
echo "Package Manager:  ${PM:-None detected (Manual dependency install)}"
echo "Config Target:    $CONFIG_DIR"
echo "Opt-outs:         SysAdmin=$NO_SYSADMIN, Secondary=$NO_SECONDARY, Fonts=$NO_FONTS, AI=$NO_AI"
echo ""

is_pkg_installed() {
  local pkg="$1"
  case "$PM" in
    apt)
      dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "ok installed"
      ;;
    pacman)
      pacman -Qq "$pkg" >/dev/null 2>&1
      ;;
    dnf)
      rpm -q "$pkg" >/dev/null 2>&1
      ;;
    zypper)
      rpm -q "$pkg" >/dev/null 2>&1
      ;;
    eopkg)
      eopkg list-installed 2>/dev/null | grep -qw "$pkg"
      ;;
    xbps)
      xbps-query "$pkg" >/dev/null 2>&1
      ;;
    emerge)
      (command -v qlist >/dev/null 2>&1 && qlist -I "$pkg" >/dev/null 2>&1) || \
      (command -v equery >/dev/null 2>&1 && equery list "$pkg" >/dev/null 2>&1) || \
      [[ -d "/var/db/pkg/$pkg" ]] || \
      command -v "${pkg##*/}" >/dev/null 2>&1
      ;;
    pkg)
      pkg info -e "$pkg" >/dev/null 2>&1
      ;;
    *)
      command -v "$pkg" >/dev/null 2>&1
      ;;
  esac
}

# Plan packages to install (differentiate already installed vs new)
TO_INSTALL_BASE=()
TO_INSTALL_EXTRA=()

if [[ -n "$PM" && "$NO_DEPS" -eq 0 ]]; then
  for p in "${BASE_PKGS[@]}"; do
    if ! is_pkg_installed "$p"; then
      TO_INSTALL_BASE+=("$p")
    fi
  done

  for p in "${EXTRA_PKGS[@]}"; do
    if ! is_pkg_installed "$p"; then
      TO_INSTALL_EXTRA+=("$p")
    fi
  done
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "--- DRY RUN SUMMARY ---"
  echo "Base packages needing installation:  ${TO_INSTALL_BASE[*]:-None (All present)}"
  echo "Extra packages needing installation: ${TO_INSTALL_EXTRA[*]:-None (All present)}"
  echo "Target config directory:             $CONFIG_DIR"
  echo "Alacritty theme target:              $ALACRITTY_CONFIG_DIR"
  echo "Kitty config target:                 $KITTY_CONFIG_DIR"
  echo "Helix config target:                 $HELIX_CONFIG_DIR"
  echo "Yazi config target:                  $YAZI_CONFIG_DIR"
  echo "Nerd Font installation check:        $([[ $NO_FONTS -eq 1 ]] && echo 'Skipped (--no-fonts)' || echo 'Enabled')"
  echo "Process causation tracer (witr):     Enabled (Will install binary if missing)"
  echo "Native gesture daemon compilation:   Enabled (Will compile C daemon if gcc available)"
  echo "Manifest file path:                  $DATA_DIR/install-manifest.json"
  echo "-----------------------"
  exit 0
fi

# Track components for uninstaller manifest (and load previous manifest if available for idempotence)
add_unique() {
  local -n arr=$1
  local val="$2"
  for item in "${arr[@]:-}"; do
    if [[ "$item" == "$val" ]]; then return 0; fi
  done
  arr+=("$val")
}

PREV_MANIFEST=""
if [[ -f "$CONFIG_DIR/.install-manifest.json" ]]; then
  PREV_MANIFEST="$CONFIG_DIR/.install-manifest.json"
elif [[ -f "$DATA_DIR/install-manifest.json" ]]; then
  PREV_MANIFEST="$DATA_DIR/install-manifest.json"
fi

NEWLY_INSTALLED_PKGS=()
PIPX_PACKAGES=()
STANDALONE_BINS=()
INSTALLED_FONTS=()
CREATED_FILES=()
ORIGINAL_BACKUP_PATH=""

if [[ -n "$PREV_MANIFEST" && -f "$PREV_MANIFEST" ]]; then
  echo "Found existing install manifest: $PREV_MANIFEST (preserving previous install history)"
  eval "$(python3 -c "
import json
try:
    with open('$PREV_MANIFEST', 'r', encoding='utf-8') as f:
        data = json.load(f)
    def bash_arr(name, lst):
        items = ' '.join(f'\"{x}\"' for x in lst)
        return f'{name}=({items})'
    print(bash_arr('NEWLY_INSTALLED_PKGS', data.get('newly_installed_packages', [])))
    print(bash_arr('PIPX_PACKAGES', data.get('pipx_packages', [])))
    print(bash_arr('STANDALONE_BINS', data.get('standalone_binaries', [])))
    print(bash_arr('INSTALLED_FONTS', data.get('installed_fonts', [])))
    print(bash_arr('CREATED_FILES', data.get('created_files', [])))
    print(f'ORIGINAL_BACKUP_PATH=\"{data.get(\"backup_path\", \"\")}\"')
except Exception:
    pass
")"
fi

# ------------------------------------------------------------------------------
# 5. Install Packages via Native Package Manager
# ------------------------------------------------------------------------------
if [[ -n "$PM" && "$NO_DEPS" -eq 0 ]]; then
  if [[ ${#TO_INSTALL_BASE[@]} -eq 0 && ${#TO_INSTALL_EXTRA[@]} -eq 0 ]]; then
    echo "[OK] All required and optional system packages are already installed."
  else
    echo "The following dependencies will be installed:"
    [[ ${#TO_INSTALL_BASE[@]} -gt 0 ]] && echo "  Base:  ${TO_INSTALL_BASE[*]}"
    [[ ${#TO_INSTALL_EXTRA[@]} -gt 0 ]] && echo "  Extra: ${TO_INSTALL_EXTRA[*]}"
    echo ""

    if [[ "$ASSUME_YES" -ne 1 ]]; then
      read -r -p "Proceed with package installation? [Y/n] " confirm
      [[ "$confirm" =~ ^[Nn]$ ]] && { echo "Package installation skipped by user."; TO_INSTALL_BASE=(); TO_INSTALL_EXTRA=(); }
    fi

    if [[ ${#TO_INSTALL_BASE[@]} -gt 0 || ${#TO_INSTALL_EXTRA[@]} -gt 0 ]]; then
      echo "Updating package repository index..."
      case "$PM" in
        apt) sudo apt-get update -y || echo "WARNING: apt update failed, attempting installation anyway..." >&2 ;;
        pacman) sudo pacman -Sy --noconfirm || echo "WARNING: pacman sync failed, attempting installation anyway..." >&2 ;;
        dnf) sudo dnf makecache || echo "WARNING: dnf makecache failed, attempting installation anyway..." >&2 ;;
        zypper) sudo zypper refresh || echo "WARNING: zypper refresh failed, attempting installation anyway..." >&2 ;;
        eopkg) sudo eopkg update-repo || true ;;
        xbps) sudo xbps-install -S || true ;;
        emerge) sudo emerge --sync || true ;;
        pkg) sudo pkg update || true ;;
      esac

      install_pkg() {
        local p="$1"
        local is_required="$2"
        echo "--> Installing: $p"
        local rc=0
        case "$PM" in
          apt) sudo apt-get install -y "$p" || rc=$? ;;
          pacman) sudo pacman -S --needed --noconfirm "$p" || rc=$? ;;
          dnf) sudo dnf install -y "$p" || rc=$? ;;
          zypper) sudo zypper --non-interactive install "$p" || rc=$? ;;
          eopkg) sudo eopkg install -y "$p" || rc=$? ;;
          xbps) sudo xbps-install -y "$p" || rc=$? ;;
          emerge) sudo emerge --ask=n --oneshot "$p" || rc=$? ;;
          pkg) sudo pkg install -y "$p" || rc=$? ;;
        esac
        if [[ $rc -eq 0 ]]; then
          add_unique NEWLY_INSTALLED_PKGS "$p"
        else
          if [[ "$is_required" == "1" ]]; then
            echo "WARNING: Required package '$p' failed to install." >&2
          else
            echo "Notice: Optional package '$p' not available in repository; continuing."
          fi
        fi
      }

      for p in "${TO_INSTALL_BASE[@]}"; do
        install_pkg "$p" 1
      done

      for p in "${TO_INSTALL_EXTRA[@]}"; do
        install_pkg "$p" 0
      done
    fi
  fi
fi

# ------------------------------------------------------------------------------
# 6. Fallback for Qtile Window Manager (pipx / pip3)
# ------------------------------------------------------------------------------
export PATH="$HOME/.local/bin:$HOME/.local/share/pipx/venvs/qtile/bin:$PATH"
if command -v qtile >/dev/null 2>&1; then
  echo "[OK] Qtile window manager is available ($(command -v qtile))."
else
  echo "Qtile executable not found on PATH. Attempting automated fallback installation..."
  if command -v pipx >/dev/null 2>&1; then
    if pipx list 2>/dev/null | grep -q "package qtile"; then
      echo "Qtile is already installed in pipx environment."
    else
      echo "Installing Qtile via pipx..."
      pipx install "qtile>=0.28.0" || true
      pipx inject qtile psutil requests dbus-python 2>/dev/null || true
    fi
    add_unique PIPX_PACKAGES "qtile"
  elif command -v pip3 >/dev/null 2>&1; then
    echo "Installing Qtile via pip3 --user..."
    pip3 install --user "qtile>=0.28.0" psutil requests || true
  else
    echo "WARNING: Neither package manager, pipx, nor pip3 could install Qtile." >&2
    echo "Please install Qtile with its X11 backend manually before starting a session." >&2
  fi
fi

# ------------------------------------------------------------------------------
# 7. Fallback for 'witr' Process Causation Tracer
# ------------------------------------------------------------------------------
if command -v witr >/dev/null 2>&1 || [[ -x "$HOME/.local/bin/witr" ]]; then
  echo "[OK] 'witr' process causation tracer is already installed."
else
  echo "Installing 'witr' (Why Is This Running? process causality tracer)..."
  mkdir -p "$HOME/.local/bin"
  arch="$(uname -m)"
  case "$arch" in
    x86_64) witr_arch="linux-amd64" ;;
    aarch64|arm64) witr_arch="linux-arm64" ;;
    *) witr_arch="" ;;
  esac
  if [[ -n "$witr_arch" ]]; then
    if curl -fsSL -o "$HOME/.local/bin/witr" "https://github.com/pranshuparmar/witr/releases/download/v0.3.3/witr-${witr_arch}" 2>/dev/null; then
      chmod +x "$HOME/.local/bin/witr"
      add_unique STANDALONE_BINS "$HOME/.local/bin/witr"
      echo "[OK] Installed witr to $HOME/.local/bin/witr"
    fi
  fi
fi

# ------------------------------------------------------------------------------
# 8. Fallback for JetBrainsMono Nerd Font
# ------------------------------------------------------------------------------
has_nerd_font() {
  if command -v fc-list >/dev/null 2>&1; then
    fc-list : family | grep -qi "JetBrainsMono.*Nerd Font" && return 0
  fi
  if [[ -d "$HOME/.local/share/fonts/JetBrainsMono" ]] && [[ $(find "$HOME/.local/share/fonts/JetBrainsMono" -name "*.ttf" 2>/dev/null | head -n 1) ]]; then
    return 0
  fi
  return 1
}

if [[ "$NO_FONTS" -eq 1 ]]; then
  echo "Notice: JetBrainsMono font download skipped (--no-fonts)."
elif has_nerd_font; then
  echo "[OK] JetBrainsMono Nerd Font is already installed."
else
  echo "JetBrainsMono Nerd Font not detected. Downloading and installing..."
  FONT_DIR="$HOME/.local/share/fonts/JetBrainsMono"
  mkdir -p "$FONT_DIR"
  FONT_URL="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.tar.xz"
  if curl -fsSL "$FONT_URL" | tar -xJ -C "$FONT_DIR" 2>/dev/null; then
    if command -v fc-cache >/dev/null 2>&1; then
      fc-cache -f "$FONT_DIR" 2>/dev/null || true
    fi
    add_unique INSTALLED_FONTS "$FONT_DIR"
    echo "[OK] JetBrainsMono Nerd Font installed successfully."
  else
    echo "Notice: Could not download Nerd Font automatically. Bar icons will use system monospace font."
  fi
fi

# ------------------------------------------------------------------------------
# 9. Native Gesture Daemon compilation
# ------------------------------------------------------------------------------
if [[ -f "$ROOT/scripts/gesture-daemon.c" ]]; then
  if [[ ! -x "$ROOT/scripts/gesture-daemon" ]] || [[ "$ROOT/scripts/gesture-daemon.c" -nt "$ROOT/scripts/gesture-daemon" ]]; then
    if command -v gcc >/dev/null 2>&1; then
      echo "Compiling native sub-millisecond X11 gesture daemon..."
      gcc -O2 -Wall "$ROOT/scripts/gesture-daemon.c" -lX11 -lXtst -o "$ROOT/scripts/gesture-daemon" 2>/dev/null && chmod +x "$ROOT/scripts/gesture-daemon" || true
    fi
  else
    echo "[OK] Native gesture daemon is already compiled and up to date."
  fi
fi

# Touchpad input group permission check
if ! groups 2>/dev/null | grep -qw "input"; then
  echo "Notice: Adding user '$USER' to 'input' group for hardware touchpad gesture monitoring..."
  sudo gpasswd -a "$USER" input 2>/dev/null || sudo usermod -aG input "$USER" 2>/dev/null || true
fi

# ------------------------------------------------------------------------------
# 10. Backup Existing Configuration
# ------------------------------------------------------------------------------
BACKUP_PATH="$ORIGINAL_BACKUP_PATH"
if [[ -d "$CONFIG_DIR" ]]; then
  # Check if $CONFIG_DIR is an existing Qtile-Con configuration
  if [[ -f "$CONFIG_DIR/.install-manifest.json" ]] || [[ -f "$CONFIG_DIR/qtile_config/__init__.py" && -f "$CONFIG_DIR/scripts/qtile-run" ]]; then
    echo "Existing Qtile-Con deployment detected in $CONFIG_DIR (updating in place)..."
  else
    BACKUP_PATH="${CONFIG_DIR}.backup.$(date +%Y%m%d-%H%M%S)"
    echo "Backing up existing non-Qtile-Con config to: $BACKUP_PATH"
    mv "$CONFIG_DIR" "$BACKUP_PATH"
  fi
fi

# ------------------------------------------------------------------------------
# 11. Deploy Cohesive Qtile Configuration
# ------------------------------------------------------------------------------
echo "Deploying cohesive Qtile configuration to $CONFIG_DIR..."
mkdir -p "$CONFIG_DIR"
cp -a "$ROOT/config.py" "$CONFIG_DIR/"
cp -a "$ROOT/qtile_config" "$CONFIG_DIR/"
cp -a "$ROOT/scripts" "$CONFIG_DIR/"
cp -a "$ROOT/themes" "$CONFIG_DIR/"
chmod +x "$CONFIG_DIR/scripts/"*

# Ensure user asset directories exist
mkdir -p "$HOME/Pictures/Wallpapers" "$HOME/Pictures/Screenshots" "$HOME/.cache" "$HOME/.local/bin"

# Ensure fd symlink if fdfind is installed (standard on Debian/Ubuntu)
if ! command -v fd >/dev/null 2>&1 && command -v fdfind >/dev/null 2>&1; then
  ln -sf "$(command -v fdfind)" "$HOME/.local/bin/fd"
  add_unique STANDALONE_BINS "$HOME/.local/bin/fd"
  echo "[OK] Symlinked fdfind -> ~/.local/bin/fd"
fi

# Deploy libinput-gestures configuration
mkdir -p "$HOME/.config"
if [[ ! -f "$HOME/.config/libinput-gestures.conf" ]] || ! cmp -s "$ROOT/gestures/libinput-gestures.conf" "$HOME/.config/libinput-gestures.conf"; then
  cp -f "$ROOT/gestures/libinput-gestures.conf" "$HOME/.config/libinput-gestures.conf"
fi
add_unique CREATED_FILES "$HOME/.config/libinput-gestures.conf"

# Deploy Alacritty configuration & theme
mkdir -p "$ALACRITTY_CONFIG_DIR"
cp -f "$ROOT/alacritty/catppuccin-mocha.toml" "$ALACRITTY_CONFIG_DIR/qtile-con-catppuccin-mocha.toml"
add_unique CREATED_FILES "$ALACRITTY_CONFIG_DIR/qtile-con-catppuccin-mocha.toml"
if [[ ! -f "$ALACRITTY_CONFIG_DIR/alacritty.toml" ]]; then
  cp -f "$ROOT/alacritty/alacritty.toml" "$ALACRITTY_CONFIG_DIR/alacritty.toml"
  add_unique CREATED_FILES "$ALACRITTY_CONFIG_DIR/alacritty.toml"
  echo "[OK] Configured Alacritty starter configuration."
fi

# Deploy Kitty theme & configuration
mkdir -p "$KITTY_CONFIG_DIR"
if [[ ! -f "$KITTY_CONFIG_DIR/kitty.conf" ]]; then
  cp -f "$ROOT/kitty/kitty.conf" "$KITTY_CONFIG_DIR/kitty.conf"
  add_unique CREATED_FILES "$KITTY_CONFIG_DIR/kitty.conf"
  echo "[OK] Configured Kitty starter configuration."
fi
if [[ ! -f "$CONFIG_DIR/themes/current_theme.json" ]]; then
  cp -f "$ROOT/themes/catppuccin-mocha.json" "$CONFIG_DIR/themes/current_theme.json" 2>/dev/null || true
fi

# Deploy Dunst notification daemon configuration
mkdir -p "$DUNST_CONFIG_DIR"
if [[ ! -f "$DUNST_CONFIG_DIR/dunstrc" ]]; then
  cp -f "$ROOT/dunst/dunstrc" "$DUNST_CONFIG_DIR/dunstrc"
  add_unique CREATED_FILES "$DUNST_CONFIG_DIR/dunstrc"
  echo "[OK] Configured Dunst notification daemon."
fi

# Deploy Helix configuration
mkdir -p "$HELIX_CONFIG_DIR"
if [[ ! -f "$HELIX_CONFIG_DIR/config.toml" ]]; then
  cp -f "$ROOT/helix/config.toml" "$HELIX_CONFIG_DIR/config.toml"
  add_unique CREATED_FILES "$HELIX_CONFIG_DIR/config.toml"
  echo "[OK] Configured Helix editor."
fi

# Deploy Yazi configuration
mkdir -p "$YAZI_CONFIG_DIR"
if [[ ! -f "$YAZI_CONFIG_DIR/yazi.toml" ]]; then
  cp -f "$ROOT/yazi/yazi.toml" "$YAZI_CONFIG_DIR/yazi.toml"
  add_unique CREATED_FILES "$YAZI_CONFIG_DIR/yazi.toml"
  echo "[OK] Configured Yazi terminal file manager."
fi

# Deploy Micro theme directory if micro is installed
if command -v micro >/dev/null 2>&1 || [[ -d "$MICRO_CONFIG_DIR" ]]; then
  mkdir -p "$MICRO_CONFIG_DIR/colorschemes"
fi

# Deploy udev backlight brightness rules if running as root or with sudo
if [[ -d "/etc/udev/rules.d" ]] && (sudo -n true 2>/dev/null || [[ "$ASSUME_YES" -eq 1 ]]); then
  if [[ ! -f "/etc/udev/rules.d/90-backlight.rules" ]]; then
    sudo cp -f "$ROOT/udev/90-backlight.rules" /etc/udev/rules.d/90-backlight.rules 2>/dev/null || true
    if command -v udevadm >/dev/null 2>&1; then
      sudo udevadm control --reload-rules 2>/dev/null || true
      sudo udevadm trigger --subsystem-match=backlight 2>/dev/null || true
    fi
    add_unique CREATED_FILES "/etc/udev/rules.d/90-backlight.rules"
    echo "[OK] Installed udev brightness control rule."
  fi
fi

# ------------------------------------------------------------------------------
# 12. Synchronize Default or Active Global Theme across all apps
# ------------------------------------------------------------------------------
CURRENT_THEME="catppuccin-mocha"
if [[ -f "$CONFIG_DIR/themes/current_theme.json" ]]; then
  DETECTED_THEME=$(python3 -c "import json; print(json.load(open('$CONFIG_DIR/themes/current_theme.json')).get('name', ''))" 2>/dev/null || echo "")
  if [[ -n "$DETECTED_THEME" ]]; then
    CURRENT_THEME="$DETECTED_THEME"
  fi
fi
echo "Synchronizing global theme ($CURRENT_THEME)..."
if [[ -x "$CONFIG_DIR/scripts/apply-global-theme" ]]; then
  python3 "$CONFIG_DIR/scripts/apply-global-theme" "$CURRENT_THEME" --no-restart-firefox >/dev/null 2>&1 || true
fi

# ------------------------------------------------------------------------------
# 13. Setup X11 Desktop Session entry
# ------------------------------------------------------------------------------
if [[ -d "/usr/share/xsessions" ]]; then
  if [[ ! -f "/usr/share/xsessions/qtile.desktop" ]]; then
    if sudo -n true 2>/dev/null || [[ "$ASSUME_YES" -eq 1 ]]; then
      echo "Creating /usr/share/xsessions/qtile.desktop for display manager selection..."
      sudo tee /usr/share/xsessions/qtile.desktop >/dev/null << 'EOF'
[Desktop Entry]
Name=Qtile
Comment=Qtile X11 Window Manager
Exec=qtile start
Type=Application
Keywords=wm;tiling
EOF
      add_unique CREATED_FILES "/usr/share/xsessions/qtile.desktop"
    fi
  else
    add_unique CREATED_FILES "/usr/share/xsessions/qtile.desktop"
  fi
fi

# Setup X11 Touchpad Configuration (Tap-to-click, Natural Scrolling)
echo "Configuring touchpad tap-to-click and natural scrolling..."
if [[ -x "$CONFIG_DIR/scripts/setup-touchpad" ]]; then
  "$CONFIG_DIR/scripts/setup-touchpad" --verbose >/dev/null 2>&1 || true
fi
if [[ -d "/etc/X11/xorg.conf.d" ]] && (sudo -n true 2>/dev/null || [[ "$ASSUME_YES" -eq 1 ]]); then
  if [[ ! -f "/etc/X11/xorg.conf.d/40-libinput-touchpad.conf" ]]; then
    sudo tee /etc/X11/xorg.conf.d/40-libinput-touchpad.conf >/dev/null << 'EOF'
Section "InputClass"
    Identifier "libinput touchpad tap-to-click"
    MatchIsTouchpad "on"
    MatchDevicePath "/dev/input/event*"
    Driver "libinput"
    Option "Tapping" "on"
    Option "TappingDrag" "on"
    Option "NaturalScrolling" "true"
    Option "ClickMethod" "clickfinger"
EndSection
EOF
    add_unique CREATED_FILES "/etc/X11/xorg.conf.d/40-libinput-touchpad.conf"
  fi
fi

# ------------------------------------------------------------------------------
# 14. Write Installer Manifest for Clean Uninstallation
# ------------------------------------------------------------------------------
mkdir -p "$DATA_DIR"
python3 -c "
import json, time, os

def dedupe(lst):
    seen = set()
    res = []
    for x in lst:
        if x and x not in seen:
            seen.add(x)
            res.append(x)
    return res

newly_pkgs = dedupe($(python3 -c "import json, sys; print(json.dumps(sys.argv[1:]))" "${NEWLY_INSTALLED_PKGS[@]:-}"))
pipx_pkgs = dedupe($(python3 -c "import json, sys; print(json.dumps(sys.argv[1:]))" "${PIPX_PACKAGES[@]:-}"))
standalone_bins = dedupe($(python3 -c "import json, sys; print(json.dumps(sys.argv[1:]))" "${STANDALONE_BINS[@]:-}"))
installed_fonts = dedupe($(python3 -c "import json, sys; print(json.dumps(sys.argv[1:]))" "${INSTALLED_FONTS[@]:-}"))
created_files = dedupe($(python3 -c "import json, sys; print(json.dumps(sys.argv[1:]))" "${CREATED_FILES[@]:-}"))

manifest = {
    'version': '1.0',
    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'os_name': '$OS_NAME',
    'os_id': '$OS_ID',
    'package_manager': '$PM',
    'newly_installed_packages': newly_pkgs,
    'pipx_packages': pipx_pkgs,
    'standalone_binaries': standalone_bins,
    'installed_fonts': installed_fonts,
    'created_files': created_files,
    'backup_path': '$BACKUP_PATH',
    'config_dir': '$CONFIG_DIR'
}

with open('$DATA_DIR/install-manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

with open('$CONFIG_DIR/.install-manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
"

# ------------------------------------------------------------------------------
# 15. Ensure PATH in User Shell Profiles (~/.profile and ~/.bashrc)
# ------------------------------------------------------------------------------
echo "Setting up unified binary PATH across user environment..."
QTILE_PATH_LINE='export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$HOME/.config/qtile/scripts:$PATH"'
for pfile in "$HOME/.profile" "$HOME/.bashrc"; do
  if [[ -f "$pfile" ]]; then
    if ! grep -qs 'qtile/scripts' "$pfile"; then
      printf "\n# Qtile-Con unified binary PATH\n%s\n" "$QTILE_PATH_LINE" >> "$pfile"
      echo "  [OK] Added Qtile-Con scripts and ~/.local/bin to $pfile"
    fi
  fi
done
if command -v pipx >/dev/null 2>&1; then
  pipx ensurepath >/dev/null 2>&1 || true
fi

# ------------------------------------------------------------------------------
# 16. Validation & Sanity Check
# ------------------------------------------------------------------------------
echo ""
echo "================================================================="
echo " Validation & Sanity Check"
echo "================================================================="

MISSING_DEPS=0
check_tool() {
  local tool="$1"
  local desc="$2"
  local req="$3"
  if command -v "$tool" >/dev/null 2>&1; then
    printf '  [OK]      %-18s %s\n' "$tool" "$desc"
  else
    printf '  [MISSING] %-18s %s\n' "$tool" "$desc"
    if [[ "$req" == "1" ]]; then MISSING_DEPS=1; fi
  fi
}

check_tool python3 "Python 3 Runtime" 1
check_tool qtile "Qtile Window Manager" 1
check_tool rofi "Application & Command Launcher" 1
check_tool alacritty "Default Terminal Emulator" 1
check_tool feh "Wallpaper Manager" 1
check_tool maim "Screenshot Utility" 1
check_tool xclip "X11 Clipboard" 1
check_tool curl "Weather & Network Fetcher" 0
check_tool jq "JSON Processor" 0
check_tool btop "System & Process Monitor" 0
check_tool htop "Interactive Process Viewer" 0
check_tool witr "Process Causation Tracer" 0
check_tool pamixer "Volume Control Utility" 0
check_tool brightnessctl "Backlight Controller" 0
check_tool dunst "Notification Daemon" 0
check_tool i3lock "Screen Locker" 0

if [[ "$NO_SYSADMIN" -eq 0 ]]; then
  check_tool cockpit-bridge "Cockpit Web Console Bridge" 0
  check_tool snapper "Snapper Btrfs Snapshot Manager" 0
fi

# ------------------------------------------------------------------------------
# 17. SysAdmin Services and Permissions Configuration
# ------------------------------------------------------------------------------
if [[ "$NO_SYSADMIN" -eq 0 ]]; then
  if command -v systemctl >/dev/null 2>&1; then
    if systemctl list-unit-files 2>/dev/null | grep -q "cockpit.socket"; then
      echo "Configuring Cockpit Web Console socket..."
      if [[ $EUID -eq 0 ]]; then
        systemctl enable --now cockpit.socket >/dev/null 2>&1 || true
      elif command -v pkexec >/dev/null 2>&1; then
        pkexec --disable-internal-agent systemctl enable --now cockpit.socket >/dev/null 2>&1 || true
      elif command -v sudo >/dev/null 2>&1; then
        sudo systemctl enable --now cockpit.socket >/dev/null 2>&1 || true
      fi
    fi
  fi

  if command -v snapper >/dev/null 2>&1 && [[ -f /etc/snapper/configs/root ]]; then
    echo "Configuring Snapper user permissions for $USER..."
    if [[ $EUID -eq 0 ]]; then
      snapper -c root set-config "ALLOW_USERS=$USER" "ALLOW_GROUPS=sudo" >/dev/null 2>&1 || true
      chmod a+rx /.snapshots >/dev/null 2>&1 || true
    elif command -v pkexec >/dev/null 2>&1; then
      pkexec --disable-internal-agent bash -c "snapper -c root set-config 'ALLOW_USERS=$USER' 'ALLOW_GROUPS=sudo' && chmod a+rx /.snapshots" >/dev/null 2>&1 || true
    elif command -v sudo >/dev/null 2>&1; then
      sudo bash -c "snapper -c root set-config 'ALLOW_USERS=$USER' 'ALLOW_GROUPS=sudo' && chmod a+rx /.snapshots" >/dev/null 2>&1 || true
    fi
  fi
fi

if command -v qtile >/dev/null 2>&1; then
  echo ""
  echo "Validating Qtile configuration syntax..."
  if "$CONFIG_DIR/scripts/check-config" >/dev/null 2>&1; then
    echo "[OK] Qtile configuration is valid and ready to load."
  else
    echo "[WARNING] 'qtile check' reported warnings or syntax notices."
  fi
fi

echo ""
echo "================================================================="
echo " Installation Complete!"
echo "================================================================="
echo "Quick Start:"
echo "  1. Log out of your current session."
echo "  2. Select 'Qtile' from your display manager session menu."
echo "  3. Log in and enjoy your cohesive desktop!"
echo ""
echo "Key Shortcuts to Get Started:"
echo "  • Super + /         : Interactive Keybindings Cheatsheet"
echo "  • Super + d         : Application Launcher (All / Apps / Run)"
echo "  • Super + r         : Run Command / CLI Binary Launcher"
echo "  • Super + Return    : Terminal (Alacritty)"
echo "  • Super + Shift + t : Global Theme Switcher"
echo "  • Super + Shift + e : Power & Logout Menu"
echo ""
echo "To completely uninstall later:"
echo "  ./uninstall.sh --purge"
echo "================================================================="
