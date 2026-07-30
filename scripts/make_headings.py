#!/usr/bin/env python3
"""Build hd-*.svg -- a heading label plus a hairline running to the right
edge, one per section. Rendered as SVG (not markdown headers) because
GitHub strips <style> from READMEs, and an image is the only way to put
this page's own typeface on a heading."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

WIDTH, HEIGHT = 940, 26
WORDS = ["portrait", "system info", "ecosystem", "timeline", "about this readme"]


def build(word):
    fs = 16
    text_end = len(word) * fs * 0.62 + 18
    p = [svgkit.svg_open(WIDTH, HEIGHT, f"section: {word}"), svgkit.style_block()]
    p.append(svgkit.label(0, 18, svgkit.esc(word), fs, "ink", weight="600"))
    p.append(f'<line x1="{text_end:.0f}" y1="12.5" x2="{WIDTH}" y2="12.5" class="rule" stroke-width="1"/>')
    p.append("</svg>")
    return "".join(p)


def slug(word):
    return word.replace(" ", "-")


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    for word in WORDS:
        path = os.path.join(out_dir, f"hd-{slug(word)}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(word))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
