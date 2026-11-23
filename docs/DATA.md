# Data dictionary

## `data/blockers.json` (also `blockers.csv`): one row per blocker, 91 rows

| Field | Meaning | Values |
|---|---|---|
| `id` | Row id, in the order of `coding/docs91.txt` | `B01`–`B91` |
| `company`, `cik` | Borrower and its SEC Central Index Key | |
| `document`, `url` | The credit-agreement exhibit coded, and its EDGAR link | |
| `covers_nonguarantor_subs` | Clause reaches restricted subsidiaries that are not guarantors (the Revlon and Pluralsight route) | `YES` / `NO` |
| `covers_outside_group` | Clause reaches entities outside the subsidiary group: JVs, sister companies, any non-Loan Party (the Xerox and Trinseo route) | `YES` / `NO` |
| `assets` | Assets protected | `IP only` / `IP and other assets` |
| `materiality_decided_by` | Who decides what counts as "material" | `Borrower` / `Agent` / `Not named` / `Undefined term` |
| `covers_exclusive_licences` | Clause reaches exclusive licences as well as transfers of title | `YES` / `NO` / `UNCLEAR` |
| `timing` | When the clause bites | `Ongoing` / `Designation only` / `Unclear` |
| `sacred_right` | Blocker can be amended only with each affected lender's consent | `Yes` / `No` |
| `subordination_sacred` | Same contract makes lien or payment subordination a sacred right | `Yes` / `No` |
| `filing_year` | Year the exhibit was filed | |
| `clause_quote` | The words the coding rests on | |
| `note` | Corrections and reasons, where a call was changed | |

## `data/events.json` (also `events.csv`): one row per dropdown, 14 rows

| Field | Meaning |
|---|---|
| `event`, `year` | Borrower and year of the transaction |
| `assets_moved` | `IP`, `Non-IP` or `IP and non-IP`; decides whether IP-only blockers can stop it |
| `what_moved`, `destination` | Plain-language description |
| `route` | Destinations in stop-rule notation: `R>U` is sequential, `U+N` is parallel |
| `lender_consent` | Whether lenders consented |
| `in_test` | `Included`, or the reason it is excluded |
| `source` | The opened source the row was built from |

## `stack/`: whole-agreement provisions

| File | Contents |
|---|---|
| `stack_provisions.json` | Every provision found outside the coded clause, with its reach, asset scope and verbatim basis, plus what was read and deliberately not counted |
| `F4_chewy.csv` | Each Chewy provision, graded `strong` or `weak`, with the reason |
| `stack_backtest.py` | The whole-agreement scoring rule |

## Other files

| File | Contents |
|---|---|
| `data/checks.json` | The verification results shown in the paper |
| `data/event_check.csv` | The independent fact-check of each dropdown |
| `data/second_reader_labels.csv` | The blind second reading of blocker tiers |
| `data/wave3_classification.csv`, `data/wave4_classification.csv` | Census classification of every sampled agreement, including those without a blocker |
| `data/lme_event_table.csv` | The wider event table before verification |
| `data/verbatim_checks.md` | Quotes checked against the filings |
| `coding/scope_coding_*.csv`, `coding/loophole_*.csv` | Raw outputs of the two blind coders |
