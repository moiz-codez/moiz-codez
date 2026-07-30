#!/usr/bin/env python3
"""Build hello.svg -- the "hi, it's me" banner.

tayyabadev's README opens with a big decorative ASCII-art name in a static
<pre> block. This keeps that spirit but borrows the portrait's own trick:
each row of the letterforms wipes in left-to-right with a cursor riding the
edge, the same clipPath animation ascii.svg uses, so the two pieces feel
like one system instead of two READMEs taped together.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

try:
    import pyfiglet
    BANNER_LINES = [l for l in pyfiglet.Figlet(font="big").renderText("HI IM MOIZ").split("\n")
                     if True][:-1]  # drop the trailing blank line figlet appends
    while BANNER_LINES and not BANNER_LINES[-1].strip():
        BANNER_LINES.pop()
except ImportError:
    # fallback if pyfiglet isn't installed when this is regenerated later
    BANNER_LINES = [
        " _    _ _____   _____ __  __   __  __  ____ _____ ______",
        "| |  | |_   _| |_   _|  \\/  | |  \\/  |/ __ \\_   _|___  /",
        "| |__| | | |     | | | \\  / | | \\  / | |  | || |    / / ",
        "|  __  | | |     | | | |\\/| | | |\\/| | |  | || |   / /  ",
        "| |  | |_| |_   _| |_| |  | | | |  | | |__| || |_ / /__ ",
        "|_|  |_|_____| |_____|_|  |_| |_|  |_|\\____/_____/_____|",
    ]

CHAR_W, LINE_H, FONT_SIZE = 10.6, 22, 17
PAD_X, PAD_TOP = 6, 10
ROW_DELAY = 0.11
SUBTITLE = "Full-Stack Developer  \u00b7  Agentic AI  \u00b7  Hyderabad, Sindh, Pakistan"
TAGLINE = "CS @ Mehran University  \u00b7  Execution Lead @ Verior  \u00b7  github.com/moiz-codez"


def build():
    cols = max(len(l) for l in BANNER_LINES)
    width = int(cols * CHAR_W + PAD_X * 2)
    banner_h = len(BANNER_LINES) * LINE_H
    sub_y = PAD_TOP + banner_h + 28
    tag_y = sub_y + 24
    height = tag_y + 18

    p = [svgkit.svg_open(width, height, "Hi, I'm Muhammad Moiz"), svgkit.style_block()]

    for i, line in enumerate(BANNER_LINES):
        y = PAD_TOP + i * LINE_H
        begin, end = i * ROW_DELAY, i * ROW_DELAY + ROW_DELAY
        w = max(len(line), 1) * CHAR_W
        safe = svgkit.esc(line)
        p.append(f'<clipPath id="hc{i}"><rect x="{PAD_X}" y="{y}" height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/></rect></clipPath>')
        p.append(f'<g clip-path="url(#hc{i})"><text xml:space="preserve" x="{PAD_X}" '
                 f'y="{y + FONT_SIZE - 1:.1f}" class="ink" font-size="{FONT_SIZE}" '
                 f'font-weight="600">{safe}</text></g>')
        p.append(f'<rect y="{y}" width="7" height="{LINE_H - 2}" class="data" opacity="0">'
                 f'<animate attributeName="x" from="{PAD_X}" to="{PAD_X + w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.7" begin="{begin:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/></rect>')

    banner_end = len(BANNER_LINES) * ROW_DELAY
    p.append(f'<g opacity="0">{svgkit.fade(banner_end + 0.15, 0.5)}'
             + svgkit.label(PAD_X, sub_y, svgkit.esc(SUBTITLE), 13.5, "dim", spacing="0.2") + '</g>')
    p.append(f'<g opacity="0">{svgkit.fade(banner_end + 0.35, 0.5)}'
             + svgkit.label(PAD_X, tag_y, svgkit.esc(TAGLINE), 11.5, "dim", spacing="0.2") + '</g>')

    p.append("</svg>")
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hello.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
