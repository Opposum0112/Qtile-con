# Qtile Systems Architecture & Settings Guide

Welcome to the comprehensive configuration, maintenance, and customization guide for the **Qtile-Con** desktop environment.

---

## 1. System Architecture & Modular Layout

Qtile-Con is engineered using a modular Python configuration pattern:

| Component | Active File | Description |
| :--- | :--- | :--- |
| **Core Entry** | `~/.config/qtile/config.py` | Top-level entry point, session lifecycle hooks, and dialog auto-centering rules. |
| **Settings** | `~/.config/qtile/qtile_config/settings.py` | Global constants, fonts, default applications, launcher modes, and unified PATH. |
| **Keybindings** | `~/.config/qtile/qtile_config/keys.py` | Mac ergonomics shortcuts, brightness controls, screenshot tools, and layouts. |
| **Layouts** | `~/.config/qtile/qtile_config/layouts.py` | Tiling layouts (Scroller, Columns, Monad) and Polkit/utility floating rules. |
| **Widgets** | `~/.config/qtile/qtile_config/widgets.py` | Bar capsules, process watchdog, window title expander, and tap gesture handlers. |
| **Colors** | `~/.config/qtile/qtile_config/colors.py` | Dynamic palette synchronized across Qtile, terminals, editors, and menus. |
| **Autostart** | `~/.config/qtile/scripts/autostart` | Session startup script initializing Polkit, Dunst, gestures, and daemons. |

---

## 2. Color Theme Customization

Themes are stored in JSON format inside `~/.config/qtile/themes/`.

### 2.1 Supported Preset Themes
- **Catppuccin Mocha** (`catppuccin-mocha`)
- **Catppuccin Frappé** (`catppuccin-frappe`)
- **Catppuccin Latte** (`catppuccin-latte` - light theme)
- **Gruvbox Dark** (`gruvbox-dark`)
- **GitHub Dark** (`github-dark`)
- **Ayu Dark** (`ayu-dark`)
- **Solarized Dark** (`solarized-dark`)

### 2.2 Adding a New Custom Theme
To add a new theme, create a JSON file in `~/.config/qtile/themes/<theme_name>.json`:
```json
{
  "name": "My Theme",
  "colors": {
    "base": "#1a1b26",
    "mantle": "#16161e",
    "crust": "#13141c",
    "surface0": "#24283b",
    "surface1": "#292e42",
    "surface2": "#3b4261",
    "text": "#c0caf5",
    "subtext": "#a9b1d6",
    "overlay": "#565f89",
    "mauve": "#bb9af7",
    "lavender": "#7aa2f7",
    "red": "#f7768e",
    "peach": "#ff9e64",
    "yellow": "#e0af68",
    "green": "#9ece6a",
    "teal": "#73daca",
    "blue": "#7aa2f7",
    "sapphire": "#2ac3de",
    "pink": "#f7768e"
  }
}
```

### 2.3 Applying Themes
- **Interactive Selector:** Press `Super + Shift + t` to open the visual theme picker.
- **Command Line:** Run `apply-global-theme <theme_name>` (e.g., `apply-global-theme gruvbox-dark`).
  - Automatically updates: Qtile Bar, Alacritty, Kitty, Micro, Firefox, Dunst, Rofi, Thunar/GTK icons (`Tela` vs `Tela-dark`), and Yazi flavors.

---

## 3. Hardware Controls & Mac Ergonomics

Configured specifically for Apple keyboards (`mod4` = Command, `mod1` = Option, no physical PrintScreen or Home keys):

### 3.1 Screenshots (Standard Mac Ergonomics)
- **Fullscreen Screenshot:** `Super + Shift + 3` (saved to `~/Pictures/Screenshots` & clipboard)
- **Area / Window Selection:** `Super + Shift + 4` (interactive crosshair selection)
- **Direct to Clipboard:** `Super + Shift + Control + 4` (copies directly to clipboard without disk clutter)
- *Note:* Legacy `PrintScreen` and `Home` keys are eliminated; window moving to workspaces is mapped to `Super + Ctrl + 1..9` ensuring zero conflict with screenshots.

### 3.2 Display & Keyboard Backlight
- **Screen Brightness:**
  - Dedicated hardware keys: `XF86MonBrightnessUp` / `XF86MonBrightnessDown` (+/- 5%)
  - Ergonomic keyboard fallbacks: `Super + F2` (increase) / `Super + F1` (decrease), `Super + n` / `Super + b`
- **Keyboard Backlight:**
  - Dedicated hardware keys: `XF86KbdBrightnessUp` / `XF86KbdBrightnessDown` (+/- 10%)
  - Keyboard fallbacks: `Super + F6` (increase) / `Super + F5` (decrease)
- **Passwordless Hardware Permission Setup:**
  - Udev rule: `/etc/udev/rules.d/90-backlight.rules`
  - Group requirements: `sudo usermod -aG video,input $USER`
  - Helper script: `setup-backlight` (run once to apply permissions)

---

## 4. PolicyKit Management & Root GUI Authentication

To allow GUI tools requiring root authorization (like **GParted**, synaptic, or disk utilities) to prompt graphically:

### 4.1 Agent Daemon
- Managed by `lxpolkit` (or `polkit-gnome`), launched automatically in `~/.config/qtile/scripts/autostart`.
- Memory footprint: strictly < 5 MB RAM.

### 4.2 Qtile Window Rules
- Configured in `~/.config/qtile/qtile_config/layouts.py` (`Match(wm_class="lxpolkit")`, etc.).
- Hook in `~/.config/qtile/config.py` (`client_new`) automatically forces floating, centers the prompt dialog, and brings it above tiled windows.

---

## 5. Qtile Bar Widget Interactions & Process Management

### 5.1 Active Window Title Expansion
- The `WindowTitle` widget has been expanded to support full window names without truncation.
- **Single-Tap on Title:** Focus active window / bring to front.
- **Double-Tap on Title:** Toggle maximize / restore.
- **Middle-Click on Title:** Toggle minimize.
- **Right-Click on Title:** Toggle floating.
- **Mouse Scroll on Title:** Cycle focus between adjacent windows on current workspace.

### 5.2 Background Process Watchdog Widget (`󰒋`)
- **Bar Capsule:** Sits alongside Session Services in a unified pill capsule.
- **Hover:** Displays real-time breakdown of top memory daemons, top CPU processes, and total background count.
- **Left-Click:** Opens interactive Rofi popup list of running background processes.
- **Middle-Click or Right-Click:** Opens the safe termination menu: select any running process to send `SIGTERM` gracefully.

### 5.3 Memory Lock (< 800 MB Idle)
- Redundant daemons (`baloo_file`, `mate-user-share`) disabled in `~/.config/autostart/`.
- Autostart streamlined to essential desktop services.

---

## 6. File Management Integration

### 6.1 Graphical File Manager: Thunar
- Launch shortcut: `Super + e`
- Configured with `thunar-archive-plugin`, `thunar-volman`, and `gvfs`.
- Uses **Tela** and **Tela-dark** icon themes, automatically synchronized with the global theme.

### 6.2 Terminal File Manager: Yazi
- Launch shortcut: `Super + Shift + e` (runs `alacritty -e yazi`).
- Fast asynchronous Rust architecture with low idle footprint.
- Native image preview support via Kitty graphics protocol.
- Integrates with `fzf`, `zoxide`, `jq`, and `pdftoppm`.
- Theme flavors located in `~/.config/yazi/flavors/` (`catppuccin-mocha`, `catppuccin-latte`, `dracula`, `gruvbox-dark`).

---

## 7. Interactive Reference & Cheatsheet (Tabbed Launcher)

Press `Super + /`, `Super + ?`, or `Super + s` to open the unified cheatsheet palette. It features an interactive **8-tab launcher** with Rofi native sidebar modes:

### 7.1 Eight Dedicated Modes & Tabs
1. **Qtile & Gestures (`Super + /` or `keybindings-cheatsheet qtile`):**
   - **Real-Time Dynamic Updates:** Keybindings are parsed directly from `qtile_config/keys.py` via Python source loading on every launch. Whenever you edit `keys.py` or add a new shortcut, the cheatsheet reflects the change **immediately** without requiring manual catalog edits.
   - Includes 100+ keyboard shortcuts, 10 touchpad gestures, and 13 bar widget click interactions.
2. **Environment Configuration Files (`Super + Ctrl + /` or `keybindings-cheatsheet config`):**
   - Catalogs 74+ configuration files, symlink targets, active paths, statuses, and file sizes.
   - Selecting any file opens it immediately in the terminal editor (`micro`/`nano`/`helix`).
3. **Settings Guide (`keybindings-cheatsheet guide`):**
   - Quick interactive guide to the 10 architecture chapters in `SETTINGS_GUIDE.md`.
4. **Kitty Terminal Keybindings (`keybindings-cheatsheet kitty`):**
   - Complete reference for window layouts, kittens, hints, tabs, and splits.
   - Selecting any shortcut copies the key combination to the X11 clipboard and sends a desktop notification.
5. **Micro Editor Keybindings (`keybindings-cheatsheet micro`):**
   - Comprehensive shortcuts for multi-cursor (`Alt+n`, `Ctrl+Alt+Up/Down`), file operations, splits, and search.
6. **Helix Modal Editor Keybindings (`keybindings-cheatsheet helix`):**
   - Normal mode movement, Kakoune selection model (`x`, `v`, `s`, `Alt+s`), Space leader menu, and LSP shortcuts.
7. **Yazi File Manager Keybindings (`keybindings-cheatsheet yazi`):**
   - Asynchronous navigation, tabs, bulk file operations, visual selection, and fast search (`z`, `Z`, `s`).
8. **GNU Nano Editor Keybindings (`keybindings-cheatsheet nano`):**
   - File management, cutbuffer actions (`Ctrl+K`, `Ctrl+U`, `Alt+6`), justify, and search/replace.

### 7.2 Native Rofi Sidebar Tabs & Navigation
- Rofi renders 8 clickable buttons at the bottom of the window (`-sidebar-mode`).
- Cycle between tabs using `Shift+Left` / `Shift+Right` or `Ctrl+Tab`.
- Quick jump lines (`[SWITCH TO TAB: ...]`) and compact tab chips are displayed at the top of each view for instant fuzzy jumping.
- Run non-interactively via CLI flags: `--json [tab]`, `--json-all`, `--markdown`, `--help`.

---

## 8. Independent Workspace Layouts & Zero-Leakage Architecture

Every workspace in Qtile-Con maintains an isolated, independent layout state:

### 8.1 Zero Layout Leakage
- Changing the layout on one workspace (via `Super + Tab`, `Super + Option + Up/Down`, or `Super + Shift + Space`) modifies **only the active workspace**.
- No other workspace is modified or affected.

### 8.2 Purposeful Workspace Defaults
Each workspace initializes with a default layout optimized for its application role:
- **Workspace 1 (󰈹 Browsers):** `columns`
- **Workspace 2 (󰆍 Terminals):** `scroller` (infinite horizontal ribbon)
- **Workspace 3 (󰖟 Code / IDEs):** `columns`
- **Workspace 4 (󰙯 Chat / Discord):** `monadtall`
- **Workspace 5 (󰎆 Media / Music):** `monadtall`
- **Workspace 6 (󰓓 Gaming):** `max` (fullscreen single client)
- **Workspace 7 (󰒓 System Tools):** `floating` (utility dialogs)
- **Workspace 8 (󰉋 File Managers):** `columns` (side-by-side comparison)
- **Workspace 9 (󰐃 Graphics / Design):** `monadwide` (wide canvas)

### 8.3 Persistent Layout Cache
- Interactive layout choices are saved automatically to `~/.cache/qtile/workspace_layouts.json`.
- Restored cleanly across desktop reloads and reboots without overwriting other workspaces.

### 8.4 Workspace-Scoped Selector & Responsive Bar
- **Selector (`Super + Shift + Space`):** Displays the active workspace name, indicates which layout is currently active with `(active)`, and sends a confirmation notification.
- **Bar Icon Widget:** Listens to both `layout_change` and `setgroup` hooks to ensure immediate visual updates whenever you switch between workspaces.

---

## 9. SysAdmin Expandable Widget Group & Immediate Rollback Architecture

To balance comprehensive administrative capability with a clean, clutter-free bar, Qtile-Con provides an expandable SysAdmin WidgetBox (`󰠬`):

### 9.1 Expandable WidgetBox Architecture
- **Collapsed by Default:** The widget group starts collapsed as a single icon (`󰠬`), preserving horizontal bar real estate.
- **Dynamic Capsule Expansion:** Clicking `󰠬` smoothly expands the widget box inline (`󰠬 `), displaying three subwidgets in a matching themed pill capsule (`surface0` background). Clicking again collapses the capsule back to the icon.
- **Custom Widget Class:** Implemented in `qtile_config/widgets.py` via `SysAdminWidgetBox` (subclass of `libqtile.widget.WidgetBox`) with custom redraw and toggle callbacks.

### 9.2 Cockpit Web Console Integration (`scripts/cockpit-info`)
- **Status Indicator:** Displays `󰟀 ON` (green accent when `cockpit.socket` / `cockpit.service` is active) or `󰟀 OFF` (overlay/subtext color when inactive).
- **Left-Click:** Opens the Cockpit Web Administration Console directly at `https://localhost:9090` in your default browser.
- **Right-Click:** Opens an interactive Rofi service menu allowing you to:
  - Open Web Console (`https://localhost:9090`)
  - Start Cockpit Service (`sudo systemctl start cockpit.socket`)
  - Stop Cockpit Service (`sudo systemctl stop cockpit.socket`)
  - Restart Cockpit Service (`sudo systemctl restart cockpit.socket`)
  - View Live Cockpit Logs (`journalctl -u cockpit -n 50`)

### 9.3 Running AI Agents Monitor (`scripts/ai-agents-info`)
- **Real-Time Monitoring:** Continuously scans the process table for active AI coding agents, local model runners, and background assistants:
  - Antigravity / Google AI CLI (`antigravity`, `agy`, `gemini`)
  - Autonomous Developer Agents: Goose (`goose`, `goose-server`), Codex (`codex`, `codex-cli`, `openai-codex`), Grok (`grok`, `grok-cli`, `xai-grok`), Claude Code (`claude`), Aider (`aider`), Devin
  - Local LLM Runners (`ollama`, `vllm`, `llama-server`, `open-webui`, `tabby`)
  - IDE Agents & Tools (`copilot-agent`, `cursor-agent`, `continue-server`, `interpreter`)
  - Python Multi-Agent Frameworks (`crewai`, `autogen`, `langchain`, `langgraph`, `fabric`, `swarm`)
  - Process causation tracers (`witr`)
- **Status Pill:** Displays `󰧑 {N} agents` (e.g., `󰧑 2 agents`).
- **Interactive Process Manager (Left-Click):**
  - Displays each running agent process with PID, CPU %, Memory, and Command line in Rofi.
  - Quick launch shortcuts for available agents (`agy`, `goose`, `codex`, `grok`, `claude`, `aider`, `ollama`).
  - Selecting any running agent displays its full process causation tree using `witr`.
  - Offers graceful termination (`SIGTERM`) or forced termination (`SIGKILL`) with desktop notifications.

### 9.4 Snapper Btrfs Snapshots & Immediate Rollback (`scripts/snapper-info`)
- **Status Pill:** Displays `󰁯 {N} snaps` showing the current total number of snapshots on the Btrfs root filesystem.
- **Immediate Rollback Palette (Left-Click):**
  - Opens an interactive Rofi menu displaying all snapshots in reverse-chronological order (newest first) with snapshot ID, date/time, type (`single`, `pre`, `post`), and description.
  - Selecting any snapshot enters the **Immediate Rollback Routine**:
    1. Prompts for explicit confirmation with the snapshot ID and description.
    2. Automatically creates a safety pre-rollback snapshot (`pre-rollback-backup-to-<id>`).
    3. Executes `pkexec snapper rollback <id>` using Polkit graphical authentication.
    4. Displays a success notification and offers an immediate reboot prompt to boot into the restored snapshot state.
- **Manual Snapshot Creation (Right-Click):** Prompts for a snapshot description and instantly triggers `snapper -c root create -d "<description>"`.
- **Non-Root Unprivileged Configuration:** Automatically configured by `install.sh` via Snapper's `ALLOW_USERS` and `ALLOW_GROUPS` configuration directives with permission bits set on `/.snapshots`, allowing status queries without root privileges.
