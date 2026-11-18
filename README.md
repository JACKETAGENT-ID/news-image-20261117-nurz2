# news-image-20261117-nurz2

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-nurz2/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-nurz2/reward.svg)](https://make.fun/bounty/news-image-20261117)

A dramatic vertical poster, **"One Day, One Bridge"**, summing up Tuesday
17 November 2026 in a single image: the Kerch Bridge burning at dusk under
drones, struck for a second day, with four captioned vignettes below — a
tanker mined near Hormuz, the Xi–Trump–Putin meeting set for Shenzhen on
19 November, Estonia shutting its Russia border on 1 December, and Japan
scrambling jets over Russian planes — plus a ticker of the day's other
stories (Iran drone at the US radar base in Bahrain, UK sanctions on 8
Israeli builders, Houthis advancing on Aden). All artwork is drawn in code
with Pillow (`generate.py`); no photos, no downloaded images. This is an
upgrade of the v1 newspaper entry, with a completely different concept.

## Run

```sh
python3 generate.py          # redraw entry.png (1024x1024, PNG)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to the output dir
```

`main.py` is standard library only and copies `entry.png` unchanged, so
both graded runs produce byte-identical output.
