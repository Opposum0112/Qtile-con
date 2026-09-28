#!/usr/bin/env bash
set -Eeuo pipefail

# Qtile-Con installer. Package installation is best-effort per package so one
# unavailable optional package does not prevent the rest of the setup.
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
    OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python3-pip)
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
    # Fall back to a recognizable package manager for derivatives or custom systems.
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
      eopkg) BASE_PACKAGES=(python3 git fuzzel foot grim slurp wl-clipboard playerctl curl jq libnotify); OPTIONAL_PACKAGES=(cliphist pamixer brightnessctl swww python3-pip) ;;
    esac
    ;;
esac

echo "Qtile-Con installer"
echo "Detected OS: $OS_NAME (ID=$OS_ID${OS_LIKE:+, ID_LIKE=$OS_LIKE})"
echo "Package manager: ${PM:-not detected}"

if [[ -z "$PM" ]]; then
  echo "Could not detect a supported package manager."
  echo "Install dependencies manually: Python 3, Qtile with Wayland support, fuzzel, foot, grim, slurp, wl-clipboard, playerctl, curl, jq, libnotify, and optionally cliphist, pamixer, brightnessctl, swww."
elif [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: would install base packages: ${BASE_PACKAGES[*]}"
  echo "Dry run: would attempt optional packages: ${OPTIONAL_PACKAGES[*]}"
else
  if [[ "$ASSUME_YES" != 1 ]]; then
    read -r -p "Install dependencies using $PM? [y/N] " answer
    [[ "$answer" =~ ^[Yy]$ ]] || { echo "Dependency installation skipped."; PM=""; }
  fi
  if [[ -n "$PM" ]]; then
    case "$PM" in
      apt) sudo apt-get update ;;
      dnf) sudo dnf makecache ;;
      pacman) sudo pacman -Sy --noconfirm ;;
      zypper) sudo zypper refresh ;;
      eopkg) sudo eopkg update-repo ;;
    esac

    install_one() {
      local package="$1" required="$2"
      echo "Installing $package..."
      case "$PM" in
        apt) sudo apt-get install -y "$package" ;;
        dnf) sudo dnf install -y "$package" ;;
        pacman) sudo pacman -S --needed --noconfirm "$package" ;;
        zypper) sudo zypper --non-interactive install "$package" ;;
        eopkg) sudo eopkg install -y "$package" ;;
      esac
      local rc=$?
      if (( rc != 0 )); then
        if [[ "$required" == required ]]; then
          echo "WARNING: required package '$package' could not be installed." >&2
        else
          echo "Optional package '$package' unavailable or failed to install; continuing." >&2
        fi
        return 1
      fi
    }

    for package in "${BASE_PACKAGES[@]}"; do install_one "$package" required || true; done
    for package in "${OPTIONAL_PACKAGES[@]}"; do install_one "$package" optional || true; done
  fi
fi

if [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: would back up $CONFIG and install configuration files."
  exit 0
fi

# Install configuration even if a package was unavailable; report missing tools below.
if [[ -e "$CONFIG" ]]; then
  backup="${CONFIG}.backup.$(date +%Y%m%d-%H%M%S)"
  mv "$CONFIG" "$backup"
  echo "Existing configuration backed up to: $backup"
fi
mkdir -p "$CONFIG"
cp -a "$ROOT/config.py" "$ROOT/config" "$ROOT/scripts" "$ROOT/themes" "$CONFIG/"
chmod +x "$CONFIG"/scripts/*

echo
echo "Dependency check (commands not found are listed as missing):"
MISSING=0
check_command() {
  local command_name="$1" description="$2" required="$3"
  if command -v "$command_name" >/dev/null 2>&1; then
    printf '  OK      %-16s %s\n' "$command_name" "$description"
  else
    printf '  MISSING %-16s %s\n' "$command_name" "$description"
    [[ "$required" == required ]] && MISSING=1
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
check_command swww "animated wallpaper service" optional
check_command qtile "Qtile compositor/window manager" required

if ! command -v qtile >/dev/null 2>&1; then
  echo
  echo "Qtile was not found. Install Qtile with Wayland support using your distro package"
  echo "if available, or install it in an isolated Python environment (for example, pipx)."
  echo "Qtile's Wayland backend may need additional system libraries; consult the Qtile"
  echo "installation documentation for your distribution."
fi

echo
echo "Configuration installed to $CONFIG"
echo "Validate when Qtile is installed with Wayland support:"
echo "  qtile check -c ~/.config/qtile/config.py"
if (( MISSING != 0 )); then
  echo "One or more required commands are missing. Review the messages above." >&2
  exit 1
fi
