# Forcing functions: what history says about the AI build-out

Calibration record for the page's stance model, 4 November 2026. The red and amber lines on the page come from this table; the calls themselves are computed from live data each morning. Numbers in [brackets] point to the sources at the end.

## The idea in five lines

1. Overbuilding alone doesn't lose investors money. Losses come when someone owes cash on a schedule out of falling revenue, or needs new money just as the market for it shuts. Call that a **forcing function**.
2. Each past boom broke through one of a handful of them, at a level we can measure.
3. For each AI layer we ask three things: is a forcing function live, how close is today's reading to where it broke before, and is funding still open.
4. The call follows from the answers, not from a weighted score.
5. Benchmarks: layers against an equal-weight basket of all layers; the macro call against the S&P 500.

## The rule

| Situation | Call |
|---|---|
| No forced seller, long-lived asset | Overweight |
| No forced seller, short-lived asset | Neutral |
| Forced seller, reading still far from the historical break | Neutral |
| Forced seller, reading close to or past the break | Underweight |
| Funding check fires (2 of 3 below) | Every call moves one step toward underweight |

**Funding check, 2 of 3:** the central bank is raising rates; high-yield spreads are 1.5 points or more above their 12-month low; a major AI listing is pulled or cut in price. Today: **1 of 3**. The Fed raised rates in September to 3.75–4.00%, two members voted for another hike in October, and markets price about a 78% chance of one in December [27]. High-yield spreads are 3.31%, at least 0.65 points above their 12-month low (2.66% on 21 September is the lowest I found) [28]. The IPO window is open, with Anthropic expected to price around 19–20 November [22].

## The table

| # | Forcing function | Where it broke, and at what level | AI equivalent | Today | Distance |
|---|---|---|---|---|---|
| 1 | **Calls on partly paid capital** | UK Railway Mania. Shares were sold for a deposit, the rest called as lines were built. Investors had paid in 9.9% of their liability at end-1845, 38% by 1847, 72% by 1849 [2]. Prices fell in call weeks, by 4% in 1845 and 16% in 1848, as holders sold some shares to pay for others [2]. The Bank of England raised rates on 16 October 1845 and the long decline began [1]; the index fell about two-thirds by April 1850 [4]. | Labs' compute commitments, funded by new money. Gauge: cash plus a year of revenue ÷ commitments, against the railway path: red at 38% (1847 crisis), amber at 72% (where the fall ran out, 1849) | **OpenAI:** plans to burn about $278B of cash in 2026–30 on $36B of 2026 revenue [23]; one analyst estimate puts its outside-capital need at about $207B through 2030 [24]. **Anthropic:** $131.7B of cash and short-term investments against $265.6B of fixed commitments at 30 June, about half "paid in"; positive free cash flow in H1 2026; some deals pay only on delivery or can be cancelled [21]. | OpenAI: close. Anthropic: far |
| 2 | **Fixed charges outrun earnings** | US railroads, 1893. The Reading's fixed charges were 95% of net earnings in 1891; it went into receivership in February 1893 [5][6]. The B&O's rose from 75% of net earnings in 1894 to 98% in 1896, when it failed [5]. In 1893 alone courts took over more than 27,000 miles with about $2B of capital [5]. Shareholders were assessed cash to keep a stake; bonds were scaled down [5]. | Neocloud and leveraged-builder debt service | **CoreWeave Q2 2026:** interest $640M, which is 42% of adjusted EBITDA ($1.51B) and more than all of its operating income (an operating loss of $49M). Top three customers are 72% of revenue [16]. **Oracle:** free cash flow −$23.7B in fiscal 2026 and −$5.4B last quarter; funded by $43B of debt, then a $20B share sale; OpenAI is over half of its $638B backlog [17][18]. | CoreWeave: past, after the cost of wearing out GPUs. Oracle: close |
| 3 | **Price per unit falls faster than volume grows** | Fiber, 2000–02. Bandwidth prices fell about 65% a year while traffic roughly doubled, so revenue fell [p:wsj27][p:lr_wcom]. Telecom shares fell about 50% a year for three years [p:rupak]. | GPU rent and token prices against usage | H100 rent fell from about $8 an hour in early 2024 to $1.70 by October 2025, a fiber-speed drop, then recovered to $2.35 by March 2026 [19]. Token prices at fixed capability fall about tenfold a year [p:epoch_price], but lab revenue is still growing faster: Anthropic H1 revenue up 14× [21]. | Not live now. It has fired once already |
| 4 | **Suppliers financing their customers** | Lucent, 2000. Vendor financing commitments of $8.1B, 24% of revenue; $3.5B of bad-debt provisions in 2001–02 [13]. Lucent, Nortel, JDSU and Corning fell 98% [p:cnn_tel4]. | Nvidia's stakes in its customers | Investments in private companies $51.2B [p:nv10q], 17% of the last four quarters' $303B revenue [29]. Up to 50% if the $100B OpenAI commitment is fully drawn [13]. | Close; past if OpenAI draws |
| 5 | **Peak margins just before capacity lands** | Memory chips. Micron's gross margin was 61.0% in the August 2018 quarter and 28.6% a year later [11]. Memory revenue fell 31.5% in 2019 [12] and 37% in 2023 [14]. | Memory makers | Micron's gross margin is 87% (quarter to 3 Sept 2026) [29][15]. Mitigant: makers say they're sold out through 2029 under long-term deals [p:skh]. | Past |
| 6 | **Orders placed at the peak arrive in the bust** | Merchant power, 2000–03. Planned plants equal to 51% of the existing 750 GW base [8]; reserve margins were heading toward 37% by 2004 [9]. A quarter of planned turbine capacity was cancelled within six months [8]; Mirant filed with $11.4B of debt [p:cw_mirant]; more than $90B of merchant debt fell due in 2003–06 [10]. | Turbine backlogs; data center construction | **Power:** the grid is short, not long: PJM cleared at its cap and 6,831 MW short [p:opis_pjm]. **Data centers:** 7.5 GW under construction, 69% of the 10.9 GW already built in the main markets, but more than 80% preleased and vacancy 1.4% [p:cbre26]. The 2000 merchant plants had no buyers lined up. | Power: far. Data centers: past on volume, far on who carries the risk |
| 7 | **Lenders re-value collateral** | Shale, 2015–16. Banks cut borrowing bases by 39% in fall 2015 and 38% in spring 2016 as oil fell [25]; 58 producers with $50.4B of debt filed in 2016 alone [26]. | Loans backed by GPUs | More than $20B of GPU-backed facilities announced; CoreWeave's 2023 loan advanced about 70 cents per dollar of hardware. A 2–3-year-old GPU is worth roughly 50–70% of new as a going concern and 30–50% in a forced sale. CoreWeave's loan terms have no borrowing base or re-marking clause [19]. | The shale mechanism is absent; losses would come all at once, on default |
| 8 | **A new technology replaces the old asset** | Canals. Pennsylvania's Main Line cost about $10M [30] and was sold in 1857 for $7.5M, to the railroad that had replaced it [31]. | Custom chips replacing Nvidia GPUs | Custom chips were about 11% of accelerator revenue in 2024, projected to grow 45% a year against 16% for GPUs [20]. Anthropic's largest commitment is $161.2B of Google TPU leases through Broadcom; the next is $114.5B with Google Cloud [21][p:ant_s1]. | Early |
| 9 | **The asset outlives the bust (the fine case)** | The Erie Canal paid back its loans in about nine years [p:brit_erie]. Railway track and fiber stayed in use [p:odly10][p:acm]. Digital Realty was assembled from distressed data centers bought in the dot-com crash [7]. | Buildings, sites and grid hookups | Vacancy 1.4%, rents rising, more than 80% preleased [p:cbre26]. | n/a |

## Calls

The page computes them each morning from live readings, so they aren't listed here. As built on 4 November 2026 the model read: macro neutral, leaning underweight; funding check 1 of 3; first domino OpenAI. The labs gauge was recalibrated to the full railway path (shares kept falling until investors had paid in 72%), and now counts a year of revenue alongside cash, since the 1840s lines earned nothing until they opened.

What changed from the draft table when it went live:
- Oracle is measured by how much of its capex is funded from outside its own cash flow (the 1873 Northern Pacific and canal mechanism), against the canal and railway line of more than half.
- GPU-backed credit is measured by the change in H100 rent, against the 38–39% cut in shale borrowing bases. It reads neutral while rents are rising.
- Speculative data centers read neutral while the uncontracted build is far from the 2000 merchant-power level.
- Lines marked "ours" (amber, two-thirds of the way to the break) are judgment, not history.

## Lab revenue

Most calls hang on how much revenue OpenAI and Anthropic make, so the page makes it the main control: revenue in $B for each year 2027–30, separately for each lab, with presets for OpenAI's plan and the three history paths. The page shows the growth each number implies.

- OpenAI's plan: $36B (2026) to $350B (2030), $840B in total, $856B of compute, and $278B of cash burn [23]. That implies non-compute costs of about 31% of revenue, used for both labs.
- Funded share through 2030 = (cash + 69% of 2026–30 revenue) ÷ commitments. Under its own plan OpenAI funds about 82% and still needs about $155B from outside, consistent with the reported burn net of its cash.
- Break-evens, holding today's funding warnings and both labs growing at the same rate: OpenAI exposure moves to neutral at about $330B of OpenAI revenue in 2030 (74% a year); below about $91B (26% a year) OpenAI covers less than the 1847 line, the listing window counts as shut, the funding check fires and most calls move down a step.
- Anthropic has published no revenue plan, so the "OpenAI's plan" preset puts it on the Absorbed path.

## Rough backtest

| Case | Forced seller | Funding check | Call | Outcome |
|---|---|---|---|---|
| UK railways, 1845 | Yes: investors had paid in under 10% [2] | Bank of England raised rates on 16 October and 6 November 1845 [1][34]; £4.4M of calls in October–December, and new railway shares stopped selling (our reading, since 1845 has no listing data) | Underweight from November 1845, three months after the August peak | The index was about 19% below its peak then and fell to 66% below by April 1850 [4][34]. Avoided about 71% of the fall. |
| Fiber, 1998 | Yes: carriers funded with high-yield debt | 1 of 3: spreads jumped from 3.45% to 5.39% after the 1998 crisis [3], but the Fed was cutting [33] | No call | Telecom shares kept rising until March 2000 [p:rupak]. A one-signal rule would have been about 15 months early. |
| Fiber, 1999 to mid-2000 | Yes | 1 of 3: the Fed raised rates from June 1999 to May 2000 [33], but spreads at end-1999 (4.97%) were not 1.5 points above their own 12-month low [3] | No call; the March 2000 peak passes | |
| Fiber, second half of 2000 | Yes | 2 of 3: spreads widened sharply in the second half of 2000 [36][35] while the Fed's rate was still above its level six months earlier (until mid-November) [33] | Underweight between July and November 2000, 4–8 months after the peak | Telecom shares fell about 50% a year for three years from March 2000 [p:rupak]. Avoided roughly 58–77% of the fall. |

What this shows: the rules turn underweight after the peak, not before it, and would have avoided most of each decline. An earlier draft said the telecom call came three months before the peak; that used 1997's spread as the baseline, not the 12-month low the rule specifies, and was wrong. What it doesn't show: anything predictive. It's two cases, the 1845 second warning is our reading, and the 2-of-3 rule was chosen after seeing that one warning alone misfired in 1998.

## Weak spots to decide on

1. **Breaking points are single historical readings**, not ranges. "Close" means within about a third of the old break; that cutoff is mine.
2. **Some AI figures are second-hand** (Anthropic via an S-1 summary, OpenAI via press reports). Swap in primary filings when OpenAI's S-1 is public.
3. **No year-by-year payment schedule** for lab commitments is disclosed, so the "calls" comparison uses cash against total commitments.
4. **Regulated utilities and merchant generators** need their own historical numbers before those calls mean much.
5. **CoreWeave's interest** from the SEC feed reads $558M, not the reported $640M, because the filing tag covers debt interest only. The page should use the reported figure or both tags.

## Sources

`[p:key]` means a source already on the page under that key.

1. Federal Reserve Bank of New York, Liberty Street Economics, Crisis Chronicles: Railway Mania, the Hungry Forties, and the Commercial Crisis of 1847 (2015). https://libertystreeteconomics.newyorkfed.org/2015/06/crisis-chronicles-railway-mania-the-hungry-forties-and-the-commercial-crisis-of-1847
2. Gareth Campbell, Leveraging the British Railway Mania (MPRA paper 21822), Tables 5–6 and p. 25. https://mpra.ub.uni-muenchen.de/21822/1/MPRA_paper_21822.pdf
3. Edward Altman, Defaults and Returns on High Yield Bonds: Analysis Through September 30, 2002 (NYU Stern). https://archive.nyu.edu/bitstream/2451/26494/2/02-50.pdf
4. Campbell and Turner, Dispelling the Myth of the Naive Investor (page key ct12).
5. Stuart Daggett, Railroad Reorganization (1908), Project Gutenberg. https://www.gutenberg.org/ebooks/55397
6. Gareth Campbell, working paper on the Railway Mania and the Commercial Crisis of 1847 (Queen's University Belfast), pp. 4–5, 19–20. https://pureadmin.qub.ac.uk/ws/files/18161511/RailwayCrisis.pdf ; Reading receivership date: page key brew1893.
7. Data Center Knowledge, Digital Realty: How to Survive a Market Meltdown and Come Out on Top (July 2017). https://www.datacenterknowledge.com/next-gen-data-centers/digital-realty-how-to-survive-a-market-meltdown-and-come-out-on-top
8. Public Utilities Fortnightly, Why it happened? Who lost in the bust? (June 2002; page key fort02): about 380,000 MW planned on a 750,000 MW base.
9. Renewable Energy World, U.S. reserve margins expected to peak in 2004 (April 2002, citing Energy Ventures Analysis). https://www.renewableenergyworld.com/?p=8079811070
10. Natural Gas Intelligence, S&P: worst time for energy merchants to refinance (November 2002). https://www.naturalgasintel.com/sp-worst-time-for-energy-merchants-to-refinance-several-face-problems/
11. Micron, results for the fourth quarter and full year of fiscal 2019 (September 2019). https://aeccafe.com/nbc/articles/1/1701476/Micron-Technology-Inc.-Reports-Results-Fourth-Quarter-Full-Year-Fiscal-2019
12. eeNews Europe, Chip market declined 12% in 2019, says Gartner (January 2020). https://www.eenewseurope.com/en/chip-market-declined-12-in-2019-says-gartner/
13. Tomasz Tunguz, Circular financing: does Nvidia's bet echo the telecom bubble? (page key tunguz_vf).
14. Gartner, worldwide semiconductor revenue declined 11% in 2023 (January 2024). https://www.gartner.com/en/newsroom/press-releases/2024-01-16-gartner-says-worldwide-semiconductor-revenue-declined-11-percent-in-2023
15. Pulse 2.0, Micron reports record fiscal Q4 revenue of $54.23 billion (September 2026). https://pulse2.com/micron-reports-record-fiscal-q4-revenue-of-54-23-billion-and-fy2026-revenue-of-133-19-billion/
16. Beancount, CoreWeave FY2026 Q2 earnings analysis (September 2026). https://beancount.io/blog/2026/09/22/coreweave-fy2026-q2-earnings-analysis
17. Parameter, Oracle stock falls on a $40B fundraising plan (June 2026). https://parameter.io/oracle-orcl-stock-plunges-10-despite-earnings-beat-on-40b-fundraising-plan/
18. NeoTeo, Oracle reports $5.4B negative free cash flow for Q1 FY2027 (October 2026). https://www.neoteo.com/en/oracle-reports-5396-billion-in-negative-free-cash-flow-for-q1-fy2027
19. Wing VC, How the GPU Became Collateral (September 2026). https://www.wing.vc/content/how-the-gpu-became-collateral
20. Introl, The Custom Silicon Inflection Point (February 2026, citing Bloomberg Intelligence). https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu
21. AlphaSense, Anthropic company primers on the public S-1 (October 2026). https://www.alpha-sense.com/api/html-embed/file-037a4037e03a4c06f42a72c2c7dfa251727bff93-html/ and https://www.alpha-sense.com/api/html-embed/file-4c88b5685d7120f5cdcdc99545773cca679d25fd-html/
22. AlphaSense primer above (expected pricing 19–20 November 2026).
23. Reuters via DealStreetAsia, OpenAI sees nearly $280B cash burn by 2030 (September 2026). https://www.dealstreetasia.com/?p=495626
24. RoboRhythms, OpenAI filed for IPO (May 2026), citing HSBC. https://www.roborhythms.com/?p=32956
25. Haynes and Boone, Spring 2016 borrowing base redetermination survey (January 2016). https://www.haynesboone.com/news/press-releases/spring-2016-borrowing-base-redeterminations
26. Haynes and Boone, Fall 2016 borrowing base survey (September 2016). https://www.haynesboone.com/news/press-releases/fall-2016-borrowing-survey
27. StockAnalysis, Fed holds rates steady at 3.75% to 4.00% in a 10–2 vote (October 28, 2026). https://stockanalysis.com/news/fed-holds-rates-steady-oct-2026/
28. Convex Trade, ICE BofA US High Yield OAS (331 bps on October 16, 2026). https://convextrade.com/metrics/bamlh0a0hym2
29. SEC EDGAR company filings via the page's daily updater (data/latest.json, 4 Nov 2026): Nvidia revenue for the four quarters to July 2026; Micron gross profit ÷ revenue; hyperscaler operating cash flow and capex for Q3 2026.
30. Citizendium, Pennsylvania Main Line of Public Works (estimated cost). https://www.citizendium.org/wiki/Pennsylvania_Main_Line_of_Public_Works
31. Wikipedia, Main Line of Public Works (sale on 25 June 1857). https://en.wikipedia.org/wiki/Main_Line_of_Public_Works
32. Vested Finance, Alphabet Q3 2026 earnings (October 2026). https://vestedfinance.com/blog/us-stocks/alphabet-q3-2026-earnings-ai-boom-meets-a-cash-crunch/
33. Federal Reserve, federal funds target rate (FRED series DFEDTAR). https://fred.stlouisfed.org/series/DFEDTAR
34. Gareth Campbell, The Railway Mania: a narrative (railwaymania.co.uk): Bank rate moves, monthly calls and yearly index changes, 1843–50. https://www.railwaymania.co.uk/narrative.html
35. Federal Reserve Bank of San Francisco, Economic Letter 2001-33 (spreads +334 bps June–October 1998; +300 bps from early 2000). https://www.frbsf.org/wp-content/uploads/el2001-33.pdf
36. Bank of England Quarterly Bulletin, Interpreting movements in high-yield corporate bond market spreads (2001). https://www.bankofengland.co.uk/quarterly-bulletin/2001/q1/interpreting-movements-in-high-yield-corporate-bond-market-spreads
37. Macrotrends, Micron gross margin, trailing four quarters (used for the memory trail). https://macrotrends.net/stocks/charts/MU/micron-technology/gross-margin
