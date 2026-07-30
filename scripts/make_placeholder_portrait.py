#!/usr/bin/env python3
"""Build a stand-in for ascii.svg until make_portrait.py has a real photo to run.

assets/profile.jpg doesn't exist yet in this build, so instead of shipping a
broken image tag, this draws a generic head-and-shoulders silhouette with the
same character ramp and the same row-by-row typewriter reveal that the real
portrait will use. Swap it out by running:

    python3 scripts/make_portrait.py assets/profile.jpg
    python3 scripts/embed_portrait_font.py

Both scripts always overwrite ascii.svg, so this placeholder is disposable.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

RAMP = " .`:-=+*#%@"          # sparse -> dense, same alphabet the real portrait uses
COLS, ROWS = 58, 30
CHAR_W, LINE_H, FONT_SIZE = 7.9, 16, 13.0
PAD = 16
ROW_DELAY = 0.045


def shade(cx, cy):
    """1.0 at the silhouette core, falling off softly at the edge -- the same
    kind of soft boundary a real bilateral-filtered photo produces, so the
    placeholder sits comfortably next to the real thing once it exists."""
    # head: circle: shoulders: wide flattened ellipse anchored below it
    head_r = 7.6
    hx, hy = COLS / 2, ROWS * 0.34
    d_head = math.hypot(cx - hx, cy - hy) - head_r

    sx, sy = COLS / 2, ROWS * 0.86
    sa, sb = 17.5, 11.5
    dy = cy - sy
    d_sh = math.hypot((cx - sx) / sa, max(dy, 0) / sb) - 1.0 if dy > -sb * 0.2 else 999

    d = min(d_head, d_sh)
    if d > 1.6:
        return 0.0
    if d < -1.2:
        return 1.0
    return max(0.0, min(1.0, 0.5 - d / 2.4))


def to_lines():
    n = len(RAMP)
    out = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            v = shade(c + 0.5, r + 0.5)
            row.append(RAMP[min(n - 1, int(v * n))])
        out.append("".join(row).rstrip())
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def build(lines):
    width = int(COLS * CHAR_W + PAD * 2)
    height = len(lines) * LINE_H + PAD * 2 + 34  # + room for the caption
    p = [svgkit.svg_open(width, height, "Placeholder portrait -- add assets/profile.jpg"),
         svgkit.style_block(".cap{fill:none}")]

    for i, line in enumerate(lines):
        y = PAD + i * LINE_H
        begin, end = i * ROW_DELAY, (i + 1) * ROW_DELAY
        w = max(len(line), 1) * CHAR_W
        safe = svgkit.esc(line)
        p.append(f'<clipPath id="pc{i}"><rect x="{PAD}" y="{y}" height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" '
                 f'begin="{begin:.3f}s" dur="{ROW_DELAY}s" fill="freeze"/></rect></clipPath>')
        p.append(f'<g clip-path="url(#pc{i})"><text xml:space="preserve" x="{PAD}" '
                 f'y="{y + 11.4:.1f}" class="data" font-size="{FONT_SIZE}">{safe}</text></g>')
        p.append(f'<rect y="{y + 1}" width="6" height="12" class="data" opacity="0">'
                 f'<animate attributeName="x" from="{PAD}" to="{PAD + w:.1f}" '
                 f'begin="{begin:.3f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.75" begin="{begin:.3f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{end:.3f}s"/></rect>')

    cap_y = len(lines) * LINE_H + PAD + 22
    cap_delay = len(lines) * ROW_DELAY + 0.15
    p.append(f'<g opacity="0">{svgkit.fade(cap_delay, 0.5)}'
             + svgkit.label(PAD, cap_y, "placeholder -- run make_portrait.py on assets/profile.jpg",
                             10.5, "dim", spacing="0.2") + '</g>')
    p.append("</svg>")
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ascii.svg")
    svg = build(to_lines())
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
