"""Layout collection and consistent Catppuccin borders."""
from libqtile import layout
from qtile_config.colors import COLORS
from qtile_config.settings import GAP, BORDER_WIDTH

layouts = [
    layout.Columns(border_focus=COLORS["mauve"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH, margin=GAP, insert_position=1),
    layout.MonadTall(border_focus=COLORS["mauve"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH, margin=GAP),
    layout.MonadWide(border_focus=COLORS["blue"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH, margin=GAP),
    layout.Max(),
    layout.Tile(border_focus=COLORS["teal"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH, margin=GAP),
    layout.Matrix(border_focus=COLORS["pink"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH, margin=GAP),
    layout.Floating(),
]
floating_layout = layout.Floating(border_focus=COLORS["mauve"], border_normal=COLORS["surface0"], border_width=BORDER_WIDTH)
