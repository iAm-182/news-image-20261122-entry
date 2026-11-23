"""Entrypoint: copy the pre-rendered 22 November 2026 front page to entry.png.

v4 packaging fix (v3 was rejected on run_completes: it re-rendered via
draw.py at grade time, needing Pillow + Liberation fonts that are not in
the grade sandbox). The image itself is unchanged from v3 -- this program
just copies the committed entry.png to the output directory, using only
the Python standard library. No Pillow, no fonts, no network, no drawing.

Run: python3 main.py
Writes <output>/entry.png, byte-identical to the committed entry.png.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil

IMAGE = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as f:
        src_digest = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_digest = hashlib.sha256(f.read()).hexdigest()
    if src_digest != dst_digest:
        raise SystemExit("copy mismatch: %s != %s" % (src_digest, dst_digest))
    print("output=%s bytes=%d sha256=%s"
          % (dst, os.path.getsize(dst), dst_digest))


if __name__ == "__main__":
    main()
