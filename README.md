# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/983022631/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/983022631/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image front page summing up Saturday 21 November 2026: Mexico
captures FBI most-wanted cartel boss "El Chapo Isidro" in a Sinaloa raid,
a Russian "triple-tap" missile strike hits Zelenskyy's hometown of Kryvyi
Rih and then its rescuers, COP31 climate talks in Antalya run into
overtime with no deal, Cyclone Akvan fades over Odisha with no major
damage, Wolbachia mosquitoes cut dengue infections about 69% in a Brazilian
trial, and Trump says he will not decide on new Iran strikes until after
the new year. The image is drawn programmatically with Python (PIL) in
`draw.py` — masthead, headlines and six small drawn illustrations, no
AI-generated pictures — and `main.ts` copies it to the entry point.

## Run it

```sh
python3 draw.py          # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources (all stories verified against reputable outlets)

- Mexico captures "El Chapo Isidro": Reuters ("Mexico captures top drug
  lord 'El Chapo Isidro,' latest in string of captures", 21 Nov 2026);
  AP (published 21 Nov 2026); Al Jazeera (21 Nov 2026) — Fausto Isidro
  Meza Flores seized Friday night in Guasave, Sinaloa; four soldiers and
  seven gunmen killed; FBI Top 10 fugitive, $5m reward.
- Kryvyi Rih strike: AP ("Ballistic missile attack on Zelenskyy's
  hometown in central Ukraine kills 2 and wounds scores", 21 Nov 2026);
  Al Jazeera and CNN (21 Nov 2026) — Friday-night "triple-tap" strike
  kills a 7-year-old boy and a 20-year-old paramedic, wounds 60.
- COP31 overtime: The Straits Times ("COP31 climate talks near final
  deal", 22 Nov 2026); Al Jazeera via Pajhwok and The Thursday Times
  (21 Nov 2026) — talks run past the 20 Nov deadline; Thursday draft
  drops fossil fuels and a $120bn adaptation-finance target.
- Cyclone Akvan: The Hindu live updates (21 Nov 2026); DT Next and
  The Indian Express (21 Nov 2026) — landfall near Gopalpur on Friday,
  weakened to a depression, no major damage or loss of life; 4.4 lakh
  people evacuated.
- Wolbachia mosquitoes: AP ("Scientists report strong new evidence that
  specially bred mosquitoes can fend off dengue", 21 Nov 2026); The
  Straits Times (21 Nov 2026) — about 69% fewer dengue and chikungunya
  infections in a four-year trial of 5,700 children in Belo Horizonte,
  Brazil, presented at the American Society of Tropical Medicine and
  Hygiene meeting.
- Trump on Iran: Mid-Day and News One USA (21 Nov 2026), reporting an
  Axios interview aboard Air Force One on Thursday — Trump says he will
  wait until the new year before deciding on further action against Iran,
  as Netanyahu presses for a joint air campaign.

---

<sub>Entered on [make.fun](https://make.fun/?ref=76bwm2a6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
