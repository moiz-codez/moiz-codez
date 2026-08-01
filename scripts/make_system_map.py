#!/usr/bin/env python3
"""Build system-map.svg -- a hub-and-spoke view of the stack, in the same
masked-wire style as Sharann-del's ecosystem.svg: wires are drawn first,
then a <mask> punches a hole wherever a node sits, so nothing ever overlaps
a label and the whole thing stays transparent on GitHub's own background.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import svgkit

WIDTH, HEIGHT = 1000, 620
HUB = dict(x=500, y=330, w=210, h=64, title="MOIZ.SYS", sub="full-stack \u00d7 agentic pipeline")
NODE_W, NODE_H = 220, 72

NODES = [
    ("Frontend", "React \u00b7 Next.js \u00b7 Tailwind"),
    ("Backend", "Node \u00b7 Express \u00b7 Flask \u00b7 Django \u00b7 FastAPI"),
    ("Mobile", "Flutter \u00b7 Dart \u00b7 Android Studio"),
    ("Data", "PostgreSQL \u00b7 MongoDB \u00b7 Redis \u00b7 Firebase \u00b7 Supabase"),
    ("DevOps", "Docker \u00b7 K8s \u00b7 AWS \u00b7 GCP \u00b7 Vercel \u00b7 Netlify"),
    ("Agentic AI", "LLM tooling \u00b7 automation workflows"),
    ("Systems", "C \u00b7 C++ \u00b7 Java \u00b7 Arduino"),
    ("Execution", "QA \u2192 delivery \u00b7 sprint velocity \u00b7 Verior"),
]


def layout():
    n = len(NODES)
    positions = []
    start = -90 - (360 / n) / 2  # keep a node off dead-north/south
    for i in range(n):
        ang = math.radians(start + i * 360 / n)
        rx, ry = 372, 218
        cx = WIDTH / 2 + rx * math.cos(ang)
        cy = HUB["y"] + ry * math.sin(ang)
        cy = max(88, min(HEIGHT - 60, cy))
        positions.append((cx, cy))
    return positions


def wrap_subtitle(text, max_chars=28):
    parts = text.split(" \u00b7 ")
    lines = [parts[0]]
    for part in parts[1:]:
        candidate = f"{lines[-1]} \u00b7 {part}"
        if len(candidate) <= max_chars:
            lines[-1] = candidate
        else:
            lines.append(part)
    return lines


def node_text(cx, cy, title, subtitle):
    lines = wrap_subtitle(subtitle)
    title_y = cy - 13 if len(lines) > 1 else cy - 4
    p = [svgkit.label(cx, title_y, svgkit.esc(title), 13, "ink", "middle", weight="600",
                      spacing="0.6")]
    if len(lines) == 1:
        p.append(svgkit.label(cx, cy + 15, svgkit.esc(lines[0]), 9, "dim", "middle"))
    else:
        p.append(svgkit.label(cx, cy + 3, svgkit.esc(lines[0]), 9, "dim", "middle"))
        p.append(svgkit.label(cx, cy + 15, svgkit.esc(lines[1]), 9, "dim", "middle"))
    return "".join(p)


def build():
    positions = layout()
    p = [svgkit.svg_open(WIDTH, HEIGHT, "System map: tech stack ecosystem around one pipeline"),
         svgkit.style_block()]

    p.append(f'<line x1="48" y1="40" x2="{WIDTH-48}" y2="40" class="rule" stroke-width="1"/>')
    p.append(svgkit.label(48, 28, "SYSTEM MAP \u2014 ONE STACK, ONE PIPELINE", 11, "dim", spacing="2.5"))
    p.append(svgkit.label(WIDTH - 48, 28, "FIG. 01", 11, "dim", "end", spacing="2.5"))

    mask_id = "nodeCutouts"
    p.append(f'<defs><mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" '
             f'width="{WIDTH}" height="{HEIGHT}"><rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>')
    hx = HUB["x"] - HUB["w"] / 2
    hy = HUB["y"] - HUB["h"] / 2
    p.append(f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{HUB["w"]}" height="{HUB["h"]}" fill="black"/>')
    for cx, cy in positions:
        p.append(f'<rect x="{cx - NODE_W/2:.0f}" y="{cy - NODE_H/2:.0f}" '
                 f'width="{NODE_W}" height="{NODE_H}" fill="black"/>')
    p.append('</mask></defs>')

    wires = []
    for i, (cx, cy) in enumerate(positions):
        delay = 0.2 + i * 0.09
        length = int(math.hypot(cx - HUB["x"], cy - HUB["y"])) + 20
        wires.append(f'<line x1="{HUB["x"]}" y1="{HUB["y"]}" x2="{cx:.1f}" y2="{cy:.1f}" '
                     f'class="rule" stroke-width="1" {svgkit.draw(delay, 0.9, length)}</line>')
    p.append(f'<g mask="url(#{mask_id})">{"".join(wires)}</g>')

    hub_delay = 0.1
    p.append(f'<g opacity="0">{svgkit.fade(hub_delay, 0.5)}'
             f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{HUB["w"]}" height="{HUB["h"]}" '
             f'rx="3" class="rule" fill="none" stroke-width="1"/>'
             + svgkit.label(HUB["x"], HUB["y"] - 4, HUB["title"], 14, "ink", "middle",
                             weight="600", spacing="1.5")
             + svgkit.label(HUB["x"], HUB["y"] + 15, HUB["sub"], 9.5, "dim", "middle") + '</g>')

    for i, ((cx, cy), (title, sub)) in enumerate(zip(positions, NODES)):
        delay = 1.0 + i * 0.1
        nx = cx - NODE_W / 2
        ny = cy - NODE_H / 2
        p.append(f'<g opacity="0">{svgkit.fade(delay, 0.5)}'
                 f'<rect x="{nx:.0f}" y="{ny:.0f}" width="{NODE_W}" height="{NODE_H}" '
                 f'rx="3" class="rule" fill="none" stroke-width="1"/>'
                 + node_text(cx, cy, title, sub) + '</g>')

    p.append(f'<line x1="48" y1="{HEIGHT-30}" x2="{WIDTH-48}" y2="{HEIGHT-30}" class="rule" stroke-width="1"/>')
    p.append("</svg>")
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "system-map.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
