# Adversarial review — C11 Intent intake (9-field crucible) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Spec Intake
Target: spec/C11-intent-intake.md (+ plan-faithful/C11-intent-intake.md)
Charter: canonical track → attack FIDELITY and COMPLETENESS only, not the design; PLUS the
capability-for-principle bar (flag additions that harden the existing stack rather than realize a 12-principle).

## Summary of attack

v4 is near-silent on C11: the only hard anchor is **F-MODE-COVERAGE F41 (line 91)** — *"Under-defined-intent
debt — Intent Crucible pack (gene transfusion from GF-C) — 9-field structured intake — Addressed"* — plus the
inventory atoms **A97** ("Intent Crucible 9-field intake … gene transfusion from GF-C") and **A149** (F41). I
verified: GF-C is **never defined** (the only other mention, F-MODE:19/F9, is an unrelated signed-scenarios
pattern — confirmed); **no source names any of the 9 fields** (confirmed across F-MODE, inventory-A, one-shot
Parts 1–2); C12 genuinely owns workflow/DAG/methodology (so the "NOT a workflow engine" boundary is faithful);
C08/C09/C10 cross-references all quote correctly; every one-shot Part 2 citation (2406.00215 line 92, 2510.26130
line 94, the four attributes line 8/86–122) and Part 1 citation (Kilroy `DoD.md` line 29, StrongDM line 14,
Fabro "embeds a target-system goal" line 68) is accurate. The FAITHFUL-FILL discipline on the field set is
**unusually strong** — names *and* the 9-way partition are flagged inferred, count-9 is the sole fact, and the
spec even concedes "the arithmetic does not fall out cleanly." THE BAR is correctly applied (validation gate →
C53, no second store, no workflow engine, no field-DSL — all four refusals present and grounded). G23 is
addressed from the C11 side (DoD becomes a required field) with the gate itself deferred to C53, with reason.

The findings below are narrow: one real over-attribution of provenance metadata (major), and three minor
qualify-the-inference / tighten-the-citation items.

## Findings

### RC11-01 — major — `transfused_from` is **component-level** provenance (A93) but the spec attaches it to **every intent record** (INV-4 / AC-3 / §3.1 / §4)
**Claim.** INV-4 ("Each record carries `transfused_from` (GF-C lineage)"), AC-3 ("Each intent record is a git
commit carrying … `transfused_from` lineage (C51)"), §3.1 Provenance interface ("The record carries
`transfused_from` lineage (GF-C)"), and §4 Identity all treat `transfused_from: GF-C` as **per-record** state.
**Evidence.** Atom **A93** (`component-inventory-A.md:262`) defines `transfused_from` as *"Records external
exemplar URL **per factory-built component**"* — "P9 applied to the **factory's own work**." GF-C is the
exemplar that **C11-the-component / the crucible pack** was transfused from; it is a property of *the schema*,
not of an operator's individual intent record. An intent record is operator-authored content describing a unit
of *their* intended work — it has no GF-C lineage. The spec actually **states this exact distinction itself** in
field #9 ("distinct from C51's `transfused_from`, which records the provenance of the **C11 component itself**,
INV-4; field #9 is per-record content, not the universal provenance metadata") — and then contradicts it by
putting `transfused_from` on every record in INV-4/AC-3/§3.1/§4. So this is an internal inconsistency *plus* an
over-attribution of A93 beyond what the atom supports. **Fix (applied).** Moved `transfused_from: GF-C` to where
A93 puts it — the **pack/schema** (component-level provenance, carried once for C11 the crucible) — and left
**only** `created_by` (C41) as the genuine per-record provenance field. INV-4, AC-3, §3.1, §4-Identity, §7, and
the plan's T6/M3/AC-3 wording were updated to match (record carries `created_by`; the pack carries
`transfused_from`). Field #9's "distinct from `transfused_from`" note now reads cleanly.

### RC11-02 — minor — field #9's grounding cites A93/A107, the very lineage it is defined to be *distinct from*
**Claim.** §3.3 field #9 (Exemplar / transfusion reference) lists grounding "A93/A107 external-grounding lineage
via inventory map." **Evidence.** A93 is `transfused_from` (component provenance) and A107 is "External grounding
discipline — *foundations stay upstream OSS; factory builds only orchestration glue*" — both are about the
**factory's own components**, not about a per-record intent-level "behave like this exemplar" pointer. The field
is explicitly *distinct from* A93 (per RC11-01), so citing A93 as its *grounding* is self-undercutting. The
honest grounding for field #9 is **one-shot Part 1** (the corpus literally *is* exemplar specs an agent is
pointed at to "behave like") — which the spec already cites first. **Fix (applied).** Dropped the A93 citation
from field #9 grounding (it is the contrast, not the support); kept one-shot Part 1 and softened "A93/A107
lineage" to "the external-grounding *spirit* (A107) — distinct from A93 component provenance, see #9 note."

### RC11-03 — minor — field #7 (DoD) has a *firmer* anchor than the spec claims, and the FAITHFUL-FILL should say so
**Claim.** The §3.3 FAITHFUL-FILL banner treats all nine slots as equally inferred from "≈4 attributes + ≈2
Part-1 practices." **Evidence.** This slightly *under-sells* fidelity for two slots: **A94** "Definition-of-Done
(DoD) — *Acceptance-criteria checkbox set driving build loops*" is a first-class inventory atom (not merely the
Kilroy `DoD.md` file), and field #6/#8 map onto the named **requirement-classes** and **ambiguity** attributes
almost 1:1. So field #7 (DoD) in particular is anchored by an *atom*, not just a corpus file — relevant because
field #7 is the load-bearing one for G23. A faithful review should record that the fill is *graded* (some slots
better-anchored than others), not uniformly weak. This is a fidelity-strengthening note, not an error. **Fix
(applied).** Added one clause to the §3.3 FAITHFUL-FILL noting field #7 is additionally grounded in atom **A94**
(DoD) and #6/#8 track the requirement-class/ambiguity attributes closely, so the fill is *graded*; the slots
most at risk of GF-C divergence are the *boundary/partition* ones (Scope vs Non-goals vs Inputs split), which
remains the OQ-1 thing to confirm.

### RC11-04 — minor — C51/C53 forward-references are to **unwritten** sibling specs; ownership claims are asserted, not yet verifiable
**Claim.** §1, §2, §3.2, §7, §9 lean on **C51** ("owns the `transfused_from` provenance field, the
exemplar-correctness predicate, and license handling") and **C53** ("owns the go/no-go gate"). **Evidence.**
Neither `spec/C51-*.md` nor `spec/C53-*.md` exists yet (both are later-batch; confirmed by directory listing) —
so these ownership statements are forward-references the C11 author cannot currently check against a sibling
doc. This is acceptable and even correct for sweep-1 (the inventory *does* name C51 = gene-transfusion and C53 =
bootstrap-validation, so the routing is grounded at the atom/inventory level), but the C51 *license + predicate*
ownership should be flagged as **asserted-pending-C51** exactly as the C23 review qualified adopted upstream
properties, rather than stated as settled fact. **Fix (applied).** Added "(asserted; C51/C53 specs are
later-batch — to confirm against those specs at integration)" to the §2 C51 row and the §9/G23 C53 disposition.
No routing changed — only the certainty is now labelled.

### RC11-05 — minor (no change) — confirm the canonical spec does NOT drift toward the optimized C08 "C11 emits a C08 bundle" design
**Claim.** The canonical C11 keeps the crucible record *distinct but co-versioned* from C08 (OQ-2). **Evidence.**
The parallel `spec-optimized/C08-spec-artifact.md` carries **DELTA-05**: "C11 … *produces* a C08 bundle … its
DoD/constraints become the spec's required sections." That is a **Track-B/optimized design choice** and must NOT
leak into the canonical C11. I checked: the canonical C11 spec does **not** adopt it (it keeps the C11→C08 seam
as an *anchor*, not a bundle-emit, and flags the artifact-count question as OQ-2 contingent on C08:OQ-1).
**Disposition:** correct as written; flagged here only so the integrator does not later import the optimized
"emit-a-bundle" framing into the canonical track under the impression C11 already assumes it. **No fix.**

## Verdict
**accept-with-fixes.** Strongly faithful, meticulously sourced, and exemplary in its FAITHFUL-FILL honesty (count-9
as the sole fact; names + partition flagged inferred; GF-C-undefined called out; over-build line cleanly held to
P1). The one substantive fidelity defect is RC11-01 — `transfused_from` is A93 *component-level* provenance and
was wrongly attached to every per-record state, contradicting the spec's own field-#9 note; fixed by moving it to
the pack/schema and leaving `created_by` as the record-level field. The remaining four are minor citation/qualifier
tightenings, all applied in place. Nothing architecturally significant is deferred; no blockers. The load-bearing
ambiguity (OQ-1, the real GF-C field set) is correctly the dominant sweep-2/de-risk item and is already routed to
the review-log.
