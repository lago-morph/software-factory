# Adversarial review — C07 Vocabulary & Glossary (Tracks A + B, sweep 1)

Reviewer persona: Subsystem Adversary (Runtime Substrate)
Targets: spec-faithful/C07-vocabulary-glossary.md, plan-faithful/C07-vocabulary-glossary.md,
spec-optimized/C07-vocabulary-glossary.md, plan-optimized/C07-vocabulary-glossary.md

## Findings — Track A (faithful: attack fidelity/completeness)

### RC07-01 — major — The faithful glossary pins "layer 3 = pipeline engine" terminology that the optimized "layer" CanonicalReading does NOT use, risking the exact G01 overload C07 exists to kill
Claim: spec-A §4.1 defines the three-layer architecture and C01-A §1 (already fixed) calls C01 "the three-
layer-architecture pipeline-engine tier (C07 'layer' sense 1)." The C07-B CanonicalReading for "layer"
pins sense 1 as "(1) LLM client, (2) agent loop, (3) pipeline engine — plus persistence."
Evidence/reasoning: The faithful C07 glossary does NOT contain an explicit "layer" entry with a pinned
canonical reading and a rejected sense (the way C07-B does). It defines the three-layer architecture in
prose but leaves the G01 collision to OQ-C07-1 ("record both readings and defer"). That is *charter-
faithful* (Track A may not pin a contested term). BUT C01-A already cites "C07 'layer' sense 1" as if a
numbered canonical-sense registry exists in the faithful track — and it does not. So a downstream reader
following C01-A's citation into faithful-C07 finds no "sense 1" entry to land on. This is a dangling
cross-reference: C01-A asserts a C07 faithful artifact that C07-A defers.
Fix (APPLIED): added an explicit (non-pinning) "layer" entry to the C07-A §4.1 term table that *records
both readings and labels them* "sense 1 (three-layer architecture)" / "sense 2 (numbered Layer 0–6
principle tier)" — without picking a winner (faithful), so C01-A's "sense 1" citation has a concrete
anchor. The disambiguation authority stays deferred per OQ-C07-1; only the *labeling* is added.

### RC07-02 — minor — Term inventory differs between the two tracks (faithful ~23 terms incl. Polecat/Mayor/Wait; optimized enumerates ~13+10)
Claim: spec-A §4.1 lists Polecat, Mayor, Wait, Gas City placement, Convoy as distinct rows; spec-B §1
enumerates "~13 Gas City + ~10 paradigm" terms and does not separately call out Polecat/Mayor/Wait in §1.
Evidence: Not a defect — the faithful track is correctly a *superset* (its invariant §3.4 "C07 is a
superset, never a subset" of AI-CONTEXT §3.2/§3.3, which DO list Polecat/Mayor). The optimized §1 count is
illustrative. The two tracks should both ultimately register the same Gas City term family. Fix (DEFERRED):
no change; flagged so sweep-2 reconciles that the optimized `CanonicalTermSet` includes the §3.3 pack-
specific roles (Polecat/Mayor) the faithful track carries, or explicitly scopes them out.

### RC07-03 — minor — "gene transfusion" definition is faithful-by-analogy but G07 (no correctness predicate) is not surfaced as a C07 limitation
Claim: spec-A §4.1 defines "gene transfusion" from README:384 ("pointing the agent at a concrete exemplar
and asking it to reproduce the behavior").
Evidence: Faithful to the source. But G07 flags that this definition is *analogy-only with no operational
success predicate* — and C07 is the canonical home of the term. C07 cannot invent the predicate (that is
C51's job, faithful-correctly), but the glossary entry should note the definition is analogy-only and that
the operational meaning is owned/unresolved at C51 (G07), so a reader does not mistake the one-liner for a
complete definition. Fix (APPLIED): added an owner-pointer + G07 caveat to the gene-transfusion row (points
to C51, notes the success predicate is unresolved per G07).

## Findings — Track B (optimized: attack the design)

### RC07-04 — major — DELTA-02 grants C07 authority to pin "layer"/"phase" but the "phase" resolution asserts a corpus fact (Phase 6 = typo for Layer 6) that the corpus does not actually establish
Claim: spec-B §4 CanonicalReading for "phase": pinned sense = four-phase plan P0–P3; "Stray 'Phase 6'
(README:342) is a **typo for the numbered 'Layer 6'** principle tier, not a missing phase."
Evidence/reasoning: G02 (the source gap) explicitly says "a reader cannot tell whether 'Phase 6' is a typo
for 'Layer 6' or a missing phase." C07-B resolves it by *asserting* it is a typo for Layer 6. That is a
defensible reading (Track B may pin), but it is stated as fact ("is a typo") rather than as a pinned
*decision among genuinely ambiguous readings*. If "Phase 6" actually meant a later delivery phase the docs
never enumerated, rewriting every "Phase ≥4" to "Layer N" (the disambiguation rule C07-B mandates) would
*erase* a real gap rather than resolve it. The authority to pin is in-charter; presenting the pin as a
discovered fact is the over-reach.
Fix (APPLIED): softened the "phase" CanonicalReading from "**is** a typo for Layer 6" to "**pinned reading:**
a typo for the numbered Layer-6 principle tier (the most v4-consistent reading of G02; there is no enumerated
Phase 4/5/6)" — preserving the pin while marking it a decision, not a discovered fact. The rewrite rule now
says "rewrite to Layer N *or* flag for human confirmation" rather than unconditionally rewriting.

### RC07-05 — major — DELTA-02's rename authority (OQ1) is the load-bearing risk and the spec lets the `rename_recommendation` field read as binding
Claim: spec-B §3 `CanonicalReading.rename_recommendation` ("Layer N" → "principle tier N"); OQ1 concedes it
is unresolved whether C07 may *mandate* the rename across C54/C57/AI-CONTEXT §6/§7.
Evidence/reasoning: A corpus-wide rename is a cross-component edit touching at least C54, C57, and the v4
source docs — i.e. it would require editing files outside C07's ownership and even outside the spec/plan
set (the AI-CONTEXT source). If `rename_recommendation` is treated as binding by a downstream builder, C07
silently authorizes edits it has no authority to make. OQ1 flags this but the field name ("recommendation")
plus DELTA-02's "granted authority to pin" can be read as license to rename. Fix (APPLIED): clarified in §3
and the DELTA-02 line that `rename_recommendation` is **advisory only**; pinning + off-canon lint is the
binding authority, and any actual rename is an integrator/human cross-component decision (OQ1) — C07 may not
edit C54/C57/source docs. Keeps the recommendation, removes the implied mandate.

### RC07-06 — minor — Six deltas; DELTA-04 lint-set wiring couples C07 to C10/C15 build order, which the plan handles but the spec under-states as a hard dependency
Claim: spec-B DELTA-04 + invariant "lint-set completeness"; the linters "can never be asked to accept a
term the glossary doesn't carry."
Evidence: Good design. The plan-B (T10) correctly backgrounds this on C10/C15 and stubs the sink, and the
single-source-of-truth-data pattern (OQ2) is the right vehicle. The only nit: the *spec* presents the
linter consumption as if C07 is purely upstream, while in practice the `CanonicalTermSet` *export format*
must be co-agreed with C10/C15 (a two-way contract), which OQ2 raises. No over-claim, just an emphasis gap.
Fix: none applied (plan already handles it); noted for sweep-2 that the export schema is a C07↔C10/C15
co-freeze, not a pure C07 output.

### RC07-07 — minor — DELTA-06 `extraction_safe_synonym` / `lock_in_cost` per term is a nice idea but has no consumer and risks being dead metadata
Claim: spec-B §3 `GlossaryEntry` carries `lock_in_cost` and `extraction_safe_synonym`; DELTA-06 frames
these as making vocabulary "recoverable, not a trap."
Evidence/reasoning: Neither field has a named consumer — no linter reads them, no acceptance criterion
tests them (§8 AC-1…7 do not reference them), and no other component queries them. They are documentation-
of-intent fields. That is not harmful, but a Track-B delta should be forced by a concrete consumer; as
written DELTA-06 is taste/hygiene, not a forced improvement. Fix (APPLIED): added a one-line justification
tying `extraction_safe_synonym` to the C01-B DELTA-01 portability contract (if the runtime substrate is
re-platformed, the synonym is the term-level migration map) and `lock_in_cost` to C57's residual-risk
register — giving both fields a named downstream consumer so they are not dead metadata. If no consumer is
accepted, DELTA-06 should be dropped (DEFERRED to integrator).

## Cross-component notes
- **"layer"/"phase" overload resolution is the through-line of C07** and it is correctly handled *as a
  track difference*: faithful C07 records-both-and-defers (OQ-C07-1), optimized C07 pins via CanonicalReading
  (DELTA-02). C01-A's "sense 1" citation now has an anchor in faithful-C07 (RC07-01). Consistent.
- **C07 is cited by ~15+ components for term ownership** (C07-B §2). The owner-pointer-integrity invariant
  (every `owning_components` C-ID resolves) is the right guard; note it depends on the inventory C-ID set
  being frozen (plan-B risk 3 handles this). No contradiction found between C07's owner-pointers and the
  inventory.
- **`model stylesheet` / `Order` / `bead` / `gene transfusion`** carry their depth in C29/C40/C19-20/C51 —
  both tracks correctly hold only a one-liner + pointer (faithful §4.1 FAITHFUL-FILL; optimized owner-
  pointer-integrity invariant). No dual-source-of-truth drift introduced by C07.
- **Rename authority (RC07-05 / OQ1)** is the one item that could cause C07 to authorize out-of-scope edits
  to C54/C57/source docs; now marked advisory. Mirror to review-log as an integrator decision.

## Verdict
- **Track A: accept-with-fixes** — faithful and complete against the G06 bar; the dangling "sense 1"
  citation (RC07-01) is anchored and the gene-transfusion G07 caveat added. Collision-pinning correctly
  deferred per charter.
- **Track B: accept-with-fixes** — the CanonicalReading mechanism is the right structural kill for G01/G02,
  but the "phase" pin over-asserted a corpus fact (now marked a decision), the rename authority read as
  binding (now advisory), and DELTA-06's two fields lacked consumers (now tied to C01-B/C57). Design is
  sound; the authority-scope of DELTA-02 (OQ1) remains the one genuine open architectural question.
