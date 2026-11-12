"""Object and mechanism animations for the HacWM research card.

Data provenance (local source; no raw telemetry is distributed):
  Source: 期刊/HacWM/our历史实验/new_e1/A/data_all_202607180226_auto.csv
  UTF-8-SIG CSV; 2,880 samples.  This extract takes data-row indices
  0, 24, ..., 960 inclusive (41 points; nominally one sample every 2 min).
  Actual timestamp range: 2026-07-17 22:26:41 to 2026-07-17 23:46:42.
  Fields: 时间戳 -> elapsed minutes; 室内环境温度 -> Celsius.
  室内设定温度 is 27.0 throughout.  Values below are direct samples,
  not a fitted response; linear interpolation is only for animation playback.

The archive identifies a recorded AI-enabled AC run, but does not establish
the deployed model's version.  Therefore this renderer says Recorded AC trace,
not final HacWM result, and makes no energy-saving, baseline, or transfer claim.
The room, units, airflow, and warm/cool color field are schematic illustrations,
not measured spatial temperature or flow.  The right-hand rollouts, scores,
and execution cycle are entirely illustrative and use no experiment metrics.
"""

from __future__ import annotations

import math
from bisect import bisect_right

from research_pair_common import (
    AMBER, BG, BLUE, INK, LINE, MUTED, PANEL, TEAL, Canvas,
)


ELAPSED_MIN = (
    0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0,
    20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0,
    40.0, 42.0, 44.0, 46.0, 48.0, 49.983, 51.983, 53.983, 55.983,
    57.983, 59.983, 61.983, 63.983, 65.983, 67.983, 70.017, 72.017,
    74.017, 76.017, 78.017, 80.017,
)
TEMPERATURE_C = (
    32.1, 32.0, 32.0, 31.9, 31.8, 31.6, 31.5, 31.2, 30.9, 30.6,
    30.1, 29.8, 29.4, 29.0, 28.6, 28.3, 28.0, 27.6, 27.3, 27.0,
    26.9, 26.8, 26.9, 27.0, 27.3, 27.3, 27.4, 27.3, 27.2, 27.2,
    27.3, 27.3, 27.4, 27.5, 27.5, 27.5, 27.5, 27.4, 27.2, 27.0, 27.0,
)
def _mix(a, b, fraction):
    fraction = max(0.0, min(1.0, fraction))
    left = [int(a[index:index + 2], 16) for index in (1, 3, 5)]
    right = [int(b[index:index + 2], 16) for index in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * fraction):02x}"
                          for x, y in zip(left, right))


def _trace_at(minutes, values):
    index = min(len(ELAPSED_MIN) - 2, max(0, bisect_right(ELAPSED_MIN, minutes) - 1))
    fraction = (minutes - ELAPSED_MIN[index]) / (ELAPSED_MIN[index + 1] - ELAPSED_MIN[index])
    return values[index] + max(0.0, min(1.0, fraction)) * (values[index + 1] - values[index])


def _dashed(c, start, end, color=LINE, width=1):
    distance = math.dist(start, end)
    for step in range(0, max(1, int(distance)), 13):
        a, b = step / max(1.0, distance), min(1, (step + 7) / max(1.0, distance))
        c.line([(start[0] + a * (end[0] - start[0]), start[1] + a * (end[1] - start[1])),
                (start[0] + b * (end[0] - start[0]), start[1] + b * (end[1] - start[1]))],
               color, width=width)


def _bezier(points, count=55):
    a, b, d, e = points
    result = []
    for index in range(count):
        u = index / (count - 1)
        result.append(tuple((1-u)**3 * a[k] + 3*(1-u)**2*u*b[k]
                            + 3*(1-u)*u*u*d[k] + u**3*e[k] for k in (0, 1)))
    return result


def _moving_dot(c, path, fraction, color, radius=4):
    point = path[min(len(path) - 1, max(0, int(fraction * (len(path) - 1))))]
    c.circle(point, radius + 4, _mix(PANEL, color, 0.16))
    c.circle(point, radius, color)


def _fan(c, center, radius, rotation):
    c.circle(center, radius, "#f0f4f8", outline="#8da2b8", width=2)
    for n in range(3):
        a = rotation + n * math.tau / 3
        vertices = []
        for rr, aa in [(5, a), (radius * .84, a + .25),
                       (radius * .83, a + .85), (radius * .34, a + 1.08)]:
            vertices.append((center[0] + rr * math.cos(aa), center[1] + rr * math.sin(aa)))
        c.polygon(vertices, "#94a9bd")
    c.circle(center, 6, INK)


def hacwm_effect(t):
    """A schematic cooling scene alongside a faithfully sampled real trace."""
    t %= 1.0
    c = Canvas()
    # Hold both ends briefly; the loop reset is a replay, not a discontinuity
    # claimed to occur in the recorded physical experiment.
    progress = max(0.0, min(1.0, (t - .04) / .88))
    minutes = progress * ELAPSED_MIN[-1]
    temperature = _trace_at(minutes, TEMPERATURE_C)
    cooled = max(0.0, min(1.0, (32.1 - temperature) / 5.1))

    c.text((22, 17), "Cool the room", size=29, bold=True)
    c.text((511, 24), "HacWM", size=20, fill=MUTED, bold=True)
    c.text((22, 55), "Recorded AC trace · schematic room", size=19, fill=MUTED)

    # Cutaway room and outdoor unit.  The tint describes the measured scalar
    # room-temperature trend, without pretending to be a measured heat map.
    room_color = _mix("#fff0db", "#e7f3fa", cooled)
    c.rect((26, 91, 443, 248), room_color, radius=5)
    c.line([(27, 247), (27, 92), (443, 92), (443, 247)], "#aab9c9", width=3)
    c.line([(27, 247), (443, 247)], "#aab9c9", width=3)
    # Standing indoor cabinet (schematic, not a product rendering).
    c.rect((52, 107, 111, 237), PANEL, outline="#93a8bd", width=2, radius=13)
    c.rect((62, 119, 101, 144), "#dce9f2", radius=5)
    for y in range(155, 200, 9):
        c.line([(63, y), (100, y)], "#99aebf", width=2)
    c.circle((82, 218), 4, TEAL)
    c.text((130, 105), "Room", size=24, fill=MUTED)
    c.text((219, 101), f"{temperature:.1f}°C", size=30, fill=INK, bold=True)
    # A sofa and plant make the object spatially recognisable without extra
    # textual explanation; all movement remains illustrative.
    c.rect((292, 206, 403, 236), "#c5d6dd", radius=7)
    c.rect((300, 190, 395, 216), "#d3e1e7", radius=8)
    c.line([(302, 236), (302, 244)], "#8299a9", width=3)
    c.line([(392, 236), (392, 244)], "#8299a9", width=3)
    c.polygon([(416, 216), (433, 216), (429, 238), (420, 238)], "#d0b398")
    c.line([(424, 216), (424, 186)], TEAL, width=2)
    c.ellipse((410, 181, 425, 199), "#8ab7a4")
    c.ellipse((424, 190, 438, 209), "#72a892")
    # Two cooling ribbons and traveling particles, deliberately no CFD claim.
    for index, ending in enumerate(((370, 176), (314, 224))):
        path = _bezier(((103, 163 + index*14), (174, 156 + index*21),
                        (229, 171 + index*35), ending))
        c.line(path, "#c6deef", width=9)
        c.line(path, "#83b6d8", width=2)
        for particle in range(3):
            _moving_dot(c, path, (t*3 + particle/3) % 1, BLUE, radius=3)
        c.arrow(path[-4], path[-1], color="#83b6d8", width=2)

    # Refrigerant pipes through the room wall to the outdoor cabinet.
    c.line([(110, 218), (458, 218), (458, 153), (488, 153)], "#d2a287", width=3)
    c.line([(110, 226), (466, 226), (466, 165), (488, 165)], "#a8bfd1", width=3)
    c.rect((489, 127, 612, 219), PANEL, outline="#93a8bd", width=2, radius=8)
    _fan(c, (535, 172), 33, t*math.tau*4)
    for x in (580, 586, 592, 598):
        c.line([(x, 143), (x, 202)], "#b3c3cf", width=2)
    c.text((480, 228), "Outdoor unit", size=20, fill=MUTED)

    # Real trace: the full sampled run remains visible from frame zero;
    # playback highlights only the prefix observed at the shown instant.
    c.text((22, 263), "Indoor temperature", size=24, bold=True)
    c.text((432, 267), f"{minutes:02.0f} / 80 min", size=20, fill=MUTED)
    x0, x1, y0, y1 = 65, 610, 305, 357
    to_y = lambda value: y1 - (value - 26.4) / (32.4 - 26.4) * (y1-y0)
    xy = [(x0 + m/ELAPSED_MIN[-1]*(x1-x0), to_y(v))
          for m, v in zip(ELAPSED_MIN, TEMPERATURE_C)]
    for value in (32, 27):
        c.text((24, to_y(value)-10), str(value), size=18, fill=MUTED)
    _dashed(c, (x0, to_y(27)), (x1, to_y(27)), color="#a6c7b8")
    c.line(xy, "#c9d7df", width=3)
    seen = [point for point, elapsed in zip(xy, ELAPSED_MIN) if elapsed <= minutes]
    current = (x0 + progress*(x1-x0), to_y(temperature))
    if seen:
        c.line(seen + [current], TEAL, width=3)
    c.circle(current, 5, TEAL, outline=PANEL, width=1)
    c.text((22, 377), "Real trace; room and airflow are schematic", size=18, fill=MUTED)
    return c.finish()


def _future_path(x0, y0, x1, endpoint, bend):
    return [(x0+(x1-x0)*u, y0+(endpoint-y0)*(1-math.exp(-3*u))/(1-math.exp(-3))
             + bend*math.sin(math.pi*u)) for u in (index/49 for index in range(50))]


def hacwm_mechanism(t):
    """Moving rollout fan with scoring, a short action prefix, and a shifting horizon."""
    t %= 1.0
    c = Canvas()
    cycle = min(2, int(t*3))
    phase = (t*3) % 1
    c.text((22, 17), "Imagine, then act", size=29, bold=True)
    c.text((511, 24), "HacWM", size=20, fill=MUTED, bold=True)
    c.text((22, 55), "Action-conditioned world-model planning", size=19, fill=MUTED)

    c.text((40, 97), "History", size=24, bold=True)
    action = "Roll out futures" if phase < .40 else "Score & choose" if phase < .70 else "Act & replan"
    c.text((318, 97), action, size=25, fill=TEAL, bold=True)
    now_x, now_y = 203 + cycle*32, 173 + cycle*14
    end_x, target_y = now_x + 300, 231
    # This is a sliding prediction horizon, not a row of workflow rectangles.
    c.line([(39, 309), (603, 309)], LINE, width=2)
    c.arrow((591, 309), (607, 309), color=MUTED, width=1)
    _dashed(c, (now_x, 137), (now_x, 309), color="#93aac0")
    _dashed(c, (end_x, 137), (end_x, 309), color="#d1dce6")
    c.text((now_x-18, 315), "now", size=20, fill=MUTED)
    c.text((end_x-36, 315), "future", size=20, fill=MUTED)
    # A comfort/response reference provides a reason to compare candidates.
    _dashed(c, (now_x+20, target_y), (end_x+22, target_y), color="#a7cdbf")
    c.text((end_x-75, 244), "Target", size=20, fill=TEAL)

    history = _bezier(((40, 148), (91, 142), (now_x-52, now_y+13), (now_x, now_y)))
    c.line(history, TEAL, width=4)
    endpoints = (139, 181, 231, 276, 297)
    paths = [_future_path(now_x, now_y, end_x, endpoint, (i-2)*6)
             for i, endpoint in enumerate(endpoints)]
    selected = 2
    for index, path in enumerate(paths):
        c.line(path, "#c6d6e5", width=2)
        c.circle(path[-1], 4, "#a4b8cb")
    winner = paths[selected]
    c.line(winner, "#bedfd6", width=10)
    c.line(winner, TEAL, width=4)
    # Tiny cost bars sit beside each candidate end; shorter is preferable.
    # They are purely illustrative, without numeric experimental scores.
    for index, endpoint in enumerate(endpoints):
        length = (31, 20, 7, 18, 30)[index]
        color = TEAL if index == selected else "#aebfce"
        c.line([(end_x+14, endpoint), (end_x+14+length, endpoint)], color, width=4)
    if phase < .40:
        for index, path in enumerate(paths):
            _moving_dot(c, path, phase/.40, TEAL if index == selected else BLUE, radius=3)
    else:
        c.circle(winner[-1], 8, TEAL, outline=PANEL, width=2)
        c.line([(end_x-5, 231), (end_x-1, 235), (end_x+6, 226)], PANEL, width=2)

    # Execute a short action prefix. The paper executes multiple control steps
    # before replanning, rather than necessarily taking just one control step.
    # The next cycle advances now_x and
    # updates now_y before creating the next candidate fan.
    short_path = winner[:6]
    c.line(short_path, AMBER, width=5)
    c.circle((now_x, now_y), 6, TEAL, outline=PANEL, width=2)
    c.line([(now_x, 299), (now_x+36, 299)], AMBER, width=5)
    if phase >= .70:
        _moving_dot(c, short_path, (phase-.70)/.30, AMBER, radius=5)
        c.arrow((now_x+37, 298), (now_x+48, 298), color=AMBER, width=2)
    c.text((22, 350), "Short action prefix", size=22, fill=INK, bold=True)
    c.arrow((227, 364), (272, 364), color=AMBER, width=2)
    c.text((290, 350), "Observe & replan", size=24, fill=INK, bold=True)
    c.text((22, 379), "Illustrative rollouts · comfort, energy, smoothness", size=18, fill=MUTED)
    return c.finish()
