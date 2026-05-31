# Adversarial review — C38 Diagnosis Agent (Healer) (canonical track, sweep 1)

Reviewer persona: Subsystem Adversary — Self-Healing Loop
Target: spec/C38-diagnosis-agent.md + plan-faithful/C38-diagnosis-agent.md
Charter: canonical track → attack FIDELITY and COMPLETENESS only (not design), PLUS the
capability-for-principle bar (flag any custom investigation/agent loop or CXDB query tooling that is
hardening on existing stack capability rather than new capability tied to a 12-principle).

## Findings

### RC38-01 — major — "C39's spec is not yet on disk" is stale and false; C39's spec exists and *confirms* the C38/C39 split the spec frames as open
**Claim.** The spec (§9 OQ1) and plan (§3 "Built concurrently", §4 milestone 4) assert the C38↔C39 seam is
open *because* "C39, whose spec is not yet on disk" / "overlaps C39, whose spec is not yet on disk."
**Evidence.** `spec/C39-fix-task-loop-closure.md` is present on disk (40 KB, sweep-1) and is unambiguous on
the seam: its §1 — "C39 is the **fix-task generation + loop-closure control-loop** … takes a **diagnosis**
(from C38, the Healer) and (1) generates a `fix_task` bead"; its §1 "Explicitly NOT … the **diagnosis**.
Root-cause analysis over clustered failures is **C38** … C39 *consumes* a diagnosis and *generates* the fix
task from it; it does not diagnose"; its §2 lists C38 as the upstream `Depends on`; its §3.1 contract 1
("Diagnosis-intake contract (C38 → C39)"). So the exact split C38 *infers* from the inventory
(C38 emits `Diagnosis`; C39 mints `fix_task`) is now **independently confirmed by C39's own spec**, not a
still-unverified inference. The "not yet on disk" justification is a factual error that understates the
seam's settledness and would mislead a sweep-2 author into re-litigating a confirmed boundary.
**Fix (applied).** Replaced the three "C39 spec not yet on disk" clauses with the live cross-reference: the
C38/C39 *split* is **confirmed by `spec/C39-fix-task-loop-closure.md`** (§1, §3.1 contract 1); only the
*handoff mechanism* (poll-vs-hand-off) remains a sweep-2 detail. Severity major because it is a citable
false statement about the corpus state on the spec's single load-bearing seam.

### RC38-02 — minor — OQ1/Risk-4 frame the seam *ownership* as open when only the handoff *mechanism* is
**Claim.** OQ1 ("C38↔C39 seam — who writes `fix_task`?") and plan Risk-4 ("a wrong split strands the
loop-closure") read as if *who emits Diagnosis vs who mints fix_task* is still undecided.
**Evidence.** Given RC38-01, ownership is settled in both directions (inventory split + C39 spec §1/§2/§3.1).
What is genuinely open is narrower: whether C39 *polls* C38's `Diagnosis` beads or C38 *hands* the
`Diagnosis` to a C39 entry — a wiring/transport detail, not an ownership question. C39's own OQ set does not
re-open the split either. Leaving the broad framing overstates residual risk on a confirmed boundary.
**Fix (applied).** Narrowed OQ1 and Risk-4 to the *handoff mechanism* (poll vs hand-off) and recorded that
the *ownership split is confirmed* by C39's spec; the numeric termination/escalation policy is C39's
(XC-3), which C39's spec §1/§3.2 contract 7 now explicitly carries.

### RC38-03 — minor — `transfused_from` is modeled onto the per-cluster `Diagnosis` record, but the corpus puts transfusion provenance on the `factory_build` bead (C20/C51/D-3), not on each runtime output
**Claim.** §4 data-model row and the `Diagnosis` shape (§3 contract 5, §5 step 4, plan T5) carry
`transfused_from` as a field of the per-cluster `Diagnosis` runtime record; AC7/I6 likewise stamp it "on the
build" but the schema row lists it inside `Diagnosis`.
**Evidence.** Per C51 §1/§3 and C20 (D-3), `transfused_from` + the per-source license fact + the
pattern-vs-code flag are fields on the **`factory_build`** bead (the provenance of *building C38 itself* — a
one-time build fact), graded once by C51's predicate. A `Diagnosis` is a *runtime output* emitted per
failure cluster; stamping the build-time transfusion provenance onto every per-cluster diagnosis record
conflates build provenance with runtime payload and would mis-place the field at sweep-2 schema-freeze
(C39 binds to the `Diagnosis` schema). The *intent* (C38 records what it transfused from; C51 owns the
framework) is correct and faithful; only the *carrier* is mis-located.
**Fix (applied).** Clarified that the transfusion provenance (`transfused_from` + pattern-vs-code flag) lives
on C38's **`factory_build`** bead (C20/C51, D-3), not as a field of each per-cluster `Diagnosis`; dropped
`transfused_from` from the `Diagnosis` minimal field set and noted the build-bead home. The `Diagnosis`
still carries {cluster_id, root_cause, evidence_refs[], confidence, proposed_remedy}. This keeps the C51
routing intact and removes a schema mis-placement before C39 binds to it.

### RC38-04 — minor — `[AMBIGUITY: G07-adjacent]` tag on the §1 boundary is a non-standard label and double-counts the §6 G07 treatment
**Claim.** §1 boundary tags the C38/C39 `fix_task` discussion `> [AMBIGUITY: G07-adjacent]`.
**Evidence.** The C38↔C39 `fix_task` seam is the README:257-vs-inventory split (OQ1) — it is **not** G07
(diagnosis *correctness*), which §6 already handles in full. The "G07-adjacent" coinage is not a real gap id
and risks a reader treating the seam as part of the G07 disposition. The faithful tag for an
inventory-vs-README ownership ambiguity is a plain OQ pointer (OQ1), not a Gxx.
**Fix (applied).** Retagged the §1 boundary note to reference **OQ1** (the seam) and dropped the
"G07-adjacent" label so G07 is named only where it is actually handled (§6). No substantive change to the
reading (the inventory split stays authoritative).

### RC38-05 — minor — D-1 is verbatim a *judge*-provider decision; the spec attributes the diagnosis-LLM reading to D-1 directly. Sanctioned by the dispatch brief, but worth an explicit fill-tag for traceability
**Claim.** Throughout (§1, §2 C28/C29 rows, §5, §7) the spec attributes "the diagnosis LLM = Claude Code,
same provider as the coder" to review-log **D-1**.
**Evidence.** D-1 verbatim (review-log:10–15) decides the **judge** provider ("implement the judge with the
SAME provider/family as the coder for now") — it does not name the diagnosis/healer agent. Extending
same-provider-at-Phase-0 to the diagnosis role is a reasonable parallel (and the *dispatch brief explicitly
sanctions* "D-1 (diagnosis LLM = Claude Code same-provider)"), so this is correct *as briefed*, not an
over-reach. The only fidelity nit: the spec presents it as D-1's literal scope rather than a
brief-sanctioned extension of D-1's posture, which a future reader checking D-1's text would trip on.
**Fix (applied).** Added a one-line note at the §1 first D-1 use that D-1 verbatim governs the *judge*
provider and is applied to the diagnosis role as the same Phase-0 same-provider posture (per the C38
dispatch brief); FE-1 is the cross-provider future. Mechanical citation hygiene; no reading change.

## Verdict
**accept-with-fixes.** C38 is faithful and well-traced, and it passes the two bars that matter most for this
component:
- **THE BAR (capability-for-principle):** correctly KEEPS only the diagnosis prompt/role + the
  `Diagnosis`→C39 handoff, and explicitly DROPS the investigation/agent loop (C28), the CXDB query tooling
  (C21), and the transfusion correctness/license *framework* (C51) — §1 even states the reasoning ("the
  investigation loop is what the stack already does → DROP", line 107). No custom investigation loop or CXDB
  query tooling is invented. Clean.
- **THE SEAM (C38↔C39):** C38 took the inventory split — it emits `Diagnosis`, does **not** write `fix_task`,
  does **not** own termination/escalation (I2, AC5, §1 boundary, XC-3) — and this is now confirmed by C39's
  on-disk spec. No over-reach into C39's job.
- **G30/G07:** both routed correctly — pattern-by-default transfusion (legal regardless of Tracker license)
  with the license-hygiene *framework* + correctness *predicate* sent to C51 (verified against C51 §1/§3,
  which names C38's exact concepts); C38 keeps only its local part (the C38-local license question +
  match-the-human acceptance AC2).

All citations spot-checked clean: README:248/256/257/261/462/466, AI-CONTEXT:276/331/407/625, F-MODE
F4@42 / F22@44 / F23@45 / F54@93 all match exactly. Fixes are all hygiene/staleness corrections (the stale
"C39 not on disk" claim — the one major; the OQ1 over-framing; the `transfused_from` carrier; the
"G07-adjacent" mislabel; the D-1-scope note). Nothing architecturally significant deferred; no blockers.
