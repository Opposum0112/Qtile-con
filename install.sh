#!/usr/bin/env bash
set -Eeuo pipefail

# Qtile-Con installer. Installs distro packages individually, then checks tools.
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
    BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx)
    ;;
  debian|ubuntu|linuxmint|pop)
    PM=apt
    BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify-bin)
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx)
    ;;
  fedora|nobara)
    PM=dnf
    BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx)
    ;;
  arch|manjaro|endeavouros|garuda)
    PM=pacman
    BASE_PACKAGES=(python git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python-pipx)
    ;;
  opensuse*|opensuse-tumbleweed|opensuse-leap|suse)
    PM=zypper
    BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify)
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python3-pipx)
    ;;
  *)
    if command -v apt-get >/dev/null 2>&1; then PM=apt
    elif command -v dnf >/dev/null 2>&1; then PM=dnf
    elif command -v pacman >/dev/null 2>&1; then PM=pacman
    elif command -v zypper >/dev/null 2>&1; then PM=zypper
    elif command -v eopkg >/dev/null 2>&1; then PM=eopkg
    fi
    case "$PM" in
      apt) BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify-bin); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx) ;;
      dnf) BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx) ;;
      pacman) BASE_PACKAGES=(python git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python-pipx) ;;
      zypper) BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python3-pipx) ;;
      eopkg) BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww pipx) ;;
    esac
    ;;
esac

echo "Qtile-Con installer"
echo "Detected OS: $OS_NAME (ID=$OS_ID${OS_LIKE:+, ID_LIKE=$OS_LIKE})"
echo "Package manager: ${PM:-not detected}"

if [[ -z "$PM" ]]; then
  echo "Could not detect a supported package manager."
  echo "Install dependencies manually: Python 3, Qtile with Wayland support, fuzzel, foot, grim, slurp, wl-clipboard, playerctl, curl, jq, libnotify; optional tools: cliphist, pamixer, brightnessctl, swww, pipx."
elif [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: would install base packages: ${BASE_PACKAGES[*]}"
  echo "Dry run: would attempt optional packages: ${OPTIONAL_PACKAGES[*]}"
  echo "Dry run: if Qtile is missing and pipx is available, would install qtile[wayland]."
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

  # Qtile is not consistently packaged across distributions. Prefer a distro
  # package if the user installed one; otherwise use pipx to isolate its Python deps.
  export PATH="$HOME/.local/bin:$PATH"
  if ! command -v qtile >/dev/null 2>&1; then
    if command -v pipx >/dev/null 2>&1; then
      echo "Qtile not found; attempting isolated installation of Qtile with Wayland support."
      pipx install 'qtile[wayland]' || echo "WARNING: pipx could not install qtile[wayland]. See Qtile's distro-specific Wayland dependencies." >&2
      export PATH="$HOME/.local/bin:$PATH"
    else
      echo "Qtile not found and pipx is unavailable; install Qtile with Wayland support manually." >&2
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
cp -a "$ROOT/config.py" "$ROOT/config" "$ROOT/scripts" "$ROOT/themes" "$CONFIG/"
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
check_command fuzzel "launcher" required
check_command foot "terminal" required
check_command grim "screenshots" required
check_command slurp "region selection" required
check_command wl-copy "Wayland clipboard" required
check_command wl-paste "Wayland clipboard read" required
check_command playerctl "media controls" optional
check_command curl "weather lookup" optional
check_command jq "JSON utilities" optional
check_command notify-send "desktop notifications" optional
check_command cliphist "clipboard history" optional
check_command pamixer "audio controls" optional
check_command brightnessctl "brightness controls" optional
check_command swww "wallpaper service" optional
check_command pipx "isolated Python installer" optional
check_command qtile "Qtile window manager" required

if command -v qtile >/dev/null 2>&1; then
  echo
  echo "Qtile validation:"
  "$CONFIG/scripts/check-config" || {
    echo "WARNING: 'qtile check' failed. Review the output before using this config." >&2
    MISSING=1
  }
else
  echo
  echo "Qtile is missing. Install it with Wayland support and consult the Qtile documentation"
  echo "for any distribution-specific wlroots/Wayland development libraries."
fi

echo
echo "Configuration installed to $CONFIG"
if (( MISSING != 0 )); then
  echo "One or more required dependencies or validation checks failed. Review the messages above." >&2
  exit 1
fi
