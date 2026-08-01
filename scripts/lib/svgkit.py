import base64
import os

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")

LIGHT = dict(ink="#24292f", data="#6e7681", dim="#57606a", rule="#d0d7de", surface="#ffffff")
DARK = dict(ink="#f0f6fc", data="#8b949e", dim="#8b949e", rule="#30363d", surface="#0d1117")

FAMILY = "MJBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def _face(weight, filename):
    path = os.path.join(FONT_DIR, filename)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return (f"@font-face{{font-family:MJBMono;font-style:normal;font-weight:{weight};"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


def fonts():
    return _face(400, "jbmono-regular.woff2") + _face(600, "jbmono-semibold.woff2")


def palette_css():
    def block(t):
        return (f".ink{{fill:{t['ink']}}}.data{{fill:{t['data']};stroke:{t['data']}}}"
                f".dim{{fill:{t['dim']}}}.rule{{stroke:{t['rule']}}}"
                f".surface{{fill:{t['surface']}}}")
    return (block(LIGHT)
            + f"@media(prefers-color-scheme:dark){{{block(DARK)}}}")


def style_block(extra_css=""):
    return f"<style>{fonts()}{palette_css()}{extra_css}</style>"


def svg_open(width, height, aria_label=""):
    label = f' role="img" aria-label="{aria_label}"' if aria_label else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" fill="none" font-family="{FAMILY}"{label}>')


def fade(delay, dur=0.45, fmt=".2f"):
    return (f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:{fmt}}s" dur="{dur}s" fill="freeze"/>')


def draw(delay, dur=1.2, length=1000):
    return (f'stroke-dasharray="{length}" stroke-dashoffset="{length}">'
            f'<animate attributeName="stroke-dashoffset" from="{length}" to="0" '
            f'begin="{delay:.2f}s" dur="{dur}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.6 0 0.2 1"/>')


def wipe_clip(cid, x, y, w, h, delay, dur=1.0):
    """clipPath reveal + a cursor block riding its edge -- the portrait's
    signature move, reused everywhere something should feel 'typed'."""
    clip = (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" height="{h}" width="0">'
            f'<animate attributeName="width" from="0" to="{w}" '
            f'begin="{delay:.2f}s" dur="{dur}s" fill="freeze"/></rect></clipPath>')
    cursor = (f'<rect y="{y}" width="2" height="{h}" class="data" opacity="0">'
              f'<animate attributeName="x" from="{x}" to="{x + w}" '
              f'begin="{delay:.2f}s" dur="{dur}s" fill="freeze"/>'
              f'<set attributeName="opacity" to="0.6" begin="{delay:.2f}s"/>'
              f'<set attributeName="opacity" to="0" begin="{delay + dur:.2f}s"/></rect>')
    return clip, cursor


def label(x, y, text, size=12, cls="dim", anchor="start", weight=None, spacing=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    s = f' letter-spacing="{spacing}"' if spacing else ""
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}"{a}{w}{s}{extra}>{text}</text>'


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                  .replace(">", "&gt;").replace('"', "&quot;"))
