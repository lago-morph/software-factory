# Adversarial review — C51 Gene-transfusion discipline (canonical track, sweep 1)

Reviewer persona: ADVERSARY / critic-fixer (single canonical track; posture = fidelity + completeness, plus the capability-for-principle bar).
Target: `spec/C51-gene-transfusion.md` (+ `plan-faithful/C51-gene-transfusion.md`)
Gaps in scope: **G07, G14, G30** only. Binding: D-1..D-17 (esp. D-6, D-15, D-14; RC11-01).

## Summary of attack

C51 is the foundational "bet" component: its **transfusion-correctness/completeness predicate** is the acceptance
contract C52–C54 hang on (inventory critical-path note #4). The hardest scrutiny went to (a) whether that predicate
is REAL + FALSIFIABLE + MINIMAL and built on the existing C30/C31/C32/C33 tier rather than a new engine; (b) whether
THE BAR's dropped items (second judge, SBOM/license scanner, signed provenance) stayed dropped; (c) RC11-01 component
grain; (d) the G30 license-mode contract grounding; (e) citation fidelity against README/AI-CONTEXT and contract
consistency with C08/C20/C52/C53.

**Predicate is real.** It is a `{pass|fail|inconclusive}` decision = *(every named exemplar behavior covered by ≥1
scenario) ∧ (satisfaction over those scenarios ≥ bar)*, expressed over C30/C31/C32/C33 (no new scorer), grounded in
two verbatim v4 anchors — README:496 "does this behave like the exemplar?" and AI-CONTEXT §9.2 "Scenarios cite
original exemplar behavior". It is falsifiable (§8.3: a component satisfying a generic spec but covering no exemplar
behavior does **not** pass) and minimal. The one genuine soft spot — the *completeness* half depends on "named
exemplar behaviors" being enumerable, which v4 never gives a method for — is honestly surfaced by the spec itself
(OQ-C51-1, top) and spiked first in the plan (§5 risk #1). It is **not** an empty/hand-wavy predicate; it is not a
blocker.

## Findings

### RC51-01 — major — Predicate's *completeness* half is overclaimed as "addressed" while its only input (named-behavior extraction) is undefined
- **Claim.** §6 F-mode table marks G07 "**Addressed at sweep-1 altitude**" and §8.3 states `pass` requires "every *named*
  exemplar behavior is covered by ≥1 scenario." But the *enumeration* of "named exemplar behaviors" — the completeness
  anchor — has **no defined source** (OQ-C51-1 concedes v4 "names no behavior-extraction method"). A predicate clause
  whose input set is undefined is not yet a checkable predicate; "complete" is currently subjective.
- **Evidence.** Spec §3.3, §8.3 (completeness clause) vs OQ-C51-1 ("Without a defined anchor, 'complete' is
  subjective — the residual edge of G07"). Plan §5 risk #1 itself says "If enumeration is infeasible, completeness must
  weaken to a coverage heuristic at sweep-2." v4 grounding (AI-CONTEXT §9.2 "Scenarios cite original exemplar
  behavior") supports the *correctness* half strongly but gives no behavior *list* mechanism.
- **Severity reasoning.** Not a blocker — the *correctness* half of the predicate is fully grounded and operational at
  sweep-1, and the completeness gap is explicitly carried as the top OQ + first spike. But the F-mode wording
  "Addressed" overstates closure of G07's completeness dimension.
- **Fix (APPLIED).** Softened the §6 G07 row and the §1 framing to state that the *correctness* half is closed at
  sweep-1 and the *completeness* half is **predicate-shape-defined but anchor-deferred** (OQ-C51-1), so the doc no
  longer reads as if completeness is fully operational pre-sweep-2. No design change; wording only.

### RC51-02 — minor — G14 class-level fallback asserted-adjacent to C54 ownership that C54 does not yet carry
- **Claim.** §6 (G14 row) and §9 OQ-C51-2 route the *class-level* hedge ("a whole high-value class cannot be
  transfused → re-sequence / hand-build") to **C54**. C54's spec sequences *when* transfusion-built components land
  but does **not** own a "the bet failed for a whole class" fallback.
- **Evidence.** `spec/C54-phase-plan.md` lines 32, 44, 81 sequence per-piece transfusion under C51 but contain no
  class-failure hedge; C51 OQ-C51-2 says "Confirm C54 owns the class-level hedge." So C51 already frames this as an
  open *confirmation*, not a settled fact — which is the correct, honest posture.
- **Severity reasoning.** Minor: C51 does not falsely assert C54 owns it; it raises it as an OQ. The only risk is a
  reader treating the §6 "the strategic fallback … is a C54 phase-plan decision" line as settled. Per-component
  falsification (the part C51 actually delivers — §3.5 `transfusion-insufficient` → human review) is real and grounded
  (README:498).
- **Fix (APPLIED).** Added "(to be confirmed — see OQ-C51-2; C54 does not yet carry this)" to the §6 G14 row so the
  class-level hedge reads as an open routing rather than an established C54 contract.

### RC51-03 — minor — `transfusion_mode`/`transfusion_verdict`/`transfusion_license` are C20 slot *requests*; ensure no reader mistakes them for existing C20 fields
- **Claim.** §4 lists four component-grain values as if co-resident on the `factory_build` bead. C20's actual spec
  (§4 line 134) lists **only `transfused_from`** as a `factory_build` field; the other three do not exist in C20 yet.
- **Evidence.** `spec/C20-bead-schema.md` §4 (`factory_build` row carries `transfused_from` + spec/scenario pointers
  only). C51 §4 already flags `transfusion_mode`/`transfusion_verdict` as `[FAITHFUL-FILL]` "inferred field names …
  C20 schema-slot requests"; `transfusion_license` is grounded in AI-CONTEXT:429 prose but is likewise not yet a C20
  field. C52 §3 line 79 corroborates C51's framing ("Recorded on the `factory_build` bead (C20 slot per C51 §4)").
- **Severity reasoning.** Minor — the spec's `[FAITHFUL-FILL]` block already does the right thing (frames them as
  requests, keeps grain component-level per RC11-01, invents no richer provenance). This is a clarity hardening, not a
  contradiction.
- **Fix (APPLIED).** Extended the §4 `[FAITHFUL-FILL]` note to state explicitly that `transfusion_license` is also a
  C20 slot request (not just mode/verdict), and that C20 today carries only `transfused_from` — so the table is read
  as "values C51 gives meaning to and requests as C20 slots", not "fields C20 already provides."

### RC51-04 — minor — Citation precision: AI-CONTEXT:430 vs ":625" labeling, and README line-anchors
- **Claim.** §1/§3.4 cite "AI-CONTEXT:430" for donate-back-vs-private and "AI-CONTEXT:625" for the code-vs-pattern
  rule. Both verify, but worth recording for downstream auditors: :430 is §9.2 "Permissively-licensed transfusions can
  be donated back upstream; restrictively-licensed ones stay private" (exact), and :625 is the **risk-register** line
  "Tracker license is non-permissive … if restrictive, transfuse pattern without adopting code" (exact — a *stronger*
  anchor than a generic prose ref, since it grounds the code/pattern split in v4's own risk table).
- **Evidence.** AI-CONTEXT.md:430 and :625 read verbatim as the spec uses them. README:496–500, :285–306, :335,
  :457–470 all verify. §16 cold-start step 2 = "Check `transfused_from` attribution" (verbatim).
- **Severity reasoning.** Minor/no-defect — this is a *confirmation* finding. All load-bearing citations check out;
  none is mislabeled-fact or mis-cited. Recorded so the orchestrator need not re-verify.
- **Fix.** None required (citations correct). No edit.

### RC51-05 — minor — Forward reference to C57 (not yet on disk) for license-disposition aggregation
- **Claim.** §2, §6, §7, OQ-C51-4 route license-disposition aggregation + census authority to **C57**, which does not
  yet have a spec on disk.
- **Evidence.** `spec/C57-*` absent; inventory confirms C57 `depends on C51` and "owns license hygiene + the …
  residual/caution register". So the dependency direction (C57 ← C51) and the ownership claim are inventory-grounded;
  C51 is the *supplier*, C57 the *aggregator*.
- **Severity reasoning.** Minor — forward reference to an inventoried-but-unbuilt later-batch component (Batch 5) is
  expected and consistent with the inventory; not a fidelity defect. Flagged only so the C57 builder inherits the
  obligation (census authority + verification workflow) C51 hands it.
- **Fix.** None required; left as the standing OQ-C51-4. No edit.

## What was checked and is SOUND (no finding)

- **THE BAR upheld.** C51 explicitly drops a second judge (§NOT-list, §7 cost), an automated SBOM/license scanner
  (§NOT-list, §6 G30, §9), and signed transfusion provenance (§7, OQ-C51-5 → FE-3 blocked on G37 per D-14). The keep
  is exactly the predicate + `transfused_from` recording + license-mode contract. No hardening-on-existing-capability
  smuggled in.
- **RC11-01 component grain.** §3.2 invariant, §4 table, §8.2, plan DoD-2 all hold `transfused_from` at the
  per-factory-built-component grain on the `factory_build` bead — not per-record/per-trajectory. Consistent with
  C20 §2 (C51 listed as `transfused_from` consumer) and C52 (resume reads it from the build bead).
- **G30 license-mode contract grounded in v4's census.** §3.4 / §6 build the verified-permissive→code-port vs
  unverified/restrictive→pattern-reimplement rule on README:285–306 (the actual census, Tracker = "Verify before
  adopting") + AI-CONTEXT:625 (risk-register "if restrictive, transfuse pattern without adopting code"). Real, not
  invented.
- **Contract consistency with C08/C20/C52/C53.** C08 §2 lists C51 as a DoD consumer (free-form DoD; D-15 holistic —
  matches §3.3). C20 §2/§4 corroborate the `factory_build`+`transfused_from` slot. C52 §1/§2/§3 confirm it *calls*
  C51's predicate and *consumes* `transfusion-insufficient` (no contradiction; bidirectional). C53 §1/§2 confirm it
  *consumes a passing* C51 predicate for the first component and disclaims being the per-component predicate. No
  cross-component contradiction found.
- **D-15 / threshold-free.** §3.3 / §8.3 correctly route the *numeric* satisfaction bar to C50/C53 (parity with
  C33:OQ-1 threshold-freedom), not set in C51. Consistent with D-15 holistic satisfaction over C08's free-form DoD.
- **External-grounding exclusion (A107).** §3 invariant / §8.6 correctly exempt adopted upstream substrate (CXDB,
  Temporal) from the ≥1-exemplar invariant — grounded in README:500.
- **Plan fidelity.** Critical path (T1→T3→T6→T8) correctly identifies T3 (predicate) as the load-bearing node;
  parallelization (T2/T3/T4 after T1) is real; the §5 spike order retires the right uncertainty (named-behavior
  extraction) first; the §5 over-build-drift row restates THE BAR. No invented architecture.

## Verdict

**accept-with-fixes.** The predicate is real, falsifiable, minimal, and built on the existing eval tier — the
foundational bet is sound and the BAR is respected. All load-bearing citations verify and the contract is consistent
with C08/C20/C52/C53. The five findings are one major (completeness-half overclaim — wording) and four minor
(clarity / open-routing / forward-ref / citation-confirmation); all confident fixes applied in place. No
blocker-class finding; no architecturally-significant deferral introduced beyond the spec's own existing OQs (which
are correctly homed).
