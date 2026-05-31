# C03 — Layered config / feature-flag model  (Build Plan, Track A)

> Source / Spec ref: [`spec/C03-config-feature-flags.md`](../spec/C03-config-feature-flags.md)

## 1. Work breakdown

Ordered tasks to build C03. Sizes: S/M/L. Sweep-1 altitude — tasks are scoped to "make the config model
real and gateable," not to deep schema/validator code (that is sweep 2+).

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** | Enumerate the **canonical capability-section catalog** (section → capability gated → owning C-ID → phase), from spec §4. This is the load-bearing artifact the rest of C03 hangs on. | M | spec §4 |
| **T2** | Fix the **presence-is-the-flag** contract + the **absent⇒inert** invariant in prose the substrate (C01) and every gated component agree to. | S | T1 |
| **T3** | Define the **layer set + merge precedence** (`pack.toml` imports → `city.toml` → per-agent `env`); resolve the §4 FAITHFUL-FILL against verified Gas City behavior (G11). | M | T1; Gas City verification |
| **T4** | Author the **three phase skeletons** as committed reference configs (Phase 0 §13.1, Phase 1 §13.2, Phase 2 §13.3) and prove they compose under T3 precedence. | M | T1, T3 |
| **T5** | Implement the **G03 phase-relative native-count derivation** (count from present sections ⇒ 5 at Phase 0, 6 at Phase 1). | S | T1, T4 |
| **T6** | **G37 secrets-surfacing audit hook**: detect credential-bearing keys in `env`/`[[service]]`; emit residual-risk finding (detection only). | S | T1 |
| **T7** | (sweep 2) Concrete **TOML schema + config validator** (key types, required keys per section, schema-version pin per AI-CONTEXT §3.5). | L | T1–T4 |
| **T8** | (sweep 2) **Merge-precedence test vectors** + array-section (`[[service]]`/`[[rig]]`) merge rules. | M | T3, T7 |

## 2. Dependency graph

- **Upstream gate**: **C01** (Gas City substrate) must expose how it parses/merges TOML before T3 can be
  authoritative — this is the G11 "Gas City behavior unverified" dependency. T1/T2 can proceed on v4 text
  alone; T3 needs C01 reality.
- **Downstream dependents**: **C12** (formulas), **C08** (spec artifact), **C06**, **C42**, **C04**, **C40**,
  services — all consume the §4 catalog + presence predicate. They can build against the **frozen catalog
  (T1) + flag contract (T2)** as stubs before T3–T8 land.
- **Critical path**: T1 → T2 → (catalog+contract frozen, unblocks dependents) → T3 → T4 → T5/T6. T7/T8 are
  sweep-2 and off the sweep-1 critical path.

## 3. Parallelization

Within C03, after T1 freezes the catalog:
- **Stream A** (contract): T2 → T5 (native-count derivation).
- **Stream B** (layering): T3 → T4 (phase skeletons compose).
- **Stream C** (security): T6 (secrets-surfacing) — independent of A/B, depends only on T1.
- **Stream D** (sweep 2): T7 → T8 — starts once T1–T4 stabilize.

Streams A, B, C run concurrently once T1 is done. T4 (skeletons) is the join point where A and B meet
(the count derivation in T5 validates against T4's skeletons).

## 4. Interfaces-first / contract milestones

Freeze early so dependents build in parallel against stubs:

1. **M1 — Capability-section catalog (T1)**: the section→capability→C-ID→phase table. *Highest-leverage
   freeze*: every gated component reads it. Freeze first.
2. **M2 — Feature-flag predicate (T2)**: "is section present ⇒ capability on." One-line contract; freeze
   with M1.
3. **M3 — Layer-merge precedence (T3)**: needed before any component relies on *parameter values* (vs mere
   presence); can freeze slightly later than M1/M2 since presence-only dependents don't need it.
4. **M4 — Phase skeletons (T4)**: the reference `pack.toml`/`city.toml` per phase; the integration target
   for C54 (phase plan) and for end-to-end install tests.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **Gas City merge/precedence behavior (G11)** — T3 rests on an unverified third-party. *De-risk first*:
   confirm against an actual `gc` install how `[imports.*]` composes with local `city.toml` and whether
   array sections append or replace. If Gas City's real rule differs from the §4 FAITHFUL-FILL, T3/T4/T8
   shift. This is the single biggest unknown.
2. **G03 count semantics** — low technical risk but high *correctness* risk for downstream claims; pin the
   phase-relative count (T5) early so no other doc re-introduces a fixed "6 of 12."
3. **G37 secrets** — bounded: detection-only is cheap; the *deferral* (no mitigation) is the risk to flag
   loudly to review-log, not a build risk.

## 6. Definition of done

**Per-component (sweep 1):**
- The capability-section catalog (§4) is committed and every section traces to a v4 source.
- Presence-is-flag + absent⇒inert invariants stated and adopted by C01 and the gated components.
- The three phase skeletons compose under a stated precedence; the Phase-0 "Explicitly off" set is inert
  by omission.
- The phase-relative native count derives 5 (Phase 0) / 6 (Phase 1) — G03 made explicit, not a fixed headline.
- G37 secrets risk surfaced as a residual-risk finding and mirrored to review-log; no silent plaintext-secret
  acceptance.

**Per-task:** each task exits when its spec-§8 acceptance criterion holds:
- T1↔AC "presence-is-flag" catalog complete; T4↔AC "phase skeletons compose"; T5↔AC "phase-relative count";
  T6↔AC "secrets surfaced"; T3/T8↔AC "deterministic precedence, no silently-dropped key."
- Sweep-2 tasks (T7/T8) deferred with their open questions (OQ-C03-1 secrets scope, OQ-C03-2 merge rule)
  recorded in the spec §9 and the review-log.
