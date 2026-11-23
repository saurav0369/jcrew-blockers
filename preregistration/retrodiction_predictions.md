# Retrodiction predictions (each written BEFORE reading that case's event filing)

## Case 1: Trinseo (written 2026-11-21, before opening the Sep 2023 8-K/new credit agreement beyond its cover page)
Governing doc: Credit Agreement (Sep 6, 2017) as amended through 2023 SOFR Amendment (Jun 30, 2023); EX-10.2, acc 0001558370-23-013353. Access: read-directly (sections quoted in retro/trinseo_spec.py comments and below).
Key clauses (verbatim, short):
- No investments covenant as such (Section 8.02 "[Reserved]"); investments are policed as Restricted Investments under the RP covenant.
- Permitted Investment (t): "Investments in joint ventures and Unrestricted Subsidiaries" unlimited if pro forma FCCR is "not lower than immediately prior" or >= 2.25x, AND fair-market-value consideration is received.
- Permitted Investment (u): greater of $120M and 5.0% of Total Assets. (b)(i): Similar Business, greater of $50M and 2.0%. (a): Loan Party -> non-Loan-Party cap greater of $100M and 4.25%.
- RP (g): greater of $125M and 4.25% of Total Assets plus Cumulative Credit. RP (l): unlimited if Total Net Leverage <= 2.00x (not modeled as met).
- No J.Crew-style blocker found (no "material intellectual property" text in the document).
Solver output (frozen v2): FCCR prong met -> UNBOUNDED to U and to N (non-subsidiary JV / any Person). If not met -> certified 423.0M (all via L->N), additive survey count 582.8M. Cumulative Credit set to 0 (lower bound; not computed).
PREDICTION: open routes = N (JVs / non-subsidiary persons) and U, both potentially unlimited via PI(t), subject to an FMV-consideration condition. If the actual transaction moved value outside the Subsidiary perimeter or to an unrestricted sub, case passes on route; on size, passes if PI(t) applied (unbounded) or if transfer <= 423M.
Caveat: PI(t)'s FMV-consideration condition means the route is open for exchanges, not gifts; capacity counts collateral moved, not value lost.

### Case 1 outcome (read AFTER prediction hash 8070c4ae...)
Source (read-directly): new Credit Agreement, Sep 8 2023, EX-10.1 acc 0001104659-23-099167, definition of "Transactions":
"(c) contribution by Trinseo LLC of the JV Interests to the Co-Borrower". Co-Borrower is a subsidiary of the new deal's Parent (Trinseo Luxco),
a sister of Trinseo Holdings, so it is outside "Subsidiary of the Lead Borrower" under the 2017 agreement -> route N.
Size: Trinseo's investment in Americas Styrenics, book value $249.2M at Sep 30 2023 (10-Q, Note 6) -- book value, not a reported transfer price.
Result: route N had positive certified capacity (423.0M even if the FCCR prong of PI(t) is not met; unbounded if met); 249.2 <= 423.0. PASS on route and size.
Limits: (1) the solver predicted the route was OPEN; it did not single out N over U (both open). (2) The other half of the deal (double-dip intercompany loan
+ limited guaranties from non-guarantor subs) is a debt-capacity mechanism the v2 solver does not model. (3) Which basket the company relied on is not disclosed.

## Case 2: Bausch Health (written 2026-11-21, before reading the Aug 2022 event filing)
Governing doc: Fourth A&R Credit and Guaranty Agreement (Jun 1 2018) as amended by Second Amendment (May 10 2022), EX-10.1, acc 0001193125-22-146413. Access: read-directly.
Key clauses: 6.06(b)(ii) unlimited investments among Restricted Subsidiaries; 6.06(d) UnSub/Similar Business: greater of $300M and 12% of EBITDA;
6.06(x) JV/UnSub: greater of $437.5M and 17.5% of EBITDA per fiscal year (carry-forward ignored); 6.06(q) general: greater of $1,000M and 40% of EBITDA
+ Shared RP Amount (set 0); 6.06(dd) unlimited if Total Leverage <= 5.00x; 6.06(p)(ii) SpinCo may be designated Unrestricted if RemainCo Total Leverage <= 7.60x.
Section 5.10 blocker: no designation of a sub owning Material Intellectual Property, SpinCo entities excepted.
Inputs: TA 29,202 (XBRL FY2021); EBITDA proxy 3,472 (reported Adjusted EBITDA FY2021). Redline ambiguity: pre-amendment numbers run as alternative.
Solver output: certified capacity to U (and to N; same pools) = 2,413.0M with amended values; 1,900.0M with pre-amendment values; UNBOUNDED if TLR <= 5.0x (judged not met).
Separately, the SpinCo route 6.06(p)(ii) is UNBOUNDED subject to RemainCo TLR <= 7.60x.
PREDICTION: route U is open. Size: up to ~2.4B through general/UnSub baskets for any asset; for the SpinCo itself, effectively unlimited if the 7.60x test is met.
Pass if actual transfer went to an Unrestricted Subsidiary and its value <= 2,413M, or relied on the SpinCo designation route.

### Case 2 outcome (read AFTER prediction hash 2aaf762b...)
Source (read-directly): 8-K EX-99.1, Nov 29 2022 (acc 0001193125-22-294492): Bausch Health "has designated 1261229 B.C. Ltd., the entity that directly or
indirectly holds 88.7% of the issued and outstanding shares of Bausch + Lomb ... as an unrestricted subsidiary ... in accordance with the terms of the
Company's debt documents." No credit-agreement amendment was found on EDGAR between May 10 and Nov 29 2022 (full-text search; Oct 2022 exhibits were indentures).
Route: U via designation of the SpinCo holder. Size: 88.7% of B+L is a multi-billion stake (not priced here), above the 2,413M general/UnSub capacity,
so only the SpinCo route 6.06(p)(ii) (unbounded subject to RemainCo TLR <= 7.60x) fits. PASS on route; size consistent only with the conditional unbounded route.
Limits: (1) LOW INFORMATION CASE: the May 2022 amendment wrote the SpinCo unrestricting route in by name, so finding it is reading, not discovery.
(2) Whether the 7.60x test was met was not checked. (3) The Aug 2022 38.6% step listed in the plan doc was not separately located in a filing.

## Case 3: AMC Entertainment (written 2026-11-21, before reading the Jul 2024 event filings)
Governing doc: Credit Agreement (Apr 30 2013) as amended through Ninth Amendment (conformed, acc 0001104659-21-033869); 10th-12th amendments
read and found not to touch Section 6.04. Access: read-directly. Scope: credit agreement only (AMC's 2026 notes indentures not modeled).
Key clauses: 6.04(c)(iii)(A) Loan Party -> non-guarantor restricted sub: pre-discharge greater of $150M / 22.5% EBITDA, NON-CASH capped at $10M;
6.04(n) general: pre-discharge greater of $100M / 15% EBITDA, plus Available Amount, plus Available Equity Amount (AEA = net equity proceeds since 2013),
plus Available RP Capacity; prior to the 2026 Notes Covenant Discharge, NO investment in Unrestricted Subsidiaries (U blocked).
Inputs: EBITDA proxy 425.8; AEA lower bound 0, upper bound 2,888.5 (equity proceeds 2020-23, before deductions).
Solver output (value leaving the Loan Parties):
- pre-discharge: 160M (AEA=0) to 3,048.5M (AEA upper); U closed; routes open = R (non-guarantor restricted sub) and N.
- post-discharge: 1,000M (AEA=0) to 3,888.5M (AEA upper); U opens.
PREDICTION: the dropdown, if any, goes to a non-guarantor RESTRICTED subsidiary or outside the Subsidiary perimeter (R/N), NOT to an unrestricted sub
(unless the 2026 notes covenants had been discharged). Size: the AEA (equity raised 2021-2023) is the only basket big enough for a transfer
above ~160M, so a large transfer implies reliance on the equity-proceeds builder.

### Case 3 outcome (read AFTER prediction hash 02160f0a...)
Source (read-directly): 8-K Jul 22 2024 (acc 0001104659-24-081453): AMC "transferred certain leases, owned real property and related assets and rights in
respect of 175 theatres ... to Muvico, along with certain intellectual property, including the AMC brand name". "Each of Muvico and Centertainment is an
'unrestricted subsidiary' under the Existing Term Loans and the Existing First Lien Notes". Same day, the Fourteenth Amendment, signed by lenders constituting
the Required Lenders, removed negative covenants and those lenders "consented to all of the transactions described herein".
Route: U. Predicted: U closed (pre-discharge clause). RESULT: FAIL under the pre-registered criteria.
Post-hoc reading (NOT part of the pre-registered test): the transfer was made with majority-lender consent that stripped the covenants, i.e. a consent-type
LME. The solver's 'U closed' is consistent with the company needing that consent, but this explanation was formed after seeing the outcome.
Protocol error: the Thirteenth Amendment (Jun 23 2023) was not found by the EDGAR search and was not read; the governing document was incomplete.

## Pilot tally (pre-registered rule: pass if >= 2 of 3)
Trinseo PASS (informative: non-subsidiary route found in a 2017 agreement). Bausch PASS (low information: route written in by name in 2022).
AMC FAIL (consent transaction; the clause-reading route was closed). Formal result: 2/3 -> pilot passes. Substantive result: 1 informative pass.
Controls (3 non-event borrowers) NOT YET RUN, so specificity is unknown.

## Controls (modeled 2026-11-21 after the metric and reading rule were fixed in retrodiction_protocol.md, hash 34d69be3...)
Spec and quotes: retro/controls_spec.py. Lower-bound branch, value reaching U or N (outside every covenant) / total assets:
  Gannett 0.0% (0.0 / 2,181.2)   Thryv 5.7% (45.0 / 783.2)   Vestis 7.7% (225.0 / 2,932.4)
Event cases, same metric: Trinseo 11.2% (423.0 / 3,760.2); Bausch 8.3% (2,413 / 29,202); AMC 1.7% (150.0 / 9,009.2).
(Correction: the protocol text listed AMC as 160/9,009.2 = 1.8%; 160 was the 'exit Loan Parties' figure. Same-objective figure is 150 -> 1.7%.)
Reading rule: not all three controls fall inside the event range (Gannett is below it), so the pre-registered 'does not separate' conclusion is not triggered.
But two of three controls sit inside the event range and the samples are 3 vs 3: certified capacity as a share of assets shows NO usable separation.
POST-HOC observation (formed after seeing the controls, to be tested on new cases, not claimed): both informative event cases had an unlimited route behind a
test a stressed company can pass (Trinseo: FCCR 'not lower than immediately prior'; Bausch: RemainCo leverage <= 7.60x). The controls' unlimited routes need
tests a stressed firm is unlikely to pass (Vestis: net leverage <= 4.00x; Gannett: first-lien net leverage <= 1.0x; Thryv: none).
