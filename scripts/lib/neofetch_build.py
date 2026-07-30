from . import svgkit
from .neofetch_layout import ROWS, GH_ROW_LABELS, mascot_lines, uptime_string

MASCOT_CHAR_W, MASCOT_LINE_H, MASCOT_FS = 7.6, 13.5, 11
ROW_H = 21
COL2_X = 300
WIDTH = 940
PAD = 22


def _mascot_block(delay0=0.05, step=0.03):
    lines = mascot_lines()
    p = []
    y0 = PAD + 8
    for i, line in enumerate(lines):
        y = y0 + i * MASCOT_LINE_H
        begin = delay0 + i * step
        w = max(len(line), 1) * MASCOT_CHAR_W
        cid = f"mc{i}"
        clip, cursor = svgkit.wipe_clip(cid, PAD, y, w, MASCOT_LINE_H, begin, 0.30)
        p.append(clip)
        p.append(f'<g clip-path="url(#{cid})"><text xml:space="preserve" x="{PAD}" '
                 f'y="{y + MASCOT_FS - 0.5:.1f}" class="data" font-size="{MASCOT_FS}">'
                 f'{svgkit.esc(line)}</text></g>')
        p.append(cursor)
    return "".join(p), y0 + len(lines) * MASCOT_LINE_H


def _kv_row(x, y, key, value, delay):
    if key == "":
        return ""
    dots_w = 20
    key_span = f'<tspan class="ink" font-weight="600">{svgkit.esc(key)}</tspan>'
    return (f'<g opacity="0">{svgkit.fade(delay, 0.4)}'
            f'<text x="{x}" y="{y}" font-size="12.5">'
            f'{key_span}<tspan class="rule" dx="4">'
            f'{"." * dots_w}</tspan>'
            f'<tspan class="data" dx="6">{svgkit.esc(value)}</tspan>'
            f'</text></g>')


def build(gh_stats):
    """gh_stats: dict with keys repos, contributed, stars, commits, followers
    (strings, already formatted -- pass '\u2014' placeholders if unknown)."""
    mascot_svg, mascot_bottom = _mascot_block()

    right_rows = list(ROWS)
    header_y = PAD + 6
    y = header_y + 26
    body = []
    delay = 0.05
    rule_w = WIDTH - COL2_X - PAD

    body.append(f'<g opacity="0">{svgkit.fade(0.0, 0.4)}'
                + svgkit.label(COL2_X, header_y, "moiz@codez", 14, "ink", weight="600")
                + f'<line x1="{COL2_X + 92}" y1="{header_y - 5}" x2="{WIDTH - PAD}" '
                  f'y2="{header_y - 5}" class="rule" stroke-width="1"/></g>')

    for key, value in right_rows:
        if key == "":
            y += ROW_H * 0.5
            continue
        if key == "Uptime":
            value = uptime_string()
        body.append(_kv_row(COL2_X, y, key, value, delay))
        y += ROW_H
        delay += 0.025

    y += ROW_H * 0.4
    body.append(f'<g opacity="0">{svgkit.fade(delay, 0.4)}'
                + svgkit.label(COL2_X, y, "GitHub Stats", 13, "ink", weight="600")
                + f'<line x1="{COL2_X + 108}" y1="{y - 5}" x2="{WIDTH - PAD}" y2="{y - 5}" '
                  f'class="rule" stroke-width="1"/></g>')
    y += ROW_H
    delay += 0.04

    gh_values = [gh_stats.get("repos", "\u2014"), gh_stats.get("contributed", "\u2014"),
                 gh_stats.get("stars", "\u2014"), gh_stats.get("commits", "\u2014"),
                 gh_stats.get("followers", "\u2014")]
    for label_, value in zip(GH_ROW_LABELS, gh_values):
        body.append(_kv_row(COL2_X, y, label_, value, delay))
        y += ROW_H
        delay += 0.025

    height = max(y + PAD, mascot_bottom + PAD)
    out = [svgkit.svg_open(WIDTH, height, "moiz@codez system info"),
           svgkit.style_block(),
           f'<rect width="{WIDTH}" height="{height}" class="surface" rx="12"/>',
           mascot_svg]
    out.extend(body)
    out.append("</svg>")
    return "".join(out)
