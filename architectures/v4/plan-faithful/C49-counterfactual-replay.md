# C49 — Counterfactual Replay Driver  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C49-counterfactual-replay.md`](../spec/C49-counterfactual-replay.md)
> Sequencing (binding): **built last — Phase 3d**, after Layers 1–5 are solid (README:278, 470), **heaviest
> human review** (README:470). Depends only on **C21** (inventory); runs **behind C43 + against C44 twins**
> (D-13); fed by **C47** (variant) → feeds **C48** (comparison) → **C50** (gate).
> **G19 framing (binding):** v4 admits this is "**largely unsolved**" (AI-CONTEXT §12). This plan builds the
> **tractable-now slice** (`deterministic-tool-replay`) and **defers** the unsolved core (full LLM-step
> counterfactual) as an explicit research bet — it does **not** schedule a "solve G19" task.

## 1. Work breakdown

Sweep-1 plan: name the tasks, their order, and where the contract freezes — not implementation detail. Tasks
are ordered to **prove the cheap/safe parts first** and **isolate the unsolved part last**.

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| **T0 — Contract freeze (interfaces-first)** | Freeze the C49 contract surface against the spec: I1 replay-request (trajectory+midpoint+variant), I5 paired-result record, **I6 fidelity-tag taxonomy** (`deterministic-tool-replay` vs `counterfactual-reexecution`). Publish so C47/C48 can build against stubs. | S | C21 I5/I6 frozen; spec §3 |
| **T1 — Branch-at-midpoint over C21 I5** | Implement I2: given (trajectory, turn T), invoke C21 I5 to O(1)-fork a branch rooted at T (INV-1/INV-2). The low-risk, primitive-driven core. | S | T0; **C21 I5/INV-3** |
| **T2 — Variant binding (I3)** | Bind a variant spec onto the branch at T: substitute prompt (C09) / model-route (C29) / hyperparam / workflow step (C12). | M | T0, T1; C47 variant-spec shape (OQ-4) |
| **T3 — Deterministic-tool replay engine (I4, `deterministic-tool-replay`)** | Re-execute forward from T for continuations touching **only deterministic tool nodes + twin-served deps**; reproduce original outcome (INV-5) and produce a clean variant diff. **The tractable-now KEEP.** | M | T1, T2; **C44 twins**, **C43 routing** |
| **T4 — Isolation + fail-closed guard (INV-4)** | Wire re-execution behind **C43** (twin-by-default routing); route all external calls to **C44 twins**; **fail closed** on any non-twinnable external effect (never touch production). The security de-risker. | M | T3; **C43** (D-13), **C44** |
| **T5 — Paired-outcome result + fidelity stamping (I5/I6)** | Emit (original, variant) outcome over T in a C48-comparable / C32-C33-scorable shape; stamp the fidelity tag (INV-3). | S | T0, T3 |
| **T6 — Best-effort LLM-counterfactual path (`counterfactual-reexecution`)** | Re-execute continuations involving **LLM steps**: produce a result **labeled best-effort**, with a repeat-N variance estimate; **claim no reproduction** (INV-3). **Built last; heaviest human review.** | L | T3, T4, T5; **OQ-1 open** |
| **T7 — Integration pack + acceptance suite** | Package as a Gas City pack/tool node(s) (C02/C17), feature-gated with P12; drive the spec's AC-1…AC-8 against pinned C21 + a C44 twin behind C43. | M | T1–T6 |

## 2. Dependency graph

**Inbound (must precede C49 — C49 is the last leaf, Batch 5 / Phase 3d):**
- **C21** (sole inventory dep) — I5 O(1) branch + I6 replay must be frozen and conformance-passing (C21 AC-4).
- **C44 twins** + **C43 isolation** — must exist (Phase 3c / D-18) so re-execution has reconstructable external
  state and a blast-radius bound. C49 cannot safely re-execute before these.
- **C47** (variant in) and **C48** (comparison out) — the producer/consumer C49 sits between; their seams
  (OQ-4) freeze jointly.

**Critical path inside C49:** `T0 → T1 → T2 → T3 → (T4, T5) → T6 → T7`. The **load-bearing milestone is T3**
(the deterministic slice actually reproduces + compares) — it is the proof C49 delivers *real* value for the
tractable partition. **T6 is deliberately last and gated on OQ-1**; it is the research bet, not a blocker for
T0–T5 shipping.

**Outbound (C49 gates these — but they are siblings in the same Batch-5 wave):** C48 (consumes paired results),
C50 (gate over C48's verdict). C49 gates *nothing foundational* — its failure or deferral does not block the
factory's build/heal loops (spec AC-8).

## 3. Parallelization

Independent workstreams that can run concurrently once **T0 (contract freeze)** lands:
- **Stream A — primitive path:** T1 (branch) → T3 (deterministic replay) → T5 (result). The cheap, high-value
  spine; depends only on C21 + C44/C43.
- **Stream B — variant binding:** T2 (variant injection onto the branch) — can be built against a C47 stub once
  the variant-spec shape (OQ-4) is agreed; merges into T3.
- **Stream C — isolation guard:** T4 (C43/C44 wiring + fail-closed) — built against the C43/C44 specs (already
  on disk) in parallel with Stream A; merges before T7.
- **Stream D (deferred, serialized last):** T6 (LLM-counterfactual) — **not parallelized in**; it waits on
  T3/T4/T5 and on OQ-1's research outcome, and gets isolated review.

Fan-out is modest (C49 is a single driver, not a subsystem). The real parallelism is **interfaces-first**: T0
unblocks C47 and C48 to build against C49 stubs while C49's own engine is implemented.

## 4. Interfaces-first / contract milestones

Freeze early so siblings build against stubs in parallel:
- **M0 — C49 contract (T0):** I1 request shape, I5 paired-result record, **I6 fidelity-tag taxonomy**. This is
  the contract C47 (producer) and C48 (consumer) bind to. **Freeze first.**
- **M1 — Branch seam (T1):** the exact use of C21 I5 (fork-at-T handle) — frozen jointly with C21.
- **M2 — Variant-injection + result schema (T2/T5):** joint freeze with **C47** (variant spec) + **C48**
  (comparison contract) — **OQ-4**.
- **M3 — Isolation contract (T4):** how C49 invokes C43 routing + C44 twins + the fail-closed rule — against
  the on-disk C43/C44 specs (D-13).
- **M4 — Fidelity/trust threshold (T6):** the *open* milestone — when a `counterfactual-reexecution` result is
  trustworthy enough to feed C48/C50 — **deferred to the research bet (OQ-1)**; this plan does NOT pretend to
  freeze it at Sweep-1.

## 5. Risks & de-risking order

Prototype/spike in this order — **retire the cheap/safe uncertainty first, isolate the unsolved core last:**
1. **Spike T1 (branch-at-midpoint):** confirm C21 I5 forks at an arbitrary midpoint turn O(1) with no history
   copy and a clean independent branch (C21 AC-4). *Lowest risk; pure primitive validation.*
2. **Spike T3 (deterministic-tool replay):** prove a deterministic-tool-only continuation **reproduces** the
   original post-T outcome and a variant produces a clean diff (INV-5). **This is the make-or-break de-risker
   for the tractable slice — if even this doesn't reproduce, the whole concept is in doubt.** (Analog: git
   cherry-pick / Temporal replay, AI-CONTEXT §10:423.)
3. **Spike T4 (fail-closed production guard):** prove a non-twinnable external effect **fails closed** and a
   twinned one routes to C44 (never production). *Security-critical; gates any LLM-counterfactual work.*
4. **Spike T6 (LLM-counterfactual variance):** measure how much an LLM step's outcome varies on re-run from a
   fixed midpoint (force-1 from spec §6) — quantify the variance band so C48 can compare distributions. **This
   spike's purpose is to characterize the unsolved problem, NOT to solve it** — its output is evidence for OQ-1
   (what N / what bound / human-review-only?), the input to the heaviest-human-review decision (README:470).

**Top risk = G19's core (force 1):** LLM non-determinism means an LLM-step counterfactual can never be a
deterministic reproduction. De-risking posture: **ship the deterministic slice (1–3) as the real capability;
treat the LLM slice (4) as labeled best-effort + human-reviewed** until OQ-1 settles. The plan's success is NOT
contingent on solving force 1 — that would contradict v4.

## 6. Definition of done

**Per-task DoD** ties to the spec's acceptance criteria:
- **T0 done:** contract (I1/I5/**I6 fidelity taxonomy**) frozen + published; C47/C48 can compile against stubs.
- **T1 done:** **AC-1** (branch-at-midpoint via C21 I5, no history copy) + **AC-2** (variant isolated to branch).
- **T2 done:** a variant (prompt/model/hyperparam/step) binds onto the branch at T (feeds AC-3/AC-6).
- **T3 done:** **AC-3** — deterministic-tool-only continuation **reproduces** original outcome + clean variant
  diff (INV-5). *The load-bearing "it works for the tractable slice" gate.*
- **T4 done:** **AC-4** — all external calls route to C44 twins; non-twinnable effect **fails closed**; no
  production side effect.
- **T5 done:** **AC-6** — paired (original, variant) result emitted in a C48-comparable / C32-C33-scorable
  shape; **AC-5** — fidelity tag stamped, deterministic vs best-effort mechanically distinguishable.
- **T6 done:** **AC-7** — LLM-counterfactual produces a **labeled, variance-bounded, best-effort** result that
  **does NOT claim reproduction**. *DoD is "honestly labeled and bounded", explicitly NOT "reproduces".*
- **T7 done:** integration pack drives **AC-1…AC-8** against pinned C21 + a C44 twin behind C43; **AC-8** clean
  degradation (factory unaffected when C49 disabled) passes.

**Per-component DoD (Sweep-1 exit):**
- The **contract + the G19 honest partition** are specced (spec §6): the **tractable-now slice**
  (`deterministic-tool-replay`) has hard acceptance criteria (AC-3); the **deferred slice** (full LLM-step
  counterfactual) is **explicitly framed as best-effort/human-reviewed** with the trust question logged as
  **OQ-1** — not claimed solved.
- The branch/replay seam (C21), the isolation/twin seam (C43/C44), and the producer/consumer seams (C47/C48)
  are **named with freeze milestones**; nothing C49 owns duplicates C21's primitive (INV-1).
- **OQ-1 (the unsolved core)** is recorded in [`_meta/review-log.md`](../_meta/review-log.md) as the riskiest
  open question in v4 (component-inventory:127), routed to the heaviest-human-review posture (README:470).
- **Drop check:** C49 adds **no trajectory store**, **no custom branch implementation**, **no variant authoring**,
  **no statistical test**, **no twin/isolation engine** — all are reused from C21 / C47 / C48 / C44 / C43. The
  sole KEEP is the **branch-from-midpoint replay driver + the fidelity-labeled, honestly-partitioned contract**.
