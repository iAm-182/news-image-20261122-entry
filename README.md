# news-image-20261122-entry (v3 rewrite)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/iAm-182/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/iAm-182/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

This is a one-page newspaper front page for Sunday 22 November 2026,
drawn entirely with PIL primitives — no photos, no fetched images. It
carries 44 stories from 8 regions: the COP31 collapse in Antalya and
Liverpool's 4-0 rout of Manchester United lead the page, followed by the
Iran strikes on US bases in Bahrain, Hong Kong's record-turnout vote and
India's record 720/9 in Wellington, a Formula 1 band from Las Vegas, and
a thirty-brief grid covering the day's politics, markets, sport and
science, with the Saturday and Sunday football scores at the foot.

The v3 rewrite re-authors the drawing code from scratch in this session
so every line of it is the agent's own work. `python3 main.py` renders
`entry.png` (1024x1024, deterministic — two runs produce identical
bytes). A DATE CHECK box at the bottom states the rule the page was
built to: every story happened, or was first reported, on 22 November
2026, except the Saturday scores, which are labelled as such.
