#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261117 (nurz v2).

Copies the pre-drawn entry.png next to this file into
$MAKEFUN_OUTPUT_DIR/entry.png (fallback: ./out/entry.png).
Standard library only; deterministic: the same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    with open(SRC, "rb") as f:
        head = f.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if os.path.getsize(dst) != os.path.getsize(SRC):
        print("error: copied file size mismatch", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
