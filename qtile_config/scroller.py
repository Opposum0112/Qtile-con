"""Niri-style infinite horizontal ribbon / smooth scroller layout for Qtile.

Windows/columns are arranged side-by-side along an infinite horizontal strip.
Moving focus between columns smoothly pans the viewport with ease-out cubic
interpolation, keeping the active column centered or comfortably in view.
"""
from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Sequence

from libqtile.command.base import expose_command
from libqtile.config import ScreenRect
from libqtile.layout.base import Layout, _ClientList

if TYPE_CHECKING:
    from typing_extensions import Self
    from libqtile.backend.base import Window
    from libqtile.group import _Group


class _Column(_ClientList):
    """A vertical column of windows along the ribbon."""

    cw = _ClientList.current_client
    current = _ClientList.current_index

    def __init__(self, split: bool = True, width_ratio: float = 0.5) -> None:
        super().__init__()
        self.split = split
        self.width_ratio = width_ratio
        self.heights: dict[Any, int] = {}

    def toggle_split(self) -> None:
        self.split = not self.split

    def add_client(
        self, client: Window, offset_to_current: int = 1, client_position: str | None = None
    ) -> None:
        super().add_client(client, offset_to_current=offset_to_current, client_position=client_position)
        self.heights[client] = 100
        self._normalize_heights()

    def remove(self, client: Window) -> Window | None:
        ret = super().remove(client)
        if client in self.heights:
            del self.heights[client]
        self._normalize_heights()
        return ret

    def _normalize_heights(self) -> None:
        count = len(self.clients)
        if count == 0:
            return
        base = 100 // count
        rem = 100 % count
        for idx, c in enumerate(self.clients):
            self.heights[c] = base + (1 if idx < rem else 0)

    @expose_command()
    def info(self) -> dict[str, Any]:
        info = super().info()
        info.update({
            "split": self.split,
            "width_ratio": self.width_ratio,
            "heights": [self.heights.get(c, 100) for c in self.clients],
        })
        return info


class Scroller(Layout):
    """Niri-style smooth scrolling horizontal ribbon layout for Qtile."""

    defaults = [
        ("border_focus", "#cba6f7", "Border colour(s) for the focused window."),
        ("border_normal", "#313244", "Border colour(s) for un-focused windows."),
        ("border_focus_stack", "#cba6f7", "Border colour(s) for focused window in stacked columns."),
        ("border_normal_stack", "#313244", "Border colour(s) for un-focused windows in stacked columns."),
        ("border_width", 2, "Border width."),
        ("single_border_width", None, "Border width for single window."),
        ("border_on_single", True, "Draw a border when there is only one window."),
        ("margin", 4, "Margin of the layout (int or list of ints [N E S W])."),
        ("margin_on_single", None, "Margin when only one window."),
        ("default_width", 0.5, "Default column width as fraction of screen width."),
        ("min_column_width", 200, "Minimum column width in pixels."),
        ("preset_widths", [0.333333, 0.5, 0.666667, 1.0], "Preset width fractions for cycle_width."),
        ("width_step", 0.05, "Step fraction for grow_width and shrink_width."),
        ("center_focused", "on-overflow", "Centering mode: 'always', 'on-overflow', or 'never'."),
        ("scroll_clamp", False, "Clamp scroll offset to ribbon edges."),
        ("new_window_as_column", True, "Whether new windows create a new column (Niri style)."),
        ("split", True, "Whether columns with multiple windows tile vertically by default."),
        ("wrap_focus_columns", True, "Wrap around when moving focus across columns."),
        ("wrap_focus_rows", True, "Wrap around when moving focus across rows."),
        ("animate", True, "Smooth animated horizontal scrolling."),
        ("animation_duration", 0.22, "Animation duration in seconds."),
        ("animation_fps", 60, "Target frame rate for animation."),
    ]

    def __init__(self, **config: Any) -> None:
        super().__init__(**config)
        self.add_defaults(Scroller.defaults)
        self.columns: list[_Column] = []
        self.current_col_idx: int = 0
        self.scroll_offset: float = 0.0
        self.target_scroll_offset: float = 0.0
        self._anim_timer: Any = None
        self._anim_start_offset: float = 0.0
        self._anim_start_time: float = 0.0
        self._last_screen_rect: ScreenRect | None = None

    @property
    def has_group(self) -> bool:
        """Safely check if layout is currently attached to a group."""
        return getattr(self, "_group", None) is not None

    def _focus_group_client(self, client: Window) -> None:
        if self.has_group and client is not None:
            try:
                self.group.focus(client, True)
            except Exception:
                pass

    def _layout_group(self, focus: bool = False) -> None:
        if self.has_group:
            try:
                self.group.layout_all(focus=focus)
            except Exception:
                pass

    def clone(self, group: _Group) -> Self:
        c = super().clone(group)
        c.columns = []
        c.current_col_idx = 0
        c.scroll_offset = 0.0
        c.target_scroll_offset = 0.0
        c._anim_timer = None
        c._anim_start_offset = 0.0
        c._anim_start_time = 0.0
        c._last_screen_rect = None
        return c

    @property
    def current_column(self) -> _Column | None:
        if 0 <= self.current_col_idx < len(self.columns):
            return self.columns[self.current_col_idx]
        return None

    @property
    def current_window(self) -> Window | None:
        col = self.current_column
        return col.cw if col else None

    def _get_column_for_client(self, client: Window) -> tuple[int, _Column] | tuple[None, None]:
        for idx, col in enumerate(self.columns):
            if client in col:
                return idx, col
        return None, None

    def get_windows(self) -> list[Window]:
        wins: list[Window] = []
        for col in self.columns:
            wins.extend(col.clients)
        return wins

    def add_client(self, client: Window) -> None:
        if not self.columns:
            col = _Column(split=self.split, width_ratio=self.default_width)
            col.add_client(client)
            self.columns.append(col)
            self.current_col_idx = 0
            self.scroll_to_focused(animate=False)
            return

        cur_col = self.current_column
        if cur_col is None or len(cur_col) == 0:
            if cur_col is None:
                cur_col = _Column(split=self.split, width_ratio=self.default_width)
                self.columns.append(cur_col)
                self.current_col_idx = len(self.columns) - 1
            cur_col.add_client(client)
        elif self.new_window_as_column:
            new_col = _Column(split=self.split, width_ratio=self.default_width)
            new_col.add_client(client)
            insert_idx = self.current_col_idx + 1
            self.columns.insert(insert_idx, new_col)
            self.current_col_idx = insert_idx
        else:
            cur_col.add_client(client)

        self.scroll_to_focused(animate=self.animate)

    def remove(self, client: Window) -> Window | None:
        col_idx, found_col = self._get_column_for_client(client)
        if found_col is None or col_idx is None:
            return None

        found_col.remove(client)
        if len(found_col) == 0 and len(self.columns) > 1:
            self.columns.pop(col_idx)
            if self.current_col_idx >= len(self.columns):
                self.current_col_idx = len(self.columns) - 1
            elif col_idx < self.current_col_idx:
                self.current_col_idx -= 1
        elif len(found_col) == 0 and len(self.columns) == 1:
            self.columns = []
            self.current_col_idx = 0
            return None

        col = self.current_column
        cw = col.cw if col else None
        self.scroll_to_focused(animate=self.animate)
        return cw

    def focus(self, client: Window) -> None:
        col_idx, found_col = self._get_column_for_client(client)
        if found_col is not None and col_idx is not None:
            self.current_col_idx = col_idx
            found_col.focus(client)
            self.scroll_to_focused(animate=self.animate)

    def _is_client_active(self, client: Window) -> bool:
        """Check if client is active and tiled (not minimized)."""
        return getattr(client, "minimized", False) is not True

    def _get_active_columns(self) -> list[tuple[int, _Column]]:
        """Return columns that contain at least one non-minimized tiled window."""
        active: list[tuple[int, _Column]] = []
        for idx, col in enumerate(self.columns):
            if any(self._is_client_active(c) for c in col.clients):
                active.append((idx, col))
        return active

    def focus_first(self) -> Window | None:
        for col in self.columns:
            for w in col.clients:
                if self._is_client_active(w):
                    return w
        return None

    def focus_last(self) -> Window | None:
        for col in reversed(self.columns):
            for w in reversed(col.clients):
                if self._is_client_active(w):
                    return w
        return None

    def focus_next(self, win: Window) -> Window | None:
        col_idx, found_col = self._get_column_for_client(win)
        if found_col is None or col_idx is None:
            return None
        next_in_col = found_col.focus_next(win)
        while next_in_col is not None and not self._is_client_active(next_in_col):
            next_in_col = found_col.focus_next(next_in_col)
        if next_in_col is not None:
            return next_in_col
        for next_ci in range(col_idx + 1, len(self.columns)):
            for w in self.columns[next_ci].clients:
                if self._is_client_active(w):
                    return w
        if self.wrap_focus_columns and len(self.columns) > 1:
            return self.focus_first()
        return None

    def focus_previous(self, win: Window) -> Window | None:
        col_idx, found_col = self._get_column_for_client(win)
        if found_col is None or col_idx is None:
            return None
        prev_in_col = found_col.focus_previous(win)
        while prev_in_col is not None and not self._is_client_active(prev_in_col):
            prev_in_col = found_col.focus_previous(prev_in_col)
        if prev_in_col is not None:
            return prev_in_col
        for prev_ci in range(col_idx - 1, -1, -1):
            for w in reversed(self.columns[prev_ci].clients):
                if self._is_client_active(w):
                    return w
        if self.wrap_focus_columns and len(self.columns) > 1:
            return self.focus_last()
        return None

    def next(self) -> None:
        cur = self.current_window
        target = self.focus_next(cur) if cur else self.focus_first()
        if target:
            self._focus_group_client(target)

    def previous(self) -> None:
        cur = self.current_window
        target = self.focus_previous(cur) if cur else self.focus_last()
        if target:
            self._focus_group_client(target)

    def _calculate_target_scroll_offset(
        self, screen_width: int, force_center: bool = False
    ) -> float:
        active_cols = self._get_active_columns()
        if not active_cols:
            return 0.0

        widths = [
            max(self.min_column_width, int(round(col.width_ratio * screen_width)))
            for _, col in active_cols
        ]
        total_width = sum(widths)

        curr_col = self.current_column
        active_col_objs = [col for _, col in active_cols]
        if curr_col in active_col_objs:
            curr_idx = active_col_objs.index(curr_col)
        else:
            curr_idx = min(self.current_col_idx, len(active_cols) - 1)

        curr_x = sum(widths[:curr_idx])
        curr_w = widths[curr_idx]

        mode = "always" if force_center else self.center_focused
        if isinstance(mode, bool):
            mode = "always" if mode else "never"

        if mode == "always":
            target = curr_x + (curr_w / 2.0) - (screen_width / 2.0)
            if self.scroll_clamp:
                if total_width >= screen_width:
                    target = max(0.0, min(float(total_width - screen_width), target))
                else:
                    target = -(screen_width - total_width) / 2.0
            return float(target)

        if mode == "on-overflow":
            if total_width <= screen_width:
                # If only 1 column, center it; otherwise align smoothly from 0
                if len(active_cols) == 1:
                    return float(-(screen_width - total_width) / 2.0)
                return 0.0
            target = curr_x + (curr_w / 2.0) - (screen_width / 2.0)
            if self.scroll_clamp:
                target = max(0.0, min(float(total_width - screen_width), target))
            return float(target)

        # mode == "never"
        left_on_screen = curr_x - self.scroll_offset
        right_on_screen = curr_x + curr_w - self.scroll_offset
        if left_on_screen < 0:
            target = float(curr_x)
        elif right_on_screen > screen_width:
            target = float(curr_x + curr_w - screen_width)
        else:
            target = self.scroll_offset

        if self.scroll_clamp and total_width >= screen_width:
            target = max(0.0, min(float(total_width - screen_width), target))
        return float(target)

    def scroll_to_focused(self, animate: bool = True, force_center: bool = False) -> None:
        screen_w = 1920
        if self._last_screen_rect:
            screen_w = self._last_screen_rect.width
        elif self.has_group and getattr(self.group, "screen", None):
            screen_w = self.group.screen.width

        self.target_scroll_offset = self._calculate_target_scroll_offset(screen_w, force_center=force_center)

        # Skip animation if disabled, in headless test, or no event loop
        qtile = getattr(self.group, "qtile", None) if self.has_group else None
        if not self.animate or not animate or qtile is None or getattr(qtile, "testing", False):
            self.scroll_offset = self.target_scroll_offset
            self._layout_group(focus=False)
            return

        if abs(self.target_scroll_offset - self.scroll_offset) < 1.0:
            self.scroll_offset = self.target_scroll_offset
            return

        if self._anim_timer is not None:
            try:
                self._anim_timer.cancel()
            except Exception:
                pass
            self._anim_timer = None

        self._anim_start_offset = self.scroll_offset
        self._anim_start_time = time.monotonic()
        frame_interval = 1.0 / max(10, self.animation_fps)
        self._anim_timer = qtile.call_later(
            frame_interval,
            self._step_animation,
            self._anim_start_offset,
            self.target_scroll_offset,
            self._anim_start_time,
            self.animation_duration,
        )

    def _step_animation(
        self, start_offset: float, target_offset: float, start_time: float, duration: float
    ) -> None:
        if target_offset != self.target_scroll_offset:
            return
        now = time.monotonic()
        elapsed = now - start_time
        progress = min(1.0, elapsed / max(0.01, duration))
        # Ease-out cubic: 1 - (1 - t)^3
        t = 1.0 - ((1.0 - progress) ** 3)
        self.scroll_offset = start_offset + (target_offset - start_offset) * t

        self._layout_group(focus=False)

        qtile = getattr(self.group, "qtile", None) if self.has_group else None
        if progress < 1.0 and qtile is not None:
            frame_interval = 1.0 / max(10, self.animation_fps)
            self._anim_timer = qtile.call_later(
                frame_interval,
                self._step_animation,
                start_offset,
                target_offset,
                start_time,
                duration,
            )
        else:
            self.scroll_offset = target_offset
            self._anim_timer = None
            self._layout_group(focus=False)

    def layout(self, windows: Sequence[Window], screen_rect: ScreenRect) -> None:
        self._last_screen_rect = screen_rect
        for w in windows:
            if getattr(w, "minimized", False) is not True:
                self.configure(w, screen_rect)

    def configure(self, client: Window, screen_rect: ScreenRect) -> None:
        self._last_screen_rect = screen_rect
        if not self._is_client_active(client):
            client.hide()
            return

        col_idx, col = self._get_column_for_client(client)
        if col is None or col_idx is None:
            client.hide()
            return

        active_cols = self._get_active_columns()
        active_col_objs = [c for _, c in active_cols]
        if col not in active_col_objs:
            client.hide()
            return

        active_col_idx = active_col_objs.index(col)
        widths = [
            max(self.min_column_width, int(round(c.width_ratio * screen_rect.width)))
            for c in active_col_objs
        ]
        col_w = widths[active_col_idx]
        col_x_ribbon = sum(widths[:active_col_idx])
        col_x_screen = screen_rect.x + int(round(col_x_ribbon - self.scroll_offset))

        # Check visibility relative to viewport
        screen_end = screen_rect.x + screen_rect.width
        # Windows way offscreen (more than 1 screen width away) are hidden to save resources
        if (col_x_screen + col_w < screen_rect.x - screen_rect.width) or (col_x_screen > screen_end + screen_rect.width):
            client.hide()
            return

        is_focused = (client == self.current_window)
        if is_focused:
            color = self.border_focus if col.split else self.border_focus_stack
        else:
            color = self.border_normal if col.split else self.border_normal_stack

        active_in_col = [c for c in col.clients if self._is_client_active(c)]
        is_single = len(active_cols) == 1 and (len(active_in_col) == 1 or not col.split)
        border = (
            self.single_border_width
            if (is_single and self.single_border_width is not None)
            else (self.border_width if (not is_single or self.border_on_single) else 0)
        )
        margin_size = (
            self.margin_on_single
            if (is_single and self.margin_on_single is not None)
            else self.margin
        )

        if col.split:
            if not active_in_col or client not in active_in_col:
                client.hide()
                return

            num_clients = len(active_in_col)
            win_idx = active_in_col.index(client)

            base_h = screen_rect.height // max(1, num_clients)
            rem = screen_rect.height % max(1, num_clients)
            y_offset = 0
            for idx in range(win_idx):
                y_offset += base_h + (1 if idx < rem else 0)

            win_h = base_h + (1 if win_idx < rem else 0)
            client.place(
                col_x_screen,
                screen_rect.y + y_offset,
                col_w - 2 * border,
                win_h - 2 * border,
                border,
                color,
                margin=margin_size,
            )
            client.unhide()
        elif client == col.cw:
            client.place(
                col_x_screen,
                screen_rect.y,
                col_w - 2 * border,
                screen_rect.height - 2 * border,
                border,
                color,
                margin=margin_size,
            )
            client.unhide()
        else:
            client.hide()

    def hide(self) -> None:
        if self._anim_timer is not None:
            try:
                self._anim_timer.cancel()
            except Exception:
                pass
            self._anim_timer = None
        for col in self.columns:
            for c in col:
                c.hide()

    def show(self, screen_rect: ScreenRect) -> None:
        self._last_screen_rect = screen_rect
        self._layout_group(focus=False)

    # Exposed navigation & manipulation commands

    @expose_command()
    def left(self) -> None:
        """Focus column to the left."""
        if not self.columns:
            return
        if self.current_col_idx > 0:
            self.current_col_idx -= 1
        elif self.wrap_focus_columns and len(self.columns) > 1:
            self.current_col_idx = len(self.columns) - 1
        else:
            return

        cw = self.current_window
        if cw:
            self._focus_group_client(cw)
        self.scroll_to_focused(animate=self.animate)

    @expose_command()
    def right(self) -> None:
        """Focus column to the right."""
        if not self.columns:
            return
        if self.current_col_idx + 1 < len(self.columns):
            self.current_col_idx += 1
        elif self.wrap_focus_columns and len(self.columns) > 1:
            self.current_col_idx = 0
        else:
            return

        cw = self.current_window
        if cw:
            self._focus_group_client(cw)
        self.scroll_to_focused(animate=self.animate)

    @expose_command()
    def up(self) -> None:
        """Focus window above in current column."""
        col = self.current_column
        if not col or len(col) <= 1:
            return
        if self.wrap_focus_rows:
            col.current_index = (col.current_index - 1) % len(col)
        elif col.current_index > 0:
            col.current_index -= 1
        cw = col.cw
        if cw:
            self._focus_group_client(cw)

    @expose_command()
    def down(self) -> None:
        """Focus window below in current column."""
        col = self.current_column
        if not col or len(col) <= 1:
            return
        if self.wrap_focus_rows:
            col.current_index = (col.current_index + 1) % len(col)
        elif col.current_index + 1 < len(col):
            col.current_index += 1
        cw = col.cw
        if cw:
            self._focus_group_client(cw)

    @expose_command()
    def shuffle_left(self) -> None:
        """Swap active column with column on the left."""
        if len(self.columns) <= 1 or self.current_col_idx <= 0:
            return
        idx = self.current_col_idx
        self.columns[idx], self.columns[idx - 1] = self.columns[idx - 1], self.columns[idx]
        self.current_col_idx -= 1
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def shuffle_right(self) -> None:
        """Swap active column with column on the right."""
        if len(self.columns) <= 1 or self.current_col_idx + 1 >= len(self.columns):
            return
        idx = self.current_col_idx
        self.columns[idx], self.columns[idx + 1] = self.columns[idx + 1], self.columns[idx]
        self.current_col_idx += 1
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def shuffle_up(self) -> None:
        """Swap active window up within the current column."""
        col = self.current_column
        if not col or len(col) <= 1:
            return
        col.shuffle_up()
        self._layout_group(focus=False)

    @expose_command()
    def shuffle_down(self) -> None:
        """Swap active window down within the current column."""
        col = self.current_column
        if not col or len(col) <= 1:
            return
        col.shuffle_down()
        self._layout_group(focus=False)

    @expose_command()
    def grow_width(self, step: float | None = None) -> None:
        """Increase the active column's width fraction."""
        col = self.current_column
        if not col:
            return
        delta = step if step is not None else self.width_step
        col.width_ratio = min(2.0, round(col.width_ratio + delta, 3))
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def shrink_width(self, step: float | None = None) -> None:
        """Decrease the active column's width fraction."""
        col = self.current_column
        if not col:
            return
        delta = step if step is not None else self.width_step
        col.width_ratio = max(0.1, round(col.width_ratio - delta, 3))
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def grow(self, step: float | None = None) -> None:
        """Generic alias for grow_width."""
        self.grow_width(step=step)

    @expose_command()
    def shrink(self, step: float | None = None) -> None:
        """Generic alias for shrink_width."""
        self.shrink_width(step=step)

    @expose_command()
    def grow_left(self) -> None:
        self.shrink_width()

    @expose_command()
    def grow_right(self) -> None:
        self.grow_width()

    @expose_command()
    def cycle_width(self) -> None:
        """Cycle active column width through preset ratios (e.g. 1/3, 1/2, 2/3, 1.0)."""
        col = self.current_column
        if not col:
            return
        curr = col.width_ratio
        next_width = None
        for p in self.preset_widths:
            if p > curr + 0.02:
                next_width = p
                break
        if next_width is None:
            next_width = self.preset_widths[0]
        col.width_ratio = next_width
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def set_width(self, width: float | str) -> None:
        """Set active column width ratio or named preset."""
        col = self.current_column
        if not col:
            return
        if isinstance(width, str):
            named = {
                "1/3": 0.333333,
                "1/2": 0.5,
                "half": 0.5,
                "2/3": 0.666667,
                "1": 1.0,
                "full": 1.0,
                "max": 1.0,
            }
            width_val = named.get(width.strip().lower(), 0.5)
        else:
            width_val = float(width)

        col.width_ratio = max(0.1, min(2.0, width_val))
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def reset_width(self) -> None:
        """Reset active column width to default_width."""
        col = self.current_column
        if not col:
            return
        col.width_ratio = self.default_width
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def reset(self) -> None:
        """Reset all column widths to default_width."""
        for col in self.columns:
            col.width_ratio = self.default_width
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def normalize(self) -> None:
        self.reset()

    @expose_command()
    def toggle_split(self) -> None:
        """Toggle active column between vertical tiling and stacking mode."""
        col = self.current_column
        if not col:
            return
        col.toggle_split()
        self._layout_group(focus=False)

    @expose_command()
    def consume_left(self) -> None:
        """Merge left column's window into current column."""
        if self.current_col_idx <= 0 or len(self.columns) <= 1:
            return
        left_col = self.columns[self.current_col_idx - 1]
        cur_col = self.current_column
        if not left_col or not cur_col or not left_col.cw:
            return
        win = left_col.cw
        left_col.remove(win)
        cur_col.add_client(win)
        if len(left_col) == 0:
            self.columns.pop(self.current_col_idx - 1)
            self.current_col_idx -= 1
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def consume_right(self) -> None:
        """Merge right column's window into current column."""
        if self.current_col_idx + 1 >= len(self.columns):
            return
        right_col = self.columns[self.current_col_idx + 1]
        cur_col = self.current_column
        if not right_col or not cur_col or not right_col.cw:
            return
        win = right_col.cw
        right_col.remove(win)
        cur_col.add_client(win)
        if len(right_col) == 0:
            self.columns.pop(self.current_col_idx + 1)
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def expel(self) -> None:
        """Move the active window out of current column into its own new column."""
        cur_col = self.current_column
        if not cur_col or len(cur_col) <= 1 or not cur_col.cw:
            return
        win = cur_col.cw
        cur_col.remove(win)
        new_col = _Column(split=self.split, width_ratio=cur_col.width_ratio)
        new_col.add_client(win)
        self.columns.insert(self.current_col_idx + 1, new_col)
        self.current_col_idx += 1
        self.scroll_to_focused(animate=self.animate)
        self._layout_group(focus=False)

    @expose_command()
    def center(self) -> None:
        """Center the active column in the viewport."""
        self.scroll_to_focused(animate=self.animate, force_center=True)

    @expose_command()
    def scroll_left(self, delta: int = 150) -> None:
        """Pan viewport to the left."""
        self.scroll_offset -= delta
        self._layout_group(focus=False)

    @expose_command()
    def scroll_right(self, delta: int = 150) -> None:
        """Pan viewport to the right."""
        self.scroll_offset += delta
        self._layout_group(focus=False)

    @expose_command()
    def toggle_maximize(self) -> None:
        """Toggle maximize on current focused window."""
        win = self.current_window
        if self.has_group and getattr(self.group, "current_window", None):
            win = self.group.current_window
        if win and hasattr(win, "toggle_maximize"):
            win.toggle_maximize()

    @expose_command()
    def toggle_minimize(self) -> None:
        """Toggle minimize on current focused window."""
        win = self.current_window
        if self.has_group and getattr(self.group, "current_window", None):
            win = self.group.current_window
        if win and hasattr(win, "toggle_minimize"):
            win.toggle_minimize()

    @expose_command()
    def restore_minimized(self) -> None:
        """Restore the most recently minimized window in this layout or group."""
        minimized: list[Window] = []
        if self.has_group and hasattr(self.group, "windows"):
            minimized = [w for w in self.group.windows if getattr(w, "minimized", False) is True]
        if not minimized:
            for col in self.columns:
                for c in col.clients:
                    if getattr(c, "minimized", False) is True:
                        minimized.append(c)
        if minimized:
            win = minimized[-1]
            win.minimized = False
            if self.has_group and hasattr(self.group, "focus"):
                self.group.focus(win, warp=True)
            else:
                self.focus(win)

    @expose_command()
    def info(self) -> dict[str, Any]:
        group_name = None
        if self.has_group:
            try:
                group_name = self.group.name
            except Exception:
                pass
        d: dict[str, Any] = {
            "name": self.name,
            "group": group_name,
            "current_column": self.current_col_idx,
            "columns": [c.info() for c in self.columns],
            "scroll_offset": self.scroll_offset,
            "target_scroll_offset": self.target_scroll_offset,
            "clients": [c.name for c in self.get_windows()],
        }
        return d

    # Aliases for cmd_* naming convention
    cmd_left = left
    cmd_right = right
    cmd_up = up
    cmd_down = down
    cmd_shuffle_left = shuffle_left
    cmd_shuffle_right = shuffle_right
    cmd_shuffle_up = shuffle_up
    cmd_shuffle_down = shuffle_down
    cmd_grow_width = grow_width
    cmd_shrink_width = shrink_width
    cmd_grow = grow
    cmd_shrink = shrink
    cmd_grow_left = grow_left
    cmd_grow_right = grow_right
    cmd_cycle_width = cycle_width
    cmd_set_width = set_width
    cmd_reset_width = reset_width
    cmd_reset = reset
    cmd_normalize = normalize
    cmd_toggle_split = toggle_split
    cmd_consume_left = consume_left
    cmd_consume_right = consume_right
    cmd_expel = expel
    cmd_center = center
    cmd_scroll_left = scroll_left
    cmd_scroll_right = scroll_right
    cmd_toggle_maximize = toggle_maximize
    cmd_toggle_minimize = toggle_minimize
    cmd_restore_minimized = restore_minimized
    cmd_info = info

