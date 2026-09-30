# bleedingtones

Terminal troll yourself by playing sounds now or randomly. Because sometimes you
finished and just survived another a task — and the Mii victory theme is the correct response.

Four tools. One folder of MP3s. Zero apologies.

---

## What It Does

| Tool | What It Is |
|---|---|
| `chaos` | Picks a random sound and plays it. |
| `ambient` | Continuous shuffle — plays one sound after another until you tell it to stop. |
| `scheduler` | Fires a random sound on a timer. Fixed interval or random window. Runs in the background. |
| `notify` | Category-aware dispatcher. Wire different subfolders to different events in your scripts. |

---

## Who It's For

Developers, technicians, and anyone who runs a terminal for hours and wants
spontaneous audio interruptions that are charming instead of annoying.
Works on Linux. Plays MP3, WAV, OGG, and FLAC.

---

## Requirements

- Python 3.11+
- `pygame` >= 2.5 (`pip install pygame`)
- A folder of audio files you actually want to hear

---

## Installation

```bash
git clone https://github.com/BleedingCodes/bleedingtones
cd bleedingtones
pip install -r requirements.txt
```

Or install as a package with CLI entry points:

```bash
pip install .
```

---

## Usage

### chaos — The Original

Play one random sound. No context. No ceremony.

```bash
python -m bleedingtones.chaos
python -m bleedingtones.chaos --path ~/my/sounds
python -m bleedingtones.chaos --full                  # play the whole track
python -m bleedingtones.chaos --duration 10           # stop after 10 seconds
python -m bleedingtones.chaos --list                  # see what you've got
```

This is the upgraded version of the original one-liner. Fixed: empty folder
crash, missing path crash, hardcoded 30-second cutoff that ignored track length,
and the complete absence of any way to configure it.

---

### ambient — Continuous Shuffle

Plays sounds back to back. Picks a new one at random after each finishes.
Runs until `Ctrl+C`.

```bash
python -m bleedingtones.ambient
python -m bleedingtones.ambient --path ~/my/sounds
python -m bleedingtones.ambient --gap 5              # 5 seconds between tracks
python -m bleedingtones.ambient --no-repeat          # never play the same one twice in a row
```

---

### scheduler — Timed Random Trigger

Fires a random sound on an interval. Keeps running in the background.
Good for: remembering to stand up, rewarding yourself for surviving,
or making your desk sound alive.

```bash
python -m bleedingtones.scheduler                     # random interval, 60–300s default
python -m bleedingtones.scheduler --interval 120      # fixed: every 2 minutes
python -m bleedingtones.scheduler --min 30 --max 90   # random between 30 and 90 seconds
python -m bleedingtones.scheduler --count 5           # stop after 5 sounds
```

---

### notify — Script-Friendly Dispatcher

Plays a random sound from a named subfolder. Wire it into your scripts,
Makefiles, or CI hooks so different events sound different.

```bash
python -m bleedingtones.notify --category win
python -m bleedingtones.notify --category fail
python -m bleedingtones.notify --list                 # show available categories
python -m bleedingtones.notify --category done --strict  # error if category missing
```
## Sounds

Bring your own. Point any tool at your folder with `--path`.
Free sound libraries: [freesound.org](https://freesound.org),
[soundsnap.com](https://soundsnap.com), [zapsplat.com](https://zapsplat.com).

**Folder structure for categories:**

```
~/Sounds_FX/
    win/
        mii-victory-theme.mp3
        home-run.mp3
    fail/
        spongebob-fail.mp3
        error.mp3
    alert/
        you-got-mail.mp3
    done/
        cha-ching.ogg
```

**Pipe it into your workflow:**

```bash
make build && python -m bleedingtones.notify --category win \
    || python -m bleedingtones.notify --category fail
```

```bash
# In a script
run_long_job.sh && bleedingtones-notify --category done
```

Falls back to the root folder if the category subfolder doesn't exist.
Pass `--strict` to error instead of falling back.

---

## Supported Formats

`.mp3` `.wav` `.ogg` `.flac`

---

## Default Sound Folder

All tools default to `~/Sounds_FX`. Override with `--path` on any tool.

---

## License

MIT — see [LICENSE](LICENSE)

---

## Built by MainbyteLabs

Python tooling for people who actually use their terminal.
[github.com/MR-MainbyteLabs](https://github.com/MR-MainbyteLabs)
