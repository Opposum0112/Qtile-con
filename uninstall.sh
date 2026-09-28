#!/usr/bin/env bash
set -Eeuo pipefail

DRY_RUN=0
ASSUME_YES=0
TARGET="${QTILE_CONFIG_DIR:-$HOME/.config/qtile}"

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --yes|-y) ASSUME_YES=1 ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] [--yes]"
      echo "  --dry-run  Show target and backup path without changing anything"
      echo "  --yes      Skip interactive confirmation"
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

if [[ ! -d "$TARGET" ]]; then
  echo "No Qtile configuration found at $TARGET."
  exit 0
fi

BACKUP="${TARGET}.removed.$(date +%Y%m%d-%H%M%S)"
echo "Configuration to move: $TARGET"
echo "Backup destination:    $BACKUP"
echo "Packages, wallpapers and screenshots will not be removed."

if [[ "$DRY_RUN" == 1 ]]; then
  echo "Dry run: no files changed."
  exit 0
fi

if [[ "$ASSUME_YES" != 1 ]]; then
  read -r -p "Move the configuration to the backup path above? [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 0; }
fi

mv -- "$TARGET" "$BACKUP"
echo "Configuration moved to $BACKUP."
