# Methods

The paper ([PDF](../paper/Sharma_JCrew_Blockers_2026.pdf)) is the full account. This page is the short version for someone checking the code.

## 1. Sample

An EDGAR full-text search for "Material Intellectual Property", "Unrestricted Subsidiary" and "Credit Agreement" in EX-10 exhibits filed 1 January 2020 to 19 November 2026, keeping the first filing per company, returned **504 companies**. Two seeded random draws (seeds `20261120`, `20261121`) gave **102 agreements carrying a blocker**. Of these, **91** had blocker text readable for coding (`coding/docs91.txt` lists them in id order, B01–B91).

## 2. Coding

Each blocker is coded on six dimensions (see [DATA.md](DATA.md)). Two independent first-pass coders split the agreements, blind to earlier labels, and quoted the clause for every answer. Their raw outputs are in `coding/`, unreconciled.

| Check | Result |
|---|---|
| Independent second reader on blocker tiers (29 random) | 27 agree; Cohen's κ = 0.84 |
| Hand check of scope coding (15 random, seed 20261122) | 13 agree; both misses corrected |
| Hand check of materiality coding (14) | 13 agree; 3 corrections in total |
| Independent fact-check of the 14 dropdowns | 12 agree; 1 excluded |

Every correction is recorded in the `note` field of the affected row.

## 3. The attack library

Eleven dropdowns completed without lender consent, 2016–2026, each traced to a primary source and re-checked independently by a second reader who did not see the first's work (`data/events.json`, `data/event_check.csv`). AMC and STG are listed but excluded, because their lenders consented. Revlon BrandCo is excluded because its destination could not be confirmed.

## 4. The stop rule

Each event *e* moved assets *aₑ* ∈ {IP, non-IP} along a route over three destination types:
**U** (unrestricted subsidiary), **R** (non-guarantor restricted subsidiary) and **N** (outside the group). A route is either sequential (`A>B`: blocking any step stops it) or parallel (`A+B`: every destination must be blocked).

Each blocker *b* reaches a set of destinations *D_b* (always containing U) and has asset scope *x_b* = 1 if it names assets beyond IP.

```
covers(b, d, e) = [d ∈ D_b]  and  [aₑ = IP  or  x_b = 1]
stops(b, e)     = any(covers over route)   if sequential
                  all(covers over route)   if parallel
score(b)        = number of the 11 events stopped
```

In code this is about ten lines: `stops()` in `reproduce.py`, and `stops()` in `stack/stack_backtest.py` for the whole agreement.

## 5. The whole agreement

Named blockers often sit in different sections of the same contract. The full text of all 91 agreements was scanned for five families. Every one of the 248 flagged passages was read by hand.

| Family | What it guards against | Usual location | Found |
|---|---|---|---|
| Pluralsight | dropdowns to non-guarantor subsidiaries | investment covenant | nothing beyond coded clauses |
| Outside the group | transfers to affiliates and JVs | dispositions, investments | nothing beyond coded clauses |
| Envision | designating subsidiaries that hold material assets | unrestricted-subsidiary definition | 1 agreement |
| Chewy | guarantor release after a partial equity sale | guarantee release | 21 agreements (8 strong) |
| Omni | any liability management transaction | negative covenants | 1 agreement (Cumulus) |

Each provision found is in `stack/stack_provisions.json`, with the basis for counting it. Chewy calls are in `stack/F4_chewy.csv`.

## 6. Uncertainty

- **Shares:** Wilson 95% intervals.
- **Median and the share stopping at most 3:** 10,000 bootstrap resamples of the 91 agreements, seed `20261123`.

Both are computed by `robustness.py`.
