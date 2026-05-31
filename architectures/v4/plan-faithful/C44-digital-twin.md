# C44 — Digital Twin (per service)  (Build Plan, canonical track)

> Source / Spec ref: spec/C44-digital-twin.md

## 1. Work breakdown

C44 is a **per-service template**, instantiated once per twinned dependency (README:468 "Repeat per
dependency"). The tasks below build (a) the **template** — the LocalStack-shaped assembly pattern + the C17
tool-node packaging — and (b) the **first concrete twin** that proves it. Re-running T7–T9 per dependency is
the steady-state.

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the twin contract surface (M1)** — the **cloned-surface declaration** schema (I2) + the **fidelity-observation seam** (I8) + the **isolation-ready call surface** (I1). This is the contract C45 (fidelity) and C43 (isolation) build against; freezing it unblocks both siblings. | S | C17 tool-node ABI; coordinate I2/I8 with C45, I1/I2 with C43 |
| T2 | **C17 tool-node packaging skeleton** — package the twin as a Gas City **C17 tool node** (per-twin Go binary, README:202) over the C02 ABI; the per-twin `[[service]]` block + config surface (I7) per C03 (service id, fixture source, OpenAPI ref, mode precedence, reset policy, capture-vs-serve). **No Gas City Go import; no custom twin framework** (INV-4). | S | C17/C02 ABI, T1 |
| T3 | **Record/replay layer (I3)** — wire an off-the-shelf record/replay engine (go-vcr/HoverFly/VCR.py per dep language) as the replay tier; serve recorded fixtures for matching requests; offline capture-mode populates fixtures from real traffic (the **only** production-touching path, INV-2). | M | T2; chosen engine (OQ-5) |
| T4 | **Stateful-mock layer (I4) + session-state lifecycle (I6)** — wire an off-the-shelf stateful mock (WireMock/Mountebank/Mockoon); custom-logic responses over evolving session state; init-from-seed, mutate-in-run, **reset between runs/scenarios** (INV-3). | M | T2; chosen engine (OQ-5) |
| T5 | **OpenAPI-driven mock layer (I5)** — wire an OpenAPI mock (Prism/Stoplight) against the vendored service spec; on-contract synthetic responses as the in-scope **fall-through** (INV-1). | M | T2; vendored OpenAPI spec |
| T6 | **Three-mode precedence resolver (INV-1) + scope check (I2/INV-5)** — resolve **replay→stateful→OpenAPI**; gate every request on the declared cloned surface, returning explicit out-of-scope for un-cloned requests (never faked). The one piece of genuine glue (everything else is off-the-shelf). | M | T3, T4, T5; OQ-2 (match/merge rule) |
| T7 | **Instantiate the first concrete twin (per-dependency)** — pick a dependency; declare its cloned surface (I2) from its OpenAPI/SDK contract; capture fixtures (T3); seed stateful state (T4); vendor its OpenAPI spec (T5); transfuse the **LocalStack** assembly pattern + record `transfused_from` (C51). | M | T3–T6, C51 |
| T8 | **Fidelity-observation seam impl (I8)** — emit the twin's request/response trail + a real-vs-twin diff seam for **C45** to consume; surface OpenAPI-fall-through events (low-fidelity-risk indicator). **C44 asserts no fidelity verdict** (G22 → C45). | S | T6, T1 (M1 seam frozen) |
| T9 | **Per-twin conformance harness (AC-1…AC-8)** — drive the twin with the **real dependency made unreachable** (the AC-6 isolation-prerequisite proof); exercise three-mode precedence, statefulness, reset, declared-surface honesty. Re-runnable per instantiated twin (the template). | L | T3–T8 |

## 2. Dependency graph

**Must precede C44:**
- **C17** (tool-node abstraction — the twin is exposed as a C17 tool node) + transitively **C02** (pack/tool-node ABI).
- **C03** (config/feature-flag model — the `[[service]]` block that gates + configures a twin).
- **C51** (gene-transfusion discipline — the twin transfuses LocalStack + records `transfused_from`).
- Off-the-shelf engines available + license-vetted (record/replay, stateful-mock, OpenAPI-mock; hygiene → C57).

**C44 must precede (its same-batch consumers):**
- **C45** twin fidelity — verifies this twin against the real service (G22); consumes I2 (cloned surface) + I8 (fidelity seam).
- **C43** isolation/lethal-trifecta boundary — isolates the agent behind this twin (G31, **D-13**); consumes I1 (call surface) + I2 (cloned surface).
- **C30/C31** scenarios run against the twin (README:195/499); C44 is the addressable run target (C31:OQ-5).

**Critical path inside C44:** T1 → T2 → (T3‖T4‖T5) → T6 → T7 → T9. The **precedence resolver + scope check
(T6)** is the load-bearing custom glue (the rest is off-the-shelf wiring); **T1 (contract-surface freeze)** is
the load-bearing *interface* task because **both** siblings (C45, C43) block on it. Note the build is
deliberately **thin**: T3/T4/T5 are *wire an existing engine*, not *write a mock engine* — the keep is the
assembly + contract surface, not the mocking (THE BAR).

## 3. Parallelization

Once **T1 (contract freeze)** and **T2 (tool-node skeleton)** land, the three twin modes fan out concurrently:
- **WS-A (replay):** T3 — record/replay engine + capture-mode. Independent; needs only fixtures.
- **WS-B (stateful):** T4 — stateful-mock engine + session-state lifecycle/reset. Independent; needs seed state.
- **WS-C (OpenAPI):** T5 — OpenAPI mock against the vendored spec. Independent; needs the OpenAPI spec.

T6 (precedence resolver + scope check) **joins A/B/C**. T8 (fidelity seam) can build against the T1-frozen I8
**in parallel** with T6 (it only needs the request/response trail shape). T7 (first concrete twin) is a
per-dependency instantiation that consumes A/B/C + T6. T9 (conformance harness) joins all.

**Cross-component parallelism:** because **M1 freezes I1/I2/I8 first (T1)**, **C45 (fidelity)** and **C43
(isolation)** can build against the frozen contract surface **concurrently with C44's internals** — C45 against
the I8 seam, C43 against the I1/I2 substitution surface — rather than waiting for a finished twin.

## 4. Interfaces-first / contract milestones

- **M1 — twin contract-surface freeze (T1):** the three contracts the siblings build against:
  (a) **cloned-surface declaration** (I2) — the named in-scope slice the twin promises,
  (b) **fidelity-observation seam** (I8) — the request/response + real-vs-twin diff seam **C45** consumes,
  (c) **isolation-ready call surface** (I1) — the real-dependency-shaped surface **C43** substitutes + confines behind.
  Freezing M1 lets C45 and C43 build in parallel and pins that **C44 carries no fidelity bar (G22→C45) and no
  enforcement teeth (G31→C43)**.
- **M2 — three-mode precedence + scope rule frozen (T6/OQ-2):** replay→stateful→OpenAPI ordering + the
  declared-surface gate, before C45 reasons over twin behavior (the precedence affects what "fidelity" means).
- **M3 — per-twin packaging schema frozen (T2/T7/OQ-4):** the `[[service]]` block + fixture/cassette format +
  OpenAPI-spec vendoring, before twins are instantiated per dependency at scale.

## 5. Risks & de-risking order

1. **Spike first — the LocalStack-shaped assembly is viable for a real dependency (T6+T7 thin slice).** Prove
   one dependency's declared surface can be served by **replay→stateful→OpenAPI** composition with the **real
   service unreachable** (AC-1/AC-6). This retires the single highest-value uncertainty v4 itself flags — "the
   most labor-intensive principle … no turnkey OSS for 'twin a service from its SDK'" (README:204) — and proves
   the keep (assembly + contract surface) without building a framework.
2. **Confirm — the off-the-shelf engines compose (T3+T4+T5).** Validate that a record/replay engine, a stateful
   mock, and an OpenAPI mock can sit behind one precedence resolver for one service without reimplementation
   (THE BAR: if any mode tempts a custom engine, flag it). Engine choice is per-dependency-language (OQ-5).
3. **Freeze early — the contract surface (T1/M1)** so **C45 (fidelity)** and **C43 (isolation)** unblock; a late
   I2/I8/I1 freeze serializes the whole Digital-Twins + isolation slice of Batch 4.
4. **Confirm — reset/state-isolation under concurrent scenarios (T4/OQ-3)** so "thousands per hour" repeatable
   runs (README:195) are deterministic; interacts with C42 run isolation.
5. **Confirm the deferrals hold (G22→C45, G31→C43, D-13):** C44 provides the twin + seams and asserts **no**
   fidelity verdict and **no** blast-radius bound. C45/C43 are now **on disk (sweep-1) and accept these seams**
   (C45 owns the fidelity predicate, not the twin; C43 owns the blast-radius bound + twin-by-default routing) —
   so the residual is the **sweep-2 shape freeze**, not a missing owner. The gap must still **not** silently
   fall back into C44 if a later sweep narrows either sibling (OQ-1).

## 6. Definition of done

**Per-component DoD:** the per-twin conformance harness (T9) passes **AC-1…AC-8** for the first concrete twin
against the **real dependency made unreachable** — twin answers on-contract via replay→stateful→OpenAPI
precedence, record/replay + stateful + OpenAPI-fall-through all work, deterministic + reset between runs,
declared-surface honesty (explicit out-of-scope, never faked), delivered as a **C17 tool node** (per-twin Go
binary + `[[service]]` block, **no Gas City Go import, no custom twin framework**), LocalStack transfusion
recorded (`transfused_from`, C51). **AC-9 (fidelity seam exposed) and AC-10 (isolation seam exposed) are
satisfied as *seams*, with the verdicts owned by C45 and C43 respectively.**

**Per-task DoD:**
- T1: M1 contracts written + agreed with C45 (I2/I8) and C43 (I1/I2) owners; both siblings can build against stubs.
- T2: twin boots + is invoked as a C17/C02 tool node via its `[[service]]` block; no Gas City Go import (AC-8).
- T3: a recorded fixture is served on match; capture-mode records real traffic offline (AC-2); serve-path never reaches production (contributes AC-6).
- T4: a multi-step interaction is stateful within a run and resets between runs (AC-3/AC-5).
- T5: an in-scope request with no fixture/rule returns an on-contract synthetic response (AC-4).
- T6: replay→stateful→OpenAPI precedence holds; out-of-scope requests return an explicit not-cloned signal (AC-1/AC-7).
- T7: one concrete twin instantiated for a real dependency; LocalStack transfusion recorded (C51); fixtures + OpenAPI spec version-pinned with the twin.
- T8: the fidelity-observation seam (I8) emits the request/response + diff seam C45 consumes; **C44 asserts no fidelity verdict** (AC-9, G22→C45).
- T9: full AC-1…AC-8 suite green with real dependency unreachable; harness re-runnable per instantiated twin; **must pass before C45 verifies fidelity and C43 isolates behind the twin**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (G22/G31 cross-component seams —
C45 fidelity bar + C43 isolation, both **on disk sweep-1 and confirming this attribution**; residual = the
sweep-2 shape freeze; D-13), OQ-2 (three-mode precedence + match/merge rule),
OQ-3 (session-state + reset granularity / concurrent-scenario isolation), OQ-4 (`[[service]]` TOML + fixture/
cassette schema), OQ-5 (record-replay + stateful + OpenAPI engine choice per twin / per SDK language).
