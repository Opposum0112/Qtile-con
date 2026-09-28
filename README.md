# Qtile-Con: Material Desktop for Qtile Wayland

A modular Qtile Wayland desktop configuration inspired by Dank Material Shell and Noctalia, with Catppuccin colors, an interactive bar, launcher, widgets, wallpaper-driven palette generation, and quick desktop actions.

> **Status:** initial configuration. Distribution/package combinations have not all been tested. Review scripts and run the installer with `--dry-run` first.

## Features

- Qtile's Wayland backend with modular Python configuration.
- Catppuccin Mocha default and Latte, Frappe, Macchiato theme presets.
- Bar with workspaces, focused window, CPU, memory, weather, volume, clock, tray and action icons.
- Fuzzel launcher and interactive layout, wallpaper, theme and clipboard pickers.
- Wallpaper selection via `swww`; optional pywal palette generation updates Qtile colors.
- grim/slurp screenshots copied to clipboard, wl-clipboard and cliphist integration.
- Configurable layouts, gaps, borders, keybindings and bar dimensions.
- Installer with backup and dry-run; uninstall preserves a backup and does not remove packages.

## Quick start

```sh
git clone https://github.com/Opposum0112/Qtile-con.git
cd Qtile-con
./install.sh --dry-run
./install.sh
```

Put wallpapers in `~/Pictures/Wallpapers`, then log out and choose the Qtile Wayland session. Ensure Qtile is installed with its Wayland backend and native dependencies. Validate the configuration with:

```sh
qtile check -c ~/.config/qtile/config.py
```

The installer backs up an existing `~/.config/qtile` before copying this configuration. It does not change your display manager or install Qtile itself.

## Dependencies

Install Qtile with Wayland support, Python, fuzzel, foot (or change `config/settings.py`), swww or swaybg, grim, slurp, wl-clipboard, cliphist, playerctl, pamixer, brightnessctl, curl, jq, libnotify, a Nerd Font, and optionally btop, pavucontrol, nm-connection-editor, nm-applet, swaylock, wlogout and pywal.

The installer offers package installation for Debian/Ubuntu, Fedora, Arch and openSUSE. Package names vary by release; review the list and install missing packages manually. Qtile's Wayland backend requires additional system libraries depending on your distribution.

## Keybindings

| Shortcut | Action |
|---|---|
| Super + Return | Terminal |
| Super + D | Fuzzel launcher |
| Super + 1…9 | Switch workspace |
| Super + Shift + 1…9 | Move window to workspace |
| Super + Tab | Next layout |
| Super + Shift + Space | Interactive layout picker |
| Super + Shift + W | Wallpaper picker |
| Super + Shift + T | Theme picker |
| Super + V | Clipboard history |
| Print | Region screenshot (saved and copied) |
| Super + Print | Full screenshot (saved and copied) |
| Super + Ctrl + R | Restart Qtile |
| Super + Shift + Q | Close focused window |
| Super + Shift + E | wlogout (optional) |
| Super + comma / period | Volume down / up |
| Super + M | Mute |
| Super + B / N | Brightness down / up |

## Modular structure

```text
config.py
config/
  settings.py   # user preferences
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

Click the palette icon or press `Super + Shift + T` to select a Catppuccin preset. A theme writes `config/colors.py`; restart Qtile if existing widgets do not update.

Choose a wallpaper with `Super + Shift + W`. If pywal is installed, it generates a palette and the helper maps it to Qtile's semantic colors before restarting Qtile. Without pywal, the wallpaper changes but the active Catppuccin palette remains. To restore a Catppuccin preset, use the theme picker.

## Weather

Weather is fetched from wttr.in using curl. Set `QTILE_WEATHER_LOCATION` to a city or postal code in the environment; otherwise wttr.in auto-detects a coarse location. The widget needs network access and may be blank if the service is unavailable.

## Customize

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md). Edit `config/settings.py` for gaps, border width, bar height, terminal and wallpaper directory. Edit `config/layouts.py` for layout order and `config/widgets.py` for bar modules.

## Screenshots

No screenshots are included yet. Add genuine screenshots from a running session under `docs/screenshots/`.

## Troubleshooting and uninstall

- Qtile fails to start: run `qtile check -c ~/.config/qtile/config.py` and inspect session logs.
- Missing icons: install and select a Nerd Font.
- Wallpaper fails: check that swww-daemon is running and the image is readable.
- Clipboard history empty: ensure the autostart watcher `wl-paste --type text --watch cliphist store` is running.
- Weather blank: verify curl, network access and the location setting.

Run `./uninstall.sh` to move the active config to a timestamped backup. Packages and wallpapers are left untouched.
