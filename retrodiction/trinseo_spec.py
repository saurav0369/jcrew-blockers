"""Trinseo pilot spec. Governing doc: Credit Agreement of Sep 6, 2017 as amended through the 2023 SOFR Amendment
(June 30, 2023), EX-10.2 to 10-Q filed 2023-08-04, acc 0001558370-23-013353 (conformed copy). Read directly in sections
quoted in retro/trinseo_extract.md. Units: $ millions. Total Assets: FY2022 10-K, XBRL us-gaap:Assets = 3,760.2."""
import sys, json; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solver'))
from capacity_compiler_v2 import capacity, additive, B
TA = 3760.2
def doc(ratio_met, cum_credit=0):
    return {"doc": "TL2017", "ratio_met": ratio_met, "available_amount": cum_credit,
      "baskets": [
        B("PI(a)+(b)(ii) LP->nonLP", "R", 100, .0425, shared_pool="ab"),
        B("PI(b)(i) Similar Business", "N", 50, .02, from_any=True),
        B("PI(t) JV/UnSub if FCCR test", "U", 0, unlimited_if_ratio=True, from_any=True, shared_pool="t"),
        B("PI(t) JV (N)", "N", 0, unlimited_if_ratio=True, from_any=True, shared_pool="t"),
        B("PI(u) general", "ANY", 120, .05, from_any=True),
        B("RP(g) general RP + Cumulative Credit", "ANY", 125, .0425, aa=True, from_any=True),
      ],
      "blocked_nodes": []}
for label, rm in (("FCCR test met", True), ("FCCR test not met", False)):
    s = {"total_assets": TA, "documents": [doc(rm)]}
    cap, flows = capacity(s)
    print(label, "| certified capacity to U+N:", cap if cap == "UNBOUNDED" else float(cap),
          "| flows:", {k: float(v) for k, v in flows.items()} if flows else None, "| additive:", additive(s))
