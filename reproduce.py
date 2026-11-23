"""Recompute every number in the paper from data/ and fail loudly if any differs from what is published.
Run: python3 reproduce.py   (no dependencies beyond the Python standard library)"""
import json, os, statistics, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
B = json.load(open(os.path.join(D, "blockers.json")))
E = [e for e in json.load(open(os.path.join(D, "events.json"))) if e["in_test"] == "Included"]

def reach(b, d):  # destination covered? U = unrestricted sub, R = non-guarantor restricted sub, N = outside the group
    return d == "U" or (d == "R" and b["covers_nonguarantor_subs"] == "YES") or (d == "N" and b["covers_outside_group"] == "YES")
def stops(b, e):  # the stop rule published on the page
    if e["assets_moved"] != "IP" and b["assets"] != "IP and other assets":
        return False
    r = e["route"]
    return all(reach(b, d) for d in r.split("+")) if "+" in r else any(reach(b, d) for d in r.split(">"))

scores = [sum(stops(b, e) for e in E) for b in B]
pct = lambda k, n: round(100 * k / n)
defined = [b for b in B if b["materiality_decided_by"] != "Undefined term"]
ex = [b for b in B if b["covers_exclusive_licences"] in ("YES", "NO")]
got = {
    "blockers": len(B),
    "real dropdowns in the test": len(E),
    "median dropdowns stopped": statistics.median(scores),
    "blockers stopping only the minimum (2)": scores.count(min(scores)),
    "blockers stopping all": scores.count(len(E)),
    "% IP only": pct(sum(b["assets"] == "IP only" for b in B), len(B)),
    "% not reaching outside the group": pct(sum(b["covers_outside_group"] == "NO" for b in B), len(B)),
    "% not reaching non-guarantor subs": pct(sum(b["covers_nonguarantor_subs"] == "NO" for b in B), len(B)),
    "% borrower decides materiality (of defined)": pct(sum(b["materiality_decided_by"] == "Borrower" for b in defined), len(defined)),
    "% no exclusive-licence coverage": pct(sum(b["covers_exclusive_licences"] == "NO" for b in ex), len(ex)),
    "blockers that are sacred rights": sum(b["sacred_right"] == "Yes" for b in B),
    "contracts with anti-subordination sacred rights": sum(b["subordination_sacred"] == "Yes" for b in B),
}
published = {
    "blockers": 91, "real dropdowns in the test": 11, "median dropdowns stopped": 2,
    "blockers stopping only the minimum (2)": 56, "blockers stopping all": 3,
    "% IP only": 87, "% not reaching outside the group": 87, "% not reaching non-guarantor subs": 69,
    "% borrower decides materiality (of defined)": 36, "% no exclusive-licence coverage": 46,
    "blockers that are sacred rights": 4, "contracts with anti-subordination sacred rights": 53,
}
# Full-agreement ("stack") backtest: preregistration/stack_prereg.md, provisions in stack/
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "stack"))
import stack_backtest as sb
P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stack", "stack_provisions.json")))
ALL_E = json.load(open(os.path.join(D, "events.json")))
st, st_ev, _ = sb.run(B, ALL_E, P)
sw, _, _ = sb.run(B, ALL_E, P, weak=True)
stv, swv = list(st.values()), list(sw.values())
got.update({
    "stack: median dropdowns stopped": statistics.median(stv),
    "stack: agreements stopping at most 3": sum(v <= 3 for v in stv),
    "stack: agreements stopping all": stv.count(len(E)),
    "stack: agreements with a strong Chewy blocker": len(P["chewy_strong"]),
    "stack: agreements with any Chewy blocker": len(P["chewy_strong"]) + len(P["chewy_weak"]),
    "stack: agreements with an omni-blocker": len(P["omni"]),
    "stack (weak Chewy counted): median dropdowns stopped": statistics.median(swv),
})
published.update({
    "stack: median dropdowns stopped": 2, "stack: agreements stopping at most 3": 58, "stack: agreements stopping all": 4,
    "stack: agreements with a strong Chewy blocker": 8, "stack: agreements with any Chewy blocker": 21,
    "stack: agreements with an omni-blocker": 1, "stack (weak Chewy counted): median dropdowns stopped": 3,
})
# Robustness and intervals (robustness.py)
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location("rob", os.path.join(os.path.dirname(os.path.abspath(__file__)), "robustness.py"))
rob = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(rob)
R = rob.out
got.update({
    "robust: other nine dropdowns, agreements stopping none": R["other_nine"]["stop_none"],
    "robust: leave-one-out median range": R["leave_one_out_median_range"],
    "robust: clause level with no non-IP credit, median": R["variants"]["B. Clause level, non-IP coverage never counts"]["median"],
    "robust: bootstrap 95% interval for median": R["bootstrap"]["median_ci95"],
    "robust: Wilson 95% interval, IP only": list(R["wilson"]["ip_only"]["ci95"]),
    "robust: Wilson 95% interval, sacred right": list(R["wilson"]["sacred"]["ci95"]),
})
published.update({
    "robust: other nine dropdowns, agreements stopping none": 52,
    "robust: leave-one-out median range": [1, 2],
    "robust: clause level with no non-IP credit, median": 2,
    "robust: bootstrap 95% interval for median": [2, 3],
    "robust: Wilson 95% interval, IP only": [78, 92],
    "robust: Wilson 95% interval, sacred right": [2, 11],
})
# Pre-registrations whose fingerprints were recorded before their results were seen
import hashlib
PRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preregistration")
RECORDED = {
    "last_war_prereg.md": "7b9d6a321f97cad3fc391db2935420c6c30cfd107b0d2af0c58ae9f99cdd9447",
    "stack_prereg.md": "f23654f1ba811ab1eb71d4831f31421aa2334e2dc9d7b00b89a2010c7a274e76",
    "retrodiction_protocol.md": "34d69be34773bf4415f91f0e43dd6f4ed7b7ebdf4eb0fa78817c77014359e9de",
    "sue_rule.md": "2d23d89fc67796f4fe0fbd1254223b2839842ea22d098d86b4c20bfcdfde3307",
}
for f, h in RECORDED.items():
    got["pre-registration unchanged: " + f] = hashlib.sha256(open(os.path.join(PRE, f), "rb").read()).hexdigest()[:16]
    published["pre-registration unchanged: " + f] = h[:16]
bad = 0
for k, v in published.items():
    ok = got[k] == v
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {k}: recomputed {got[k]}, published {v}")
for e in E:
    print(f"     {e['event']:24} stopped by {sum(stops(b, e) for b in B):2}/{len(B)}")
if bad:
    sys.exit(f"{bad} published number(s) do not match the data")
print("ALL PUBLISHED NUMBERS REPRODUCED")
