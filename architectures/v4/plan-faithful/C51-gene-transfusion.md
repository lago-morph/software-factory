# C51 — Gene-transfusion discipline (`gene-transfusion`)  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C51-gene-transfusion.md`](../spec/C51-gene-transfusion.md)

## 1. Work breakdown

Ordered tasks to build C51. Sizes: S (≤½ day), M (~1–2 days), L (multi-day). C51 is a **cross-cutting
discipline** (a predicate + invariants + a license-mode contract), not a runtime service — most tasks are
**contract definition** that ride existing components (C20 fields, C30–C33 evaluation), so sizes skew
small. The load-bearing task is **T3 (the predicate)**.

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Transfusion record contract.** Pin the component-grain values `transfused_from` (set, ≥1), `transfusion_license`, `transfusion_mode`, `transfusion_verdict` as **C20 schema-slot requests** on the `factory_build` bead (spec §4). Confirm grain = per-component (RC11-01), not per-record. | S | C20 `factory_build` shape known (D-3) |
| T2 | **≥1-exemplar invariant + declaration-time gate.** Reject a factory-build declaring zero exemplars; this is the "no invention from scratch" check (spec §3.2, §8.1; B55). | S | T1 |
| T3 | **Transfusion-correctness/completeness predicate (G07 — load-bearing).** Define the predicate shape: exemplar's *named* behaviors ⇒ each covered by ≥1 scenario (completeness) **and** satisfaction distribution over those scenarios ≥ bar (correctness). Wire to C30 (scenarios) / C31 (run) / C32 (judge) / C33 (distribution). **Do NOT build a scorer** — express the contract over the existing tier. | M | T1; C30/C32/C33 output shapes |
| T4 | **License-mode contract (G30).** Decision table: per exemplar, license fact (from README:285–306 census) ⇒ {code-port if verified-permissive | pattern-reimplement otherwise} + donate-back-vs-stay-private disposition. Fix mode **pre-build**. | S | T1; census home confirmed (OQ-C51-4) |
| T5 | **Bet-failure fallback signal (G14).** Define the *transfusion-insufficient* outcome emitted on fail/inconclusive, and its hand-off to C52's design-review gate (spec §3.5, §5). | S | T3 |
| T6 | **Acceptance-gate integration with C52.** Specify the two call-points C52 invokes: declaration-time (T2+T4) pre-build, acceptance-time (T3) pre-deploy; verdict recorded on the bead (spec §5). | M | T2, T3, T4, T5; C52 loop contract |
| T7 | **External-grounding exclusion rule (A107).** Define how an *adopted* upstream substrate dependency is excluded from the ≥1-exemplar invariant (only factory-built glue is in scope; spec §3 invariant, §8.6). | S | T2 |
| T8 | **Conformance vectors.** Author the test set: empty-exemplar reject; component-grain provenance resolves via §16 step 2; generic-spec-but-no-exemplar-behavior fails predicate; code-port-from-unverified-license blocked; fail ⇒ routes-to-review-not-ship. | M | T2–T7 |

## 2. Dependency graph

```
C20 (factory_build bead fields)      ← schema-slot host; transfused_from/license/mode/verdict live here
C08 (Definition-of-Done)             ← predicate grades against this
C30/C31/C32/C33 (eval tier)          ← predicate is EXPRESSED OVER this tier (not rebuilt)
        │
        ▼
       T1 ──▶ T2 ──▶ T7
        │      │
        │      ├──▶ T4
        ▼      │
       T3 ─────┼──▶ T5 ──▶ T6 ──▶ T8
        ▲      │            ▲
        └──────┘            │
   (C30/C32/C33 shapes)─────┘
```

- **Critical path**: C20/C30–C33 shapes → T1 → **T3 (predicate)** → T6 (C52 gate integration) → T8. T3 is
  the load-bearing node — it is the acceptance contract the entire bootstrap (C52–C54) is blocked on
  (inventory critical-path note #4).
- **External prerequisites**: C20 must expose the `factory_build` bead's extensibility (D-3) before T1 can
  request slots. C30/C32/C33 must expose their scenario/score/distribution output shapes before T3 can
  bind the predicate to them — this is a **read** of those contracts, not a change to them.
- **Soft prerequisite**: C52's loop contract gates T6's *finalization* (the exact call-points) but not
  T3's first draft.

## 3. Parallelization

- **Parallel after T1**: T2 (≥1-exemplar invariant), T3 (predicate), and T4 (license mode) are
  independent contract work once the record slots are fixed — **three workstreams**. T3 is the long pole;
  start it first and in parallel with everything else.
- **T7 (external-grounding exclusion)** runs concurrently with T3/T4 — it only needs T2's invariant.
- **T8 (conformance vectors)** can be drafted per-task as each of T2/T3/T4 lands, in parallel with T5/T6.
- **Cross-component**: C51's T1 is a **schema-slot request into C20** — coordinate with the C20 author so
  the `factory_build` bead carries the transfusion fields (parity with how C20 itself took G18 slots). And
  T3 is a **contract read against C30/C32/C33** — coordinate with that tier so the predicate binds to
  their real output shapes. These are the two synchronization points; neither requires C51 to own new
  storage or scoring.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents (C52, C53, C54, C57) can build against stubs:

1. **Transfusion record slots (T1)** — `transfused_from` (set, ≥1) / `transfusion_license` /
   `transfusion_mode` / `transfusion_verdict` at component grain — freeze first as a **C20 slot request**;
   C57 (license hygiene) and the §16 cold-start path read them.
2. **Predicate shape (T3)** — the {pass | fail | inconclusive} contract = *(every named exemplar behavior
   covered) ∧ (satisfaction ≥ bar)* — freeze the **shape** immediately (the numeric bar stays
   policy-deferred to C50/C53) so **C52** can build its acceptance gate and **C53** its milestone against
   a stub verdict.
3. **License-mode decision table (T4)** — the {code-port | pattern-reimplement} mapping — freeze so a
   factory-build knows its legal envelope *before* the transfusion act; C57 aggregates the dispositions.
4. **Transfusion-insufficient signal (T5)** — freeze the fail/inconclusive ⇒ review hand-off so **C52**'s
   loop and **C54**'s phase plan can wire the human-review fallback (README:498).

## 5. Risks & de-risking order

| Risk | De-risking action | Order |
|---|---|---|
| **G07 / OQ-C51-1**: "named exemplar behaviors" has no defined extraction method, so the *completeness* half of the predicate is subjective and may not be checkable. | Spike: take one real Phase-3a exemplar (e.g. git reflog / CloudTrail override-shape, README:457) and try to enumerate its named behaviors → scenarios. If enumeration is infeasible, completeness must weaken to a coverage heuristic at sweep-2. **Retires the most uncertainty in the load-bearing deliverable.** | **First** |
| **G14 / OQ-C51-2**: per-component fallback may be insufficient — a whole high-value class (Healer/twins/self-opt) failing to transfuse has no home if C54 disclaims it. | Confirm with C54 (phase plan) that the class-level hedge (re-sequence / hand-build) is C54's, so C51's per-component signal has somewhere to escalate. | Second |
| **Predicate-tier coupling**: C30/C32/C33 output shapes may not expose enough to compute completeness (per-scenario→behavior trace). | Read C30/C32/C33 contracts early; if the scenario record can't carry an exemplar-behavior tag, that becomes a C30 slot request (mirrors T1→C20). | Second |
| **G30 / OQ-C51-4**: license census (README:285–306) is hand-maintained, partly "verify (convention)", and may be stale at first use of a new exemplar. | Make "add exemplar's license to the census" a prerequisite build step; confirm C57 owns the census + verification workflow (no SBOM scanner at Phase 0). | Third |
| **Over-build drift**: temptation to build a second judge / SBOM scanner / signing for the transfusion record. | Hold the line per THE BAR: predicate rides C30–C33, license rides the existing census, signing is FE-3 (G37). Code-review against §1/§6 NOT-list. | Ongoing |

## 6. Definition of done

**Per-component (ties to spec §8 acceptance criteria):**
- **DoD-1**: a factory-built component declaring **zero** exemplars is rejected; ≥1 `transfused_from` URL
  passes — "no invention from scratch" enforced (spec §8.1; B55).
- **DoD-2**: `transfused_from` is recorded **once per factory-built component** on its `factory_build`
  bead and resolves via §16 cold-start step 2 — component-grain provenance, not per-record (spec §8.2;
  RC11-01).
- **DoD-3**: the predicate is **exemplar-grounded + complete** — every named exemplar behavior is covered
  by ≥1 scenario and a `pass` requires satisfaction ≥ bar; a component satisfying a generic spec but
  covering no exemplar behavior does **not** pass (spec §8.3). **The numeric bar is correctly deferred to
  C50/C53, not set here** (G07 predicate-shape delivered, threshold policy relocated).
- **DoD-4**: a **code-port** from an unverified/restrictive-license exemplar is blocked; the same exemplar
  passes under **pattern-reimplement** (spec §8.4; G30). Tracker (unverified) is the test instance.
- **DoD-5**: a fail/inconclusive predicate emits **transfusion-insufficient** and routes to human design
  review, never silent-ships (spec §8.5). **This is G14 *made falsifiable per component*, not eliminated**
  — the class-level hedge is C54's (OQ-C51-2).
- **DoD-6**: an *adopted* upstream substrate dependency (CXDB, Temporal) is **not** flagged for a missing
  `transfused_from` — only factory-built glue is in scope (spec §8.6; A107).

**Per-task**: each Tn lands with its contract documented and a conformance vector covering its rule. T1
lands as an accepted C20 slot request; T3 lands with its binding to C30/C32/C33 output shapes named; T4
lands with the license decision table referencing the README:285–306 census.

**Open-question exit**: OQ-C51-1 (named-behavior extraction — the completeness anchor) and OQ-C51-2 (C54
class-level fallback ownership) must be resolved or explicitly carried to sweep 2 before T3/T5 are
considered frozen rather than draft. OQ-C51-3 (threshold owner) and OQ-C51-4 (census authority) co-resolve
with C50/C53 and C57 respectively.
