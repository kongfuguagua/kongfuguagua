# Research concept animations

Rebuild the four GIFs used by the profile README with Python 3.10+ and Pillow 10+:

```sh
python3 scripts/build_research_gifs.py
```

The script works from any directory when invoked with its full path. It writes
`assets/research/{ada,soa,hacwm,solarjepa}.gif` in this repository. The animations
use an 800 × 360 canvas, a shared palette, and a 7.2-second loop. Every first frame
contains a complete overview for visitors who disable GIF autoplay.

All signals, grid states, cloud shapes, and trajectories are synthetic teaching
illustrations. These assets contain no paper figures, experimental data, or
performance claims. The original SVG overviews remain available alongside the GIFs.

- `research_agentic.py`: ADA's two feedback loops and SOA's model refinement.
- `research_world_models.py`: HacWM's receding-horizon planning and SolarJEPA's
  alignment of historical observations for future forecasting.
- `research_animation_common.py`: colors, fonts, and antialiased drawing helpers.
