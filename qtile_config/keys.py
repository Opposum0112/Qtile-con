"""Keyboard shortcuts, interactive desktop actions, and Mac hardware ergonomic bindings.

This module defines all keybindings for Qtile, prioritizing Apple Mac ergonomics:
- Command key (Super / mod4) as the primary modifier.
- Mac screenshot ergonomics (Cmd+Shift+3, Cmd+Shift+4, Cmd+Shift+Ctrl+4).
- Dedicated hardware keys and fallbacks for screen and keyboard brightness.
- Direct launch bindings for GUI (Thunar) and asynchronous TUI (Yazi) file managers.
"""

# Qtile configuration objects for binding keyboard combinations to lazy functions
from libqtile.config import Key
from libqtile.lazy import lazy

# Application defaults and modular script paths
from qtile_config.settings import MOD, TERMINAL, SCRIPTS, LAUNCHER
from qtile_config.groups import groups


@lazy.function
def window_to_prev_group(qtile):
    """Move focused window to the previous workspace group and follow it."""
    if qtile.current_window is not None:
        i = qtile.groups.index(qtile.current_group)
        prev_group = qtile.groups[(i - 1) % len(qtile.groups)]
        qtile.current_window.togroup(prev_group.name, switch_group=True)


@lazy.function
def window_to_next_group(qtile):
    """Move focused window to the next workspace group and follow it."""
    if qtile.current_window is not None:
        i = qtile.groups.index(qtile.current_group)
        next_group = qtile.groups[(i + 1) % len(qtile.groups)]
        qtile.current_window.togroup(next_group.name, switch_group=True)


@lazy.function
def restore_minimized_window(qtile):
    """Restore the most recently minimized window on the current group, or any group."""
    minimized_windows = [w for w in qtile.current_group.windows if getattr(w, "minimized", False) is True]
    if not minimized_windows:
        for grp in qtile.groups:
            minimized_windows = [w for w in grp.windows if getattr(w, "minimized", False) is True]
            if minimized_windows:
                break
    if minimized_windows:
        win = minimized_windows[-1]
        win.minimized = False
        if win.group:
            win.group.focus(win, warp=True)
            if win.group != qtile.current_group:
                win.group.toscreen()


@lazy.function
def restore_all_minimized_windows(qtile):
    """Restore all minimized windows on the current group."""
    minimized_windows = [w for w in qtile.current_group.windows if getattr(w, "minimized", False) is True]
    for win in minimized_windows:
        win.minimized = False
    if minimized_windows:
        qtile.current_group.focus(minimized_windows[-1], warp=True)


# ==============================================================================
# KEYBOARD SHORTCUTS SPECIFICATION
# ==============================================================================
keys = [
    # --------------------------------------------------------------------------
    # 1. CORE APPLICATIONS & SYSTEM LAUNCHERS
    # --------------------------------------------------------------------------
    # Spawn terminal emulator (Alacritty)
    Key([MOD], "Return", lazy.spawn(TERMINAL)),

    # Application launcher in Combi mode (GUI apps, CLI run, fuzzy files & content)
    Key([MOD], "d", lazy.spawn(f"{SCRIPTS}/qtile-action launcher")),

    # Dedicated fast command/CLI binary execution launcher
    Key([MOD], "r", lazy.spawn(f"{SCRIPTS}/qtile-action run")),

    # Graphical file manager (Thunar)
    Key([MOD], "e", lazy.spawn("thunar")),

    # Asynchronous Rust terminal file manager (Yazi in terminal)
    Key([MOD, "shift"], "e", lazy.spawn(f"{TERMINAL} -e yazi")),

    # --------------------------------------------------------------------------
    # 2. WINDOW MANAGER LIFECYCLE & MENUS
    # --------------------------------------------------------------------------
    # Restart Qtile in-place without dropping running X11 client windows
    Key([MOD, "control"], "r", lazy.restart()),

    # Close currently focused window gracefully
    Key([MOD, "shift"], "q", lazy.window.kill()),

    # Power & session logout menu (Mod+Ctrl+Q or Mod+Shift+Escape)
    Key([MOD, "control"], "q", lazy.spawn(f"{SCRIPTS}/logout-menu")),
    Key([MOD, "shift"], "Escape", lazy.spawn(f"{SCRIPTS}/logout-menu")),

    # Lock session screen
    Key([MOD], "Escape", lazy.spawn("i3lock")),

    # --------------------------------------------------------------------------
    # 3. LAYOUT SELECTION & NAVIGATION
    # --------------------------------------------------------------------------
    # Cycle forward and backward through layouts
    Key([MOD], "Tab", lazy.next_layout()),
    Key([MOD, "shift"], "Tab", lazy.prev_layout()),

    # Interactive layout picker popup menu
    Key([MOD, "shift"], "space", lazy.spawn(f"{SCRIPTS}/qtile-action layout")),

    # --------------------------------------------------------------------------
    # 4. THEMING & APPEARANCE
    # --------------------------------------------------------------------------
    # Interactive wallpaper selector grid with live image thumbnails
    Key([MOD, "shift"], "w", lazy.spawn(f"{SCRIPTS}/set-wallpaper")),

    # Global color theme selector (Catppuccin, Gruvbox, GitHub, Ayu, Solarized)
    Key([MOD, "shift"], "t", lazy.spawn(f"{SCRIPTS}/set-theme")),

    # --------------------------------------------------------------------------
    # 5. PRODUCTIVITY TOOLS, CLIPBOARD & REFERENCE
    # --------------------------------------------------------------------------
    # Clipboard history manager
    Key([MOD], "v", lazy.spawn(f"{SCRIPTS}/qtile-action clipboard")),

    # Interactive volume slider popup
    Key([MOD, "shift"], "v", lazy.spawn(f"{SCRIPTS}/qtile-action slider")),

    # Formatted keybinding cheatsheet & environment reference palette
    Key([MOD], "slash", lazy.spawn(f"{SCRIPTS}/qtile-action cheatsheet")),
    Key([MOD, "shift"], "slash", lazy.spawn(f"{SCRIPTS}/qtile-action cheatsheet")),
    Key([MOD], "s", lazy.spawn(f"{SCRIPTS}/qtile-action cheatsheet")),

    # Environment configuration files location browser
    Key([MOD, "control"], "slash", lazy.spawn(f"{SCRIPTS}/qtile-action configs")),

    # System manual pages and documentation lookup
    Key([MOD, "shift"], "m", lazy.spawn(f"{SCRIPTS}/qtile-action man")),

    # --------------------------------------------------------------------------
    # 6. MAC ERGONOMIC SCREENSHOT SHORTCUTS (No physical PrintScreen key)
    # --------------------------------------------------------------------------
    # Cmd + Shift + 3: Capture full screen
    Key([MOD, "shift"], "3", lazy.spawn(f"{SCRIPTS}/screenshot full")),

    # Cmd + Shift + 4: Interactively select region/window to file
    Key([MOD, "shift"], "4", lazy.spawn(f"{SCRIPTS}/screenshot region")),

    # Cmd + Shift + Ctrl + 4: Interactively select region directly to clipboard
    Key([MOD, "shift", "control"], "4", lazy.spawn(f"{SCRIPTS}/screenshot clipboard")),

    # --------------------------------------------------------------------------
    # 7. HARDWARE CONTROLS (BRIGHTNESS, KEYBOARD BACKLIGHT, AUDIO)
    # --------------------------------------------------------------------------
    # Screen brightness via XF86 hardware keys and Mac F1/F2 ergonomics
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([MOD], "F2", lazy.spawn("brightnessctl set +5%")),
    Key([MOD], "F1", lazy.spawn("brightnessctl set 5%-")),
    Key([MOD], "n", lazy.spawn("brightnessctl set +5%")),
    Key([MOD], "b", lazy.spawn("brightnessctl set 5%-")),

    # Keyboard backlight via XF86 hardware keys and Mac F5/F6 ergonomics
    Key([], "XF86KbdBrightnessUp", lazy.spawn("brightnessctl --device='*kbd*' set +10%")),
    Key([], "XF86KbdBrightnessDown", lazy.spawn("brightnessctl --device='*kbd*' set 10%-")),
    Key([MOD], "F6", lazy.spawn("brightnessctl --device='*kbd*' set +10%")),
    Key([MOD], "F5", lazy.spawn("brightnessctl --device='*kbd*' set 10%-")),

    # Audio volume control (dedicated XF86 keys and ergonomic fallbacks)
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
    Key([MOD], "period", lazy.spawn("pamixer --increase 5")),
    Key([MOD], "comma", lazy.spawn("pamixer --decrease 5")),
    Key([MOD], "m", lazy.spawn("pamixer --toggle-mute")),

    # --------------------------------------------------------------------------
    # 8. WINDOW NAVIGATION & FOCUS
    # --------------------------------------------------------------------------
    Key([MOD], "Left", lazy.layout.left()),
    Key([MOD], "Right", lazy.layout.right()),
    Key([MOD], "Down", lazy.layout.down()),
    Key([MOD], "Up", lazy.layout.up()),

    # Window shuffling / moving within layout
    Key([MOD, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([MOD, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([MOD, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([MOD, "shift"], "Up", lazy.layout.shuffle_up()),

    # --------------------------------------------------------------------------
    # 9. SCROLLER LAYOUT COLUMN RESIZING & CENTERING
    # --------------------------------------------------------------------------
    Key([MOD], "equal", lazy.layout.grow_width()),
    Key([MOD], "minus", lazy.layout.shrink_width()),
    Key([MOD], "w", lazy.layout.cycle_width()),
    Key([MOD], "c", lazy.layout.center()),
    Key([MOD, "control"], "s", lazy.layout.toggle_split()),
    Key([MOD, "control"], "e", lazy.layout.expel()),
    Key([MOD, "control"], "bracketleft", lazy.layout.consume_left()),
    Key([MOD, "control"], "bracketright", lazy.layout.consume_right()),

    # --------------------------------------------------------------------------
    # 10. WINDOW STATES: FULLSCREEN, FLOATING, MAXIMIZE, MINIMIZE, RESTORE
    # --------------------------------------------------------------------------
    Key([MOD], "f", lazy.window.toggle_fullscreen()),
    Key([MOD], "space", lazy.window.toggle_floating()),
    Key([MOD, "shift"], "f", lazy.window.toggle_maximize()),
    Key([MOD], "x", lazy.window.toggle_maximize()),
    Key([MOD], "i", lazy.window.toggle_minimize()),
    Key([MOD, "shift"], "minus", lazy.window.toggle_minimize()),
    Key([MOD], "u", restore_minimized_window),
    Key([MOD, "shift"], "u", restore_all_minimized_windows),
    Key([MOD, "control"], "u", lazy.spawn(f"{SCRIPTS}/qtile-action restore")),

    # --------------------------------------------------------------------------
    # 11. WORKSPACE / GROUP SWITCHING
    # --------------------------------------------------------------------------
    Key([MOD], "bracketleft", lazy.screen.prev_group()),
    Key([MOD], "bracketright", lazy.screen.next_group()),
    Key([MOD, "shift"], "bracketleft", window_to_prev_group),
    Key([MOD, "shift"], "bracketright", window_to_next_group),
    Key([MOD, "control"], "Left", window_to_prev_group),
    Key([MOD, "control"], "Right", window_to_next_group),

    # --------------------------------------------------------------------------
    # 12. TRACKPAD GESTURE SHORTCUT TARGETS (libinput-gestures)
    # --------------------------------------------------------------------------
    Key([MOD, "mod1"], "Left", lazy.screen.prev_group()),
    Key([MOD, "mod1"], "Right", lazy.screen.next_group()),
    Key([MOD, "mod1", "shift"], "Left", window_to_prev_group),
    Key([MOD, "mod1", "shift"], "Right", window_to_next_group),
    Key([MOD, "mod1"], "Up", lazy.next_layout()),
    Key([MOD, "mod1"], "Down", lazy.prev_layout()),
    Key([MOD, "mod1"], "Return", lazy.spawn(LAUNCHER)),
    Key([MOD, "mod1", "shift"], "Return", lazy.spawn(TERMINAL)),
    Key([MOD, "mod1"], "f", lazy.window.toggle_fullscreen()),
    Key([MOD, "mod1"], "space", lazy.window.toggle_floating()),
]

# ------------------------------------------------------------------------------
# 13. WORKSPACE TAG KEYS (Command + [1..9] to view, Command + Control + [1..9] to move)
# ------------------------------------------------------------------------------
for group in groups:
    keys.extend([
        # Switch to workspace tag (Command + 1..9)
        Key([MOD], group.name, lazy.group[group.name].toscreen()),
        # Move focused window to workspace tag and follow focus (Command + Control + 1..9)
        Key([MOD, "control"], group.name, lazy.window.togroup(group.name, switch_group=True)),
    ])

