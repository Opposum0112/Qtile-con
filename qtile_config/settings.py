"""Qtile Global Settings, PATH Environment, and Desktop Dimensions.

This module initializes the core environmental variables and layout parameters:
- Unified binary search PATH covering Cargo, Homebrew, Pipx, Go, Flatpak, and scripts.
- Default key modifiers (mod4 for Command/Super on Apple Mac keyboards).
- Default terminal, Rofi launcher modes (Combi, Apps, Run, File, Content), and fonts.
- Window gaps, border dimensions, and status bar geometry.
"""

import os


def get_unified_path() -> str:
    """Construct an enriched search PATH with Cargo, Homebrew, Pipx, Go, Flatpak, Snap, and local scripts."""
    home = os.path.expanduser("~")
    custom_dirs = [
        os.path.join(home, ".cargo", "bin"),
        "/home/linuxbrew/.linuxbrew/bin",
        "/home/linuxbrew/.linuxbrew/sbin",
        os.path.join(home, ".linuxbrew", "bin"),
        os.path.join(home, ".linuxbrew", "sbin"),
        os.path.join(home, ".local", "bin"),
        os.path.join(home, ".local", "share", "pipx", "venvs", "qtile", "bin"),
        os.path.join(home, "go", "bin"),
        "/usr/local/go/bin",
        "/snap/bin",
        "/var/lib/flatpak/exports/bin",
        os.path.join(home, ".local", "share", "flatpak", "exports", "bin"),
        os.path.join(home, ".config", "qtile", "scripts"),
        os.path.join(home, "scripts"),
    ]
    pipx_venvs = os.path.join(home, ".local", "share", "pipx", "venvs")
    if os.path.isdir(pipx_venvs):
        for entry in os.listdir(pipx_venvs):
            vbin = os.path.join(pipx_venvs, entry, "bin")
            if os.path.isdir(vbin) and vbin not in custom_dirs:
                custom_dirs.append(vbin)

    system_defaults = [
        "/usr/local/bin",
        "/usr/bin",
        "/bin",
        "/usr/local/sbin",
        "/usr/sbin",
        "/sbin",
    ]
    current_dirs = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]

    unified: list[str] = []
    for d in custom_dirs + current_dirs + system_defaults:
        if d not in unified:
            unified.append(d)
    return os.pathsep.join(unified)


# Export enriched PATH so all child processes and Rofi find all user/system binaries
os.environ["PATH"] = get_unified_path()

# Guarantee DISPLAY is always set in environment so GUI and Rofi dialogs never abort
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"

# Modifier key: mod4 corresponds to the Command (Super) key on Apple Mac keyboards
MOD = "mod4"

# Default terminal emulator (Alacritty GPU terminal)
TERMINAL = os.environ.get("QTILE_TERMINAL", "alacritty")

# Rofi launcher theme and backend script locations
ROFI_THEME = os.path.expanduser("~/.config/qtile/themes/catppuccin-mocha.rasi")
ROFI_RUN_BIN = os.path.expanduser("~/.config/qtile/scripts/qtile-run")
ROFI_FILES_BIN = os.path.expanduser("~/.config/qtile/scripts/rofi-file-search")
ROFI_CONTENT_BIN = os.path.expanduser("~/.config/qtile/scripts/rofi-content-search")

# Unified application launcher command string
LAUNCHER = os.environ.get(
    "QTILE_LAUNCHER",
    f"rofi -show combi -modes combi,drun,run,file:{ROFI_FILES_BIN},content:{ROFI_CONTENT_BIN} -combi-modes drun,run -combi-hide-mode-prefix -run-command '{ROFI_RUN_BIN} {{cmd}}' -run-shell-command '{ROFI_RUN_BIN} {{cmd}}' -show-icons -icon-theme Adwaita -terminal {TERMINAL} -theme {ROFI_THEME}",
)

# Wallpaper collection directory
WALLPAPER_DIR = os.path.expanduser(os.environ.get("QTILE_WALLPAPER_DIR", "~/Pictures/Wallpapers"))

# Window layout spacing and border geometry
GAP = 4
BORDER_WIDTH = 2
BAR_HEIGHT = 36

# Typography configuration
FONT = "JetBrainsMono Nerd Font"
FONT_SIZE = 12

# Internal path references
THEME_FILE = os.path.expanduser("~/.config/qtile/qtile_config/colors.py")
SCRIPTS = os.path.expanduser("~/.config/qtile/scripts")
