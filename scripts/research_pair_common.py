"""Drawing primitives for paired object / mechanism research animations."""

from PIL import Image, ImageDraw

from research_animation_common import (
    AMBER, BG, BLUE, INK, LINE, MUTED, PANEL, TEAL,
    Canvas as OriginalCanvas,
)

W, H, SCALE = 640, 400, 2


class Canvas(OriginalCanvas):
    def __init__(self, bg=BG):
        self.image = Image.new("RGB", (W * SCALE, H * SCALE), bg)
        self.draw = ImageDraw.Draw(self.image)

    def polygon(self, points, fill, outline=None, width=1):
        vertices = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
        self.draw.polygon(vertices, fill=fill)
        if outline:
            self.draw.line(vertices + [vertices[0]], fill=outline,
                           width=max(1, round(width * SCALE)), joint="curve")

    def ellipse(self, box, fill, outline=None, width=1):
        self.draw.ellipse(tuple(round(v * SCALE) for v in box), fill=fill,
                          outline=outline, width=max(1, round(width * SCALE)))

    def finish(self):
        return self.image.resize((W, H), Image.Resampling.LANCZOS)
