"""Qtile entry point. Keep this file intentionally small and modular."""
from libqtile import hook
from config.groups import groups
from config.keys import keys
from config.layouts import layouts, floating_layout
from config.screens import screens
from config.settings import MOD, TERMINAL

@hook.subscribe.startup_once
def autostart():
    import os
    import subprocess
    script = os.path.expanduser("~/.config/qtile/scripts/autostart")
    if os.path.isfile(script):
        subprocess.Popen([script], start_new_session=True)

@hook.subscribe.client_new
def set_floating_dialogs(client):
    if client.window.get_wm_type() == "dialog":
        client.floating = True

# Qtile configuration
auto_fullscreen = True
focus_on_window_activation = "smart"
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
wmname = "LG3D"
