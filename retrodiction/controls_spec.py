"""Controls, same extraction rules, lower-bound branch (unknown builders = 0, ratio baskets not met). Units $M. Access: read-directly.
Gannett: A&R credit agreement Oct 15 2024, EX-10.1 acc 0001140361-24-043565. Permitted Intercompany Investments (d): LP -> non-LP RS <= $100M;
 Permitted Investments (q): RP/Investment Amount, cash only, $0 unless First Lien Net Leverage <= 2.0x (unlimited if <= 1.0x);
 proviso: no Loan Party may transfer any Material Assets to a non-Loan-Party Subsidiary or let a holder of Material Assets be designated unrestricted.
 TA FY2023 2,181.2.
Thryv: Term Loan Credit Agreement May 1 2024, EX-10.1 acc 0001556739-24-000025. 7.3(c) non-guarantor subs $30M; 7.3(w) UnSubs $15M (only route to U);
 7.3(aa) general $30M (not U); 7.3(n) Available Amount, 7.3(x) equity proceeds, 7.3(y) RP amounts set 0. MIP blocker covers non-guarantor subs and U.
 TA FY2023 783.2.
Vestis: Credit Agreement as amended by Amendment No. 2 (May 1 2025), EX-10.1 acc 0001967649-25-000029. PI(a) non-guarantor RS greater of $95M/25% EBITDA;
 PI(p) JV/UnSub greater of $75M/20% EBITDA (only route to U); PI(u) general greater of $150M/40% EBITDA; PI(v) unlimited if Total Net Leverage <= 4.00x
 (not modeled as met); PI(r) Applicable Amount set 0. 6.07(c) MIP blocker on U. EBITDA proxy = reported FY2024 Adjusted EBITDA 353; TA FY2024 2,932.4."""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solver'))
from capacity_compiler_v2 import capacity, B
def BE(i, to, floor, pe, **kw):
    b = B(i, to, floor, **kw); b["pct_ebitda"] = pe; return b
C = {
 "Gannett": (2181.2, 0, [B("PII(d) LP->nonLP RS (non-material assets only)", "R", 100)]),
 "Thryv":   (783.2, 0, [B("7.3(c) nonguarantor", "R", 30), B("7.3(w) UnSub", "U", 15, from_any=True),
                         B("7.3(aa) general not U", "R", 30, from_any=True, shared_pool="aa"), B("7.3(aa) general not U (N)", "N", 30, from_any=True, shared_pool="aa")]),
 "Vestis":  (2932.4, 353, [BE("PI(a) nonguarantor RS", "R", 95, .25), BE("PI(p) JV/UnSub", "U", 75, .20, from_any=True, shared_pool="p"),
                          BE("PI(p) JV (N)", "N", 75, .20, from_any=True, shared_pool="p"),
                          BE("PI(u) general", "R", 150, .40, from_any=True, shared_pool="u"), BE("PI(u) general (N)", "N", 150, .40, from_any=True, shared_pool="u")]),
}
for name, (ta, eb, bs) in C.items():
    out = []
    for obj in ("outside", "exit_loan_parties"):
        s = {"total_assets": ta, "ebitda": eb, "documents": [{"doc": name, "baskets": bs, "pass_through": [{"id": "pt", "funded_by": []}]}]}
        if obj != "outside": s["objective"] = obj
        cap, _ = capacity(s); out.append(float(cap))
    print(f"{name:8} outside(U+N)={out[0]:7.1f}  exit Loan Parties={out[1]:7.1f}  exit/TA={100*out[1]/ta:5.1f}%  outside/TA={100*out[0]/ta:5.1f}%")
