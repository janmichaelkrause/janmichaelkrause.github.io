#!/usr/bin/env python3
"""Record today's calls in data/calls.json.

The calls are worked out by the page itself, so the record always matches what a
reader saw. This script serves the repo locally, opens the page in headless Chrome,
reads the calls the page writes into <html data-c2c-calls="...">, and appends them
with the day's closing prices. One entry per data date; a rerun replaces it.

Standard library only. Needs Chrome or Chromium (preinstalled on GitHub's Ubuntu
runners). Set CHROME_BIN to point at a specific binary.
"""
import functools
import html
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)                      # ai-capex-research/ai-capex
ROOT = os.path.dirname(os.path.dirname(SITE))     # repo root
DATA = os.path.join(SITE, "data")
LATEST = os.path.join(DATA, "latest.json")
CALLS = os.path.join(DATA, "calls.json")
TICKERS = ["SPY", "NVDA", "MU", "GEV", "ORCL", "CRWV", "EQIX", "AMZN", "GOOGL", "MSFT", "META"]


def log(msg):
    print("[log_calls] " + msg, flush=True)


def chrome():
    for name in [os.environ.get("CHROME_BIN"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        if name and (os.path.isfile(name) or shutil.which(name)):
            return name if os.path.isfile(name) else shutil.which(name)
    return None


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def page_calls(binary):
    srv = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/ai-capex-research/ai-capex/index.html" % srv.server_address[1]
    try:
        out = subprocess.run([binary, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                              "--window-size=1280,900", "--virtual-time-budget=20000", "--dump-dom", url],
                             capture_output=True, timeout=120)
    finally:
        srv.shutdown()
    dom = out.stdout.decode("utf-8", "replace")
    m = re.search(r'data-c2c-calls="([^"]*)"', dom)
    if not m:
        raise RuntimeError("the page did not write its calls (exit %s): %s" % (out.returncode, out.stderr.decode("utf-8", "replace")[-400:]))
    return json.loads(html.unescape(m.group(1)))


def main():
    binary = chrome()
    if not binary:
        log("no Chrome or Chromium found; calls not logged today")
        return 0
    try:
        got = page_calls(binary)
    except Exception as e:
        log("skipped: %s" % e)
        return 0
    if not got.get("live"):
        log("the page fell back to its built-in figures (no data file); not logging")
        return 0
    latest = json.load(open(LATEST, encoding="utf-8"))
    px = (latest.get("metrics") or {}).get("prices") or {}
    prices = {t: {"close": px[t].get("close"), "date": px[t].get("date")} for t in TICKERS
              if isinstance(px.get(t), dict) and px[t].get("close") is not None and not px[t].get("stale")}
    entry = {"date": got.get("asof"), "generated": got.get("generated"), "macro": got.get("macro"),
             "funding": got.get("funding"), "fired": got.get("fired"), "flags": got.get("flags"),
             "calls": got.get("calls"), "readings": got.get("readings"),
             "breakeven_openai_2030_rev": got.get("breakeven"), "prices": prices}
    try:
        book = json.load(open(CALLS, encoding="utf-8"))
    except Exception:
        book = {}
    book["_note"] = ("One entry per data date, written by scripts/log_calls.py after the daily update. "
                     "calls: uw / n / ow per position, as the page showed them that day, with no what-ifs. "
                     "readings: each gauge's value and zone. breakeven_openai_2030_rev: for each position, "
                     "the call at each level of OpenAI's 2030 revenue ($B) where it starts. prices: closes "
                     "from the same data file; SPY is the benchmark.")
    rows = [r for r in book.get("log", []) if r.get("date") != entry["date"]]
    rows.append(entry)
    rows.sort(key=lambda r: r.get("date") or "")
    book["log"] = rows
    # one line per day keeps the file small and the daily diff readable
    with open(CALLS, "w", encoding="utf-8") as f:
        f.write('{\n "_note": %s,\n "log": [\n' % json.dumps(book["_note"], ensure_ascii=False))
        f.write(",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows))
        f.write("\n ]\n}\n")
    changed = ""
    if len(rows) > 1:
        a, b = rows[-2].get("calls") or {}, entry.get("calls") or {}
        moved = [k for k in b if a.get(k) != b.get(k)]
        changed = "; moved since %s: %s" % (rows[-2].get("date"), ", ".join(moved) if moved else "none")
    log("logged %d calls for %s, macro %s%s" % (len(entry["calls"] or {}), entry["date"], entry["macro"], changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
