#!/usr/bin/env python3
"""Build lang-stats.svg from live GitHub language data. Run locally or from
.github/workflows/lang-stats.yml. Idempotent: only rewrites when changed."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.lang_stats_build import build, fetch_all_languages


def main():
    out_dir = os.environ.get("OUT_DIR", os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    svg = build(fetch_all_languages())
    path = os.path.join(out_dir, "lang-stats.svg")

    old = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
    if old == svg:
        print("no change")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"updated {path}")


if __name__ == "__main__":
    main()
