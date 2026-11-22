"""News-image entry for Sunday 22 November 2026.

The repository ships the finished front page as entry.png: one
1024x1024 picture holding 39 stories reported on 22 November 2026,
led by the collapse of the COP31 climate talks in Antalya, the
Russian drone strike on flats in Dymer near Kyiv, and Iran's strike
on a site in Bahrain. This program copies that image to the output
directory, byte for byte, with no network use.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    # Revision 2: entry.png is the balanced two-column front page
    # rendered by build_image.py (39 stories, 1024x1024, under 200 KB).
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    shutil.copyfile(source, out_dir / "entry.png")


if __name__ == "__main__":
    main()
