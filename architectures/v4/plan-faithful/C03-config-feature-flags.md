# C03 — Layered config / feature-flag model  (Build Plan, canonical track)

> Source / Spec ref: [`spec/C03-config-feature-flags.md`](../spec/C03-config-feature-flags.md)
> Sweep-2 update: updated to match spec §4.1 field tables, §4.2 layer-merge, §4.3 catalog, §5.1 diagram,
> §6.1 E-codes, §8.2 AC-codes. All Sweep-1 tasks preserved; Sweep-2 tasks (T7/T8) promoted and refined.

## 1. Work breakdown

Ordered tasks to build C03. Sizes: S/M/L. Sweep-2 updates reflect implementation-ready depth.

| Task | Description | Size | Prereqs | Status |
|---|---|---|---|---|
| **T1** | Enumerate the **canonical capability-section catalog** (section → capability gated → owning C-ID → phase), from spec §4.3. This is the load-bearing artifact the rest of C03 hangs on. | M | spec §4.3 | Done at Sweep-1; catalog now frozen with verification-status column at Sweep-2 |
| **T2** | Fix the **presence-is-the-flag** contract + the **absent⇒inert** invariant in prose the substrate (C01) and every gated component agree to. | S | T1 | Done at Sweep-1 |
| **T3** | Define the **layer set + merge precedence** (`pack.toml` imports → `city.toml` → `.gc/site.toml` → per-agent `env`); grounded in F1/F3/anchor §2; residual merge-algebra → G11. | M | T1; F1/F3 harvest facts | **Partially resolved (Sweep-2)**: precedence order concrete (§4.2); deep-merge vs replace and array-section semantics remain needs-G11 |
| **T4** | Author the **three phase skeletons** as committed reference configs (Phase-0 §5.2, Phase-1 additions, Phase-2 additions) and prove they compose under T3 precedence. | M | T1, T3 | Done at Sweep-2 (§5.2) |
| **T5** | Implement the **G03 phase-relative native-count derivation** (count from present sections ⇒ 5 at Phase 0, 6 at Phase 1). | S | T1, T4 | Done at Sweep-1/Sweep-2; AC-C03-01..03 |
| **T6** | **G37 secrets-surfacing audit hook**: detect credential-bearing keys in `env`/`[[service]]`; emit residual-risk finding (detection only; D-25 posture). | S | T1 | Done at Sweep-1; AC-C03-07 |
| **T7** | **Concrete TOML schema + config validator**: key types, required keys per section, unknown-key rejection, schema-version pin per AI-CONTEXT §3.5. Implements E-C03-01 through E-C03-07 at load time. | L | T1–T4 | **Sweep-2 deliverable** — field table §4.1 + E-codes §6.1 + ACs §8.2 are the spec; implementation in sprint |
| **T8** | **Merge-precedence test vectors** + array-section (`[[service]]`/`[[rig]]`) merge rules — verified against pinned `gc` install (G11 discharge). | M | T3, T7, G11 | **Sweep-2 deliverable — gated on G11 verification** (needs Docker + pinned `gc` run) |
| **T9** | **AC-C03-01 through AC-C03-10 test suite** — executable checks against the E-codes and config validator from T7. | M | T7 | **Sweep-2 deliverable** |

## 2. Dependency graph

- **Upstream gate**: **C01** (Gas City substrate) must expose how it parses/merges TOML before T8 can be
  authoritative — this is the G11 "Gas City behavior unverified" dependency. T1/T2/T3 (precedence order)
  can proceed on F1/F3 harvest facts; T8 (deep-merge algebra + array-section semantics) needs pinned `gc`.
- **C01↔C03 load-time contract**: C01 reads C03's files; C03's presence flags tell C01 what to activate.
  This cycle is broken by the M1 interface freeze (catalog T1 + precedence T3). Dependents may build
  against M1-frozen stubs.
- **Downstream dependents**: **C12** (formulas), **C08** (spec artifact), **C06**, **C42**, **C04**, **C40**,
  services — all consume the §4.3 catalog + presence predicate. They can build against the **frozen catalog
  (T1) + flag contract (T2)** as stubs before T3–T8 land.
- **Critical path**: T1 → T2 → (catalog+contract frozen, unblocks dependents) → T3 → T4 → T5/T6 → T7 →
  T9. T8 is G11-gated and off the critical path until the Docker spike runs.

## 3. Parallelization

Within C03, after T1 freezes the catalog:
- **Stream A** (contract): T2 → T5 (native-count derivation) → T9 (AC-C03-01..03).
- **Stream B** (layering): T3 → T4 (phase skeletons compose) → T8 (G11-gated).
- **Stream C** (security): T6 (secrets-surfacing) → AC-C03-07 — independent of A/B, depends only on T1.
- **Stream D** (validator): T7 (TOML schema + validator) → T9 (full AC suite) — starts once T1–T4 stabilize.

Streams A, B, C run concurrently once T1 is done. T7 is the join point where A, B, and C feed (the
validator needs the catalog, the precedence, and the secrets-lint hook). T9 (test suite) closes D.

## 4. Interfaces-first / contract milestones

Freeze early so dependents build in parallel against stubs:

1. **M1 — Capability-section catalog (T1)**: the section→capability→C-ID→phase table (spec §4.3) with
   verification-status column. *Highest-leverage freeze*: every gated component reads it. Freeze first.
2. **M2 — Feature-flag predicate (T2)**: "is section present ⇒ capability on." One-line contract; freeze
   with M1.
3. **M3 — Layer-merge precedence (T3)**: pack imports → city.toml → site.toml → per-agent env; concrete
   override semantics and the "no-path-in-city-toml" + "no-duplicate-import" F1/F3 rules baked in.
   Residual array-section algebra marked G11.
4. **M4 — Phase skeletons (T4)**: the reference `pack.toml` / `city.toml` / `.gc/site.toml` per phase
   (spec §5.2); the integration target for C54 (phase plan) and for end-to-end install tests.
5. **M5 — TOML validator + E-codes (T7)**: config validator implementing E-C03-01 through E-C03-07;
   each error maps to at least one AC.
6. **M6 — AC suite (T9)**: all AC-C03-01 through AC-C03-10 pass against the T7 validator and the T4
   skeletons. G11-gated ACs (merge-algebra) are stubbed with a G11 marker.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **Gas City merge/precedence behavior (G11)** — T8 rests on an unverified third-party. *De-risk first*:
   confirm against a pinned `gc` install how `[imports.*]` composes with local `city.toml` and whether
   array sections append or replace. T3's precedence order is now concrete (F1/F3 grounded); the residual
   is array-section merge semantics. If Gas City's real rule differs, T8/AC-C03-08 shifts.
2. **`[[rig]]` vs `[[rigs]]` spelling in city.toml (G11)** — F1 and the prototype `city.toml.example`
   disagree. All C03 rig-block authoring must note the spelling as needs-pinned-gc-run until G11 resolves.
3. **G03 count semantics** — low technical risk; AC-C03-01..03 pin the phase-relative count (5/6) early.
4. **G37 secrets** — bounded: detection-only is cheap (T6/AC-C03-07); the deferral (D-25) is the posture.

## 6. Definition of done

**Per-component (Sweep-2):**
- The capability-section catalog (§4.3) is committed with verification-status and every section traces
  to a v4 source or harvest fact.
- Presence-is-flag + absent⇒inert invariants stated and adopted by C01 and the gated components (M1/M2).
- The layer-merge precedence is concrete (§4.2, M3); residual array-section algebra marked G11.
- The three phase skeletons (§5.2) compose under stated precedence (M4).
- The field table (§4.1) provides Key/File/Type/Req/Semantics/R-W-by for every C03-governed config key.
- The state diagram (§5.1) shows the config-load lifecycle in valid Mermaid.
- E-codes E-C03-01 through E-C03-07 are defined with surfaced-as and caller-recovery.
- AC-codes AC-C03-01 through AC-C03-10 are defined with given/when/then and E-code cross-refs.
- Phase-relative native count derives 5 (Phase 0) / 6 (Phase 1) — G03 resolved.
- G37 secrets risk surfaced as residual-risk finding and mirrored to review-log; D-25 posture applied.
- XC-7 (CapabilityDescriptor ownership) stated and deferred to orchestrator ledger.
- OQ-C03-1 resolved (D-25); OQ-C03-2 partially resolved (§4.2); OQ-C03-3 still open.

**Per-task:** each task exits when its spec-§8.2 acceptance criterion holds:
- T1↔AC-C03-01,02 catalog + presence-is-flag; T4↔AC-C03-08 phase skeletons compose;
- T5↔AC-C03-01,02,03 phase-relative count; T6↔AC-C03-07 secrets surfaced;
- T7↔AC-C03-04,05,06,09,10 validator rejects bad configs; T9↔all ACs pass.
- Sweep-2 G11-gated tasks (T8) deferred with G11 marker; OQ-C03-3 recorded open.
