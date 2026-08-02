"""Shared layout + data for lang-stats.svg, used by the one-off builder and
the GitHub Actions refresh script so the two never drift."""
import json
import urllib.request

from . import svgkit

OWNER = "moiz-codez"
TOP_LANGS = 7


def get_json(url):
    with urllib.request.urlopen(url) as resp:
        return json.load(resp)


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
