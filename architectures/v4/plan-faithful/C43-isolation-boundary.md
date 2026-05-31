# C43 — Isolation & lethal-trifecta boundary  (Build Plan, canonical track)

> Source / Spec ref: [C43 spec (canonical)](../spec/C43-isolation-boundary.md)
> Track: canonical   Status: sweep-1

C43 is **policy/declaration**, not a service: it defines the closed boundary-type set
(`twin`/`isolated`/`production`), the **twin-by-default / production-scissors** routing rule (F44), the
**blast-radius invariant** for a broad-tool-access agent (D-13), and the Bash/network/fs security posture.
The genuine keep is the **deterministic boundary typing (P4) + default-twin routing (P7)**; the **mechanical
isolation is the stack's** (C04/C42 process/worktree boundaries + C44 twins) and the C43 enforcement/grant
layer, OS jail, OPA, and `boundary_class` tags are **dropped** (C02-04/C04-05/C42-06/C41-07). The plan is
correspondingly small; the load-bearing work is **freezing the typing/routing contracts** that C44/C45/C57
build against and **carrying the G31 exposure-window residual honestly** until C44 twins land.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | **Freeze the boundary-typing contract** — closed type set {`twin`, `isolated`, `production`}; deterministic-typing invariant (type by rule, not LLM — F51/F33). (Spec §3.1, §4.1) | S | — |
| **T2** | **Freeze the twin-by-default / production-scissors routing rule** — surfaces are `twin` by default; `production` requires an explicit per-pack scissors declaration (F44); blast-radius invariant (D-13). (Spec §3.2, §4.2) | S | T1 |
| **T3** | **Freeze the twin-route binding contract** — `twin`-typed surface → its C44 twin; default-twin posture. (Spec §3.3) | S | T2; C44 twin seam |
| **T4** | **Write the Bash/network/fs security-posture statement** — per-surface default posture, with enforcement substrate identified as C04/C42 + C44 (not C43-built). (Spec §3.4) | S | T1, T2 |
| **T5** | **Write the one-line G31 authority note + residual feed** — typing/routing is C43's keep; mechanical isolation is the stack's; enforcement/grant layer + OS jail + OPA + tags dropped; the bound is *aspirational until C44 twins land*. A sweep-1 clarification + a residual feed to C57, **not** a control plane. (Spec §4.3, §3.5) | S | T2 |
| **T6** | **Author boundary-type + scissors config exemplars** — a `twin`-default surface, an `isolated` surface, and a `production` surface *with* its explicit per-pack scissors declaration; plus the invalid (production-by-default / LLM-typed) negative examples. | S | T1, T2 |
| **T7** | **Resolve enforcement-strength + exposure-window OQs (G31/OQ-C43-1/OQ-C43-2)** — spike: does the pack/`gc` loader *reject* a production-defaulted or LLM-typed surface, or permit-with-review? Is detection-only-until-C44 the accepted Phase-0 posture, or must C43 be sequenced earlier? Feeds the C57 residual + the orchestrator decision. | M | T2; G11-class `gc`/twin availability; C44 status |
| **T8** | **Resolve the boundary OQs** — OQ-C43-3 (`isolated` vs C42/C04 worktree scope — label-only vs new sandbox), OQ-C43-4 (scissors grammar + attach point in C02/C03, not the dropped grant engine). | S | T1, T2 |

## 2. Dependency graph

```
                  T1 ─► T2 ─► {T4, T5, T6}
C44 (twin seam) ──┴────► T3
C42 (partition) ──► (baseline scope consumed by T1/T2)
                         T2 ─► T7 (spike) ──► C57 residual + orchestrator decision
                         T1 ─► T8 (OQs) ────► review-log / C02 / C03 / C42 / C04
```

- **Critical path:** T1 → T2 → (T4 + T5). These freeze the boundary-type set + the twin-by-default rule +
  the blast-radius invariant that C44/C45/C57 all build against. Everything else hangs off them.
- **Upstream blockers:** T1/T2 consume **C42**'s partition (the baseline scope) — already built. T3 needs
  the **C44** twin seam (same Batch 4 — co-developed). T7's spike is gated on the real `gc`/twin stack being
  runnable end-to-end (the same **G11** assumption that blocks C01/C34) **and** on C44 status (the residual
  shrinks only as twins land).
- **Downstream consumers waiting on these freezes:** **C44** (its twins bind to `twin`-typed surfaces),
  **C45** (verifies usage against the declared typing), **C57** (records the F12/F44/F56 mechanism + the G31
  residual), and the autonomy/blast-radius consumers **C56/C39** (the bound caps L4/L5 reach).

## 3. Parallelization

- **Independent once T1+T2 land:** T4 (security-posture statement), T5 (G31 authority note + residual feed),
  T6 (config exemplars) are disjoint and can be authored concurrently by separate workstreams.
- **Independent of the contract path:** T8 (the `isolated`-scope / scissors-grammar OQs) only needs T1/T2
  and can run in parallel with the whole T2→T4/T5 chain.
- **The one serial spike:** T7 (enforcement-strength + exposure-window) is the long pole and gates the C57
  residual + the orchestrator's "detection-only-until-C44 vs sequence-C43-earlier" decision; start it as soon
  as T2's invariant is frozen and the `gc`/twin stack + C44 status are known — do not let it block T4/T5/T6.
- **Cross-component parallelism:** because C43 is Batch-4 declaration, **C44** can build twins against the
  **stubbed** `twin` boundary type the moment T1+T3 freeze, and **C57** can record the mechanism (with the
  G31 residual) against T5's note, before T7 resolves enforcement strength.

## 4. Interfaces-first / contract milestones

| Milestone | Freezes | Unblocks |
|---|---|---|
| **M1 (earliest, load-bearing)** | Boundary-type set + twin-by-default + blast-radius invariant (T1+T2) — {`twin`,`isolated`,`production`}, `production` requires explicit per-pack scissors | C44 (what `twin` means), C45 (what to verify), C57 (what "Addressed" rests on) |
| **M2** | Twin-route binding contract (T3) — `twin`-typed surface → C44 twin | C44 binds its twins to `twin`-typed surfaces |
| **M3** | Security-posture statement (T4) — Bash/network/fs defaults + enforcement-substrate ownership (C04/C42 + C44) | C04/C42 ↔ C43 boundary on who isolates vs who types |
| **M4** | One-line G31 authority note + residual feed (T5) | C57 (records F12/F44/F56 mechanism + the aspirational-until-C44 residual). *(Not "what to enforce" — the C43 grant/enforcement layer is dropped, C02-04; the mechanical isolation is C04/C42 + C44. See spec §4.3.)* |

Freeze M1 first: it is the clause F12/F44/F56 all rest on. M2 lets C44 start; M4 lets C57 record the
mechanism + the honest residual without waiting on the T7 enforcement spike.

## 5. Risks & de-risking order

1. **(Highest) The bound is aspirational — twins are unbuilt and last (G31/XC-8/OQ-C43-2).** F12/F44/F56 are
   "Addressed" on a mechanism (C44 twins) that does not exist Phase 0→3b, so for the whole early period the
   lethal-trifecta is exposed. **De-risk via T7's spike + the C57 residual**: establish whether
   detection-only-until-C44 is the accepted Phase-0 posture or C43 must be sequenced earlier. The residual
   must be loud in C57 so no one lifts "Addressed" without the caveat. *(Ownership is settled by **D-13** —
   C43 owns the blast-radius bound, C34 the holdout enforcement+audit, C42 the partition. The substrate
   question — does the loader/stack *prevent* production reach at interaction time, or rely on C44 + C04/C42
   boundaries — stays for the spike, G11.)*
2. **Scope-creep into the dropped enforcement layer (C02-04/C04-05/C42-06/C41-07).** The temptation is to
   build a C43 capability-grant engine, a spawn-time OS jail, an OPA policy, or `boundary_class` tags — **all
   explicitly dropped** by the bar. De-risk by keeping C43 to *typing + default-twin routing* (the genuine
   P4/P7 keep) and the §4.3 authority note that names the mechanical isolation as the stack's. When in doubt:
   DROP (this is the dominant failure mode for a security component).
3. **`gc`/twin primitive may not exist as described (G11-class).** T3/T7 assume C44 twins + the
   process/worktree boundaries (C04/C42) are real and routable. Spike the `twin`-route binding against a real
   twin early (T7) — same uncertainty that blocks C44/C34.
4. **`isolated`-type / scissors-grammar drift (OQ-C43-3/-4).** Low impact but cheap to retire — T8 early so
   `isolated` is confirmed as a *label* on the C42/C04 boundary (not a new sandbox) and the scissors
   declaration attaches in C02/C03 config (not the dropped grant engine), before C44/C57 build against them.

## 6. Definition of done

**Per-task:** each contract task (T1–T5) is done when its spec section is frozen and a downstream consumer
(C44/C45/C57) can build a stub against it; T6 is done when the F44-faithful exemplars (incl. the invalid
production-by-default / LLM-typed negative cases) exist; T7/T8 are done when the OQ is answered in review-log
(or explicitly carried forward with owner + reason).

**Per-component (tied to spec §8 acceptance criteria):**
- The twin-by-default invariant is frozen and a production-by-default config is documented as **invalid**
  (§8.1); the deterministic-typing invariant holds (§8.2). The blast-radius bound is the **distinct**
  boundary from C34/C42 — the split is **D-13** (C43 bounds; C34 enforces+audits holdout; C42 provides
  partition).
- The Bash/network/fs security posture is stated with the enforcement substrate identified as C04/C42 + C44
  (§8.4), and the twin-route + scissors feed exists for C44/C45/C57 (§8.5).
- The **G31 exposure-window residual** (aspirational-until-C44) is explicit and discoverable by
  C57/C56/C39 (§8.6), and enforcement strength is recorded (T7).
- **No over-build:** no capability-grant engine, OS jail, OPA, or `boundary_class` tags (§8.7,
  C02-04/C04-05/C42-06/C41-07).
- **G35 blast-radius half** is handled and the **objective-drift half routed to C39/C56/C35**; **G37
  secrets** documented as **C03/G37** (deferred, D-14), not a C43 layer (§8.8).
- All four OQs are in review-log with owners (OQ-C43-1/-2 → orchestrator/C57 + C44-sequencing; OQ-C43-3 →
  C42/C04; OQ-C43-4 → C02/C03).
