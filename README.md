# The World in One Picture — Friday 20 November 2026

One image summing up the world's news of Friday 20 November 2026, drawn
programmatically with Python + PIL (no AI image generation, so every word
is crisp and legible).

## What the image shows

- **Cyclone Akvan hits India's east coast** — landfall near Gopalpur at
  noon; 300,000 people moved to safety, 47 trains cancelled.
- **COP31 closes with fossil fuels cut from text** — the near-final deal
  in Antalya drops any phase-out pledge, drawing anger from nations.
- **GTA VI takes $2.36bn on day one, estimate says** — Sensor Tower puts
  first-day sales at 24.6m copies; Take-Two has confirmed no figure.
- **Wall Street slides 2% as Anthropic IPO debuts** — the Dow falls
  1,101 points; Anthropic closes up 17% in the largest IPO on record,
  $107bn raised.
- **Iran widens attacks on Gulf tankers** — Tehran steps up strikes on
  shipping as oil prices slide; the IEA warns of a historic energy
  threat.
- **Shenzhen summit ends with no breakthrough** — Trump, Xi and Putin's
  peace declaration sidesteps the wars in Ukraine and Iran.

Footer note: 20 November is also World Children's Day.

## How it was built

`render.py` draws the 1024×1024 PNG with PIL from the story list embedded
in the script: a navy masthead with the date, six story cards (tag chip,
drawn pictogram, headline, one-line summary), and a source footer.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Rendering is deterministic: two runs
produce byte-identical output.

## Sources

The Hindu, News18, Reuters, CNA, Indian Express, Japan Times, The
Independent — all stories first reported on 20 November 2026.
