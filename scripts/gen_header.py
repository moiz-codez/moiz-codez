#!/usr/bin/env python3
"""Generate the animated header SVG — tayyabadev ASCII art + greeting."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

RAMP = " .`:-=+*cs#%@"
COLS = 90
CHAR_W = 7.74
FONT_SIZE = 12.9
LINE_H = 15
ROW_DELAY = 0.09
PAD = 14

FG_LIGHT = "#6e7681"
FG_DARK = "#c9d1d9"
FG_EMP_LIGHT = "#424a53"
FG_EMP_DARK = "#f0f6fc"
FG_DIM_LIGHT = "#8c959f"
FG_DIM_DARK = "#8b949e"

ascii_lines = [
    '                                   ___           ___           ___       ___       ___     ',
    '                                  /\\__\\         /\\  \\         /\\__\\     /\\__\\     /\\  \\    ',
    '                                 /:/  /        /::\\  \\       /:/  /    /:/  /    /::\\  \\   ',
    '                                /:/__/        /:/\\:\\  \\     /:/  /    /:/  /    /:/\\:\\  \\  ',
    '                               /::\\  \\ ___   /::\\~\\:\\  \\   /:/  /    /:/  /    /:/  \\:\\  \\ ',
    '                              /:/\\:\\  /\\__\\ /:/\\:\\ \\:\\__\\ /:/__/    /:/__/    /:/__/ \\:\\__\\',
    '                              \\/__\\:\\/:/  / \\:\\~\\:\\ \\/__/ \\:\\  \\    \\:\\  \\    \\:\\  \\ /:/  /',
    '                                   \\::/  /   \\:\\ \\:\\__\\    \\:\\  \\    \\:\\  \\    \\:\\  /:/  /',
    '                                   /:/  /     \\:\\ \\/__/     \\:\\  \\    \\:\\  \\    \\:\\/:/  /  ',
    '                                  /:/  /       \\:\\__\\        \\:\\__\\    \\:\\__\\    \\::/  /   ',
    '                                  \\/__/         \\/__/         \\/__/     \\/__/     \\/__/    ',
]

def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build():
    h_ascii = len(ascii_lines) * LINE_H + PAD * 2
    h1_y = h_ascii + 30
    h2_y = h1_y + 40
    total_h = h2_y + 60
    max_w = max(len(l) for l in ascii_lines) * CHAR_W + PAD * 2
    svg_w = max(int(max_w) + 10, 640)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg"',
        f' width="{svg_w}" height="{total_h}" viewBox="0 0 {svg_w} {total_h}"',
        ' font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        '<style>',
        f'.a{{fill:{FG_LIGHT}}}.b{{fill:{FG_EMP_LIGHT}}}.c{{fill:{FG_DIM_LIGHT}}}',
        f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}.b{{fill:{FG_EMP_DARK}}}.c{{fill:{FG_DIM_DARK}}}}}',
        '@media(prefers-reduced-motion){.anim{animation:none!important}',
        'animate{display:none}set{display:none}}',
        '</style>',
    ]

    total = len(ascii_lines) + 2

    for i, line in enumerate(ascii_lines):
        y = PAD + i * LINE_H
        begin = i * ROW_DELAY
        endv = (i + 1) * ROW_DELAY
        w = max(len(line), 1) * CHAR_W
        safe = esc(line)

        parts.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" height="{LINE_H}" width="0">'
                     f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                     f'</rect></clipPath>')
        parts.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" x="{PAD}" y="{y+11.2:.1f}" class="a" font-size="{FONT_SIZE}">{safe}</text></g>')
        parts.append(f'<rect y="{y+1}" width="6" height="12" class="a" opacity="0">'
                     f'<animate attributeName="x" from="{PAD}" to="{PAD+w:.1f}" begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                     f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
                     f'<set attributeName="opacity" to="0" begin="{endv:.2f}s"/></rect>')

    # "Hi, I'm Muhammad Moiz"
    i = len(ascii_lines)
    y = h1_y
    begin = i * ROW_DELAY
    endv = (i + 1) * ROW_DELAY
    text1 = "Hi, I'm Muhammad Moiz"
    w1 = len(text1) * 18
    parts.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" height="40" width="0">'
                 f'<animate attributeName="width" from="0" to="{w1:.1f}" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>'
                 f'</rect></clipPath>')
    parts.append(f'<g clip-path="url(#c{i})"><text x="{PAD}" y="{y+30}" class="b" font-size="28">{esc(text1)}</text></g>')
    parts.append(f'<rect y="{y+2}" width="6" height="34" class="b" opacity="0">'
                 f'<animate attributeName="x" from="{PAD}" to="{PAD+w1:.1f}" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{endv:.2f}s"/></rect>')

    # subtitle
    i = len(ascii_lines) + 1
    y = h2_y
    begin = i * ROW_DELAY
    endv = (i + 1) * ROW_DELAY
    sub = "a developer crafting systems that matter"
    w2 = len(sub) * 10
    parts.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" height="24" width="0">'
                 f'<animate attributeName="width" from="0" to="{w2:.1f}" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>'
                 f'</rect></clipPath>')
    parts.append(f'<g clip-path="url(#c{i})"><text x="{PAD}" y="{y+18}" class="c" font-size="16">{esc(sub)}</text></g>')
    parts.append(f'<rect y="{y+2}" width="6" height="18" class="c" opacity="0">'
                 f'<animate attributeName="x" from="{PAD}" to="{PAD+w2:.1f}" begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{endv:.2f}s"/></rect>')

    parts.append("</svg>")
    return "".join(parts)

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "header.svg")
    out = os.path.abspath(out)
    svg = build()
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
