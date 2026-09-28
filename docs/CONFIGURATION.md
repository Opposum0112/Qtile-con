# Configuration guide

- `config/settings.py`: terminal, launcher, wallpaper directory, gaps, borders and bar dimensions.
- `config/keys.py`: keyboard shortcuts.
- `config/groups.py`: workspace labels.
- `config/layouts.py`: layouts, borders and gaps.
- `config/widgets.py`: bar widgets and click actions.
- `config/screens.py`: screen and bar placement.
- `config/colors.py`: active palette generated from a theme preset.

## X11 backend

This project targets Qtile's X11 backend. Use an Xorg session and select **Qtile (X11)** in the display manager. The configuration remains modular and preserves the existing workspaces, layouts, Catppuccin themes, bar and keybindings.

The X11 scripts use Rofi for menus, feh for wallpapers, maim for screenshots, xclip for clipboard integration and optional greenclip for clipboard history. Wayland-only tools (Fuzzel, swww, grim, slurp, wl-clipboard and cliphist) are not required.

## Themes and wallpapers

Put PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then use Super+Shift+W. Theme JSON files live in `themes/`. Required palette keys are `base`, `text`, `mauve`, `overlay`, and `surface0`.

## Validation

Run:

```sh
qtile check -c ~/.config/qtile/config.py
```

If Qtile is installed in a pipx environment, make sure validation tools such as mypy are installed in that same environment. The repository's `scripts/check-config` helper reports which executable is being used.

Package names vary by distribution. Review `./install.sh --dry-run` before installing dependencies.
