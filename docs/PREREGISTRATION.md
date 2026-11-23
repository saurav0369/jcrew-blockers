# Pre-registration ledger

Every rule and prediction in this project was written down before the result it governs was seen. This page lists each one, what it fixed, what happened, and how far its timing can be verified from this repository alone.

**How to read the "Fingerprint" column.** Where a SHA-256 was recorded at the time of writing, `reproduce.py` recomputes it from the file today and fails if they differ. A ✓ therefore means the file you are reading is byte-for-byte the one that existed before the result. "Dated" means the file carries its date and was written before the result, but no fingerprint was retained, so its timing rests on the project record rather than on a check you can run.

| File | Fixed before | What it fixed | Fingerprint | Outcome |
|---|---|---|---|---|
| [`last_war_prereg.md`](../preregistration/last_war_prereg.md) | any scope coding or event result | H1: fewer than half of real dropdowns use the IP-to-unrestricted move. H2: fewer than 15% of blockers reach outside the group. H3: fewer than 20% protect non-IP assets. A hand check of 15 codings, with a redo below 13 agreeing. | `7b9d6a32` ✓ | All three held on point estimates; the H2 and H3 intervals reach about 20% and 22%. Hand check 13 of 15. [Results](../preregistration/last_war_results.md) |
| [`stack_prereg.md`](../preregistration/stack_prereg.md) | the scan of all 91 agreements | Detection patterns for Pluralsight, Envision, Chewy and omni provisions; the whole-agreement stop rule; five predictions; the rule that the headline is rewritten if two of them fail. | `f23654f1` ✓ | All five held. One clarification was logged before any score was computed ([log](../preregistration/stack_prereg_log.md)). [Results](../preregistration/stack_results.md) |
| [`retrodiction_protocol.md`](../preregistration/retrodiction_protocol.md) | any case was modelled | Three blind cases: read the pre-event agreement, predict the route, then open the event filing. Pass bar: 2 of 3. | `34d69be3` ✓ | Passed formally, 2 of 3. Only Trinseo was informative. [Predictions and outcomes](../preregistration/retrodiction_predictions.md) |
| [`sue_rule.md`](../preregistration/sue_rule.md) | any case was scored | "Soft unlimited exit": flag at least 3 of 4 new events and at most 2 of 6 controls. | `2d23d89f` ✓ | **Failed:** 2 of 4 events. Decisions made while scoring are kept separately in the [interpretation log](../preregistration/sue_rule_interpretation_log.md). [Scores](../preregistration/sue_scores.md) |
| [`sacred_prereg.md`](../preregistration/sacred_prereg.md) | the sacred-rights coding | Fewer than 25% of blockers are entrenched as sacred rights. | dated | Held: 4 of 91 (4%). |
| [`loophole_prereg.md`](../preregistration/loophole_prereg.md) | the loophole coding | Definitions for who decides materiality, timing and exclusive licences. | dated | Coded as defined; see `coding/loophole_*.csv`. |

## Decided after the data, stated as such

- **The clause-level stop rule** (Section 4.1 of the paper) was written after the scope coding came in. The thresholds it rests on (H1–H3 above) were fixed before. The paper says so wherever the headline appears.
- **The anti-subordination count** (53 of 91) is an observation, not a test, and was never pre-registered.
- **The robustness variants** in `robustness.py` were chosen after the main results, to probe them. None changes the median by more than one.

## Why two files were split

`stack_prereg.md` and `sue_rule.md` each had text appended after they were frozen: the stack results, and the SUE interpretation log. The appended text now lives in its own file, so the frozen file matches its recorded fingerprint exactly. Nothing in the frozen text was changed.
