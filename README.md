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

Run validation before logging out. If Qtile was installed with pipx, ensure `~/.local/bin` is on `PATH` and use that same executable for validation.

The installer backs up an existing `~/.config/qtile` before copying this configuration. The modular Python package is named `qtile_config` to avoid a Python import collision between `config.py` and a `config/` package. It does not change your display manager or configure Xorg.

## Prerequisites

### Required

- A supported Linux distribution with an **Xorg/X11 session**. This configuration does not target Wayland.
- Qtile installed with its X11 backend dependencies, plus Python 3.
- An Xorg server and a display manager/session capable of launching Qtile, or a known way to start an Xorg session manually.
- Rofi, an X11 terminal (default `xterm`), `feh`, `maim`, `xclip`, `xsel`, `playerctl`, `curl`, `jq`, and desktop notifications (`libnotify` / `notify-send`; package names vary).
- A Nerd Font for the bar icons.

The installer can attempt to install common dependencies on Debian/Ubuntu, Fedora, Arch-family, openSUSE and Solus. It does **not** install or reconfigure Xorg, your display manager, or the display-manager session entry. Qtile's Python package alone may not be sufficient if system X11 dependencies are missing.

### Optional integrations

- `greenclip`: clipboard history.
- `btop`: system monitor.
- `pavucontrol` and `pamixer`: graphical audio mixer and volume keybindings. The bar detects PulseAudio/PipeWire (`pactl`/`wpctl`) or falls back to ALSA (`amixer`), and displays `VOL N/A` rather than crashing if no backend is available.
- `brightnessctl`: brightness keys.
- `nm-connection-editor` / `nm-applet`: network controls.
- `i3lock`: lock-screen shortcut.
- `i3lock`: optional lock action in the Catppuccin-themed power menu.
- `pywal` (the `wal` command): wallpaper palette generation.
- `gnome-calendar`: calendar shortcut.

Some optional shortcuts do nothing when their application is not installed.

Review planned package operations before installing:

```sh
./install.sh --dry-run
```


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
  set-weather-location
  volume-status
  screenshot
themes/         # Catppuccin JSON presets
docs/
  CONFIGURATION.md
install.sh
uninstall.sh
```

## Rofi theme and weather location

Rofi uses the included Catppuccin Mocha theme for the application launcher, weather-location prompt, and power menu. The weather widget defaults to automatic location detection. Click the weather text in the bar to enter a city (for example, `London, UK`); the choice is saved in `~/.config/qtile/weather-location`. Weather requires a working network connection and `curl`.

## Theming and wallpaper

Place PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then press Super+Shift+W or click the wallpaper icon. `feh` applies the wallpaper. If `wal` is installed, the selected image can also generate an updated Qtile palette.

## Uninstall

```sh
./uninstall.sh --dry-run  # show the target and backup path
./uninstall.sh            # confirm interactively
./uninstall.sh --yes      # skip confirmation
```

The uninstaller moves `~/.config/qtile` to a timestamped backup. It does not remove packages, wallpapers or screenshots. Review the backup before deleting it manually.

## Troubleshooting

- If the configuration does not load, run `bash ~/.config/qtile/scripts/check-config` and inspect the traceback.
- If the Qtile (X11) session is missing, configure an Xorg session entry for your display manager; this repository does not manage that.
- If icons are missing, install and select a Nerd Font, then restart Qtile.
- After changing a theme, press Super+Ctrl+R to reload the palette.

## Notes

- This configuration targets **X11 only**. Wayland-only tools such as `fuzzel`, `swww`, `grim`, `slurp`, `wl-clipboard`, and `cliphist` are not used by the X11 scripts.
- Qtile itself supports both X11 and Wayland, but their system dependencies and session launchers differ.
- See [the configuration guide](docs/CONFIGURATION.md) for customization and troubleshooting.
