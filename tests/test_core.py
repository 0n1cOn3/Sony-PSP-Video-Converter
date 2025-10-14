from pathlib import Path

from psp_converter.core import ConversionOptions, build_ffmpeg_command


def test_default_command_generation():
    options = ConversionOptions(
        input_path="input.mkv",
        output_path="output.mp4",
        resolution=(720, 480),
        aspect_ratio=(16, 9),
    )

    command = build_ffmpeg_command(options)

    assert command == [
        "ffmpeg",
        "-i",
        "input.mkv",
        "-vcodec",
        "libx264",
        "-s",
        "720x480",
        "-aspect",
        "16:9",
        "-profile:v",
        "baseline",
        "-level:v",
        "3.0",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30000/1001",
        "-acodec",
        "aac",
        "-b:a",
        "160k",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-movflags",
        "+faststart",
        "-f",
        "psp",
        "output.mp4",
    ]


def test_command_includes_x264_params_when_requested():
    options = ConversionOptions(
        input_path="in.mp4",
        output_path="out.mp4",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        x264_params=("cabac=0", "ref=1"),
    )

    command = build_ffmpeg_command(options)

    assert "-x264-params" in command
    assert command[command.index("-x264-params") + 1] == "cabac=0:ref=1"


def test_command_with_overrides():
    options = ConversionOptions(
        input_path="~/movie.mov",
        output_path="~/movie.mp4",
        resolution=(480, 272),
        aspect_ratio=(16, 9),
        audio_bitrate=192,
        video_bitrate=1200,
        extra_args=("-vf", "scale=iw/2:ih/2"),
    )

    command = build_ffmpeg_command(options)

    assert command[:8] == [
        "ffmpeg",
        "-i",
        str(Path("~/movie.mov").expanduser()),
        "-vcodec",
        "libx264",
        "-b:v",
        "1200k",
        "-s",
    ]
    assert command[-3:] == [
        "-vf",
        "scale=iw/2:ih/2",
        str(Path("~/movie.mp4").expanduser()),
    ]
