# Retrodiction pilot: pre-registered protocol (frozen before any case is modeled)

Date frozen: 2026-11-21
Solver: capacity_compiler_v2.py, sha256 c3ec70b7a9b09abdcb6b36549ba4b9c29f1c1733ce255608bc5385e3ce74d307 (self-test: ALL CHECKS OK)

## Question
Given only the credit agreement in force before a known dropdown/designation event, does the frozen solver
(a) show positive certified capacity on the route the company actually used, and
(b) show capacity at least as large as the reported transfer value?

## Pilot cases (not modeled before; J.Crew and Neiman were modeled earlier with the answer known and are excluded)
1. Trinseo: double-dip via sister entity outside "Subsidiary", Sep 2023 (route N)
2. Bausch Health: 38.6% of Bausch + Lomb shares to an unrestricted sub, Aug 2022 (route U)
3. AMC Entertainment: Muvico dropdown, Jul 2024 (route R or U; to be read from the event filing AFTER the prediction is written)

## Fixed extraction rules
Governing document = the credit agreement as amended by the last amendment filed on EDGAR before the event date.
Scope = that credit agreement only (notes indentures out of scope in the pilot; stated as a limit).
Extract, with verbatim quotes and section numbers:
- definitions of Subsidiary, Restricted/Unrestricted Subsidiary, Loan Party
- every investment basket that can reach a non-Loan-Party restricted sub (R), unrestricted sub (U), or any Person/JV (N)
- general basket, Available Amount (builder) with its starter, ratio-based unlimited baskets and whether the ratio was met
- pass-through / trapdoor clause for investments by non-Loan-Party restricted subs
- J.Crew-style or other blockers (which nodes they cover)
Financial inputs (total assets, EBITDA) from the last 10-K before the event; if a ratio test cannot be evaluated, report both branches.
Map to the v2 spec JSON without changing the solver.

## Order of work (blinding)
For each case: build spec -> run solver -> write prediction to retrodiction_predictions.md and record its sha256 ->
only then read the event filing for the actual route and transfer value.

## Pass criteria
Per case: actual route has positive certified capacity AND capacity >= reported transfer value (UNBOUNDED counts).
Pilot passes if >= 2 of 3 cases pass. Also run 3 non-event controls from the census and report capacity / total assets.
Fail -> publish census note honestly and stop this track.

## Known contamination (disclosed)
The modeling session (an AI assistant) has general knowledge of these events from training and earlier notes.
Blinding is procedural (fixed rules, prediction written first), not true ignorance. Any rule deviation is logged below.

## Deviations log
(none yet)
- 2026-11-21 Trinseo: the agreement has no standalone investments covenant (8.02 [Reserved]); investments were read under Permitted Investment + RP. Unknown builders set to 0. Not a rule change.
- 2026-11-21 Bausch: conformed redline shows old and new numbers side by side; amended values used, old values run as alternative (protocol's both-branches rule).
- 2026-11-21 AMC: Thirteenth Amendment (Jun 23 2023) missed by the search and not read (protocol error, recorded in outcome). Available Equity Amount bounds taken from XBRL equity-proceeds tags.

## Controls (added 2026-11-21 BEFORE any control is modeled)
Controls: Gannett (CIK 1579684), Thryv (CIK 1556739), Vestis (CIK 1967649): leveraged public borrowers from the wave-4 census with no
dropdown/designation LME in the event list. Chosen for leverage and availability, not by looking at their baskets.
Metric fixed in advance: certified capacity in the lower-bound branch (unknown builders = 0, ratio baskets not met) divided by total assets,
plus a flag for any ratio-unlimited route whose test is plausibly met. Same extraction rules as the event cases.
Comparison: event cases (lower-bound branch) Trinseo 423.0/3,760.2 = 11.2%; Bausch 2,413/29,202 = 8.3%; AMC 160/9,009.2 = 1.8%.
Reading rule fixed now: if all three controls fall inside the event range (1.8%-11.2%), capacity does NOT separate event from non-event firms.
