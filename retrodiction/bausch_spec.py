"""Bausch Health pilot spec. Governing doc: Fourth A&R Credit and Guaranty Agreement (Jun 1 2018) as amended by the Second Amendment
(May 10 2022), EX-10.1 to 8-K acc 0001193125-22-146413 (conformed redline; where the extracted text shows two numbers, the second is
taken as the amended value and the first is run as an alternative branch). Units $M.
Inputs: Total Assets FY2021 10-K XBRL = 29,202. EBITDA proxy = company-reported Adjusted EBITDA FY2021 = 3,472 (8-K EX-99.1, Feb 23 2022);
the agreement's 'Consolidated Adjusted EBITDA' may differ. Shared RP Amount and Available Amount set to 0 (lower bound)."""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solver'))
from capacity_compiler_v2 import capacity, additive, B
TA, EB = 29202, 3472
def BE(i, to, floor, pe, **kw):
    b = B(i, to, floor, **kw); b["pct_ebitda"] = pe; return b
def doc(amended=True, ratio_met=False):
    if amended: d, x, xpct, q = .12, 437.5, .175, .40
    else:       d, x, xpct, q = .086, 600, 0, .285   # old (x) was 1.50% of Total Assets: handled below
    bs = [
        B("6.06(b)(ii) among Restricted Subs (unlimited)", "R", 10**9),
        BE("6.06(d) UnSub/Similar Business", "U", 300, d, from_any=True, shared_pool="d"),
        BE("6.06(d) Similar Business JV (N)", "N", 300, d, from_any=True, shared_pool="d"),
        BE("6.06(x) JV/UnSub per FY", "U", x, xpct, from_any=True, shared_pool="x"),
        BE("6.06(x) JV (N)", "N", x, xpct, from_any=True, shared_pool="x"),
        BE("6.06(q) general", "ANY", 1000, q, from_any=True),
        B("6.06(dd) TLR<=5.0x unlimited", "U", 0, unlimited_if_ratio=True, from_any=True),
    ]
    if not amended:
        bs[3]["pct_assets"] = .015; bs[4]["pct_assets"] = .015
    return {"doc": "CA2018", "ratio_met": ratio_met, "baskets": bs, "pass_through": [{"id": "pt", "funded_by": []}]}
for lab, am in (("amended values", True), ("pre-amendment values", False)):
    s = {"total_assets": TA, "ebitda": EB, "documents": [doc(am)]}
    cap, fl = capacity(s)
    print(lab, "| TLR<=5.0 not met | certified to U+N:", float(cap), "| flows:", {k: float(v) for k, v in fl.items()})
s = {"total_assets": TA, "ebitda": EB, "documents": [doc(True, True)]}
print("if TLR<=5.0x met:", capacity(s)[0])
print("SpinCo-only route, 6.06(p)(ii): designation of SpinCo as Unrestricted is UNBOUNDED if RemainCo TLR <= 7.60x, no EoD, notice given.")
