"""Keyboard shortcuts and interactive desktop actions."""
from libqtile.config import Key
from libqtile.lazy import lazy
from config.settings import MOD, TERMINAL, SCRIPTS, LAUNCHER
from config.groups import groups

keys = [
    Key([MOD], "Return", lazy.spawn(TERMINAL)),
    Key([MOD], "d", lazy.spawn(LAUNCHER)),
    Key([MOD], "Tab", lazy.next_layout()),
    Key([MOD, "shift"], "space", lazy.spawn(f"{SCRIPTS}/qtile-action layout")),
    Key([MOD, "shift"], "w", lazy.spawn(f"{SCRIPTS}/set-wallpaper")),
    Key([MOD, "shift"], "t", lazy.spawn(f"{SCRIPTS}/set-theme")),
    Key([MOD], "v", lazy.spawn(f"{SCRIPTS}/qtile-action clipboard")),
    Key([], "Print", lazy.spawn(f"{SCRIPTS}/screenshot region")),
    Key([MOD], "Print", lazy.spawn(f"{SCRIPTS}/screenshot full")),
    Key([MOD, "ctrl"], "r", lazy.restart()),
    Key([MOD, "shift"], "q", lazy.window.kill()),
    Key([MOD, "shift"], "e", lazy.spawn("lxsession-logout")),
    Key([MOD], "Escape", lazy.spawn("i3lock")),
    Key([MOD], "Left", lazy.layout.left()),
    Key([MOD], "Right", lazy.layout.right()),
    Key([MOD], "Down", lazy.layout.down()),
    Key([MOD], "Up", lazy.layout.up()),
    Key([MOD, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([MOD, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([MOD], "f", lazy.window.toggle_fullscreen()),
    Key([MOD], "space", lazy.window.toggle_floating()),
    Key([MOD], "comma", lazy.spawn("pamixer --decrease 5")),
    Key([MOD], "period", lazy.spawn("pamixer --increase 5")),
    Key([MOD], "m", lazy.spawn("pamixer --toggle-mute")),
    Key([MOD], "b", lazy.spawn("brightnessctl set 5%-")),
    Key([MOD], "n", lazy.spawn("brightnessctl set +5%")),
]
for group in groups:
    keys.extend([
        Key([MOD], group.name, lazy.group[group.name].toscreen()),
        Key([MOD, "shift"], group.name, lazy.window.togroup(group.name, switch_group=True)),
    ])
