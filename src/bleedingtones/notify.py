"""
bleedingtones notify
---------------------
Category-aware sound dispatcher. Plays a random sound from a named
subfolder, so you can wire different moods to different events.

Folder structure:
    ~/Sounds_FX/
        win/        ← played on --category win
        fail/       ← played on --category fail
        alert/      ← played on --category alert
        done/       ← played on --category done
        (anything)  ← --category anything

Falls back to the root folder if the category subfolder doesn't exist
and --strict is not set.

Usage:
    python -m bleedingtones.notify --category win
    python -m bleedingtones.notify --category fail --path /your/sounds
    python -m bleedingtones.notify --list
    python -m bleedingtones.notify --category done --strict

Pipe-friendly: exits 0 on success, 1 on error.
Designed to be called from scripts, Makefiles, CI hooks, etc.

    make build && python -m bleedingtones.notify --category win \\
        || python -m bleedingtones.notify --category fail
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import engine


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bleedingtones-notify",
        description=(
            "Play a random sound from a named category subfolder.\n"
            "Pipe it into your scripts. Make your terminal expressive."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / "Sounds_FX",
        help="Root folder containing category subfolders (default: ~/Sounds_FX)",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Subfolder name to draw from (e.g. win, fail, alert, done)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error if the category subfolder does not exist (default: fallback to root)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_categories",
        help="List all available categories (subfolders) and exit",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Play the full track (default: play full track — this flag exists for explicitness)",
    )
    args = parser.parse_args()

    root = args.path
    if not root.is_dir():
        sys.exit(f"[bleedingtones] Root folder not found: {root}")

    if args.list_categories:
        cats = [d for d in sorted(root.iterdir()) if d.is_dir()]
        if not cats:
            print(f"[bleedingtones] No category subfolders found in: {root}")
            print("  Create subfolders like win/, fail/, alert/ and drop sounds into them.")
        else:
            print(f"[bleedingtones] Categories in {root}:")
            for cat in cats:
                sounds = engine.collect(cat) if any(
                    f.suffix.lower() in engine.SUPPORTED for f in cat.iterdir()
                ) else []
                print(f"  {cat.name}/  ({len(sounds)} sound(s))")
        return

    if args.category is None:
        # No category — play from root
        target = root
    else:
        target = root / args.category
        if not target.is_dir():
            if args.strict:
                sys.exit(
                    f"[bleedingtones] Category not found: {target}\n"
                    "  Use --list to see available categories, or drop --strict to fallback to root."
                )
            else:
                print(
                    f"[bleedingtones] Category '{args.category}' not found — falling back to root: {root}",
                    file=sys.stderr,
                )
                target = root

    files = engine.collect(target)
    chosen = engine.pick(files)
    print(f"[bleedingtones] [{args.category or 'root'}] {chosen.name}")
    engine.play(chosen, duration=None)


if __name__ == "__main__":
    main()
