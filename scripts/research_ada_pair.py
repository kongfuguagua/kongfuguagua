"""ADA object and search-space illustrations, independent of experimental data."""

from math import cos, floor, pi, sin

from research_pair_common import (
    AMBER, BG, BLUE, INK, LINE, MUTED, PANEL, TEAL, Canvas,
)


def _mix(a, b, p):
    p = min(1.0, max(0.0, p))
    channels = zip(
        (int(a[i:i + 2], 16) for i in (1, 3, 5)),
        (int(b[i:i + 2], 16) for i in (1, 3, 5)),
    )
    return "#" + "".join(f"{round(x + (y - x) * p):02x}" for x, y in channels)


def _smooth(a, b, t):
    p = min(1.0, max(0.0, (t - a) / (b - a)))
    return p * p * (3 - 2 * p)


def _heading(c, title, subtitle):
    c.text((22, 15), title, size=29, bold=True)
    c.text((618, 57), "ILLUSTRATIVE", size=18, fill=MUTED, anchor="rm")
    c.text((23, 72), subtitle, size=19, fill=MUTED)


def _point_on_path(points, p):
    lengths = [
        ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        for a, b in zip(points, points[1:])
    ]
    distance = min(1.0, max(0.0, p)) * sum(lengths)
    for a, b, length in zip(points, points[1:], lengths):
        if distance <= length:
            q = distance / length if length else 0.0
            return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)
        distance -= length
    return points[-1]


def _partial_path(c, points, p, color, width=3):
    lengths = [
        ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        for a, b in zip(points, points[1:])
    ]
    distance = min(1.0, max(0.0, p)) * sum(lengths)
    for a, b, length in zip(points, points[1:], lengths):
        if distance >= length:
            c.line([a, b], color, width)
            distance -= length
        else:
            q = distance / length if length else 0.0
            c.line([a, (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)], color, width)
            return


def _flow(c, points, t, color, width=4, density=3):
    c.line(points, _mix(PANEL, color, 0.56), width)
    for i in range(density):
        p = (t + i / density) % 1.0
        position = _point_on_path(points, p)
        c.circle(position, 4, color)


def _tower(c, x, y):
    c.line([(x - 15, y + 22), (x, y - 27), (x + 15, y + 22)], MUTED, 3)
    c.line([(x - 12, y + 9), (x + 12, y + 9), (x - 8, y - 5), (x + 8, y - 5)], MUTED, 2)
    c.line([(x - 22, y - 10), (x + 22, y - 10)], MUTED, 3)
    c.line([(x - 17, y - 20), (x + 17, y - 20)], MUTED, 3)
    c.line([(x - 21, y + 23), (x + 21, y + 23)], MUTED, 3)
    for offset in (-19, 19):
        c.line([(x + offset, y - 10), (x + offset, y - 3)], BLUE, 2)


def _station(c, x, y):
    c.rect((x - 33, y - 10, x + 33, y + 29), PANEL, outline=MUTED, width=2, radius=3)
    c.rect((x - 23, y - 34, x - 12, y - 10), _mix(PANEL, BLUE, 0.10), outline=MUTED, width=2)
    c.rect((x + 1, y - 25, x + 12, y - 10), _mix(PANEL, BLUE, 0.10), outline=MUTED, width=2)
    c.line([(x - 40, y + 29), (x + 40, y + 29)], MUTED, 2)
    c.polygon([(x + 2, y - 4), (x - 10, y + 12), (x, y + 12), (x - 3, y + 25), (x + 13, y + 6), (x + 2, y + 6)], AMBER)
    for offset in (-24, 21):
        c.rect((x + offset, y + 2, x + offset + 5, y + 14), _mix(PANEL, BLUE, 0.30), radius=1)


def _solar(c, x, y):
    c.circle((x + 29, y - 24), 11, _mix(PANEL, AMBER, 0.17), outline=AMBER, width=2)
    for angle in (0, pi / 2, pi, 3 * pi / 2):
        c.line([(x + 29 + 15 * cos(angle), y - 24 + 15 * sin(angle)), (x + 29 + 20 * cos(angle), y - 24 + 20 * sin(angle))], AMBER, 2)
    c.polygon([(x - 39, y - 8), (x + 20, y - 8), (x + 31, y + 22), (x - 28, y + 22)], _mix(PANEL, BLUE, 0.16), outline=BLUE, width=2)
    c.line([(x - 35, y + 2), (x + 24, y + 2)], PANEL, 2)
    c.line([(x - 31, y + 12), (x + 28, y + 12)], PANEL, 2)
    for dx in (-19, 1):
        c.line([(x + dx, y - 7), (x + dx + 11, y + 21)], PANEL, 2)
    c.line([(x - 16, y + 22), (x - 16, y + 30), (x + 20, y + 30)], MUTED, 2)


def _city(c, x, y, demand):
    color = _mix(BLUE, AMBER, demand)
    heights = (32, 54, 42, 63)
    for i, height in enumerate(heights):
        left = x - 42 + 22 * i
        top = y + 26 - height
        c.rect((left, top, left + 18, y + 26), _mix(PANEL, color, 0.09), outline=MUTED, width=2, radius=2)
        for row in range(max(1, (height - 10) // 13)):
            for col in (0, 1):
                c.rect((left + 4 + col * 7, top + 7 + row * 13, left + 7 + col * 7, top + 12 + row * 13), color, radius=1)
    c.line([(x - 50, y + 28), (x + 51, y + 28)], MUTED, 2)


def ada_effect(t):
    """Demand rises and a dispatch action distributes schematic grid flows."""
    t %= 1.0
    c = Canvas()
    _heading(c, "ADA · Grid response", "Changing load, adaptive dispatch.")
    c.rect((20, 105, 620, 348), PANEL, outline=LINE, radius=16)

    # These are scene elements, not a specific network or L2RPN rollout.
    c.ellipse((46, 117, 183, 205), _mix(PANEL, TEAL, 0.055))
    c.ellipse((415, 117, 593, 213), _mix(PANEL, BLUE, 0.045))
    c.ellipse((415, 246, 592, 336), _mix(PANEL, BLUE, 0.045))
    reset = 1 - _smooth(0.89, 1.0, t)
    demand = _smooth(0.13, 0.38, t) * reset
    reroute = _smooth(0.40, 0.73, t) * reset
    pressure = demand * (1 - 0.85 * reroute)

    source_top, source_lower = (105, 162), (105, 270)
    hub_top, hub_lower = (286, 188), (309, 279)
    city_top, city_lower = (512, 172), (512, 278)
    c.ellipse((city_top[0] - 66 - 7 * demand, city_top[1] - 58 - 7 * demand, city_top[0] + 65 + 7 * demand, city_top[1] + 36 + 7 * demand), _mix(PANEL, AMBER, 0.055 * demand))

    _flow(c, [source_top, hub_top], 2.2 * t, BLUE, density=3)
    _flow(c, [source_lower, hub_top], 2.6 * t + 0.1, BLUE, density=3)
    _flow(c, [hub_top, city_top], (2.2 + 1.3 * demand) * t, _mix(BLUE, AMBER, pressure), width=4 + 3 * pressure, density=4)
    _flow(c, [source_lower, hub_lower], 2.4 * t + 0.2, _mix(BLUE, TEAL, reroute), width=4 + reroute, density=3)
    _flow(c, [hub_top, hub_lower], 2.0 * t + 0.3, BLUE, width=3, density=2)
    _flow(c, [hub_lower, city_top], 2.7 * t + 0.15, _mix(LINE, TEAL, 0.15 + 0.85 * reroute), width=3 + 3 * reroute, density=2 + int(reroute > 0.5))
    _flow(c, [hub_lower, city_lower], 2.4 * t + 0.2, BLUE, density=3)

    _solar(c, *source_top)
    _station(c, *source_lower)
    _tower(c, *hub_top)
    _tower(c, *hub_lower)
    _city(c, *city_top, demand)
    _city(c, *city_lower, 0.05)

    c.text((104, 328), "Generation", size=24, bold=True, anchor="mm")
    c.text((299, 328), "Grid", size=24, bold=True, anchor="mm")
    c.text((513, 328), "City load", size=24, bold=True, anchor="mm")
    if reroute > 0.2:
        caption, accent = "Dispatch redistributes the flow", TEAL
    elif demand > 0.2:
        caption, accent = "A load shift changes line loading", AMBER
    else:
        caption, accent = "Power flows from sources to loads", BLUE
    c.circle((31, 376), 5, accent)
    c.text((46, 362), caption, size=24, fill=accent, bold=True)
    return c.finish()


def _cross(c, point, color=AMBER):
    x, y = point
    c.circle(point, 10, _mix(PANEL, color, 0.10))
    c.line([(x - 5, y - 5), (x + 5, y + 5)], color, 3)
    c.line([(x - 5, y + 5), (x + 5, y - 5)], color, 3)


def ada_mechanism(t):
    """MCTS-like candidate branches meet constraints while experience updates."""
    t %= 1.0
    c = Canvas()
    _heading(c, "ADA · Search and learn", "Fast search, slower knowledge updates.")
    c.rect((20, 105, 620, 326), PANEL, outline=LINE, radius=16)

    broad = [(57, 285), (93, 191), (197, 143), (365, 138), (532, 168), (577, 249), (480, 304), (233, 314), (103, 309)]
    learned = [(76, 282), (122, 201), (224, 165), (357, 160), (478, 189), (520, 242), (443, 283), (232, 302), (119, 295)]
    slow = _smooth(0.22, 0.87, t)
    feasible = [(x + (u - x) * slow, y + (v - y) * slow) for (x, y), (u, v) in zip(broad, learned)]
    c.polygon(broad, _mix(PANEL, BLUE, 0.025), outline=LINE, width=1)
    c.polygon(feasible, _mix(PANEL, BLUE, 0.07), outline=BLUE, width=2)
    c.polygon([(494, 143), (600, 143), (600, 229), (539, 204)], _mix(PANEL, AMBER, 0.09))
    c.polygon([(483, 280), (600, 248), (600, 310), (514, 310)], _mix(PANEL, AMBER, 0.07))

    c.text((37, 116), "Tool-guided candidates", size=24, bold=True)
    c.text((597, 123), "Physical limits", size=19, fill=AMBER, anchor="rm")

    candidates = [
        [(80, 276), (153, 244), (232, 226), (306, 196), (398, 188), (477, 205)],
        [(80, 276), (153, 240), (222, 192), (299, 166), (400, 146), (514, 153)],
        [(80, 276), (161, 274), (251, 281), (334, 266), (428, 274), (554, 294)],
        [(80, 276), (151, 253), (216, 241), (302, 222), (391, 215), (473, 241)],
    ]
    for points in candidates:
        c.line(points, _mix(PANEL, BLUE, 0.24), 2)
        for point in points[1:-1]:
            c.circle(point, 3, PANEL, outline=_mix(PANEL, BLUE, 0.48), width=1)

    # The two unsafe branches are visibly screened even when autoplay is off.
    _cross(c, candidates[1][-1])
    _cross(c, candidates[2][-1])
    for point in (candidates[0][-1], candidates[3][-1]):
        c.circle(point, 7, _mix(PANEL, TEAL, 0.12), outline=TEAL, width=2)
    c.rect((337, 298, 489, 321), PANEL, radius=6)
    c.text((413, 309), "Feasible region", size=19, fill=BLUE, anchor="mm")

    fast = (4 * t) % 1.0
    branch = int(floor(4 * t)) % 4
    path = candidates[branch]
    rejected = branch in (1, 2)
    _partial_path(c, path, min(1.0, fast * 1.18), AMBER if rejected else TEAL, 4)
    cursor = _point_on_path(path, min(1.0, fast * 1.18))
    c.circle(cursor, 6, AMBER if rejected else TEAL, outline=PANEL, width=2)
    c.circle((80, 276), 7, BLUE, outline=PANEL, width=2)

    # Tool probes enlarge the observed state, then physical feedback judges trials.
    probe = path[min(4, max(1, int(fast * 5)))]
    pulse = (sin(2 * pi * fast) + 1) / 2
    c.circle(probe, 10 + 5 * pulse, None, outline=_mix(PANEL, BLUE, 0.25 + 0.35 * pulse), width=2)
    if fast > 0.83 and rejected:
        _cross(c, path[-1])

    c.text((25, 341), "Slow knowledge", size=24, bold=True, fill=TEAL)
    c.line([(246, 356), (605, 356)], LINE, 2)
    known = 3 + int(t * 10)
    for i in range(13):
        x = 248 + 29 * i
        filled = i < known
        c.circle((x, 356), 5 if filled else 4, TEAL if filled else PANEL, outline=TEAL if filled else LINE, width=2)
    c.text((25, 377), "Experience reshapes the feasible region.", size=19, fill=MUTED)
    return c.finish()
