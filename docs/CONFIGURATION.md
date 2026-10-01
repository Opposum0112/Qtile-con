# Configuration Guide

- `qtile_config/settings.py`: Terminal, launcher, wallpaper directory, gaps, borders and bar dimensions.
- `qtile_config/keys.py`: Keyboard shortcuts and workspace navigation actions.
- `qtile_config/groups.py`: Workspace labels and numbering.
- `qtile_config/layouts.py`: Layout definitions (including Niri-style smooth Scroller, Columns, Monad, Tile, Matrix), borders, and gaps.
- `qtile_config/scroller.py`: Niri-style smooth scroller horizontal ribbon layout engine with cubic ease-out viewport panning.
- `qtile_config/widgets.py`: Top bar widgets, styling capsules, separators and click actions.
- `qtile_config/screens.py`: Screen and bar placement.
- `qtile_config/colors.py`: Active palette loaded from the selected theme preset.
- `alacritty/alacritty.toml`: Starter Alacritty configuration importing the active theme palette.
- `alacritty/catppuccin-mocha.toml`: Matching Catppuccin Mocha terminal color palette.

## Prerequisites & External Software Requirements

This project targets **Qtile on X11/Xorg**, not a Wayland session. The automated installer (`./install.sh`) automatically installs all required dependencies and configures fallback mechanisms.

The environment relies on the following external software components:
- **Core Environment**: `qtile` (X11 backend), Xorg display server, Python 3 (`python3-psutil`, `python3-requests`, `python3-cairocffi`, `python3-xcffib`, `python3-dbus`, `libpangocairo-1.0-0`).
- **Terminals & Editors**: `alacritty` (primary GPU terminal), `kitty` (secondary terminal), `micro` (terminal editor with synchronized themes).
- **Launcher & Menus**: `rofi` (applications combi launcher, run dialog, window manager menus, power menu, theme selector).
- **Audio & Media**: `pamixer`, `pavucontrol`, `alsa-utils` (`amixer`), PulseAudio / PipeWire (`pactl` / `wpctl`), `playerctl` (media keys).
- **Display, Wallpaper & Screenshots**: `feh`, `maim`, `xclip`, `xsel`.
- **Hardware & Networking**: `network-manager-applet` (`nm-connection-editor`), `brightnessctl`.
- **System Monitoring & Diagnostics**: `btop`, `htop`, `witr` (process causation tree tracer).
- **System Administration & Snapshots**: `cockpit` (`cockpit-ws`, `cockpit-bridge`, `cockpit-system`), `snapper` (Btrfs root/home snapshot management & immediate rollback).
- **Notifications & Security**: `libnotify` (`notify-send`), notification daemon (e.g. `dunst`), `i3lock`.
- **Utilities & Docs**: `greenclip` (clipboard history), `man-db` (searchable man pages `Super+F1`), `curl`, `jq`, `xdotool`.
- **Typography & Gesture Compilation**: JetBrainsMono Nerd Font (or any Nerd Font for bar icons), `gcc`, `make`, `libx11-dev`, `libxtst-dev` (for native C gesture daemon compilation).

## Interactive Bar & System Widgets

- **Parrot OS Launcher**: Click the Parrot OS icon (``) at the left of the bar to open the Rofi application launcher.
- **RAM & CPU Widgets**: The RAM widget shows used memory in GB (`󰘚 3.3G`). Left-click opens `btop`/`htop` in Alacritty. Right-click opens the deep system investigation tool.
- **Process & Background Tools**: Displays total processes and background tools/daemons count (`󰒋 233 (bg:228)`). Hover displays a detailed breakdown of top background tools and resource consumption. Left-click opens an interactive process manager with actions (inspect memory, deep investigate, trace syscalls, terminate), and middle-click filters background tools directly.
- **Session & Autostart Services**: The services widget (`󰒓 25 svcs`) tracks active systemd user services and desktop autostart background daemons. Clicking opens an interactive management menu to view status, restart, stop, or read journal logs. Right-click launches `sys-investigate --services`.
- **Battery & Power Diagnostics**: Monitors battery level and charging state with dynamic icons (`󰂄 72%`, `󰁹`, `󰂃`). Left-click triggers a detailed battery health and power notification.
- **SysAdmin Expandable Widget Group (`󰠬`)**: Starts collapsed as a single icon widget (`󰠬`) in the top bar to preserve screen real estate. Left-clicking toggles open (`󰠬 `) an integrated capsule revealing three real-time administrative subwidgets:
  - **Cockpit Web Console (`󰟀 ON` / `󰟀 OFF`)**: Real-time status of the Cockpit web administration socket. Left-click opens `https://localhost:9090` in the browser. Right-click opens an interactive Rofi menu to start, stop, or restart the Cockpit service.
  - **AI Agents Running (`󰧑 {count} agents`)**: Continuous monitoring of background AI processes, local LLM runners, and autonomous coding agents (`agy`, `antigravity`, `goose`, `codex`, `grok`, `claude`, `aider`, `ollama`, Python agents, `witr`). Left-click opens an interactive Rofi management menu with quick launchers, process causation tracing (`witr`), and termination controls (SIGTERM/SIGKILL).
  - **Snapper Snapshots & Immediate Rollback (`󰁯 {count} snaps`)**: Real-time Btrfs snapshot count. Left-clicking displays the snapshot list in reverse chronological order; selecting any snapshot immediately prompts for confirmation, creates a safety pre-rollback snapshot, executes `pkexec snapper rollback <num>`, and offers an instant reboot prompt. Right-click creates a manual snapshot with a custom description.
- **Critical Indicators & System Health**: Real-time watchdog monitoring CPU, RAM, root disk, battery, and thermal limits (`󰗠 OK`). If any critical threshold is breached (CPU > 85%, RAM > 85%, Disk > 90%, Battery < 15%), it displays an alert pill in the bar. Click launches `sys-investigate`.
- **Interactive Volume Slider**: Left-clicking the volume widget (or pressing `Super+Shift+V`) displays a smooth native floating volume slider popup with quick preset buttons (0%, 25%, 50%, 75%, 100%), mute toggle, and mouse scroll support. Right-click opens the output selector menu.
- **Network Speed & Wi-Fi**: The bar displays real-time download and upload speeds (`󰖩 ↓... ↑...`). Left-click opens the Wi-Fi launcher menu (which automatically deduplicates duplicate AP signals and sorts strongest first), and right-click launches `nm-connection-editor`.
- **Hourly Weather Forecast (Card Grid Dashboard)**: Left-clicking the weather widget opens a multi-column weather card grid dashboard displaying today's hourly conditions, precipitation probabilities, wind, and temperatures in cards rather than a list. Right-click allows configuring the target city.
- **Documentation & Man Pages**: Clicking the `󰈙` icon in the bar (or pressing `Super+Shift+M`) opens an instant fuzzy-searchable manual page index launching `man` in Alacritty.
- **Clipboard History**: Clicking `󰅍` (or pressing `Super+V`) opens clipboard history using a compact Catppuccin Rofi menu.
- **Unified 8-Tab Shortcuts & Developer Tools Launcher**: Pressing `Super + /` (or `Super + ?` / `Super + s`) opens the interactive tabbed cheatsheet palette with 8 dedicated modes/tabs:
  1. **Qtile & Gestures (`qtile`)**: Real-time dynamically parsed Qtile keyboard shortcuts (100+ keys) + 10 touchpad gestures + 13 bar widget clicks. Qtile shortcuts update **automatically and immediately** whenever `qtile_config/keys.py` is edited or added to, without requiring manual catalog updates or reloading.
  2. **Config Locations (`config`)**: Pressing `Super + Ctrl + /` directly opens the environment configuration catalog covering 74+ config files, paths, statuses, and file sizes. Selecting any file opens it immediately in the terminal editor (`micro`/`nano`/`helix`).
  3. **Settings Guide (`guide`)**: Interactive systems architecture guide with 10 structured sections from `SETTINGS_GUIDE.md`.
  4. **Kitty Terminal (`kitty`)**: Complete GPU-accelerated terminal emulator keybindings, kitten hints, tabs, splits, and layouts. Clicking any shortcut copies the key combination to your X11 clipboard.
  5. **Micro Text Editor (`micro`)**: Full terminal editor shortcuts covering file operations, multi-cursor (`Alt+n`, `Ctrl+Alt+Up/Down`), search/replace, splits, and tabs.
  6. **Helix Modal Editor (`helix`)**: Modal text editing shortcuts covering normal movements, Kakoune selection model (`x`, `v`, `s`, `Alt+s`), Space leader menu (`Space+f`, `Space+s`, `Space+d`), and LSP actions.
  7. **Yazi File Manager (`yazi`)**: Complete asynchronous terminal file manager shortcuts covering navigation (`h`/`j`/`k`/`l`), tabs, selection, search/jump (`z`, `Z`, `s`), and file operations (`y`, `x`, `p`, `d`).
  8. **GNU Nano Editor (`nano`)**: Standard terminal editor shortcuts covering file management, cutbuffer operations (`Ctrl+K`, `Ctrl+U`, `Alt+6`), search/replace, and navigation.
  - **Native Rofi Sidebar Tabs**: Rofi natively renders clickable tab buttons at the bottom of the window (`-sidebar-mode`). Switch between tabs effortlessly using `Shift+Left` / `Shift+Right`, `Ctrl+Tab`, or mouse clicks. Quick jump lines are also embedded in the list view for instant fuzzy switching.
- **Clean Consistent Spacing**: The top bar uses styled capsule pills and subtle vertical separators to cleanly demarcate layout, hardware metrics, network/audio, quick tools, and system tray.

## Niri-Style Smooth Scroller Layout (`Scroller`)

Qtile-Con introduces a native Niri / PaperWM inspired **infinite horizontal ribbon layout** with smooth animated scrolling (`qtile_config/scroller.py`):

- **Horizontal Ribbon Architecture**: Windows and columns are organized along an infinite horizontal plane. Moving focus between columns smoothly pans the viewport camera to keep the active column centered or comfortably in view.
- **Column-Based Dynamic Tiling**:
  - Each new application opens in its own new column to the right of the active window by default (`new_window_as_column=True`).
  - Columns can contain multiple windows stacked vertically (`split=True`), dividing the column height evenly.
  - Press `Super + Ctrl + s` (`toggle_split`) to switch between vertical tiling and single-window stacked view within the active column.
  - Press `Super + Ctrl + e` (`expel`) to detach a stacked window into its own separate column.
  - Press `Super + Ctrl + [` or `Super + Ctrl + ]` (`consume_left` / `consume_right`) to merge neighboring columns together.
- **Buttery-Smooth Ease-Out Viewport Animations**:
  - Panning uses a cubic ease-out curve: $f(t) = 1 - (1 - t)^3$ at 60 FPS, providing fluid physical deceleration.
  - If focus changes rapidly, active animations are cancelled and smoothly interpolated from the current position without stutter or sudden jumping.
  - Configurable parameters: `animation_duration=0.22`, `animation_fps=60`, `animate=True`.
- **Column Width Presets & Sizing**:
  - Presets: `1/3` (33.3%), `1/2` (50%), `2/3` (66.7%), and `1.0` (Full screen width).
  - Press `Super + w` (`cycle_width`) to cycle the active column through preset proportions.
  - Press `Super + =` / `Super + -` (`grow_width` / `shrink_width`) to adjust column width in fine 5% increments.
  - Press `Super + c` (`center`) to manually center the focused column in the viewport.
- **Centering Strategies (`center_focused`)**:
  - `"on-overflow"` (Default): When total column widths exceed the screen width, the active column is centered on screen with adjacent columns peeking in at the left and right borders. When columns fit within screen width, they align cleanly across the display.
  - `"always"`: Always center the active column on screen.
  - `"never"`: Only pan viewport as much as necessary to ensure the active column is completely on screen.

## Window State Management (Maximize, Minimize & Restore)

Qtile-Con provides unified, layout-agnostic window state management across all layouts (Scroller, Columns, MonadTall, MonadWide, Tile, Matrix, Max, and Floating):

- **Maximize Window (`Super + Shift + f` or `Super + x`)**:
  - Toggles the active window between maximized state and its tiled position (`lazy.window.toggle_maximize()`).
  - Maximized windows automatically display the active theme's accent border (`border_focus=ACCENT`, `max_border_width=BORDER_WIDTH`), floating over the layout layer without clipping or hiding borders.
- **Minimize Window (`Super + i` or `Super + Shift + -`)**:
  - Hides the active window from view (unmapped Iconic state) and removes it from the layout's active geometry (`lazy.window.toggle_minimize()`).
  - In `Scroller`, minimized windows do not occupy any column ribbon space or create empty visual slots. In stacked columns, remaining non-minimized windows dynamically stretch to occupy the full column height.
- **Restore Most Recently Minimized Window (`Super + u`)**:
  - Immediately restores and focuses the last minimized window on the current workspace (or searches adjacent workspaces if current workspace has none).
- **Restore All Minimized Windows (`Super + Shift + u`)**:
  - Unminimizes every minimized window on the current workspace simultaneously (`qtile-action restore all`).
- **Browse & Restore Minimized Windows Palette (`Super + Ctrl + u` or `qtile-action restore`)**:
  - Opens an interactive Rofi menu listing all minimized windows across workspaces with their workspace number, window title, and application class.
  - Selecting an item unminimizes the window, brings its workspace to screen, and shifts focus directly to it. Selecting `󰖯  Restore All Minimized Windows` unminimizes all windows at once.

## Touchpad Gestures & Workspace Navigation

Qtile-Con includes a native X11 gesture daemon (`scripts/gesture-daemon`) using XInput 2.4 gesture events on the root window. It requires no root privileges or `input` group membership. It is automatically launched by `scripts/autostart` and can be managed via `./scripts/setup-gestures` or `scripts/gesture-daemon`.

- **Switch Workspaces**: 3-finger swipe left (next) / right (prev), `Super+[`, or `Super+]`.
- **Cycle Layouts**: 3-finger swipe up (next) / down (prev).
- **Move Window across Workspaces**: 4-finger swipe left (next) / right (prev), `Super+Shift+[`, `Super+Shift+]`, or `Super+Ctrl+Left/Right`.
- **Application Launcher**: 4-finger swipe up (`Super + Alt + Return`).
- **Terminal Emulator**: 4-finger swipe down (`Super + Alt + Shift + Return`).
- **Toggle Floating / Fullscreen**: Pinch in (contract to floating: `Super + Alt + Space`), Pinch out (expand to fullscreen: `Super + Alt + f`).

## Multi-Application Theme Synchronization & Wallpaper Grid

- **Global Theme Switcher**: Selecting a theme via `Super+Shift+T` (or running `scripts/apply-global-theme <theme>`) automatically propagates the chosen color palette across:
  - **Qtile**: Updates bar, borders, layout accents, and pills in `qtile_config/colors.py`.
  - **Alacritty**: Updates `~/.config/alacritty/qtile-con-catppuccin-mocha.toml` with live hot-reloading.
  - **Kitty**: Updates `~/.config/kitty/current-theme.conf` and `qtile-theme.conf`, instantly sending `SIGUSR1` to active kitty instances.
  - **Micro Editor**: Compiles and updates `~/.config/micro/colorschemes/qtile-theme.micro`.
  - **Firefox**: Dynamically styles the browser chrome via `userChrome.css` across all profiles.
  - **All Rofi Menus & Widgets**: Dynamically regenerates `catppuccin-mocha.rasi`, `catppuccin-mocha-grid.rasi`, and `catppuccin-mocha-weather.rasi` so that the App Launcher, Layout Picker, Volume Slider, Wi-Fi Menu, Clipboard, Power Menu, Weather Forecast, Process & Services menus, and the Cheatsheet Reference Palette (`Super+/`) all instantly match the selected palette.
- **Supported Built-in Presets**:
  - `catppuccin-mocha.json` (Default soothing dark pastel)
  - `catppuccin-frappe.json` (Muted dark pastel)
  - `catppuccin-latte.json` (Light pastel)
  - `gruvbox-dark.json` (Warm retro groove palette)
  - `github-dark.json` (Sleek GitHub dark canvas palette)
  - `ayu-dark.json` (Modern high-contrast editor palette)
  - `solarized-dark.json` (Classic cyan/base03 terminal palette)
- **Extensible Architecture**: Dropping any new theme JSON file into `themes/` automatically exposes it in the Rofi Theme Selector with complete multi-application synchronization.
- **Wallpaper Thumbnail Grid**: Pressing `Super+Shift+W` displays wallpapers in a 3x3 visual thumbnail card grid with image previews. It also features a built-in font selection mode to switch active Nerd Font families dynamically.

## Application Rules & Workspace Tag Assignments (Apprules)

Qtile automatically routes newly launched applications to dedicated workspaces based on the tag icons displayed in the top bar:

- **1 (`󰈹`)**: Firefox and primary web browsers (`firefox`, `firefox-esr`, `librewolf`, `waterfox`, `tor-browser`, `zen-browser`).
- **2 (`󰆍`)**: Terminal emulators (`alacritty`, `kitty`, `xterm`, `foot`, `wezterm`, `gnome-terminal`, `st`, etc.).
- **3 (`󰖟`)**: Web development, code editors, and secondary browsers (`chromium`, `google-chrome`, `brave-browser`, `code`, `vscodium`, `sublime_text`, `geany`, `jetbrains-*`, `neovide`).
- **4 (`󰙯`)**: Communication & messaging (`discord`, `vesktop`, `telegram-desktop`, `slack`, `signal`, `element`, `thunderbird`, `whatsapp-for-linux`).
- **5 (`󰎆`)**: Music, audio, and media players (`spotify`, `rhythmbox`, `audacious`, `vlc`, `mpv`, `celluloid`, `kodi`).
- **6 (`󰓓`)**: Steam, gaming platforms, and emulators (`steam`, `steamwebhelper`, `lutris`, `heroic`, `prismlauncher`, `retroarch`, `bottles`).
- **7 (`󰒓`)**: Settings, hardware configuration, and system tools (`pavucontrol`, `arandr`, `lxappearance`, `nitrogen`, `gparted`, `timeshift-gtk`).
- **8 (`󰉋`)**: File managers and archive utilities (`thunar`, `nemo`, `nautilus`, `dolphin`, `pcmanfm`, `file-roller`).
- **9 (`󰐃`)**: Creative design, office, and document viewers (`gimp`, `inkscape`, `blender`, `krita`, `obs`, `libreoffice`, `obsidian`, `evince`, `zathura`).

## Smart Launcher & Terminal Execution Engine (`scripts/qtile-run`)

Qtile-Con provides a unified application and command launching experience:

- **Enriched Binary PATH Resolution**:
  The session automatically enriches `PATH` across Qtile, autostart, and Rofi scripts to discover binaries from:
  - Cargo: `~/.cargo/bin`
  - Linuxbrew: `/home/linuxbrew/.linuxbrew/bin`, `/home/linuxbrew/.linuxbrew/sbin`, `~/.linuxbrew/bin`, `~/.linuxbrew/sbin`
  - Pipx and User Binaries: `~/.local/bin`
  - Snap & Flatpak: `/snap/bin`, `/var/lib/flatpak/exports/bin`
  - Go: `~/go/bin`
  - Qtile Desktop Scripts: `~/.config/qtile/scripts`
- **Application Launcher with Mode Tabs (`Super+d`)**:
  `Super+d` (or left-clicking the Parrot OS icon ``) invokes Rofi with dedicated mode switcher tabs (`sidebar-mode: true`):
  - `󰍉 All` (`combi`): Unified view combining desktop applications (`drun`) and run binaries (`run`) with `-combi-hide-mode-prefix` for a clean list.
  - `󰣆 Apps` (`drun`): Freedesktop installed desktop applications matching name, generic, and exec fields with desktop icons.
  - `󰌌 Run` (`run`): Raw executables in your enriched `PATH`.
  - `󰈞 File` (`file` via `scripts/rofi-file-search`): Blazing-fast fuzzy file search powered by Rust `fd` / `fdfind` (with `find` fallback). Indexes up to 10,000 files in under 50ms across your home and project workspaces while intelligently excluding heavy system caches (`.git`, `.cache`, `node_modules`, `.venv`, `.cargo`, `snap`, etc.). Typing dynamically filters matching files; selecting a text/code file opens it in `micro` within Alacritty, images in `feh`, and documents via `xdg-open`.
  - `󰈬 Content` (`content` via `scripts/rofi-content-search`): Instant file content search powered by Rust `ripgrep` (`rg`) (with `grep` fallback). Type any search string (or prefix with `re:` for regular expressions) and press Enter to search inside project, document, and configuration files across `$HOME` in milliseconds. Selecting any matched line directly opens `micro` at the exact line number (`micro +LINE:COL FILE`).
  - **Mode Switching Navigation**: Use `Shift+Right` / `Shift+Left`, `Control+Tab`, or click the tab buttons at the bottom to switch modes.
- **Dedicated Run Dialog**:
  `Super+r` (or right-clicking the Parrot OS icon ``) opens a dedicated run launcher specifically for executing command-line utilities and scripts without mode tabs.
- **Smart Runner (`scripts/qtile-run`)**:
  Standard Rofi executes commands blindly in the background, which causes CLI/TUI tools to fail silently or exit immediately without a TTY. `scripts/qtile-run` solves this dynamically:
  1. Inspects `.desktop` files for `Terminal=true`.
  2. Recognizes interactive terminal utilities (e.g. `htop`, `btop`, `top`, `micro`, `nano`, `vim`, `nvim`, `cargo`, `brew`, `bash`, `zsh`, `python3`, `ipython`, `gdb`, `curl`, `wget`, `ping`).
  3. Launches CLI tools inside an interactive Alacritty terminal: `alacritty -e bash -ic '<cmd>; exec bash'`, keeping the shell active so output can be inspected.
  4. Launches GUI applications detached cleanly in the background without terminal clutter.

## Installer & Uninstaller Architecture

The installer (`install.sh`) and uninstaller (`uninstall.sh`) are designed for complete OS awareness, non-destructive operation, and clean removal:

### 1. Operating System Detection & Package Management
`install.sh` queries `/etc/os-release` and matches native package managers:
- **Debian / Ubuntu / Parrot / Kali**: `apt` (uses `dpkg-query -W -f='${Status}'`)
- **Arch / Manjaro / EndeavourOS**: `pacman` (uses `pacman -Qq`)
- **Fedora**: `dnf` (uses `rpm -q`)
- **openSUSE**: `zypper` (uses `rpm -q` / `zypper se -i`)
- **Solus**: `eopkg` (uses `eopkg list-installed`)

### 2. Automated Fallback Engines
- **Qtile**: If the host distribution lacks Qtile packages or encounters broken package dependencies, `install.sh` automatically falls back to installing Qtile via `pipx`.
- **Process Causation Tracer (`witr`)**: If unavailable in system repositories, the installer automatically detects the CPU architecture (`x86_64` or `aarch64`) and downloads the official binary from GitHub releases into `~/.local/bin/witr`.
- **JetBrainsMono Nerd Font**: If no Nerd Font is installed, the installer downloads and unpacks the JetBrainsMono Nerd Font bundle to `~/.local/share/fonts/JetBrainsMono`, followed by `fc-cache -f`.
- **Native Gesture Daemon**: Automatically compiles `scripts/gesture-daemon.c` using `gcc -O2 -lX11 -lXtst` if `gcc` and development headers are present.
- **Display Manager Session**: Automatically writes `/usr/share/xsessions/qtile.desktop` if absent so the session is immediately available at login.

### 3. Manifest-Driven Clean Uninstallation
To guarantee that `uninstall.sh` never damages pre-existing software:
- Prior to installation, `install.sh` checks which packages already exist on the machine.
- Only newly installed system packages, pipx packages, standalone binaries, and fonts are recorded in the install manifest (`~/.local/share/qtile-con/install-manifest.json` and `~/.config/qtile/.install-manifest.json`).
- Running `./uninstall.sh --purge` reads the manifest and uninstalls **only** packages that were installed by `install.sh`. Pre-existing packages (like `git`, `python3`, or system editors) are left completely untouched.
- `uninstall.sh` safely archives `~/.config/qtile` to `~/.config/qtile.removed.<timestamp>` and can automatically restore previous user configuration backups via `./uninstall.sh --restore`.

## Complete Configuration Deployment & PATH Resolution

The installer guarantees deployment of all configuration files needed for a fully functional, cohesive desktop environment:

- **Qtile Configuration** (`~/.config/qtile/`): Includes `config.py`, all `qtile_config/` modules, all executable utility scripts in `scripts/`, theme presets in `themes/`, and documentation.
- **Alacritty Configuration** (`~/.config/alacritty/`): Starter `alacritty.toml` importing `qtile-con-catppuccin-mocha.toml` with live hot-reloading.
- **Kitty Configuration** (`~/.config/kitty/`): Starter `kitty.conf` importing `qtile-theme.conf` with instant `SIGUSR1` palette updates.
- **Dunst Notification Configuration** (`~/.config/dunst/dunstrc`): Pre-configured with rounded corners, JetBrainsMono Nerd Font, and theme accents.
- **Micro Editor Configuration** (`~/.config/micro/colorschemes/qtile-theme.micro`): Synchronized editor syntax highlighting palette.
- **Touchpad Configuration & Gestures** (`scripts/setup-touchpad`, `~/.config/libinput-gestures.conf`): Automated tap-to-click, double-tap, tap-and-drag, natural scrolling, and multi-finger gestures.
- **Display Manager Session** (`/usr/share/xsessions/qtile.desktop`): Standard X11 session launcher.

### Touchpad Tap-to-Click & Bar Tap Architecture

- **Hardware Tap-to-Click (`scripts/setup-touchpad`)**:
  - Automatically queries XInput for all detected pointer devices and enables `libinput Tapping Enabled` (1-finger left click, 2-finger right click, 3-finger middle click), `libinput Tapping Drag Enabled`, and `libinput Natural Scrolling Enabled`.
  - Sets click method to `clickfinger` for intuitive MacBook/laptop touchpad ergonomics.
  - Triggered automatically on session login via `scripts/autostart` and available as a standalone utility.
- **Bar Single & Double Tap Interactions (`WindowTitle` & `BarSpacer`)**:
  - **Window Title Single Tap / Click**: Focuses the window and brings it to front. If on an empty workspace, restores the most recently minimized window.
  - **Window Title Double Tap / Double Click**: Instantly toggles maximize / restore (`toggle_maximize`) on the active window.
  - **Window Title 2-Finger Tap / Right Click**: Toggles window floating mode (`toggle_floating`).
  - **Window Title 3-Finger Tap / Middle Click**: Minimizes active window (`toggle_minimize`).
  - **Window Title Scroll Wheel**: Cycles window focus forward / backward within the active workspace.
  - **Empty Bar Space Single Tap**: Restores the most recently minimized window.
  - **Empty Bar Space Double Tap**: Toggles maximize / restore on the active window.
  - **Empty Bar Space 2-Finger Tap / Right Click**: Restores all minimized windows on the workspace.

### 4-Layer PATH Setting Architecture

1. **Qtile WM Process**: `qtile_config/settings.py` sets `os.environ["PATH"] = get_unified_path()` so any process spawned by Qtile inherits all user binary paths.
2. **Session Autostart**: `scripts/autostart` exports the unified `PATH` to all startup daemons and background tasks.
3. **Runners & Dispatchers**: `scripts/qtile-action` and `scripts/qtile-run` ensure that commands launched via Rofi (`Super+d` and `Super+r`) have access to all user tools.
4. **Shell Profiles**: `install.sh` automatically adds `export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$HOME/.config/qtile/scripts:$PATH"` to `~/.profile` and `~/.bashrc`, and invokes `pipx ensurepath`.

## Desktop Notification Architecture

Qtile-Con routes desktop alerts through `dunst` using standard Freedesktop notifications:

- **Battery Diagnostics** (`scripts/battery-status`): Dispatches detailed power diagnostics, cycle count, and charging health. Alerts with critical urgency when battery is under 15%.
- **Critical Threshold Watchdog** (`scripts/critical-indicators`): High-priority sticky alerts when CPU > 85%, RAM > 85%, Disk > 90%, or Battery < 15%.
- **Hover Tooltips** (`qtile_config/widgets.py`): Instantaneous hover popups via `notify-send -h string:x-canonical-private-synchronous:hover_<id>` displaying top background daemons, user services, and weather details without needing mouse clicks.
- **Volume & Audio Feedback** (`scripts/volume-slider`): Instant volume feedback popup with volume percentage or mute state.
- **Wi-Fi & Network Events** (`scripts/wifi-menu`): Network connection status, SSID details, and authentication prompts.
- **System Services & Process Management** (`scripts/services-info`, `scripts/process-info`): Real-time notifications for service restart, stop, and SIGTERM/SIGKILL confirmations.
- **Screenshots & Clipboard** (`scripts/screenshot`, `scripts/clipboard-history`): Screenshot preview with path and clipboard status, and clipboard history copy confirmations.
- **Theme Synchronization** (`scripts/apply-global-theme`): Dynamically regenerates `~/.config/dunst/dunstrc` to match the selected theme (Mocha, Gruvbox, GitHub, Ayu, Solarized) and triggers `dunstctl reload`.

## Validation

Run:

```sh
bash ~/.config/qtile/scripts/check-config
# Or:
qtile check -c ~/.config/qtile/config.py
```

If Qtile is installed in a pipx environment, `check-config` automatically locates the pipx executable. Always run `check-config` before logging out of the session.

