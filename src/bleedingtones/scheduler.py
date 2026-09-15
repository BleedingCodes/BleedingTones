"""
bleedingtones scheduler
------------------------
Plays a random sound on a timer — at a fixed interval or randomly
within a window. Runs until killed.

Use case: you're deep in a task and need something to randomly
remind you that life is good and Snake is calling.

Usage:
    python -m bleedingtones.scheduler
    python -m bleedingtones.scheduler --interval 300
    python -m bleedingtones.scheduler --min 120 --max 600
    python -m bleedingtones.scheduler --path /your/sounds --interval 60
"""

from __future__ import annotations

import argparse
import random
import signal
import sys
import time
from pathlib import Path

from . import engine

_running = True


def _handle_signal(sig, frame):  # noqa: ANN001
    global _running
    print("\n[bleedingtones] Scheduler stopped.")
    _running = False


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bleedingtones-scheduler",
        description="Random sound on a timer. Set it and forget it.",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / "Sounds_FX",
        help="Folder containing your audio files (default: ~/Sounds_FX)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=None,
        help="Fixed seconds between sounds. Mutually exclusive with --min/--max.",
    )
    parser.add_argument(
        "--min",
        type=float,
        default=60.0,
        dest="min_interval",
        help="Minimum seconds between sounds when using random interval (default: 60)",
    )
    parser.add_argument(
        "--max",
        type=float,
        default=300.0,
        dest="max_interval",
        help="Maximum seconds between sounds when using random interval (default: 300)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Stop after N sounds (default: run forever)",
    )
    args = parser.parse_args()

    if args.interval is not None and args.interval <= 0:
        sys.exit("[bleedingtones] --interval must be > 0")
    if args.min_interval >= args.max_interval and args.interval is None:
        sys.exit("[bleedingtones] --min must be less than --max")

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    files = engine.collect(args.path)
    plays = 0

    if args.interval:
        mode_str = f"every {args.interval:.0f}s"
    else:
        mode_str = f"every {args.min_interval:.0f}–{args.max_interval:.0f}s (random)"

    limit_str = f", stopping after {args.count}" if args.count else ", running until Ctrl+C"
    print(f"[bleedingtones] scheduler — {mode_str}{limit_str}")

    while _running:
        if args.count is not None and plays >= args.count:
            print("[bleedingtones] Count reached. Done.")
            break

        wait = args.interval if args.interval else random.uniform(args.min_interval, args.max_interval)
        print(f"  ⏱  Next sound in {wait:.0f}s...")

        # Sleep in small chunks so Ctrl+C is responsive
        elapsed = 0.0
        while elapsed < wait and _running:
            time.sleep(0.25)
            elapsed += 0.25

        if not _running:
            break

        chosen = engine.pick(files)
        print(f"  ▶  {chosen.name}")
        engine.play(chosen, duration=None)
        plays += 1

    sys.exit(0)


if __name__ == "__main__":
    main()
