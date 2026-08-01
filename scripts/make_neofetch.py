#!/usr/bin/env python3
"""Build neofetch.svg once."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.neofetch_build import build

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "neofetch.svg")
    if os.path.exists(out):
        sys.exit(f"refusing to overwrite existing file: {out}")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
