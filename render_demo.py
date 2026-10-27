"""Render a short, silent modulo-clock MP4 with a matching data receipt."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont
from studio_core import modulo_walk

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 1280, 720, 24


def font(size: int):
    # Public code contains no operator-specific absolute paths.
    for candidate in ("DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def frame(data: dict, index: int) -> Image.Image:
    item = data["positions"][index]
    modulus = data["modulus"]
    image = Image.new("RGB", (WIDTH, HEIGHT), "#101b2a")
    draw = ImageDraw.Draw(image)
    gold, teal, white = "#e9c674", "#51ddcf", "#edf3fa"
    draw.text((55, 30), "MODULO WORKSHOP", font=font(34), fill=gold)
    draw.text((55, 80), "The cosmic clock retained its remainder. The total is still here.",
              font=font(23), fill=white)
    cx, cy, radius = 350, 380, 205
    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=gold, width=4)
    for residue in range(modulus):
        angle = 2 * math.pi * residue / modulus - math.pi / 2
        px, py = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        draw.text((px, py), str(residue), anchor="mm", font=font(27), fill=white)
    angle = 2 * math.pi * item["residue"] / modulus - math.pi / 2
    tx, ty = cx + radius * .77 * math.cos(angle), cy + radius * .77 * math.sin(angle)
    draw.line((cx, cy, tx, ty), fill=teal, width=8)
    draw.ellipse((tx-12, ty-12, tx+12, ty+12), fill=teal)
    sign = "+" if data["steps"] >= 0 else "-"
    lines = [f"{data['start']} {sign} {index} = {item['total']}",
             f"modulus: {modulus}", f"residue: {item['residue']}",
             f"quotient: {item['quotient']}",
             f"{item['total']} = {item['quotient']} x {modulus} + {item['residue']}"]
    for row, text in enumerate(lines):
        draw.text((650, 220 + row * 66), text, font=font(32), fill=white if row else teal)
    draw.text((55, 652), "Different integers can share a residue. This is a demonstration, not a complexity proof.",
              font=font(22), fill=gold)
    return image


def render(start: int, steps: int, modulus: int, output: str) -> dict:
    data = modulo_walk(start, steps, modulus)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("FFmpeg and ffprobe must be on PATH")
    render_dir = (ROOT / "renders").resolve()
    render_dir.mkdir(exist_ok=True)
    target = (ROOT / output).resolve()
    if not target.is_relative_to(render_dir) or target.suffix.lower() != ".mp4":
        raise ValueError("output must be an .mp4 inside this project's renders directory")
    if target.exists() or target.with_suffix(".json").exists():
        raise FileExistsError("Choose a new output filename; existing results are preserved")
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-n", "-f", "rawvideo",
               "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
               "-i", "pipe:0", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(target)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for index in range(len(data["positions"])):
            raw = frame(data, index).tobytes()
            for _ in range(FPS * 2):
                process.stdin.write(raw)
        process.stdin.close()
        error = process.stderr.read().decode("utf-8", errors="replace")
        code = process.wait(timeout=120)
        if code:
            raise RuntimeError(f"FFmpeg failed ({code}): {error}")
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    metadata = json.loads(subprocess.check_output(
        [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(target)], text=True))
    video = next(stream for stream in metadata["streams"] if stream["codec_type"] == "video")
    duration = float(metadata["format"]["duration"])
    expected_duration = len(data["positions"]) * 2
    assert video["codec_name"] == "h264" and video["width"] == WIDTH and video["height"] == HEIGHT
    assert abs(duration - expected_duration) < 0.1
    receipt = {"example": data, "video": {"path": target.name, "width": WIDTH,
               "height": HEIGHT, "fps": FPS, "codec": video["codec_name"],
               "duration_seconds": duration, "audio": False,
               "sha256": hashlib.sha256(target.read_bytes()).hexdigest()},
               "checks": ["H.264 codec", "1280x720 dimensions", "expected duration"],
               "limits": ["No narration", "No editor UI", "Visual semantics require review",
                          "No external publishing tools"]}
    target.with_suffix(".json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=10)
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--modulus", type=int, default=12)
    parser.add_argument("--output", default="renders/modulo-clock.mp4")
    args = parser.parse_args()
    print(json.dumps(render(args.start, args.steps, args.modulus, args.output), indent=2))
