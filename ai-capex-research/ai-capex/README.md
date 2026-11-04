# AI capex brief (/ai-capex-research/ai-capex/)

A subpage of this site. `index.html` is the whole page. It reads `data/latest.json`, which a GitHub Action rewrites every morning.

## Files

| Path | What it is |
|---|---|
| `ai-capex-research/ai-capex/index.html` | The page. Opens on its own; with no data file it shows the figures written into it. |
| `ai-capex-research/ai-capex/data/manual.json` | Figures with no free daily feed. You edit this. |
| `ai-capex-research/ai-capex/data/latest.json` | Written by the updater. Don't edit. |
| `ai-capex-research/ai-capex/data/history.json` | Written by the updater: daily snapshots and every change to a manual figure. |
| `ai-capex-research/ai-capex/scripts/update.py` | The updater. Python standard library only. |
| `.github/workflows/ai-capex-daily.yml` | Runs the updater daily at 13:43 UTC (about 5:45 am Pacific), commits the result, then starts `static.yml` so the site republishes. |
| `ai-capex-research/ai-capex/CLAUDE.md` | Rules for Claude (here or in Claude Code) when editing this page. |

## One-time setup

1. The `ai-capex-research` folder sits in the repo root, and the workflow at `.github/workflows/ai-capex-daily.yml`. GitHub only runs workflows from that folder.
2. On GitHub: **Settings → Secrets and variables → Actions → New repository secret**.
   Name: `SEC_USER_AGENT`. Value: your name and email, e.g. `Jan Krause you@example.edu`. The SEC requires this on automated requests. It stays private.
3. **Actions → ai-capex daily data → Run workflow**. That writes the first `latest.json`.
4. Open `https://janmichaelkrause.com/ai-capex-research/ai-capex/`. The footer should read "Live figures updated ...".

If step 3 fails at the push step, go to **Settings → Actions → General → Workflow permissions** and choose "Read and write permissions".

## What updates on its own

| Source | Figures |
|---|---|
| SEC EDGAR (company filings) | Nvidia revenue and inventory; Micron revenue and gross margin; CoreWeave revenue and interest; capex and operating cash flow at Amazon, Alphabet, Microsoft, Meta; diluted EPS for the P/E calls |
| Stooq, Yahoo as fallback | Daily closes and 52-week highs; trailing P/E against each stock's own five-year average |
| FRED | High-yield and BBB credit spreads |

From these the page recomputes, each morning: the layer signals and their direction, the watchlist, the signposts, the five gauges, the price factor, and the overall and per-instrument stance. Momentum compares each reading with the one before it, and the P/E baselines roll forward as new months come in.

Company figures change when a 10-Q or 10-K is filed, so expect jumps around earnings, not every day.

If a source fails, the last good value is kept and marked stale, so a bad morning never blanks the page. The reasons are in the `log` field of `latest.json`.

## What you update by hand

Edit `data/manual.json` when a new number comes out:

- vacancy, H100 rental prices, the PJM auction, GE Vernova's backlog, Oracle's CDS and rating, debt share of capex, the Nvidia 10-Q items, lab commitments and run-rates
- the "Latest step" list (`changes`) and the calendar (`calendar`). Past calendar dates drop off automatically.
- three yes/no `flags` used by the signposts

Change `v` and `date`. Leave `prev` out: the updater fills it with the last different value it saw. `src` is a source key already on the page. For a new source, add `{"k", "t", "url"}` to `sources` and use its `k`.

## Preview locally

From the repo root run `python3 -m http.server 8000` and open `http://localhost:8000/ai-capex-research/ai-capex/`. Opening the file directly (double-click) also works, but shows the built-in figures.

To run the updater yourself: `SEC_USER_AGENT="Your Name you@example.edu" python3 ai-capex-research/ai-capex/scripts/update.py`

## If your site is deployed by a workflow

Pushes made by Actions don't start other workflows. If your Pages site is built by a workflow (not "Deploy from a branch"), make sure that workflow has `workflow_dispatch:` under `on:`. The daily job then starts it after each commit.
