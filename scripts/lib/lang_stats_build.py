"""Shared layout + data for lang-stats.svg, used by the one-off builder and
the GitHub Actions refresh script so the two never drift."""
import json
import os
import time
import urllib.error
import urllib.request

from . import svgkit

OWNER = "moiz-codez"
TOP_LANGS = 7

RETRY_STATUS = frozenset((403, 429, 500, 502, 503, 504))
RETRY_ATTEMPTS = 3
RETRY_DELAYS = (1, 2)


def _read_token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def get_json(url, _urlopen=None, _token=_read_token, _sleep=time.sleep):
    urlopen = _urlopen if _urlopen is not None else urllib.request.urlopen
    token = _token() if callable(_token) else _token
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    last_error = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            with urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in RETRY_STATUS:
                raise
        except urllib.error.URLError as exc:
            last_error = exc
        if attempt < len(RETRY_DELAYS):
            _sleep(RETRY_DELAYS[attempt])
    raise last_error


def fetch_repos(owner=OWNER, _get_json=get_json):
    data = _get_json(
        f"https://api.github.com/users/{owner}/repos?per_page=100&sort=updated")
    return [repo["name"] for repo in data]


def fetch_repo_languages(owner, repo, _get_json=get_json):
    return _get_json(f"https://api.github.com/repos/{owner}/{repo}/languages")


def fetch_all_languages(owner=OWNER, _get_json=get_json):
    totals = {}
    for repo in fetch_repos(owner, _get_json):
        for lang, n in fetch_repo_languages(owner, repo, _get_json).items():
            totals[lang] = totals.get(lang, 0) + n
    return totals


def compute_percentages(lang_bytes, top=TOP_LANGS):
    total = sum(lang_bytes.values())
    if total == 0:
        return []
    items = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:top]
    return [(name, n, n / total * 100.0) for name, n in items]


WIDTH = 940
PAD = 22
BAR_H = 14
ROW_H = 30
TRACK_W = 380


def _bar_row(i, x, y, name, n, pct, delay, width):
    cid = f"langBar{i}"
    fill_w = max(TRACK_W * pct / 100.0 - 2, 1)
    clip, cursor = svgkit.wipe_clip(cid, x, y + 1, fill_w, BAR_H - 2, delay, 0.8)
    track = (f'<rect x="{x}" y="{y}" width="{TRACK_W}" height="{BAR_H}" '
             f'class="rule" fill="none" rx="2" stroke-width="1"/>')
    fill = (f'<g clip-path="url(#{cid})">'
            f'<rect x="{x}" y="{y + 1}" width="{fill_w:.1f}" height="{BAR_H - 2}" '
            f'class="data" rx="1"/></g>')
    left = svgkit.label(PAD, y + 6, svgkit.esc(name), 12.5, "ink", weight="600")
    right = (svgkit.label(width - PAD, y + 6, f"{pct:.1f}%", 12.5, "ink",
                          "end", weight="600")
             + svgkit.label(width - PAD - 64, y + 6, f"{n:,}", 10, "dim", "end"))
    return (f'<g opacity="0">{svgkit.fade(delay, 0.4)}{left}{track}{fill}{right}</g>'
            + clip + cursor)


def build(lang_bytes, width=WIDTH):
    rows = compute_percentages(lang_bytes)
    height = PAD + 34 + len(rows) * ROW_H + PAD + 30
    p = [svgkit.svg_open(width, height,
                         "language stats: bytes per language across public repos"),
         svgkit.style_block(),
         f'<rect width="{width}" height="{height}" class="surface" rx="12"/>']
    p.append(f'<line x1="48" y1="40" x2="{width - 48}" y2="40" '
             f'class="rule" stroke-width="1"/>')
    p.append(svgkit.label(48, 28, "LANGUAGE STATS \u2014 GITHUB, BY BYTES",
                          11, "dim", spacing="2.5"))
    p.append(svgkit.label(width - 48, 28, "FIG. 02", 11, "dim", "end",
                          spacing="2.5"))

    y = PAD + 34
    for i, (name, n, pct) in enumerate(rows):
        p.append(_bar_row(i, 180, y, name, n, pct, 0.2 + i * 0.09, width))
        y += ROW_H

    p.append(f'<line x1="48" y1="{height - 30}" x2="{width - 48}" y2="{height - 30}" '
             f'class="rule" stroke-width="1"/>')
    p.append("</svg>")
    return "".join(p)
