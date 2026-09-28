"""Central settings; adjust these values to personalize the X11 desktop."""
import os

MOD = "mod4"
TERMINAL = os.environ.get("QTILE_TERMINAL", "xterm")
LAUNCHER = os.environ.get("QTILE_LAUNCHER", "rofi -show drun")
WALLPAPER_DIR = os.path.expanduser(os.environ.get("QTILE_WALLPAPER_DIR", "~/Pictures/Wallpapers"))
GAP = 8
BORDER_WIDTH = 2
BAR_HEIGHT = 36
FONT = "JetBrainsMono Nerd Font"
FONT_SIZE = 12
THEME_FILE = os.path.expanduser("~/.config/qtile/qtile_config/colors.py")
SCRIPTS = os.path.expanduser("~/.config/qtile/scripts")
