# Qtile-Con Keyboard Shortcuts & Gestures Cheatsheet

## Unified Tabbed Developer Tools & Keybindings Reference Palette

Quickly access this interactive tabbed reference palette anywhere on your desktop by pressing:

> `Super + /`  or  `Super + ?`  or  `Super + s`

To jump directly to any specific tool tab:

- **Qtile & Gestures:** `Super + /` or `keybindings-cheatsheet qtile`
- **Config Locations:** `Super + Ctrl + /` or `keybindings-cheatsheet config`
- **Settings Guide:** `keybindings-cheatsheet guide`
- **Kitty Terminal:** `keybindings-cheatsheet kitty`
- **Micro Editor:** `keybindings-cheatsheet micro`
- **Helix Modal Editor:** `keybindings-cheatsheet helix`
- **Yazi File Manager:** `keybindings-cheatsheet yazi`
- **GNU Nano Editor:** `keybindings-cheatsheet nano`

---

# 1. Qtile Window Manager & Gestures

## Launchers & Tools

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Super + Return` | Terminal Emulator (Alacritty) | `alacritty` |
| `Super + d` | Application Launcher (Rofi Combi: Apps & Run) | `~/.config/qtile/scripts/qtile-action launcher` |
| `Super + r` | Run Command / CLI Binary Launcher | `~/.config/qtile/scripts/qtile-action run` |
| `Super + e` | Graphical File Manager (Thunar with plugins) | `thunar` |
| `Super + Shift + e` | Terminal Emulator (Alacritty) | `alacritty -e yazi` |
| `Super + v` | Clipboard History Manager (Greenclip / Rofi) | `~/.config/qtile/scripts/qtile-action clipboard` |
| `Super + Shift + v` | Interactive Floating Volume Slider & Sinks | `~/.config/qtile/scripts/qtile-action slider` |
| `Super + /` | Keybinding Cheatsheet & Reference Palette | `~/.config/qtile/scripts/qtile-action cheatsheet` |
| `Super + Shift + /` | Keybinding Cheatsheet & Reference Palette | `~/.config/qtile/scripts/qtile-action cheatsheet` |
| `Super + s` | Keybinding Cheatsheet & Reference Palette | `~/.config/qtile/scripts/qtile-action cheatsheet` |
| `Super + Ctrl + /` | Environment Configuration Files & Locations Browser | `~/.config/qtile/scripts/qtile-action configs` |
| `Super + Shift + m` | Manual Pages & Documentation Lookup (Rofi man) | `~/.config/qtile/scripts/qtile-action man` |
| `Super + Alt + Return` | Terminal Emulator (Alacritty) | `rofi -show combi -modes combi,drun,run,file:~/.config/qtile/scripts/rofi-file-search,content:~/.config/qtile/scripts/rofi-content-search -combi-modes drun,run -combi-hide-mode-prefix -run-command '~/.config/qtile/scripts/qtile-run {cmd}' -run-shell-command '~/.config/qtile/scripts/qtile-run {cmd}' -show-icons -icon-theme Adwaita -terminal alacritty -theme ~/.config/qtile/themes/catppuccin-mocha.rasi` |
| `Super + Shift + Alt + Return` | Terminal Emulator (Alacritty) | `alacritty` |

## Screenshots & Power

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Super + Ctrl + r` | Restart / Reload Qtile Window Manager | `qtile cmd-obj -o window -f restart` |
| `Super + Ctrl + q` | Power & Session Logout Menu (Lock, Reboot, Poweroff) | `~/.config/qtile/scripts/logout-menu` |
| `Super + Shift + Escape` | Power & Session Logout Menu (Lock, Reboot, Poweroff) | `~/.config/qtile/scripts/logout-menu` |
| `Super + Escape` | Instant Screen Lock (i3lock) | `i3lock` |
| `Super + Shift + 3` | Fullscreen Screenshot (Mac Ergonomics) | `~/.config/qtile/scripts/screenshot full` |
| `Super + Shift + 4` | Area / Window Screenshot to File (Mac Ergonomics) | `~/.config/qtile/scripts/screenshot region` |
| `Super + Ctrl + Shift + 4` | Area Screenshot Directly to Clipboard (Mac Ergonomics) | `~/.config/qtile/scripts/screenshot clipboard` |

## Window Focus & Layout

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Super + Shift + q` | Close / Kill Focused Window | `qtile cmd-obj -o window -f kill` |
| `Super + Tab` | Cycle to Next Layout (Columns, Scroller, Monad, etc.) | `qtile cmd-obj -o window -f next_layout` |
| `Super + Shift + Tab` | Cycle to Previous Layout | `qtile cmd-obj -o window -f prev_layout` |
| `Super + Shift + Space` | Layout Selector Menu (Columns, Scroller, Monad, etc.) | `~/.config/qtile/scripts/qtile-action layout` |
| `Super + Left` | Focus Window to the Left | `qtile cmd-obj -o window -f left` |
| `Super + Right` | Focus Window to the Right | `qtile cmd-obj -o window -f right` |
| `Super + Down` | Focus Window Downwards | `qtile cmd-obj -o window -f down` |
| `Super + Up` | Focus Window Upwards | `qtile cmd-obj -o window -f up` |
| `Super + Shift + Left` | Shuffle / Swap Focused Window to the Left | `qtile cmd-obj -o window -f shuffle_left` |
| `Super + Shift + Right` | Shuffle / Swap Focused Window to the Right | `qtile cmd-obj -o window -f shuffle_right` |
| `Super + Shift + Down` | Shuffle Focused Window Downwards | `qtile cmd-obj -o window -f shuffle_down` |
| `Super + Shift + Up` | Shuffle Focused Window Upwards | `qtile cmd-obj -o window -f shuffle_up` |
| `Super + =` | Grow Column Width in Viewport | `qtile cmd-obj -o layout -f grow_width` |
| `Super + -` | Shrink Column Width in Viewport | `qtile cmd-obj -o layout -f shrink_width` |
| `Super + w` | Cycle Column Width (1/3, 1/2, 2/3, Full) | `qtile cmd-obj -o layout -f cycle_width` |
| `Super + c` | Center Active Column in Viewport | `qtile cmd-obj -o layout -f center` |
| `Super + Ctrl + s` | Toggle Column Split / Stacked Mode | `qtile cmd-obj -o layout -f toggle_split` |
| `Super + Ctrl + e` | Expel Active Window to New Column | `qtile cmd-obj -o layout -f expel` |
| `Super + Ctrl + [` | Consume / Merge Column to the Left | `qtile cmd-obj -o window -f consume_left` |
| `Super + Ctrl + ]` | Consume / Merge Column to the Right | `qtile cmd-obj -o window -f consume_right` |
| `Super + f` | Toggle Active Window Fullscreen | `qtile cmd-obj -o window -f toggle_fullscreen` |
| `Super + Space` | Toggle Active Window Floating Mode | `qtile cmd-obj -o window -f toggle_floating` |
| `Super + Shift + f` | Toggle Active Window Maximize (With Theme Borders) | `qtile cmd-obj -o window -f toggle_maximize` |
| `Super + x` | Toggle Active Window Maximize (With Theme Borders) | `qtile cmd-obj -o window -f toggle_maximize` |
| `Super + i` | Minimize Active Window (Hide & Exclude from Layout) | `qtile cmd-obj -o window -f toggle_minimize` |
| `Super + Shift + -` | Minimize Active Window (Hide & Exclude from Layout) | `qtile cmd-obj -o window -f toggle_minimize` |
| `Super + u` | Restore Most Recently Minimized Window | Desktop Notification |
| `Super + Shift + u` | Restore All Minimized Windows on Workspace | Desktop Notification |
| `Super + Ctrl + u` | Browse & Restore Minimized Windows Palette (Rofi) | `~/.config/qtile/scripts/qtile-action restore` |
| `Super + Alt + Up` | Cycle to Next Layout (Columns, Scroller, Monad, etc.) | `qtile cmd-obj -o window -f next_layout` |
| `Super + Alt + Down` | Cycle to Previous Layout | `qtile cmd-obj -o window -f prev_layout` |
| `Super + Alt + f` | Toggle Active Window Fullscreen | `qtile cmd-obj -o window -f toggle_fullscreen` |
| `Super + Alt + Space` | Toggle Active Window Floating Mode | `qtile cmd-obj -o window -f toggle_floating` |

## Theme & Styling

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Super + Shift + w` | Wallpaper & Font Thumbnail Grid Selector | `~/.config/qtile/scripts/set-wallpaper` |
| `Super + Shift + t` | Global Theme Selector (Catppuccin, Gruvbox, GitHub, Ayu, Solarized) | `~/.config/qtile/scripts/set-theme` |

## Media & Hardware

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `XF86MonBrightnessUp` | Increase Screen Brightness (+5%) | `brightnessctl set +5%` |
| `XF86MonBrightnessDown` | Decrease Screen Brightness (-5%) | `brightnessctl set 5%-` |
| `Super + F2` | Increase Screen Brightness (+5%) | `brightnessctl set +5%` |
| `Super + F1` | Decrease Screen Brightness (-5%) | `brightnessctl set 5%-` |
| `Super + n` | Increase Screen Brightness (+5%) | `brightnessctl set +5%` |
| `Super + b` | Decrease Screen Brightness (-5%) | `brightnessctl set 5%-` |
| `XF86KbdBrightnessUp` | Increase Keyboard Backlight (+10%) | `brightnessctl --device='*kbd*' set +10%` |
| `XF86KbdBrightnessDown` | Decrease Keyboard Backlight (-10%) | `brightnessctl --device='*kbd*' set 10%-` |
| `Super + F6` | Increase Keyboard Backlight (+10%) | `brightnessctl --device='*kbd*' set +10%` |
| `Super + F5` | Decrease Keyboard Backlight (-10%) | `brightnessctl --device='*kbd*' set 10%-` |
| `XF86AudioRaiseVolume` | Increase Audio Volume (+5%) | `pamixer --increase 5` |
| `XF86AudioLowerVolume` | Decrease Audio Volume (-5%) | `pamixer --decrease 5` |
| `XF86AudioMute` | Toggle Audio Mute | `pamixer --toggle-mute` |
| `Super + . (period)` | Increase Audio Volume (+5%) | `pamixer --increase 5` |
| `Super + , (comma)` | Decrease Audio Volume (-5%) | `pamixer --decrease 5` |
| `Super + m` | Toggle Audio Mute | `pamixer --toggle-mute` |

## Workspaces & Tags

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Super + [` | Switch to Previous Workspace (Bracket Navigation) | `qtile cmd-obj -o window -f prev_group` |
| `Super + ]` | Switch to Next Workspace (Bracket Navigation) | `qtile cmd-obj -o window -f next_group` |
| `Super + Shift + [` | Move Focused Window to Prev Workspace & Follow | Desktop Notification |
| `Super + Shift + ]` | Move Focused Window to Next Workspace & Follow | Desktop Notification |
| `Super + Ctrl + Left` | Move Focused Window to Prev Workspace & Follow | Desktop Notification |
| `Super + Ctrl + Right` | Move Focused Window to Next Workspace & Follow | Desktop Notification |
| `Super + Alt + Left` | Switch to Previous Workspace (Bracket Navigation) | `qtile cmd-obj -o window -f prev_group` |
| `Super + Alt + Right` | Switch to Next Workspace (Bracket Navigation) | `qtile cmd-obj -o window -f next_group` |
| `Super + Shift + Alt + Left` | Move Focused Window to Prev Workspace & Follow | Desktop Notification |
| `Super + Shift + Alt + Right` | Move Focused Window to Next Workspace & Follow | Desktop Notification |
| `Super + 1` | Switch to Workspace 1 | Desktop Notification |
| `Super + Ctrl + 1` | Move Focused Window to Workspace 1 & Follow | Desktop Notification |
| `Super + 2` | Switch to Workspace 2 | Desktop Notification |
| `Super + Ctrl + 2` | Move Focused Window to Workspace 2 & Follow | Desktop Notification |
| `Super + 3` | Switch to Workspace 3 | Desktop Notification |
| `Super + Ctrl + 3` | Move Focused Window to Workspace 3 & Follow | Desktop Notification |
| `Super + 4` | Switch to Workspace 4 | Desktop Notification |
| `Super + Ctrl + 4` | Move Focused Window to Workspace 4 & Follow | Desktop Notification |
| `Super + 5` | Switch to Workspace 5 | Desktop Notification |
| `Super + Ctrl + 5` | Move Focused Window to Workspace 5 & Follow | Desktop Notification |
| `Super + 6` | Switch to Workspace 6 | Desktop Notification |
| `Super + Ctrl + 6` | Move Focused Window to Workspace 6 & Follow | Desktop Notification |
| `Super + 7` | Switch to Workspace 7 | Desktop Notification |
| `Super + Ctrl + 7` | Move Focused Window to Workspace 7 & Follow | Desktop Notification |
| `Super + 8` | Switch to Workspace 8 | Desktop Notification |
| `Super + Ctrl + 8` | Move Focused Window to Workspace 8 & Follow | Desktop Notification |
| `Super + 9` | Switch to Workspace 9 | Desktop Notification |
| `Super + Ctrl + 9` | Move Focused Window to Workspace 9 & Follow | Desktop Notification |

## Touchpad Gestures

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `3-Finger Swipe Left` | Switch to Next Workspace (Super + Alt + Right) | Desktop Notification |
| `3-Finger Swipe Right` | Switch to Previous Workspace (Super + Alt + Left) | Desktop Notification |
| `3-Finger Swipe Up` | Cycle to Next Layout (Super + Alt + Up) | Desktop Notification |
| `3-Finger Swipe Down` | Cycle to Previous Layout (Super + Alt + Down) | Desktop Notification |
| `4-Finger Swipe Left` | Move Active Window to Next Workspace & Follow | Desktop Notification |
| `4-Finger Swipe Right` | Move Active Window to Prev Workspace & Follow | Desktop Notification |
| `4-Finger Swipe Up` | Open Application Launcher (Super + Alt + Return) | `~/.config/qtile/scripts/qtile-action launcher` |
| `4-Finger Swipe Down` | Open Terminal Emulator (Super + Alt + Shift + Return) | `~/.config/qtile/scripts/qtile-action monitor general` |
| `3/4-Finger Pinch Out` | Toggle Window Fullscreen (Super + Alt + f) | `qtile cmd-obj -o window -f toggle_fullscreen` |
| `3/4-Finger Pinch In` | Toggle Window Floating (Super + Alt + Space) | `qtile cmd-obj -o window -f toggle_floating` |

## Bar Widget Clicks

| Key / Gesture | Description | Action |
| :--- | :--- | :--- |
| `Click Parrot Logo` | Left: App Launcher │ Right: Power Menu | `~/.config/qtile/scripts/qtile-action launcher` |
| `Click RAM / CPU Widget` | Left: System Monitor (btop/htop) │ Right: Deep Investigate | `~/.config/qtile/scripts/qtile-action monitor cpu` |
| `Click Process Widget` | Left: witr Process Menu │ Middle: BG Filter │ Right: Deep Trace | `~/.config/qtile/scripts/process-info --menu` |
| `Click Services Widget` | Left: Services Management │ Right: Service Memory | `~/.config/qtile/scripts/services-info --menu` |
| `Click SysAdmin Icon` | Left: Toggle Subwidgets (Cockpit, AI, Snapper) │ Right: SysAdmin Control Center | `~/.config/qtile/scripts/qtile-action sysadmin` |
| `Click Cockpit Subwidget` | Left: Open Web Console (Port 9090) │ Right: Cockpit Service Menu | `~/.config/qtile/scripts/qtile-action cockpit` |
| `Click AI Agents Subwidget` | Left/Right: AI Agents Monitor, Process Inspection & Termination Menu | `~/.config/qtile/scripts/qtile-action agents` |
| `Click Snapper Subwidget` | Left: Immediate Rollback Menu │ Right: Create Manual Snapshot | `~/.config/qtile/scripts/qtile-action snapper` |
| `Click Weather Widget` | Left: Hourly Card Dashboard │ Right: Configure City | `~/.config/qtile/scripts/qtile-action weather` |
| `Click Network Widget` | Left: Wi-Fi Menu │ Right: Connection Editor | `~/.config/qtile/scripts/qtile-action wifi` |
| `Click Volume Widget` | Left: Volume Slider │ Right: Audio Sinks │ Scroll: Vol +/- | `~/.config/qtile/scripts/qtile-action slider` |
| `Click Battery Widget` | Left: Battery Health Diagnostics Notification | `~/.config/qtile/scripts/battery-status --notify` |
| `Click Health Widget` | Left: Deep System Watchdog Investigation | `~/.config/qtile/scripts/sys-investigate` |

---

# 2. Kitty Terminal Emulator

## Window Management

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + Enter` | New Window in current layout |
| `Ctrl + Shift + w` | Close active window |
| `Ctrl + Shift + ]` | Focus next window |
| `Ctrl + Shift + [` | Focus previous window |
| `Ctrl + Shift + f` | Move active window forward |
| `Ctrl + Shift + b` | Move active window backward |
| `Ctrl + Shift + `` | Move active window to top |
| `Ctrl + Shift + r` | Start interactive window resize mode |
| `Ctrl + Shift + 1 .. 9` | Focus specific window 1..9 |

## Tab Management

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + t` | Open new tab |
| `Ctrl + Shift + q` | Close active tab |
| `Ctrl + Shift + Right / Left` | Next / Previous tab |
| `Ctrl + Shift + . / ,` | Move tab forward / backward |
| `Ctrl + Shift + Alt + t` | Set / rename tab title |

## Layouts & Splits

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + l` | Cycle to next window layout (splits, stack, grid, fat, tall) |
| `Ctrl + Shift + z` | Toggle zoomed / maximized window in stack layout |

## Scrolling & Search

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + Up / Down` | Scroll terminal buffer one line up / down |
| `Ctrl + Shift + PageUp / PageDown` | Scroll terminal buffer one page up / down |
| `Ctrl + Shift + Home / End` | Scroll directly to top / bottom of buffer |
| `Ctrl + Shift + h` | View scrollback buffer in pager / search |
| `Ctrl + Shift + g` | View last command output in pager |

## Clipboard & Font Size

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + c` | Copy selection to system clipboard |
| `Ctrl + Shift + v` | Paste from system clipboard |
| `Ctrl + Shift + s` | Paste from primary selection buffer |
| `Ctrl + Shift + Equal (+)` | Increase terminal font size (+1pt) |
| `Ctrl + Shift + Minus (-)` | Decrease terminal font size (-1pt) |
| `Ctrl + Shift + Backspace` | Reset terminal font size to default |

## Hints & Kittens

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Shift + e` | Open URL / file path hints picker |
| `Ctrl + Shift + p > f` | Insert matched file path into terminal |
| `Ctrl + Shift + p > l` | Insert line hint into terminal |
| `Ctrl + Shift + p > w` | Insert word hint into terminal |
| `Ctrl + Shift + u` | Open Unicode character input & picker |
| `Ctrl + Shift + F5` | Reload kitty.conf configuration without restarting |
| `Ctrl + Shift + F6` | Open debug / log inspector window |

---

# 3. Micro Terminal Text Editor

## File Operations

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + s` | Save current file buffer |
| `Ctrl + q` | Quit editor (prompts if unsaved changes exist) |
| `Ctrl + o` | Open file prompt |
| `Ctrl + p` | Command palette / interactive command bar |

## Editing & Clipboard

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + z` | Undo last edit |
| `Ctrl + y` | Redo last undone change |
| `Ctrl + c` | Copy selected text to clipboard |
| `Ctrl + x` | Cut selected text to clipboard |
| `Ctrl + v` | Paste text from clipboard |
| `Ctrl + a` | Select all text in buffer |
| `Ctrl + d` | Duplicate current line |
| `Ctrl + k` | Cut entire current line to clipboard |
| `Alt + /  or  Ctrl + _` | Toggle line comment (#, //, etc.) |

## Multi-Cursor

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + Alt + Up` | Spawn multi-cursor on line above |
| `Ctrl + Alt + Down` | Spawn multi-cursor on line below |
| `Alt + n` | Spawn cursor on next occurrence of selection |
| `Alt + p` | Remove last spawned multi-cursor |
| `Alt + x` | Skip current occurrence and find next match |
| `Escape` | Clear all multi-cursors / cancel selection |

## Search & Navigation

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + f` | Find text in current buffer |
| `Ctrl + n` | Jump to next search match |
| `Ctrl + p` | Jump to previous search match |
| `Alt + r` | Find and interactive replace text |
| `Ctrl + l` | Jump to line number (:line) |

## Split Panes & Tabs

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + e > vsplit <file>` | Split view vertically with file |
| `Ctrl + e > hsplit <file>` | Split view horizontally with file |
| `Ctrl + w` | Cycle focus between split panes |
| `Ctrl + t` | Open new tab |
| `Alt + , / .` | Switch to previous / next editor tab |

## Help & Commands

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + g` | Open interactive help document |
| `Ctrl + e` | Open command line prompt (:set tabsize 4, :term, etc.) |

---

# 4. Helix Modern Modal Editor

## Normal Mode Movement

| Key Combination | Description |
| :--- | :--- |
| `h / j / k / l` | Move cursor left / down / up / right |
| `w` | Jump forward to beginning of next word |
| `b` | Jump backward to beginning of previous word |
| `e` | Jump forward to end of current/next word |
| `W / B / E` | Jump forward / backward by WORD (whitespace-delimited) |
| `0 / ^` | Jump to beginning of line / first non-blank character |
| `$` | Jump to end of line |
| `g + g` | Go to first line of buffer |
| `g + e` | Go to last line of buffer |
| `Ctrl + u / Ctrl + d` | Scroll half-page up / down |
| `Ctrl + b / Ctrl + f` | Scroll full-page up / down |

## Selection & Expansion

| Key Combination | Description |
| :--- | :--- |
| `x` | Select current line (repeat to extend downwards) |
| `X` | Extend selection upwards line-by-line |
| `v` | Enter / toggle Select (Visual) mode |
| `;` | Collapse selection to single cursor |
| `Alt + ;` | Flip cursor to opposite end of selection |
| `Alt + s` | Split active selection into separate lines |
| `s` | Select regex matches inside active selection |
| `S` | Split active selection by regex matches |

## Changes & Editing

| Key Combination | Description |
| :--- | :--- |
| `i / a` | Insert mode before / after cursor |
| `I / A` | Insert mode at line start / line end |
| `o / O` | Open line below / above and enter Insert mode |
| `c` | Change selection (delete text and enter Insert mode) |
| `d` | Delete selection (yanked to register) |
| `y` | Yank selection into register |
| `p / P` | Paste after / before cursor |
| `r` | Replace single character under cursor |
| `u / U` | Undo / Redo change |
| `> / <` | Indent / outdent selected lines |
| `~` | Toggle letter case (lower/upper) |

## Space Leader Menu

| Key Combination | Description |
| :--- | :--- |
| `Space + f` | Fuzzy file picker |
| `Space + b` | Buffer list & switcher |
| `Space + s` | Document symbol picker (LSP) |
| `Space + S` | Workspace symbol picker (LSP) |
| `Space + d` | Diagnostics picker (errors/warnings) |
| `Space + k` | Hover documentation popup (LSP) |
| `Space + r` | Rename symbol under cursor (LSP) |
| `Space + a` | Code action quickfix (LSP) |
| `Space + w` | Window split actions (vsplit, hsplit) |
| `Space + y` | Yank selection directly to system clipboard |
| `Space + p` | Paste from system clipboard |
| `Space + ?` | Command reference / cheatsheet palette |

## Search & Characters

| Key Combination | Description |
| :--- | :--- |
| `/ / ?` | Search forward / backward regex pattern |
| `n / N` | Next / Previous search match |
| `*` | Search pattern for word under cursor |
| `f <char>` | Find character forward on line |
| `F <char>` | Find character backward on line |
| `t <char>` | Till character forward (stop before char) |
| `T <char>` | Till character backward |

## Splits & Files

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + w > v` | Split active pane vertically |
| `Ctrl + w > s` | Split active pane horizontally |
| `Ctrl + w > h/j/k/l` | Move focus to adjacent split pane |
| `Ctrl + w > q` | Close active split pane |
| `:w / :q / :wq` | Save / Quit / Save and Quit buffer |

---

# 5. Yazi Asynchronous File Manager

## Navigation & Movement

| Key Combination | Description |
| :--- | :--- |
| `h` | Move to parent directory (back) |
| `l` | Enter directory / open file |
| `j / k` | Move selection down / up |
| `Enter` | Open file in default application |
| `g + g` | Jump to first entry in directory |
| `G` | Jump to last entry in directory |
| `Ctrl + u / Ctrl + d` | Scroll preview half-page up / down |
| `Ctrl + b / Ctrl + f` | Scroll preview full-page up / down |
| `~` | Jump to user home directory (~) |
| `g + c` | Jump directly to ~/.config |
| `g + d` | Jump directly to ~/Downloads |

## Tabs & Workspaces

| Key Combination | Description |
| :--- | :--- |
| `t` | Create new tab with current directory |
| `1 .. 9` | Switch directly to tab 1..9 |
| `[ / ]` | Switch to previous / next tab |
| `w` | Close active tab |

## File Operations

| Key Combination | Description |
| :--- | :--- |
| `Space` | Toggle file selection and advance cursor |
| `v` | Enter visual range selection mode |
| `V` | Enter visual select-unset mode |
| `Ctrl + a` | Select all files in directory |
| `Ctrl + r` | Invert file selection |
| `y` | Yank (copy) selected files |
| `x` | Cut selected files |
| `p` | Paste copied / cut files here |
| `d` | Move selected files to Trash |
| `D` | Permanently delete selected files |
| `a` | Create new file or folder (end with / for folder) |
| `r` | Rename selected file |
| `;` | Run shell command on selected files |
| `:` | Execute blocking shell command |

## Search & Jump

| Key Combination | Description |
| :--- | :--- |
| `/` | Fuzzy filter files in current folder |
| `f` | Hop / jump to matching file |
| `z` | Fast jump using Zoxide database |
| `Z` | Interactive fuzzy jump with FZF |
| `s` | Search file contents with ripgrep (rg) |

## Sorting & Display

| Key Combination | Description |
| :--- | :--- |
| `.` | Toggle hidden dotfiles visibility |
| `, + m` | Sort by modified time |
| `, + s` | Sort by file size |
| `, + a` | Sort alphabetically by name |
| `, + e` | Sort by file extension |
| `, + r` | Reverse sort order |
| `F1 / ?` | Show interactive Yazi keybindings & help |

---

# 6. GNU Nano Terminal Editor

## File Management

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + O` | WriteOut (Save active file to disk) |
| `Ctrl + X` | Exit editor (prompts to save if modified) |
| `Ctrl + R` | Read file into current buffer |
| `Alt + F` | Toggle multiple file buffers |
| `Alt + < / >` | Switch to previous / next file buffer |

## Editing & Cutbuffer

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + K` | Cut current line into cutbuffer |
| `Ctrl + U` | Uncut (paste) cutbuffer at cursor position |
| `Alt + 6  (Alt + ^)` | Copy marked text or current line to cutbuffer |
| `Alt + A  (Ctrl + 6)` | Set mark (begin text selection) |
| `Alt + U` | Undo last action |
| `Alt + E` | Redo last undone action |
| `Ctrl + J` | Justify current paragraph |
| `Alt + J` | Justify entire buffer |

## Search & Replace

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + W` | Where Is (search text forward) |
| `Alt + W` | Repeat last search forward (Find next) |
| `Ctrl + \  (Alt + R)` | Search and interactive replace |
| `Alt + Q` | Search backward |

## Navigation & Position

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + Y` | Move up one page (PageUp) |
| `Ctrl + V` | Move down one page (PageDown) |
| `Alt + \  (Alt + |)` | Jump to first line of buffer |
| `Alt + /  (Alt + ?)` | Jump to last line of buffer |
| `Ctrl + _  (Alt + G)` | Go to specific line and column number |
| `Ctrl + C` | Report current cursor line, column, and position |

## Help & Display

| Key Combination | Description |
| :--- | :--- |
| `Ctrl + G` | Display interactive Help menu |
| `Alt + X` | Toggle two-line help key menu at bottom |
| `Alt + C` | Toggle constant cursor position display |
| `Alt + L` | Toggle long line soft-wrapping |
| `Alt + N` | Toggle line numbers display |

---

# 7. Environment Configuration Locations Catalog

## Qtile Core

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `config.py` | `~/.config/qtile/config.py` | `~/Qtile-con/config.py` | Active | 5.7 KB | Primary Qtile entrypoint initializing layouts, widgets, screens, hooks, and keys |
| `qtile_config/settings.py` | `~/.config/qtile/qtile_config/settings.py` | `~/Qtile-con/qtile_config/settings.py` | Active | 3.7 KB | Desktop preferences, gaps, borders, bar dimensions, and 4-layer unified PATH resolution |
| `qtile_config/colors.py` | `~/.config/qtile/qtile_config/colors.py` | `~/Qtile-con/qtile_config/colors.py` | Active | 794 B | Active Catppuccin / selected theme color palette loaded dynamically into Qtile |
| `qtile_config/groups.py` | `~/.config/qtile/qtile_config/groups.py` | `~/Qtile-con/qtile_config/groups.py` | Active | 4.9 KB | Workspace tag definitions (1-9) & automated application class window routing rules |
| `qtile_config/keys.py` | `~/.config/qtile/qtile_config/keys.py` | `~/Qtile-con/qtile_config/keys.py` | Active | 12.2 KB | Keyboard shortcuts, window state management (maximize, minimize, restore), media keys |
| `qtile_config/layouts.py` | `~/.config/qtile/qtile_config/layouts.py` | `~/Qtile-con/qtile_config/layouts.py` | Active | 4.6 KB | Layout collection (Scroller, Columns, Monad, Tile, Matrix, Max, Floating) with borders |
| `qtile_config/scroller.py` | `~/.config/qtile/qtile_config/scroller.py` | `~/Qtile-con/qtile_config/scroller.py` | Active | 32.5 KB | Niri-style smooth scroller horizontal ribbon layout engine with ease-out cubic animation |
| `qtile_config/widgets.py` | `~/.config/qtile/qtile_config/widgets.py` | `~/Qtile-con/qtile_config/widgets.py` | Active | 32.8 KB | Top bar widgets, hardware monitoring capsules, separators, tooltips, and click actions |
| `qtile_config/screens.py` | `~/.config/qtile/qtile_config/screens.py` | `~/Qtile-con/qtile_config/screens.py` | Active | 349 B | Display screen outputs and top bar placement geometry |

## Session & Launchers

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scripts/autostart` | `~/.config/qtile/scripts/autostart` | `~/Qtile-con/scripts/autostart` | Active | 5.5 KB | Session initialization script exporting unified PATH and launching background daemons |
| `scripts/qtile-action` | `~/.config/qtile/scripts/qtile-action` | `~/Qtile-con/scripts/qtile-action` | Active | 15.5 KB | Action dispatcher for launcher, run, volume, wifi, weather, restore, man, witr |
| `scripts/qtile-run` | `~/.config/qtile/scripts/qtile-run` | `~/Qtile-con/scripts/qtile-run` | Active | 3.8 KB | Smart runner executing CLI/TUI utilities in terminal and detaching GUI applications |
| `scripts/keybindings-cheatsheet` | `~/.config/qtile/scripts/keybindings-cheatsheet` | `~/Qtile-con/scripts/keybindings-cheatsheet` | Active | 97.8 KB | Tabbed shortcuts reference palette, cheatsheet, and config file browser |
| `scripts/apply-global-theme` | `~/.config/qtile/scripts/apply-global-theme` | `~/Qtile-con/scripts/apply-global-theme` | Active | 39.1 KB | Multi-app theme compiler synchronizing Qtile, Alacritty, Kitty, Micro, Dunst, and Rofi |
| `scripts/set-theme` | `~/.config/qtile/scripts/set-theme` | `~/Qtile-con/scripts/set-theme` | Active | 1.0 KB | Themed Rofi interactive global theme selector |
| `scripts/set-wallpaper` | `~/.config/qtile/scripts/set-wallpaper` | `~/Qtile-con/scripts/set-wallpaper` | Active | 8.9 KB | 3x3 wallpaper thumbnail preview card grid and dynamic Nerd Font family switcher |
| `scripts/theme_apply.py` | `~/.config/qtile/scripts/theme_apply.py` | `~/Qtile-con/scripts/theme_apply.py` | Active | 972 B | Python theme compiler generating application-specific theme configurations |
| `scripts/wal_to_qtile.py` | `~/.config/qtile/scripts/wal_to_qtile.py` | `~/Qtile-con/scripts/wal_to_qtile.py` | Active | 1.6 KB | Pywal / wallpaper image color palette extractor |

## Widgets & Watchdogs

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scripts/volume-slider` | `~/.config/qtile/scripts/volume-slider` | `~/Qtile-con/scripts/volume-slider` | Active | 8.0 KB | Native floating volume slider popup with percentage presets and audio sink switching |
| `scripts/volume-status` | `~/.config/qtile/scripts/volume-status` | `~/Qtile-con/scripts/volume-status` | Active | 1.2 KB | Real-time audio volume level and mute status provider for the top bar |
| `scripts/wifi-menu` | `~/.config/qtile/scripts/wifi-menu` | `~/Qtile-con/scripts/wifi-menu` | Active | 4.7 KB | Deduplicated Wi-Fi scanner and interactive network connection picker |
| `scripts/wifi-status` | `~/.config/qtile/scripts/wifi-status` | `~/Qtile-con/scripts/wifi-status` | Active | 849 B | Real-time network throughput (download/upload speed) monitor |
| `scripts/weather` | `~/.config/qtile/scripts/weather` | `~/Qtile-con/scripts/weather` | Active | 1.5 KB | Top bar weather widget script reporting current temperature |
| `scripts/weather-forecast` | `~/.config/qtile/scripts/weather-forecast` | `~/Qtile-con/scripts/weather-forecast` | Active | 5.7 KB | Hourly multi-column weather card grid dashboard |
| `scripts/set-weather-location` | `~/.config/qtile/scripts/set-weather-location` | `~/Qtile-con/scripts/set-weather-location` | Active | 1.5 KB | Weather forecast city and location configuration prompt |
| `scripts/battery-status` | `~/.config/qtile/scripts/battery-status` | `~/Qtile-con/scripts/battery-status` | Active | 3.9 KB | Battery health diagnostics and low-power warning notification daemon |
| `scripts/critical-indicators` | `~/.config/qtile/scripts/critical-indicators` | `~/Qtile-con/scripts/critical-indicators` | Active | 4.0 KB | Hardware watchdog alerting on critical CPU, RAM, disk, battery, or thermal limits |
| `scripts/sys-investigate` | `~/.config/qtile/scripts/sys-investigate` | `~/Qtile-con/scripts/sys-investigate` | Active | 27.9 KB | Deep system resource metrics, memory breakdown, and process causation inspector |
| `scripts/process-info` | `~/.config/qtile/scripts/process-info` | `~/Qtile-con/scripts/process-info` | Active | 12.9 KB | Interactive process manager and background daemon tracer |
| `scripts/services-info` | `~/.config/qtile/scripts/services-info` | `~/Qtile-con/scripts/services-info` | Active | 8.4 KB | Systemd user service monitor and interactive service manager |
| `scripts/cockpit-info` | `~/.config/qtile/scripts/cockpit-info` | `~/Qtile-con/scripts/cockpit-info` | Active | 4.2 KB | Cockpit Web Console status, browser launcher, and service control manager |
| `scripts/ai-agents-info` | `~/.config/qtile/scripts/ai-agents-info` | `~/Qtile-con/scripts/ai-agents-info` | Active | 10.2 KB | Active AI agent & LLM daemon process monitor, witr inspection, and management |
| `scripts/snapper-info` | `~/.config/qtile/scripts/snapper-info` | `~/Qtile-con/scripts/snapper-info` | Active | 9.7 KB | Snapper Btrfs snapshot monitor, manual snapshot creation, and immediate rollback menu |

## Input & Security

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `scripts/gesture-daemon` | `~/.config/qtile/scripts/gesture-daemon` | `~/Qtile-con/scripts/gesture-daemon` | Active | 21.8 KB | Native compiled C XInput 2.4 touchpad gesture daemon binary |
| `scripts/gesture-daemon.c` | `~/.config/qtile/scripts/gesture-daemon.c` | `~/Qtile-con/scripts/gesture-daemon.c` | Active | 15.4 KB | Zero-dependency C source code for root window touchpad gesture capture |
| `scripts/setup-gestures` | `~/.config/qtile/scripts/setup-gestures` | `~/Qtile-con/scripts/setup-gestures` | Active | 3.9 KB | Gesture daemon setup and management utility |
| `scripts/clipboard-history` | `~/.config/qtile/scripts/clipboard-history` | `~/Qtile-con/scripts/clipboard-history` | Active | 5.9 KB | Fuzzy clipboard history manager with Greenclip/xclip fallback |
| `scripts/rofi-file-search` | `~/.config/qtile/scripts/rofi-file-search` | `~/Qtile-con/scripts/rofi-file-search` | Active | 12.1 KB | Fast fuzzy file search backend for Rofi launcher tab using fd/fdfind |
| `scripts/rofi-content-search` | `~/.config/qtile/scripts/rofi-content-search` | `~/Qtile-con/scripts/rofi-content-search` | Active | 11.6 KB | Fast content search backend for Rofi launcher tab using ripgrep (rg) |
| `scripts/man-lookup` | `~/.config/qtile/scripts/man-lookup` | `~/Qtile-con/scripts/man-lookup` | Active | 1.4 KB | Fuzzy searchable manual page index and reader in Alacritty |
| `scripts/screenshot` | `~/.config/qtile/scripts/screenshot` | `~/Qtile-con/scripts/screenshot` | Active | 2.0 KB | Maim region and full screen screenshot utility with clipboard copying |
| `scripts/logout-menu` | `~/.config/qtile/scripts/logout-menu` | `~/Qtile-con/scripts/logout-menu` | Active | 1018 B | Themed power session menu (Lock, Logout, Reboot, Poweroff) |
| `scripts/check-config` | `~/.config/qtile/scripts/check-config` | `~/Qtile-con/scripts/check-config` | Active | 763 B | Configuration syntax, typing, and dependency verification script |
| `udev/90-backlight.rules` | `/etc/udev/rules.d/90-backlight.rules` | `~/Qtile-con/udev/90-backlight.rules` | In Repo | 953 B | Udev rules granting video/input groups passwordless backlight control |

## Themes & Menus

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `themes/current_theme.json` | `~/.config/qtile/themes/current_theme.json` | `~/Qtile-con/themes/current_theme.json` | Active | 1.2 KB | Active serialized color palette JSON applied across desktop tools |
| `themes/catppuccin-mocha.json` | `~/.config/qtile/themes/catppuccin-mocha.json` | `~/Qtile-con/themes/catppuccin-mocha.json` | Active | 623 B | Catppuccin Mocha preset (default soothing dark pastel palette) |
| `themes/catppuccin-frappe.json` | `~/.config/qtile/themes/catppuccin-frappe.json` | `~/Qtile-con/themes/catppuccin-frappe.json` | Active | 624 B | Catppuccin Frappé preset palette |
| `themes/catppuccin-latte.json` | `~/.config/qtile/themes/catppuccin-latte.json` | `~/Qtile-con/themes/catppuccin-latte.json` | Active | 623 B | Catppuccin Latte preset light palette |
| `themes/gruvbox-dark.json` | `~/.config/qtile/themes/gruvbox-dark.json` | `~/Qtile-con/themes/gruvbox-dark.json` | Active | 619 B | Gruvbox Dark warm retro groove palette |
| `themes/github-dark.json` | `~/.config/qtile/themes/github-dark.json` | `~/Qtile-con/themes/github-dark.json` | Active | 618 B | GitHub Dark canvas palette |
| `themes/ayu-dark.json` | `~/.config/qtile/themes/ayu-dark.json` | `~/Qtile-con/themes/ayu-dark.json` | Active | 615 B | Ayu Dark high-contrast editor palette |
| `themes/solarized-dark.json` | `~/.config/qtile/themes/solarized-dark.json` | `~/Qtile-con/themes/solarized-dark.json` | Active | 621 B | Solarized Dark cyan/base03 terminal palette |
| `themes/catppuccin-mocha.rasi` | `~/.config/qtile/themes/catppuccin-mocha.rasi` | `~/Qtile-con/themes/catppuccin-mocha.rasi` | Active | 2.1 KB | Primary Rofi menu styling theme |
| `themes/catppuccin-mocha-grid.rasi` | `~/.config/qtile/themes/catppuccin-mocha-grid.rasi` | `~/Qtile-con/themes/catppuccin-mocha-grid.rasi` | Active | 1.8 KB | Rofi 3x3 thumbnail card grid theme for wallpapers |
| `themes/catppuccin-mocha-weather.rasi` | `~/.config/qtile/themes/catppuccin-mocha-weather.rasi` | `~/Qtile-con/themes/catppuccin-mocha-weather.rasi` | Active | 1.7 KB | Rofi multi-column hourly weather card dashboard theme |
| `weather-location` | `~/.config/qtile/weather-location` | `~/Qtile-con/weather-location` | Active | 6 B | Saved weather forecast city file |
| `Pictures/Wallpapers` | `~/Pictures/Wallpapers` | `~/Qtile-con/wallpapers` | Directory | 1.9 KB | Desktop wallpapers collection directory |

## External Integration

| File / Target | Active Location | Source / Fallback | Status | Size | Purpose & Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `alacritty/alacritty.toml` | `~/.config/alacritty/alacritty.toml` | `~/Qtile-con/alacritty/alacritty.toml` | Active | 682 B | Primary GPU terminal emulator configuration |
| `alacritty/catppuccin-mocha.toml` | `~/.config/alacritty/qtile-con-catppuccin-mocha.toml` | `~/Qtile-con/alacritty/catppuccin-mocha.toml` | Active | 515 B | Alacritty dynamic imported theme palette |
| `kitty/kitty.conf` | `~/.config/kitty/kitty.conf` | `~/Qtile-con/kitty/kitty.conf` | Active | 538 B | Secondary terminal emulator configuration |
| `kitty/qtile-theme.conf` | `~/.config/kitty/qtile-theme.conf` | `~/Qtile-con/kitty/qtile-theme.conf` | Active | 861 B | Kitty dynamic imported theme palette |
| `dunst/dunstrc` | `~/.config/dunst/dunstrc` | `~/Qtile-con/dunst/dunstrc` | Active | 1.7 KB | Dunst desktop notification daemon styling and configuration |
| `micro/qtile-theme.micro` | `~/.config/micro/colorschemes/qtile-theme.micro` | `~/Qtile-con/micro/qtile-theme.micro` | Active | 1.3 KB | Micro terminal text editor synchronized color scheme |
| `helix/config.toml` | `~/.config/helix/config.toml` | `~/Qtile-con/helix/config.toml` | Active | 2.1 KB | Helix modern modal text editor configuration |
| `libinput-gestures.conf` | `~/.config/libinput-gestures.conf` | `~/Qtile-con/gestures/libinput-gestures.conf` | Active | 1.2 KB | Fallback touchpad gesture configuration |
| `qtile.desktop` | `/usr/share/xsessions/qtile.desktop` | `~/Qtile-con/qtile.desktop` | Active | 138 B | X11 display manager desktop session entry |
| `install-manifest.json` | `~/.local/share/qtile-con/install-manifest.json` | `~/Qtile-con/.install-manifest.json` | Not Found | 0 B | Automated installer package tracking manifest |
| `witr` | `~/.local/bin/witr` | `~/Qtile-con/bin/witr` | Active | 7.5 MB | Process causation tree tracer binary |
| `.bashrc` | `~/.bashrc` | `~/.bashrc` | Active | 4.4 KB | Interactive user Bash shell configuration and unified PATH export |
| `.profile` | `~/.profile` | `~/.profile` | Active | 664 B | User login session environment profile and PATH configuration |
| `SETTINGS_GUIDE.md` | `~/.config/qtile/SETTINGS_GUIDE.md` | `~/Qtile-con/docs/SETTINGS_GUIDE.md` | Active | 14.5 KB | Comprehensive systems architecture, customization, and settings guide |
| `yazi/yazi.toml` | `~/.config/yazi/yazi.toml` | `~/.config/yazi/yazi.toml` | Active | 266 B | Yazi asynchronous terminal file manager configuration |
| `yazi/theme.toml` | `~/.config/yazi/theme.toml` | `~/.config/yazi/theme.toml` | Active | 93 B | Yazi theme flavor selector configuration |
| `gtk-3.0/settings.ini` | `~/.config/gtk-3.0/settings.ini` | `~/.config/gtk-3.0/settings.ini` | Active | 223 B | GTK3 and Thunar widget/icon theme settings (Tela icon theme) |

