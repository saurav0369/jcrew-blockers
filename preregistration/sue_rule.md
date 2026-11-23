# Pre-registered rule: "Soft Unlimited Exit" (SUE)  — frozen 2026-11-21 before any of the cases below is read

## Rule
A credit agreement is SUE-POSITIVE if its investment, restricted-payment, designation or disposition provisions allow value to move from the
Loan Parties to an Unrestricted Subsidiary, a non-subsidiary affiliate/JV/any Person, or a non-guarantor restricted subsidiary
IN AN UNLIMITED AMOUNT under ANY of these conditions:
 (a) no ratio test at all (unconditional);
 (b) a "no worse" test (ratio not lower / not higher than immediately prior to the transaction);
 (c) a total or net total leverage cap >= 6.00x, or a first-lien / secured leverage cap >= 4.50x;
 (d) a fixed-charge or interest coverage floor <= 1.75x;
 (e) a carve-out naming a specific entity or transaction (e.g. a named SpinCo);
 (f) a J.Crew-style pass-through: unlimited investments by non-guarantor restricted subs into U or N, combined with Loan Party -> non-guarantor capacity >= 5% of total assets.
Otherwise SUE-NEGATIVE. A route closed by an applicable blocker (for the asset class at issue, or all assets) does not count.
Unlimited routes gated by tighter tests (e.g. total leverage <= 5.0x) are SUE-NEGATIVE.
Exclusions: carve-outs limited to ordinary course, cash management, securitization or receivables entities.

## Prediction
SUE-POSITIVE agreements are the ones whose borrowers do non-consent dropdown/designation LMEs.
Success: hit rate on events >= 3 of 4 AND false-alarm rate on controls <= 2 of 6.

## Cases (chosen before reading; documents = last credit agreement version on EDGAR before the event, or the census document for controls)
Events (non-consent dropdown/designation, public filers): iHeartMedia (2024), Rackspace (Mar 2024), Xerox (2025-26), Altice USA / CSC Holdings (Nov 2025).
(DISH DBS dropped: its debt is indentures, outside the credit-agreement scope.)
Controls (stressed public borrowers with no dropdown/designation LME in the event list): E2open, Cano Health, Diebold Nixdorf, 2U, Vacasa, Getty Images.
Known weakness: the consent status of each event is to be checked from the event filing AFTER scoring; a consent event is reported separately, not counted.
