"""Native Qtile bar widgets and clickable shell actions."""
import json
import subprocess

from libqtile import widget
from libqtile.widget.decorations import RectDecoration
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


def weather_text(payload):
    """Return compact bar text and a useful hover tooltip from weather JSON."""
    try:
        data = json.loads(payload)
        temperature = str(data.get("temperature") or "").strip()
        location = str(data.get("location") or "Unknown location").strip()
        if not temperature:
            return "Weather N/A", "Weather details unavailable"
        details = [
            location,
            str(data.get("condition") or "").strip(),
            f"Feels like {data.get('feels_like')}" if data.get("feels_like") else "",
            f"Humidity {data.get('humidity')}" if data.get("humidity") else "",
            f"Wind {data.get('wind')}" if data.get("wind") else "",
        ]
        return temperature, "\n".join(part for part in details if part)
    except (TypeError, ValueError):
        return "Weather N/A", "Weather details unavailable"


class WeatherPollText(widget.GenPollText):
    """Show only temperature; update the tooltip with full weather details."""

    def poll(self):
        payload = self.func()
        text, tooltip = weather_text(payload)
        self.tooltip = tooltip
        return text


def pill(item, colour=None):
    """Give a widget a small Catppuccin capsule and consistent spacing."""
    item.padding = 8
    item.margin_x = 3
    item.decorations = [
        RectDecoration(
            colour=colour or COLORS["surface0"],
            radius=10,
            filled=True,
            padding_y=3,
            group=False,
        )
    ]
    return item


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
        pill(widget.TextBox(
            text="  ", foreground=ACCENT, background=BG,
            fontsize=FONT_SIZE + 4,
            mouse_callbacks={"Button1": lambda: spawn(*LAUNCHER.split())},
        ), COLORS["surface0"]),
        widget.GroupBox(
            font=FONT, fontsize=FONT_SIZE, margin_y=6, margin_x=4,
            padding_y=4, padding_x=7, borderwidth=2, active=FG,
            inactive=MUTED, rounded=True, highlight_method="line",
            this_current_screen_border=ACCENT, this_current_screen=FG,
            other_current_screen_border=COLORS["surface1"],
            urgent_border=COLORS["red"], background=BG, disable_drag=True,
        ),
        widget.Spacer(length=8),
        widget.WindowName(
            font=FONT, fontsize=FONT_SIZE, foreground=FG, background=BG,
            max_chars=42, empty_group_string="Desktop",
        ),
        widget.Spacer(),
        pill(widget.TextBox(
            text="󰍛 ", foreground=COLORS["green"], background=BG,
            mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")},
        )),
        pill(widget.CPU(
            format="{load_percent}%", foreground=FG, background=BG,
            update_interval=3,
            mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")},
        )),
        pill(widget.TextBox(text="󰘚 ", foreground=COLORS["blue"], background=BG)),
        pill(widget.Memory(
            format="{MemUsed:.0f}/{MemTotal:.0f}M ({MemPercent}%)",
            foreground=FG, background=BG, update_interval=5,
        )),
        pill(widget.TextBox(
            text="󰖩 ", foreground=COLORS["teal"], background=BG,
            mouse_callbacks={"Button1": lambda: spawn("nm-connection-editor")},
        )),
        pill(WeatherPollText(
            name="weather", func=poll_script("weather", "{}"),
            update_interval=300, foreground=FG, background=BG,
            mouse_callbacks={"Button1": lambda: spawn(f"{SCRIPTS}/set-weather-location")},
        ), COLORS["surface1"]),
        pill(widget.GenPollText(
            func=poll_script("volume-status", "VOL N/A"),
            update_interval=5, foreground=COLORS["peach"], background=BG,
            mouse_callbacks={"Button1": open_audio_mixer},
        )),
        pill(widget.TextBox(
            text="󰸉 ", foreground=COLORS["pink"], background=BG,
            mouse_callbacks=action("set-wallpaper"),
        )),
        pill(widget.TextBox(
            text="󰏘 ", foreground=COLORS["mauve"], background=BG,
            mouse_callbacks=action("set-theme"),
        )),
        pill(widget.Clock(
            format=" %a %d %b   %H:%M", foreground=ACCENT,
            background=BG, fontsize=FONT_SIZE, update_interval=30,
            mouse_callbacks={"Button1": lambda: spawn("gnome-calendar")},
        ), COLORS["surface1"]),
        widget.Systray(background=BG, padding=8),
        pill(widget.TextBox(
            text=" ⏻ ", foreground=COLORS["red"], background=BG,
            mouse_callbacks=action("logout-menu"),
        )),
    ]
