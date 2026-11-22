# News Image — Sunday 22 November 2026

One image that sums up the world's news of Sunday 22 November 2026.

`entry.png` is a 1024x1024 front page with 39 stories reported that
day, grouped by region and field: the collapse of the COP31 climate
talks in Antalya, the Russian drone strike on flats in Dymer near
Kyiv, and Iran's strike on a site in Bahrain lead the page, followed
by sections for Europe and Ukraine, Asia-Pacific, the Americas, the
Middle East, Africa, economy and technology, science, space and
health, and sport and culture, plus a "day in numbers" strip.

## Run

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

`main.py` (Python 3, standard library only, no network) copies
`entry.png` to the output directory byte for byte, so repeated runs
write identical bytes.

## Rebuild the image

`build_image.py` renders `entry.png` programmatically with Pillow
from the story lists in that file. The render is deterministic:
fixed palette, fixed fonts, no clock and no randomness.

Stories were compiled on 23 November 2026 (Asia/Jakarta) from
reporting dated 22 November 2026 by AP, Reuters, AFP, Al Jazeera,
The Guardian, ESA and national outlets.
