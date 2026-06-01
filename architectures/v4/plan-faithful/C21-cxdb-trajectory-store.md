# C21 — CXDB Trajectory Store  (Build Plan, canonical track)

> Source / Spec ref: spec/C21-cxdb-trajectory-store.md
> Sources cited in spec: README §Part 4 (lines 122, 241–242, 252, 261, 274–278, 290, 302), §Part 6 Phase 1 (lines 388–397), §Part 7 (lines 500, 541); AI-CONTEXT §5.1–§5.5, §10, §11, §13.2, §14, §15.2; inventory C21 row (line 33) + critical-path notes (lines 107, 123); gaps G17, G33 (and the G11 content-addressing thread).
> Binding decisions: **D-2** (`softwarefactory.v4.trajectory`), **D-11** (two-sink anti-edge), **D-12** (cross-referenced per-spec).

## 1. Work breakdown

C21 is *adoption + verification + seam-freeze*, not authorship — CXDB stays upstream OSS (README line
500). Sweep-2 adds: concrete turn/payload schemas, the session-index chaining rule, the branch contract,
the two-sink anti-edge test, and the full AC-S2 conformance suite.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| **T1** Source & pin CXDB | Obtain CXDB from `github.com/strongdm/cxdb` (AI-CONTEXT §15.2); pick a version; record commit+pin (mirrors C01 INV-1). Note small-team/abandonment risk (§14). | M | C01 standing |
| **T2** Stand up service | Expose :9009 (binary) + :9010 (HTTP); register the `[[service]]` block in `city.toml` (AI-CONTEXT §13.2 lines 558, 579); confirm `turns.log`/`blobs.pack`/`registry/` layout (AC-1). | S | T1 |
| **T3** Conformance: CAS + DAG + branch | Conformance pack asserting AC-2 (BLAKE3 dedup), AC-3 (turn-DAG replay), AC-4 (**O(1) branch — cost independent of depth**), AC-8 (no OTLP). Wire-level: AC-S2-I1, AC-S2-I2, AC-S2-B1, AC-S2-B2. **The primitive C49 depends on; verify explicitly.** | L | T2 |
| **T4** Conformance: performance | Assert AC-6 (p50<1ms append/10KB; sub-ms retrieval TB-scale) against the real pinned binary (de-risks the G11/upstream perf assumption). | M | T2 |
| **T5** Registry-mechanism proof | Register a *placeholder* v4 `{bundle_id="softwarefactory.v4.trajectory",type,version}` bundle into `registry/` and resolve it on read with structural projection (AC-5, AC-S2-N1). **Proves the mechanism C22 fills; addresses G17 store-side. Verifies D-2 namespace enforcement (E6/AC-S2-N1).** | M | T2 |
| **T6** Fail-open + idempotency proof | Assert AC-7: a CXDB-down run continues on beads+events (no crash); re-posting an accepted turn is a no-op (BLAKE3 idempotency + §4.4 dedup, AC-S2-I1). **Addresses G33 store-side; the property C24's buffer relies on.** | M | T2, C19/C23 standing |
| **T7** Two-sink anti-edge test | Assert AC-S2-D1: an OTLP-typed write (any bundle_id ≠ `softwarefactory.v4.trajectory`) is rejected at the store level (E2/E9/INV-7). **Enforces D-11/D-12 at the store — not just at the routing layer (C26/C24). Must pass before C22/C24 wire up.** | S | T2 |
| **T8** Session-chaining conformance | Assert AC-S2-C1/C2/C3: sequential appends with same `session_id` chain automatically; explicit `parent_turn_id` overrides the index; new session produces null parent (§3.2 rule; G26 resolution at C21's side). | M | T2 |
| **T9** Turn-record / field conformance | Assert AC-S2-T1/T2/T3/T4: round-trip of all Req=R fields; missing `session_id` / `created_by` rejected (E3); BLAKE3 mismatch rejected (E4); orphaned parent rejected (E5). | M | T2 |
| **T10** Freeze store seams | Enumerate + freeze I1–I8 (binary :9009, HTTP :9010, turn-append §3.1, session-chaining §3.2, branch §3.3, registration §3.4, Blob CAS put/get, replay/retrieve, `[[service]]` lifecycle) + the §4.1 turn-record so C22/C24/C49 build against stubs. | M | T2 |

## 2. Dependency graph

- **Upstream of C21:** **C01** (the substrate that hosts the `[[service]]` block) must be standing; C21 is
  *additive Phase-1* over the Phase-0 substrate (spec §4). T6 also needs C19 (beads) + C23 (event bus) so
  the fail-open path has a source-of-truth to fall back to.
- **Critical path:** **T1 → T2 → T3** is the gating chain. T3's **O(1)-branch proof (AC-4 / AC-S2-B1)**
  is the single most load-bearing check — **C49 counterfactual replay** ("most significant invention") and
  self-healing investigations are unbuildable if branching is not actually O(1). Until T3 passes, every
  "branching/dedup" claim is provisional (G11 thread).
- **T7 (two-sink anti-edge)** should run alongside T3/T4 — it is low-cost (a negative-path test) and
  blocks the D-11/D-12 invariant from being taken on faith at the routing layer only.
- **Downstream gated by T10 (seam freeze):** **C22** (registry bundle → I7 + turn-record), **C24** (bridge
  → I1/I2 ingest + session-chaining rule §3.2 + the AC-7 idempotency property for back-pressure; OQ-4
  resolution for :9009 vs :9010), **C49** (→ I5 branch + I6 replay), **C36/C37/C38** (P11 loop → I6
  replay/retrieve). C22 and C49 are explicitly named critical-path dependents (inventory line 123).

## 3. Parallelization

C21 fans out cleanly once the service is up (T2):
- **After T2:** **T3 (CAS/DAG/branch)**, **T4 (performance)**, **T5 (registry mechanism)**, **T7
  (two-sink anti-edge)**, **T8 (session chaining)**, **T9 (turn-record fields)**, and **T10 (seam
  freeze)** are all independent workstreams — none depends on another's result.
- **Within T3:** the four assertions (dedup AC-2, replay AC-3, O(1)-branch AC-4, no-OTLP AC-8) are
  independent and can be authored in parallel.
- **T7 parallels T3:** the anti-edge test is a simple negative-path assertion that does not need the
  dedup/branch proofs to complete first.
- **Cross-component:** C22's *bundle design* can proceed in parallel with C21's T1–T9 against the
  T10-frozen registry seam (I7) + turn-record stub; C24's *delivery design* can proceed against the frozen
  ingest seam (I1/I2) + the session-chaining rule (§3.2) + the AC-7 idempotency guarantee — both before
  C21's conformance fully passes, since they build against stubs.

## 4. Interfaces-first / contract milestones

Freeze early (T10) so dependents build against stubs:
- **M1 — Version pin published (after T1):** exact CXDB version/commit, so every downstream spec pins the
  same store.
- **M2 — Ingest seam frozen (T10):** I1 (binary :9009) + I2 (HTTP :9010) + the `TurnAppend` message
  shape (§3.1) + the session-chaining rule (§3.2) — which path C24's bridge uses (OQ-4) + the AC-7
  idempotency guarantee + two-sink rejection rule (INV-7/E2) → unblocks **C24**.
- **M3 — Branch + replay seam frozen (T10):** I5 (O(1) branch, §3.3 `BranchRequest`/`BranchResponse`) +
  I6 (replay/retrieve) → unblocks **C49** and **C36/C37/C38**.
- **M4 — Registry seam + turn-record frozen (T10/§4.1):** I7 (`{bundle_id="softwarefactory.v4.trajectory",
  type_name, version}` register/resolve, §3.4) + the turn-record [FAITHFUL-FILL] (§4.1) → unblocks **C22**
  (the G17 split seam). D-2 namespace ruling baked in at M4.

## 5. Risks & de-risking order

Retire in this order (highest uncertainty first):
1. **O(1) branching is real (AC-4 / AC-S2-B1, blocker for C49).** Spike T1→T2→T3 first: stand CXDB up
   and prove a fork at depth N is constant-time with no history copy. If branching is *not* O(1), C49
   ("most significant invention", largely unsolved — G19) loses its foundational primitive and the
   self-optimization layer reorganizes. → OQ-3, top of review-log.
2. **G11 thread — content-addressing + performance claims unverified.** T3 (dedup) + T4 (p50<1ms / sub-ms
   retrieval) exercise the upstream assumptions against a real binary before C24/C36–C38 rely on volume.
3. **OQ-4 — :9010 vs :9009 under P11/P12 load.** T4 (performance) feeds this: if :9010 cannot sustain
   bridge-volume throughput, C24 must use the binary client (Go library on :9009). C21's seam is
   symmetric; the decision belongs to C24 at its M2, informed by T4 measurements.
4. **G17 — registry/schema split.** T5 proves a v4 bundle *can* be registered under `softwarefactory.v4.trajectory`
   (D-2 namespace); the *content* defers to C22. Freeze the C21/C22 seam (OQ-1, M4) before C22 builds.
5. **D-11/D-12 two-sink anti-edge integrity.** T7 (AC-S2-D1) verifies the anti-edge is enforced at
   the store level, not just relied upon at the routing layer. Low-cost; run alongside T3.
6. **G33 — store-down behaviour.** T6 proves fail-open + idempotency; the buffer/back-pressure design is
   C24's. Confirm the fail-open reading (OQ-2) — does P11/P12 volume need replication v4 never specs?
7. **§14 small-team / lock-in.** Pin the version (T1) and keep integration behind I1–I8 so a fork
   (Apache 2.0) is a seam-swap, not a rewrite.

## 6. Definition of done

**Per-component DoD (Sweep-2 altitude):**
- A pinned CXDB version is recorded and stands up as a Phase-1 `[[service]]` exposing :9009 + :9010 with
  the `turns.log`/`blobs.pack`/`registry/` layout (AC-1), alongside the Gas City substrate.
- The CXDB-conformance pack passes AC-1…AC-8 + AC-S2-N1…AC-S2-D2 against the pinned binary:
  - BLAKE3 dedup (AC-2 / AC-S2-I1/I2)
  - Turn-DAG replay (AC-3 / AC-S2-T1)
  - **O(1) branch, cost independent of depth** (AC-4 / AC-S2-B1/B2)
  - Registry mechanism holds + resolves a v4 `softwarefactory.v4.trajectory` bundle (AC-5 / AC-S2-N1)
  - p50<1ms / sub-ms retrieval measured and recorded (AC-6 / T4)
  - Fail-open + idempotent ingest (AC-7 / AC-S2-I1)
  - No OTLP (AC-8 / E9/E2)
  - **Two-sink anti-edge: OTLP/non-trajectory writes rejected at the store (AC-S2-D1/D2)** — enforces
    D-11: "NEVER to CXDB (two-sink anti-edge holds)" + D-12: "Collector✗→CXDB anti-edge at C26"
  - Session chaining rule (AC-S2-C1/C2/C3): G26 C21-side resolution
  - Required turn fields enforced (AC-S2-T2/T3/T4)
  - D-2 namespace enforced (AC-S2-N1/N2/N3)
- The store seams (I1–I8) + the §4.1 turn-record + the §3.1–§3.4 contracts are frozen and published so
  C22/C24/C49/C36–C38 build against stubs (M1–M4).
- OQ-4 (:9009 vs :9010 ingest path) is measured by T4 and a recommendation handed to C24 for its M2
  decision. C21 does not freeze this choice — C24 does.
- Open questions OQ-1/OQ-2/OQ-3 mirrored to review-log with current status; OQ-4 handed to C24.

**Per-task DoD:** each Tn meets its mapped acceptance criterion (T2→AC-1, T3→AC-2/3/4/8+AC-S2-I1/I2/B1/B2,
T4→AC-6, T5→AC-5+AC-S2-N1, T6→AC-7+AC-S2-I1, T7→AC-S2-D1/D2, T8→AC-S2-C1/C2/C3,
T9→AC-S2-T1/T2/T3/T4, T10→M2–M4) and updates the spec's Open Questions / review-log as items close.
**T3's AC-4 (O(1) branch) is the gating exit criterion** — it must pass before C49/C22/C24 are unblocked.
