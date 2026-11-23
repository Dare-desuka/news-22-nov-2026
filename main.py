"""news-image-20261122 entry (Python 3.13, standard library only).

The entry image is the front page in entry.png beside this file: a
newspaper page summing up the world's news of Sunday 22 November
2026 -- the COP31 collapse in Antalya, the Dymer drone strike, the
Merkury sinking off Benghazi, and the Democrats' 258-seat House
majority, plus the day's other stories.

This program copies it to /output/entry.png. It writes the same bytes
on every run: a straight copy, no timestamps, no randomness.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
if not os.path.isfile(src):
    raise SystemExit("entry.png is missing from the repository")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(src, dst)
print("wrote entry.png (%d bytes)" % os.path.getsize(dst))
