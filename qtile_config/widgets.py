"""Native Qtile bar widgets and clickable shell actions."""
import json
import os
import shlex
import shutil
import subprocess
import time

from libqtile import widget
try:
    from libqtile.widget.decorations import RectDecoration  # type: ignore[import-not-found,import-untyped]
except ImportError:
    try:
        from qtile_extras.widget.decorations import RectDecoration  # type: ignore[import-not-found,import-untyped]
    except ImportError:
        RectDecoration = None  # type: ignore[assignment,misc]
from qtile_config.colors import COLORS, BG, FG, ACCENT, MUTED
from qtile_config.settings import FONT, FONT_SIZE, SCRIPTS, LAUNCHER, TERMINAL

LAYOUT_ICONS = {
    "scroller": "󰨘",
    "columns": "󰕰",
    "monadtall": "󰆍",
    "monadwide": "󰖲",
    "max": "󰍹",
    "tile": "󰕰",
    "matrix": "󰓡",
    "floating": "󰉋",
}


class CurrentLayoutIconOnly(widget.CurrentLayout):
    """Display only the layout icon for the active layout without any layout name text."""

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        self._update_icon()

    def _update_icon(self):
        """Synchronize the icon with the currently viewed workspace's layout."""
        if hasattr(self, "bar") and self.bar and self.bar.screen and self.bar.screen.group:
            grp = self.bar.screen.group
            if hasattr(grp, "current_layout") and grp.current_layout is not None and grp.layouts:
                layout_name = grp.layouts[grp.current_layout].name
                self.text = LAYOUT_ICONS.get(layout_name.lower(), "󰕰")
                self.bar.draw()

    def hook_response(self, layout, group):
        if group.screen is not None and group.screen == self.bar.screen:
            self.text = LAYOUT_ICONS.get(layout.name.lower(), "󰕰")
            self.bar.draw()

    def setup_hooks(self):
        super().setup_hooks()
        from libqtile import hook
        hook.subscribe.setgroup(self._update_icon)

    def remove_hooks(self):
        super().remove_hooks()
        from libqtile import hook
        try:
            hook.unsubscribe.setgroup(self._update_icon)
        except Exception:
            pass


def spawn(*args):
    """Launch a command safely detached with guaranteed UTF-8 locale environment and DISPLAY."""
    try:
        env = os.environ.copy()
        if not env.get("DISPLAY"):
            env["DISPLAY"] = ":0"
        if "utf" not in env.get("LANG", "").lower():
            env["LANG"] = "en_US.UTF-8"
            env["LC_ALL"] = "en_US.UTF-8"
        subprocess.Popen(
            list(args),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            cwd=os.path.expanduser("~"),
            env=env,
        )
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


_GROUP_ID_COUNTER = 0


def show_hover_popup(title, body, nid=9988):
    """Display instantaneous hover popup using dunstify or notify-send."""
    if shutil.which("dunstify"):
        spawn("dunstify", "-r", str(nid), "-u", "low", "-t", "4000", title, body)
    elif shutil.which("notify-send"):
        spawn("notify-send", "-h", f"string:x-canonical-private-synchronous:hover_{nid}", "-u", "low", "-t", "4000", title, body)


def close_hover_popup(nid=9988):
    """Dismiss hover popup when mouse leaves widget."""
    if shutil.which("dunstify"):
        spawn("dunstify", "-C", str(nid))


def pill(item, colour=None, padding=6, margin_x=2):
    """Give a single widget a Catppuccin capsule and consistent spacing."""
    global _GROUP_ID_COUNTER
    _GROUP_ID_COUNTER += 1
    item.padding = padding
    item.margin_x = margin_x
    if RectDecoration is not None:
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


def pill_group(items, colour=None, padding=6, margin_x=2):
    """Enclose multiple consecutive widgets in a single shared Catppuccin pill capsule."""
    global _GROUP_ID_COUNTER
    _GROUP_ID_COUNTER += 1
    gid = _GROUP_ID_COUNTER
    dec_colour = colour or COLORS["surface0"]
    for item in items:
        item.padding = padding
        item.margin_x = 0
        if RectDecoration is not None:
            item.decorations = [
                RectDecoration(
                    colour=dec_colour,
                    radius=10,
                    filled=True,
                    padding_y=3,
                    group=True,
                    group_id=gid,
                )
            ]
    if items:
        items[0].margin_x = margin_x
        items[-1].margin_x = margin_x
    return items


def bar_sep(padding=6):
    """Sleek vertical separator between functional widget pill groups."""
    return widget.Sep(linewidth=1, padding=padding, foreground=COLORS["surface1"], background=BG)


def open_system_monitor():
    """Open interactive system monitor in terminal (btop/htop/top)."""
    spawn(f"{SCRIPTS}/qtile-action", "monitor")


def open_calendar():
    """Open calendar application or display month notification."""
    try:
        if shutil.which("gnome-calendar"):
            spawn("gnome-calendar")
            return
        import calendar
        import datetime
        now = datetime.datetime.now()
        cal_str = calendar.month(now.year, now.month)
        spawn("notify-send", "-a", "Calendar", f"📅 {now.strftime('%B %Y')}", cal_str)
    except OSError:
        return


def autostart_text_and_tooltip(payload):
    """Parse autostart session applications JSON into bar label and hover tooltip."""
    try:
        data = json.loads(payload)
        icon = str(data.get("icon") or "󱓞").strip()
        tooltip = str(data.get("tooltip") or "Autostart details unavailable").strip()
        return icon or "󱓞", tooltip or "Autostart details unavailable"
    except (TypeError, ValueError):
        return "󱓞", "Autostart details unavailable"


class AutostartPollText(widget.GenPollText):
    """Display autostart icon in bar and complete daemon statuses on hover."""

    def poll(self):
        payload = self.func()
        _, tooltip = autostart_text_and_tooltip(payload)
        self.tooltip = tooltip
        return "󱓞"

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󱓞 Autostart Session Applications", self.tooltip, nid=9980)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9980)


def process_text_and_tooltip(payload):
    """Parse process information JSON into bar label and hover tooltip."""
    try:
        data = json.loads(payload)
        summary = str(data.get("summary") or "󰒋 procs").strip()
        tooltip = str(data.get("tooltip") or "").strip()
        return summary or "󰒋 procs", tooltip or "Process details unavailable"
    except (TypeError, ValueError):
        text = str(payload or "").strip()
        return text if text else "󰒋 procs", "Process details unavailable"


class ProcessPollText(widget.GenPollText):
    """Display process icon in bar and complete process details / sub-widget options on hover."""

    def poll(self):
        payload = self.func()
        _, tooltip = process_text_and_tooltip(payload)
        self.tooltip = tooltip
        return "󰒋"

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰒋 Processes & Background Tools", self.tooltip, nid=9981)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9981)


def battery_text_and_tooltip(payload):
    """Parse battery status JSON into bar label and hover tooltip."""
    try:
        data = json.loads(payload)
        text = str(data.get("text") or "󰂎 N/A").strip()
        tooltip = str(data.get("tooltip") or "Battery status unavailable").strip()
        return text, tooltip
    except (TypeError, ValueError):
        return "󰂎 N/A", "Battery status unavailable"


class BatteryPollText(widget.GenPollText):
    """Display battery level, charging state, and health diagnostics."""

    def poll(self):
        payload = self.func()
        text, tooltip = battery_text_and_tooltip(payload)
        self.tooltip = tooltip
        return text

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰁹 Battery & Power", self.tooltip, nid=9983)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9983)


def critical_text_and_tooltip(payload):
    """Parse critical indicators JSON into bar label and warning tooltip."""
    try:
        data = json.loads(payload)
        text = str(data.get("text") or "󰗠 OK").strip()
        tooltip = str(data.get("tooltip") or "System health details unavailable").strip()
        return text, tooltip
    except (TypeError, ValueError):
        return "󰗠 OK", "System health details unavailable"


class CriticalIndicatorsPollText(widget.GenPollText):
    """Display real-time critical system warnings or nominal health status."""

    def poll(self):
        payload = self.func()
        text, tooltip = critical_text_and_tooltip(payload)
        self.tooltip = tooltip
        return text

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰗠 System Health & Diagnostics", self.tooltip, nid=9984)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9984)


def services_text_and_tooltip(payload):
    """Parse session services JSON into bar label and services tooltip."""
    try:
        data = json.loads(payload)
        summary = str(data.get("summary") or "󰒓 0 svcs").strip()
        tooltip = str(data.get("tooltip") or "Session services details unavailable").strip()
        return summary, tooltip
    except (TypeError, ValueError):
        return "󰒓 0 svcs", "Session services details unavailable"


class ServicesPollText(widget.GenPollText):
    """Display services icon in bar and complete services / daemon options on hover."""

    def poll(self):
        payload = self.func()
        _, tooltip = services_text_and_tooltip(payload)
        self.tooltip = tooltip
        return "󰒓"

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰒓 Session Services & Daemons", self.tooltip, nid=9982)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9982)


def cockpit_text_and_tooltip(payload):
    """Parse Cockpit Web Console JSON into bar text and hover tooltip."""
    try:
        data = json.loads(payload)
        summary = str(data.get("summary") or "󰟀 OFF").strip()
        tooltip = str(data.get("tooltip") or "Cockpit Web Console unavailable").strip()
        return summary, tooltip
    except (TypeError, ValueError):
        return "󰟀 OFF", "Cockpit Web Console unavailable"


class CockpitPollText(widget.GenPollText):
    """Display Cockpit web console status and management options."""

    def poll(self):
        payload = self.func()
        text, tooltip = cockpit_text_and_tooltip(payload)
        self.tooltip = tooltip
        return text

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰟀 Cockpit Web Console", self.tooltip, nid=9991)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9991)


def ai_agents_text_and_tooltip(payload):
    """Parse AI Agents JSON into bar text and hover tooltip."""
    try:
        data = json.loads(payload)
        summary = str(data.get("summary") or "󰧑 0").strip()
        tooltip = str(data.get("tooltip") or "AI agents details unavailable").strip()
        return summary, tooltip
    except (TypeError, ValueError):
        return "󰧑 0", "AI agents details unavailable"


class AIAgentsPollText(widget.GenPollText):
    """Display running AI agent count and management options."""

    def poll(self):
        payload = self.func()
        text, tooltip = ai_agents_text_and_tooltip(payload)
        self.tooltip = tooltip
        return text

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰧑 AI Agents Monitor", self.tooltip, nid=9992)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9992)


def snapper_text_and_tooltip(payload):
    """Parse Snapper snapshots JSON into bar text and hover tooltip."""
    try:
        data = json.loads(payload)
        summary = str(data.get("summary") or "󰁯 Snaps").strip()
        tooltip = str(data.get("tooltip") or "Snapper snapshots unavailable").strip()
        return summary, tooltip
    except (TypeError, ValueError):
        return "󰁯 Snaps", "Snapper snapshots unavailable"


class SnapperPollText(widget.GenPollText):
    """Display Snapper snapshot status and immediate rollback menu trigger."""

    def poll(self):
        payload = self.func()
        text, tooltip = snapper_text_and_tooltip(payload)
        self.tooltip = tooltip
        return text

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰁯 Snapper Btrfs Snapshots", self.tooltip, nid=9993)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9993)


class SysAdminWidgetBox(widget.WidgetBox):
    """SysAdmin widget group displaying an icon-only button that expands subwidgets on click."""

    def button_press(self, x, y, button):
        if button == 1:
            self.toggle()
            return
        super().button_press(x, y, button)

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        state = "expanded (subwidgets visible)" if self.box_is_open else "collapsed (click to show subwidgets)"
        show_hover_popup(
            "󰠬 SysAdmin Widget Group",
            f"State: {state}\nLeft-Click: Toggle Cockpit, AI Agents & Snapper subwidgets\nRight-Click: SysAdmin Control Center",
            nid=9990,
        )

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9990)


widget_defaults = dict(
    font=FONT,
    fontsize=FONT_SIZE,
    padding=4,
    foreground=FG,
    background=BG,
)
extension_defaults = widget_defaults.copy()


class WeatherPollText(widget.GenPollText):
    """Show only temperature; update the tooltip with full weather details."""

    def poll(self):
        payload = self.func()
        text, tooltip = weather_text(payload)
        self.tooltip = tooltip
        if text and text != "Weather N/A":
            display = text.lstrip("+")
            icon = "󰖐"
            try:
                data = json.loads(payload)
                cond = str(data.get("condition") or "").lower()
                if "sun" in cond or "clear" in cond or "✨" in cond:
                    icon = "󰖙"
                elif "partly" in cond or "few" in cond:
                    icon = "󰖕"
                elif "rain" in cond or "shower" in cond or "drizzle" in cond:
                    icon = "󰖗"
                elif "thunder" in cond or "storm" in cond:
                    icon = "󰖓"
                elif "snow" in cond or "ice" in cond:
                    icon = "󰖘"
                elif "fog" in cond or "mist" in cond or "haze" in cond or "dust" in cond:
                    icon = "󰖑"
                elif "cloud" in cond or "overcast" in cond:
                    icon = "󰖐"
            except Exception:
                pass
            return f"{icon} {display}"
        return "󰖐 N/A"

    def mouse_enter(self, x, y):
        super().mouse_enter(x, y)
        if hasattr(self, "tooltip") and self.tooltip:
            show_hover_popup("󰖙 Weather & Environment", self.tooltip, nid=9985)

    def mouse_leave(self, x, y):
        super().mouse_leave(x, y)
        close_hover_popup(nid=9985)


def open_audio_mixer():
    if shutil.which("pavucontrol"):
        spawn("pavucontrol")
    else:
        term = TERMINAL
        spawn(term, "-e", "alsamixer")


class WindowTitle(widget.WindowName):
    """Interactive window title supporting single tap (focus/restore) and double tap (maximize/restore)."""

    def __init__(self, **config):
        super().__init__(**config)
        self._last_click_time = 0.0

    def button_press(self, x, y, button):
        now = time.monotonic()
        if button == 1:
            if (now - self._last_click_time) < 0.35:
                # Double tap / double click: toggle maximize
                self._last_click_time = 0.0
                if self.qtile and self.qtile.current_window:
                    self.qtile.current_window.toggle_maximize()
                return
            self._last_click_time = now

            # Single tap: focus active window or restore minimized window if on empty desktop
            if self.qtile:
                win = self.qtile.current_window
                if win and not getattr(win, "minimized", False):
                    win.focus(warp=False)
                    win.bring_to_front()
                elif self.qtile.current_group:
                    minimized = [w for w in self.qtile.current_group.windows if getattr(w, "minimized", False)]
                    if minimized:
                        minimized[-1].minimized = False
                        self.qtile.current_group.focus(minimized[-1], warp=False)
            return

        elif button == 2:  # Middle click / 3-finger tap: toggle minimize
            if self.qtile and self.qtile.current_window:
                self.qtile.current_window.toggle_minimize()
            return

        elif button == 3:  # Right click / 2-finger tap: toggle floating
            if self.qtile and self.qtile.current_window:
                self.qtile.current_window.toggle_floating()
            return

        elif button == 4:  # Scroll up: focus next window
            if self.qtile and self.qtile.current_group:
                self.qtile.current_group.next_window()
            return

        elif button == 5:  # Scroll down: focus prev window
            if self.qtile and self.qtile.current_group:
                self.qtile.current_group.prev_window()
            return

        super().button_press(x, y, button)


class BarSpacer(widget.Spacer):
    """Interactive bar space supporting single tap (restore) and double tap (maximize)."""

    def __init__(self, **config):
        super().__init__(**config)
        self._last_click_time = 0.0

    def button_press(self, x, y, button):
        now = time.monotonic()
        if button == 1:
            if (now - self._last_click_time) < 0.35:
                # Double tap: toggle maximize on active window
                self._last_click_time = 0.0
                if self.qtile and self.qtile.current_window:
                    self.qtile.current_window.toggle_maximize()
                return
            self._last_click_time = now

            # Single tap: restore any minimized window on current workspace
            if self.qtile and self.qtile.current_group:
                minimized = [w for w in self.qtile.current_group.windows if getattr(w, "minimized", False)]
                if minimized:
                    minimized[-1].minimized = False
                    self.qtile.current_group.focus(minimized[-1], warp=False)
            return

        elif button == 3:  # Right click / 2-finger tap: restore all minimized windows
            if self.qtile and self.qtile.current_group:
                minimized = [w for w in self.qtile.current_group.windows if getattr(w, "minimized", False)]
                for w in minimized:
                    w.minimized = False
                if minimized:
                    self.qtile.current_group.focus(minimized[-1], warp=False)
            return

        super().button_press(x, y, button)


def build_widgets():
    return [
        pill(widget.TextBox(
            text="", font=FONT, fontsize=FONT_SIZE + 1,
            foreground=COLORS["teal"], background=BG,
            mouse_callbacks={
                "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "launcher"),
                "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "run"),
            },
        ), COLORS["surface0"], padding=6, margin_x=2),
        widget.GroupBox(
            font=FONT, fontsize=FONT_SIZE, margin_y=4, margin_x=2,
            padding_y=2, padding_x=5, borderwidth=2, active=FG,
            inactive=MUTED, rounded=True, highlight_method="line",
            this_current_screen_border=ACCENT, this_current_screen=FG,
            other_current_screen_border=COLORS["surface1"],
            urgent_border=COLORS["red"], background=BG, disable_drag=True,
        ),
        pill(CurrentLayoutIconOnly(
            font=FONT, fontsize=FONT_SIZE + 1,
            foreground=COLORS["teal"], background=BG,
            mouse_callbacks={
                "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "layout"),
                "Button2": lambda: spawn("qtile", "cmd-obj", "-o", "cmd", "-f", "prev_layout"),
                "Button3": lambda: spawn("qtile", "cmd-obj", "-o", "cmd", "-f", "next_layout"),
            },
        ), padding=6, margin_x=2),
        widget.Spacer(length=4),
        WindowTitle(
            font=FONT, fontsize=FONT_SIZE, foreground=FG, background=BG,
            max_chars=80, empty_group_string="󰍹 Desktop",
        ),
        BarSpacer(),
        bar_sep(),
        # Hardware Resources (CPU + RAM in unified pill capsule)
        *pill_group([
            widget.CPU(
                font=FONT, fontsize=FONT_SIZE,
                format="󰍛 {load_percent:.0f}%", foreground=COLORS["green"], background=BG,
                update_interval=3,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "cpu"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "investigate"),
                },
            ),
            widget.Memory(
                font=FONT, fontsize=FONT_SIZE,
                format="󰘚 {MemUsed:.1f}G",
                measure_mem="G",
                foreground=COLORS["blue"], background=BG, update_interval=5,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "memory"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "investigate"),
                },
            ),
        ], padding=6, margin_x=2),
        bar_sep(),
        # System Autostart, Processes & Services (grouped icons; options & details on hover)
        *pill_group([
            AutostartPollText(
                name="autostart-info",
                font=FONT, fontsize=FONT_SIZE,
                func=poll_script("autostart-info", "󱓞"),
                update_interval=5, foreground=COLORS["peach"], background=BG,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/autostart-info", "--menu"),
                    "Button2": lambda: spawn(f"{SCRIPTS}/autostart-info", "--restart"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/autostart-info", "--edit"),
                },
            ),
            ProcessPollText(
                name="process-info",
                font=FONT, fontsize=FONT_SIZE,
                func=poll_script("process-info", "󰒋 procs"),
                update_interval=3, foreground=COLORS["lavender"], background=BG,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/process-info", "--background"),
                    "Button2": lambda: spawn(f"{SCRIPTS}/process-info", "--terminate"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/process-info", "--terminate"),
                },
            ),
            ServicesPollText(
                name="services-info",
                font=FONT, fontsize=FONT_SIZE,
                func=poll_script("services-info", "󰒓 0 svcs"),
                update_interval=5, foreground=COLORS["sapphire"], background=BG,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/services-info", "--menu"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/sys-investigate", "--services"),
                },
            ),
        ], padding=6, margin_x=2),
        bar_sep(),
        # SysAdmin Widget Group (only icon widget initially, expands subwidgets on click)
        pill(SysAdminWidgetBox(
            name="sysadmin-box",
            font=FONT, fontsize=FONT_SIZE + 1,
            foreground=COLORS["peach"], background=BG,
            text_closed="󰠬",
            text_open="󰠬 ",
            start_opened=False,
            close_button_location="left",
            widgets=pill_group([
                CockpitPollText(
                    name="cockpit-info",
                    font=FONT, fontsize=FONT_SIZE,
                    func=poll_script("cockpit-info", '{"summary": "󰟀 OFF", "tooltip": "Cockpit Web Console unavailable"}'),
                    update_interval=5, foreground=COLORS["teal"], background=BG,
                    mouse_callbacks={
                        "Button1": lambda: spawn(f"{SCRIPTS}/cockpit-info", "--open"),
                        "Button3": lambda: spawn(f"{SCRIPTS}/cockpit-info", "--menu"),
                    },
                ),
                AIAgentsPollText(
                    name="ai-agents-info",
                    font=FONT, fontsize=FONT_SIZE,
                    func=poll_script("ai-agents-info", '{"summary": "󰧑 0", "tooltip": "No AI agents running"}'),
                    update_interval=3, foreground=COLORS["mauve"], background=BG,
                    mouse_callbacks={
                        "Button1": lambda: spawn(f"{SCRIPTS}/ai-agents-info", "--menu"),
                        "Button3": lambda: spawn(f"{SCRIPTS}/ai-agents-info", "--menu"),
                    },
                ),
                SnapperPollText(
                    name="snapper-info",
                    font=FONT, fontsize=FONT_SIZE,
                    func=poll_script("snapper-info", '{"summary": "󰁯 Snaps", "tooltip": "Snapper snapshots unavailable"}'),
                    update_interval=10, foreground=COLORS["sapphire"], background=BG,
                    mouse_callbacks={
                        "Button1": lambda: spawn(f"{SCRIPTS}/snapper-info", "--rollback-menu"),
                        "Button3": lambda: spawn(f"{SCRIPTS}/snapper-info", "--create"),
                    },
                ),
            ], colour=COLORS["surface0"]),
            mouse_callbacks={
                "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "sysadmin"),
            },
        ), padding=6, margin_x=2),
        bar_sep(),
        # Health & Power (Battery + Critical Indicators in unified pill capsule)
        *pill_group([
            BatteryPollText(
                name="battery-status",
                font=FONT, fontsize=FONT_SIZE,
                func=poll_script("battery-status", "󰁹 100%"),
                update_interval=10, foreground=COLORS["yellow"], background=BG,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/battery-status", "--info"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "investigate"),
                },
            ),
            CriticalIndicatorsPollText(
                name="critical-indicators",
                font=FONT, fontsize=FONT_SIZE,
                func=poll_script("critical-indicators", "󰗠 OK"),
                update_interval=4, foreground=COLORS["teal"], background=BG,
                mouse_callbacks={
                    "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "investigate"),
                    "Button3": lambda: spawn(f"{SCRIPTS}/qtile-action", "monitor", "investigate"),
                },
            ),
        ], padding=6, margin_x=2),
        bar_sep(),
        # Network
        pill(widget.Net(
            font=FONT, fontsize=FONT_SIZE,
            format="󰖩 ↓{down:.0f}{down_suffix} ↑{up:.0f}{up_suffix}",
            prefix="k",
            update_interval=2,
            foreground=COLORS["teal"],
            background=BG,
            mouse_callbacks={
                "Button1": lambda: spawn(f"{SCRIPTS}/wifi-menu"),
                "Button3": lambda: spawn("nm-connection-editor"),
            },
        ), padding=6, margin_x=2),
        # Weather
        pill(WeatherPollText(
            name="weather",
            font=FONT, fontsize=FONT_SIZE,
            func=poll_script("weather", "{}"),
            update_interval=300, foreground=FG, background=BG,
            mouse_callbacks={
                "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "weather"),
                "Button3": lambda: spawn(f"{SCRIPTS}/set-weather-location"),
            },
        ), COLORS["surface1"], padding=8, margin_x=3),
        bar_sep(),
        # Volume
        pill(widget.GenPollText(
            name="volume-status",
            font=FONT, fontsize=FONT_SIZE,
            func=poll_script("volume-status", "󰝟 N/A"),
            update_interval=4,
            foreground=COLORS["peach"],
            background=BG,
            mouse_callbacks={
                "Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "slider"),
                "Button2": lambda: spawn("pamixer", "--toggle-mute"),
                "Button3": lambda: spawn(f"{SCRIPTS}/volume-menu"),
                "Button4": lambda: spawn("pamixer", "--increase", "5"),
                "Button5": lambda: spawn("pamixer", "--decrease", "5"),
            },
        ), padding=6, margin_x=2),
        bar_sep(),
        # Quick Actions (grouped 4-icon dock in unified pill capsule)
        *pill_group([
            widget.TextBox(
                text="󰈙", font=FONT, fontsize=FONT_SIZE, foreground=COLORS["yellow"], background=BG,
                mouse_callbacks={"Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "man")},
            ),
            widget.TextBox(
                text="󰸉", font=FONT, fontsize=FONT_SIZE, foreground=COLORS["pink"], background=BG,
                mouse_callbacks=action("set-wallpaper"),
            ),
            widget.TextBox(
                text="󰏘", font=FONT, fontsize=FONT_SIZE, foreground=COLORS["mauve"], background=BG,
                mouse_callbacks=action("set-theme"),
            ),
            widget.TextBox(
                text="󰅍", font=FONT, fontsize=FONT_SIZE, foreground=COLORS["sapphire"], background=BG,
                mouse_callbacks={"Button1": lambda: spawn(f"{SCRIPTS}/qtile-action", "clipboard")},
            ),
        ], padding=6, margin_x=2),
        bar_sep(),
        # Clock
        pill(widget.Clock(
            font=FONT, fontsize=FONT_SIZE,
            format=" %a %d %b   %H:%M", foreground=COLORS["peach"],
            background=BG, update_interval=30,
            mouse_callbacks={"Button1": open_calendar},
        ), COLORS["surface1"], padding=6, margin_x=2),
        widget.Systray(background=BG, padding=4),
        pill(widget.TextBox(
            text="⏻", font=FONT, fontsize=FONT_SIZE, foreground=COLORS["red"], background=BG,
            mouse_callbacks=action("logout-menu"),
        ), padding=6, margin_x=2),
    ]
