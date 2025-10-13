# Sony PSP Video Converter

The PSP Video Converter bundles the project history into a single, text user interface (TUI) that guides you through picking presets and generating the right `ffmpeg` command line for PSP-compatible MP4 files.

## Features

- Interactive wizard powered by [Rich](https://rich.readthedocs.io) for clearer prompts and preset tables.
- Library of community presets spanning PSP-3000 and PSP-1000 friendly resolutions.
- Emits ffmpeg commands that target the PSP baseline profile, 48 kHz AAC audio, and the `psp` container for certified playback.
- Ability to override audio bitrate, aspect ratio, resolution, and optionally force a constant video bitrate.
- CLI mode to skip the wizard when the preset key and paths are known.

## Requirements

- Python 3.9 or newer
- `ffmpeg` available on your `PATH`

## Installation

Create a virtual environment (recommended) and install the project in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

This will expose a `psp-converter` console script.

## Usage

Run the wizard and follow the prompts:

```bash
psp-converter
```

If you already know which preset you want to use, you can bypass the wizard:

```bash
psp-converter --preset 0 input.mkv output.mp4
```

Pass `--no-exec` to only print the generated command:

```bash
psp-converter --no-exec
```

## Preset reference

| Key | Resolution | Aspect | Audio bitrate |
| --- | ---------- | ------ | ------------- |
| 0   | 720x480    | 16:9   | 256 kbps      |
| 1   | 720x480    | 16:9   | 192 kbps      |
| 2   | 720x480    | 16:9   | 160 kbps      |
| 3   | 720x480    | 16:9   | 128 kbps      |
| 4   | 640x480    | 4:3    | 256 kbps      |
| 5   | 640x480    | 4:3    | 192 kbps      |
| 6   | 640x480    | 4:3    | 160 kbps      |
| 7   | 640x480    | 4:3    | 128 kbps      |
| 8   | 480x272    | 16:9   | 256 kbps      |
| 9   | 480x272    | 16:9   | 192 kbps      |
| A   | 480x272    | 16:9   | 160 kbps      |
| B   | 480x272    | 16:9   | 128 kbps      |
| C   | 368x208    | 16:9   | 256 kbps      |
| D   | 320x240    | 4:3    | 192 kbps      |
| E   | 320x240    | 4:3    | 160 kbps      |
| F   | 320x240    | 4:3    | 128 kbps      |

## Development

Run the automated tests:

```bash
pytest
```

## License

This project continues to use the ROOTBEER-WARE license attributed to the original authors; see [LICENSE](LICENSE) for details.
