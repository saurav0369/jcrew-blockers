# Pre-registration: loophole dimensions (written 2026-11-22 before coding)
Descriptive prevalence only; no pass/fail threshold, so no test claim is made from these.
On the same 91 documents (docs91.txt), coded blind to all earlier labels:
 D1 materiality decider: who decides whether IP is "material" — BORROWER (e.g. "as determined by the Borrower in good faith"), AGENT, OBJECTIVE (no decider named), SCHEDULE (listed IP).
 D2 timing: ONGOING (bars transfers / ownership at all times) vs DESIGNATION_ONLY (tested only when a subsidiary is designated).
 D3 exclusive licences: does the blocker cover exclusive licences of the IP? YES/NO.
Crash-test rule (computed 2026-11-22 from existing coding, crash_test.json): a blocker stops an event if it covers every asset class moved
(non-IP covered only when asset_scope = IP_PLUS; generous upper bound) and the destination (U always; R if reaches_R; N if reaches_N).
