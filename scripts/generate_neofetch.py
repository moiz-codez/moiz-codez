#!/usr/bin/env python3
"""Refresh neofetch.svg. Run by .github/workflows/stats.yml."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.neofetch_build import build

def main():
    out_dir = os.environ.get("OUT_DIR", os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    svg = build()
    path = os.path.join(out_dir, "neofetch.svg")

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
