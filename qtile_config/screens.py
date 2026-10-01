"""Screen and bar definitions."""
from libqtile import bar
from libqtile.config import Screen
from qtile_config.colors import BG
from qtile_config.settings import BAR_HEIGHT
from qtile_config.widgets import build_widgets

screens = [Screen(top=bar.Bar(build_widgets(), BAR_HEIGHT, background=BG, margin=[6, 8, 0, 8], opacity=0.97, border_width=0))]
