"""
Certified leakage capacity, v2.

New in v2 (each one is a route or a constraint that additive basket sums cannot see):
  1. Several debt documents at once (term loan, notes, ABL). Every transfer must be allowed by EVERY document,
     so capacity is computed jointly, not as the smallest single-document number.
  2. A node N for affiliates outside the "Subsidiary" definition (joint ventures, sister entities:
     Xerox 2025-26, Trinseo 2023). Blockers written against "Unrestricted Subsidiaries" do not reach N.
  3. Ratio-based baskets ("unlimited if leverage <= x"). If the test is met, capacity is unbounded and the
     output says so instead of returning a number.
  4. The additive benchmark (how analysts and Octus-style surveys count) printed next to the certified value.

Nodes: L loan parties, R non-loan-party restricted subs, U unrestricted subs, N non-subsidiary affiliates.
Edges: L->R, L->U, L->N, R->U, R->N.  Objective: value reaching U or N (outside every covenant).
"""
from fractions import Fraction as F
from scipy.optimize import linprog
import json, sys

EDGES = ["LR", "LU", "LN", "RU", "RN"]
TARGET = {"U": ["LU", "RU"], "N": ["LN", "RN"], "R": ["LR"]}


def edges_for(to, from_any=False):
    """from_any: the basket covers investments by any Restricted Subsidiary (typical of general and
    ratio baskets: "the Borrower and its Restricted Subsidiaries"), so it can also fund R->U and R->N."""
    out = {"R": ["LR"], "U": ["LU"], "N": ["LN"], "ANY": ["LR", "LU", "LN"]}[to]
    if from_any:
        out = out + [e for e in {"U": ["RU"], "N": ["RN"], "ANY": ["RU", "RN"], "R": []}[to]]
    return out


def cap_of(b, ta, ebitda):
    return max(F(str(b.get("floor", 0))), F(str(b.get("pct_assets", 0))) * ta, F(str(b.get("pct_ebitda", 0))) * ebitda)


def build(spec):
    ta, eb = F(str(spec.get("total_assets", 0))), F(str(spec.get("ebitda", 0)))
    cols = {e: i for i, e in enumerate(EDGES)}                 # global flows
    def new(key):
        cols[key] = len(cols); return cols[key]
    rows = []                                                   # (dict col->coef, rhs)  meaning sum <= rhs
    for d in spec["documents"]:
        dn = d["doc"]
        alloc = {}                                              # (basket, edge) -> col
        for b in d["baskets"]:
            for e in edges_for(b["to"], b.get("from_any", False)):
                alloc[(b["id"], e)] = new((dn, b["id"], e))
            if b.get("plus_available_amount"):
                alloc[(b["id"], "AA")] = new((dn, b["id"], "AA"))
        # every L-origin flow must be covered by this document's baskets
        for e in ["LR", "LU", "LN"]:
            r = {cols[e]: 1}
            for (bid, ee), c in alloc.items():
                if ee == e: r[c] = r.get(c, 0) - 1
            rows.append((r, F(0)))
        # basket caps, shared pools take the smallest stated cap
        pools = {}
        for b in d["baskets"]:
            if b.get("unlimited_if_ratio") and d.get("ratio_met"):
                continue
            key = b.get("shared_pool") or b["id"]
            cap = cap_of(b, ta, eb)
            p = pools.setdefault(key, {"cap": cap, "cols": [], "aa": []})
            p["cap"] = min(p["cap"], cap)
            p["cols"] += [c for (bid, e), c in alloc.items() if bid == b["id"] and e != "AA"]
            if (b["id"], "AA") in alloc: p["aa"].append(alloc[(b["id"], "AA")])
        for p in pools.values():
            r = {c: 1 for c in p["cols"]}
            for c in p["aa"]: r[c] = -1
            rows.append((r, p["cap"]))
        aa_cols = [c for (bid, e), c in alloc.items() if e == "AA"]
        if aa_cols:
            rows.append(({c: 1 for c in aa_cols}, F(str(d.get("available_amount", 0)))))
        # R-origin flows need this document's pass-through, limited to proceeds from the named baskets
        funded = set().union(*[set(p["funded_by"]) for p in d.get("pass_through", [])]) if d.get("pass_through") else set()
        r = {cols["RU"]: 1, cols["RN"]: 1}
        for (bid, e), c in alloc.items():
            if e == "LR" and bid in funded: r[c] = -1
            if e in ("RU", "RN"): r[c] = -1          # R-origin use of a from_any basket
        rows.append((r, F(0)))
        # blockers: total flow into a blocked node type is zero under this document
        for node in d.get("blocked_nodes", []):
            rows.append(({cols[e]: 1 for e in TARGET[node]}, F(0)))
        for e in d.get("blocked_edges", []):           # e.g. a blocker on Loan-Party IP going to U blocks LU only
            rows.append(({cols[e]: 1}, F(0)))
    # conservation at R
    rows.append(({cols["RU"]: 1, cols["RN"]: 1, cols["LR"]: -1}, F(0)))
    n = len(cols)
    c = [0] * n
    # default objective: value reaching U or N (outside every covenant).
    # "exit_loan_parties": value leaving the guarantor group at all (into R, U or N) -> the lenders' collateral loss.
    obj = ["LR", "LU", "LN"] if spec.get("objective") == "exit_loan_parties" else ["LU", "RU", "LN", "RN"]
    for e in obj: c[cols[e]] = 1
    A = [[r.get(j, 0) for j in range(n)] for r, _ in rows]
    b = [rhs for _, rhs in rows]
    return c, A, b, cols


def certify(c, A, b, x, y):
    for row, bi in zip(A, b):
        if sum(F(a) * xi for a, xi in zip(row, x)) > bi: raise ValueError("primal infeasible")
    if any(v < 0 for v in x) or any(v < 0 for v in y): raise ValueError("negative variable")
    for j in range(len(c)):
        if sum(F(A[i][j]) * y[i] for i in range(len(A))) < c[j]: raise ValueError(f"dual infeasible at {j}")
    p = sum(F(ci) * xi for ci, xi in zip(c, x)); d = sum(bi * yi for bi, yi in zip(b, y))
    if p != d: raise ValueError(f"gap {p} != {d}")
    return p


def capacity(spec):
    c, A, b, cols = build(spec)
    r = linprog([-v for v in c], A_ub=A, b_ub=[float(v) for v in b], bounds=[(0, None)] * len(c), method="highs")
    if r.status == 3:
        return "UNBOUNDED", None
    assert r.status == 0, r.message
    x = [F(v).limit_denominator(10**6) for v in r.x]
    y = [F(-v).limit_denominator(10**6) for v in r.ineqlin.marginals]
    return certify(c, A, b, x, y), {e: x[cols[e]] for e in EDGES}


def additive(spec):
    """How surveys count: per document, every basket that can reach a non-loan party, each plus the Available Amount."""
    ta, eb = F(str(spec.get("total_assets", 0))), F(str(spec.get("ebitda", 0)))
    out = {}
    for d in spec["documents"]:
        s = F(0)
        for b in d["baskets"]:
            if b.get("unlimited_if_ratio") and d.get("ratio_met"): return {d["doc"]: "UNBOUNDED"}
            s += cap_of(b, ta, eb) + (F(str(d.get("available_amount", 0))) if b.get("plus_available_amount") else 0)
        out[d["doc"]] = s
    return out


def B(i, to, floor, pct=0, aa=False, **kw):
    return {"id": i, "to": to, "floor": floor, "pct_assets": pct, "plus_available_amount": aa, **kw}


JCREW_TL = {"doc": "TL", "available_amount": 0,
            "baskets": [B("c(iv)", "R", 150, .04, True), B("n", "ANY", 100, .0325, True, from_any=True)],
            "pass_through": [{"id": "t", "funded_by": ["c(iv)", "n"]}]}

if __name__ == "__main__":
    ok = True
    def check(label, got, want):
        global ok
        good = got == want; ok &= good
        print(f"{'PASS' if good else 'FAIL'}  {label}: got {got}, want {want}")

    s = {"total_assets": 1516.277, "documents": [JCREW_TL]}
    check("J.Crew term loan alone", capacity(s)[0], 250)
    s40 = json.loads(json.dumps(s)); s40["documents"][0]["available_amount"] = 40
    check("J.Crew, Available Amount 40: certified", capacity(s40)[0], 290)
    print("      additive benchmark for the same contract:", additive(s40)["TL"], "(counts the Available Amount twice)")

    # Discovery 1: two documents that each allow 200 can allow 0 together, because they open different routes.
    tl = {"doc": "TL", "baskets": [B("nlp", "R", 200)], "pass_through": [{"id": "pt", "funded_by": ["nlp"]}]}
    notes = {"doc": "Notes", "baskets": [B("unsub", "U", 200)]}
    check("Term loan alone (trapdoor route only)", capacity({"documents": [tl]})[0], 200)
    check("Notes alone (direct route only)", capacity({"documents": [notes]})[0], 200)
    check("Both documents together", capacity({"documents": [tl, notes]})[0], 0)

    # Discovery 2: a J.Crew blocker on U does not reach a joint venture outside "Subsidiary".
    blk = {"doc": "TL", "baskets": [B("general", "ANY", 100)], "blocked_nodes": ["U"]}
    check("Blocker on U, general basket open to any person -> value reaches N", capacity({"documents": [blk]})[0], 100)
    fix = json.loads(json.dumps(blk)); fix["blocked_nodes"] = ["U", "N"]
    check("Blocker also covering non-subsidiary affiliates", capacity({"documents": [fix]})[0], 0)

    # Discovery 3: ratio-based baskets make capacity unbounded when the test is met.
    rat = {"doc": "Notes", "ratio_met": True, "baskets": [B("ratio", "U", 0, unlimited_if_ratio=True)]}
    check("Ratio basket, test met", capacity({"documents": [rat]})[0], "UNBOUNDED")
    rat2 = json.loads(json.dumps(rat)); rat2["ratio_met"] = False
    check("Ratio basket, test failed", capacity({"documents": [rat2]})[0], 0)

    # Control: dropping the trapdoor must change the J.Crew answer.
    ctl = json.loads(json.dumps(s)); ctl["documents"][0]["pass_through"] = []
    check("Control: J.Crew without clause (t)", capacity(ctl)[0], 100)
    print("ALL CHECKS OK" if ok else "SOME CHECK FAILED"); sys.exit(0 if ok else 1)
