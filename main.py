"""news-image-20261122 v2 entrypoint: place the bundled image for grading.

The image itself is drawn at build time by draw.py and shipped as
entry.png next to this file. This program only copies it into the output
folder the grader provides, so both graded runs write identical bytes.
Standard library only; no network, no randomness.
"""

import os
import shutil
from pathlib import Path


def bundled_image() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def output_image() -> Path:
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(folder) / "entry.png"


def run() -> int:
    src = bundled_image()
    dst = output_image()
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
