# Paired research animations

Rebuild the six GIFs used by the profile README with Python 3.10+ and Pillow 10+:

```sh
python3 scripts/build_research_gifs.py
```

The script works from any directory when invoked with its full path. It writes
`assets/research/{ada,soa,hacwm}-{effect,mechanism}.gif` and updates their linked
360 × 225 display copies under `assets/research/previews/`. Each full-size
640 × 400 animation loops in about eight seconds. Every first frame contains a
complete overview for visitors who disable GIF autoplay. The README pairs the
object view on the left with the mechanism view on the right in Markdown tables.
The previews have a natural width of 360 pixels, so the two columns fit typical
desktop README widths without relying on HTML width attributes. Each preview
links to the full-size original.

To rebuild only the display copies from existing GIFs:

```sh
python3 scripts/build_research_previews.py
```

## Sources and interpretation

- **ADA:** generation, transmission, city loads, and redispatch are schematic.
  Candidate searches and physical-constraint screening explain the method;
  they are not L2RPN results or a real grid deployment replay.
- **SOA:** the subject is the PV-array calibration task described in the research
  paper. A normalized one-diode equation generates the I–V curves. Candidate
  schedules, component edits, and fuzzy weights are teaching illustrations,
  not measured responses or a recorded SOA optimization trajectory.
- **HacWM object view:** indoor temperatures are 41 direct samples from a local
  historical AC experiment, with interpolation for animation playback. The
  embedded values and exact file/field/time provenance are documented in
  `research_hacwm_pair.py`; no complete telemetry logs are distributed. The
  record does not establish the deployed model version, so it supports no
  final-model, energy-saving, baseline, or cross-model performance claim.
- **HacWM mechanism:** the room, airflow, candidate rollouts, scores, and planning
  horizon are illustrative. The room tint is not a measured spatial heat map.
  The planner executes a short prefix of control actions before replanning;
  the animation does not imply exactly one control step per planning cycle.

## Renderers

- `research_ada_pair.py`: grid behavior and constrained candidate exploration.
- `research_soa_pair.py`: PV objects and equivalent-circuit model refinement.
- `research_hacwm_pair.py`: recorded AC trace and receding-horizon planning.
- `research_pair_common.py`: 640 × 400 canvas and object drawing primitives.
- `research_animation_common.py`: shared colors, fonts, and antialiasing.

The published profile and default builder include only the paired views above.
