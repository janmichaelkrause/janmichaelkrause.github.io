#!/usr/bin/env python3
"""Daily data updater for the AI capex brief (ai-capex-research/ai-capex/index.html).

Pulls free public data, merges the hand-kept figures in data/manual.json,
and writes data/latest.json for the page to read. Standard library only.

  SEC EDGAR company facts  quarterly revenue, inventory, margins, capex, cash flow, EPS
  Stooq (Yahoo fallback)   daily closes, 52-week highs; trailing P/E and its own 5-year average
  FRED                     ICE BofA high-yield and BBB option-adjusted spreads

Any source that fails keeps its last good value from the previous latest.json,
so a bad morning never blanks the page.

Environment:
  SEC_USER_AGENT   required by the SEC, e.g. "Jane Doe jane@example.edu"
  FRED_API_KEY     optional, free from fred.stlouisfed.org; more reliable than the CSV download
  AI_CAPEX_MOCK    optional folder of saved responses, for offline testing
"""
import csv, io, json, os, sys, time, datetime as dt, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
LATEST = os.path.join(DATA, "latest.json")
HISTORY = os.path.join(DATA, "history.json")
MANUAL = os.path.join(DATA, "manual.json")

UA_SEC = os.environ.get("SEC_USER_AGENT", "").strip()
FRED_KEY = os.environ.get("FRED_API_KEY", "").strip()
UA_WEB = "Mozilla/5.0 (compatible; ai-capex-updater/1.0)"
MOCK = os.environ.get("AI_CAPEX_MOCK", "").strip()
TODAY = dt.datetime.now(dt.timezone.utc).date()
LOG = []

def log(msg):
    LOG.append(msg)
    print(msg, flush=True)

# ---------------------------------------------------------------- http
def get(url, ua, tries=3, timeout=30):
    if MOCK:
        name = "".join(c if c.isalnum() else "_" for c in url)[:180]
        path = os.path.join(MOCK, name)
        if not os.path.exists(path):
            raise IOError("no mock for " + url)
        with open(path, "rb") as f:
            return f.read()
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network, 403, 429, timeouts
            last = e
            time.sleep(2 * (i + 1))
    raise IOError("%s: %s" % (url, last))

def d(s):
    return dt.date.fromisoformat(s[:10])

# ---------------------------------------------------------------- SEC
FALLBACK_CIK = {"NVDA": 1045810, "MU": 723125, "AMZN": 1018724, "GOOGL": 1652044, "MSFT": 789019,
                "META": 1326801, "ORCL": 1341439, "GEV": 1996810, "EQIX": 1101239, "CRWV": 1769628}

def cik_map():
    try:
        raw = json.loads(get("https://www.sec.gov/files/company_tickers.json", UA_SEC))
        m = {v["ticker"].upper(): int(v["cik_str"]) for v in raw.values()}
        out = dict(FALLBACK_CIK)
        out.update({t: m[t] for t in FALLBACK_CIK if t in m})
        return out
    except Exception as e:
        log("SEC ticker map failed, using built-in CIKs: %s" % e)
        return dict(FALLBACK_CIK)

_facts = {}
def facts(cik):
    if cik not in _facts:
        url = "https://data.sec.gov/api/xbrl/companyfacts/CIK%010d.json" % cik
        _facts[cik] = json.loads(get(url, UA_SEC))
        time.sleep(0.25)  # stay well under the SEC's 10 requests a second
    return _facts[cik]

def _rows(cf, tag, unit):
    t = cf.get("facts", {}).get("us-gaap", {}).get(tag)
    if not t:
        return []
    rows = [r for r in t.get("units", {}).get(unit, []) if str(r.get("form", "")).startswith(("10-Q", "10-K"))]
    return rows

def _filing_url(cik, accn):
    return "https://www.sec.gov/Archives/edgar/data/%d/%s/" % (cik, accn.replace("-", "")) if accn else ""

def quarterly(cik, tags, unit="USD", instant=False, keep=24, splits=None):
    """Quarterly series, newest first: [{end, v, first_filed, filed, form, url}].
    Duration facts are reported year-to-date in most 10-Qs and as full years in 10-Ks,
    so a quarter is derived as YTD(end) minus YTD(end of the prior quarter) when no
    three-month fact exists."""
    cf = facts(cik)
    merged = {}
    for tag in tags:
        rows = _rows(cf, tag, unit)
        if not rows:
            continue
        if splits:  # per-share facts filed before a split are on the old share count
            rows = [dict(r, val=r["val"] / split_factor(splits, r.get("filed"))) for r in rows]
        # one value per period: latest filing wins (restatements, split restatements);
        # first_filed records when the market first saw it
        per = {}
        for r in rows:
            k = (r.get("start"), r["end"])
            cur = per.get(k)
            if cur is None or r.get("filed", "") > cur.get("filed", ""):
                first = min(r.get("filed", "9999"), cur.get("first_filed", "9999")) if cur else r.get("filed", "9999")
                per[k] = dict(r, first_filed=first)
            else:
                cur["first_filed"] = min(cur.get("first_filed", "9999"), r.get("filed", "9999"))
        series = {}
        if instant:
            for (s, e), r in per.items():
                if s is None:
                    series[e] = r
        else:
            by_start = {}
            for (s, e), r in per.items():
                if s is None:
                    continue
                by_start.setdefault(s, []).append((e, r))
            for (s, e), r in per.items():
                if s is None:
                    continue
                days = (d(e) - d(s)).days
                if 80 <= days <= 100:
                    series[e] = r
            for (s, e), r in per.items():
                if s is None or e in series:
                    continue
                days = (d(e) - d(s)).days
                if not (170 <= days <= 380):
                    continue
                for e0, r0 in by_start.get(s, []):
                    gap = (d(e) - d(e0)).days
                    if 80 <= gap <= 100:
                        series[e] = dict(r, val=r["val"] - r0["val"], derived=True,
                                         first_filed=r.get("first_filed"))
                        break
        for e, r in series.items():
            if e not in merged:
                merged[e] = {"end": e, "v": r["val"], "filed": r.get("filed"), "first_filed": r.get("first_filed"),
                             "form": r.get("form"), "url": _filing_url(cik, r.get("accn")), "tag": tag}
    out = sorted(merged.values(), key=lambda x: x["end"], reverse=True)
    return out[:keep]

# ---------------------------------------------------------------- prices
KNOWN_SPLITS = {  # date, ratio; used when Yahoo's split list is unavailable
    "NVDA": [("2021-07-20", 4.0), ("2024-06-10", 10.0)],
    "AMZN": [("2022-06-06", 20.0)],
    "GOOGL": [("2022-07-18", 20.0)],
}

def prices_stooq(t):
    raw = get("https://stooq.com/q/d/l/?s=%s.us&i=d" % t.lower(), UA_WEB).decode("utf-8", "replace")
    if not raw.startswith("Date"):
        raise IOError("stooq: unexpected reply for %s" % t)
    rows = []
    for r in csv.DictReader(io.StringIO(raw)):
        try:
            rows.append((r["Date"], float(r["Close"]), float(r["High"])))
        except (ValueError, KeyError):
            pass
    if len(rows) < 30:
        raise IOError("stooq: too few rows for %s" % t)
    return rows, []

def prices_yahoo(t):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%s?range=6y&interval=1d&events=split" % t
    j = json.loads(get(url, UA_WEB))
    res = j["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    rows = []
    for ts, c, h in zip(res["timestamp"], q["close"], q["high"]):
        if c is None:
            continue
        day = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date().isoformat()
        rows.append((day, float(c), float(h if h is not None else c)))
    splits = []
    for s in (res.get("events", {}) or {}).get("splits", {}).values():
        try:
            day = dt.datetime.fromtimestamp(s["date"], dt.timezone.utc).date().isoformat()
            splits.append((day, float(s["numerator"]) / float(s["denominator"])))
        except Exception:
            pass
    if len(rows) < 30:
        raise IOError("yahoo: too few rows for %s" % t)
    return rows, splits

def prices(t):
    errs = []
    for fn in (prices_stooq, prices_yahoo):
        try:
            rows, splits = fn(t)
            rows.sort()
            return rows, splits
        except Exception as e:
            errs.append(str(e))
    raise IOError("; ".join(errs))

def split_factor(splits, filed):
    """EPS filed before a split is on the old share count; divide by later split ratios."""
    f = 1.0
    for day, ratio in splits:
        if filed and filed < day and ratio > 0:
            f *= ratio
    return f

def ttm_eps(eps_q):
    """Trailing four-quarter EPS, newest first: [(available_from, end, ttm)]."""
    adj = sorted(eps_q, key=lambda x: x["end"])  # already split-adjusted by quarterly()
    out = []
    for i in range(3, len(adj)):
        four = adj[i - 3:i + 1]
        span = (d(four[-1]["end"]) - d(four[0]["end"])).days
        if not (250 <= span <= 300):  # four consecutive quarters only
            continue
        avail = four[-1].get("first_filed") or (d(four[-1]["end"]) + dt.timedelta(days=45)).isoformat()
        out.append((avail, four[-1]["end"], sum(q["v"] for q in four)))
    return sorted(out, reverse=True)

def price_block(t, cik=None):
    rows, splits = prices(t)
    allsplits = sorted(set(KNOWN_SPLITS.get(t, []) + splits))
    eps_q = None
    if cik:
        try:
            eps_q = quarterly(cik, EPS, "USD/shares", False, keep=40, splits=allsplits)
        except Exception as e:
            log("SEC EPS %s failed: %s" % (t, e))
    last_day, close, _ = rows[-1]
    yr_ago = (d(last_day) - dt.timedelta(days=365)).isoformat()
    high52 = max(h for day, c, h in rows if day >= yr_ago)
    out = {"close": round(close, 2), "date": last_day, "high52": round(high52, 2)}
    if eps_q:
        ttm = ttm_eps(eps_q)
        if ttm and ttm[0][2] > 0:
            out["pe"] = round(close / ttm[0][2], 2)
            out["eps_ttm"] = round(ttm[0][2], 3)
            out["eps_end"] = ttm[0][1]
        # own average trailing P/E: month-end closes over the last five years,
        # each against the TTM EPS the market had at that date; loss-making months skipped
        start = (d(last_day) - dt.timedelta(days=5 * 365)).isoformat()
        month_end = {}
        for day, c, h in rows:
            if day >= start:
                month_end[day[:7]] = (day, c)
        pes, first = [], None
        for ym in sorted(month_end):
            day, c = month_end[ym]
            known = [x for x in ttm if x[0] <= day]
            if not known or known[0][2] <= 0:
                continue
            pe = c / known[0][2]
            if 0 < pe < 400:
                pes.append(pe)
                first = first or day[:4]
        if len(pes) >= 12:
            out["pe_avg"] = round(sum(pes) / len(pes), 2)
            out["pe_since"] = first
            out["pe_months"] = len(pes)
    return out

# ---------------------------------------------------------------- FRED
def _fred_rows_api(series, start):
    url = ("https://api.stlouisfed.org/fred/series/observations?series_id=%s&api_key=%s"
           "&file_type=json&observation_start=%s" % (series, FRED_KEY, start))
    j = json.loads(get(url, UA_WEB, timeout=60))
    return [(o["date"], float(o["value"])) for o in j.get("observations", []) if o.get("value") not in (".", "", None)]

def _fred_rows_csv(series, start):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s&cosd=%s" % (series, start)
    raw = get(url, UA_WEB, timeout=90).decode("utf-8", "replace")
    rows = []
    for r in csv.reader(io.StringIO(raw)):
        if len(r) < 2 or r[1] in (".", "") or not r[0][:1].isdigit():
            continue
        try:
            rows.append((r[0], float(r[1])))
        except ValueError:
            pass
    return rows

def fred(series):
    """Uses the FRED API when FRED_API_KEY is set (free key), else the public CSV,
    which is slow from cloud servers. Only the last ~13 months are requested."""
    start = (TODAY - dt.timedelta(days=400)).isoformat()
    errs, rows = [], []
    for fn in ([_fred_rows_api] if FRED_KEY else []) + [_fred_rows_csv]:
        try:
            rows = fn(series, start)
            if rows:
                break
        except Exception as e:
            errs.append(str(e).replace(FRED_KEY, "***") if FRED_KEY else str(e))
    if not rows and errs:
        raise IOError("; ".join(errs))
    if not rows:
        raise IOError("FRED: no rows for " + series)
    rows.sort()
    day, v = rows[-1]
    target = (d(day) - dt.timedelta(days=91)).isoformat()
    prev = [x for x in rows if x[0] <= target]
    out = {"kind": "d", "v": v, "date": day, "src": "live_fred",
           "url": "https://fred.stlouisfed.org/series/" + series}
    if prev:
        out["prev"], out["prevDate"] = prev[-1][1], prev[-1][0]
    return out

# ---------------------------------------------------------------- what to pull
REV = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"]
CAPEX = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"]
OCF = ["NetCashProvidedByUsedInOperatingActivities"]
EPS = ["EarningsPerShareDiluted"]
SEC_SERIES = [  # key, ticker, tags, unit, instant
    ("nvda_revenue", "NVDA", REV, "USD", False),
    ("nvda_inventory", "NVDA", ["InventoryNet"], "USD", True),
    ("mu_revenue", "MU", REV, "USD", False),
    ("mu_gross_profit", "MU", ["GrossProfit"], "USD", False),
    ("crwv_revenue", "CRWV", REV, "USD", False),
    ("crwv_interest", "CRWV", ["InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt"], "USD", False),
] + [("capex_" + t, t, CAPEX, "USD", False) for t in ("AMZN", "GOOGL", "MSFT", "META")] \
  + [("ocf_" + t, t, OCF, "USD", False) for t in ("AMZN", "GOOGL", "MSFT", "META")]
PE_TICKERS = ["NVDA", "MU", "GEV", "ORCL", "AMZN", "GOOGL", "MSFT", "META"]
PX_ONLY = ["CRWV", "EQIX"]
FRED_SERIES = [("hy_oas", "BAMLH0A0HYM2"), ("bbb_oas", "BAMLC0A4CBBB")]

def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def main():
    if not UA_SEC and not MOCK:
        log("SEC_USER_AGENT is not set. Add it as a repository secret (your name and email). SEC data will be skipped.")
    old = load(LATEST, {})
    old_m = old.get("metrics", {})
    metrics, status = {}, {}

    # SEC
    ciks = cik_map() if (UA_SEC or MOCK) else dict(FALLBACK_CIK)
    if UA_SEC or MOCK:
        for key, t, tags, unit, inst in SEC_SERIES:
            try:
                q = quarterly(ciks[t], tags, unit, inst, keep=12)
                if len(q) < 2:
                    raise IOError("fewer than two quarters")
                metrics[key] = {"kind": "q", "q": [{k: x[k] for k in ("end", "v", "form", "url")} for x in q], "src": "live_sec", "tag": q[0]["tag"]}
                status[key] = "ok"
            except Exception as e:
                log("SEC %s failed: %s" % (key, e))
        # compare the four hyperscalers on the same quarter
        hk = [k for k in metrics if k.startswith(("capex_", "ocf_"))]
        if len(hk) == 8:
            common = min(metrics[k]["q"][0]["end"] for k in hk)
            for k in hk:
                metrics[k]["q"] = [x for x in metrics[k]["q"] if x["end"] <= common]

    # prices and P/E
    px = {}
    use_sec = bool(UA_SEC or MOCK)
    for t in PE_TICKERS + PX_ONLY:
        try:
            px[t] = price_block(t, ciks.get(t) if (use_sec and t in PE_TICKERS) else None)
            status["px_" + t] = "ok"
        except Exception as e:
            log("price %s failed: %s" % (t, e))

    # FRED
    for key, sid in FRED_SERIES:
        try:
            metrics[key] = fred(sid)
            status[key] = "ok"
        except Exception as e:
            log("FRED %s failed: %s" % (key, e))

    # keep last good values for anything that failed today
    for k, v in old_m.items():
        if k == "prices":
            continue
        if k not in metrics:
            metrics[k] = dict(v, stale=True)
            status[k] = "stale"
    for t, v in (old_m.get("prices") or {}).items():
        if t not in px:
            px[t] = dict(v, stale=True)
            status["px_" + t] = "stale"
    metrics["prices"] = px

    # hand-kept figures; prev is filled from history when not given
    manual = load(MANUAL, {})
    hist = load(HISTORY, {"manual": {}, "daily": {}})
    for k, o in manual.items():
        if not isinstance(o, dict) or not isinstance(o.get("v"), (int, float)) or isinstance(o.get("v"), bool):
            continue
        log_k = hist["manual"].setdefault(k, [])
        if not log_k or log_k[-1][1] != o["v"]:
            log_k.append([o.get("date") or TODAY.isoformat(), o["v"]])
        if "prev" not in o and len(log_k) >= 2:
            o["prev"] = log_k[-2][1]
            o["prevDate"] = log_k[-2][0]

    snap = {}
    for k, m in metrics.items():
        if k == "prices":
            continue
        if m.get("kind") == "q" and m.get("q"):
            snap[k] = m["q"][0]["v"]
        elif m.get("kind") == "d":
            snap[k] = m.get("v")
    for t, p in px.items():
        snap["close_" + t] = p.get("close")
        if p.get("pe") is not None:
            snap["pe_" + t] = p["pe"]
    hist["daily"][TODAY.isoformat()] = snap
    for day in sorted(hist["daily"])[:-1000]:
        del hist["daily"][day]

    out = {"asof": TODAY.isoformat(), "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
           "metrics": metrics, "manual": manual, "status": status, "log": LOG[-40:]}
    os.makedirs(DATA, exist_ok=True)
    with open(LATEST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, separators=(",", ":"))
    ok = sum(1 for s in status.values() if s == "ok")
    print("wrote %s: %d fresh, %d stale" % (LATEST, ok, len(status) - ok))
    return 0

if __name__ == "__main__":
    sys.exit(main())
