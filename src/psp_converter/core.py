"""Core primitives for building and running ffmpeg commands."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Preset:
    """Configuration for a PSP conversion preset."""

    key: str
    name: str
    description: str
    resolution: Tuple[int, int]
    aspect_ratio: Tuple[int, int]
    audio_bitrate: int
    video_bitrate: Optional[int] = None


@dataclass
class ConversionOptions:
    """All parameters required to generate an ffmpeg command."""

    input_path: str
    output_path: str
    resolution: Tuple[int, int]
    aspect_ratio: Tuple[int, int]
    audio_bitrate: int = 160
    video_bitrate: Optional[int] = None
    audio_channels: int = 2
    audio_sample_rate: int = 48000
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    video_profile: str = "baseline"
    video_level: str = "3.0"
    frame_rate: str = "30000/1001"
    pixel_format: str = "yuv420p"
    container_format: str = "psp"
    x264_params: Optional[Sequence[str]] = None
    faststart: bool = True
    extra_args: Sequence[str] = field(default_factory=tuple)

    def resolved_input(self) -> str:
        return str(Path(self.input_path).expanduser())

    def resolved_output(self) -> str:
        return str(Path(self.output_path).expanduser())


def build_ffmpeg_command(options: ConversionOptions) -> List[str]:
    """Render the ffmpeg invocation for the provided options."""

    command: List[str] = [
        "ffmpeg",
        "-i",
        options.resolved_input(),
        "-vcodec",
        options.video_codec,
    ]

    if options.video_bitrate:
        command.extend(["-b:v", f"{options.video_bitrate}k"])

    width, height = options.resolution
    command.extend([
        "-s",
        f"{width}x{height}",
        "-aspect",
        f"{options.aspect_ratio[0]}:{options.aspect_ratio[1]}",
        "-profile:v",
        options.video_profile,
        "-level:v",
        options.video_level,
        "-pix_fmt",
        options.pixel_format,
        "-r",
        str(options.frame_rate),
        "-acodec",
        options.audio_codec,
        "-b:a",
        f"{options.audio_bitrate}k",
        "-ar",
        str(options.audio_sample_rate),
        "-ac",
        str(options.audio_channels),
    ])

    if options.x264_params and options.video_codec in {"libx264"}:
        command.extend(["-x264-params", ":".join(options.x264_params)])

    if options.faststart:
        command.extend(["-movflags", "+faststart"])

    if options.container_format:
        command.extend(["-f", str(options.container_format)])

    if options.extra_args:
        command.extend(options.extra_args)

    command.append(options.resolved_output())
    return command


def execute_ffmpeg(command: Iterable[str]) -> int:
    """Execute ``ffmpeg`` with the provided command sequence."""

    import subprocess

    process = subprocess.run(list(command), check=False)
    return process.returncode


def apply_preset(
    preset: Preset, *, input_path: str, output_path: str, **overrides: object
) -> ConversionOptions:
    """Build conversion options from a preset and override values."""

    resolution = overrides.pop("resolution", preset.resolution)
    aspect_ratio = overrides.pop("aspect_ratio", preset.aspect_ratio)
    audio_bitrate = int(overrides.pop("audio_bitrate", preset.audio_bitrate))

    video_bitrate = overrides.pop("video_bitrate", preset.video_bitrate)
    video_bitrate_int: Optional[int] = (
        None if video_bitrate in (None, "", 0) else int(video_bitrate)
    )

    return ConversionOptions(
        input_path=input_path,
        output_path=output_path,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
        audio_bitrate=audio_bitrate,
        video_bitrate=video_bitrate_int,
        **overrides,
    )
