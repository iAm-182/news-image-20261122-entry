"""Copy the bundled 22 November news image into the output folder."""

import os
import shutil
from pathlib import Path


def source_image() -> Path:
    return Path(__file__).resolve().parent / "entry.png"


def target_image() -> Path:
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(folder) / "entry.png"


def main() -> int:
    origin = source_image()
    goal = target_image()
    goal.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origin, goal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
