"""Native Qtile bar widgets and clickable shell actions."""
import subprocess

from libqtile import widget
from config.colors import COLORS, BG, FG, ACCENT, MUTED
from config.settings import FONT, FONT_SIZE, SCRIPTS, LAUNCHER, TERMINAL


def spawn(*args):
    subprocess.Popen(list(args))


def action(command):
    return {"Button1": lambda: spawn(f"{SCRIPTS}/{command}")}


def build_widgets():
    return [
        widget.TextBox(
            text="  ", foreground=ACCENT, background=BG,
            fontsize=FONT_SIZE + 4, padding=10,
            mouse_callbacks={"Button1": lambda: spawn(*LAUNCHER.split())},
        ),
        widget.GroupBox(
            font=FONT, fontsize=FONT_SIZE, margin_y=6, margin_x=4,
            padding_y=4, padding_x=7, borderwidth=2,
            active=FG, inactive=MUTED, rounded=True,
            highlight_method="line",
            this_current_screen_border=ACCENT,
            this_current_screen=FG,
            other_current_screen_border=COLORS["surface1"],
            urgent_border=COLORS["red"],
            background=BG, disable_drag=True,
        ),
        widget.Spacer(length=8),
        widget.WindowName(font=FONT, fontsize=FONT_SIZE, foreground=FG,
                          background=BG, max_chars=42, empty_group_string="Desktop"),
        widget.Spacer(),
        widget.TextBox(text="󰍛 ", foreground=COLORS["green"], background=BG,
                       mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")}),
        widget.CPU(format="{load_percent}%", foreground=FG, background=BG,
                   update_interval=3,
                   mouse_callbacks={"Button1": lambda: spawn(TERMINAL, "-e", "btop")}),
        widget.TextBox(text="󰘚 ", foreground=COLORS["blue"], background=BG),
        widget.Memory(format="{MemPercent}%", foreground=FG, background=BG, update_interval=5),
        widget.TextBox(text="󰖩 ", foreground=COLORS["teal"], background=BG,
                       mouse_callbacks={"Button1": lambda: spawn("nm-connection-editor")}),
        widget.GenPollText(
            func=lambda: subprocess.run([f"{SCRIPTS}/weather"], capture_output=True,
                                         text=True, timeout=4).stdout.strip() or "Weather unavailable",
            update_interval=900, foreground=FG, background=BG,
            mouse_callbacks={"Button1": lambda: spawn("rofi", "-dmenu", "-p", "Weather location:")},
        ),
        widget.TextBox(text="󰕾 ", foreground=COLORS["peach"], background=BG,
                       mouse_callbacks={"Button1": lambda: spawn("pavucontrol")}),
        widget.Volume(fmt="{volume}%", foreground=FG, background=BG, update_interval=2),
        widget.TextBox(text="󰸉 ", foreground=COLORS["pink"], background=BG,
                       mouse_callbacks=action("set-wallpaper")),
        widget.TextBox(text="󰏘 ", foreground=COLORS["mauve"], background=BG,
                       mouse_callbacks=action("set-theme")),
        widget.Clock(format=" %a %d %b   %H:%M", foreground=ACCENT,
                     background=BG, fontsize=FONT_SIZE, update_interval=30,
                     mouse_callbacks={"Button1": lambda: spawn("gnome-calendar")}),
        widget.Systray(background=BG, padding=8),
        widget.TextBox(text=" ⏻ ", foreground=COLORS["red"], background=BG,
                       mouse_callbacks={"Button1": lambda: spawn("lxsession-logout")}),
    ]
