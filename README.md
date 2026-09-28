# Qtile-Con: Material Desktop for Qtile X11

A modular Qtile desktop configuration for **X11**, inspired by Dank Material Shell and Noctalia. It keeps the existing Catppuccin themes, bar, widgets, layouts, workspaces, wallpaper-driven palette generation and desktop actions, using X11-native utilities.

> **Status:** initial X11 refactor. Distribution/package combinations have not all been tested. Run `./install.sh --dry-run` first.

## Features

- Qtile's X11 backend with modular Python configuration.
- Catppuccin Mocha default and Latte, Frappe theme presets.
- Bar with workspaces, focused window, CPU, memory, weather, volume, clock, tray and action icons.
- Rofi launcher and interactive layout, wallpaper, theme and clipboard pickers.
- Wallpaper selection via `feh`; optional `pywal` palette generation updates Qtile colors.
- `maim` screenshots with `xclip` clipboard support.
- Configurable layouts, gaps, borders, keybindings and bar dimensions.
- Installer with OS detection, dependency checks, backup and dry-run; uninstall preserves a backup and does not remove packages.

## Quick start

```sh
git clone https://github.com/Opposum0112/Qtile-con.git
cd Qtile-con
./install.sh --dry-run
./install.sh
```

Log out and choose the **Qtile (X11)** session in your display manager. Ensure your system has an Xorg server and an X11-capable display manager/session. Validate the configuration with:

```sh
qtile check -c ~/.config/qtile/config.py
```

The installer backs up an existing `~/.config/qtile` before copying this configuration. The modular Python package is named `qtile_config` to avoid a Python import collision between `config.py` and a `config/` package. It does not change your display manager or configure Xorg.

## Dependencies

Qtile with its X11 dependencies, Python, Rofi, an X11 terminal (default `xterm`), `feh`, `maim`, `xclip`, `xsel`, `playerctl`, `pamixer`, `brightnessctl`, `curl`, `jq`, `libnotify`, and a Nerd Font. Optional tools include `greenclip` (clipboard history), `btop`, `pavucontrol`, `nm-connection-editor`, `nm-applet`, `i3lock`, `lxsession-logout`, and `pywal`.

The installer offers package installation for Debian/Ubuntu, Fedora, Arch-family, openSUSE and Solus where package names are known. Review the planned package list; package names vary by release.

## Keybindings

| Shortcut | Action |
|---|---|
| Super + Return | Terminal |
| Super + D | Rofi launcher |
| Super + 1…9 | Switch workspace |
| Super + Shift + 1…9 | Move window to workspace |
| Super + Tab | Next layout |
| Super + Shift + Space | Interactive layout picker |
| Super + Shift + W | Wallpaper picker |
| Super + Shift + T | Theme picker |
| Super + V | Clipboard history (optional greenclip) |
| Print | Region screenshot (saved and copied) |
| Super + Print | Full screenshot (saved and copied) |
| Super + Ctrl + R | Restart Qtile |
| Super + Shift + Q | Close focused window |
| Super + Shift + E | Logout menu (optional) |
| Super + comma / period | Volume down / up |
| Super + M | Mute |
| Super + B / N | Brightness down / up |

## Modular structure

```text
config.py
qtile_config/
  settings.py   # user preferences and X11 application defaults
  colors.py     # active palette
  groups.py     # workspaces
  keys.py       # keybindings
  layouts.py    # layouts, gaps, borders
  widgets.py    # bar and interactions
  screens.py    # screen/bar setup
scripts/
  autostart
  qtile-action
  set-wallpaper
  set-theme
  theme_apply.py
  wal_to_qtile.py
  weather
  screenshot
themes/         # Catppuccin JSON presets
docs/
  CONFIGURATION.md
install.sh
uninstall.sh
```

## Theming and wallpaper

Place PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then press Super+Shift+W or click the wallpaper icon. `feh` applies the wallpaper. If `wal` is installed, the selected image can also generate an updated Qtile palette.

## Notes

- This configuration targets **X11 only**. Wayland-only tools such as `fuzzel`, `swww`, `grim`, `slurp`, `wl-clipboard`, and `cliphist` are not used by the X11 scripts.
- Qtile itself supports both X11 and Wayland, but their system dependencies and session launchers differ.
- See [the configuration guide](docs/CONFIGURATION.md) for customization and troubleshooting.
