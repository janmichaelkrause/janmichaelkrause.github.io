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

## The stance (read before changing it)
It's a rules-based reading, not a validated model, and the copy must not claim more.
- Known problems: the macro score can't reach overweight with default weights (fixed penalties for cycle, base rate and payback gap, and downside is never positive); lab equity is underweight by construction; thresholds are judgment and untested; trailing P/E against a stock's own average misreads cyclicals; no benchmark is named.
- Planned rework: drive each layer's call from historical forcing functions (railway calls, fixed charges on railroads in 1873 and 1893, fiber's price-per-unit collapse, vendor financing, collateral re-marks in shale, orders landing in the bust, substitution). Each check asks: is there a forced seller, how close is today's reading to where it broke before, and is funding still open.

## Check before you finish
Serve from the repo root (`python3 -m http.server 8000`), open `http://localhost:8000/ai-capex-research/ai-capex/`, and check: no console errors; no horizontal scroll at 390px wide; dark mode readable; also opens as a plain file. If you changed `update.py`, run it once.
