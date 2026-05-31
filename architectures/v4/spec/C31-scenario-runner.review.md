# Adversarial review — C31 Scenario Runner (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Evaluation & Judge
Target: `spec/C31-scenario-runner.md` + `plan-faithful/C31-scenario-runner.md`
Posture (per CONVERGENCE BANNER): single canonical track — attack **fidelity + completeness**, not design,
**plus** the capability-for-principle bar (flag hardening-on-existing-capability disguised as new capability).

## Summary of attack vectors (all cleared except the findings below)

- **THE BAR (off-the-shelf runner).** PASS. The spec is emphatic and consistent that C31 **wraps** Inspect
  AI's `inspect eval` and builds **no** custom runner / scheduler / eval-loop / parallel-run engine / retry /
  rate-limiter / scoring: INV-1, the §6 explicit DROP list, AC-9, and the plan's risk #5 + critical-path note
  all enforce this. The single genuine KEEP is the **session-id adapter (I4 / G25)**, correctly scoped as a
  thin 1:1 id translation baseline with a thick id-map fallback (depth = OQ-1, a spike). This is a real
  capability-for-principle item (P5 trajectory attribution → P6 scoring → P10/P11 memory cannot be met without
  the reconciliation, and no OSS piece provides it — "impedance unknown"), not hardening on existing stack.
- **D-13 (read-isolation).** PASS. C31 runs in `work_partition="scenarios"` and explicitly does **not**
  enforce/audit holdout (INV-3, §1 boundary, §6 DROP). C34 enforces, C42 provides the partition, C30 stores,
  C32 judges, C24 delivers turns. No ownership crossing; the §2 table and plan §2 "governed-by, not a build
  dep" are correct.
- **G25 (the assigned gap).** PASS. Addressed as C31's core custom deliverable (§6, I4, INV-2, AC-3/AC-4,
  OQ-1, plan T2/T4). The two-reading [AMBIGUITY] block is well-formed and routes depth to a spike.
- **Citations.** Spot-checked the load-bearing ones against source: README:170/172/173/175/177/195/240/252
  and the Phase-2 block 423–442; AI-CONTEXT §12 L512 (G25), §4.3 L178 (`session.id`), §13.3 L599–608 (the
  exact `inspect_eval` `[[tool]]` subprocess with `work_partition="scenarios"`), §5.4 L229 (parent-chain via
  `session.id`), §7 L300, §11.1 L467; F-MODE F9:19, F28:22, F39:90, F45:92. **All verified accurate** — an
  unusually well-traced spec. C30 (storage/authoring) and C17 (tool-node) specs are consistent with C31 (the
  author/execute split, the C32-is-not-a-tool-node note, the session-id adapter landing on C31 not C30).

## Findings

### RC31-01 — minor — Mis-cited binding decision: the cross-family relaxation is **D-1**, not **D-9**
**Claim.** §1, last boundary bullet ("NOT cross-family enforcement"): *"And per review-log D-9, cross-family
is relaxed to same-provider for now."* **Evidence.** Review-log **D-9** is *"F38 (undefined-vocabulary
detection) owner = C10"* — nothing to do with model family. The decision that relaxes "judge ≠ coder family"
to same-provider is **D-1** (*"implement the judge with the SAME provider/family as the coder for now … C29
cross-family rule becomes advisory/relaxed"*). This is a wrong decision-ID citation — a fidelity defect (the
substance is right; the pointer is wrong, and the brief lists D-13/D-6 as the relevant settled decisions, so a
stray D-9 invites confusion). **Fix (applied).** Re-pointed the citation to **D-1**.

### RC31-02 — minor — README:439 supports "scenario-to-bead binding via pack" but the spec twice attaches it to claims slightly beyond the source phrase
**Claim.** I5 and AC-8 cite README:439 for *"the emitted trajectory + run identity are **bound to a bead**
such that C32 can locate and score the right trajectory ('scenario-to-bead binding via pack')."* **Evidence.**
README:439 reads *"**P5** … Inspect AI handles storage + execution; **scenario-to-bead binding via pack**"* —
it confirms the *binding-via-pack* concept but does not itself spell out "trajectory + run identity bound to a
bead so the judge can locate it"; that elaboration is a faithful inference, not a verbatim v4 statement. The
inference is sound (it follows from the bead model C19/C20 + the judge-consumes-trajectory flow) but at sweep 1
it reads marginally as asserted-fact. **Fix (applied).** Added a one-clause `[FAITHFUL-FILL]` qualifier at I5
flagging the bead-binding *shape* as inferred from README:439 + the bead model, with the exact shape deferred
to sweep 2 (already listed in the §5 deferral note and OQ-4) — so it is not read as a v4-stated contract.

### RC31-03 — minor — INV-2 / AC-3 assert C24 will land turns "as one parent-chained trajectory" as if a settled cross-component fact; it depends on an unresolved C24 seam (G26)
**Claim.** INV-2 and AC-3 state the adapter's correct `session.id` makes C24 land the run's turns "as a single
parent-chained trajectory in CXDB," cited to AI-CONTEXT §5.4. **Evidence.** AI-CONTEXT §5.4 (L229) says only
*"parent-chain via `session.id`"* as a one-line property; the actual `session.id` → CXDB parent-turn-pointer
**mapping rule is undefined** and is flagged as gap **G26** (the raw-bodies→CXDB bridge seam, owned by C24).
C31 correctly makes its *own* obligation "produce a coherent `session.id`," but the downstream guarantee that
this yields one parent-chained trajectory is contingent on C24's unresolved mapping. The spec already hedges
this softly (OQ-3 granularity, "verifiable by C24 landing them") but states the landing as a guarantee in
INV-2/AC-3. **Fix (applied).** Qualified INV-2 to note the *parent-chain landing itself* is C24's mechanism
(G26 seam) — C31 guarantees only the coherent `session.id` that makes it possible — keeping the C31/C24
ownership boundary clean and not over-claiming a cross-seam result. AC-3 left as a verification *target*
(testing C31+C24 together is the right end-to-end check); no over-claim remains once INV-2 is scoped.

### RC31-04 — minor (completeness) — F45 residual is named but its "Partial" status (not "Addressed") could be stated, to match F-MODE-COVERAGE
**Claim.** §6 / §7 / INV-5 treat the Python-harness fault (F45) as *bounded* by the subprocess boundary,
phrased as if fully handled. **Evidence.** F-MODE-COVERAGE F45 (L92) is **"Partial — Python sections inherit
risk,"** not Addressed; the subprocess boundary bounds the *blast radius* but does not eliminate the
language-mismatch residual. C31's framing ("bounded to the subprocess") is correct as far as it goes but reads
as stronger than the canonical "Partial." **Fix (applied).** Adjusted the §6 F-mode note to say C31 *bounds*
(not closes) the F45 residual — the residual remains Partial per F-MODE-COVERAGE, with the canonical mapping
owned by C57. Minor wording; keeps the spec from implying a stronger status than the coverage map.

### RC31-05 — minor — D-9 stray reference is the only review-log mis-pointer; no other binding-decision violations found (positive finding / no fix)
**Claim/Evidence.** Confirming the negative: D-6 (canonical track) is honored — the spec headers say
"canonical track" and do not frame a live Track B (one residual `Track: A (faithful)` line in the source
header is legacy-but-harmless and matches the example C23 review's tolerance; flagged here, not rewritten, as
the BUILDER-brief header format is `_meta`-governed). D-13 is honored throughout. No D-1..D-14 decision is
*violated*. **Fix.** None — recorded for completeness so the verdict rests on a full decision sweep.

## Verdict

**accept-with-fixes.** A strong, faithful, exceptionally well-cited spec+plan that correctly nails the central
bar (Inspect AI is the runner; the session-id adapter is the only genuine custom code) and keeps the D-13
read-isolation boundary clean (runs-in / does-not-enforce). All five findings are **minor** fidelity/altitude
qualifications, not design or architecture issues: one wrong decision-ID citation (D-9→D-1), and four
"qualify an inferred/cross-seam/adopted-status claim as such rather than asserting it as a settled v4 fact"
fixes (bead-binding shape, C24 parent-chain landing, F45 Partial status). **All five applied in place; nothing
deferred** — no finding was architecturally significant or ambiguous enough to need orchestrator escalation.
The load-bearing uncertainty (adapter thin-vs-thick depth, OQ-1) is already correctly carried as a spike and
is a genuine empirical unknown, not a spec defect.
