# C21 — CXDB trajectory store  (Spec, Track B)

> Source: AI-CONTEXT §5 (CXDB content-addressed trajectory store: §5.1 metadata, §5.2 ingestion API two-protocol, §5.3 turn model + BLAKE3 Blob CAS + `{bundle_id,type,version}` type system + storage layout, §5.4 bridge impedance ranking, §5.5 what CXDB adds over JSONL incl. perf contract), §4 (memory-layer principle 10), §11 (decisions: install CXDB Phase 1, raw-API-bodies bridge, skip OTLP path), §15 (open: Kilroy integration shape, repo-inspection residual); README Part 4 P10/P11/P12 "Gas City placement" cells (CXDB substrate, counterfactual replay O(1) branching), Part 6 Phase 1 (install CXDB + build bridge), §552 (Gas City single-point-of-failure framing applied to OSS stack); F-MODE-COVERAGE §2 (F10, F16), §6 (F11, F61), §7 (F54), §1 (F50 lives in C22); _meta component-inventory C21 row (depends C01; gaps G17, G33; foundational); _meta gaps G17 (no schema for core stores), G33 (no partial/cascading OSS-stack failure story), G11 (touched: unverified third-party dependency).
> Inventory ID: C21   Kind: data-store   Status: sweep-1
> Deltas: DELTA-01 (CXDB wrapped behind a thin `TrajectoryStore` port that C21 *is* — adopted CXDB is an implementation, not an axiom; **bounds the swap-cost / blast radius of the G11/G33 single-vendor bet and preserves the Apache-2.0 fork option — it does not "retire" the bet, since the real fallback is the fork; port thickness is OQ1**), DELTA-02 (ingest is **append-idempotent by content+parent**, not at-least-once-blind — the bridge seam C24 can retry without duplicating turns), DELTA-03 (the v4 trajectory type bundle is *named, versioned, and CI-pinned here* — `softwarefactory.v4.trajectory` — partially resolving G17 for the CXDB half; full registry semantics deferred to C22. **RESOLVED (review-log D-2): one factory-owned reverse-DNS root with per-store sub-bundles — `softwarefactory.v4.trajectory` (CXDB turn types, here), `softwarefactory.v4.beads` (C20 bead types), `softwarefactory.v4.packs` (C02). Vendor `strongdm.*` and the merged-single-bundle option are dropped. C21 pins the trajectory bundle-id consistently with C22's registration mechanism.**), DELTA-04 (explicit **degraded-mode + durable spool** contract: when CXDB is down, ingestion does not block the run — events spool to the event bus C23 as the durable source of truth and replay on recovery; directly answers G33 **for the C23-sourced event class. NOTE: the raw-API-bodies path (the one v4 actually builds, AI-CONTEXT §5.4 #2) has no C23 record to spool — its durability is C24's client-side on-disk spool (G26/G27); DELTA-04 does not cover it. See OQ2.**), DELTA-05 (branch/replay is a **first-class C21 API surface** with a defined `BranchRef` + provenance turn, not an undocumented O(1) trick — makes C49 counterfactual-replay and C37 clustering buildable against a contract), DELTA-06 (retention/GC + integrity-verification contract: BLAKE3 self-verifying reads + a compaction story, since v4 claims TB-scale but never says how blobs are reclaimed or corruption is detected), DELTA-07 (read/query API is a **typed projection contract**, not "HTTP/JSON REST" hand-wave — defines the trajectory-walk + payload-fetch + branch-enumeration queries the loop components actually need).

## 1. Purpose & responsibility

C21 is **the content-addressed trajectory store**: the persistence layer that records the *conversation-shaped* history of every agent run as an immutable, deduplicated, branchable **turn DAG**, and lets downstream components walk it, fetch payloads by content hash, and fork it in O(1) for counterfactual replay. It is principle 10's "trajectory store" half (the bead work-graph C19 is the other half) and the substrate that the self-healing (P11) and self-optimization (P12) loops mine.

Concretely C21 owns four capabilities, exposed behind the `TrajectoryStore` port (DELTA-01):

1. **Content-addressed payload storage (Blob CAS).** Every payload (a request/response body, a tool result, an event) is serialized to msgpack, hashed with BLAKE3, and stored once. Identical payloads across turns/runs collapse to one blob → free dedup + tamper-evidence (AI-CONTEXT §5.3, §5.5).
2. **Turn-DAG structure.** The unit is a **turn**, each carrying a parent-turn pointer (DAG, not tree), a typed payload reference (`{bundle_id,type,version}` → blob hash), and attribution. Turns are append-only and immutable once written.
3. **O(1) branching + replay.** Forking from any turn is a new head pointer with a provenance marker (DELTA-05) — no history copy. This is the primitive C49 (counterfactual replay) and the self-optimization variant tests stand on.
4. **Dual ingest + typed query.** Binary msgpack ingest (:9009, high-throughput writer) and HTTP/JSON (:9010, browsers/ad-hoc), per AI-CONTEXT §5.2; plus the typed-projection read API (DELTA-07) downstream loops query.

What C21 is **NOT**:
- **Not** the *type registry*. The `{bundle_id,type,version}` *schema-resolution* semantics (registering bundles, version negotiation, viewpoint tagging) are **C22**. C21 stores the triple on each turn and stamps the v4 bundle ID (DELTA-03); C22 owns what the triple *means* and how schemas are looked up.
- **Not** the *ingestion bridge*. Watching the `OTEL_LOG_RAW_API_BODIES` directory and posting to C21 is **C24** (a standalone tool-node binary). C21 defines the *server-side ingest contract* (idempotency, ordering, back-pressure response); C24 defines the *client-side* delivery/ordering/spool behavior at the seam.
- **Not** the *event bus*. C23 is the append-only JSONL ledger that is the *lowest-impedance source* feeding C21 (AI-CONTEXT §5.4). C23 is the run's durable linearization point; C21 is the richer, content-addressed, branchable projection of it. (DELTA-04 makes C23 the fallback durable store when C21 is down.)
- **Not** a *span/trace store*. CXDB is explicitly positioned *against* OTel (AI-CONTEXT §5.3, §5.4) — span trees are not turn DAGs. LangFuse (C27) holds OTel-shaped traces; C21 holds conversation-shaped turns. No OTLP receiver (decision §11, README "skip OTLP→CXDB path").
- **Not** the *replay driver*. C49 is the agent/component that *uses* C21's branch API to re-run a trajectory from a midpoint; C21 only provides the O(1) fork + the means to read the branched prefix back.
- **Not** the bead/work-graph (C19) — that is the typed task ledger; a bead may *reference* a turn, but C21 stores no dependency/status semantics.

## 2. Context & dependencies

- **Depends on (inventory): C01** — the runtime substrate hosts C21's storage lifecycle (mount, open/close, supervised restart) the same way it hosts C19/C23; C01 provides the `created_by` attribution stamp (C41) that C21 records on every turn. *Note: C21 runs as an external process (Rust server, AI-CONTEXT §5.1) that C01 supervises and routes to, not an in-process library — this is the DELTA-01 port boundary.*
- **Tightly coupled sibling: C22** (type registry) — C22 resolves the `{bundle_id,type,version}` triples C21 stores; they co-specify the v4 bundle (DELTA-03). Build-order: the triple *format* must freeze before either ships (plan §4).
- **Primary writers:** **C24** (telemetry→CXDB bridge, the recommended raw-API-bodies path) and **C23** (event-bus JSONL, the lowest-impedance path per AI-CONTEXT §5.4). Both write through C21's ingest contract (DELTA-02 idempotency).
- **Primary readers / downstream consumers:** **C49** (counterfactual replay — O(1) branch API, DELTA-05), **C36** (numeric anomaly detection over trajectory metrics), **C37** (trajectory embedding & clustering — walks turn DAGs to embed), **C38** (diagnosis agent — queries clustered failures via C21 read API). These are the loop components that make C21 load-bearing.
- **Sits at:** the Persistence & Memory subsystem, one layer above C01, beside C19 (work-graph) and C23 (event bus). It is foundational: every observability/clustering/replay/loop-closure path reads or writes here.

## 3. Interfaces / contracts

Named-and-described (sweep 1; concrete msgpack/JSON schemas, port wire formats, and the conformance suite in sweep 2). All operations are offered behind the **`TrajectoryStore` port** (DELTA-01) so the adopted CXDB server is swappable.

**Inbound — Ingest (writers: C24, C23):**
- `AppendTurn(parent_ref, typed_payload, attribution) → TurnRef` — serialize payload to msgpack, BLAKE3-hash → blob (dedup if present), write an immutable turn pointing at `parent_ref`. **Idempotency invariant (DELTA-02):** the dedup identity `TurnRef` is a deterministic function of `(parent_ref, blob_hash, type_triple)` — the content + position — and **must be invariant under the *retrying* actor**; `attribution`/`created_by` is recorded *on* the turn as metadata but is **not** part of the dedup key. (Folding the actor into the key would mint a duplicate when DELTA-04 replay-on-recovery re-appends under a recovery actor, or when C24 restarts under a different process identity — defeating retry-safety.) Re-appending the same logical turn returns the existing `TurnRef`, never a duplicate. This is what lets C24 retry safely after a partial failure (G33). *(Exact key composition frozen at sweep 2.)* Pre: `parent_ref` exists or is the genesis sentinel; `type_triple` is registrable in C22's bundle. Post: blob stored once; turn durable; `created_by` recorded.
- `PutBlob(bytes) → BlobHash` / implicit within `AppendTurn` — content-address a payload independently (used when a large payload is referenced by multiple turns).
- Back-pressure response (DELTA-04): on overload/unavailability the ingest contract returns an explicit `BUSY`/`UNAVAILABLE` signal (not a silent drop), which C24 honors by spooling to C23 and retrying — the seam where G33 degradation is defined.

**Inbound — Read / Query (readers: C49, C36, C37, C38, C22 UI):**
- `GetTurn(turn_ref) → Turn` and `GetBlob(blob_hash) → bytes` — point reads; BLAKE3 self-verifies on read (DELTA-06 integrity).
- `WalkTrajectory(head_ref, opts) → TurnStream` — walk the DAG from a head back to genesis (or forward over a known branch); the primitive C37 embeds and C49 replays. Typed projection (DELTA-07): each turn yields its resolved `{bundle_id,type,version}` so readers render structurally, not as raw JSON.
- `EnumerateBranches(turn_ref) → [BranchRef]` — list forks off a turn (DELTA-05), so the optimization loop can see the variant fan-out.
- `Query(typed_filter) → [TurnRef]` — typed selection over turns (e.g., "all turns of type `softwarefactory:JudgeVerdict` since seq N") for C36/C38. HTTP/JSON on :9010.

**Inbound — Branch (writers: C49, self-optimization):**
- `Branch(from_turn_ref, reason) → BranchRef` — O(1) fork: a new head pointing at `from_turn_ref` plus a provenance turn recording *who/why* the branch was created (DELTA-05). No history copy. Post: original trajectory unmodified (immutability preserved); new branch shares the prefix's blobs (dedup).

**Outbound (what C21 requires):**
- Storage lifecycle from **C01** (mount the `turns.log` / `blobs.pack` / `registry/` layout, AI-CONTEXT §5.3; supervised restart).
- Type-triple resolution from **C22** (validate/resolve `{bundle_id,type,version}` on write and read).
- The `created_by` actor from **C41** via C01 on every `AppendTurn`/`Branch`.
- The durable spool target **C23** when degraded (DELTA-04).

**Invariants:**
- **Immutability + content-address:** a turn and its blobs are write-once; the BLAKE3 hash *is* the address; equal bytes ⇒ one blob (dedup) ⇒ stable references (F11 — renumbering can't break references because there are no numbers, only hashes).
- **Append-idempotent (DELTA-02):** identical logical appends collapse; retries are safe.
- **Branch-isolating (DELTA-05):** branching never mutates the source trajectory.
- **Attribution-total:** every turn carries `created_by` (P9), inherited from C01 — feeds F14 attribution and F54 RSI-objective-drift audit.
- **Self-verifying reads (DELTA-06):** a read recomputes BLAKE3 and rejects a blob whose bytes don't match its address (tamper/corruption detection).
- **GC referential integrity (DELTA-06):** compaction MUST NOT sweep any blob reachable from a retained turn (including every branch head and all retained-by-policy turns). "Retained turn ⇒ retained payload blob" is a hard rule, so the keep-turns-forever audit trail (F54) can never develop a dangling payload reference.
- **Performance contract (AI-CONTEXT §5.5):** p50 < 1 ms append for 10 KB payloads; sub-ms retrieval at TB-scale. Treated as an acceptance target, not an assumption (G11/DELTA-01).

## 4. Data model / state

C21 owns the trajectory store's *physical* state; C22 owns the *schema* meaning of the type triples.

- **Blob CAS** (`blobs.pack` + index): `BlobHash (BLAKE3) → msgpack bytes`, write-once, dedup-on-write. The dedup and tamper-evidence layer.
- **Turn log** (`turns.log`): append-only sequence of immutable turns. Each turn: `{ turn_ref, parent_ref, type_triple:{bundle_id,type,version}, payload: BlobHash, created_by, seq, branch_id }`. DAG via `parent_ref`; multiple turns may share a parent (the branch points).
- **Branch table** (DELTA-05): `BranchRef → { head_turn, base_turn, reason, created_by, created_at }` — the O(1) fork records; each branch is a head pointer + provenance, sharing the base prefix's turns/blobs.
- **Type-bundle pin** (DELTA-03): the v4 trajectory bundle ID `softwarefactory.v4.trajectory` and the set of turn types v4 registers (e.g. `softwarefactory.v4.trajectory:RawApiTurn`, `:ToolResult`, `:EventBusRecord`, `:JudgeVerdict`) — *named here, registration-owned by C22*, CI-pinned so cold-agent commands (G17: `gc bd find --type …` analog) resolve.
- **Storage layout** (AI-CONTEXT §5.3): `turns.log`, `blobs.pack`, `registry/` — **no Postgres/Redis/Kafka**. A single-process Rust server's files, hosted on C01's mount.
- **Consistency model:** an append is durable once fsync'd to `turns.log`; reads are linearizable per branch head. C23 (event bus) is the *cross-component* linearization point — a turn is "real for the loop" once its source event is sequenced on C23, with C21 the downstream content-addressed projection (DELTA-04 makes this ordering load-bearing for replay-on-recovery).
- **Retention/GC** (DELTA-06): blobs are reachable-from-turn; a compaction pass marks-and-sweeps unreachable blobs after a configurable retention window. Turns themselves are retained per policy (trajectories are the audit trail; default = keep). Defined as a contract because v4 claims TB-scale but is silent on reclamation.

## 5. Behavior

Key flows (sweep 1 prose; sweep 2 = Mermaid sequence/state diagrams):

- **Ingest (happy path):** C24 reads a raw-API body → `AppendTurn(parent=session-head, payload, created_by)` over binary :9009 → C21 msgpack-serializes, BLAKE3-hashes, dedups the blob, appends the immutable turn, returns `TurnRef`. Parent-chain reconstructed via `session.id` (AI-CONTEXT §5.4). p50 < 1 ms target.
- **Ingest under failure (DELTA-04, the G33 answer):** C21 unavailable or returns `BUSY` → C24 does **not** block the agent run; it writes the record to C23 (event-bus JSONL, the durable source) and marks it pending. On C21 recovery, a replay pass drains pending C23 records through `AppendTurn`; idempotency (DELTA-02) makes the drain safe even if some appends had partially landed. Net: a CXDB outage degrades *trajectory richness* (no live content-addressed query) but never loses committed work and never stalls the run.
- **Branch + replay (DELTA-05, feeds C49):** C49 picks a midpoint turn → `Branch(from_turn, "variant: model=floor")` → O(1) new `BranchRef` sharing the prefix → C49 drives a fresh agent run whose turns append onto the branch head. The original trajectory is untouched; the two share all prefix blobs (dedup). Self-optimization variant tests are N branches off one base.
- **Trajectory mining (feeds C37/C36/C38):** C37 `WalkTrajectory(head)` → turn stream → embed → cluster; C36 `Query(type=metric)` for numeric anomaly; C38 `Query` + `WalkTrajectory` over a failure cluster for root-cause. Typed projection (DELTA-07) means readers get structured payloads, not raw bytes.
- **Cold start / restart:** C01 supervises the CXDB process; on restart C21 reopens `turns.log`/`blobs.pack`/`registry/`, replays any pending C23 spool (DELTA-04), self-verifies blob integrity lazily on read (DELTA-06).

## 6. Failure modes & handling

| F-mode / gap | Risk | C21 handling |
|---|---|---|
| **G17 (blocker): no schema for core stores** | The v4-specific CXDB type bundle `{bundle_id,type,version}` is never specified; cold agents reference types that don't exist. | **DELTA-03:** C21 *names + CI-pins* the v4 trajectory bundle `softwarefactory.v4.trajectory` and its turn types; **C22** owns the registration/resolution semantics. Partially resolves G17 (CXDB half); bead-schema half is C20 (bundle `softwarefactory.v4.beads`, D-2/D-3). The triple format is the contract frozen first (plan §4). |
| **G33 (major): no partial/cascading OSS-stack failure story** ("what happens when CXDB is down mid-run?") | A single-process, 3-person-team Rust store sits on the run's hot path; an outage could stall every agent or lose trajectory. | **DELTA-04 + DELTA-02:** ingest is non-blocking with a durable C23 spool fallback + idempotent replay-on-recovery. CXDB down ⇒ degrade richness, never lose committed work, never stall the run. This is the concrete G33 answer for C21's seam. |
| **G11 (blocker, touched): unverified third-party dependency** | No author has run CXDB; perf contract (p50<1 ms, TB-scale) is asserted (AI-CONTEXT §5.1, §15). | **DELTA-01:** wrap CXDB behind the `TrajectoryStore` port so adoption is a swappable implementation; treat the perf contract as an *acceptance target* the conformance suite measures (§8), not an axiom. Apache-2.0 ⇒ fork-on-failure is always available (README §618). |
| **F10: findings disappear into chat** | Diagnostic findings lost to ephemeral conversation. | Content-addressed trajectory store *is* the v4 mechanism (F-MODE §2): every turn is durable, addressable, queryable — findings become turns, not lost chat. |
| **F11: renumbering breaks references** | IDs shift; references rot. | BLAKE3 content-addressing makes references immutable by construction (F-MODE §6) — the address *is* the content; nothing to renumber. |
| **F16: resume-fidelity decay** (Partial) | Replayed trajectory drifts from original; KV-cache loss inherent. | Turn-DAG replay (DELTA-05) reconstructs the *recorded* trajectory exactly (immutable turns); residual = model KV-cache loss is inherent and out of C21 scope (F-MODE §2 "Partial"). C21 guarantees byte-faithful payload replay, not model-state replay. |
| **F61: context fragmentation across agents** (Partial) | Multi-agent runs take divergent local views. | Shared C21 store is the single trajectory source of truth (F-MODE §6); agents read a common DAG. Residual = agents still decide locally (out of scope). |
| **F54: RSI goal subversion over cycles** (Partial) | Self-optimization drifts the objective via prompt-injection over branches. | Immutable content-addressed history + branch provenance (DELTA-05) gives the Healer (C38) an audit-able, tamper-evident objective trail to detect drift (F-MODE §7); residual significant, requires audit discipline. |
| Blob corruption / tamper | Disk rot or malicious edit of `blobs.pack`. | **DELTA-06:** self-verifying reads recompute BLAKE3 and reject mismatched blobs; corruption is detected at read, not silently served. |
| Storage exhaustion at TB-scale | v4 claims TB-scale, silent on GC. | **DELTA-06:** mark-and-sweep compaction of unreachable blobs after a retention window; turns retained per policy. |

## 7. Cross-cutting

- **Security:** content-addressing + self-verifying reads (DELTA-06) make the trajectory tamper-evident — the substrate for F54 RSI-drift audit and F14 attribution. Every turn carries `created_by` (P9). Read access to trajectories is a holdout-leakage surface (F28 lives in C-scenario components, but C21 should honor C01/C43 isolation on who may `Query`/`WalkTrajectory` a given bundle).
- **Cost/scale:** dedup is the cost lever — long repeated payloads (system prompts, repeated tool outputs) stored once (AI-CONTEXT §5.5); O(1) branching means variant tests cost O(new turns), not O(trajectory). Perf ceiling is the single Rust process (§5.1) — sweep-2 must size the :9009 writer throughput against the C24 ingest rate.
- **Observability:** C21 is itself the observability substrate for the self-healing loop; its own health (`UNAVAILABLE`/`BUSY` signals, spool depth, compaction lag) must surface to C01 `Health()` so the loop can see when it is degraded (DELTA-04).
- **Ops:** version-pin the CXDB binary (G11 discipline, mirrors C01 DELTA-02); the `turns.log`/`blobs.pack`/`registry/` layout backs up as plain files (no Postgres/Redis/Kafka to operate — AI-CONTEXT §5.3). Degraded-mode + spool-replay (DELTA-04) is the runtime ops contract; compaction (DELTA-06) is the scheduled-maintenance contract.

## 8. Acceptance criteria & test strategy

1. **Ingest + dedup (core):** appending two turns with identical 10 KB payloads stores exactly one blob; both turns resolve to the same `BlobHash`; `GetBlob` round-trips bytes-faithfully.
2. **Idempotency (DELTA-02):** replaying the same logical `AppendTurn` N times yields one turn and one `TurnRef` — asserted with a forced double-delivery from a simulated C24 retry.
3. **O(1) branch isolation (DELTA-05):** `Branch` from a midpoint creates a new `BranchRef` in constant time independent of trajectory length; subsequent appends to the branch do not mutate the source trajectory (verified by re-walking the original head); branch shares prefix blobs (no blob duplication).
4. **Degraded-mode + replay (DELTA-04, G33):** kill CXDB mid-run → C24 ingestion spools to C23 and the agent run continues; restart CXDB → pending C23 records drain via idempotent replay with zero duplicate turns and zero lost records.
5. **Integrity (DELTA-06):** flip a byte in `blobs.pack` → the next `GetBlob`/`WalkTrajectory` over that blob is rejected (BLAKE3 mismatch), not silently served.
6. **Type-triple pin (DELTA-03, G17):** every turn carries a `{bundle_id,type,version}` registrable in C22's `softwarefactory.v4.trajectory` bundle; an unregistered type is rejected at `AppendTurn`; a cold-agent `Query(type=…)` over a pinned type resolves.
7. **Port swappability (DELTA-01):** a stub `TrajectoryStore` (in-memory) passes the same conformance suite, proving readers/writers (C24, C49, C37) code against the port, not CXDB internals.
8. **Performance contract (G11):** measured p50 append < 1 ms for 10 KB payloads and sub-ms point retrieval on a ≥100 GB store — **measured and recorded as a de-risking datum against the asserted §5.5 claim; a miss is an integrator finding (fork / accept / tune the adopted store), not a hard build gate** (C21 cannot patch CXDB's internals). Full TB-scale is sweep-3.

## 9. Open questions

- **OQ1 (→ review-log, top):** How thick is the `TrajectoryStore` port (DELTA-01) before it re-implements CXDB? CXDB's turn-DAG + Blob-CAS + branch semantics are idiosyncratic; a faithful-but-thin port may be infeasible, degrading DELTA-01 to "document the lock-in + keep the fork option." This is the load-bearing optimization risk and mirrors C01 OQ1. Needs direct CXDB repo inspection (AI-CONTEXT §15: "need direct repo inspection for transfusion").
- **OQ2:** Is the C23→C21 spool-replay ordering (DELTA-04) the *only* durable path, or does C24's recommended raw-API-bodies path also need its own on-disk spool? Determines whether G33 degradation is owned at the C21↔C23 seam or split across C24. Co-spec with C24 (which owns the bridge's client-side spool, G26/G27).
- **OQ3:** Exact split of the `{bundle_id,type,version}` contract between C21 (stores/pins the triple) and C22 (resolves/version-negotiates) — must freeze the triple *format* before either ships (DELTA-03). Co-spec with C22.
- **OQ4 (→ G11 residual):** The p50<1 ms / TB-scale perf contract is unverified upstream (§5.1, §15). Acceptance #8 is the de-risking action; until measured, every loop component sizing assumption (C37 clustering throughput, C49 replay cost) is provisional.
- **OQ5:** Retention/GC policy defaults (DELTA-06) — are trajectories ever deleted, or only blobs compacted? Audit-trail (F54) argues keep-turns-forever; cost argues windowed. Needs a policy decision tied to the holdout/audit requirements.
