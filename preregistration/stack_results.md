# Results: full-agreement ("stack") backtest
Appended 2026-11-23 after the scan. The pre-registration it answers is `stack_prereg.md`, whose SHA-256 (f23654f1…) was recorded before the scan and is checked by `reproduce.py`.
Scan windows read by hand: F1 43, F2 40, F3 85, F4 24, F5 56 (248 total). What they added beyond the coded blocker clauses:
- F1 (Pluralsight-type): no agreement gained non-guarantor reach; every hit was the already-coded blocker. B29 gained non-IP coverage for
  non-guarantor subsidiaries (a $5M cap on transfers to non-Loan Parties, not usable for liability management).
- F2 (outside the group): nothing new; hits were already-coded blockers or arm's-length affiliate-transaction tests.
- F3 (Envision-type): B45 only (no subsidiary owning all or substantially all assets may be designated unrestricted). The other 84 windows were
  pro forma, basket and definition boilerplate.
- F4 (Chewy): 21 of 91 agreements (23%). 8 strong (an affiliate transfer cannot get the release through a purpose test or capacity),
  13 weak. See stack/F4_chewy.csv and the log entry made before scoring.
- F5 (omni): 1 of 91 (B25, Cumulus, a post-LME exchange). B18's LMT covenant reaches uptiers only.

Stack results (stack/stack_backtest.py):
- Median agreement stops 2 of 11 real dropdowns (3 of 11 if weak Chewy provisions count).
- 58 of 91 agreements stop at most 3; 52 stop only J.Crew and Travelport; 4 stop all 11.
- Per event: PetSmart 3 -> 11 (24 with weak Chewy); Del Monte 12 -> 14; Xerox 12 -> 13; Trinseo 3 -> 4; others unchanged.

Predictions: P1 (median <= 3) HELD (2). P2 (>= 50% stop <= 3) HELD (64%). P3 (Chewy < 50%) HELD (23%). P4 (omni <= 3) HELD (1).
P5 (F1 adds R to < 15%) HELD (0%). Headline rule: the agreement-level headline stands.

Limits: keyword scans miss provisions worded without the searched terms, so stack protection may be understated; combining provisions across
clauses may overstate it. Reading is as written, not enforceability; later amendments not read.
