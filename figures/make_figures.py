"""Draws every figure in README.md and the paper from the released data.
Run: python3 figures/make_figures.py   (needs matplotlib)"""
import json, os, sys
from collections import Counter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(H, "stack"))
import stack_backtest as sb
B = json.load(open(os.path.join(H, "data", "blockers.json")))
E = json.load(open(os.path.join(H, "data", "events.json")))
P = json.load(open(os.path.join(H, "stack", "stack_provisions.json")))
T = [e for e in E if e["in_test"] == "Included"]

def clause_count(e):
    reach = lambda b, d: d == "U" or (d == "R" and b["covers_nonguarantor_subs"] == "YES") or (d == "N" and b["covers_outside_group"] == "YES")
    def stops(b):
        if e["assets_moved"] != "IP" and b["assets"] != "IP and other assets": return False
        r = e["route"]; return all(reach(b, d) for d in r.split("+")) if "+" in r else any(reach(b, d) for d in r.split(">"))
    return sum(map(stops, B))
_, whole, _ = sb.run(B, E, P)
nine = [e for e in E if e["event"] not in ("J.Crew", "Travelport")]
s9, _, n9 = sb.run(B, nine, P)

THEMES = {"light": dict(fg="#1f2328", muted="#57606a", grid="#d0d7de", base="#b8bec6", accent="#0b3d91"),
          "dark":  dict(fg="#e6edf3", muted="#9198a1", grid="#30363d", base="#59616b", accent="#6cb6ff")}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none"})

def frame(ax, t):
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(t["grid"]); ax.tick_params(colors=t["muted"], length=0)

def save(fig, name, theme):
    fig.savefig(os.path.join(H, "figures", f"{name}-{theme}.svg"), transparent=True, bbox_inches="tight")
    if theme == "light": fig.savefig(os.path.join(H, "figures", f"{name}.png"), dpi=200, facecolor="white", bbox_inches="tight")
    plt.close(fig)

order = sorted(T, key=lambda e: (-clause_count(e), -whole[e["event"]]))
for th, t in THEMES.items():
    # 1. backtest by dropdown
    fig, ax = plt.subplots(figsize=(9, 5.6)); frame(ax, t)
    for i, e in enumerate(order):
        y = len(order) - 1 - i; c, w = clause_count(e), whole[e["event"]]
        ax.barh(y + .2, c, .38, color=t["base"]); ax.barh(y - .2, w, .38, color=t["accent"])
        ax.text(c + 1, y + .2, c, va="center", fontsize=9, color=t["muted"]); ax.text(w + 1, y - .2, w, va="center", fontsize=9, color=t["fg"], weight="bold")
    ax.set_yticks(range(len(order))); ax.set_yticklabels([f'{e["event"].replace(" (American Crew)", "")}  {e["year"]}' for e in order][::-1], color=t["fg"])
    ax.axvline(len(B) / 2, color=t["muted"], lw=.8, ls=(0, (3, 3))); ax.text(len(B) / 2 + 1, len(order) - .35, "half of the 91 agreements", color=t["muted"], fontsize=9)
    ax.set_xlim(0, 100); ax.set_xlabel("Agreements (of 91) that would have stopped the dropdown", color=t["muted"])
    from matplotlib.patches import Patch
    lg = ax.legend(handles=[Patch(color=t["base"], label="J.Crew clause alone"), Patch(color=t["accent"], label="Whole agreement")], frameon=False, loc="lower right"); [x.set_color(t["fg"]) for x in lg.get_texts()]
    save(fig, "backtest", th)
    # 2. the nine later-pattern dropdowns
    cnt = Counter(s9.values()); xs = range(n9 + 1)
    fig, ax = plt.subplots(figsize=(9, 3.6)); frame(ax, t)
    ax.bar(xs, [cnt.get(k, 0) for k in xs], .72, color=[t["accent"] if k == 0 else t["base"] for k in xs])
    for k in xs:
        if cnt.get(k): ax.text(k, cnt[k] + 1, cnt[k], ha="center", fontsize=10, color=t["fg"] if k == 0 else t["muted"], weight="bold" if k == 0 else "normal")
    ax.set_xticks(list(xs)); ax.set_yticks([]); ax.set_xlabel("Of the nine dropdowns that did not follow the J.Crew pattern, how many the agreement stops", color=t["muted"])
    save(fig, "nine", th)
    # 3. entrenchment contrast
    sac = sum(b["sacred_right"] == "Yes" for b in B); sub = sum(b["subordination_sacred"] == "Yes" for b in B)
    fig, ax = plt.subplots(figsize=(9, 1.9)); frame(ax, t)
    ax.barh([1, 0], [len(B), len(B)], .55, color=t["grid"]); ax.barh([1, 0], [sub, sac], .55, color=[t["base"], t["accent"]])
    ax.text(sub + 1.2, 1, f"{sub} of 91", va="center", color=t["fg"]); ax.text(sac + 1.2, 0, f"{sac} of 91", va="center", color=t["fg"], weight="bold")
    ax.set_yticks([1, 0]); ax.set_yticklabels(["Subordination is a sacred right (anti-Serta)", "J.Crew blocker is a sacred right"], color=t["fg"])
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 91)
    save(fig, "entrenchment", th)
print("figures written to figures/")
