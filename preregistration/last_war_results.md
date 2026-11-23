# Results for last_war_prereg.md (hash 7b9d6a32...), 2026-11-22

## Hand check of 15 scope codings (seed 20261122), against clauses read earlier in this project
13 of 15 agree (threshold 13: met). Disagreements, both coder UNDER-calls:
- Embecta: coder R=NO; earlier read: Loan Party -> non-Loan-Party Subsidiary also barred (R=YES).
- AlTi Global: coder R=NO, N=NO; earlier read (read-directly): bars transfers "to any Unrestricted Subsidiary or any other Person that is a controlled Affiliate" unless a wholly owned Credit Party (R=YES, N=YES for controlled affiliates).
Direction: coding under-counts R and N slightly. Also: the coders used the earliest EX-10 hit, which differs from the census document for some firms (e.g. Alkermes coded NONE, earlier read CLOSED via Section 6.12).

## Census scope (91 readable agreements with a coded blocker; 11 NONE/UNREADABLE excluded)
| Measure | Count | Share | 95% Wilson |
| reaches non-guarantor restricted subs (R) | 26 | 28.6% | 20.3-38.6% |
| reaches entities outside the group (N) | 11 | 12.1% | 6.9-20.4% |
| protects assets beyond IP | 12 | 13.2% | 7.7-21.6% |
| reaches N AND protects non-IP assets | 2 | 2.2% | - |
With the two hand-check corrections, N = 12 (13.2%) and R = 28 (30.8%).

## Events (strict verified set: rows with asset and destination verified and completion stated; 14 events)
J.Crew 2016, Neiman 2018, PetSmart 2018, Revlon 2019, Revlon 2020, Travelport 2020, Bausch 2022, Envision 2023, Pluralsight 2024, Del Monte 2024, AMC 2024, STG 2024, Trinseo 2023, Xerox 2026.
IP-only moved to an unrestricted subsidiary: J.Crew, Travelport = 2 of 14 (14%).
Upper bound counting any deal whose moved assets included IP going to U (adds AMC, and Del Monte/STG/Envision if their assets included IP): 6 of 14 (43%).
Excluded as unverified: Party City, iHeart, Trinseo 2024, Optimum.

## Verdict against pre-registered thresholds
H1 (<50% of events were IP-to-U only): HOLDS (14%; 43% even at the upper bound).
H2 (<15% of blockers reach N): HOLDS on the point estimate (12.1%; 13.2% corrected), but the interval reaches 20%.
H3 (<20% protect non-IP assets): HOLDS on the point estimate (13.2%), interval to 21.6%.
Headline condition (H1 AND (H2 OR H3)): MET on point estimates.
Limits: event list is not random (built from public reporting, 14 verified rows); coding by AI agents with 13/15 hand agreement; document choice differs from the census for some firms; destinations for Revlon BrandCo entities rest on a court opinion at the pleading stage.
