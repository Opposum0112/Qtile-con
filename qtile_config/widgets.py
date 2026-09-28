"""Native Qtile bar widgets and clickable shell actions."""
import subprocess
from libqtile import widget
from qtile_config.colors import COLORS, BG, FG, ACCENT, MUTED
from qtile_config.settings import FONT, FONT_SIZE, SCRIPTS, LAUNCHER, TERMINAL


def spawn(*args):
    """Launch a command without blocking the Qtile event loop."""
    try:
        subprocess.Popen(list(args), start_new_session=True)
    except OSError:
        return


def action(command):
    return {"Button1": lambda: spawn(f"{SCRIPTS}/{command}")}


def poll_script(name, fallback):
    """Read a status script safely; keep failures from crashing a widget."""
    def poll():
        try:
            result = subprocess.run(
                [f"{SCRIPTS}/{name}"], capture_output=True, text=True,
                timeout=15, check=False,
            )
            value = result.stdout.strip()
            return value if result.returncode == 0 and value else fallback
        except (OSError, subprocess.SubprocessError):
            return fallback
    return poll


def open_audio_mixer():
    try:
        subprocess.Popen(["pavucontrol"], start_new_session=True)
    except OSError:
        try:
            subprocess.Popen(["xterm", "-e", "alsamixer"], start_new_session=True)
        except OSError:
            return


def build_widgets():
    return [
        widget.TextBox(text="  ", foreground=ACCENT, background=BG, fontsize=FONT_SIZE + 4, padding=10, mouse_callbacks={"Button1": lambda: spawn(*LAUNCHER.split())}),
        widget.GroupBox(font=FONT, fontsize=FONT_SIZE, margin_y=6, margin_x=4, padding_y=4, padding_x=7, borderwidth=2, active=FG, inactive=MUTED, rounded=True, highlight_method="line", this_current_screen_border=ACCENT, this_current_screen=FG, other_current_screen_border=COLORS["surface1"], urgent_border=COLORS["red"], background=BG, disable_drag=True),
        widget.Spacer(length=8),
        widget.WindowName(font=FONT, fontsize=FONT_SIZE, foreground=FG, background=BG, max_chars=42, empty_group_string="Desktop"),
        widget.Spacer(),
        widget.TextBox(text="󰍛 ", foreground=COLORS["green"], background=BG, mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")}),
        widget.CPU(format="{load_percent}%", foreground=FG, background=BG, update_interval=3, mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")}),
        widget.TextBox(text="󰘚 ", foreground=COLORS["blue"], background=BG),
        widget.Memory(format="{MemUsed:.0f}/{MemTotal:.0f}M ({MemPercent}%)", foreground=FG, background=BG, update_interval=5),
        widget.TextBox(text="󰖩 ", foreground=COLORS["teal"], background=BG, mouse_callbacks={"Button1": lambda: spawn("nm-connection-editor")}),
        widget.GenPollText(name="weather", func=poll_script("weather", "Weather unavailable"), update_interval=300, foreground=FG, background=BG, mouse_callbacks={"Button1": lambda: spawn(f"{SCRIPTS}/set-weather-location")}),
        widget.GenPollText(func=poll_script("volume-status", "VOL N/A"), update_interval=5, foreground=COLORS["peach"], background=BG, mouse_callbacks={"Button1": open_audio_mixer}),
        widget.TextBox(text="󰸉 ", foreground=COLORS["pink"], background=BG, mouse_callbacks=action("set-wallpaper")),
        widget.TextBox(text="󰏘 ", foreground=COLORS["mauve"], background=BG, mouse_callbacks=action("set-theme")),
        widget.Clock(format=" %a %d %b   %H:%M", foreground=ACCENT, background=BG, fontsize=FONT_SIZE, update_interval=30, mouse_callbacks={"Button1": lambda: spawn("gnome-calendar")}),
        widget.Systray(background=BG, padding=8),
        widget.TextBox(text=" ⏻ ", foreground=COLORS["red"], background=BG, mouse_callbacks=action("logout-menu")),
    ]
