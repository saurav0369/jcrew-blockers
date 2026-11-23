# Pre-registration: "Blockers guard the 2016 door" (written 2026-11-22, before any coding or event result is seen)

Question: do J.Crew blockers protect against the moves stressed borrowers actually make?

Data: (1) scope coding of the 102 blocker-bearing census agreements (scope_coding_A.csv, scope_coding_B.csv), two independent Haiku coders
on disjoint halves, blind to earlier tiers; (2) public dropdown/designation event table (lme_event_table.csv) built by a third agent from opened sources.

Predictions (each states its threshold now):
 H1. Among verified dropdown/designation events, fewer than 50% moved IP only to an unrestricted subsidiary (the one move a typical blocker stops).
 H2. Fewer than 15% of census blockers reach entities outside the subsidiary group (JVs, sister companies, "any Person other than a Loan Party").
 H3. Fewer than 20% of census blockers protect assets beyond IP.
Headline is claimed only if H1 AND (H2 OR H3) hold, with 95% Wilson intervals reported.
Checks before any claim: I hand-verify a random 15 scope codings against the clause, and every event row whose source I can open;
rows marked UNVERIFIED are excluded. If coder/hand agreement on the 15 is below 13, the scope coding is redone before use.
