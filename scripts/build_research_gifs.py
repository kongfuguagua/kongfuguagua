"""Rebuild the README's six paired GIFs with Python 3.10+ and Pillow 10+.

Run from any directory: python3 scripts/build_research_gifs.py
ADA and SOA are illustrations. HacWM's object view includes a recorded trace;
its room and all mechanism views are schematic. See scripts/README.md.
"""

from pathlib import Path

from PIL import Image, ImageColor

from research_ada_pair import ada_effect, ada_mechanism
from research_soa_pair import soa_effect, soa_mechanism
from research_hacwm_pair import hacwm_effect, hacwm_mechanism
from build_research_previews import build_preview

ROOT = Path(__file__).resolve().parents[1]
FRAME_COUNT = 72
FRAME_DURATION_MS = 110
RENDERERS = {
    "ada-effect": ada_effect,
    "ada-mechanism": ada_mechanism,
    "soa-effect": soa_effect,
    "soa-mechanism": soa_mechanism,
    "hacwm-effect": hacwm_effect,
    "hacwm-mechanism": hacwm_mechanism,
}


def build(name, render):
    frames = [render(i / FRAME_COUNT).convert("RGB") for i in range(FRAME_COUNT)]
    # A single palette keeps static labels stable throughout the animation.
    sample = Image.new("RGB", (200 * 8, 125))
    for index in range(8):
        sample.paste(frames[index * FRAME_COUNT // 8].resize((200, 125)), (index * 200, 0))
    # Preserve the original ink and accent colors: small text and thin strokes
    # otherwise get averaged into muted colors by the thumbnail sample.
    accents = [
        "#f6f8fa", "#ffffff", "#1f2937", "#59677a", "#d8e0ea", "#2563eb",
        "#0f766e", "#d48a19", "#eaf2ff", "#e7f1ef", "#e6b85c", "#9aadc3",
        "#b2c4dd", "#b3d4cd", "#e5edfc", "#eaf2fc",
    ]
    adaptive = sample.quantize(colors=240, method=Image.Quantize.MEDIANCUT)
    palette = Image.new("P", (1, 1))
    palette.putpalette(
        [channel for color in accents for channel in ImageColor.getrgb(color)]
        + adaptive.getpalette()[:240 * 3]
    )
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    output = ROOT / "assets" / "research" / f"{name}.gif"
    output.parent.mkdir(parents=True, exist_ok=True)
    provenance = (
        "Recorded historical AC temperature; schematic room. Model version unspecified."
        if name == "hacwm-effect" else
        "Illustrative physical system and method mechanics; not an experimental algorithm replay."
    )
    indexed[0].save(
        output, save_all=True, append_images=indexed[1:],
        duration=FRAME_DURATION_MS, loop=0, disposal=1, optimize=True,
        comment=provenance.encode("ascii"),
    )
    with Image.open(output) as image:
        duration = sum(
            _frame_duration(image, index) for index in range(image.n_frames)
        )
        print(f"{output.relative_to(ROOT)}: {image.n_frames} frames, "
              f"{duration / 1000:.1f}s, {output.stat().st_size / 1024:.0f} KiB")
    build_preview(output)


def _frame_duration(image, index):
    image.seek(index)
    return image.info.get("duration", 0)


if __name__ == "__main__":
    for name, renderer in RENDERERS.items():
        build(name, renderer)
