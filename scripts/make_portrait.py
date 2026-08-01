#!/usr/bin/env python3
"""Turn assets/profile.jpg into ascii.svg -- the real, photo-based portrait."""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

RAMP = " .`:-=+*cs#%@"     # bright/sparse -> dark/dense; leading space = blank
COLS = 90                  # below ~88 the face muddies; far above it dominates
CLAHE_CLIP = 3.0           # higher amplifies skin texture into noise
GAMMA = 1.0                # ramp-mapping exponent
CURVE = 1.7                # the darkening curve -- the difference-maker
ROW_RATIO = 0.48           # monospace cells run about twice as tall as wide

CHAR_W = 7.74               # advance width the whole grid assumes
FONT_SIZE = 12.9
LINE_H = 15
ROW_DELAY = 0.09            # per-row stagger, seconds


def prep(path, crop=None):
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import remove

    src = Image.open(path).convert("RGBA")
    if crop:
        src = src.crop(crop)

    cut = remove(src)
    alpha = np.array(cut.split()[-1])

    white = Image.new("RGBA", cut.size, (255, 255, 255, 255))
    gray = np.array(Image.alpha_composite(white, cut).convert("L"))

    gray = cv2.bilateralFilter(gray, 11, 50, 50)
    gray = cv2.createCLAHE(clipLimit=CLAHE_CLIP, tileGridSize=(8, 8)).apply(gray)
    gray = (255.0 * (gray / 255.0) ** CURVE).astype("uint8")
    gray[alpha < 20] = 255
    return Image.fromarray(gray)


def to_lines(img, cols=COLS, gamma=GAMMA):
    from PIL import Image
    w, h = img.size
    rows = int(cols * (h / w) * ROW_RATIO)
    img = img.resize((cols, rows), Image.LANCZOS)
    px = list(img.getdata())
    n = len(RAMP)

    out = []
    for r in range(rows):
        out.append("".join(
            RAMP[min(n - 1, int((1 - px[r * cols + c] / 255.0) ** gamma * n))]
            for c in range(cols)
        ).rstrip())

    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def build_svg(lines, cols=COLS):
    pad = 14
    width = int(cols * CHAR_W + pad * 2)
    height = len(lines) * LINE_H + pad * 2

    p = [svgkit.svg_open(width, height, "Muhammad Moiz"), svgkit.style_block()]

    for i, line in enumerate(lines):
        y = pad + i * LINE_H
        begin, end = i * ROW_DELAY, (i + 1) * ROW_DELAY
        w = max(len(line), 1) * CHAR_W
        safe = svgkit.esc(line)

        p.append(f'<clipPath id="c{i}"><rect x="{pad}" y="{y}" height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/></rect></clipPath>')
        p.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" x="{pad}" '
                 f'y="{y + 11.2:.1f}" class="data" font-size="{FONT_SIZE}">{safe}</text></g>')
        p.append(f'<rect y="{y + 1}" width="6" height="12" class="data" opacity="0">'
                 f'<animate attributeName="x" from="{pad}" to="{pad + w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/></rect>')

    p.append("</svg>")
    return "".join(p)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("photo", nargs="?", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "profile.jpg"))
    ap.add_argument("out", nargs="?", default=None)
    ap.add_argument("--crop", help="left,top,right,bottom, applied first")
    ap.add_argument("--cols", type=int, default=COLS)
    ap.add_argument("--preview", action="store_true", help="also print the ASCII to the terminal")
    args = ap.parse_args()

    out = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ascii.svg")

    if not os.path.exists(args.photo):
        sys.exit(f"no photo at {args.photo} -- add it there first "
                  f"(see README: 'assets/profile.jpg'), or pass a path explicitly")

    crop = None
    if args.crop:
        parts = [int(v) for v in args.crop.split(",")]
        if len(parts) != 4:
            sys.exit("--crop needs four numbers: left,top,right,bottom")
        crop = tuple(parts)

    lines = to_lines(prep(args.photo, crop), cols=args.cols)
    if args.preview:
        print("\n".join(lines))

    with open(out, "w", encoding="utf-8") as f:
        f.write(build_svg(lines, cols=args.cols))
    print(f"wrote {out} -- {len(lines)} rows, {args.cols} columns")


if __name__ == "__main__":
    main()
