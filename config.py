"""Qtile Main Configuration Entry Point.

This modular configuration architecture decouples Qtile into dedicated modules:
- qtile_config/settings.py: Core paths, font scales, gaps, and environmental variables.
- qtile_config/colors.py: Dynamic palette colors synchronized with global theme.
- qtile_config/keys.py: Keyboard shortcuts, Mac ergonomics, and hardware control bindings.
- qtile_config/groups.py: Workspace definitions and layout group assignments.
- qtile_config/layouts.py: Tiling layouts and floating rules for graphical auth dialogs.
- qtile_config/screens.py: Display screen configurations and status bar instantiation.
- qtile_config/widgets.py: Interactive widgets, background process monitors, and tap handlers.
"""

import json
import os
import subprocess
from libqtile import hook

# Guarantee standard X11 display environment variable
if not os.environ.get("DISPLAY"):
    os.environ["DISPLAY"] = ":0"

# Import modular Qtile configuration components
from qtile_config.groups import groups
from qtile_config.keys import keys
from qtile_config.layouts import layouts, floating_layout
from qtile_config.screens import screens
from qtile_config.settings import MOD, TERMINAL
from qtile_config.widgets import widget_defaults, extension_defaults


@hook.subscribe.startup_once
def autostart():
    """Execute session autostart script on initial desktop login."""
    script = os.path.expanduser("~/.config/qtile/scripts/autostart")
    if os.path.isfile(script):
        subprocess.Popen([script], start_new_session=True)


@hook.subscribe.client_new
def set_floating_dialogs(client):
    """Ensure dialogs and graphical authentication agents float and center properly."""
    # Auto-float standard window dialogs
    if client.window.get_wm_type() == "dialog":
        client.floating = True

    # Auto-float, center, and raise PolicyKit agents and password prompts
    wm_class = client.get_wm_class() or []
    cls_str = " ".join(wm_class).lower()
    if any(k in cls_str for k in ("polkit", "pinentry", "lxpolkit")):
        if hasattr(client, "qtile") and client.qtile and client.qtile.current_group:
            client.togroup(client.qtile.current_group.name)
        client.floating = True
        client.center()
        client.bring_to_front()
        client.focus()
    elif any(k in cls_str for k in ("gparted", "gpartedbin")):
        client.floating = True
        client.center()
        client.bring_to_front()
        if client.group:
            client.group.toscreen()
        client.focus()
    elif any(k in cls_str for k in ("lxappearance", "pavucontrol", "arandr")):
        client.floating = True
        client.center()
        client.bring_to_front()


# ==============================================================================
# INDEPENDENT WORKSPACE LAYOUT PERSISTENCE
# ==============================================================================
WORKSPACE_LAYOUTS_CACHE = os.path.expanduser("~/.cache/qtile/workspace_layouts.json")
_layouts_ready = False


@hook.subscribe.layout_change
def save_workspace_layout(layout, group):
    """Persist each workspace's independent layout choice so changes do not apply to all workspaces and survive reloads."""
    global _layouts_ready
    if not _layouts_ready:
        return
    try:
        if group is None or not hasattr(group, "name"):
            return
        cache_dir = os.path.dirname(WORKSPACE_LAYOUTS_CACHE)
        os.makedirs(cache_dir, exist_ok=True)
        data = {}
        if os.path.exists(WORKSPACE_LAYOUTS_CACHE):
            try:
                with open(WORKSPACE_LAYOUTS_CACHE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        if not isinstance(data, dict):
            data = {}
        data[str(group.name)] = layout.name.lower()
        with open(WORKSPACE_LAYOUTS_CACHE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


@hook.subscribe.startup
def restore_workspace_layouts():
    """Restore each workspace's independent layout choice from persistent cache."""
    global _layouts_ready
    try:
        if os.path.exists(WORKSPACE_LAYOUTS_CACHE):
            with open(WORKSPACE_LAYOUTS_CACHE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                from libqtile import qtile
                if qtile is not None and hasattr(qtile, "groups_map"):
                    for grp_name, layout_name in data.items():
                        if grp_name in qtile.groups_map:
                            grp = qtile.groups_map[grp_name]
                            for idx, l in enumerate(grp.layouts):
                                if l.name.lower() == str(layout_name).lower():
                                    if grp.current_layout != idx:
                                        grp.use_layout(idx)
                                    break
    except Exception:
        pass
    finally:
        _layouts_ready = True


# ==============================================================================
# GENERAL WINDOW MANAGER SETTINGS
# ==============================================================================
# Automatically fullscreen applications requesting fullscreen mode
auto_fullscreen = True

# Focus window on activation: 'smart' focuses when on the current screen
focus_on_window_activation = "smart"

# Window focus follows mouse cursor movement
follow_mouse_focus = True

# Clicking on a floating window brings it to front
bring_front_click = True

# Prevent mouse pointer from jumping across windows on focus change
cursor_warp = False

# Java GUI application compatibility string (fixes blank GUI windows in Java/AWT)
wmname = "LG3D"
