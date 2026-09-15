"""
bleedingtones.engine
--------------------
Shared audio playback engine used by all four tools.
Handles pygame init, format detection, duration, and clean teardown.
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

SUPPORTED = {".mp3", ".wav", ".ogg", ".flac"}


def _pygame():
    """Lazy import + init so tools that don't need audio don't pay for it."""
    try:
        import pygame
    except ImportError:
        sys.exit(
            "[bleedingtones] pygame is not installed.\n"
            "Fix: pip install pygame"
        )
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    return pygame


def collect(path: Path) -> list[Path]:
    """Return all supported audio files under path (non-recursive)."""
    if not path.is_dir():
        sys.exit(f"[bleedingtones] Sound folder not found: {path}")
    files = [f for f in path.iterdir() if f.suffix.lower() in SUPPORTED]
    if not files:
        sys.exit(
            f"[bleedingtones] No supported audio files found in: {path}\n"
            f"Supported formats: {', '.join(sorted(SUPPORTED))}"
        )
    return files


def pick(files: list[Path]) -> Path:
    return random.choice(files)


def play(sound_path: Path, duration: float | None = None) -> None:
    """
    Play sound_path exactly once.

    Args:
        sound_path: Path to the audio file.
        duration:   How many seconds to let it play before stopping.
                    None = play the full track to completion.
    """
    pygame = _pygame()
    pygame.mixer.music.load(str(sound_path))
    pygame.mixer.music.play()

    if duration is not None:
        time.sleep(duration)
        pygame.mixer.music.stop()
    else:
        # Poll until the track ends naturally
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    pygame.mixer.music.unload()
    pygame.quit()
