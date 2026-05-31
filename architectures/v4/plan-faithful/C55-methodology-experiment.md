# C55 — Methodology-as-Config Experiment Loop  (Build Plan, canonical track)

> Source / Spec ref: spec/C55-methodology-experiment.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the experiment+selection seam contract (M1)** — the inputs (the **candidate registry**: candidate name → C12 **formula-file** reference, I1; the **work-type key**, I2), the per-cell run contract (candidate × work_type → **C33 satisfaction distribution** + sample count, I3), the **C48 significance-consultation** seam (I4), and the **output** (`work_type → methodology` mapping + evidence + sample counts, I5). This is the interface the dispatch tier + C48 build against. | S | C12 formula reference, C30 scenario set, C33 distribution shape, C48 verdict shape (forward) |
| T2 | **Pack/tool-node skeleton** — package C55's loop as small Gas City tool node(s) per C02/C17 ABI; config surface (candidate registry, work-type set, selection policy) per C03 section-presence gate (README:128 "methodology lives in the file"; AI-CONTEXT:482 "After Phase 2"). | S | C02/C17 ABI, C03 gate, T1 |
| T3 | **Candidate registry as swappable formulas (I1/INV-1, D-7/D-8)** — register v3 candidate methodologies **as named C12 formula files** (GF-M first, README:553); swapping/adding a candidate is a **formula-file change**, not C55 code. No formula format invented (C12 owns it). | S | T2, C12 formula + swap |
| T4 | **Work-type key (I2, addresses G05)** — define the `work_type` dimension selection is computed per ("which kind of work", README:33); name the key + its role; leave the canonical taxonomy to sweep-2 (OQ-2). | S | T1 |
| T5 | **Experiment-run orchestration (I3/INV-2)** — for each (candidate formula × work_type), drive the **eval tier** (C30 held-out scenarios → C31 runner → C32 judge → C33 satisfaction) to produce a **C33 distribution + sample count per cell**, **same scenarios + same judge** for all candidates of a work type (README:31). C55 orchestrates; runs/judges/aggregates nothing itself. | M | T3, T4, C30/C31/C32/C33 contracts |
| T6 | **Per-work-type selection rule (I4/INV-3, D-15)** — rank candidates for a work type by **holistic C33 satisfaction**; select the best; record the choice. "GF-M first" is ordering, not a pre-decided winner (INV-3). | M | T5 |
| T7 | **C48 significance consultation (I4/INV-4 — C55's significance→C48 scope boundary)** — **consult C48** for "is the leading candidate actually better"; build **no** significance machinery. Until C48 exists (Batch 5), surface raw per-cell distributions + sample counts and **withhold** the significance claim (never fabricate one). | S | T6, C48 (forward; not a blocker) |
| T8 | **Selection output (I5)** — emit the `work_type → methodology` mapping + supporting evidence + sample counts (INV-5) as the tool-node declared output; shape it for the dispatch tier (which formula to run for which kind of work). | S | T6, T7 |
| T9 | **Fairness + thin-evidence honesty (INV-2/INV-5)** — exclude failed-to-evaluate candidates from a cell (with reason); flag selections on thin/uneven evidence as provisional; re-run affected candidates if the C30 corpus changed between runs (the "same scenarios" guarantee). | S | T5, T6 |
| T10 | **Methodology-experiment pack (AC-1…AC-9)** — harness registering ≥2 candidate **formula files** (a GF-M stand-in + one other) over ≥2 work types, against synthetic held-out C30 scenarios + synthetic C33 outputs (clear-winner, tie, failed candidate, thin-evidence cell), driving all acceptance tests — especially candidate-as-swapped-formula, same-scenarios/same-judge, empirical-per-work-type with **GF-M-first ≠ GF-M-wins**, **significance-consulted-from-C48/withheld-until-C48**, and **no-custom-engine**. | L | T3–T9, synthetic eval-tier fixtures |

## 2. Dependency graph

**Must precede C55:**
- **C12** (the formula a candidate methodology **is**, and the swap mechanism — D-7/D-8; C12 §1 names C55 as the swapper).
- **C30** (the held-out scenario corpus every candidate is measured against — README:31) + **C31/C32** (runner + judge that execute and score a candidate, reached via the eval tier).
- **C33** (the satisfaction distribution C55 selects on — D-15; C33 §1 names C55 as a consumer).
- **C02/C17** (pack + tool-node ABI to package/invoke) + **C03** (feature-flag gate).

**Consulted (forward reference, NOT a blocker):**
- **C48** (A/B statistical significance — "was the variant actually better"; **Batch 5, unbuilt**). C55 (Batch 4) **names the seam** and runs with significance withheld until C48 lands (C55's scope boundary, grounded in C48's inventory mandate + the C33 precedent; recorded as review-log decision **D-19**). C55 must not block on C48.

**C55 must precede (the choice is consumed downstream):**
- the **factory dispatch tier** (C05 sling, via the chosen C12 formula name) — which formula to dispatch for which kind of work.

**Critical path inside C55:** T1 → T3 → T5 → T6 → T8 → T10. The load-bearing tasks are **T5 (experiment
orchestration)** and **T6 (per-work-type selection)** — but both are *thin*: T5 drives the **existing** eval
tier (no new runner/scorer/metric) and T6 selects on **C33's** satisfaction with **C48's** significance (no new
stats). The **G05 resolution** lives in T4 (work-type key) + T6/T7 (empirical selection, GF-M-first ≠
GF-M-wins, significance routed to C48) — all deliberately scoped to *avoid* new capability (no engine, no stats,
no absolute threshold). C55 owns **no source-of-truth** (re-derivable, INV-6).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton)** land, two thin workstreams fan out concurrently:
- **WS-A (catalog/inputs):** T3 (candidate registry as formulas) → T4 (work-type key). The input spine; can
  build against C12 formula *references* (stub formulas) + a synthetic work-type set before the real candidate
  formulas are authored.
- **WS-B (experiment/select/emit):** T5 (run orchestration) → T6 (selection rule) → T7 (C48 consultation) → T8
  (output) → T9 (fairness/honesty). The selection spine; can build against **synthetic C33 distributions** +
  synthetic C48 verdicts before WS-A's real candidates + the live eval tier land.
- **T10** (experiment pack) joins both. WS-A and WS-B meet at the T3/T4 → T5 handoff (candidates × work-types
  feeding the run orchestration).

The decisive parallelism win: because C55 owns no engine, **the entire loop can be built against synthetic
eval-tier outputs** (synthetic C33 distributions, synthetic C48 verdicts, stub C12 formula refs) while C30/C31/
C32/C33/C48 firm up — C55's real risk is the *selection contract*, not the eval tier it consumes.

## 4. Interfaces-first / contract milestones

- **M1 — experiment+selection seam freeze (T1):** the contracts dependents/sub-streams build against:
  (a) **inputs** = candidate registry (name → C12 formula ref, I1) + work-type key (I2);
  (b) **per-cell run** = (candidate × work_type) → C33 distribution + sample count (I3), via C30/C31/C32/C33;
  (c) **significance seam** = the C55→C48 consultation (I4, forward);
  (d) **output** = `work_type → methodology` mapping + evidence + sample counts (I5).
  Freezing M1 lets WS-A build against stub formulas, WS-B against synthetic C33/C48 outputs, and the **dispatch
  tier** stub against the selection output.
- **M2 — methodology-as-data confirmed (T3/D-7/D-8):** every candidate is a **swappable C12 formula file**;
  adding/changing a candidate is a formula-file change, not C55 code (README:50) — frozen before any candidate
  is registered.
- **M3 — empirical selection + significance routing fixed (T6/T7, G05):** selection is **empirical C33
  satisfaction per work type** (D-15), **GF-M-first ≠ GF-M-wins** (INV-3), and **significance is C48's**
  (consulted, not computed — C55's significance→C48 scope boundary, §6) — frozen before the dispatch tier reasons over the selection.

## 5. Risks & de-risking order

1. **Confirm first — G05 selection criterion + GF-M reading (T4/T6/OQ-1).** Surface to the integrator that C55
   pins selection as **empirical satisfaction per work type** (reading (b)), treating GF-M's
   "cheapest/smallest-scope" (README:512/553) as **standing-up order only**, *not* a soft pre-commitment — and
   that the **absolute "good enough" cutline** is a **C50/operator decision-site** concern, not C55's (C55
   selects *relatively* best per work type). This retires the central G05 ambiguity and fixes C55's scope; a
   wrong call would re-introduce the v3 "pick a methodology" framing v4 calls the *wrong question*
   (AI-CONTEXT:501).
2. **Confirm — significance routing to C48 (T7/OQ-4, C55's binding scope boundary — recorded as review-log D-19).** Verify "was the variant actually
   better" lives at **C48** (Batch 5) and C55 builds **no** significance machinery; confirm C55's interim
   behavior (raw distributions + **withheld** significance until C48 exists) is acceptable. A wrong call here
   would have C55 grow a stats engine the bar forbids (and C48 already owns).
3. **Quantify — experiment fan-out cost vs single-seat throughput (T5/OQ-3, G32/G34).** Ten candidates ×
   work-types × the held-out suite through the judge is a **multiplicative** cost on one Max seat, and v4's
   "cost amortizes" claim (README:512) carries **no number**. Confirm with **C46** before running the full grid,
   and confirm C55's **incremental/evidence-accumulating** posture (INV-6, run a candidate when ready) is the
   intended cost control — with the **cost model owned by C46/G32**, not C55. *[This is C55's one real
   over-budget risk — flagged, not engineered around.]*
4. **Confirm — work-type taxonomy source (T4/OQ-2).** v4 names the *dimension* ("kind of work", README:33) but
   not its **values** (only F-MODE F20's greenfield/brownfield axis is named). Confirm the canonical `work_type`
   set + its source (C30 scenario families? a separate axis?) before the per-work-type selection record is
   schematised at sweep-2.
5. **Pin — eval-tier versions for cross-candidate fairness (T5).** Confirm Inspect AI (via C30/C33) is
   version-pinned so candidates are compared on a **stable** scenario/judge/metric contract (INV-2) — an
   unpinned reducer would make cross-candidate comparisons irreproducible.

## 6. Definition of done

**Per-component DoD:** the methodology-experiment pack (T10) passes **AC-1…AC-9** against synthetic candidates +
eval-tier outputs — **methodology-as-data** (each candidate a swappable C12 formula; INV-1/D-7/D-8),
**same-scenarios/same-judge** comparison (INV-2), a **C33 satisfaction distribution per (candidate, work-type)
cell** with **no C55 model call / metric** (I3), **empirical per-work-type selection** with **GF-M-first ≠
GF-M-wins** (INV-3, addresses G05), **significance consulted from C48 / withheld until C48** with **no custom
stats** (INV-4, C55's significance→C48 scope boundary), **sample counts surfaced** (INV-5), **re-derivable** with **no
source-of-truth** (INV-6), and a `work_type → methodology` output consumable by the dispatch tier (I5). C55 is a
small Gas City pack loop containing **no runner, scorer, metric, or significance engine**.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C12 (formula ref), C30/C33 (eval-tier), C48 (significance seam, forward), and the dispatch-tier consumer; sub-streams + downstream can stub against them.
- T3: candidates registered as **swappable C12 formula files** (GF-M first); swapping a candidate is a formula-file change, not code (AC-1/M2).
- T4: `work_type` key named + its selection role fixed; taxonomy deferred to sweep-2 (OQ-2).
- T5: a synthetic (candidate × work_type) cell yields a C33 distribution + sample count via the eval tier; **same scenarios + same judge** enforced across candidates (AC-2/AC-3).
- T6: per-work-type selection on **holistic C33 satisfaction** (D-15); GF-M-first ≠ GF-M-wins (AC-4).
- T7: significance **consulted from C48** / **withheld until C48**; **no** p-value computed (AC-5, C55's significance→C48 scope boundary).
- T8: emitted `work_type → methodology` mapping consumable by the dispatch tier (AC-9).
- T9: failed candidate excluded-with-reason; thin/uneven evidence flagged provisional; corpus-change re-run (AC-2/AC-6 fairness).
- T10: full AC suite green; **must pass before the dispatch tier acts on the selection**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (**G05** — empirical
per-work-type criterion confirmed; GF-M-first ≠ GF-M-chosen; absolute cutline at C50/operator, not C55), OQ-2
(canonical work-type taxonomy + its source), OQ-3 (experiment fan-out cost vs single-seat throughput, quantify
with C46; cost model owned by C46/G32), OQ-4 (the **C55→C48** significance-consultation contract, frozen at
sweep-2 when C48 is authored; interim withheld-significance behavior).
