"""
bleedingtones chaos
-------------------
The original — upgraded.

Picks a random sound and plays it. That's it.
No scheduling. No triggers. No reason.
Just vibes.

Usage:
    python -m bleedingtones.chaos
    python -m bleedingtones.chaos --path /your/sounds
    python -m bleedingtones.chaos --path /your/sounds --full
    python -m bleedingtones.chaos --path /your/sounds --duration 10
    python -m bleedingtones.chaos --list
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import engine

DEFAULT_DURATION = 30.0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bleedingtones-chaos",
        description="Play a random sound. No reason needed.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / "Sounds_FX",
        help="Folder containing your audio files (default: ~/Sounds_FX)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=DEFAULT_DURATION,
        help=f"Seconds to play before stopping (default: {DEFAULT_DURATION})",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Play the full track regardless of duration",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_sounds",
        help="List all available sounds and exit",
    )
    args = parser.parse_args()

    files = engine.collect(args.path)

    if args.list_sounds:
        print(f"[bleedingtones] {len(files)} sound(s) in {args.path}:")
        for f in sorted(files):
            print(f"  {f.name}")
        return

    chosen = engine.pick(files)
    print(f"[bleedingtones] {chosen.name}")
    engine.play(chosen, duration=None if args.full else args.duration)


if __name__ == "__main__":
    main()
