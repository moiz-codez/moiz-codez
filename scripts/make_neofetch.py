#!/usr/bin/env python3
"""Build neofetch.svg once, with placeholder GitHub numbers.

Once .github/workflows/stats.yml runs on your repo (needs the built-in
GITHUB_TOKEN, nothing to add), scripts/generate_neofetch.py takes over and
overwrites this file with real numbers on the daily cron or manual dispatch.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.neofetch_build import build

PLACEHOLDER = dict(repos="\u2014", contributed="\u2014", stars="\u2014",
                    commits="\u2014", followers="\u2014")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "neofetch.svg")
    if os.path.exists(out):
        sys.exit(f"refusing to overwrite existing file: {out}")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(PLACEHOLDER))
    print(f"wrote {out} (placeholder numbers -- run the Action, or "
          f"generate_neofetch.py with GITHUB_TOKEN set, to fill them in)")


if __name__ == "__main__":
    main()
