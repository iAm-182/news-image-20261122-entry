#!/usr/bin/env python3
"""news-image-20261122 v1 entrypoint.

Moves the finished front page (entry.png, drawn at build time by draw.py)
into the grader's output directory. Standard library only, no network, no
randomness: two runs write identical bytes.
"""

import os
from pathlib import Path


def run():
    root = Path(__file__).resolve().parent
    data = (root / "entry.png").read_bytes()
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    out.mkdir(parents=True, exist_ok=True)
    dest = out / "entry.png"
    dest.write_bytes(data)  # byte-identical on every run: no timestamps
    print("entry.png ->", dest, f"({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
