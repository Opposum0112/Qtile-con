#!/usr/bin/env bash
set -Eeuo pipefail

# Qtile-Con X11 installer.
DRY_RUN=0
ASSUME_YES=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] [--yes]"
      echo "  --dry-run  Show detected OS and planned actions without changing anything"
      echo "  --yes      Do not prompt before installing system packages"
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$HOME/.config/qtile"
OS_ID=unknown
OS_LIKE=""
OS_NAME="Unknown Linux"
if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  OS_ID="${ID:-unknown}"
  OS_LIKE="${ID_LIKE:-}"
  OS_NAME="${PRETTY_NAME:-$OS_ID}"
fi

PM=""
BASE_PACKAGES=()
OPTIONAL_PACKAGES=()
case "$OS_ID" in
  solus)
    PM=eopkg
    BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol nm-connection-editor network-manager-applet i3lock lxsession pywal pipx)
    ;;
  debian|ubuntu|linuxmint|pop)
    PM=apt
    BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify-bin)
    OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol network-manager-gnome i3lock lxsession pywal pipx)
    ;;
  fedora|nobara)
    PM=dnf
    BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol NetworkManager-gnome i3lock lxsession pywal pipx)
    ;;
  arch|manjaro|endeavouros|garuda)
    PM=pacman
    BASE_PACKAGES=(python git rofi xterm feh maim xclip xsel playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol nm-connection-editor network-manager-applet i3lock lxsession python-pywal python-pipx)
    ;;
  opensuse*|opensuse-tumbleweed|opensuse-leap|suse)
    PM=zypper
    BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify-tools)
    OPTIONAL_PACKAGES=(pamixer brightnessctl btop pavucontrol NetworkManager-applet i3lock lxsession pywal python3-pipx)
    ;;
  *)
    if command -v apt-get >/dev/null 2>&1; then PM=apt
    elif command -v dnf >/dev/null 2>&1; then PM=dnf
    elif command -v pacman >/dev/null 2>&1; then PM=pacman
    elif command -v zypper >/dev/null 2>&1; then PM=zypper
    elif command -v eopkg >/dev/null 2>&1; then PM=eopkg
    fi
    case "$PM" in
      apt) BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify-bin); OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol network-manager-gnome i3lock lxsession pywal pipx) ;;
      dnf) BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify); OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol NetworkManager-gnome i3lock lxsession pywal pipx) ;;
      pacman) BASE_PACKAGES=(python git rofi xterm feh maim xclip xsel playerctl curl jq libnotify); OPTIONAL_PACKAGES=(greenclip pamixer brightnessctl btop pavucontrol nm-connection-editor network-manager-applet i3lock lxsession python-pywal python-pipx) ;;
      zypper) BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify-tools); OPTIONAL_PACKAGES=(pamixer brightnessctl btop pavucontrol NetworkManager-applet i3lock lxsession pywal python3-pipx) ;;
      eopkg) BASE_PACKAGES=(python3 git rofi xterm feh maim xclip xsel playerctl curl jq libnotify); OPTIONAL_PACKAGES=(pamixer brightnessctl btop pavucontrol nm-connection-editor network-manager-applet i3lock lxsession pywal pipx) ;;
    esac
    ;;
esac

echo "Qtile-Con X11 installer"
echo "Detected OS: $OS_NAME (ID=$OS_ID${OS_LIKE:+, ID_LIKE=$OS_LIKE})"
echo "Package manager: ${PM:-not detected}"
if [[ -z "$PM" ]]; then
  echo "Could not detect a supported package manager."
  echo "Install manually: Python 3, Qtile with X11 dependencies, rofi, xterm, feh, maim, xclip, xsel, playerctl, curl, jq and libnotify."
elif [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: would install base packages: ${BASE_PACKAGES[*]}"
  echo "Dry run: would attempt optional packages: ${OPTIONAL_PACKAGES[*]}"
  echo "Dry run: if Qtile is missing and pipx is available, would install qtile."
else
  if [[ "$ASSUME_YES" != 1 ]]; then
    read -r -p "Install dependencies using $PM? [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]] || { echo "Dependency installation skipped."; PM=""; }
  fi
  if [[ -n "$PM" ]]; then
    case "$PM" in
      apt) sudo apt-get update || echo "WARNING: apt metadata refresh failed." >&2 ;;
      dnf) sudo dnf makecache || echo "WARNING: dnf metadata refresh failed." >&2 ;;
      pacman) sudo pacman -Sy --noconfirm || echo "WARNING: pacman database refresh failed." >&2 ;;
      zypper) sudo zypper refresh || echo "WARNING: zypper refresh failed." >&2 ;;
      eopkg) sudo eopkg update-repo || echo "WARNING: eopkg repository refresh failed." >&2 ;;
    esac

    install_one() {
      local package="$1" required="$2" rc=0
      echo "Installing package: $package"
      case "$PM" in
        apt) sudo apt-get install -y "$package" || rc=$? ;;
        dnf) sudo dnf install -y "$package" || rc=$? ;;
        pacman) sudo pacman -S --needed --noconfirm "$package" || rc=$? ;;
        zypper) sudo zypper --non-interactive install "$package" || rc=$? ;;
        eopkg) sudo eopkg install -y "$package" || rc=$? ;;
      esac
      if (( rc != 0 )); then
        if [[ "$required" == required ]]; then
          echo "WARNING: required package '$package' could not be installed." >&2
        else
          echo "Optional package '$package' unavailable or failed; continuing." >&2
        fi
        return "$rc"
      fi
    }

    for package in "${BASE_PACKAGES[@]}"; do install_one "$package" required || true; done
    for package in "${OPTIONAL_PACKAGES[@]}"; do install_one "$package" optional || true; done
  fi

  export PATH="$HOME/.local/bin:$PATH"
  if ! command -v qtile >/dev/null 2>&1; then
    if command -v pipx >/dev/null 2>&1; then
      echo "Qtile not found; attempting isolated installation. Ensure the system's X11 development dependencies are installed."
      pipx install qtile || echo "WARNING: pipx could not install Qtile. Install it using your distribution package or Qtile's X11 dependency instructions." >&2
      export PATH="$HOME/.local/bin:$PATH"
    else
      echo "Qtile not found and pipx is unavailable; install Qtile with X11 support manually." >&2
    fi
  fi
fi

if [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: would back up $CONFIG and install configuration files."
  exit 0
fi

if [[ -e "$CONFIG" ]]; then
  backup="${CONFIG}.backup.$(date +%Y%m%d-%H%M%S)"
  mv "$CONFIG" "$backup"
  echo "Existing configuration backed up to: $backup"
fi
mkdir -p "$CONFIG"
cp -a "$ROOT/config.py" "$ROOT/qtile_config" "$ROOT/scripts" "$ROOT/themes" "$CONFIG/"
chmod +x "$CONFIG"/scripts/*

export PATH="$HOME/.local/bin:$PATH"
echo
echo "Dependency check:"
MISSING=0
check_command() {
  local command_name="$1" description="$2" required="$3"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf '  OK      %-16s %s\n' "$command_name" "$description"
  else
    printf '  MISSING %-16s %s\n' "$command_name" "$description"
    if [[ "$required" == required ]]; then MISSING=1; fi
  fi
}
check_command python3 "Python runtime" required
check_command git "Git" required
check_command rofi "launcher" required
check_command xterm "terminal (default)" required
check_command feh "wallpaper utility" required
check_command maim "screenshots" required
check_command xclip "X11 clipboard" required
check_command xsel "X11 selection utility" optional
check_command playerctl "media controls" optional
check_command curl "weather lookup" optional
check_command jq "JSON utilities" optional
check_command notify-send "desktop notifications" optional
check_command greenclip "clipboard history" optional
check_command pamixer "audio controls" optional
check_command brightnessctl "brightness controls" optional
check_command pipx "isolated Python installer" optional
check_command qtile "Qtile window manager" required

if command -v qtile >/dev/null 2>&1; then
  echo
  echo "Qtile validation:"
  qtile check -c "$CONFIG/config.py" || {
    echo "WARNING: 'qtile check' failed. Review the output before using this config." >&2
    MISSING=1
  }
else
  echo
  echo "Qtile is missing. Install Qtile with its X11 dependencies before starting the session."
fi

echo
echo "Configuration installed to $CONFIG"
echo "Select the Qtile X11 session in your display manager. This installer does not install or reconfigure Xorg or your display manager."
if (( MISSING != 0 )); then
  echo "One or more required dependencies or validation checks failed. Review the messages above." >&2
  exit 1
fi
