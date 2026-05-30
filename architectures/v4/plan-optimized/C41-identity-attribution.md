# C41 — Identity / actor model & attribution  (Build Plan, Track B)

> Source / Spec ref: [spec-optimized/C41-identity-attribution.md](../spec-optimized/C41-identity-attribution.md)

C41 is a Batch-1 foundational cross-cutting load-bearer: its `Actor` + `Attribution` shapes and `attribute`/`sign`/`verify` contracts are embedded by *every* component that writes a bead (C19/C20), emits an event (C23), or sends a message (C06). The plan's whole shape is **freeze the data shapes and the four verbs first**, ship the cheap `asserted` path so the rest of Batch 1 is unblocked, then layer signing → tamper-evidence → verification as independent workstreams.

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Freeze `Actor` + `Attribution` schemas** (spec §4.1–4.2): field set, `ActorClass` enum (DELTA-02), `boundary_class` enum (DELTA-07), assurance-level enum (DELTA-05). The contract every Batch-1 component embeds. | S | — |
| T2 | **Freeze the four verb contracts**: `attribute`/`sign`/`verify`/`audit` signatures + `register_actor`/`resolve` (spec §3). Named signatures sufficient for stub dependents. | S | T1 |
| T3 | **Identity Registry** — `register_actor`/`resolve`/`list_actors` over C01 Gas City `actor` schema + the C19 store for persistence; hierarchy via `parent_ref`. | M | T1, C01, C19 |
| T4 | **`asserted`-path `attribute`** — build the `Attribution` record, stamp `boundary_class` unconditionally (DELTA-07), embed as `created_by`. No crypto yet. Unblocks C19/C20/C23/C06. | M | T2, T3 |
| T5 | **Key/credential model** (DELTA-06) — per-actor keypair minted at registration, `key_history`, `rotate_key`/`revoke_actor`; trust-rooted at the operator/city. Consumes the secrets-store seam (OQ2). | M | T3 |
| T6 | **`sign` + signed-path `attribute`** — provenance signature over canonical attribution + payload digest; assurance escalation. | M | T4, T5 |
| T7 | **Attribution policy tier** (DELTA-01) — config-driven `(class, boundary_class, op_type) → required_level` table via C03; fail-closed rejection when an action under-signs. | M | T6, C03 |
| T8 | **Verification service** — `verify`/`verify_chain` returning `{level_met, ok, reason}` (DELTA-05); key-non-revocation + historical-key checks. | M | T6 |
| T9 | **Tamper-evident provenance chain** (DELTA-04) — per-actor `prev_provenance_hash` anchored in C23; `verify_chain` walk + break detection. | M | T6, C23 |
| T10 | **Delegation** (DELTA-03) — `delegate`/`on_behalf_of` chain construction + propagation through agent→tool-node spawns. | S | T4 |
| T11 | **Audit query surface** — `audit(predicate)` over C19 history + C23 log; the C34 holdout-audit + F14/F43 query path. | M | T4, T9, C19, C23 |
| T12 | **C06 Mail integration** — wire `sign`/`verify` into the Mail send/receive path (closes F32); replaces "optional HMAC." | S | T7, T8, C06 |
| T13 | **Acceptance test suite** — the 9 criteria (spec §8), incl. tamper-injection, policy-tier conformance, Phase-0 boundary-coverage, holdout-audit contract test with C34. | M | T7–T11 |

## 2. Dependency graph

- **Critical path:** T1 → T2 → T3 → T4 → T6 → T7 → {T8, T9} → T11 → T13. The schema/verb freeze (T1–T2) gates everything downstream *and* everything in other components that embeds attribution — it is the system-wide bottleneck, so it is first and small.
- **Upstream component prereqs:** C01 (actor primitive, T3), C19 (persistence + bead history, T3/T11), C23 (event anchor for the chain, T9/T11), C03 (policy-tier config, T7), C06 (Mail wiring, T12). C43 supplies the `boundary_class` taxonomy (T1) — but C41 can proceed with a provisional enum and reconcile, since the *labelling* must exist from Phase 0 regardless of whether isolation does (the G31 point).
- **Downstream unblock:** T1+T2 (shapes + verbs) unblock C19/C20/C23/C06 stub work immediately — they need the `Attribution` shape, not its crypto. T4 (`asserted` path) is enough for all of Phase-0 Batch 1 to run end-to-end.

## 3. Parallelization

After T2 freezes the contracts, three workstreams run concurrently:
- **WS-A (registry + identity):** T3 → T5 (key model) → T10 (delegation).
- **WS-B (attribution + policy):** T4 (`asserted`) → T6 (`signed`) → T7 (policy tier).
- **WS-C (integrity + audit):** T8 (verify) and T9 (chain) — both depend on T6 but are independent of each other — → T11 (audit) → T12 (Mail).

WS-A and WS-B both start at T3/T4 right after T2; WS-C joins once T6 lands. T13 (tests) is authored interface-first against the T1/T2 freeze and fleshed out as each workstream completes its criterion.

## 4. Interfaces-first / contract milestones

Freeze in this order so dependents build against stubs:
1. **`Attribution` record shape (T1)** — the single most-referenced contract in Batch 1; everyone embeds it. Freeze before any other component's write path.
2. **`ActorRef` / `register_actor` / `resolve` (T2/T3)** — so C19/C23 can reference actors.
3. **`attribute(actor_ref, op_context) → Attribution` (T4)** — the hot-path verb every writer calls; `asserted`-only stub first, signing added transparently later (callers don't change).
4. **`verify(attribution, expected_level)` (T8)** — frozen early as a named contract so C06/C34 build their gates against it before crypto lands.
5. **Policy-tier config schema (T7)** — the C03 section shape, so operators and OQ1 resolution have a target.

The key design lever: `attribute` and `verify` signatures are stable from T2; the *assurance* an `Attribution` carries upgrades from `asserted`→`signed` underneath without any caller change. This is what lets Phase-0 Batch 1 ship on the cheap path and gain integrity later with zero downstream churn.

## 5. Risks & de-risking order

1. **Spike the secrets-store seam (OQ2 / G37) first** — `signed`/`attested` are only as strong as where private keys live; v4 has no secrets story. Prototype the C41↔secrets-store interface (sealed-file vs OS keychain vs HSM) before T5, so the key model isn't built against a hole.
2. **Spike the policy-tier defaults (OQ1)** — author the proposed default table (cross-boundary + Mail = `signed`; self-modifying = `attested`; else `asserted`) and adversarially review it; getting the defaults wrong either taxes routine work or leaves G36 open in practice.
3. **Prototype the tamper-evident chain over C23 (T9)** before committing the append-only history model — confirm the `prev_provenance_hash` anchoring works with C23's `seq` ordering and resolve the redaction-vs-append-only tension (OQ3) before it ossifies.
4. **Validate native ergonomics early** — confirm the `asserted` `attribute` call needs zero per-call ceremony (spec AC9 / README l.231), so making integrity graduated-mandatory doesn't regress the "flows automatically" property that makes P9 the corpus's strongest match.

## 6. Definition of done

- **Per-task:** each task's exit = its spec §8 acceptance criterion passes against a real (not stubbed) collaborator where one exists.
- **Per-component (C41 done when):**
  1. `Actor` + `Attribution` shapes + the four verbs are frozen and embedded by C19/C20/C23/C06 (no component carries a bare-string `created_by`).
  2. Mandatory-actor invariant enforced at every write/emit seam (G36 presence).
  3. Graduated-mandatory signing enforced per policy tier; cross-boundary + Mail reject `asserted` (G36 integrity; F32).
  4. `verify`/`verify_chain` operational with the three assurance levels; tamper-injection detected (F14).
  5. Every action carries a `boundary_class` from Phase 0; `audit(boundary_class=production)` enumerates the G31 exposure window; C34 holdout audit runs as a pure attribution query.
  6. Key lifecycle (mint/rotate/revoke) works with historical-signature verification.
  7. The three OQs are filed in [`_meta/review-log.md`](../_meta/review-log.md) with the policy-tier defaults (OQ1) flagged as the gating operator decision.
