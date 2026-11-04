# AI capex brief: notes for Claude

The page at `/ai-capex-research/ai-capex/`. It compares the AI infrastructure build-out with canals, railways and fiber, and gives an investor stance. Read `README.md` for setup and the data flow.

## Scope
- Work only in `ai-capex-research/` and `.github/workflows/ai-capex-daily.yml`. The rest of the repo is the owner's personal site: ask before touching it.
- For anything bigger than a small fix, propose the change first and wait for a yes. The owner signs off on ideas before implementation.
- Work on a branch. The owner reviews and merges.

## Writing
- No em dashes anywhere: page copy, docs, comments, commit messages. Use a period, colon, comma or parentheses. En dashes in ranges (2026–27) are fine.
- Plain and short. No filler, no hype, no "it's not X, it's Y".
- Every figure on the page carries a source. Sources live in the `SRC` object in the script as `key: ["Publisher, title, date", "url"]`. Cite with `cite("key")` in JS or `<sup class="cite" data-s="key"></sup>` in HTML. Never invent a source, a URL or a number. Say the date of every figure.

## How index.html is built
One self-contained file: CSS in `<head>`, markup, then one `<script>`.
- CSS: color tokens on `:root`, redefined for dark mode. Keep both themes working.
- Markup: `#view-brief` (acts `#brief`, `#b-how`, `#b-next`; then `#b-pane`, `#b-deep`, `#b-src`) and `#view-history`. Hash routing switches views.
- Script: `function C2C_BOOT(D)` holds everything. A loader at the end fetches `data/latest.json` and calls `C2C_BOOT(data)`, or `C2C_BOOT(null)` if it's missing (file:// or a failed fetch). The page must always render with `D = null`, using the figures written into it.
- Inside, in order: `SRC`; chart helpers (`S`, `lin`, `lineChart`, `barChart`, `tipEl`, `placeTip`, `legend`, `slider`, `reg`); citations (`cite`, `numberStatic`); the live data layer (`MET`, `MAN`, `PX`, `val(key, i)`, `mobj(key)`, `RULE`, `applyLayers`, `applyWL`); `LAYERS` and `LY` (one record per layer); the watchlist `WL`; drawdowns, scenarios, risk map; then the acts block (`BASE`, `CAP0`, `payback`, `PATHS`, `SIGN`, `GA`, `PRICE`, `applySign`, `applyGA`, `applyPrice`, and the stance code: `FW`, `MW`, `WT`, `layerFactors`, `macroFactors`, `INST`).
- Charts register a re-render with `reg()`. Animation runs on first view and respects reduced motion.
- Any new step that reads live data goes through `safe(fn)` so bad data can't break the page.

## Data
- `data/latest.json` and `data/history.json` are written by `scripts/update.py` (daily GitHub Action). Never edit them by hand.
- `data/manual.json` holds figures with no free feed. Edit `v`, `date`, `src`; leave `prev` out (the updater fills it).
- The updater uses the Python standard library only and only free sources (SEC EDGAR, Stooq or Yahoo, FRED). No paid data.

## The stance model (read before changing it)
Rules applied to live data, not a validated model. The copy must not claim more.
- `MG` in the script holds one gauge per forcing function: a live reading, a red "break" line from history and an amber "close" line (history, or "ours" = two-thirds of the way, marked as judgment). Each gauge has one or more positions (for example Power, Data centers preleased, Data centers speculative).
- Call rule: start overweight if nobody is forced to sell and the asset is long-lived, else neutral; one step down past amber, two past red; one more if the funding check fires (2 of 3: Fed raising rates, high-yield spread 1.5 pts above its 12-month low, an AI listing pulled or cut). Macro = average of all positions.
- The calibration and its sources are in `ai-capex-research/research/forcing-functions.md`. Change a line there and in `MG` together.
- History behind each gauge: `HX` (historical paths in the gauge's units, drawn in the "Then and now" trail, matched at today's level or at the break), `CARD` (what happened after each line, with a lag in years used for the "Today" timing note), `BT` (the backtest panels). Every figure in them needs a source key.
- Dragging a marker sets `MS.over[key]`; the flip points come from each gauge's `need()`.
- Lab revenue paths: inputs are revenue in $B per year 2027–30 for each lab (`MS.G = {oai:[4], ant:[4]}`), with implied growth shown under each. `GP` (presets; `presetRev()` turns a preset into revenue, `grow()` applies rates to the 2026 base from `labBase()`), `labCalc()` (funded share through 2030 = cash plus 2026–30 revenue after `OC`, the non-compute cost share, ÷ commitments), `runModel()` (a lab under 38% shuts the listing window; if the funding check fires, labs cut compute by their unfunded share and the cut flows down the chain), `strips()` (each position's call with both labs on a uniform growth rate, labelled as OpenAI's 2030 revenue for the break-even strips). Keep the rules text under "How the calls work" in sync.
- Position flags: `fund` (OpenAI, Oracle: distance counts only as far as funding warnings allow), `cap` (preleased data centers: capped at neutral until leases are split by tenant).
- The what-if chain's coefficients (OpenAI about a fifth of AI capex, CoreWeave's 36% top customer moves with OpenAI, 80% of lost revenue reaches operating income, Oracle's ~$64B a year from OpenAI, a point of memory margin per 1% of demand, a 25% OpenAI cut shuts the IPO window) are our assumptions and are listed under "How the calls work". Keep that list in sync with the code.
- Known limits: two-case backtest; OpenAI's cash is an upper bound (the whole March round); CoreWeave's interest from the SEC feed is debt interest only.

## Check before you finish
Serve from the repo root (`python3 -m http.server 8000`), open `http://localhost:8000/ai-capex-research/ai-capex/`, and check: no console errors; no horizontal scroll at 390px wide; dark mode readable; also opens as a plain file. If you changed `update.py`, run it once.
