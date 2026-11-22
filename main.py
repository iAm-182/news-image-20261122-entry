"""Entrypoint: render the 22 November 2026 front page to entry.png.

Run: python3 main.py
Writes entry.png (1024x1024, deterministic) next to this file.
"""
import os

import draw

STORIES = 44


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    final_y = draw.render(out)
    size = os.path.getsize(out)
    print("stories=%d output=%s bytes=%d final_y=%d"
          % (STORIES, out, size, final_y))


if __name__ == "__main__":
    main()
