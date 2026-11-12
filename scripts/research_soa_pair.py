"""PV objects and fuzzy-guided model edits, rendered as physical illustrations.

The paper's PV-array calibration motivates the subject. Curves here are
generated from a normalized one-diode equation, NOT measurements or an SOA
optimization replay. The candidate schedule is an explanatory animation.
"""

from math import cos, expm1, pi, sin

from research_pair_common import (
    AMBER, BG, BLUE, INK, LINE, MUTED, PANEL, TEAL, Canvas,
)


def _iv(voltage, voc=1.0, photocurrent=1.0, rs=0.035, rsh=24.0):
    """Solve an illustrative normalized one-diode PV current by bisection."""
    thermal = voc * 0.085
    saturation = photocurrent / expm1(voc / thermal)

    def residual(current):
        junction = voltage + current * rs
        return photocurrent - saturation * expm1(junction / thermal) - junction / rsh - current

    if residual(0.0) <= 0:
        return 0.0
    lo, hi = 0.0, photocurrent
    for _ in range(30):
        mid = (lo + hi) / 2
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _progress(t):
    return max(0.0, min(1.0, (t - 0.08) / 0.72))


def _curve(voc=1.0, photocurrent=1.0, rs=0.035, rsh=24.0, box=(290, 130, 605, 290)):
    x0, y0, x1, y1 = box
    return [(x0 + i / 80 * (x1-x0),
             y1 - _iv(i / 80 * 1.12, voc, photocurrent, rs, rsh) * (y1-y0) / 1.12)
            for i in range(81)]


def _module(c, x, y, w=62, h=45):
    c.polygon([(x+9,y),(x+w,y),(x+w-9,y+h),(x,y+h)], "#245492", outline="#163d70", width=2)
    for index in (1, 2, 3):
        u = index / 4
        c.line([(x+9+(w-9)*u,y+2),(x+(w-9)*u,y+h-2)], "#86b4e5", 1)
    c.line([(x+5,y+h/2),(x+w-5,y+h/2)], "#86b4e5", 1)
    c.line([(x+12,y+h),(x+9,y+h+8)], MUTED, 2)
    c.line([(x+w-12,y+h),(x+w-15,y+h+8)], MUTED, 2)


def soa_effect(t):
    c = Canvas()
    progress = _progress(t)
    c.text((24, 16), "Photovoltaic model matching", size=29, bold=True)
    c.text((24, 57), "A digital response moves toward the reference.", size=22, fill=MUTED)

    # A physical PV array rather than a generic process box.
    c.circle((82, 118), 19, "#e9bb5d")
    for index in range(8):
        angle = index*pi/4
        c.line([(82+25*cos(angle),118+25*sin(angle)),
                (82+32*cos(angle),118+32*sin(angle))], AMBER, 2)
    for row in range(2):
        for col in range(3):
            _module(c, 31+col*68+row*5, 169+row*67)
    for index in range(4):
        u = (t*1.7+index/4) % 1
        c.circle((112+42*u, 131+28*u), 3, "#e9bb5d")
    c.text((42, 313), "PV array", size=25, bold=True)
    c.line([(236, 219),(263,219)], BLUE, 3)
    c.circle((238+23*((t*2)%1),219), 4, TEAL)

    # Both curves are physics-generated. There are no measured performance data.
    c.line([(290,126),(290,290),(605,290)], LINE, 2)
    c.line(_curve(), TEAL, 3)
    candidate = _curve(voc=0.60+0.40*progress,
                       photocurrent=0.76+0.24*progress,
                       rs=0.12-0.085*progress, rsh=8+16*progress)
    c.line(candidate, BLUE, 4)
    cursor = 20+int(30*((t*1.4)%1))
    c.circle(candidate[cursor], 5, BLUE, outline=PANEL, width=2)
    c.text((292, 94), "Current", size=21, fill=MUTED)
    c.text((520, 300), "Voltage", size=20, fill=MUTED)
    c.line([(301,342),(324,342)], TEAL, 3)
    c.text((333,330), "Reference", size=20, fill=TEAL)
    c.line([(459,342),(482,342)], BLUE, 3)
    c.text((491,330), "Candidate", size=20, fill=BLUE)
    c.text((24, 372), "Physics-based illustration · simulated signals", size=19, fill=MUTED)
    return c.finish()


def _resistor(c, start, end, color):
    x0,y0 = start
    x1,y1 = end
    dx,dy=x1-x0,y1-y0
    points=[start]
    for i in range(1,9):
        u=i/9
        offset=7 if i%2 else -7
        points.append((x0+dx*u+(offset if dy else 0), y0+dy*u+(offset if dx else 0)))
    c.line(points+[end],color,3)


def soa_mechanism(t):
    c=Canvas()
    stage=min(2,int(t*3))
    c.text((24,16), "Edit the electrical model", size=29, bold=True)
    c.text((24,57), "Structure, parameters, and fuzzy-weighted candidates.", size=22, fill=MUTED)

    # A recognizable equivalent PV circuit; colored components show which
    # part of a candidate is being revised, without pipeline/flowchart boxes.
    wire="#6a7c91"
    c.line([(78,126),(410,126)],wire,3)
    _resistor(c,(410,126),(479,126),BLUE if stage==1 else wire)
    c.line([(479,126),(560,126)],wire,3)
    c.line([(560,222),(78,222),(78,192)],wire,3)
    c.line([(78,126),(78,146)],wire,3)
    c.circle((78,169),23,PANEL,outline=TEAL,width=3)
    c.arrow((78,182),(78,155),TEAL,2)
    c.text((27,147), "Iph",size=20,fill=TEAL)
    c.line([(220,126),(220,150)],wire,3)
    c.polygon([(207,151),(233,151),(220,176)],"#dce9fa",outline=BLUE,width=2)
    c.line([(205,179),(235,179)],BLUE,3)
    c.line([(220,179),(220,222)],wire,3)
    c.text((241,153),"D",size=21,fill=BLUE)
    c.line([(339,126),(339,147)],wire,3)
    _resistor(c,(339,147),(339,198),TEAL if stage==2 else wire)
    c.line([(339,198),(339,222)],wire,3)
    c.text((355,163),"Rsh",size=20,fill=TEAL if stage==2 else MUTED)
    c.text((427,91),"Rs",size=21,fill=BLUE if stage==1 else MUTED)
    c.circle((560,126),5,PANEL,outline=BLUE,width=2)
    c.circle((560,222),5,PANEL,outline=BLUE,width=2)
    c.text((577,161),"V / I",size=20,fill=MUTED)

    # A candidate branch is proposed and retained, showing topology edits.
    branch=AMBER if stage==0 else "#9eb7cf"
    c.line([(135,126),(135,147)],branch,2)
    _resistor(c,(135,147),(135,198),branch)
    c.line([(135,198),(135,222)],branch,2)
    c.circle((135,126),5,branch)
    travel=(t*3)%1
    c.circle((410+68*travel,126),4,BLUE)

    c.text((27,254),"Candidate models",size=23,bold=True)
    c.text((355,254),"Fuzzy weights",size=23,bold=True)
    colors=["#a8bfdc",BLUE,TEAL]
    for j,color in enumerate(colors):
        # A compact ensemble of possible I–V responses, not a result chart.
        points=[]
        for i in range(41):
            u=i/40
            points.append((30+245*u,337-(42-5*j)*(1-u**(4+j))))
        c.line(points,color,3 if j==stage else 2)
        c.circle((288,302+j*19),6 if j==stage else 3,color)
    # Membership functions vary the candidate reference weights continuously.
    for j,color in enumerate(colors):
        center=390+j*83
        c.line([(center-40,342),(center,287),(center+40,342)],color,2)
    x=372+190*(0.5-0.5*cos(2*pi*t))
    c.line([(x,284),(x,346)],AMBER,2)
    for j,color in enumerate(colors):
        weight=max(0,1-abs(x-(390+j*83))/40)
        if weight>0:
            c.circle((390+j*83,353),4+6*weight,color)
    c.text((355,365),"Mismatch + uncertainty",size=18,fill=MUTED)
    c.text((24,372),"Illustrative model edits",size=19,fill=MUTED)
    return c.finish()
