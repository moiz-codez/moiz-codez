#!/usr/bin/env python3
"""Generate a placeholder ascii.svg while the real portrait generation requires
installing rembg + onnxruntime (which download ~176 MB on first run).

Run this once to get a working placeholder. When you're ready for the real
portrait:
    pip install pillow numpy opencv-python-headless rembg onnxruntime
    python3 scripts/make_portrait.py profile.jpg --crop ...
    python3 scripts/embed_portrait_font.py
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "jbmono-ramp.woff2")

COLS = 90
CHAR_W = 7.74
FONT_SIZE = 12.9
LINE_H = 15
ROW_DELAY = 0.09
PAD = 14
FG_LIGHT = "#6e7681"
FG_DARK = "#c9d1d9"

PLACEHOLDER = [
    "                                                                                       ",
    "                                                                                       ",
    "      MMMMMMMM               MMMMMMMM        OOOOOOOOO     IIIIIIIIII   ZZZZZZZZZZZZZZZ ",
    "      M:::::::M             M:::::::M      OO:::::::::OO   I::::::::I   Z:::::::::::::Z ",
    "      M::::::::M           M::::::::M    OO::::::::::::OO  I::::::::I   Z:::::::::::::Z ",
    "      M:::::::::M         M:::::::::M   O:::::::OOO:::::O II::::::II   Z::::::ZZZZZZZZZ ",
    "      M::::::::::M       M::::::::::M   O::::::O   O:::::O   I::::I     ZZZZZZ    Z:::: ",
    "      M:::::::::::M     M:::::::::::M   O:::::O     O:::::O  I::::I             Z::::Z  ",
    "      M:::::::M::::M   M::::M:::::::M   O:::::O     O:::::O  I::::I           Z::::Z    ",
    "      M::::::M M::::M M::::M M::::::M   O:::::O     O:::::O  I::::I          Z::::Z     ",
    "      M::::::M  M::::M::::M  M::::::M   O:::::O     O:::::O  I::::I         Z::::Z      ",
    "      M::::::M   M:::::::M   M::::::M   O:::::O     O:::::O  I::::I        Z::::Z       ",
    "      M::::::M    M:::::M    M::::::M   O::::::O   O:::::O  I::::I       Z::::Z        Z",
    "      M::::::M     MMMMM     M::::::M   O:::::::OOO:::::O II::::::II   ZZZ:::::Z   ZZZZZ ",
    "      M::::::M               M::::::M    OO::::::::::::OO  I::::::::I   Z:::::::::::::Z  ",
    "      M::::::M               M::::::M      OO:::::::::OO   I::::::::I   Z:::::::::::::Z  ",
    "      MMMMMMMM               MMMMMMMM        OOOOOOOOO     IIIIIIIIII   ZZZZZZZZZZZZZZZ  ",
    "                                                                                       ",
    "                                                                                       ",
    "                                                                                       ",
    "                                                                                       ",
    "                                                                                       ",
    "          ____                     _        ____            _                            ",
    "         / ___|___  _ __ ___  _ __(_) ___  |  _ \ ___  ___| |__                          ",
    "        | |   / _ \| '_ ` _ \| '__| |/ _ \ | |_) / _ \/ __| '_ \                         ",
    "        | |__| (_) | | | | | | |  | |  __/ |  __/ (_) \__ \ | | |                        ",
    "         \____\___/|_| |_| |_|_|  |_|\___| |_|   \___/|___/_| |_|                        ",
    "                                                                                       ",
]

def build_svg(lines):
    pad = PAD
    width = int(COLS * CHAR_W + pad * 2)
    height = len(lines) * LINE_H + pad * 2

    # embed the font
    with open(FONT, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    font_rule = (f"@font-face{{font-family:JBMono;font-style:normal;"
                 f"font-weight:400;font-display:block;"
                 f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
         f'height="{height}" viewBox="0 0 {width} {height}" '
         f'font-family="JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
         f'<style>{font_rule}',
         f'.a{{fill:{FG_LIGHT}}}'
         f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}',
         '@media(prefers-reduced-motion){animate{display:none}set{display:none}}',
         '</style>']

    for i, line in enumerate(lines):
        y = pad + i * LINE_H
        begin = i * ROW_DELAY
        end = (i + 1) * ROW_DELAY
        w = max(len(line), 1) * CHAR_W
        safe = (line.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;"))

        p.append(f'<clipPath id="c{i}"><rect x="{pad}" y="{y}" '
                 f'height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'</rect></clipPath>')
        p.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" '
                 f'x="{pad}" y="{y + 11.2:.1f}" class="a" '
                 f'font-size="{FONT_SIZE}">{safe}</text></g>')
        p.append(f'<rect y="{y + 1}" width="6" height="12" class="a" '
                 f'opacity="0">'
                 f'<animate attributeName="x" from="{pad}" to="{pad + w:.1f}" '
                 f'begin="{begin:.2f}s" dur="{ROW_DELAY}s" fill="freeze"/>'
                 f'<set attributeName="opacity" to="0.8" begin="{begin:.2f}s"/>'
                 f'<set attributeName="opacity" to="0" begin="{end:.2f}s"/></rect>')

    p.append("</svg>")
    return "".join(p)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "..", "assets", "ascii.svg")
    out = os.path.abspath(out)
    svg = build_svg(PLACEHOLDER)
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out} — {len(PLACEHOLDER)} rows, {COLS} columns")
    print()
    print("To generate the real portrait from your photo:")
    print("  pip install pillow numpy opencv-python-headless rembg onnxruntime")
    print("  python3 scripts/make_portrait.py profile.jpg --crop ...")
    print("  python3 scripts/embed_portrait_font.py")


if __name__ == "__main__":
    main()
