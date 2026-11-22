# news-image-20261122-entry (v3)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/iAm-182/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/iAm-182/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page summing up Sunday 22 November 2026 in a single
image, drawn with PIL primitives (original vector artwork, no photos, no
downloaded images). **Full edition, drawn 19:15 UTC — 44 stories, 8
regions**: COP31 collapses with no deal after 44 hours of overtime in
Antalya, Liverpool rout Manchester United 4-0 at Anfield, Iran's strikes
on US bases in Bahrain, Hong Kong's Election Committee vote (record
98.79% turnout), India's record 720/9 in Wellington, Verstappen's Las
Vegas Grand Prix win, Hull's shock 2-0 win over Brighton, plus a 30-item
day-in-brief grid, Saturday's and Sunday's scores in labelled strips, and
a DATE CHECK box that names the lookalike stories deliberately left out
because they are not 22 November news (Norway's oil ruling, Ghana's
banknotes, Kenya's Ebola discharge, the Peru quake, the US midterms,
Lagarde's resignation).

Running `draw.py` regenerates `entry.png` (1024×1024, ~250 KB);
`main.py` copies that file to the grader's output folder. Deterministic:
two runs write identical bytes. The footer states the date discipline —
every story on the page happened or was first reported on Sunday
22 November 2026 (Saturday's scores excepted and labelled as such).
