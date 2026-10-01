"""Layout collection and consistent Catppuccin borders.

This module configures the window tiling layouts and floating window matching
rules for Qtile, ensuring seamless window management and automatic floating
dialog behavior for graphical authentication agents (Polkit) and system utilities.
"""

# Qtile layout base classes and window matching filters
from libqtile import layout
from libqtile.config import Match

# Palette and dimension settings
from qtile_config.colors import COLORS, ACCENT
from qtile_config.settings import GAP, BORDER_WIDTH
from qtile_config.scroller import Scroller

# ==============================================================================
# TILING LAYOUT DEFINITIONS
# ==============================================================================
layouts = [
    # 1. Scroller Layout: Smooth horizontal scrolling workspace (Niri/PaperWM inspired)
    Scroller(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_focus_stack=COLORS.get("lavender", ACCENT),
        border_normal_stack=COLORS["surface1"],
        border_width=BORDER_WIDTH,
        border_on_single=True,
        margin=GAP,
        default_width=0.5,
        center_focused="on-overflow",
        animate=True,
    ),

    # 2. Columns Layout: Traditional multi-column master-stack tiling
    layout.Columns(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_focus_stack=COLORS.get("lavender", ACCENT),
        border_normal_stack=COLORS["surface1"],
        border_width=BORDER_WIDTH,
        border_on_single=True,
        margin=GAP,
        insert_position=1,
    ),

    # 3. MonadTall Layout: Classic XMonad-style primary master on left, stack on right
    layout.MonadTall(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        margin=GAP,
    ),

    # 4. MonadWide Layout: Master on top, stack on bottom
    layout.MonadWide(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        margin=GAP,
    ),

    # 5. Tile Layout: Standard master and secondary tiled columns
    layout.Tile(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        border_on_single=True,
        margin=GAP,
    ),

    # 6. Matrix Layout: Grid arrangement dividing space equally
    layout.Matrix(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        margin=GAP,
    ),

    # 7. Floating Layout: Free-form non-tiled positioning for all clients
    layout.Floating(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        max_border_width=BORDER_WIDTH,
    ),

    # 8. Max Layout: Fullscreen maximized single client view
    layout.Max(
        border_focus=ACCENT,
        border_normal=COLORS["surface0"],
        border_width=BORDER_WIDTH,
        margin=GAP,
    ),
]

# ==============================================================================
# FLOATING WINDOW RULES & AUTO-CENTERING SPECIFICATION
# ==============================================================================
floating_layout = layout.Floating(
    border_focus=ACCENT,
    border_normal=COLORS["surface0"],
    border_width=BORDER_WIDTH,
    max_border_width=BORDER_WIDTH,
    float_rules=[
        # Default Qtile floating rules (utility, notification, toolbar, splash, dialog)
        *layout.Floating.default_float_rules,

        # PolicyKit graphical authentication agents (must auto-float and center above tiled clients)
        Match(wm_class="lxpolkit"),
        Match(wm_class="Lxpolkit"),
        Match(wm_class="polkit-gnome-authentication-agent-1"),
        Match(wm_class="Polkit-gnome-authentication-agent-1"),
        Match(wm_class="polkit-kde-authentication-agent-1"),
        Match(wm_class="Polkit-kde-authentication-agent-1"),
        Match(wm_class="gpartedbin"),
        Match(wm_class="GParted"),

        # System volume, display and appearance configuration tools
        Match(wm_class="pavucontrol"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="arandr"),
        Match(wm_class="Arandr"),
        Match(wm_class="lxappearance"),
        Match(wm_class="Lxappearance"),
        Match(wm_class="nitrogen"),
        Match(wm_class="Nitrogen"),
        Match(wm_class="blueman-manager"),
        Match(wm_class="nm-connection-editor"),

        # Image viewers and security password prompts
        Match(wm_class="feh"),
        Match(wm_class="pinentry"),
        Match(wm_class="ssh-askpass"),
        Match(title="pinentry"),
    ],
)
