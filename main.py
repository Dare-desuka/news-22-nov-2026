"""Entry point for the news-image entry (Python 3.13 standard library only).

Copies the pre-rendered front page into the grader's output folder.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(TARGET_DIR, "entry.png"))


if __name__ == "__main__":
    main()
