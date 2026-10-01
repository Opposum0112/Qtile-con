"""Workspaces, group labels, and application matching rules (apprules)."""
import re
from libqtile.config import Group, Match

# Define application rules categorized by tag icons:
# 1. 󰈹: Firefox & primary web browsers
# 2. 󰆍: Terminal emulators
# 3. 󰖟: Web development, code editors, and secondary browsers
# 4. 󰙯: Communication, chat, Discord, messenger
# 5. 󰎆: Music, audio, video, and media players
# 6. 󰓓: Steam, gaming platforms, and emulators
# 7. 󰒓: System settings, hardware configuration, and utilities
# 8. 󰉋: File managers and archive utilities
# 9. 󰐃: Graphics, creative design, office, and document viewers
GROUP_RULES = [
    (
        "1",
        "󰈹",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(firefox|firefox-esr|librewolf|waterfox|tor-browser|zen-browser|zen-alpha|mullvad-browser)$"
                )
            ),
        ],
    ),
    (
        "2",
        "󰆍",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(alacritty|kitty|xterm|uxterm|urxvt|rxvt|foot|footclient|wezterm|"
                    r"gnome-terminal|gnome-terminal-server|tilix|terminator|st|st-256color|"
                    r"xfce4-terminal|konsole|lxterminal|ghostty)$"
                )
            ),
        ],
    ),
    (
        "3",
        "󰖟",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(chromium|chromium-browser|google-chrome|brave-browser|microsoft-edge|"
                    r"vivaldi-stable|opera|epiphany|qutebrowser|code|vscodium|sublime_text|atom|"
                    r"geany|kate|jetbrains-.*|emacs|neovide)$"
                )
            ),
        ],
    ),
    (
        "4",
        "󰙯",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(discord|vesktop|webcord|armcord|telegram-desktop|telegramdesktop|"
                    r"slack|signal|element|whatsapp-for-linux|caprine|skype|teams|zoom|"
                    r"thunderbird|hexchat|betterbird)$"
                )
            ),
        ],
    ),
    (
        "5",
        "󰎆",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(spotify|rhythmbox|audacious|clementine|deadbeef|cmus|amberol|"
                    r"strawberry|vlc|mpv|celluloid|parole|totem|kodi|plexamp)$"
                )
            ),
        ],
    ),
    (
        "6",
        "󰓓",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(steam|steamwebhelper|lutris|heroic|prismlauncher|polymc|"
                    r"minecraft-launcher|retroarch|bottles|itch|minigalaxy|rpcs3|pcsx2|"
                    r"dolphin-emu|yuzu|ryujinx)$"
                )
            ),
        ],
    ),
    (
        "7",
        "󰒓",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(pavucontrol|arandr|lxappearance|nitrogen|hardinfo|"
                    r"system-config-printer|blueman-manager|gparted|gpartedbin|timeshift-gtk|"
                    r"baobab|gnome-disks|gnome-disk-utility|bleachbit|kvantummanager|qt5ct|"
                    r"qt6ct|xfce4-settings-manager|lxqt-config|multipass|multipass_gui|multipass\.gui)$"
                )
            ),
        ],
    ),
    (
        "8",
        "󰉋",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(thunar|nemo|nautilus|dolphin|pcmanfm|pcmanfm-qt|caja|spacefm|"
                    r"file-roller|ark|xarchiver|peazip)$"
                )
            ),
        ],
    ),
    (
        "9",
        "󰐃",
        [
            Match(
                wm_class=re.compile(
                    r"(?i)^(gimp.*|inkscape|blender|krita|darktable|rawtherapee|kdenlive|"
                    r"obs|obs-studio|libreoffice.*|soffice.bin|obsidian|evince|zathura|"
                    r"okular|xreader|calibre.*)$"
                )
            ),
        ],
    ),
]

# Independent default layout configuration per workspace group
DEFAULT_GROUP_LAYOUTS = {
    "1": "columns",    # Web browsers: side-by-side / multi-window columns
    "2": "scroller",   # Terminal emulators: smooth horizontal ribbon
    "3": "columns",    # Code & web development: multi-column editor split
    "4": "monadtall",  # Communication / chat: master-stack layout
    "5": "monadtall",  # Media & music: master window with playlist stack
    "6": "max",        # Gaming: maximized single viewport
    "7": "floating",   # System settings & hardware: floating utility dialogs
    "8": "columns",    # File managers: side-by-side file transfer
    "9": "monadwide",  # Graphics & creative design: wide canvas
}

groups = [
    Group(
        name=name,
        label=label,
        matches=matches,
        layout=DEFAULT_GROUP_LAYOUTS.get(name, "scroller"),
    )
    for name, label, matches in GROUP_RULES
]

