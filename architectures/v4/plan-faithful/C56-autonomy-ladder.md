# C56 — Autonomy ladder (L0–L5)  (Build Plan, canonical track)

> Source / Spec ref: [C56 spec (canonical)](../spec/C56-autonomy-ladder.md)
> Track: canonical (faithful)   Status: sweep-1

C56 is a **governance/policy artifact**, not a service: it defines the six-level ladder
(`L0 Manual … L5 Dark`), the **per-level authorization boundary** (which level authorizes out-of-loop
execution and which authorizes auto-ship without a human), the **declared current authorized level**
(operator-set, L4-default, fail-safe), and the **named F54 audit-pack obligation** that L4/L5 incur. The
plan is correspondingly small; the load-bearing work is **freezing the ladder + authorization boundary +
the level-read seam** that C39 and C53 gate on, and **writing the G35/G15 dispositions** (the ownership
split across C56/C43/C39/C57). There is **no enforcement engine to build** — enforcement lives at
C39/C43/C34 (the bar's DROP).

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Freeze the ladder definition** — closed, ordered six-level set `{L0 Manual, L1 Intern, L2 Pair, L3 HITL, L4 PM mode, L5 Dark}` with one-line v4-anchored semantics + the order invariant `L0<…<L5`. (Spec §3.1, §4.1) | S | — (README:81–86 / AI-CONTEXT:56) |
| **T2** | **Freeze the per-level authorization boundary (the G35 KEEP)** — the `level → {out-of-loop? / auto-ship without human?}` table with the two named thresholds: **out-of-loop @ L4** (batched review) and **auto-ship @ L5** (dark). (Spec §3.2, §4.2) | S | T1 |
| **T3** | **Freeze the current-authorized-level read seam + fail-safe** — a single read-only operator-set value; unset/garbled ⇒ **L4 default, not L5**; read at the gated action (downgrade-safe). (Spec §3.3, §4.3) | S | T1 |
| **T4** | **Write the L4-default declaration** — L4 (PM mode, batched review) is the binding default; L5 is opt-in requiring P12 maturity + trust (README:498/527). (Spec §3.4) | S | T2 |
| **T5** | **Write the G35 disposition** — the ownership split: **C56** owns ladder + which level may auto-ship + L4 default + the **named F54 audit obligation**; **C43** owns blast radius; **C39** owns the per-fix ship gate (I4); **C57** owns the objective-drift **audit register + mechanism** (F54 audit pack, deferred Phase-3+). Findings → review-log. (Spec §6, §9 OQ-3) | S | T2 |
| **T6** | **Write the G15 disposition** — sustained L4/L5 assumes the operator can author specs fast enough (F-MODE F25); documented precondition for raising the level, not a runtime mechanism. → review-log/C57. (Spec §6, §9 OQ-1) | S | T1 |
| **T7** | **Confirm the consumer seams (C39, C53)** — C39 *reads* the level for its L5 ship gate (matches C39 I4 / C39 §3 contract 4); C53 *reads* it for the bootstrap deploy gate (README:498). Confirm C56 is **named, not depended-on**, by both; reconcile reciprocal text. | S | T1, T2, T3 |
| **T8** | **Resolve the representation/promotion OQs** — OQ-2 (where the level lives: C03 config key vs dedicated surface; read API), OQ-4 (is L5 promotion machine-checkable or operator decision). Spike against real `gc`/C03 shape. | M | T3; G11-class `gc`/C03 availability |

## 2. Dependency graph

```
README:81–86 / AI-CONTEXT:56 ──► T1 ──► T2 ──► {T4, T5}
                                  │       └──► T3 ──► {T7, T8}
                                  └──► T6
C52 (self-bootstrap dial) ········(soft: the loop C56's level governs)
```

- **Critical path:** T1 → T2 → (T3 + T5). T1/T2 freeze the ladder + the authorization boundary that
  **C39 and C53 build their gates against**; T3 freezes the level-read seam those gates call; T5 records the
  G35 split so no consumer over-trusts C56 as an enforcer. Everything else hangs off these.
- **Upstream:** the ladder is sourced verbatim from README:81–86 / AI-CONTEXT:56, so T1 has no
  component blocker. The sole inventory dependency **C52** is *soft*: C56's level is the dial on C52's
  self-bootstrap design-review loop (README:498) — C56 can be frozen before C52 lands, and C52 reads the
  L4-default behavior the ladder formalizes. (FAITHFUL-FILL — see spec §2.)
- **Downstream consumers waiting on these freezes:** **C39** (L5 ship-authorization gate reads the level —
  the primary G35 seam), **C53** (bootstrap deploy gate reads the level), **C43** (pairs its blast-radius
  bound to the rung), **C57** (records the G35 residual + owns the F54 audit pack), **C35** (override
  cadence expectation). Note: C39 is **already written on disk** treating C56 as the level source (C39 §3
  contract 4, I4) — T7 is largely a *confirmation/reconciliation* pass, not a fresh negotiation.

## 3. Parallelization

- **Independent once T1+T2 land:** T4 (L4-default), T5 (G35 disposition), T6 (G15 disposition) are disjoint
  write-ups and can be authored concurrently.
- **Independent of the boundary path:** T6 (G15) only needs T1; T7 (consumer-seam confirmation) needs
  T1–T3 but is mostly reconciliation against the *already-written* C39 spec.
- **The one serial spike:** T8 (level representation + L5-promotion gating) is the long pole and is gated on
  `gc`/C03 availability (G11-class); start it once T3's seam is frozen — do not let it block T4/T5/T6/T7.
- **Cross-component parallelism:** because C56 is a tiny policy artifact, **C39/C53 can build their gates
  against the frozen ladder + boundary (T1+T2) and the named level-read seam (T3)** before T8 resolves the
  on-disk representation — they gate on the *value*, not its storage form.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Ladder + per-level authorization boundary (T1+T2) — the six levels, the order, and the **out-of-loop @ L4 / auto-ship @ L5** thresholds | C39 (what "L5" authorizes for its ship gate), C53 (what gates the bootstrap deploy) |
| **M2** | Current-level read seam + fail-safe (T3) — a read-only operator-set value, unset ⇒ L4-not-L5, read at decision time | C39's ship gate (reads the level; downgrade-safe), C53's deploy gate |
| **M3** | G35 disposition (T5) — the C56/C43/C39/C57 ownership split + the F54 audit-pack obligation | C57 (residual-risk register + the deferred audit pack), and prevents any consumer treating C56 as an enforcement engine |
| **M4** | L4-default declaration (T4) | C39/C53 fail-safe behavior (no auto-ship unless L5 explicitly declared) |

Freeze **M1 first**: it is the clause C39's I4 and C53's deploy gate both rest on. M2 lets the gates call a
named seam; M3 keeps the G35 ownership honest so C56 stays a *definition*, not an interceptor.

## 5. Risks & de-risking order

1. **(Highest) C56 mis-scoped as an enforcement engine.** The tempting over-build is a central autonomy
   interceptor for all auto-ship/auto-deploy calls — which would **duplicate C39 (I4 ship gate), C43 (blast
   radius), C34 (holdout)** and contradict their **already-frozen** specs. **De-risk via M1/M3**: hold the
   line that C56 *defines* the ladder + authorization boundary + the declared level, and **every "blocked"
   guarantee is the consumer's**. This is the capability-for-principle bar's DROP and the spec's §6 Reading
   A; getting it wrong inflates a tiny artifact into a redundant control plane.
2. **G35 objective-drift (F54) is the weakest v4 mechanism on a self-modifying L5 factory.** C56's *own*
   bound is structural (L4-default + the L5-opt-in threshold keep dark auto-ship off by default); the actual
   drift detection is the **F54 audit pack** (F-MODE-COVERAGE:178), owned by **C57** + deferred to Phase-3+.
   **De-risk via T5**: make the C56/C43/C39/C57 split explicit and route the audit-pack obligation loudly to
   C57, so the residual is *named*, not silently absorbed. Confirm C57 (unbuilt — Batch 5) accepts the audit
   pack (OQ-3).
3. **Level representation/read unsettled (G11-class).** v4 names no on-disk form for the current level.
   **De-risk via T8 spike**: confirm a single operator-set value in C03 config read at the gated action
   (downgrade-safe), vs a dedicated C56 surface — the same `gc`/C03 uncertainty that blocks C03/C39's
   config seams. Keep the fail-safe (unset ⇒ not-L5) regardless of representation.
4. **G15 staffing assumption presented as solved.** Low impact but cheap to retire — T6 documents the
   one-operator spec-authoring bottleneck as a *precondition* for sustained L4/L5 (F-MODE F25 "honest
   staffing / document it"), not a mechanism, so no downstream reader assumes C56 relieved it.

## 6. Definition of done

**Per-task:** each definition task (T1–T6) is done when its spec section is frozen and a downstream consumer
(C39/C53/C57) can build against it; T7 is done when the C39/C53 reciprocal text is reconciled (C56 named as
the level source, not a dependency); T8 is done when the representation + L5-promotion OQs are answered in
review-log (or carried forward with owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The **ladder is defined, closed, ordered** (§8.1) and the **per-level authorization boundary** with the
  two named thresholds (out-of-loop @ L4; auto-ship @ L5) is explicit (§8.2).
- The **current authorized level is readable and fail-safe** (unset ⇒ L4-not-L5; §8.3) and **L4 is the
  default, L5 opt-in** (§8.4).
- **C39 can gate its L5 ship-authorization, and C53 its bootstrap deploy, by reading C56's level** (§8.5) —
  with the gate enforcement the consumer's, not C56's.
- The **G35 split is explicit and routed** (C56 = ladder + auto-ship threshold + L4 default + F54 audit
  obligation; C43 = blast radius; C39 = per-fix gate; C57 = drift-audit register; §8.6) and the **G15
  precondition is documented** (§8.7).
- The **no-enforcement-engine check** passes (§8.8): the spec contains no central interceptor; every
  "blocked" guarantee is attributed to C39/C53/C43 — confirming C56 is a definition/policy artifact (the
  bar's DROP held).
- All OQs are in review-log with owners (OQ-1 G15 → C57/review-log; OQ-2 representation → C03/C39 sweep-2;
  OQ-3 G35 split + F54 audit home → C57; OQ-4 L5-promotion gating → C57/sweep-2).
