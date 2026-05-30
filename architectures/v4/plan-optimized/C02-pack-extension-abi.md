# C02 — Pack & tool-node ABI  (Build Plan, Track B)

> Source / Spec ref: [`spec-optimized/C02-pack-extension-abi.md`](../spec-optimized/C02-pack-extension-abi.md)

## 1. Work breakdown

| id | description | size | prereqs |
|---|---|---|---|
| T1 | **ABI verification spike (G11/OQ1).** Install `gc`, run the `[[tool]] type="subprocess"` sketch (AI-CONTEXT §13.3); observe how Gas City actually delivers inputs and reads results from a tool node. Output: a note recording the *real* convention → decides whether §3b is define vs. conform-or-shim. | M | C01 install |
| T2 | **Freeze `ToolNodeRequest`/`ToolNodeResponse` JSON schemas** (DELTA-01/03): stdin envelope, stdout envelope, content-address-by-reference rule, stderr-for-diagnostics rule. | M | T1 |
| T3 | **Freeze the exit-code taxonomy** (0/1/2/3/≥124) and its mapping to runtime actions (commit/branch/abort/retry/kill) for C18/C40. | S | T2 |
| T4 | **Define `PackManifest` + `ToolNodeManifest` schemas** (DELTA-02): identity, semver, `abi_version` range, `imports`, `provides`, signature field, `transfused_from`, per-node `declared_capabilities`. | M | T1 |
| T5 | **Specify the ABI-version handshake + compat policy** (DELTA-05): additive-within-major, range negotiation, `AbiIncompatible` typed failure. | S | T2,T4 |
| T6 | **Specify the capability-declaration → grant seam** (DELTA-04): declared ∩ (C03/C43 policy) = effective grant; over-grant = load failure; breach = kill+attributed event. | M | T4; C03 seam; C43 seam |
| T7 | **Reference tool-node skeletons** in Go *and* Python (DELTA-06): each reads the request envelope, returns a response envelope, sets a taxonomy exit code. The language-parity proof. | M | T2,T3 |
| T8 | **Stub runtime harness:** a minimal invoker that builds a request, spawns a node, validates the response, exercises every exit code — so downstream packs build against C02 before C01 specifics settle. | M | T2,T3 |
| T9 | **No-fork falsifiability proof** (DELTA-07): express C24 (CXDB bridge), C33 (aggregator), C36 (Python anomaly node) as packs with zero Gas City Go imports; record fork-trigger criteria + escape-valve decision template. | M | T7,T8 |
| T10 | **Conformance suite** = acceptance criteria §8 as runnable tests (round-trip, exit codes, parity, stdout purity, handshake, capability enforcement, bundle integrity, attribution carriage). | L | T7,T8 |
| T11 | **Sweep-2 deepening:** Mermaid invocation sequence diagram, full schema files, error taxonomy doc, streaming/long-running node boundary (OQ4). | M | T2–T6 |

## 2. Dependency graph

- **Hard upstream:** C01 (the runtime that spawns nodes). C02 cannot be *verified* without a `gc` install (T1), though the *contract* (T2–T6) can be drafted against the §13.3 sketch in parallel with C01 standup.
- **Seam co-dependencies (not blocking, but co-designed):** C03 (pack = one `LayerSource`; capability-descriptor ownership — OQ3) and C43 (capability *enforcement* teeth — OQ2). These are *contract negotiations*, run as joint design touchpoints, not sequential blockers.
- **Critical path:** **T1 → T2 → T3 → T8 → T10**. The wire protocol + harness + conformance suite is the load-bearing spine; everything downstream (C17 and every pack) builds against the frozen T2/T3 output. T1 is the single highest-leverage unblock (it can invalidate define-vs-conform).
- **Downstream gated on C02 contract freeze (T2–T5):** C17 directly; then C10, C14, C15, C16, C24, C31, C33, C36, C37, C38, C44, C47, C48 — every pack-shaped component.

## 3. Parallelization

Once **T1** lands, three independent workstreams run concurrently:

1. **Wire-protocol stream:** T2 → T3 → T7 (skeletons) → T8 (harness). The spine.
2. **Bundle/manifest stream:** T4 → T5 (handshake) → T9 (no-fork proof). Independent of wire details until they meet at the manifest's `abi_version`.
3. **Isolation-seam stream:** T6, co-designed with C03 + C43 owners. Touches manifest (T4) for the `declared_capabilities` field only.

T7's **Go and Python** skeletons are themselves a 2-way fan-out (DELTA-06 parity is proven by building both, by different workstreams, against the same frozen schema). T10's conformance suite is partitionable by acceptance criterion (each §8 item is an independent test).

## 4. Interfaces-first / contract milestones

Freeze early, in this order, to unblock the maximum downstream fan-out:

1. **M1 — `ToolNodeRequest`/`ToolNodeResponse` schema + exit-code taxonomy frozen (T2+T3).** This is the single contract every pack and C17 build against. Highest-priority freeze. Publish as versioned schema files.
2. **M2 — `PackManifest`/`ToolNodeManifest` schema frozen (T4) + ABI-version policy (T5).** Unblocks pack authors and the C03 layer-source seam.
3. **M3 — capability-declaration schema + grant rule frozen (T6).** Unblocks C43 and any node needing fs/network.
4. **M4 — stub runtime harness published (T8).** Lets all downstream packs develop and test *without* a working C01, maximizing parallelism across the whole architecture.

## 5. Risks & de-risking order

| order | risk | de-risk action |
|---|---|---|
| 1 | **OQ1/G11 — Gas City's real tool-node I/O convention is unknown; §3b might be wrong.** If `gc` already fixes an incompatible convention, define-vs-conform flips and "no fork" itself may be at risk. | **T1 spike first, before any schema freeze.** This is the make-or-break unknown; everything else is cheap once it resolves. |
| 2 | **OQ2 — capability enforcement may be detection-only** (the G21 trap: config partitions without OS teeth). | Joint spike with C43 owner during T6: confirm whether `read_partition`/`work_partition` actually *prevents* out-of-partition access or merely scopes it. Decide DELTA-04 = prevention vs. detection honestly. |
| 3 | **OQ4 — long-running/streaming nodes (C24 watch-loop, C44 twin) may not fit single-request/single-response.** | Prototype C24's directory-watch as a pack during T9; if it needs a daemon/`[[service]]` contract instead of the tool-node ABI, draw the tool-node↔service boundary in T11 before downstream commits. |
| 4 | **DELTA-05 — Gas City's "1–2 breaking pack-schema changes/quarter" churns the manifest.** | Pin a `gc` version (per AI-CONTEXT §14 risk register); make `abi_version` independent of `gc` version so a runtime bump fails fast+typed at load, not silently. |
| 5 | **OQ3 — signature/provenance ownership straddles C02/C41/C51.** | Resolve ownership ruling before M2 freeze; keep `signature`/`transfused_from` as fields C02 *carries*, with verification logic owned wherever the ruling lands. |

## 6. Definition of done

**Per-component (C02 sweep-1):**
- Spec §3 contracts are named, the wire protocol (§3b) and bundle (§3a) are specified, and every acceptance criterion in §8 has a corresponding planned test in T10.
- The four open questions are recorded in the spec and mirrored to `_meta/review-log.md`; OQ1 is flagged as the top blocker gating the no-fork thesis.

**Per-task DoD:**
- **T1:** a written note stating the observed Gas City tool-node I/O convention and a define-vs-conform-or-shim verdict for §3b.
- **T2/T3:** versioned schema files + exit-code table merged; no downstream pack references raw `{placeholder}` argv as its primary I/O path.
- **T7:** a Go node and a Python node pass the *same* round-trip contract test with no protocol-level difference (DELTA-06 proven).
- **T8:** a downstream team can build and green-test a pack against the stub harness with no running `gc`.
- **T9:** C24, C33, C36 each demonstrably expressible as a zero-Go-import pack; fork-trigger criteria + escape-valve decision template published (DELTA-07 — "no fork" is now falsifiable).
- **T10:** all §8 acceptance criteria pass as automated conformance tests; capability-breach and stdout-impurity cases prove fail-closed behavior.
