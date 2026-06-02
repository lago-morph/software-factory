# C53 — Bootstrap-validation milestone  (Build Plan, canonical track)

> Source / Spec ref: spec/C53-bootstrap-validation.md
>
> **Sweep-2 update (2026-06-01):** Tasks T1–T9 retained verbatim (Sweep-1 WBS is correct). Updated task descriptions to reflect: concrete `decide()` signature (§3.1), `GoNoGoInput`/`GoNoGoDecision` schemas, `MilestoneConfig` knobs (§3.3), D-40 bead-slot assignment (§3.4), E-C53-01..08 error taxonomy (§8.1), AC-C53-01..13 acceptance test codes (§8.2). All four OQs resolved; no WBS restructuring needed. Critical-path unchanged: T1→T4→T5→T6→T8→T9. M1/M2/M3 contract milestones retain meaning; M1 now includes the `GoNoGoInput`/`GoNoGoDecision` schemas as the freeze artifacts.
>
> **Operator-judgment flag (OQ-1 resolved):** Before T5 (rubric evaluation) can be signed off, the operator MUST review and approve the decision-rule SHAPE (`p10 >= T_tail AND mean >= T_central`) as a morning-review item. This is a governance checkpoint, not a build step. It is a pre-condition on T5 completion and on the Phase-3 arm (T8).
>
> **Sweep-2 tri-alignment deepening (2026-06-02 — ADR-0069 / D-42 / D-43 / HANDOFF §0★.2.2):** T4 and T5 updated to reflect four-conjunctive-term `decide()` (100% hold-out floor, tri-alignment, human-review, post-deploy integrity). T9 harness extended to AC-C53-01..18 (adds AC-C53-14..18 for tri-alignment critical-path ACs). M1 updated — freeze artifacts now include `DiagnosisRecord` reference, `ReviewVerdict`, `IntegrityResult` typed structs. M2 renamed to "tri-alignment gate fixed" (distribution stats = evidence not gate; pass-rate pinned at 1.0). M3 updated with `diagnosis_bead_ref` addition to C20 bead. New T10 added: post-deploy factory-integrity harness wire-up (Term 4; owner TBD per OQ-5). WBS T1..T9 retained; T10 is net-new. Critical-path: T1→T4→T5→T6→T8→T10→T9. OQ-5 is the one open question introduced (integrity harness ownership).

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the milestone seam contract (M1)** — the **rubric** (I1: C51 predicate-pass ∧ C33 satisfaction ≥ bar ∧ C52 review-approve), the **decision-record** shape (I4: `go`/`no-go` + evidence bundle = C51 verdict ref, C33 distribution snapshot + scenario-set id + sample count, C52 review ref), and the **inputs it reads** (C51 verdict, C33 distribution, C30 scenario set, C52 review). This is the contract C54 (Phase-3 transition) builds against. | S | C51 predicate verdict shape, C33 distribution output, C52 review record, C30 scenario manifest |
| T2 | **Milestone artifact skeleton + config surface** — package C53 as the Phase-2-closing milestone evaluated with the eval/bootstrap pack; config (the **satisfaction bar value + decision rule**, the **fail-branch attempt bound**, which rubric terms gate) per C03 model. **No model call / no scorer** (the bar). | S | C02/C17 ABI, C03 config model, T1 |
| T3 | **Scenario-set precondition check (I2/INV-3)** — confirm the first factory-built component ships a **held-out scenario set** in C30's corpus (`scenarios/<component>/`); absence ⇒ automatic **no-go (insufficient-evidence)**. Reads C30; owns no corpus. | S | T1, C30 corpus + manifest |
| T4 | **Evidence read (I1/INV-2) — [tri-alignment: updated]** — pull the **C32 `DiagnosisRecord`** (keyed by `factory_build_ref`; contains `all_scenarios_satisfied`, `tri_alignment`, `holdout_pass_rate`, `judge_self_trust`, `root_cause`, `misalignments`), the **C51 transfusion-predicate verdict** (auxiliary evidence), the **C52 `ReviewVerdict`**, and the **post-deploy `IntegrityResult`** (from the factory-integrity harness). The **C33 `SatisfactionDistribution`** statistics are read as diagnostic evidence embedded in the `DiagnosisRecord`, NOT as the gate. Pure read of pre-computed signals — no scoring (INV-2). | M | T1, C32 DiagnosisRecord, C51 verdict, C52 ReviewVerdict, C30 scenario set, IntegrityResult |
| T5 | **Four-term conjunction evaluation (I1/I3/INV-5) — [tri-alignment: reframed]** — evaluate the four conjunctive terms: Term 1 (`all_scenarios_satisfied = true` — 100% floor, NEVER lowered), Term 2 (`tri_alignment = aligned` — requires Term 1 + `root_cause = none`), Term 3 (`ReviewVerdict = "approve"` — mandatory; satisfaction alone never deploys), Term 4 (`IntegrityResult.Passed = true` — post-deploy factory baseline). The satisfaction distribution stats (p10, mean, p90−p10 from `DiagnosisRecord.holdout_pass_rate` and embedded distribution) are surfaced as evidence to human review — NOT applied as a threshold gate. Bar **value** is removed as a gate concept; `pass_rate_floor` is pinned at 1.0 in `MilestoneConfig`. Surface `judge_self_trust` for oversight-level determination. | M | T2, T4 |
| T6 | **Decision record emit (I4/INV-4)** — write **`go`/`no-go`** + the **evidence bundle** to the first component's **`factory_build` bead** (C20/C19), attributed (C41), auditable/reconstructable. | S | T5, C20 slot, C19 write, C41 attribution |
| T7 | **Fail-branch escalation (I5, README:519)** — on **no-go**: name **iterate-spec + re-run** (C52); after a **bounded** attempt count still failing → escalate to **"add more substrate before Phase 3"** (AI-CONTEXT:619). Re-evaluate fresh builds; record each decision. Attempt bound + authorizer = config/operator policy (OQ-2). | S | T5, T6, C52 re-run |
| T8 | **Phase-3 arming output (I4 → C54)** — surface the decision so **C54 arms** (on `go`, README:436) or **withholds** (on `no-go`, README:519) the Phase-2 → Phase-3 transition. | S | T6 |
| T9 | **Bootstrap-validation harness (AC-C53-01…AC-C53-18) — [tri-alignment: extended]** — synthetic first-component decision driver: seed a C32 `DiagnosisRecord` (with `all_scenarios_satisfied` true/false, `tri_alignment` aligned/misaligned, `holdout_pass_rate`, `judge_self_trust`), a C51 verdict (pass/fail/inconclusive), a C52 `ReviewVerdict` (approve/reject), an `IntegrityResult` (passed/failed), and a scenario set (present/absent). Drive all ACs including the critical tri-alignment ACs: absent-scenarios→no-go (AC-C53-02), 100%-pass-with-misaligned→no-go (AC-C53-15), sub-100%-pass→no-go-regardless (AC-C53-16), all-four-terms-met→go (AC-C53-14), judge-uncalibrated→no-go (AC-C53-17), post-deploy-integrity-fail→no-go (AC-C53-18), fail-branch, no-second-scorer, one-time. | L | T3–T8, T10, synthetic DiagnosisRecord + IntegrityResult fixtures |
| T10 | **Post-deploy factory-integrity wire-up (Term 4 seam — OQ-5)** — integrate the factory-baseline scenario suite invocation after the new component is deployed into the factory. Produce an `IntegrityResult` (§3.1) that `decide()` reads as Term 4. Owner TBD: C52 (self-bootstrap loop drives the integration step) or a new integrity harness. Wire the `IntegrityResult` into the `GoNoGoInput` + the `GoNoGoDecision` evidence bundle. | S | T6, C52 deploy-phase, factory baseline scenario suite |

## 2. Dependency graph

**Must precede C53:**
- **C52** (the self-bootstrap loop that runs the first component + owns the human design-review record and `ReviewVerdict` C53 reads; drives the post-deploy integration step for Term 4).
- **C32** (produces the `DiagnosisRecord` — C53's Terms 1 + 2 key on `all_scenarios_satisfied` and `tri_alignment` from C32's `diagnose()` output; D-43).
- **C33** (satisfaction distribution — embedded in `DiagnosisRecord` as diagnostic evidence; no longer a threshold gate but still a dependency for the C32 diagnosis).
- **C51** (the transfusion-correctness predicate verdict — auxiliary evidence in `GoNoGoInput`; not a standalone conjunctive term of the four-term gate but still a precondition for meaningful tri-alignment).
- **C30/C31** (the held-out scenario set + runner that produces the trajectories C32 judges).
- **C20/C19** (the `factory_build` bead + store the go/no-go decision is recorded on; `diagnosis_bead_ref` is a new field request) + **C41** (attribution) + **C02/C03** (pack + config to host/configure the milestone).
- **Factory-integrity harness** (owner TBD per OQ-5 — produces the `IntegrityResult` C53 reads as Term 4).

**C53 must precede (its decision arms/withholds the next phase):**
- **C54** Phase delivery plan — the **Phase-2 → Phase-3 transition** reads C53's go/no-go (README:436/519).

**Critical path inside C53:** T1 → T4 → T5 → T6 → T8 → T10 → T9. The load-bearing task is **T5 (four-term conjunction evaluation)** — it composes pre-computed signals (C32 `DiagnosisRecord`, C51, C52, `IntegrityResult`), evaluates the four conjunctive terms (100% floor, tri-alignment, human-review, post-deploy integrity), builds **no** scorer, and owns **no** durable state beyond the decision record. T10 (integrity wire-up) is now on the critical path to T9 (harness). The **G23-closing tasks** are **T3 (scenario-set precondition)** + **T5 (four-term rubric)** + **T7 (fail branch)** + **T10 (integrity check)** — the four that together replace "looks good to a human" with a recorded, falsifiable tri-alignment gate; all four are deliberately scoped to avoid new capability (no second engine; no metric change; no loop; no distribution threshold).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (skeleton + config)** land, two thin workstreams fan out concurrently:
- **WS-A (evidence read):** T3 (scenario-set precondition) + T4 (evidence read). The input spine; can build
  against **synthetic** C51 verdicts / C33 distributions / C30 scenario manifests / C52 records while those
  upstreams firm up.
- **WS-B (decide/record/branch):** T5 (rubric + bar) → T6 (decision record) → T7 (fail branch) → T8
  (Phase-3 arming). The decision spine; can build against **synthetic** evidence bundles before WS-A's real
  reads land.
- **T9 (harness)** joins both. WS-A and WS-B meet at the T4 → T5 handoff (the collected evidence bundle).

## 4. Interfaces-first / contract milestones

- **M1 — milestone seam contract freeze (T1) [updated]:** the four contracts dependents/sub-streams build against:
  (a) **rubric** = four conjunctive terms: Term 1 `all_scenarios_satisfied`, Term 2 `tri_alignment`, Term 3 `ReviewVerdict`, Term 4 `IntegrityResult.Passed` (§3.2);
  (b) **decision record** = `GoNoGoDecision` schema (§3.1) written to the `factory_build` bead (D-40/D-41, §3.4), a **C20 schema-slot request** (now includes `EvidenceDiagnosisBead`/`EvidenceAllScenariosSatisfied`/`EvidenceTriAlignment`/`EvidenceIntegrityPassed`);
  (c) **inputs** = `GoNoGoInput` schema (§3.1): `DiagnosisRecord` (C32 §3.2a, keyed by `factory_build_ref`), `ReviewVerdict` (C52), `TransfusionVerdict` (C51, auxiliary), `IntegrityResult` (Term 4 harness), scenario-set id + path (I2/INV-3);
  (d) **`MilestoneConfig`** = `pass_rate_floor` pinned at 1.0 (not a knob), `min_scenarios`, `max_attempts`, `oversight_level`, `judge_self_trust_required`, `require_review_approve`, `require_factory_integrity` (§3.3).
  Freezing M1 lets WS-A build against synthetic `DiagnosisRecord` + `IntegrityResult` and WS-B against synthetic bundles in parallel; lets **C54** stub against the go/no-go output; lets C32 confirm the `DiagnosisRecord` fields C53 keys on.
- **M2 — tri-alignment gate fixed (T5/G23/ADR-0069) [renamed from "rubric + bar fixed"]:** the go/no-go is a **four-term conjunction** (Term 1–4) with `pass_rate_floor = 1.0` (pinned, not a knob). Distribution statistics (p10, mean, p90−p10) are surfaced in `DiagnosisRecord` as **diagnostic evidence to human review**, not threshold gates. `min_scenarios`, `max_attempts`, `oversight_level` are the remaining operator knobs (§3.3); `E-C53-09..E-C53-12` are the new tri-alignment codes. **Operator must confirm `judge_self_trust` precondition (PF-2) before M2 is closed.** This is the **G23 + ADR-0069 close**.
- **M3 — `factory_build` decision-slot agreed (T6) [updated]:** the `milestone_verdict` + `milestone_evidence` (extended with tri-alignment evidence fields) + `milestone_decided_at` + `diagnosis_bead_ref` fields on the `factory_build` bead (§3.4) are reconciled with C51/C52/C32 slots (OQ-4 resolved — D-40/D-41 fix #2). `status` terminal = `closed` (D-41 fix #2, not `completed`). C20 accepts the schema-slot request (now four fields) and bumps the bead-type version before any bead-write. NEW SEAM (§9).

## 5. Risks & de-risking order

1. **Confirm first — G09/G23 bar ownership + value (T5/OQ-1).** Verify the satisfaction cutline is **applied
   at C53** (reading (b)), not pushed into C33 (which stays threshold-free), and that its **value** is
   operator/integrator policy (shared with C33:OQ-1, C51:OQ-C51-3, C50). A wrong call here mis-places a
   values-decision inside the metric (anti-P6) or hard-codes a number v4 deliberately leaves open. Highest
   shared-policy uncertainty.
2. **Confirm — the seam with C51/C52 (T1/T6/OQ-4).** C51's predicate verdict, C52's review record, and C53's
   go/no-go all attach to the same `factory_build` bead. Pin **who records what** + **grain** (one decision
   per first-component build) + the C20 slot requests *before* deep build, so the three don't collide
   (parity with C51's verdict-slot request).
3. **Confirm — fail-branch attempt bound + authorizer (T7/OQ-2).** README:519 fixes **no** attempt count and
   **no** authorizer for "add substrate before Phase 3." C53 requires *a* bound; the value + escalation
   authorizer is operator policy (relates to C56 autonomy ladder). Pin the *requirement*; defer the value to
   sweep-2.
4. **Confirm — scenario-set sufficiency (T3/OQ-3).** INV-3 requires *a* held-out set and surfaces n, but
   "how many scenarios make the bet credible" is unfixed (a too-small set can meet the bar yet be weak
   evidence). Freeze a minimum-evidence guideline at sweep-2 with C30/C51; don't over-engineer at sweep-1.
5. **Measure — bet #3 honesty.** C53 makes the bootstrap go/no-go **recorded + falsifiable**; it does **not**
   guarantee the factory can self-build. Keep the artifact thin and the residual honest (README:510 — the
   milestone *tests* the bet, it does not make the bet true).

## 6. Definition of done

**Per-component DoD [updated for tri-alignment]:** the bootstrap-validation harness (T9) passes **AC-C53-01…AC-C53-18** against a synthetic first-component decision — **four-term conjunction** (ADR-0069/D-42) including the CRITICAL tri-alignment ACs: **AC-C53-14** (all four terms met → go), **AC-C53-15** (100% pass + misaligned → no-go), **AC-C53-16** (sub-100% → no-go regardless), **AC-C53-17** (judge-uncalibrated → no-go), **AC-C53-18** (post-deploy integrity fail → no-go); plus scenario-set required (AC-C53-02, E-C53-01), evidence-floor enforced (AC-C53-03, E-C53-03), conjunction both ways (AC-C53-04..07), hard error on missing inputs (AC-C53-08, E-C53-02), attempt-bound escalation (AC-C53-09, E-C53-07), evidence-anchored record (AC-C53-10, INV-4), Phase-3 arm (AC-C53-11), no model call (AC-C53-12, INV-2), oversight-only relaxation (AC-C53-13). C53 is a thin milestone artifact, not a control loop.

**Pre-condition on T5 (operator checkpoint) [updated]:** The operator MUST confirm the PF-2 judge-trust precondition (`judge_self_trust_required`) and the `oversight_level` before T5 is closed as done. The distribution rule-shape sign-off (the prior `p10 AND mean` question) is superseded — the gate is now `all_scenarios_satisfied = true` AND `tri_alignment = aligned` (boolean, not threshold). The governance checkpoint is now: confirm that `judge_self_trust_required = calibrated` and that the judge has passed a human-audited calibration sample (PF-2), or that `oversight_level = full` is in force as the fallback. This is a governance item, not a CI gate.

**Per-task DoD (tri-alignment deepening update):**
- T1: M1 contracts (`GoNoGoInput` + `GoNoGoDecision` + `ReviewVerdict` + `IntegrityResult` schemas, §3.1; `MilestoneConfig` pinned/relaxable knobs, §3.3; bead-slot table with `diagnosis_bead_ref`, §3.4) written + agreed.
- T3: absent scenario set → E-C53-01 / AC-C53-02 green.
- T4: `DiagnosisRecord` + `ReviewVerdict` + `TransfusionVerdict` + `IntegrityResult` read as pre-computed signals; distribution stats read as evidence inside `DiagnosisRecord` (not gate inputs); no scoring (AC-C53-12).
- T5: four-term conjunction (AC-C53-14..18 for critical tri-alignment paths; AC-C53-04..07 for existing conjunction checks); `pass_rate_floor = 1.0` confirmed pinned; n-floor checked via `DiagnosisRecord` coverage (AC-C53-03); **PF-2 judge-calibration precondition confirmed or oversight_level = full enforced**.
- T6: `GoNoGoDecision` written to `factory_build` bead with all four evidence fields (AC-C53-10 / INV-4); bead status = `closed` (D-41 fix #2); E-C53-02 surfaces on missing input.
- T7: `AttemptBoundReached = true` + `EscalationRequired = true` when `AttemptNo >= MaxAttempts` (AC-C53-09 / E-C53-07).
- T8: `go` arms / `no_go` withholds Phase-3 transition (AC-C53-11).
- T10: `IntegrityResult` populated from factory-baseline run after component integration; wired into T5's Term 4 check (E-C53-12 / AC-C53-18).
- T9: full AC-C53-01..18 suite green; E-C53-01..12 all exercised; **must pass before Phase 3 is armed**.

**OQ-5 open (see spec §9):** `IntegrityResult` ownership and harness scope (T10 owner TBD: C52 or new integrity harness). All four Sweep-2 OQs remain resolved; OQ-5 is the one new open question introduced by the tri-alignment deepening.
