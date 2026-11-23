"""Confidence intervals and robustness checks for the paper (Section 4.3 and Table 4 intervals).
Run: python3 robustness.py   (standard library only; bootstrap seed fixed)"""
import json, math, os, random, statistics, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "stack"))
import stack_backtest as sb

B = json.load(open(os.path.join(H, "data", "blockers.json")))
ALL_E = json.load(open(os.path.join(H, "data", "events.json")))
P = json.load(open(os.path.join(H, "stack", "stack_provisions.json")))
E = [e for e in ALL_E if e["in_test"] == "Included"]

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(100 * (c - h)), round(100 * (c + h))

def clause_scores(blockers, events, non_ip_counts=True):
    def reach(b, d):
        return d == "U" or (d == "R" and b["covers_nonguarantor_subs"] == "YES") or (d == "N" and b["covers_outside_group"] == "YES")
    def stops(b, e):
        if e["assets_moved"] != "IP" and (not non_ip_counts or b["assets"] != "IP and other assets"):
            return False
        r = e["route"]
        return all(reach(b, d) for d in r.split("+")) if "+" in r else any(reach(b, d) for d in r.split(">"))
    return [sum(stops(b, e) for e in events) for b in blockers]

def summary(s, n_ev):
    return {"median": statistics.median(s), "stop<=3": sum(v <= 3 for v in s), "stop_all": sum(v == n_ev for v in s)}

out = {}
# Wilson intervals for the six gaps
defined = [b for b in B if b["materiality_decided_by"] != "Undefined term"]
ex = [b for b in B if b["covers_exclusive_licences"] in ("YES", "NO")]
gaps = {
    "not_sacred": (sum(b["sacred_right"] != "Yes" for b in B), len(B)),
    "ip_only": (sum(b["assets"] == "IP only" for b in B), len(B)),
    "no_outside": (sum(b["covers_outside_group"] == "NO" for b in B), len(B)),
    "no_nonguarantor": (sum(b["covers_nonguarantor_subs"] == "NO" for b in B), len(B)),
    "no_excl": (sum(b["covers_exclusive_licences"] == "NO" for b in ex), len(ex)),
    "borrower_decides": (sum(b["materiality_decided_by"] == "Borrower" for b in defined), len(defined)),
    "sacred": (sum(b["sacred_right"] == "Yes" for b in B), len(B)),
    "sub_sacred": (sum(b["subordination_sacred"] == "Yes" for b in B), len(B)),
}
out["wilson"] = {k: {"k": k_, "n": n, "pct": round(100 * k_ / n), "ci95": wilson(k_, n)} for k, (k_, n) in gaps.items()}

# Robustness of the headline under alternative rules
st, _, _ = sb.run(B, ALL_E, P)
sw, _, _ = sb.run(B, ALL_E, P, weak=True)
variants = {
    "A. Clause level (baseline)": clause_scores(B, E),
    "B. Clause level, non-IP coverage never counts": clause_scores(B, E, non_ip_counts=False),
    "C. Whole agreement, strong Chewy (baseline)": list(st.values()),
    "D. Whole agreement, weak Chewy also counts": list(sw.values()),
}
out["variants"] = {k: summary(v, len(E)) for k, v in variants.items()}

# Leave-one-event-out (whole agreement, baseline)
loo = []
for drop in E:
    keep = [e for e in ALL_E if e["event"] != drop["event"]]
    s, _, n = sb.run(B, keep, P)
    loo.append((drop["event"], statistics.median(list(s.values())), sum(v <= 3 for v in s.values())))
out["leave_one_out_median_range"] = [min(x[1] for x in loo), max(x[1] for x in loo)]
out["leave_one_out"] = loo

# Excluding the two IP-to-unrestricted events the clause was written for
nine = [e for e in ALL_E if e["event"] not in ("J.Crew", "Travelport")]
s9, _, n9 = sb.run(B, nine, P)
v9 = list(s9.values())
out["other_nine"] = {"events": n9, "median": statistics.median(v9), "stop_none": sum(v == 0 for v in v9),
                     "stop_none_ci95": wilson(sum(v == 0 for v in v9), len(v9))}

# Bootstrap over agreements (whole agreement): median and share stopping <= 3
rng = random.Random(20261123)
vals = list(st.values()); meds, shares = [], []
for _ in range(10000):
    smp = [rng.choice(vals) for _ in vals]
    meds.append(statistics.median(smp)); shares.append(sum(v <= 3 for v in smp) / len(smp))
meds.sort(); shares.sort()
out["bootstrap"] = {"median_ci95": [meds[249], meds[9749]], "share_le3_ci95": [round(100 * shares[249]), round(100 * shares[9749])]}

json.dump(out, open(os.path.join(H, "results", "robustness.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
