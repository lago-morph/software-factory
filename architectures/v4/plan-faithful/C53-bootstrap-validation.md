# C53 — Bootstrap-validation milestone  (Build Plan, canonical track)

> Source / Spec ref: spec/C53-bootstrap-validation.md

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
  (a) **rubric** = the conjunction terms (C51 / C33 / C52) + the decision rule;
  (b) **decision record** = `go`/`no-go` + evidence bundle (the `factory_build` bead slot, a **C20 request**);
  (c) **inputs** = C51 verdict ref, C33 distribution + scenario-set id + n, C52 review ref.
  Freezing M1 lets WS-A build against synthetic evidence and WS-B against synthetic bundles in parallel, and
  lets **C54** stub against the go/no-go output to wire its Phase-3 transition.
- **M2 — rubric + bar fixed (T5/G23/G09):** the go/no-go is a **falsifiable conjunction over named
  evidence** with the **satisfaction cutline applied at C53** (configurable value, OQ-1), before C54 reasons
  over the decision. This is the **G23 close** at sweep-1 altitude.
- **M3 — `factory_build` decision-slot agreed (T6):** the go/no-go decision slot on the `factory_build`
  bead is reconciled with **C51's predicate-verdict slot + C52's review-record slot** (one decision per
  first-component build, grain agreement — OQ-4) as **C20 schema-slot requests**, before any bead-write.

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

**Per-component DoD:** the bootstrap-validation harness (T9) passes **AC-1…AC-10** against a synthetic
first-component decision — **falsifiable rubric** (not "looks good", G23) computed as a **conjunction over
named evidence** (C51 pass ∧ C33 ≥ bar ∧ C52 approve), **scenario-set required** (absent ⇒ no-go), **no
model call / no scorer** (reads pre-computed signals), the **satisfaction cutline applied at C53** with a
**configurable** value (G09 reading (b)), the **decision recorded + auditable** on the `factory_build` bead,
a defined **fail branch** (iterate + re-run → add-substrate), the decision **arming/withholding Phase 3**
for C54, **engine-reuse** (composes C30/C31/C32/C33 + C51, no second evaluation engine/significance test),
and **one-time** (fires once; subsequent components gated by C51/C52, steady-state by C50/C39). C53 is a
thin milestone artifact, not a control loop.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C51/C52/C33/C30/C54 owners; sub-streams + C54 can stub against them.
- T3: a component with no held-out scenario set yields **no-go (insufficient-evidence)** (AC-2).
- T4: C51 verdict + C33 distribution + n + C52 record read as **pre-computed signals**; no scoring (AC-3).
- T5: rubric evaluates as a **conjunction** (AC-1/AC-6); **bar applied here**, configurable value (AC-4); n surfaced.
- T6: go/no-go + evidence bundle **recorded** on `factory_build` bead, attributable, reconstructable (AC-5).
- T7: no-go → **iterate + re-run**; bounded repeated failure → **add-substrate** escalation (AC-7).
- T8: `go` **arms** / `no-go` **withholds** the Phase-2 → Phase-3 transition for C54 (AC-8).
- T9: full AC suite green; **must pass before Phase 3 is armed** (C54 reads C53's decision as the gate).

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G09/G23 bar value + decision
rule + cutline ownership at C53, shared C33/C51/C50), OQ-2 (fail-branch attempt bound + "add substrate"
authorizer, relates C56), OQ-3 (bootstrap scenario-set sufficiency / minimum-evidence guideline with
C30/C51), OQ-4 (C52/C51/C53 `factory_build`-bead slot ownership + grain agreement, C20 schema-slot requests).
