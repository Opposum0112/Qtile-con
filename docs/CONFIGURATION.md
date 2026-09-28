# Configuration guide

- `config/settings.py`: terminal, wallpaper directory, gaps, borders and bar dimensions.
- `config/keys.py`: keyboard shortcuts.
- `config/groups.py`: workspace labels.
- `config/layouts.py`: layouts, borders and gaps.
- `config/widgets.py`: bar widgets and click actions.
- `config/screens.py`: screen and bar placement.
- `config/colors.py`: active palette generated from a theme preset.

Put PNG, JPEG or WebP files in `~/Pictures/Wallpapers`, then use Super+Shift+W.
Theme JSON files live in `themes/`. Required palette keys are `base`, `text`, `mauve`, `overlay`, and `surface0`.

The project targets Qtile's Wayland backend. Application names and package availability vary by distribution. Optional widgets should be removed or adjusted if their helper applications are not installed.

## Validate the configuration

Run the project's wrapper:

```sh
~/.config/qtile/scripts/check-config
```

It reports the Qtile and mypy executables before running `qtile check`. This helps diagnose cases where Qtile and mypy come from different Python environments.

If Qtile was installed with pipx and the check reports that mypy cannot import `libqtile`, inject mypy into Qtile's isolated environment:

```sh
pipx inject qtile mypy
~/.config/qtile/scripts/check-config
```

If the `qtile` executable is managed by a different virtual environment, activate that environment first and install mypy there. Avoid fixing this by globally ignoring missing imports: that hides the type-checking problem instead of checking the config against Qtile's actual API.
