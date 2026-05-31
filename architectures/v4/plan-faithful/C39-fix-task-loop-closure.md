# C39 — Fix-task generation & loop-closure  (Build Plan, canonical track)

> Source / Spec ref: spec/C39-fix-task-loop-closure.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Fix-task generation.** From a completed C38 `diagnosis`, write **one** `fix_task` bead (C20's schema, D-3) chained `diagnosis ──produces──▶ fix_task`, pointing at the diagnosis/anomaly **and** the **C08 spec** the fix must satisfy ("fix the spec, not the output", README:102), with `created_by` (C41). Non-actionable diagnosis → escalate, never fabricate a fix (I1). | M | C38 (diagnosis), C20 (schema), C08 (spec), C41 |
| T2 | **Re-entry wiring.** Hand the `fix_task` to the normal build flow — dispatch via C05, converge under C18 — so the fix re-enters like any work bead. C39 owns no dispatcher/loop; it injects the per-pass bound C18 enforces (XC-3). | S | T1, C05, C18 |
| T3 | **Closure-chain advancement + proof-gated resolution.** Advance the chain node-by-node; on a **positive** closure verdict (originating anomaly silent AND scenarios/satisfaction pass, C30–C33) write the `resolution` node and set terminal `resolved`. Unproven/flaky verdict → no resolution (I2, fail-closed). | M | T1, C20, C30–C33 (verdict) |
| T4 | **Termination policy: N-attempts → escalate (G18 core).** Maintain `attempt_no` vs `max_attempts` (C20 slots; **value set by C39 policy**); on the Nth failed attempt for the same anomaly set terminal `escalated` and route to operator — do **not** spawn attempt N+1 (I3). | M | T3, C20 (slots) |
| T5 | **Oscillation / F52 detection (G18).** Detect a **recurrent** fix→new-anomaly self-feeding cycle and escalate rather than patch further; a single legitimate fix→new-anomaly iteration is NOT oscillation (I5). | M | T3, T4 |
| T6 | **L5 ship-authorization gate (G35).** Gate ship-without-review on the current C56 autonomy level: **L5** auto-ship, **L4** batch-for-operator-review, below L4 per-fix gate; re-read level at ship time (downgrade-safe). C39 never ships above the operator's level (I4). Authorization predicate is the policy `Healer governance | OPA` (AI-CONTEXT:335) would enforce — predicate here, engine wiring sweep-2. | M | T3, C56 (level read) |
| T7 | **Bound-reached consumption.** Consume C18's **bound-reached** signal for a `fix_task` pass and apply the policy (count toward N / test oscillation / escalate) — the C18→C39 policy seam (XC-3). | S | T2, T4, T5, C18 |
| T8 | **Policy config + terminal-state totality.** Surface the numeric policy (N / oscillation window / L4-L5 cadence) as C03 config (not hard-coded, OQ2); guarantee every chain ends in exactly one of `resolved | escalated | abandoned` (I3, I6 schema deference). | S | T4, T5, T6, C03 |
| T9 | **G18/G35 disposition write-up.** Record (not redesign): C39 closes G18 at the **policy layer** (C20=slots, C18=loop-bound); G35 = ship gated on C56 level + multi-cycle F54 drift audit deferred to C56/C57. Findings → review-log. | S | T1–T8 |

## 2. Dependency graph

Critical path: **C38 diagnosis + C20 `fix_task`/closure schema → T1 → T2 (re-entry) → T3 (proof-gated resolution) → T4 (N→escalate) → T5 (oscillation) → T6 (ship gate)**, with **T7 (bound-reached)** joining the policy core.
- **T1 is the gate**: nothing generates until C20's `fix_task` + closure-chain schema is frozen (D-3) and a C38 diagnosis shape exists. C08's spec-pointer must be addressable (Reading-A collapsed spec is sufficient).
- **T3 cannot close** until a closure verdict source exists (C30–C33); develop against a **seeded closure-chain fixture** + a stub verdict in parallel.
- **T4/T5/T6 are the G18/G35 policy core** — they read/write C20's boundable slots (attempt-count / max-attempts / escalated / chain-closure) and the C56 level; they can be built against schema stubs once the slot names are frozen.
- **T7** needs C18's bound-reached signal contract; until C18 lands (Batch 3, earlier) model the signal as an injected event.
- **Must precede C39:** C38 (diagnosis), C20 (schema + slots), C08 (spec target), C41 (attribution). **Lateral/soft:** C18 (loop + bound-reached — earlier batch), C05 (dispatch), C30–C33 (verdict), C56 (autonomy level — the G35 tie, **not** a hard inventory dep), C40 (durable launch — C40's inferred seam, OQ4).
- **Nothing depends on C39 internally** (inventory: C39 has no downstream C-IDs); C18 references it as the *policy owner* (XC-3), and C08/C40 name it as the fix-loop driver, but those exist independently.

## 3. Parallelization

Two workstreams fan out once T1's `fix_task` write-contract exists:
- **WS-A (generation + re-entry + closure):** T1 + T2 + T3 — diagnosis → fix_task → re-enter → proof-gated resolution. Verifiable end-to-end against a C20 schema stub + a C38 diagnosis fixture + a stub closure verdict; independent of the policy numbers.
- **WS-B (the G18/G35 policy core):** T4 + T5 + T6 + T7 — N→escalate, oscillation, ship gate, bound-reached — built against a **seeded closure-chain fixture** (no need to wait for WS-A to produce real beads) + autonomy-level fixtures. T4/T5 (termination + oscillation) and T6 (ship gate) are independent sub-streams; T7 (bound-reached) is a thin adapter onto T4/T5.
- **T8** (config + totality) and **T9** (G18/G35 disposition) ride alongside both.
The join point is a real diagnosis flowing all the way to either a proven `resolution` (shipped per autonomy level) or an `escalated` terminal — WS-A produces the chain, WS-B bounds and ships it.

## 4. Interfaces-first / contract milestones (freeze early)

1. **`fix_task` write-contract + closure-chain edges** (T1/T3) — depends on **C20's** frozen `fix_task` type, the `diagnosis→fix_task→resolution` edges, and the **boundable slots** (attempt-count / max-attempts / escalated / chain-closure). Freeze the C20↔C39 write seam first so WS-B can seed a realistic fixture chain. **C20 owns these; C39 only writes them + sets policy values.**
2. **Diagnosis-intake contract** (T1) — what C38 hands C39 (root cause + anomaly pointer). Freeze the C38→C39 seam so generation has a stable input.
3. **Closure-verdict contract** (T3) — the pass/fail signal from C30–C33 that answers "did the fix actually fix it?" (anomaly-silent + scenarios/satisfaction pass). Freeze so resolution is proof-gated against a known shape.
4. **Bound-reached signal** (T7) — C18's **bound-reached** payload (C18 §3.2); freeze the C18→C39 seam so the policy consumes it. **C18 owns the signal; C39 owns the response.**
5. **Autonomy-level read** (T6) — how C39 reads the current C56 level (config in C03 vs a C56 query, OQ3). Freeze the read so the ship gate is testable.
6. **Numeric-policy parameter shape** (T4/T5/T6/T8) — the config keys for N / oscillation window / L4-L5 cadence (C03). Freeze the *shape* now; the *values* are operator/integrator policy at sweep-2 (OQ2).

## 5. Risks & de-risking order

1. **G18 ownership + slot sufficiency (highest, OQ1).** C39 owns the numeric policy XC-3 routes here (C16:OQ-G18, C18:OQ-1, C20:OQ-C20-1 all defer to C39). De-risk **first** by confirming with the C20 author that the boundable slots (attempt-count / max-attempts / escalated / chain-closure) are **sufficient** to express the policy — if not, raise a C20 change request before building T4–T6. **Non-reverting fail-safe:** if C39 disclaimed G18 the loop would be unbounded with no home; C39 explicitly accepts ownership.
2. **Oscillation vs legitimate iteration (T5).** The hardest custom judgment: distinguishing a self-feeding fix→new-anomaly cycle from healthy iterative repair. Spike T5 against a synthetic recurrent sequence vs a single-iteration fixture *before* fixing the recurrence window; an over-eager detector escalates good fixes, an under-eager one lets the F52 trap through.
3. **G35 ship-authorization (T6, OQ3).** Auto-shipping a fix without a human is the load-bearing security surface (and the F54 *weakest* v4 mechanism). De-risk by building the **L4-batched** path first (safe default — review before ship) and gating L5 auto-ship behind an explicit autonomy-level read; confirm the C39↔C56 tie + that multi-cycle drift audit is C56/C57's, not C39's.
4. **Proof-of-fix verdict source (T3, OQ5).** "Did the fix actually fix it?" needs a reliable verdict; if C30–C33 can't return one, C39 must fail-closed (no silent resolution). Prototype the proof condition (anomaly-silent AND scenarios-pass) against a stub verdict early; confirm the C39↔(C33/C36) read seam.
5. **C40 launch coupling (OQ4).** C40 models an Order *driving* the chain as its own inference; don't assume it — confirm direction so C39 doesn't build durability C40 owns.

## 6. Definition of done

- **Per spec ACs:** AC1 (diagnosis → one traceable `fix_task` pointing at the C08 spec, `created_by` set), AC2 (resolution written **only** on a proven fix; unproven never closes), AC3 (Nth failure → `escalated`, no attempt N+1), AC4 (recurrent oscillation → escalate; single iteration not misclassified), AC5 (ship-without-review only at L5; L4 batched; never above the operator's C56 level), AC6 (every chain terminal = `resolved`/`escalated`/`abandoned`), AC7 (C18 bound-reached drives the policy), AC8 (writes only C20-declared fields; new field = C20 change request).
- **Per-task DoD:** each task's artifact (generation, re-entry wiring, closure-pack, policy core, ship gate, config) ships in a Gas City pack (README:464 "Loop closure tracking pack"; C02), version-controlled, exercised by at least one run against a real or seeded closure chain. No Go fork.
- **Component DoD:** a real diagnosis flows generate → re-enter → (proof-gated) resolve OR (on N/oscillation) escalate, with the ship gate honoring the current C56 autonomy level; **and** the G18/G35 disposition (C39 owns the numeric policy over C20's slots + C18's signal; G18 closed at the policy layer; G35 = ship gated on C56 + F54 multi-cycle drift audit deferred to C56/C57) is written to `_meta/review-log.md` — closed by escalation, not silent assumption. The numeric *values* (N, oscillation window, L4/L5 cadence) are config (C03), set at sweep-2 (OQ2).
