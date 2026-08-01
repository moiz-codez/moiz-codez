#!/usr/bin/env python3
"""Build timeline.svg with the current role highlighted as a live signal."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

WIDTH, HEIGHT = 1180, 230
AXIS_Y = 120
X0, X1 = 60, WIDTH - 60

MILESTONES = [
    ("2022", "Cadet College Petaro grad", "up"),
    ("2022", "B.S. CS begins, MUET", "down"),
    ("Jan '24", "QA Intern, Verior", "up"),
    ("Mar '24", "Execution Lead, Verior", "down"),
    ("'24\u2013'25", "IEEE Chapter Director", "up"),
    ("NOW", "Full-stack + agentic AI", "down"),
    ("2027", "B.S. CS, expected", "up"),
]


def build():
    n = len(MILESTONES)
    xs = [X0 + i * (X1 - X0) / (n - 1) for i in range(n)]

    p = [svgkit.svg_open(WIDTH, HEIGHT, "Timeline: the route so far"), svgkit.style_block()]
    p.append(f'<line x1="48" y1="40" x2="{WIDTH-48}" y2="40" class="rule" stroke-width="1"/>')
    p.append(svgkit.label(48, 28, "THE ROUTE SO FAR", 11, "dim", spacing="2.5"))
    p.append(svgkit.label(WIDTH - 48, 28, "FIG. 03", 11, "dim", "end", spacing="2.5"))

    axis_len = X1 - X0 + 12
    p.append(f'<line x1="{X0}" y1="{AXIS_Y}" x2="{X1}" y2="{AXIS_Y}" class="rule" stroke-width="1" '
             f'{svgkit.draw(0.15, 1.6, axis_len)}</line>')

    for i, (x, (year, text, side)) in enumerate(zip(xs, MILESTONES)):
        delay = 0.5 + i * 0.22
        is_now = year == "NOW"
        dot_r = 4.5 if is_now else 4
        dot_cls = "data" if is_now else "ink"

        p.append(f'<g opacity="0">{svgkit.fade(delay, 0.5)}')
        if is_now:
            p.append(f'<circle cx="{x:.1f}" cy="{AXIS_Y}" r="4" class="rule" fill="none" '
                      f'stroke-width="1"><animate attributeName="r" values="4;11;4" '
                      f'dur="2.4s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="opacity" values="0.8;0;0.8" dur="2.4s" '
                      f'begin="{delay:.2f}s" repeatCount="indefinite"/></circle>')
        p.append(f'<circle cx="{x:.1f}" cy="{AXIS_Y}" r="{dot_r}" class="{dot_cls}"/>')

        if side == "up":
            tick_y2, ty, ly = AXIS_Y - 24, AXIS_Y - 48, AXIS_Y - 32
        else:
            tick_y2, ty, ly = AXIS_Y + 24, AXIS_Y + 46, AXIS_Y + 30
        p.append(f'<line x1="{x:.1f}" y1="{AXIS_Y + (4 if side=="down" else -4)}" '
                 f'x2="{x:.1f}" y2="{tick_y2}" class="rule" stroke-width="1"/>')
        year_cls = "data" if is_now else "dim"
        p.append(svgkit.label(x, ty, svgkit.esc(year), 11.5, year_cls, "middle", weight="600" if is_now else None, spacing="1.5"))
        p.append(svgkit.label(x, ly, svgkit.esc(text), 10.3, "ink", "middle"))
        p.append('</g>')

    p.append("</svg>")
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "timeline.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
