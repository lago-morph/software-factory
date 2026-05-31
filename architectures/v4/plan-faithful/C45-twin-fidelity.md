# C45 — Twin contract & fidelity verification  (Build Plan, canonical track)

> Source / Spec ref: [C45 spec](../spec/C45-twin-fidelity.md)
> Track: canonical   Status: sweep-1

C45 is the **twin-fidelity invariant** (inventory kind): it defines the **"how close is close enough" bar**
(**G22**) and wires the two verifications that assert it — **twin-usage-vs-service-promises** (contract,
README:201) and **twin-behavior-vs-real-service** (behaviour, README:499). It is **not** a service, a twin,
or a new test framework: the contract check (Pact/schemathesis/Prism) and the behaviour diff (record/replay)
are **mature stack OSS** that C45 *invokes* (README:199/201, AI-CONTEXT:343–344); the **only custom code is
the fidelity predicate + the combine-and-gate wiring** — the one thing v4 says has "**None turnkey / DIY**"
(AI-CONTEXT:347). The plan is correspondingly small; the load-bearing work is **defining the per-service
fidelity predicate (G22)** and **freezing the verdict feed** that C31/C43/C57/C53 consume, plus retiring two
uncertainties — the **reference-capture/drift** question (OQ-C45-2) and the **probe run-target** seam
(OQ-C45-3, mirrors C31:OQ-5). Per AI-CONTEXT:487 twins are built **just-in-time per dependency**, so C45 is
instantiated **per twinned service**, not once globally.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Define the fidelity predicate — the G22 bar (the custom KEEP).** Per-service predicate over **named dimensions** (exact: contract/error-taxonomy/schema/auth; bounded: latency/ordering/numeric/omission) + the C30 probe corpus + the pass rule → `fidelity_pass\|fidelity_fail`. This is "how close is close enough" (G22; AI-CONTEXT:347). (Spec §3.1, §4.1) | M | C44 twin contract/OpenAPI; C30 probe corpus shape |
| **T2** | **Wire the contract-verification check (usage-vs-promises, README:201).** Adapter that runs **Pact/schemathesis** (or **Prism** OpenAPI conformance) of the twin vs the real service contract → per-dimension contract-conformance result. *Stack tool; C45 owns the wiring + result mapping.* (Spec §3.2, §4.3) | S | C44 service contract |
| **T3** | **Wire the behavioural-fidelity check (twin-vs-real, README:499).** Drive the C30 probe corpus at the twin, diff responses vs the **recorded reference** (record/replay, README:199), score vs T1 tolerance → per-dimension behaviour-match result. (Spec §3.3, §4.3) | M | T1; C30 probes; reference corpus (OQ-C45-2) |
| **T4** | **Freeze the fidelity verdict + report feed.** Per twin × version `fidelity_pass\|fidelity_fail` + failing-dimension report as a **bead** (C19/C20), consumable by C31/C43 (substitution gate), C57 (residual register), C53 (twin-build acceptance); `fidelity_fail` → fix-task candidate (C44/C39). (Spec §3.4) | S | T1, T2, T3 |
| **T5** | **Write the version-keying + G22-residual notes.** Verdict keyed to twin/contract/reference/probe version (change ⇒ invalidate + re-verify, §4.4); residuals routed to C57 — finite-corpus-vs-environment-surface (F3/F13) + reference-drift (F55). A sweep-1 clarification, **not** a new mechanism. (Spec §4.4, §6, §8.6–8.7) | S | T4 |
| **T6** | **Author the fidelity pack + exemplars.** The Gas City pack tool node(s) (README:201/199) that run the contract check + the behaviour diff + the predicate combine; pass and fail (per-dimension-breach) negative examples; one starter predicate against the **first real twin**. | M | T2, T3, T4 |
| **T7** | **Resolve reference-capture / drift OQ (OQ-C45-2).** Confirm where the recorded reference lives (C44 record/replay capture? C30 corpus? CXDB) and the **refresh cadence** that keeps it current vs the evolving real service — the one place real-service rate-limit/cost applies. | M | T3 |
| **T8** | **Resolve probe run-target seam (OQ-C45-3, mirrors C31:OQ-5).** Does C45 invoke **C31** to drive probes at the twin, or run the probe corpus directly as a pack? Confirm the C45↔C31 contract. | S | T3 |
| **T9** | **Resolve bar-default + gate-strength OQs.** OQ-C45-1 (concrete dimension catalog + default tolerances + per-service-class starter templates — the G22 residual after shape is fixed), OQ-C45-4 (is `fidelity_pass` a hard substitution gate or advisory; differ for C31 scenario-run vs F44/C43 production-default?). | M | T1, T4 |

## 2. Dependency graph

```
C44 (twin + contract) ─┐
C30 (probe corpus) ────┼─► T1 ─► {T3, T9}
                       │   T2 ─► T4
C44 (contract) ────────┴─► T2
                           T3 ─► {T4, T6, T7, T8}
                           T4 ─► {T5, T6, T9}
                           T3 ─► T7 (reference/drift) ─► review-log / C57(residual)
                           T3 ─► T8 (run-target) ─────► C31 seam
```

- **Critical path:** T1 → T3 → T4. T1 (the bar) is load-bearing — both checks and the verdict rest on it;
  T3 (behaviour check) is the longer of the two checks (it needs the reference); T4 freezes the verdict feed
  C31/C43/C57/C53 consume. T2 (contract check) is short and joins at T4. T6 (the pack) hangs off T2+T3+T4.
- **Upstream blockers:** T1/T2 need **C44's** twin + service contract/OpenAPI; T1/T3 need **C30's** probe
  corpus; T3 needs the **recorded reference** resolved (OQ-C45-2). C45 is **Batch 4** alongside C43/C44, so
  C44 must expose its twin + contract before C45's checks can run end-to-end.
- **Downstream consumers waiting on these freezes:** C31/C43 (a twin is certified for substitution only on a
  current `fidelity_pass`), C57 (the G22 residual — "Addressed" for F12/F33/F44/F56 is conditional on a
  passing verdict), C53 (twin-build acceptance), C44/C39 (a `fidelity_fail` is a fix-task against the twin).

## 3. Parallelization

- **The two checks fan out:** T2 (contract, usage-vs-promises) and T3 (behaviour, twin-vs-real) are
  independent workstreams off T1/C44 and can be built concurrently; they re-converge at T4 (verdict) and T6
  (the pack).
- **Independent once T4 lands:** T5 (version-keying + residual notes) is disjoint from the pack build and can
  be authored immediately after T4.
- **The OQ workstreams run in parallel with the contracts:** T7 (reference/drift) and T8 (run-target) only
  need T3's shape; T9 (bar-default + gate-strength) needs T1/T4. All can run alongside the T6 pack build.
- **The two long poles:** T1 (the predicate — the genuine custom artifact) and T7 (reference capture/drift —
  the one place real-service exposure re-enters). Start both as soon as their inputs land; do not let T7
  block T2/T4.
- **Cross-component parallelism:** because C45 is Batch-4 alongside C43/C44, C31/C43/C57 can build against a
  **stubbed** `fidelity_pass|fidelity_fail` verdict the moment T4 freezes, before T7/T8 resolve.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Fidelity predicate — the G22 bar (T1): named dimensions + per-dimension tolerance + probe corpus + pass rule | Both checks (what "close enough" *is*); the whole invariant |
| **M2** | Contract-verification check (T2) — usage-vs-promises via Pact/schemathesis/Prism → conformance result | The contract dimension of the verdict |
| **M3** | Behavioural-fidelity check (T3) — twin-vs-real diff vs recorded reference, scored vs tolerance | The behaviour dimension; the C45↔C31 run-target seam (T8) |
| **M4** | Fidelity verdict + report feed (T4) — `fidelity_pass\|fidelity_fail` bead | C31/C43 (substitution gate), C57 (residual register), C53 (twin-build acceptance), C39 (fix-task) |
| **M5** | Version-keying + G22-residual notes (T5) | C57 (residual register). *(Not "what C43 must enforce" — confinement is C43's boundary; C45 owns fidelity per the spec.)* |

Freeze M1 first: it is the bar both checks and the verdict rest on. M2/M3/M4 let C31/C43/C57 build against a
stubbed verdict without waiting on the T7 reference spike. M3 is the seam C31 needs if C45 delegates probe
execution to the runner (OQ-C45-3).

## 5. Risks & de-risking order

1. **(Highest) The bar is the unsolved deliverable (G22).** v4 names mature tooling for the two *checks* but
   says the *fidelity bar* has "**None turnkey / DIY**" (AI-CONTEXT:347). The risk is mis-shaping it — a
   single global similarity threshold both over- and under-constrains (a payment twin must match error
   taxonomy/idempotency exactly; a read API may tolerate omitted fields). **De-risk via T1 + T9** against the
   **first real twin (C44)**: fix the shape now (per-service predicate over named dimensions, exact vs
   bounded — spec §6 G22 Reading B), defer the concrete dimension catalog + default tolerances to T9. Get the
   *shape* right before C31/C43 trust a `fidelity_pass`.
2. **Reference drift re-introduces production exposure (OQ-C45-2, F55).** The behaviour check needs
   real-service ground truth, but a **live call in the loop** would defeat P7's "thousands/hour without rate
   limits / no production exposure" (README:195, F44/F56). The build uses a **recorded reference** (spec §6
   G22 Reading B) — but it can **drift** from the evolving real service, so a `fidelity_pass` is only as
   current as its reference. **De-risk via T7**: pin the capture home + a refresh cadence; surface stale-
   reference as a loud residual in C57. Do **not** wire a production call into the fidelity loop.
3. **Finite corpus vs unbounded environment surface (F3/F13, inherent).** A twin can pass the bar yet diverge
   on un-probed inputs; the environment surface exceeds any test set (spec §6). **De-risk by honesty, not
   scope creep** (T5): route the residual to C57 — "Addressed" for F12/F33/F44/F56 is **conditional on a
   passing verdict over a finite corpus**, not unconditional. C45 cannot make a finite corpus exhaustive and
   does not pretend to.
4. **Over-build temptation: re-building contract-testing / schema-diff / mocking tooling.** The inventory's
   "verifies … usage … and behavior" invites writing a contract-test engine or a diff library. **De-risk by
   holding the line** (T2/T3/T6): Pact/schemathesis/Prism/record-replay are **stack OSS** C45 *invokes*
   (README:199/201, AI-CONTEXT:343–344); the **only** custom code is the predicate + the combine-and-gate
   wiring (AI-CONTEXT:347). Flag any new test-framework / diff-library / mock-runtime creep at review.
5. **Confinement-vs-fidelity conflation (C43 boundary).** C45's fidelity verdict is **not** the isolation
   that keeps the agent off production — that is **C43's** lethal-trifecta boundary (G31). The risk is C45
   absorbing C43's job (or vice-versa). **De-risk via the spec split**: C45 = the twin is *faithful enough to
   substitute*; C43 = the agent is *confined to it*. Keep them distinct; the dropped `boundary_class` tag
   (SURVIVOR-PASS C43-07) is not C45's key.

## 6. Definition of done

**Per-task:** each contract task (T1–T5) is done when its spec section is frozen and a downstream consumer
(C31/C43/C57/C53) can build a stub against it; T6 is done when the fidelity pack + pass/fail exemplars + one
starter predicate against the first real twin exist; T7/T8/T9 are done when the OQ is answered in review-log
(or explicitly carried forward with owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The **fidelity bar is an explicit, per-service, written predicate** (named dimensions + tolerances + probe
  corpus + pass rule) — "how close is close enough" is auditable, not implicit; a twin with no predicate
  cannot be certified (§8.1, the G22 KEEP).
- The **contract check** (usage-vs-promises, Pact/schemathesis/Prism) yields a conformance result and **fails**
  on a request/auth/response the real contract forbids (§8.2).
- The **behaviour check** (twin-vs-real, vs recorded reference) yields a match result and **fails** on a
  tolerance breach (§8.3) — reference recorded/golden, not a live call (OQ-C45-2).
- The **two-sided pass rule** yields `fidelity_pass` only when **both** halves pass within the predicate;
  passing one while breaching the other ⇒ `fidelity_fail`; an uncertified twin is **not** sanctioned for
  substitution (§8.4).
- C31/C43/C57/C53 can consume C45's **verdict + report feed** (bead) to gate substitution, surface the
  residual, and accept a built twin; a `fidelity_fail` is a fix-task candidate (§8.5).
- **Version-keying invalidates stale certification** (twin/contract/reference change ⇒ re-verify) and the
  **G22 residuals are routed to C57** — finite-corpus-vs-environment (F3/F13) + reference-drift (F55); "Addressed"
  for F12/F33/F44/F56 is recorded as **conditional on a current passing verdict** (§8.6, §8.7).
- **No tooling-rebuild over-build** is present; the checks are stack OSS (Pact/schemathesis/Prism/record-
  replay), the only custom code is the predicate + the combine-and-gate wiring (§8.8, AI-CONTEXT:347).
- All four OQs are in review-log with owners (OQ-C45-1 → C45 + first real twin C44, the G22 bar default;
  OQ-C45-2 → C45 + reference-capture owner C44/C30/CXDB; OQ-C45-3 → C45 + C31; OQ-C45-4 → C45 + C43 + operator
  policy).
