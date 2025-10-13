"""Interactive command line interface for the PSP converter."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from rich import box
from rich.console import Console
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from .core import (
    ConversionOptions,
    apply_preset,
    build_ffmpeg_command,
    execute_ffmpeg,
)
from .presets import PRESET_INDEX, PRESETS

console = Console()


def _prompt_path(label: str, *, default: Optional[str] = None) -> str:
    while True:
        path = Prompt.ask(label, default=default)
        if path:
            return path
        console.print("[red]Value required.[/red]")


def _display_presets() -> None:
    table = Table(title="PSP Presets", box=box.SIMPLE_HEAVY)
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Resolution")
    table.add_column("Audio")
    for preset in PRESETS:
        width, height = preset.resolution
        aspect = f"{preset.aspect_ratio[0]}:{preset.aspect_ratio[1]}"
        table.add_row(
            preset.key,
            preset.name,
            f"{width}x{height} @ {aspect}",
            f"{preset.audio_bitrate} kbps",
        )
    console.print(table)


def _choose_preset() -> ConversionOptions:
    _display_presets()
    key = Prompt.ask(
        "Enter preset key",
        choices=[preset.key for preset in PRESETS],
        default="0",
    )
    preset = PRESET_INDEX[key.upper()]

    input_path = _prompt_path("Input file path")
    suggested_output = _suggest_output(input_path)
    output_path = _prompt_path(
        "Output file path",
        default=suggested_output,
    )

    if Confirm.ask("Override audio bitrate?", default=False):
        audio_bitrate = IntPrompt.ask(
            "Audio bitrate (kbps)",
            default=preset.audio_bitrate,
        )
    else:
        audio_bitrate = preset.audio_bitrate

    if Confirm.ask("Force constant video bitrate?", default=False):
        video_bitrate = IntPrompt.ask("Video bitrate (kbps)", default=1200)
    else:
        video_bitrate = preset.video_bitrate

    if Confirm.ask("Override resolution?", default=False):
        width = IntPrompt.ask("Width", default=preset.resolution[0])
        height = IntPrompt.ask("Height", default=preset.resolution[1])
        resolution = (width, height)
    else:
        resolution = preset.resolution

    if Confirm.ask("Override aspect ratio?", default=False):
        aspect_w = IntPrompt.ask(
            "Aspect width",
            default=preset.aspect_ratio[0],
        )
        aspect_h = IntPrompt.ask(
            "Aspect height",
            default=preset.aspect_ratio[1],
        )
        aspect_ratio = (aspect_w, aspect_h)
    else:
        aspect_ratio = preset.aspect_ratio

    return apply_preset(
        preset,
        input_path=input_path,
        output_path=output_path,
        audio_bitrate=audio_bitrate,
        video_bitrate=video_bitrate,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
    )


def _custom_configuration() -> ConversionOptions:
    input_path = _prompt_path("Input file path")
    suggested_output = _suggest_output(input_path)
    output_path = _prompt_path(
        "Output file path",
        default=suggested_output,
    )

    width = IntPrompt.ask("Width", default=720)
    height = IntPrompt.ask("Height", default=480)
    aspect_w = IntPrompt.ask("Aspect width", default=16)
    aspect_h = IntPrompt.ask("Aspect height", default=9)
    audio_bitrate = IntPrompt.ask("Audio bitrate (kbps)", default=160)

    if Confirm.ask("Force constant video bitrate?", default=False):
        video_bitrate = IntPrompt.ask("Video bitrate (kbps)", default=1200)
    else:
        video_bitrate = None

    return ConversionOptions(
        input_path=input_path,
        output_path=output_path,
        resolution=(width, height),
        aspect_ratio=(aspect_w, aspect_h),
        audio_bitrate=audio_bitrate,
        video_bitrate=video_bitrate,
    )


def _suggest_output(input_path: str) -> str:
    path = Path(input_path)
    if path.suffix:
        return str(path.with_suffix("_psp.mp4"))
    return f"{path}_psp.mp4"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PSP video converter")
    parser.add_argument(
        "--no-exec",
        action="store_true",
        help="Only print the ffmpeg command instead of executing it.",
    )
    parser.add_argument(
        "--preset",
        help="Bypass the interactive wizard and use the provided preset key.",
        choices=[preset.key for preset in PRESETS],
    )
    parser.add_argument("input", nargs="?")
    parser.add_argument("output", nargs="?")

    args = parser.parse_args(argv)

    if args.preset and args.input and args.output:
        preset = PRESET_INDEX[args.preset.upper()]
        options = apply_preset(
            preset,
            input_path=args.input,
            output_path=args.output,
        )
    else:
        console.print("[bold]Sony PSP Video Converter[/bold]")
        console.print("Select conversion mode:\n")
        if Confirm.ask("Use a preset?", default=True):
            options = _choose_preset()
        else:
            options = _custom_configuration()

    command = build_ffmpeg_command(options)
    console.print("\n[bold green]Generated command:[/bold green]")
    console.print(" ".join(command))

    if args.no_exec:
        return 0

    if Confirm.ask("Run ffmpeg now?", default=True):
        return execute_ffmpeg(command)

    console.print("[yellow]Command not executed.[/yellow]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
