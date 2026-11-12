"""Small drawing helpers shared by the research concept animations."""

from functools import lru_cache
from math import atan2, cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, SCALE = 800, 360, 2
BG = "#f6f8fa"
PANEL = "#ffffff"
INK = "#1f2937"
MUTED = "#59677a"
LINE = "#d8e0ea"
BLUE = "#2563eb"
TEAL = "#0f766e"
AMBER = "#d48a19"


@lru_cache(maxsize=64)
def font(size, bold=False):
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, round(size * SCALE))
    return ImageFont.load_default(size=round(size * SCALE))


class Canvas:
    """Draw in logical pixels, render at 2x, and downsample for sharp text."""

    def __init__(self, bg=BG):
        self.image = Image.new("RGB", (W * SCALE, H * SCALE), bg)
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, box, fill, outline=None, width=1, radius=0):
        box = tuple(round(v * SCALE) for v in box)
        self.draw.rounded_rectangle(
            box, radius=round(radius * SCALE), fill=fill,
            outline=outline, width=max(1, round(width * SCALE)),
        )

    def line(self, points, fill, width=2):
        self.draw.line(
            [(round(x * SCALE), round(y * SCALE)) for x, y in points],
            fill=fill, width=max(1, round(width * SCALE)), joint="curve",
        )

    def text(self, pos, text, size=18, fill=INK, bold=False, anchor=None):
        self.draw.text(
            tuple(round(v * SCALE) for v in pos), text,
            font=font(size, bold), fill=fill, anchor=anchor,
        )

    def circle(self, center, radius, fill, outline=None, width=1):
        x, y = center
        self.draw.ellipse(
            tuple(round(v * SCALE) for v in (x-radius, y-radius, x+radius, y+radius)),
            fill=fill, outline=outline, width=max(1, round(width * SCALE)),
        )

    def arrow(self, start, end, color=BLUE, width=2):
        self.line([start, end], color, width)
        angle = atan2(end[1] - start[1], end[0] - start[0])
        size = 7
        for delta in (-pi / 6, pi / 6):
            tail = (end[0] - size*cos(angle+delta), end[1] - size*sin(angle+delta))
            self.line([tail, end], color, width)

    def finish(self):
        return self.image.resize((W, H), Image.Resampling.LANCZOS)
