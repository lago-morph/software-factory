# Whole-57 cross-batch consistency pass (2026-05-31)

> Final cross-batch drift check over the single canonical track (`spec/` + `plan-faithful/`, C01–C57) after Sweep-1 + the operator decisions D-20..D-25. Sweep-1 integrated per-batch; this is the whole-57 sweep. Run by a real subagent over the corpus, cross-verified by the orchestrator with grep over the committed tree.

## Summary

| Check | Verdict |
|---|---|
| Nomenclature — no "Track A/B" framing in canonical-track bodies (D-6) | **consistent** (0 non-`.review.md` body files) |
| Decision citations resolve (no dangling `D-NN` outside D-1..D-25) | **consistent** (0 dangling) |
| C46 dependency edge (D-24) | **fixed-in-place this pass** → `C33, C21, C25` |
| C50 promotion-cutline cite | **consistent** (no dangling `D-20` cite present) |
| C12/C14/C15 loop-DOT encoding seam (D-16) | **consistent** (frozen by decision; no drift) |
| C42/C34/C32 judge read-surface seam (D-17) | **consistent** (frozen by decision; no drift) |
| C36↔C37 population seam | **consistent** (carrier settled; granularity = joint Sweep-2 freeze) |
| Over-claim vs C57 residual register | **consistent** (F54 = residual per D-21; F12/F28 conditioned on the D-23 prevent-vs-detect spike) |
| **Mechanical edits made by the consistency subagent** | **0** (corpus already consistent) |

## Details

### Nomenclature — "canonical track", not "Track A/B" (D-6)
`grep -rl "Track A\|Track B"` over `spec/` + `plan-faithful/`, excluding `*.review.md`: **0 files.** Spec/plan bodies are clean (the only A/B mentions are legitimate dropped-DELTA provenance citations + one explicit D-6 affirmation). Track-A/B history is preserved in `_meta/` docs and the per-component `*.review.md` adversary headers — intentional, per D-6.

### Decision citations resolve
`grep -rhoE "D-[0-9]+"` over `spec/`, `plan-faithful/`, `_meta/`: every distinct cited id is within the adopted range D-1..D-25. **0 dangling references.** C50's promotion-cutline section carries no stray `D-20` cite.

### C46 dependency edge (D-24) — fixed this pass
[`component-inventory.md`](component-inventory.md) C46 row dependency column now reads **`C33, C21, C25`** (cost via the OTLP metrics path C25→C26 + the CXDB read via C21; C24 = writer/provenance only), matching C46's spec prose and sibling C36. Was `C33, C24`. This is the one mechanical corpus edit in the wrap-up pass; the orchestrator made it (the consistency subagent confirmed C46 + C36 prose already read cost via C25/C26 + C21 with no "C24 raw-bodies" misstatement).

### Frozen seams (no drift introduced this pass)
Three seams were frozen as joint Sweep-2 freezes in the per-batch integration and are unchanged here; all sides verified mutually consistent:
- **Loop-DOT encoding (D-16):** C12 owns the back-edge/loop-marker encoding; C14 renders the marker as a seam element (interim fail-loud → end-state marked-back-edge); C15 consumes it; none invents the encoding.
- **Judge read-surface (D-17):** judge MAY read trajectories + held-out scenarios; worker MUST NOT read the judge rig or the scenarios; C42 provides / C34 enforces+audits / C32 scores; exact partition SHAPE deferred to the joint C42/C34/C32 freeze — no spec over-commits the shape.
- **C36↔C37 population seam:** carrier settled (`anomaly` signal, C36 I3) on both sides; granularity/aggregation is the open joint Sweep-2 residual on both sides.

### No over-claim vs the C57 residual register
F54 objective-drift is never marked "Addressed" — it is a registered residual per D-21. The prevent-vs-detect-contingent modes (F12/F28) keep their "Addressed" claims explicitly conditioned on twins / the D-23 Gas City spike. No spec over-claims coverage the register contradicts.

## For the operator (one flagged, non-blocking item)
- **Corpus-wide stale "Track A/faithful" labels in ~40 `*.review.md` adversary headers** (plus one straggler spec header, C12's `Track: A (faithful)` vs sibling C14's `Track: canonical`). This is **not a D-6 violation** — review/`_meta` history is intentionally preserved — but it is an inconsistent label. It was already routed by the C09 review (RC09-04) as a corpus-wide relabel-or-leave call that must not be done piecemeal. **Left for the operator** as a Sweep-2 editorial choice.
- The three frozen seams above are deliberate Sweep-2 joint-freeze items (they need the real `gc`), not drift — open by design.
- The expert panel raised stronger, forward-looking versions of two findings (same-family-judge credibility; objective-drift as a structural Goodhart risk) — logged as PF-1..PF-3 in the [decision ledger](review-log.md) for Sweep-2 review.
