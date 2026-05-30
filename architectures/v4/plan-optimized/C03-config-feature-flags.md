# C03 — Layered config / feature-flag model  (Build Plan, Track B)

> Source / Spec ref: spec-optimized/C03-config-feature-flags.md
> Track B, sweep 1. Foundational. Deltas referenced: DELTA-01…06 (see spec header).

## 1. Work breakdown

Ordered tasks. Size S/M/L. Prereqs by task id (and external C-IDs).

| id | Task | Size | Prereqs |
|---|---|---|---|
| T1 | **Layer model + precedence spec** — freeze the ordered layer stack (`core-defaults → pack → city → agent.env → runtime-override`) and merge semantics (deep-merge tables; arrays-of-tables merge by identity key `name`; scalar higher-wins). DELTA-01. | S | — (needs C01 loader behavior confirmed; see OQ2) |
| T2 | **`CapabilityDescriptor` schema** — `{capability_id, gating_section, requires, conflicts_with, schema_ref, default_state}`; define registration source (core vs pack — OQ3). DELTA-02. | S | — |
| T3 | **`SecretRef` syntax + `SecretResolver` seam** — `secret://`, `${ENV:NAME}`, `file://`; resolver interface (no provider impl yet). DELTA-03. | S | — |
| T4 | **`EffectiveConfig` + effective-hash** — flattened immutable view, queryable by capability_id / section path, content hash. | M | T1, T2, T3 |
| T5 | **Flatten + enablement engine** — collect layers, apply precedence, compute enabled set from present sections. | M | T1, T2 |
| T6 | **Validation gate** — schema-per-section, transitive `requires`, `conflicts_with`, unknown-section = error, deprecation = warn; produce `ConfigValidationReport`. DELTA-04. | M | T2, T5 |
| T7 | **No-plaintext-secret lint** — reject secret-shaped literals in version-controlled layers. DELTA-03. | S | T3 |
| T8 | **Load/reload control flow** — generation switch, fail-closed-to-last-good on bad reload. | M | T4, T5, T6 |
| T9 | **`SecretResolver` baseline provider** — env-injection baseline (Vault/SOPS deferred per OQ1). DELTA-03. | M | T3, T8 |
| T10 | **`ConfigProvenance` emission** — per-(re)load attributed event to C23 with effective hash + contributing layers. DELTA-06. | S | T4, T8, **C23**, **C41** |
| T11 | **Phase profiles (named overlays)** — Phase 0/1/2 presets as validated overlays + the G03 honesty assertion (P3 gated-off at Phase 0; flips on `[formulas]`). DELTA-05. | S | T6 |
| T12 | **Core capability registry seed** — descriptors for the v4 sections (`[formulas]`→C12, `[[rig]]`→C42, `[[service]]`→C21/C26/C27, `[mail]`→C06, `[daemon]`/orders→C40, `[beads]`→C19, agent `env` OTLP→C25/C28, model-stylesheet→C29). | M | T2, and the gated components' section names frozen |

## 2. Dependency graph

- **Upstream (must precede C03 being *complete*):** C01 (owns the TOML loader; C03 specifies the contract it must honor — OQ2 may make T1 a *describe* rather than *change*). For runtime emission: C23 (event bus) and C41 (attribution) for T10 — but only T10 blocks on them, so C03 ships its core ahead of those.
- **Downstream (gated *by* C03):** effectively the whole system — C12, C04, C42, C06, C40, C17/C44, C19, C28/C25, C29, C08. They consume `EffectiveConfig`; none re-parse TOML.
- **Critical path inside C03:** T1/T2/T3 (parallel) → T4 → T5 → T6 → T8. T9/T10/T11/T12 hang off T8/T6 and are not on the longest path.
- **System critical path note:** C03 is foundational and on Batch-1 of the inventory; its *interface freeze* (see §4) is what unblocks ~12 downstream components, so the contract milestone matters more than full impl completion.

## 3. Parallelization

Explicit fan-out after the interface freeze:

- **Stream A (resolution core):** T1 → T5 → T8.
- **Stream B (typing/validation):** T2 → T6 → T11. Joins A at T8.
- **Stream C (secrets):** T3 → T7 → T9. Independent until T8/T9.
- **Stream D (registry content):** T12 — pure data authoring against the T2 schema; can proceed as soon as gated components publish their section names (does not block A/B/C).
- **Stream E (provenance):** T10 — blocks only on C23/C41 availability; stub the event sink to unblock.

T1, T2, T3 start same day (no inter-dependencies). T12 and T10 are the two streams that depend on *other* components, so they are the natural background/last-to-land work.

## 4. Interfaces-first / contract milestones

Freeze these early so dependents build against stubs:

1. **`EffectiveConfig` query surface** (read API by capability_id / section path) — the single config surface; freeze first. Every downstream component (C04, C12, C42, …) codes against this, not raw TOML.
2. **`CapabilityDescriptor` schema** — lets each gated component (and each pack, C02 seam) declare its descriptor in parallel.
3. **Layer precedence + merge rules (DELTA-01)** — so pack authors (C02) know how their layer composes.
4. **`SecretRef` + `SecretResolver` interface (DELTA-03)** — so C28 (OAuth) and C25 (mTLS) can reference secrets before a provider is chosen (OQ1).
5. **`ConfigProvenance` event shape (DELTA-06)** — so C23/C41 reserve the schema.

Stub strategy: ship `EffectiveConfig` + descriptor schema + a hard-coded Phase-0 profile first; dependents validate against that while Streams A/B/C finish.

## 5. Risks & de-risking order

Spike highest-uncertainty first:

1. **OQ2 — does Gas City's loader already define precedence?** Spike T1 against the real `gc` loader before building T5. If it conflicts, DELTA-01 becomes a conform-or-fork decision touching C01 — retire this first; it gates the whole resolution core. (Ties to G11: Gas City behavior is an unverified assumption.)
2. **OQ3 — central vs per-pack descriptor registration.** Affects the C02↔C03 seam and whether T12 is one file or N pack contributions. Decide before T12 scales.
3. **OQ1 — secret resolver provider under Max.** G37: corpus has no secrets story. De-risk by shipping the *seam* (T3) and an env-injection baseline (T9); defer Vault/SOPS. Confirms C28 OAuth / C25 mTLS can be expressed as `SecretRef`s without the literal.
4. **Reload safety** (T8 fail-closed-to-last-good) — prototype the generation switch early; a bad reload taking down a running factory is the worst operability failure.

## 6. Definition of done

Per-component (ties to spec §8 acceptance):

- **DoD-1 Determinism:** identical ordered layers ⇒ byte-identical effective hash (golden test). [T4]
- **DoD-2 Gating:** removing `[formulas]` disables C12 *and reports it* via expected-set check; adding it (requires met) enables it; same for `[[rig]]`→C42, `[[service]]`→C21/C26/C27. [T5,T6,T12]
- **DoD-3 Precedence:** agent-env overrides city scalar; arrays-of-tables merge by `name` (override vs append). [T1,T5]
- **DoD-4 Fail-closed:** unsatisfied `requires` / unknown section / schema violation / dangling `SecretRef` each refuse load; a bad *reload* leaves the prior generation serving. [T6,T8]
- **DoD-5 No-plaintext-secret:** secret-shaped literal in a versioned layer fails the lint. [T7]
- **DoD-6 Provenance:** each load emits exactly one attributed `ConfigProvenance` to C23 with the effective hash. [T10]
- **DoD-7 Phase-0 honesty (G03):** Phase-0 profile reports P3 gated-off (native count 5); turning `[formulas]` on flips P3 to delivered. [T11]

Per-task DoD: each task lands with unit tests for its acceptance bullet above and against the frozen interfaces of §4; no task is "done" until the contract it implements is unchanged from its freeze (or the change is propagated to all stub consumers).

Component is **done** when DoD-1…7 pass and the §4 contracts are frozen and consumed by at least one real downstream component (C12 via `[formulas]` is the canonical integration check).
