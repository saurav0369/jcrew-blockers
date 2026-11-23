"""Full-agreement ("stack") backtest, per stack_prereg.md.
Usage: python3 stack_backtest.py BLOCKERS.json EVENTS.json PROVISIONS.json [--weak-chewy]
"""
import json, statistics, sys
from collections import Counter

def provisions(b, extra):
    p = [{"reaches": {"U"} | ({"R"} if b["covers_nonguarantor_subs"] == "YES" else set())
                     | ({"N"} if b["covers_outside_group"] == "YES" else set()),
          "scope": "ip_only" if b["assets"] == "IP only" else "non_ip"}]
    p += [{"reaches": set(x["reaches"]), "scope": x["scope"]} for x in extra.get(b["id"], [])]
    return p

def covers(p, d, e):
    if d not in p["reaches"]:
        return False
    if e["assets_moved"] == "IP":
        return True
    if p["scope"] == "non_ip":
        return True
    if p["scope"] == "substantially_all":
        return "ubstantially all" in e["what_moved"]
    return False

def stops(b, e, extra, chewy, omni):
    if b["id"] in omni:
        return True
    if e["event"] == "PetSmart" and b["id"] in chewy:
        return True
    ps = provisions(b, extra)
    cov = lambda d: any(covers(p, d, e) for p in ps)
    r = e["route"]
    return all(cov(d) for d in r.split("+")) if "+" in r else any(cov(d) for d in r.split(">"))

def run(blockers, events, prov, weak=False):
    extra = {}
    for x in prov["extra_provisions"]:
        extra.setdefault(x["id"], []).append(x)
    chewy = set(prov["chewy_strong"]) | (set(prov["chewy_weak"]) if weak else set())
    omni = {x["id"] for x in prov["omni"]}
    tested = [e for e in events if e["in_test"] == "Included"]
    scores = {b["id"]: sum(stops(b, e, extra, chewy, omni) for e in tested) for b in blockers}
    per_event = {e["event"]: sum(stops(b, e, extra, chewy, omni) for b in blockers) for e in tested}
    return scores, per_event, len(tested)

if __name__ == "__main__":
    B, E, P = (json.load(open(a)) for a in sys.argv[1:4])
    scores, per_event, n = run(B, E, P, "--weak-chewy" in sys.argv)
    s = list(scores.values())
    print("median", statistics.median(s), "| <=3:", sum(v <= 3 for v in s), "of", len(s), "| all", n, ":", sum(v == n for v in s))
    print("distribution", sorted(Counter(s).items()))
    for k, v in sorted(per_event.items(), key=lambda kv: -kv[1]):
        print(f"  {k:24s} {v}/{len(s)}")
