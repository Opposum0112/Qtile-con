# Qtile-Con: Material Desktop for Qtile Wayland

A modular Qtile Wayland desktop configuration inspired by Dank Material Shell and Noctalia: Catppuccin styling, interactive bar, launchers, widgets, wallpaper-driven colors, quick controls, screenshot and clipboard workflows.

> **Status:** initial community configuration. Tested hardware/distribution combinations vary. Run the installer with `--dry-run` first and review package names for your distribution.

## Features

- Qtile's native Wayland backend and modular Python configuration.
- Catppuccin Mocha default palette, with Latte, Frappe and Macchiato presets.
- Top bar: workspaces, active window, CPU, memory, weather, volume, clock, tray.
- Clickable actions: app launcher, layout selector, wallpaper picker, theme menu, clipboard history, screenshot.
- Wallpaper selection with `swww`; optional `pywal` palette generation for wallpaper-derived colors.
- Fuzzel launcher, grim/slurp screenshots, wl-clipboard clipboard tools, playerctl media controls.
- Configurable gaps, borders, layouts, keybindings and bar modules.
- Install and uninstall scripts; helper scripts are kept separate from Qtile config.

## Quick start

1. Install a supported Linux distribution with a working Wayland session and Python 3.
2. Clone this repository:
   ```sh
   git clone https://github.com/Opposum0112/Qtile-con.git
   cd Qtile-con
   ```
3. Preview installation and then install:
   ```sh
   ./install.sh --dry-run
   ./install.sh
   ```
4. Copy some images into `~/Pictures/Wallpapers`.
5. Log out and select **Qtile (Wayland)** in your display manager. If your display manager does not list it, consult the Qtile Wayland documentation for your distribution.
6. Start with `Super + Return` for a terminal, `Super + D` for the launcher, and `Super + Shift + W` for wallpapers.

The installer backs up existing `~/.config/qtile` to a timestamped directory before installing. It does not change your display manager or automatically replace your login session.

## Dependencies

Core: Qtile with Wayland support, Python, `fuzzel`, `foot` (or change terminal in `config/settings.py`), `swww`, `grim`, `slurp`, `wl-clipboard`, `cliphist`, `playerctl`, `pamixer`, `brightnessctl`, `lm_sensors`, `curl`, `jq`, `libnotify`, `network-manager-applet` (optional tray applet), and a Nerd Font.

Optional: `python-pywal` / `pywal` for wallpaper-derived colors, `wlogout` for a graphical logout menu, `pavucontrol` for audio settings, `blueman` for Bluetooth, `nm-connection-editor` for network settings.

Package names vary by distribution. The installer supports common Debian/Ubuntu, Fedora, Arch, and openSUSE package managers where possible; review the script before running it. Install Qtile from your distribution or a Python environment that provides the Wayland backend and its native dependencies.

## Keybindings

| Shortcut | Action |
|---|---|
| `Super + Return` | Terminal |
| `Super + D` | Fuzzel app launcher |
| `Super + Tab` | Next layout |
| `Super + Shift + Space` | Interactive layout picker |
| `Super + Shift + W` | Wallpaper picker |
| `Super + Shift + T` | Theme picker |
| `Super + V` | Clipboard history |
| `Print` | Select screenshot region |
| `Super + Print` | Full-screen screenshot |
| `Super + Ctrl + R` | Restart Qtile |
| `Super + Escape` | Lock screen (if `swaylock` is installed) |
| `Super + Shift + Q` | Kill focused window |
| `Super + Shift + E` | Qtile exit prompt |

## Structure

```text
.
├── config.py                 # Qtile entry point
├── config/
│   ├── __init__.py
│   ├── settings.py           # user-adjustable settings
│   ├── keys.py               # keybindings
│   ├── groups.py             # workspaces
│   ├── layouts.py            # layouts, gaps and borders
│   ├── widgets.py            # native Qtile bar
│   ├── screens.py            # screen/bar setup
│   └── colors.py              # generated/current palette
├── scripts/
│   ├── qtile-action           # launcher/layout/theme/wallpaper actions
│   ├── set-wallpaper
│   ├── set-theme
│   ├── weather
│   └── screenshot
├── themes/                    # Catppuccin palette presets
├── install.sh
└── uninstall.sh
```

## Wallpaper-driven theme

Use `Super + Shift + W` to select a wallpaper. If `pywal` is installed, the wallpaper action asks it to generate a palette and then restarts Qtile so the bar picks up the new colors. You can instead choose a fixed Catppuccin variant with `Super + Shift + T`. Theme changes update the generated `config/colors.py`; restart Qtile if a running widget does not refresh immediately.

## Weather

The weather widget uses `curl` against wttr.in and displays a compact current-conditions string. Set `QTILE_WEATHER_LOCATION` in your environment to a city or postal code. The service requires network access; weather is omitted if the request fails. Avoid setting a precise home address.

## Customize

- Edit `config/settings.py` for terminal, launcher, wallpaper directory, gaps, border width and bar height.
- Edit `config/layouts.py` to add/remove layouts.
- Add custom widgets in `config/widgets.py`.
- Add palette JSON files under `themes/` and choose them using `scripts/set-theme`.
- Helpers are designed to fail gracefully when optional applications are missing.

## Screenshots

No screenshots are included yet. Add screenshots of your own running desktop under `docs/screenshots/` and link them here; screenshots should reflect a real session rather than mockups.

## Troubleshooting

- **Qtile fails to start:** run `qtile check -c ~/.config/qtile/config.py` from a terminal and inspect the session log.
- **No Wayland session:** verify that your Qtile package was built with Wayland support and that its backend dependencies are installed.
- **Missing icons:** install a Nerd Font and select it in your terminal/font configuration.
- **Wallpaper does not change:** check `swww-daemon` is running and that the wallpaper path is readable.
- **Clipboard history empty:** copy some text first; `cliphist` needs a Wayland clipboard watcher. Start `wl-paste --type text --watch cliphist store` in your autostart.
- **Weather blank:** check `curl`, internet access, and `QTILE_WEATHER_LOCATION`.

## Safety and uninstall

Review `install.sh` before running it. The installer installs packages only after prompting. `./uninstall.sh` removes this configuration and its user-level autostart file, but deliberately does not remove packages or personal wallpapers.
