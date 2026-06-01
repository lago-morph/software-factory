# C53 — Bootstrap-validation milestone  (Build Plan, canonical track)

> Source / Spec ref: spec/C53-bootstrap-validation.md
>
> **Sweep-2 update (2026-06-01):** Tasks T1–T9 retained verbatim (Sweep-1 WBS is correct). Updated task descriptions to reflect: concrete `decide()` signature (§3.1), `GoNoGoInput`/`GoNoGoDecision` schemas, `MilestoneConfig` knobs (§3.3), D-40 bead-slot assignment (§3.4), E-C53-01..08 error taxonomy (§8.1), AC-C53-01..13 acceptance test codes (§8.2). All four OQs resolved; no WBS restructuring needed. Critical-path unchanged: T1→T4→T5→T6→T8→T9. M1/M2/M3 contract milestones retain meaning; M1 now includes the `GoNoGoInput`/`GoNoGoDecision` schemas as the freeze artifacts.
>
> **Operator-judgment flag (OQ-1 resolved):** Before T5 (rubric evaluation) can be signed off, the operator MUST review and approve the decision-rule SHAPE (`p10 >= T_tail AND mean >= T_central`) as a morning-review item. This is a governance checkpoint, not a build step. It is a pre-condition on T5 completion and on the Phase-3 arm (T8).

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the milestone seam contract (M1)** — the **rubric** (I1: C51 predicate-pass ∧ C33 satisfaction ≥ bar ∧ C52 review-approve), the **decision-record** shape (I4: `go`/`no-go` + evidence bundle = C51 verdict ref, C33 distribution snapshot + scenario-set id + sample count, C52 review ref), and the **inputs it reads** (C51 verdict, C33 distribution, C30 scenario set, C52 review). This is the contract C54 (Phase-3 transition) builds against. | S | C51 predicate verdict shape, C33 distribution output, C52 review record, C30 scenario manifest |
| T2 | **Milestone artifact skeleton + config surface** — package C53 as the Phase-2-closing milestone evaluated with the eval/bootstrap pack; config (the **satisfaction bar value + decision rule**, the **fail-branch attempt bound**, which rubric terms gate) per C03 model. **No model call / no scorer** (the bar). | S | C02/C17 ABI, C03 config model, T1 |
| T3 | **Scenario-set precondition check (I2/INV-3)** — confirm the first factory-built component ships a **held-out scenario set** in C30's corpus (`scenarios/<component>/`); absence ⇒ automatic **no-go (insufficient-evidence)**. Reads C30; owns no corpus. | S | T1, C30 corpus + manifest |
| T4 | **Evidence read (I1/INV-2)** — pull the **C51 predicate verdict** (completeness), the **C33 satisfaction distribution** + **sample count** (run by C31, judged by C32), and the **C52 design-review record**. Pure read of pre-computed signals — no scoring. | M | T1, C51 verdict, C33 output, C52 record |
| T5 | **Rubric evaluation + bar application (I1/I3/INV-5)** — evaluate the **conjunction** (C51 pass ∧ C33 ≥ milestone bar ∧ C52 approve); **apply the satisfaction cutline here** to C33's distribution (the cutline C33/C51 defer to this decision site). Bar **value** is config/operator policy (OQ-1), not hard-coded. Surface n (sample-honesty, inherits C33:INV-4). | M | T2, T4 |
| T6 | **Decision record emit (I4/INV-4)** — write **`go`/`no-go`** + the **evidence bundle** to the first component's **`factory_build` bead** (C20/C19), attributed (C41), auditable/reconstructable. | S | T5, C20 slot, C19 write, C41 attribution |
| T7 | **Fail-branch escalation (I5, README:519)** — on **no-go**: name **iterate-spec + re-run** (C52); after a **bounded** attempt count still failing → escalate to **"add more substrate before Phase 3"** (AI-CONTEXT:619). Re-evaluate fresh builds; record each decision. Attempt bound + authorizer = config/operator policy (OQ-2). | S | T5, T6, C52 re-run |
| T8 | **Phase-3 arming output (I4 → C54)** — surface the decision so **C54 arms** (on `go`, README:436) or **withholds** (on `no-go`, README:519) the Phase-2 → Phase-3 transition. | S | T6 |
| T9 | **Bootstrap-validation harness (AC-1…AC-10)** — synthetic first-component decision driver: seed a C33 distribution (above/below bar, small-n), a C51 verdict (pass/fail/inconclusive), a scenario set (present/absent), a C52 review (approve/reject); drive all ACs — falsifiable conjunction over named evidence, absent-scenarios⇒no-go, bar-applied-and-configurable, recorded+auditable, fail-branch, no-second-scorer, one-time. | L | T3–T8, synthetic input fixtures |

## 2. Dependency graph

**Must precede C53:**
- **C52** (the self-bootstrap loop that runs the first component + owns the human design-review record C53 reads).
- **C33** (the satisfaction distribution C53 applies its bar to — threshold-free, defers the cutline to C53).
- **C51** (the transfusion-correctness predicate verdict C53 consumes as the objective half of "if it works").
- **C30/C31/C32** (the held-out scenario set + the run/judge tier that produces the scores C33 reduces).
- **C20/C19** (the `factory_build` bead + store the go/no-go decision is recorded on) + **C41** (attribution) + **C02/C03** (pack + config to host/configure the milestone).

**C53 must precede (its decision arms/withholds the next phase):**
- **C54** Phase delivery plan — the **Phase-2 → Phase-3 transition** reads C53's go/no-go (README:436/519).

**Critical path inside C53:** T1 → T4 → T5 → T6 → T8 → T9. The load-bearing task is **T5 (rubric
evaluation + bar application)** — but note it is *thin*: it composes pre-computed signals (C51/C33/C52),
applies a **configurable** cutline (no hard-coded number, OQ-1), builds **no** scorer, and owns **no**
durable state beyond the decision record (C53 is a re-derivable decision over upstream signals). The
**G23-closing tasks** are **T3 (scenario-set precondition)** + **T5 (rubric/bar)** + **T7 (fail branch)** —
the three that together replace "looks good to a human" with a recorded, falsifiable bar; all three are
deliberately scoped to *avoid* new capability (no second engine; no metric change; no loop).

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

- **M1 — milestone seam contract freeze (T1):** the three contracts dependents/sub-streams build against:
  (a) **rubric** = the conjunction terms (C51 / C33 / C52) + the decision rule (`p10 >= T_tail AND mean >= T_central`, §3.2);
  (b) **decision record** = `GoNoGoDecision` schema (§3.1) written to the `factory_build` bead (D-40, §3.4), a **C20 schema-slot request**;
  (c) **inputs** = `GoNoGoInput` schema (§3.1): C51 verdict ref, C33 `SatisfactionDistribution` + scenario-set id + n, C52 review ref.
  Freezing M1 lets WS-A build against synthetic `GoNoGoInput` and WS-B against synthetic bundles in parallel, and
  lets **C54** stub against the go/no-go output to wire its Phase-3 transition.
- **M2 — rubric + bar fixed (T5/G23/G09):** the go/no-go is a **falsifiable conjunction** (`p10 >= T_tail AND mean >= T_central AND C51 pass AND C52 approve`) with operator-policy knobs `tail_threshold`, `central_threshold`, `min_scenarios` (§3.3); `E-C53-03 / E-C53-04` are the bar-not-met codes. **Operator must sign off on the SHAPE before M2 is closed** (§3.1 OPERATOR-JUDGMENT FLAG / OQ-1 resolved). This is the **G23 close**.
- **M3 — `factory_build` decision-slot agreed (T6):** the `milestone_verdict` + `milestone_evidence` + `milestone_decided_at` fields on the `factory_build` bead (§3.4) are reconciled with **C51's predicate-verdict slot + C52's review-record slot** (OQ-4 resolved — D-40). C20 accepts the schema-slot request and bumps the bead-type version before any bead-write. NEW SEAM (§9).

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

**Per-component DoD:** the bootstrap-validation harness (T9) passes **AC-C53-01…AC-C53-13** against a
synthetic first-component decision — **falsifiable rubric** (G23) as a **conjunction over named evidence**
(`p10 >= T_tail AND mean >= T_central AND C51 pass AND C52 approve`), **scenario-set required**
(AC-C53-02, E-C53-01), **evidence-floor enforced** (AC-C53-03, E-C53-03), **conjunction both ways**
(AC-C53-04..07, E-C53-04..06), **hard error on missing inputs** (AC-C53-08, E-C53-02), **attempt-bound
escalation** (AC-C53-09, E-C53-07), **evidence-anchored record** (AC-C53-10, INV-4), **Phase-3 arm**
(AC-C53-11), **no model call** (AC-C53-12, INV-2), **configurable knobs** (AC-C53-13, INV-5). C53 is a
thin milestone artifact, not a control loop.

**Pre-condition on T5 (operator checkpoint):** The operator MUST review and sign off on the decision-rule
SHAPE (`p10 >= T_tail AND mean >= T_central`) before T5 is closed as done. This is a governance item, not
a CI gate. It is the only morning-review item C53 introduces (see §3.1 OPERATOR-JUDGMENT FLAG, OQ-1 resolved).

**Per-task DoD (Sweep-2 — references updated to E/AC codes):**
- T1: M1 contracts (`GoNoGoInput` + `GoNoGoDecision` schemas, §3.1; `MilestoneConfig` knobs, §3.3; bead-slot table, §3.4) written + agreed; sub-streams + C54 can stub against them.
- T3: absent scenario set → E-C53-01 / AC-C53-02 green.
- T4: C51 verdict + C33 `SatisfactionDistribution` + n + C52 record read as pre-computed signals; no scoring (AC-C53-12).
- T5: rubric conjunction (AC-C53-04..07); bar applied and configurable (AC-C53-13); n-floor checked (AC-C53-03); **operator shape sign-off obtained**.
- T6: `GoNoGoDecision` written to `factory_build` bead with all evidence refs (AC-C53-10 / INV-4); E-C53-02 surfaces on missing input.
- T7: `AttemptBoundReached = true` + `EscalationRequired = true` when `AttemptNo >= MaxAttempts` (AC-C53-09 / E-C53-07).
- T8: `go` arms / `no_go` withholds Phase-3 transition (AC-C53-11).
- T9: full AC-C53-01..13 suite green; E-C53-01..08 all exercised; **must pass before Phase 3 is armed**.

**All four OQs resolved at Sweep-2** (see spec §9 for resolution text and §3.1/§3.2/§3.3/§3.4 for the settled contracts). No open questions deferred from Sweep-2.
