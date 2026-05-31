# C21 — CXDB Trajectory Store  (Build Plan, Track A)

> Source / Spec ref: spec/C21-cxdb-trajectory-store.md
> Sources cited in spec: README §Part 4 (lines 122, 241–242, 252, 261, 274–278, 290, 302), §Part 6 Phase 1 (lines 388–397), §Part 7 (lines 500, 541); AI-CONTEXT §5.1–§5.5, §10, §11, §13.2, §14, §15.2; inventory C21 row (line 33) + critical-path notes (lines 107, 123); gaps G17, G33 (and the G11 content-addressing thread).

## 1. Work breakdown

C21 is *adoption + verification + seam-freeze*, not authorship — CXDB stays upstream OSS (README line
500). The work is: pin the dependency, stand it up as a Phase-1 service, **prove the content-addressing /
O(1)-branching / performance claims**, prove the registry mechanism can hold a v4 bundle, and freeze the
ingest/branch/query/registry seams the critical-path dependents (C22, C24, C49) build against.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Source & pin CXDB | Obtain CXDB from `github.com/strongdm/cxdb` (AI-CONTEXT §15.2); pick a version; record commit+pin (mirrors C01 INV-1). Note small-team/abandonment risk (§14). | M | C01 standing |
| **T2** Stand up service | Expose :9009 (binary) + :9010 (HTTP); register the `[[service]]` block in `city.toml` (AI-CONTEXT §13.2 lines 558, 579); confirm `turns.log`/`blobs.pack`/`registry/` layout (AC-1). | S | T1 |
| **T3** Conformance: CAS + DAG + branch | Conformance pack asserting AC-2 (BLAKE3 dedup), AC-3 (turn-DAG replay), AC-4 (**O(1) branch — cost independent of depth**), AC-8 (no OTLP). **The primitive C49 depends on; verify explicitly.** | L | T2 |
| **T4** Conformance: performance | Assert AC-6 (p50<1ms append/10KB; sub-ms retrieval TB-scale) against the real pinned binary (de-risks the G11/upstream perf assumption). | M | T2 |
| **T5** Registry-mechanism proof | Register a *placeholder* v4 `{bundle_id,type,version}` bundle into `registry/` and resolve it on read with structural projection (AC-5). **Proves the mechanism C22 fills; addresses G17 store-side.** | M | T2 |
| **T6** Fail-open + idempotency proof | Assert AC-7: a CXDB-down run continues on beads+events (no crash); re-posting an accepted turn is a no-op (BLAKE3 idempotency). **Addresses G33 store-side; the property C24's buffer relies on.** | M | T2, C19/C23 standing |
| **T7** Freeze store seams | Enumerate + freeze I1–I8 (binary :9009, HTTP :9010, turn-append, Blob CAS put/get, O(1) branch, replay/retrieve, registry, `[[service]]` lifecycle) + the §4 turn-record [FAITHFUL-FILL] so C22/C24/C49 build against stubs. | M | T2 |

## 2. Dependency graph

- **Upstream of C21:** **C01** (the substrate that hosts the `[[service]]` block) must be standing; C21 is
  *additive Phase-1* over the Phase-0 substrate (spec §4). T6 also needs C19 (beads) + C23 (event bus) so
  the fail-open path has a source-of-truth to fall back to.
- **Critical path:** **T1 → T2 → T3** is the gating chain. T3's **O(1)-branch proof (AC-4)** is the single
  most load-bearing check — **C49 counterfactual replay** ("most significant invention") and self-healing
  investigations are unbuildable if branching is not actually O(1). Until T3 passes, every "branching/dedup"
  claim is provisional (G11 thread).
- **Downstream gated by T7 (seam freeze):** **C22** (registry bundle → I7 + turn-record), **C24** (bridge →
  I1/I2 ingest + the AC-7 idempotency property for back-pressure), **C49** (→ I5 branch + I6 replay),
  **C36/C37/C38** (P11 loop → I6 replay/retrieve). C22 and C49 are explicitly named critical-path dependents
  (inventory line 123).

## 3. Parallelization

C21 fans out cleanly once the service is up (T2):
- **After T2:** **T3 (CAS/DAG/branch)**, **T4 (performance)**, **T5 (registry mechanism)**, and **T7 (seam
  freeze)** are independent workstreams — none depends on another's result. T6 additionally needs
  beads/event-bus up but is otherwise independent.
- **Within T3:** the four assertions (dedup AC-2, replay AC-3, O(1)-branch AC-4, no-OTLP AC-8) are
  independent and can be authored in parallel.
- **Cross-component:** C22's *bundle design* can proceed in parallel with C21's T1–T6 against the T7-frozen
  registry seam (I7) + turn-record stub; C24's *delivery design* can proceed against the frozen ingest seam
  (I1/I2) + the AC-7 idempotency guarantee — both before C21's conformance fully passes, since they build
  against stubs.

## 4. Interfaces-first / contract milestones

Freeze early (T7) so dependents build against stubs:
- **M1 — Version pin published (after T1):** exact CXDB version/commit, so every downstream spec pins the
  same store.
- **M2 — Ingest seam frozen (T7):** I1 (binary :9009) + I2 (HTTP :9010) — which path C24's bridge uses
  (OQ-4) + the AC-7 idempotency guarantee → unblocks **C24**.
- **M3 — Branch + replay seam frozen (T7):** I5 (O(1) branch) + I6 (replay/retrieve) → unblocks **C49** and
  **C36/C37/C38**.
- **M4 — Registry seam + turn-record frozen (T7/§4):** I7 (`{bundle_id,type,version}` register/resolve) +
  the turn-record [FAITHFUL-FILL] → unblocks **C22** (the G17 split seam).

## 5. Risks & de-risking order

Retire in this order (highest uncertainty first):
1. **O(1) branching is real (AC-4, blocker for C49).** Spike T1→T2→T3 first: stand CXDB up and prove a fork
   at depth N is constant-time with no history copy. If branching is *not* O(1), C49 ("most significant
   invention", largely unsolved — G19) loses its foundational primitive and the self-optimization layer
   reorganizes. → OQ-3, top of review-log.
2. **G11 thread — content-addressing + performance claims unverified.** T3 (dedup) + T4 (p50<1ms / sub-ms
   retrieval) exercise the upstream assumptions against a real binary before C24/C36–C38 rely on volume.
3. **G17 — registry/schema split.** T5 proves a v4 bundle *can* be registered; the *content* defers to C22.
   Freeze the C21/C22 seam (OQ-1) before C22 builds.
4. **G33 — store-down behaviour.** T6 proves fail-open + idempotency; the buffer/back-pressure design is
   C24's. Confirm the fail-open reading (OQ-2) — does P11/P12 volume need replication v4 never specs?
5. **§14 small-team / lock-in.** Pin the version (T1) and keep integration behind I1–I8 so a fork (Apache
   2.0) is a seam-swap, not a rewrite.

## 6. Definition of done

**Per-component DoD (sweep-1 altitude):**
- A pinned CXDB version is recorded and stands up as a Phase-1 `[[service]]` exposing :9009 + :9010 with the
  `turns.log`/`blobs.pack`/`registry/` layout (AC-1), alongside the Gas City substrate.
- The CXDB-conformance pack passes AC-2…AC-8 against the pinned binary: BLAKE3 dedup; turn-DAG replay;
  **O(1) branch (cost independent of depth)**; registry mechanism holds + resolves a v4 bundle; p50<1ms /
  sub-ms retrieval; fail-open + idempotent ingest; no OTLP. (**Resolves G11 content-addressing/branching
  operationally; addresses G17 store-side and G33 store-side; defers the v4 schema bundle to C22 and the
  bridge back-pressure to C24.**)
- The store seams (I1–I8) + the §4 turn-record [FAITHFUL-FILL] are frozen and published so C22/C24/C49/
  C36–C38 build against stubs (M1–M4).

**Per-task DoD:** each Tn meets its mapped acceptance criterion (T2→AC-1, T3→AC-2/3/4/8, T4→AC-6, T5→AC-5,
T6→AC-7, T7→M2–M4) and updates the spec's Open Questions / review-log as items close. **T3's AC-4 (O(1)
branch) is the gating exit criterion** — it must pass before C49/C22/C24 are unblocked.
