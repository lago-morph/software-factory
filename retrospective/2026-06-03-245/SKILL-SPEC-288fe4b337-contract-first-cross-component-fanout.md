# Spec: `contract-first-cross-component-fanout`

- **ID**: SKILL-SPEC-288fe4b337
- **Source retrospective**: ../2026-06-03-245.md

## Intent

A cross-component change where several components must agree on one shared contract (a record schema, an interface, a payload) is the highest-drift kind of parallel authoring: each subagent can be internally correct yet collectively inconsistent. This skill encodes the orchestration recipe that produced zero drift on the frozen records in the spec-scenarios-system triangle work: the lead freezes the shared contract as a numbered ledger decision, a keystone builder authors and verifies it, the dependent components fan out pre-briefed with the verbatim contract, a seam adversary field-level-verifies producer against consumer, and an integrator pass reconciles the residual new seams the change introduced. It composes three existing skills (`cross-component-decision-ledger`, `disk-fanout-orchestration`, `parallel-subagent-fanout`) into a named, ordered workflow specialized for the *shared-contract* case, where the dominant failure mode is field-level drift between independently-authored producers and consumers.

## Trigger

Activate when ALL of these hold: (a) the task touches ≥3 components that must agree on a shared data contract / interface / payload; (b) the components will be authored by separate subagents (or sessions); (c) at least one component *produces* the shared artifact and others *consume* it. Direct phrases: "implement the X contract across A/B/C", "deepen these specs to share the new Y record", "the judge output feeds the router and the gate". Proactive: any time a single new record/schema/payload appears in ≥2 component briefs in the same fan-out. Negative triggers: a single-component change (no shared contract); a fan-out where each subagent's output is fully independent (use plain `parallel-subagent-fanout` / `disk-fanout-orchestration`); a contract that is already frozen and unchanged (no new shared surface).

## Inputs

- The task brief naming the components and the shared contract(s) to introduce or extend.
- The existing ledger file (e.g. `architectures/v4/_meta/review-log.md`) and its numbering.
- The existing component specs to deepen in place, plus any depth/format conventions (e.g. a dispatch addendum).
- Tool access: the `Agent` tool (subagent dispatch), a diagram validator if specs carry diagrams, the repo's link/lint checkers.

## Outputs

- One (or more) numbered ledger decision(s) freezing the shared contract, written by the lead before dispatch.
- The keystone component spec carrying the canonical frozen schema, plus the dependent component specs each consuming it.
- One ledger decision per residual seam the change introduced (reconciled in the integrator pass).
- Per-wave commits (orchestrator owns all git), a ready-for-review PR, and short subagent receipts (not full dumps) in the orchestrator's working set.

## Workflow

1. **Design and freeze the shared contract as a ledger decision FIRST.** Author the full field table / interface / enum-set yourself, choosing the extension shape deliberately (companion record vs additive fields vs new type). Record it as a numbered decision with a verbatim, citable table. This is the single source of truth all subagents receive.
2. **Dispatch the keystone builder** — the component that *owns* the contract — with the frozen contract in its brief. Treat its pass as verification: if it surfaces a structural problem fitting the contract to the owning component, fix the ledger entry before the dependent wave.
3. **On the keystone's receipt, commit + push** that wave.
4. **Fan out the dependent components in parallel**, each pre-briefed with the *verbatim* frozen contract (not a paraphrase) plus its own per-component mechanics. Subagents write disjoint files to disk and return ≤15-line receipts. The orchestrator never reads full subagent output.
5. **Commit each dependent subagent's disjoint files as its receipt arrives** (per-completed-subagent cadence; tolerate the stop-hook's mid-wave nag). Push at the wave boundary.
6. **Dispatch a seam adversary** (real subagent, read-only) to field-level-verify the contract against every consumer AND — critically — to diff each producer payload against each consumer's declared inbound schema field-by-field. It reports findings (BLOCKER / SEAM-DRIFT / DEFERRABLE-OQ); it does not edit.
7. **Resolve the adversary's findings via the ledger** — record each real seam as a numbered decision, then run a single integrator subagent to apply them across the affected specs.
8. **Final consistency check** (lead-run grep/diff of the converged field set), update any reframed sibling docs, mark the plan done, open the PR, subscribe to activity.

## Concrete examples

### Example 1: the spec-scenarios-system triangle (this session, PR #245)

Input: deepen C32/C52/C53/C30/C08/C34 to share a new judge-diagnosis output. (1) The lead froze the companion `DiagnosisRecord` schema as ledger **D-43** (20 fields + a `Misalignment` sub-struct), explicitly choosing a companion record over mutating the D-39-frozen `ScoreRecord`. (2) Dispatched the C32 keystone builder with D-43 verbatim → it authored `diagnose()` + §3.2a. (3) Committed C32. (4) Fanned out C52/C53/C30/C08/C34 in parallel, each brief carrying the verbatim D-43 table. (5) Committed each as its receipt arrived. (6) The opus seam adversary verdict: **zero drift** on `ScoreRecord`/`DiagnosisRecord` across all consumers; one finding on the *new* correction-request seam (producer C52 vs consumers C08/C30). (7) Recorded D-44 (canonical payload) + D-45 (enforcement owner), ran one integrator subagent. (8) Lead re-grepped the converged field set, reframed `auto-002`, marked HANDOFF §0★ done, opened PR #245.

### Example 2: adding a shared `EventEnvelope` consumed by an emitter + two sinks (hypothetical, same recipe)

Input: a new `EventEnvelope` produced by an emitter component and read by a metrics sink and a trace sink. (1) Lead freezes `EventEnvelope{event_id, stream, seq, ts, payload_digest, …}` as a ledger decision, deciding `event_id` is a structured `{stream, seq}` not a bare int. (2) Keystone = the emitter; it authors the canonical schema. (3) Commit. (4) Fan out the two sinks pre-briefed with the verbatim envelope. (5) Commit each. (6) Seam adversary diffs the emitter's emitted fields against each sink's declared read — catches a sink that consumed `event_id` as `uint64` while the emitter emits the struct (the real D-26 class of bug). (7) Record the canonical wire type as a decision; integrator applies it to the drifting sink. (8) Verify + PR.

## Anti-patterns

- **Letting the keystone builder "discover" the contract instead of lead-freezing it.** The plan said "keystone first because it defines the contract"; freezing it in the ledger first and making the keystone a verification step is what eliminated drift. Discovery-by-authoring leaves each consumer to infer the shape.
- **Briefing subagents with a paraphrase of the contract.** Paraphrase drift across parallel builders is silent and only surfaces at aggregation (AGENTS-MD-bf4431be57). Ship the verbatim table.
- **A seam adversary that only checks consumer-against-contract.** That passes each side independently and misses producer↔consumer field drift — the exact gap that hid the correction-request seam this session.
- **Committing mid-wave on the stop-hook nag.** Captures half-written subagent files. Commit per-completed-subagent.
- **Skipping the integrator pass and patching one side of a drifted seam inside a single component.** Record the resolution as a ledger decision and apply it corpus-wide in one pass, or the other side silently keeps the old shape.

## Acceptance criteria

- [ ] Every shared contract introduced/extended by the change exists as a numbered ledger decision with a verbatim field table, written before the dependent fan-out.
- [ ] Each dependent subagent brief contains the verbatim contract text (not a paraphrase).
- [ ] The seam adversary's report includes an explicit producer-field → consumer-field diff for every producer/consumer seam, not just consumer-vs-contract.
- [ ] Every real seam finding is resolved as a numbered ledger decision and applied in a single integrator pass.
- [ ] The lead independently verifies the converged field set (grep/diff) before opening the PR; no stale field names remain.

## Files this skill creates / modifies

- `<ledger file>` (e.g. `architectures/v4/_meta/review-log.md`) — the numbered decisions freezing the shared contract + reconciling residual seams.
- The keystone component spec (+ plan peer) — carries the canonical frozen schema.
- Each dependent component spec (+ plan peer) — consumes the frozen contract.
- The PR — one ready-for-review PR with the wave-by-wave commit trail and the adversary/integrator provenance in its body.
