# Configuration guide

- `config/settings.py`: terminal, wallpaper directory, gaps, borders and bar dimensions.
- `config/keys.py`: keyboard shortcuts.
- `config/groups.py`: workspace labels.
- `config/layouts.py`: layouts, borders and gaps.
- `config/widgets.py`: bar widgets and click actions.
- `config/screens.py`: screen and bar placement.
- `config/colors.py`: active palette generated from a theme preset.

Put PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then use Super+Shift+W.
Theme JSON files live in `themes/`. Required palette keys are `base`, `text`, `mauve`, `overlay`, and `surface0`.

The project targets Qtile's Wayland backend. Application names and package availability vary by distribution. Optional widgets should be removed or adjusted if their helper applications are not installed.
