"""Workspaces and group labels."""
from libqtile.config import Group
from libqtile.lazy import lazy

groups = [Group(str(i), label=label) for i, label in enumerate(
    ["󰈹", "󰆍", "󰖟", "󰙯", "󰎆", "󰓓", "󰒓", "󰉋", "󰐃"], start=1
)]
