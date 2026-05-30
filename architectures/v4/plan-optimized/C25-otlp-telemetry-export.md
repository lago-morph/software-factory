# C25 — OTLP telemetry export  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C25-otlp-telemetry-export.md
> Track B, sweep-1. Recall C25 is a **configuration + contract** component (DELTA-01), not a process — so its "build" is mostly *freezing seams* and *verifying upstream emitter behavior*, with very little code. The high-value work is contract-freezing so C24/C26/C27/C28 build in parallel.

## 1. Work breakdown

| ID | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze the enablement env-var block** (spec §3 table): the `city.toml` `[[agent]] env = {…}` block with factory defaults — `CLAUDE_CODE_ENABLE_TELEMETRY=1`, exporters=otlp, endpoint gRPC :4317, raw-bodies dir, beta-off, mTLS knobs, intervals. This is the artifact C04 injects. | S | C28 telemetry-emission contract frozen (acceptance #5 correlation keys); C03 config schema; C04 injection seam |
| T2 | **Freeze the Two-Sink Invariant + anti-edge** (DELTA-02, resolves G04): write the architectural constraint "OTLP wire ↛ CXDB; raw-bodies ↛ LangFuse" as a named, testable contract; decide mechanical-vs-documented enforcement (OQ2) with C26. | S | T1; C26 receive-endpoint seam; C24 inbox seam |
| T3 | **Freeze the raw-bodies producer contract** (DELTA-03): inbox dir path on a C01 isolated mount, write=agent / read=C24 identity, C43 boundary, and the **file-readiness mechanism** — pinned to C24 DELTA-05. Depends on resolving OQ1 (exporter write semantics). | M | T1; **OQ1 spike (T7)**; C01 mount lifecycle; C43 isolation; C24 DELTA-05/OQ5 |
| T4 | **Freeze the fail-safe / mandatory-on contract** (DELTA-04): assert export is async/buffered/bounded-drop, never an agent gate; telemetry-off is a flagged exception. Encode the degraded-mode expectations both sinks must honor. | S | T1; C28 §Consistency ("emission best-effort/at-least-once"); C24 DELTA-03 (off-hot-path) |
| T5 | **Freeze the single-wire default + mTLS rule** (DELTA-05): one endpoint/protocol (gRPC :4317), protocol as deployment knob, mTLS required+specified for non-localhost C26. | S | T1; C26 wire contract |
| T6 | **Write the conformance/acceptance suite** (spec §8): the Two-Sink-non-convergence assertion (G04 test), verify-events-flow smoke test, correlation-key presence, fail-safe-under-Collector-down, fail-safe-under-inbox-unwritable, isolation, no-torn-files, single-wire, mandatory-on, traces-gating. Mostly cross-component integration tests. | M | T1–T5; stubs/real C24, C26, C28 |
| T7 | **SPIKE — verify Claude Code exporter behavior** (OQ1): direct inspection of `code.claude.com/docs/en/monitoring-usage.md` + the exporter to determine raw-body write semantics (atomic-rename vs stream-append, end-of-session flush) and confirm the emitted-signal catalog + correlation-attr set match AI-CONTEXT §4.3. **De-risks the whole Sink-B path.** | M | none (do first) |
| T8 | **Document the C25 contract surface** for dependents (C24/C26/C28): the one-page seam doc that lets them build against stubs. | S | T1–T5 |

## 2. Dependency graph

```
T7 (exporter spike) ───────────────┐  (resolves OQ1, gates the readiness mechanism)
                                    ▼
C28 telemetry contract ─► T1 ─► T2 (anti-edge / G04)
        (frozen) │        │   ├─► T3 (raw-bodies producer)  ◄── T7, C01, C43, C24-DELTA-05
        C04 inject │      │   ├─► T4 (fail-safe / mandatory-on)
        C03 config │      │   └─► T5 (single-wire / mTLS)  ◄── C26 wire
                          └─────────────► T8 (seam doc) ─► T6 (conformance suite)
```

- **Upstream that must precede C25:** **C28** (the emitter — its telemetry-emission + correlation-key contract is what C25 configures and names; without it C25's central guarantee is unfounded) and **C04** (the injection mechanism + `session.id` ownership). **C03** (config schema), **C01** (inbox mount), **C43** (isolation) are needed for T3.
- **Critical path:** `T7 (exporter spike) → T3 (raw-bodies producer contract) → T6 (conformance)`. The exporter write-semantics unknown (OQ1) is the single biggest source of uncertainty and gates the load-bearing Sink-B path; everything else (T1/T2/T4/T5) is straightforward contract-freezing once C28 is frozen.
- **Can run concurrently:** T1 → {T2, T4, T5} fan out independently; T7 runs immediately and in parallel with all contract-freezing.
- C25 itself is in **Batch-2 "observability ingest"** alongside C24/C26/C27 — they build in parallel against C25's frozen seams.

## 3. Parallelization

C25 is small, but its build *enables* a large fan-out:
- **Internal fan-out:** after T1, the four delta-contracts T2/T4/T5 are independent single-author tasks; T3 is the only one with a real dependency (T7). T7 (the spike) parallels everything.
- **External fan-out C25 unlocks:** once C25's seams are frozen (T8), **C24** (builds its `BodyWatcher` against the frozen inbox-dir + readiness contract), **C26** (builds its receiver against the frozen OTLP-wire + anti-edge contract), and **C27** (builds against C26's fan-out) all proceed concurrently. C25 is a *contract chokepoint* for the entire Observability subsystem — freezing it early is the highest-leverage parallelization move in Batch 2.
- **Explicit:** prioritize T7 + T1 + T2 to unblock C24 and C26 simultaneously.

## 4. Interfaces-first / contract milestones

Freeze in this order (each unblocks a dependent):
1. **M1 — Enablement env block (T1).** Unblocks C04 (knows what to inject) and gives C28 the config it runs under. Frozen first.
2. **M2 — OTLP-wire seam + anti-edge (T2, T5).** The C25↔C26 contract (endpoint gRPC :4317, protocol, mTLS, **no-CXDB anti-edge**). Unblocks C26 to build its receiver + fan-out, and freezes the G04 resolution.
3. **M3 — Raw-bodies inbox + readiness seam (T3, gated by T7).** The C25↔C24 contract (dir, mount, identity, file-completion semantics). Unblocks C24's `BodyWatcher` (it is C24's #1 dependency — C24-OQ5). Co-frozen with C24 DELTA-05.
4. **M4 — Correlation-key contract (part of T1, with C28).** The join-key guarantee both sinks carry; unblocks C24 parent-chaining and C26→C27 session grouping.
5. **M5 — Fail-safe/degraded-mode contract (T4).** The off-hot-path + bounded-drop + mandatory-on guarantees; co-freeze with C24 DELTA-03 and C28 §Consistency so the three degraded-mode stories compose.

## 5. Risks & de-risking order

| Rank | Risk | De-risk |
|---|---|---|
| 1 | **OQ1 — raw-body file-write semantics unknown.** If the exporter stream-appends rather than atomic-renames, the whole readiness/no-torn-file contract (DELTA-03, and C24's `BodyWatcher`) needs the `.done`-marker/size-stable fallback, sized carefully. Gates Sink B. | **T7 spike first** — inspect Claude Code docs/exporter directly. This is the single most important thing to retire; it is shared with C24-OQ5 and C21-OQ1. |
| 2 | **G04 mis-integration latent risk.** Even with the spec, a future operator may wire C26→CXDB. | T2 decides mechanical vs documented enforcement (OQ2); prefer a mechanical guardrail in C26's config (no CXDB exporter permitted) so the rejected path is *impossible*, not just discouraged. |
| 3 | **Raw-bodies secrets exposure.** Untruncated bodies (secrets, holdout content) in an under-isolated dir. | T3 pins C01/C43 isolation up front; OQ3 (at-rest encryption / hash manifest) decided jointly with C24-OQ4 before any non-localhost or multi-tenant deployment. |
| 4 | **Telemetry on the hot path.** A naive integration that gates the agent on export liveness would let a Collector/inbox outage stall the factory. | T4 freezes off-hot-path/bounded-drop early; acceptance #4/#5 prove turn-latency independence (joint with C24 #9). |
| 5 | **Wire mismatch silent-drop.** Per-agent protocol freedom → silent telemetry loss. | T5 freezes the single-wire default; config-time validation rejects mismatches. |

## 6. Definition of done

**Per-component:**
- The enablement env block is frozen, version-pinned in `city.toml`/C03, and injected by C04 on every factory agent (M1).
- The **Two-Sink Invariant + OTLP→CXDB anti-edge** is a documented, testable contract and **G04 is resolved** — the dataflow has exactly two non-converging sinks, mechanically verified (acceptance #1).
- The raw-bodies producer contract (dir/mount/identity/readiness) is frozen and co-frozen with C24 DELTA-05; OQ1 is resolved or has a sized fallback (acceptance #7).
- Fail-safe + mandatory-on contracts are frozen and compose with C24 DELTA-03 / C28 §Consistency (acceptance #4/#5/#9).
- Single-wire + mTLS default frozen (acceptance #8).

**Per-task:** each Tn exits when its contract/artifact is frozen and the corresponding acceptance test (spec §8) passes against the real or stubbed dependent.

**Acceptance gate (ties spec §8):** all 10 acceptance criteria pass, with #1 (Two-Sink non-convergence / G04) and #2 (verify-events-flow, README §539) as the headline smoke gate, and #4/#5 (fail-safe) as the resilience gate. The five open questions (OQ1–OQ5) are mirrored to the review-log; OQ1 must be *resolved* (not deferred) before C24's `BodyWatcher` is considered done.
