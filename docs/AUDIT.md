# Audit and corrections

First-pass coding used AI tools, and every call behind the numbers was checked by hand. It has **not yet been reviewed by a lawyer**. This page explains how to check it and how corrections are handled.

## Check a single call in about a minute

1. Find the row in `data/blockers.csv` by company or id.
2. Open its `url`. That is the exact exhibit coded, on SEC EDGAR.
3. Search the document for the words in `clause_quote`.
4. Compare the clause with the row's coded fields. [DATA.md](DATA.md) defines each one.

## The practitioner audit

[`audit/lawyer_audit_20.csv`](../audit/lawyer_audit_20.csv) holds 20 agreements drawn at random, stratified by coded scope (seed `20261123`). For each one it gives the filing link and the four calls the headline depends on, with blank columns for a reviewer's verdict and note.

The results will be published in this repository **whatever they show**, together with the reviewer agreement rate and every disagreement. If you practise in leveraged finance or restructuring and are willing to review some or all of the 20, please write to sauravsharma0369@gmail.com. Reviewers will be credited by name unless they prefer otherwise.

## Corrections

To dispute a call, [open an issue](../../../issues/new?template=challenge-a-call.yml) with the row id and the clause text you rely on.

- **If the call is wrong,** the row is corrected and the change is noted in its `note` field. The numbers are then re-run, and the before-and-after figures are recorded in [CHANGELOG.md](../CHANGELOG.md).
- **If a correction moves a published number,** the README and the paper are updated in the same commit.
