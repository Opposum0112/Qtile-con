# Configuration guide

- `qtile_config/settings.py`: terminal, launcher, wallpaper directory, gaps, borders and bar dimensions.
- `qtile_config/keys.py`: keyboard shortcuts.
- `qtile_config/groups.py`: workspace labels.
- `qtile_config/layouts.py`: layouts, borders and gaps.
- `qtile_config/widgets.py`: bar widgets and click actions.
- `qtile_config/screens.py`: screen and bar placement.
- `qtile_config/colors.py`: active palette generated from a theme preset.
- `alacritty/alacritty.toml`: starter Alacritty configuration.
- `alacritty/catppuccin-mocha.toml`: matching Catppuccin Mocha terminal palette.

## Prerequisites

This project targets **Qtile on X11/Xorg**, not a Wayland session. Before logging out, confirm that Qtile is installed with its X11 dependencies, an Xorg server is available, and your display manager can launch a Qtile X11 session. Required utilities include Python 3, Rofi, `xterm` (default terminal), `feh`, `maim`, `xclip`, `xsel`, `playerctl`, `curl`, `jq`, desktop notifications and a Nerd Font. Optional integrations include `greenclip`, `btop`, `pavucontrol`, `pamixer`, `brightnessctl`, `nm-applet`, `i3lock`, `pywal`. Audio status supports `pactl`, `wpctl`, or `amixer`; `pavucontrol` and `pamixer` remain optional GUI/keybinding integrations.

The installer can offer packages on Debian/Ubuntu, Fedora, Arch-family, openSUSE and Solus, but it does not install Xorg or configure your display-manager session.

## X11 backend

This project targets Qtile's X11 backend. Use an Xorg session and select **Qtile (X11)** in the display manager. The configuration package is named `qtile_config` (not `config`) to avoid a module-name collision with the `config.py` entry point. The configuration remains modular and preserves the existing workspaces, layouts, Catppuccin themes, bar and keybindings.

The X11 scripts use Rofi for menus, feh for wallpapers, maim for screenshots, xclip for clipboard integration and optional greenclip for clipboard history. Wayland-only tools (Fuzzel, swww, grim, slurp, wl-clipboard and cliphist) are not required.

## Alacritty and bar RAM information\n\nThe `alacritty/` directory contains the Catppuccin Mocha TOML palette and a starter Alacritty config that imports it. The installer places the palette at `~/.config/alacritty/qtile-con-catppuccin-mocha.toml`, creates `alacritty.toml` only when one does not already exist, and preserves existing user configuration. Existing configs can enable the palette with `general.import = ["~/.config/alacritty/qtile-con-catppuccin-mocha.toml"]`. The RAM widget displays used and total memory in MiB plus the percentage.\n\n## Rofi, audio and weather

Rofi menus use `themes/catppuccin-mocha.rasi` for the launcher, power menu and weather-location prompt. The launcher enables desktop icons using the Adwaita icon theme; icon rendering depends on installed desktop icon metadata. Click the weather text in the bar to save a city in `~/.config/qtile/weather-location`; the widget is asked to refresh immediately and also polls every five minutes. Multi-word locations are URL-encoded before being sent to wttr.in. The audio widget polls available PulseAudio/PipeWire/ALSA tools and returns a harmless `VOL N/A` status when no backend is detected.

## Themes and wallpapers

Put PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then use Super+Shift+W. Theme JSON files live in `themes/`. Required palette keys are `base`, `text`, `mauve`, `overlay`, and `surface0`.

## Validation

Run:

```sh
bash ~/.config/qtile/scripts/check-config
# Or:
qtile check -c ~/.config/qtile/config.py
```

If Qtile is installed in a pipx environment, make sure validation tools such as mypy are installed in that same environment. Run `bash scripts/check-config` from the repository (or `~/.config/qtile/scripts/check-config` after installation) to show which Qtile executable is being used and validate the installed entry point.

Package names vary by distribution. Review `./install.sh --dry-run` before installing dependencies. Resolve validation errors before logging out. If the Qtile session is missing from your display manager, configure an Xorg session entry separately.
