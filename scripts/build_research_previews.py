"""Build naturally sized, linked GIF previews for the README's two-column rows.

Run: python3 scripts/build_research_previews.py
The full-size originals remain in assets/research. No paper data is changed.
"""

from pathlib import Path

from PIL import Image, ImageColor

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("ada", "soa", "hacwm")
WIDTH, HEIGHT = 360, 225
ACCENTS = (
    "#f6f8fa", "#ffffff", "#1f2937", "#59677a", "#d8e0ea", "#2563eb",
    "#0f766e", "#d48a19", "#eaf2ff", "#e7f1ef", "#e6b85c", "#9aadc3",
    "#b2c4dd", "#b3d4cd", "#e5edfc", "#eaf2fc",
)


def build_preview(source):
    frames, durations = [], []
    with Image.open(source) as gif:
        metadata = gif.info.copy()
        for index in range(gif.n_frames):
            gif.seek(index)
            frames.append(gif.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS))
            durations.append(gif.info["duration"])
    sample = Image.new("RGB", (180 * 8, 113))
    for index in range(8):
        frame = frames[index * len(frames) // 8]
        sample.paste(frame.resize((180, 113)), (index * 180, 0))
    adaptive = sample.quantize(colors=240, method=Image.Quantize.MEDIANCUT)
    palette = Image.new("P", (1, 1))
    palette.putpalette(
        [channel for color in ACCENTS for channel in ImageColor.getrgb(color)]
        + adaptive.getpalette()[:720]
    )
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    destination = source.parent / "previews" / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(
        destination, save_all=True, append_images=indexed[1:],
        duration=durations, loop=metadata.get("loop", 0), disposal=1,
        optimize=True, comment=metadata.get("comment", b""),
    )
    print(f"{destination.relative_to(ROOT)}: {WIDTH}x{HEIGHT}, "
          f"{sum(durations) / 1000:.2f}s, {destination.stat().st_size // 1024} KiB")


if __name__ == "__main__":
    for name in NAMES:
        for kind in ("effect", "mechanism"):
            build_preview(ROOT / "assets" / "research" / f"{name}-{kind}.gif")
