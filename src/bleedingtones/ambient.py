"""
bleedingtones ambient
----------------------
Continuous random audio player. Plays one sound at a time, picks
the next one at random when it finishes. Runs until you kill it.

Useful for: keeping your brain awake, background motivation noise,
making your desk sound like a Smash Bros lobby.

Usage:
    python -m bleedingtones.ambient
    python -m bleedingtones.ambient --path /your/sounds
    python -m bleedingtones.ambient --path /your/sounds --gap 3
    python -m bleedingtones.ambient --path /your/sounds --no-repeat
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path

from . import engine

_running = True


def _handle_signal(sig, frame):  # noqa: ANN001
    global _running
    print("\n[bleedingtones] Stopping.")
    _running = False


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bleedingtones-ambient",
        description="Continuous random sound player. Ctrl+C to stop.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / "Sounds_FX",
        help="Folder containing your audio files (default: ~/Sounds_FX)",
    )
    parser.add_argument(
        "--gap",
        type=float,
        default=2.0,
        help="Seconds of silence between tracks (default: 2.0)",
    )
    parser.add_argument(
        "--no-repeat",
        action="store_true",
        help="Don't play the same sound twice in a row",
    )
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    files = engine.collect(args.path)
    last: Path | None = None

    print(f"[bleedingtones] ambient — {len(files)} sound(s) loaded. Ctrl+C to stop.")

    while _running:
        candidates = [f for f in files if f != last] if args.no_repeat and len(files) > 1 else files
        chosen = engine.pick(candidates)
        last = chosen
        print(f"  ▶  {chosen.name}")
        engine.play(chosen, duration=None)

        if _running and args.gap > 0:
            time.sleep(args.gap)

    sys.exit(0)


if __name__ == "__main__":
    main()
