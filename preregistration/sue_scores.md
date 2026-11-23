# SUE scoring (rule: sue_rule.md, hash 2d23d89f...). Access: read-directly (clause text pulled from EDGAR exhibits).

## Events
| Case | Document | Unlimited routes found | SUE |
|---|---|---|---|
| iHeartMedia | Credit Agreement (May 2019) as amended by Amd No. 4 (Jun 2023), acc 0001400891-23-000038 | 7.02(x) and 7.06(d) unlimited only if Total Net Leverage <= 4.75x; 7.02(c) LP->non-LP capped at greater of $250M/25% EBITDA or "ordinary course or consistent with past practice" | NEGATIVE |
| Rackspace | First Lien Credit Agreement as amended by Amd No. 5 (Feb 2021), acc 0001193125-21-034506 | 6.04(b)(i): "Investments by the Borrower or any Subsidiary in the Equity Interests of the Borrower or any Subsidiary" — no cap on Loan Party -> non-guarantor Subsidiary | POSITIVE (a) |
| Xerox | First Lien Term Loan Credit Agreement (Nov 2023), acc 0001193125-23-280007 | 6.04(33) unlimited only if Total Leverage <= 3.50x; non-LP RS under Shared Investment Cap; UnSubs capped; 6.05(2) FMV sales need >= 75% cash | NEGATIVE |
| Altice USA / CSC Holdings | Credit Agreement as amended by 13th Amd (Dec 2022), acc 0001628280-22-032367 | Permitted Investment (a): "Investments in (i) a Restricted Subsidiary ... or the Borrower" — no cap on non-guarantor RS | POSITIVE (a) |
Event hit rate: 2 of 4. Pre-registered success needed >= 3 of 4 -> RULE FAILS on events regardless of controls.
Caveats: Rackspace document is Feb 2021 (later amendments before Mar 2024 not searched); Xerox and Altice event documents not checked for later amendments; consent status of events not yet checked.

## Controls
| Case | Document | Unlimited routes found | SUE |
|---|---|---|---|
| E2open | Credit Agreement as amended by Amd No. 4 (Jun 2023), acc 0000950170-23-029142 | 6.04(c) non-LP RS capped at greater of $90M/75% EBITDA (ordinary-course carve-out excluded by rule); 6.04(t) unlimited only if Total Leverage <= 4.05x | NEGATIVE |
| Diebold Nixdorf | Exit Credit Agreement (Aug 2023), acc 0001193125-23-210786 | (ii) LP -> External Subsidiary limited to cash received from them; (xv) "Designated Joint Venture Transaction" needs Required Lender approval; ratio routes none found | NEGATIVE |
| 2U | Credit and Guaranty Agreement as amended (Jan 2023), acc 0001193125-23-004247 | 6.6(e)(iii) non-guarantor RS capped ($20M amended); 6.6(bb) unlimited only if Total Net Leverage <= 5.00x | NEGATIVE |
| Vacasa | Credit Agreement as amended by Amd No. 3 (Oct 2024), acc 0001874944-24-000076 | LP -> non-LP Investments may not be increased; RP (xiv) unlimited if Liquidity >= $350M or Total Leverage <= 4.00x (liquidity tests are not in the rule) | NEGATIVE |
| Getty Images | Credit Agreement as amended by 4th Amd (Dec 2025), acc 0001628280-26-018160 | 7.02(c)(iii) back-to-back only; (c)(iv) tax/reorg Investments if Collateral "not materially impaired" (qualitative condition, not counted); RP ratio 2.75x | NEGATIVE |
| Cano Health | DROPPED: the EDGAR document found was a debtor-in-possession agreement (Feb 2024), not a pre-stress credit agreement. Logged as a deviation. | — | — |

## Result
Events SUE-positive: 2 of 4 (Rackspace, Altice). Controls SUE-positive: 0 of 5.
Pre-registered success required >= 3 of 4 events AND <= 2 of 6 controls: FAILED on the event side.
Descriptive only: positives were 2/2 events and 0 false alarms; with 9 cases, a one-sided Fisher exact test on 2/4 vs 0/5 gives p = 6/36 ≈ 0.17 (not significant).
Observed pattern among the two positives: both were UNCAPPED Loan Party -> non-guarantor restricted subsidiary investment baskets (clause (a)), not ratio routes.
