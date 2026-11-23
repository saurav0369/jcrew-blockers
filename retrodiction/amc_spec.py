"""AMC pilot spec. Governing doc: Credit Agreement (Apr 30 2013) as amended through the Ninth Amendment (Mar 8 2021; conformed copy,
EX-10.1 acc 0001104659-21-033869); Tenth (Mar 2021), Eleventh (Dec 2021), Twelfth (Jan 2023) amendments read: they change only the
revolver covenant / Covenant Suspension Period, not Section 6.04. Units $M.
Inputs: Consolidated EBITDA proxy = reported Adjusted EBITDA FY2023 = 425.8 (8-K EX-99.1, Feb 28 2024). Total Assets FY2023 = 9,009.2.
Available Equity Amount (6.04(n)(C)): lower bound 0; upper bound 2,888.5 = equity proceeds 2020-2023 in XBRL cash-flow tags
(264.7+1570.7+220.4+832.7), before any 'Otherwise Applied' deductions and excluding pre-2020 and 2024 issuances.
Available Amount and Available RP Capacity set to 0. Branch on whether the '2026 Notes Covenant Discharge' had occurred (not checked)."""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solver'))
from capacity_compiler_v2 import capacity, additive, B
EB, TA = 425.8, 9009.2
def BE(i, to, floor, pe, **kw):
    b = B(i, to, floor, **kw); b["pct_ebitda"] = pe; return b
def doc(discharged, aea):
    if not discharged:
        bs = [B("6.04(c)(iii)(A) LP->non-guarantor RS, NON-CASH cap", "R", 10),
              BE("6.04(n)(A) general", "ANY", 100, .15, aa=True, from_any=True),
              BE("6.04(y) Similar Business", "N", 50, .075, from_any=True)]
        blocked = ["U"]           # 'prior to the 2026 Notes Covenant Discharge ... will not ... make an Investment in an Unrestricted Subsidiary'
    else:
        bs = [BE("6.04(c)(iii)(A) LP->non-guarantor RS", "R", 300, .30, shared_pool="cz"),
              BE("6.04(z)(i) UnSub", "U", 300, .30, from_any=True, shared_pool="cz"),
              BE("6.04(n)(A) general", "ANY", 400, .40, aa=True, from_any=True),
              BE("6.04(y) Similar Business", "N", 300, .30, from_any=True),
              B("6.04(u) TLR<=5.0x unlimited (not met)", "ANY", 0, unlimited_if_ratio=True, from_any=True)]
        blocked = []
    return {"doc": "CA2013", "ratio_met": False, "available_amount": aea, "baskets": bs, "blocked_nodes": blocked,
            "pass_through": [{"id": "pt", "funded_by": []}]}
for disc in (False, True):
    for aea in (0, 2888.5):
        for obj in ("outside", "exit_loan_parties"):
            s = {"total_assets": TA, "ebitda": EB, "documents": [doc(disc, aea)]}
            if obj != "outside": s["objective"] = obj
            cap, fl = capacity(s)
            print(f"discharged={disc!s:5} AEA={aea:7} objective={obj:18} certified={float(cap):9.1f}",
                  {k: round(float(v), 1) for k, v in fl.items()})
