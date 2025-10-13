"""Preset definitions shared across the CLI."""

from __future__ import annotations

from typing import Dict, List

from .core import Preset


PRESETS: List[Preset] = [
    Preset(
        key="0",
        name="PSP-3000 480p",
        description="720x480 @ 16:9, 256 kbps audio",
        resolution=(720, 480),
        aspect_ratio=(16, 9),
        audio_bitrate=256,
    ),
    Preset(
        key="1",
        name="720x480 / 16:9 / 192 kbps",
        description="Balanced audio for widescreen sources",
        resolution=(720, 480),
        aspect_ratio=(16, 9),
        audio_bitrate=192,
    ),
    Preset(
        key="2",
        name="720x480 / 16:9 / 160 kbps",
        description="Smaller file size widescreen",
        resolution=(720, 480),
        aspect_ratio=(16, 9),
        audio_bitrate=160,
    ),
    Preset(
        key="3",
        name="720x480 / 16:9 / 128 kbps",
        description="Lowest audio bitrate for widescreen",
        resolution=(720, 480),
        aspect_ratio=(16, 9),
        audio_bitrate=128,
    ),
    Preset(
        key="4",
        name="PSP-3000 4:3",
        description="640x480 @ 4:3, 256 kbps audio",
        resolution=(640, 480),
        aspect_ratio=(4, 3),
        audio_bitrate=256,
    ),
    Preset(
        key="5",
        name="640x480 / 4:3 / 192 kbps",
        description="Balanced audio for classic content",
        resolution=(640, 480),
        aspect_ratio=(4, 3),
        audio_bitrate=192,
    ),
    Preset(
        key="6",
        name="640x480 / 4:3 / 160 kbps",
        description="Smaller file size 4:3",
        resolution=(640, 480),
        aspect_ratio=(4, 3),
        audio_bitrate=160,
    ),
    Preset(
        key="7",
        name="640x480 / 4:3 / 128 kbps",
        description="Lowest audio bitrate for 4:3",
        resolution=(640, 480),
        aspect_ratio=(4, 3),
        audio_bitrate=128,
    ),
    Preset(
        key="8",
        name="Most Compatible 480p",
        description="480x272 @ 16:9, 256 kbps audio",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        audio_bitrate=256,
    ),
    Preset(
        key="9",
        name="480x272 / 16:9 / 192 kbps",
        description="Balanced audio for PSP-native resolution",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        audio_bitrate=192,
    ),
    Preset(
        key="A",
        name="480x272 / 16:9 / 160 kbps",
        description="Smaller file size PSP-native",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        audio_bitrate=160,
    ),
    Preset(
        key="B",
        name="480x272 / 16:9 / 128 kbps",
        description="Lowest audio bitrate PSP-native",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        audio_bitrate=128,
    ),
    Preset(
        key="C",
        name="Most PSP-1000 Compatible",
        description="368x208 @ 16:9, 256 kbps audio",
        resolution=(368, 208),
        aspect_ratio=(16, 9),
        audio_bitrate=256,
    ),
    Preset(
        key="D",
        name="320x240 / 4:3 / 192 kbps",
        description="Balanced audio for low resolution",
        resolution=(320, 240),
        aspect_ratio=(4, 3),
        audio_bitrate=192,
    ),
    Preset(
        key="E",
        name="320x240 / 4:3 / 160 kbps",
        description="Smaller file size low resolution",
        resolution=(320, 240),
        aspect_ratio=(4, 3),
        audio_bitrate=160,
    ),
    Preset(
        key="F",
        name="320x240 / 4:3 / 128 kbps",
        description="Lowest audio bitrate low resolution",
        resolution=(320, 240),
        aspect_ratio=(4, 3),
        audio_bitrate=128,
    ),
]

PRESET_INDEX: Dict[str, Preset] = {
    preset.key.upper(): preset
    for preset in PRESETS
}
