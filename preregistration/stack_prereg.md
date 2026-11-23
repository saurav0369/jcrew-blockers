# Pre-registration: full-agreement ("stack") backtest
Written 2026-11-23, before any agreement was scanned for the provisions below. SHA-256 recorded in stack_prereg.sha256 before the scan.

## Why
The published backtest scored only each agreement's J.Crew blocker clause. Practitioners layer named blockers in other sections:
Pluralsight (non-guarantor restricted subsidiaries; usually Permitted Investments / Investment covenant), Envision (material assets to
unrestricted subsidiaries; designation / investments), Chewy (guarantee release when a guarantor stops being wholly owned), catch-all
("omni") blockers. This test scores the whole agreement.

## Sample and documents
The same 91 agreements (data/blockers.json, B01-B91), same document per agreement (coding/docs91.txt). Same 11 events, same routes.

## Detection (deterministic scan, then every hit read by hand)
Let K = the agreement's material-asset term(s): "Material Intellectual Property" and any defined term the blocker uses (e.g. "Material Asset(s)", "Material Property").
- F1 Pluralsight-type: K within 600 characters of non-guarantor wording ("not a Loan Party", "Non-Loan Party", "non-Guarantor", "is not a Guarantor", "Excluded Subsidiary"). Counts if, on reading, it bars a Loan Party from transferring K (by sale, investment, dividend or exclusive licence) to, or bars ownership of K by, a restricted subsidiary that is not a guarantor.
- F2 Non-subsidiary reach: K within 600 characters of "Affiliate", "joint venture", or "Person that is not a Loan Party" / "Person other than a Loan Party". Counts if it bars transfer of K to such persons outside the subsidiary group.
- F3 Envision-type: "Unrestricted Subsidiar" within 600 characters of "material assets", "Material Assets", "all or substantially all", "material portion", "material operating". Counts if it bars transferring material assets beyond IP to unrestricted subsidiaries, or designating a subsidiary that owns them. General investment baskets/caps do not count.
- F4 Chewy: guarantee-release text containing "wholly" within 400 characters of "solely". Counts if a guarantor is not released merely because it ceases to be wholly owned (e.g. by a minority equity transfer to an affiliate).
- F5 Omni: "Liability Management", or a covenant barring any transaction that subordinates the Obligations or primes the Liens other than pro rata/with each affected lender's consent, read as a catch-all for any dropdown. Anti-subordination sacred rights alone (already coded as subordination_sacred) do NOT count.
Each counted provision records: destination it reaches (U, R, N) and whether its asset scope goes beyond IP.

## Stack stop rule
A provision p covers destination d for an event if p reaches d and (event moved IP only, or p's scope goes beyond IP).
The original blocker is a provision (reaches U always; R, N per coding; scope per coding).
Event stopped if: (route A>B) some step's destination is covered by some provision; (route A+B) every destination is covered;
or F4 present and event = PetSmart; or F5 present.
Combining provisions this way can credit protection no single clause gives, so stack results are an UPPER BOUND on protection.

## Predictions (fixed now)
P1: median stack score <= 3 of 11.
P2: at least 50% of agreements stack-stop <= 3 of 11.
P3: F4 (Chewy) present in fewer than 50% of agreements.
P4: F5 (omni) present in at most 3 of 91.
P5: F1 adds R coverage (beyond the blocker coding) to fewer than 15% of agreements.
Headline rule: if P1 and P2 hold, the paper keeps "median protection stops few real dropdowns" at the agreement level; if either fails,
the headline is rewritten to the agreement-level result, whatever it is.

## Not claimed
Reading as written, not enforceability. Later amendments not read. Other debt documents not read.
