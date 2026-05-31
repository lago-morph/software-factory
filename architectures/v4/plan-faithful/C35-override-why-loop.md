# C35 — Override → pattern → rule loop  (Build Plan, canonical track)

> Source / Spec ref: spec/C35-override-why-loop.md

## 1. Work breakdown

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Override-detection hook handler.** Register a `PreToolUse`/`PostToolUse` handler as a Gas City pack (Claude Code native hooks via C28); implement the **override-recognition predicate** (what counts as "operator overrode the system"). Transfuse the audit-log shape from CloudTrail / git reflog (README L457). | M | C28 (hook surface), C02 (pack ABI) |
| T2 | **"Why" capture.** In the handler, force a structured rationale on override; bind it to the pending record; mark `why_missing` if the operator declines. | S | T1 |
| T3 | **Override logging.** Write one `type="override"` bead per detected override using **C20's** payload schema (D-3), with `created_by` (C41). | S | T1, C20, C19, C41 |
| T4 | **Periodic surfacing pack.** Scheduled tool node that reads the `override` log and groups recurring overrides — SQL/DuckDB for exact/structural recurrence (README L215); reuse C37 clustering for semantic recurrence. Emit a recurring-pattern report. | M | T3, C37 (optional, semantic case) |
| T5 | **Operator-review gate.** The human review step where a surfaced pattern is approved/rejected as a latent validation rule (README L216). The gate is mandatory on the conversion path (I4). | S | T4 |
| T6 | **Rule-conversion handoff.** For an approved pattern, emit a new rule to the correct sink — a **C30 Inspect-AI rubric** (satisfaction-class; the **only v4-named** sink, README L216) and, by the spec §3 contract-6 faithful inference, a C10 (spec-structural) / C15 (workflow-structural) rule. **C10/C15 are inferred sinks, not C35 inventory dependencies** — confirm scope with the orchestrator (spec OQ4) before building those two handoffs. Keep a provenance back-reference (cluster → rule). | M | T5, C30 (v4-named); C10/C15 *(only if the inferred sinks are retained)* |
| T7 | **Predicate + threshold config.** Surface the recognition predicate and recurrence threshold as C03 config / pack settings; document false-positive pruning via the same surfacing loop. | S | T1, T4, C03 |
| T8 | **G43 maturity reconciliation.** Document (not redesign) the P8-maturity disagreement: automated scope = detect→why→log→surface, conversion = operator-gated; flag that F10's "Addressed" holds only from Phase 3a. Findings → review-log. | S | T1–T6 |

## 2. Dependency graph

Critical path: **C28 hook surface + C20 `override` schema → T1 → T3 → T4 → T5 → T6 (rule lands in a sink)**.
- T1 is the gate: no override is detectable until the native hook handler is registered (needs C28's surface + C02 pack ABI).
- T3 cannot write until C20's `override` schema is frozen (D-3) and C19/C41 exist.
- T4 (surfacing) needs an `override` log to read, so it serializes after T3 — but can be developed against a seeded fixture log in parallel.
- T6 (conversion) needs all three rule sinks (C10, C15, C30) to have a rule-registration contract.
- **Must precede C35:** C28 (hook surface), C20 (schema), C19/C41 (store + attribution). **Soft/lateral:** C37 (only for semantic surfacing — the SQL case has no C37 dependency), C10/C15/C30 (only the *conversion* end T6 needs them).
- **Nothing depends on C35 internally** (inventory: C35 has no downstream C-IDs); it *feeds* C10/C15/C30 new rules, but those components exist independently of C35.

## 3. Parallelization

Two independent workstreams fan out once T1's hook handler skeleton exists:
- **WS-A (capture):** T1 + T2 + T3 — detect → why → log. Verifiable end-to-end against a C28 hook + a C20 `override` schema stub; independent of surfacing.
- **WS-B (surfacing + conversion):** T4 + T5 + T6 — built against a **seeded `override` log fixture** (no need to wait for WS-A to produce real beads). The SQL/DuckDB surfacing (T4) and the three rule-sink handoffs (T6) are themselves three independent sub-streams (C10 / C15 / C30 targets do not block each other).
- **T7** (config) and **T8** (G43 doc) ride alongside both.
The join point is a real override flowing all the way to a proposed rule once WS-A and WS-B meet.

## 4. Interfaces-first / contract milestones (freeze early)

1. **Override-recognition predicate signature** (T1) — what the hook handler receives (tool-call context fields) and what it returns (override? + overridden-action reference). Freeze first; everything downstream keys off "an override was detected."
2. **`override` bead write-contract** (T3) — depends on **C20's** frozen `override` schema (D-3). Freeze the C20↔C35 write seam so WS-B can seed a realistic fixture log.
3. **Recurring-pattern report shape** (T4) — the structure of a surfaced cluster (overridden-action class + rationale grouping + recurrence count). Freeze so the operator gate (T5) and conversion (T6) build against it.
4. **Rule-emission handoff per sink** (T6) — the three target rule schemas: C10 (EARS/INCOSE rule), C15 (Mammoth rule), C30 (Inspect-AI rubric). Coordinate each with the sink owner; these are *their* schemas, C35 only targets them.

## 5. Risks & de-risking order

1. **Override-recognition predicate ambiguity (highest, OQ2).** v4 never defines what "operator overrode the system" means. Spike T1's predicate against a fixture set of override vs non-override tool calls *first* — it is the load-bearing custom piece and an over-broad/over-narrow predicate breaks the whole loop's signal. Surface the chosen boundary to review-log.
2. **Three-sink conversion fan-out (T6).** Rule conversion targets three different rule schemas (C10/C15/C30) — the riskiest integration surface. De-risk by contract-testing each handoff against a sink stub early; do not assume one unified rule format.
3. **Semantic-surfacing scope creep (T4).** The temptation is to build a bespoke clustering engine; the bar says reuse C37 / DuckDB. Prototype the **SQL/DuckDB exact-recurrence** path first (covers the common case) and only reach for C37 embeddings if structural grouping proves insufficient — keep the custom code minimal.
4. **G43 maturity overstatement (T8).** F10 is marked "Addressed" partly on this loop; spike nothing here but *document* early that the guard is real only from Phase 3a, so no earlier phase silently relies on an unbuilt loop.

## 6. Definition of done

- **Per spec ACs:** AC1 (override → hook → predicate → one `override` bead with `created_by`), AC2 (non-empty "why", or `why_missing`, never dropped), AC3 (surfacing groups a recurring class, reports none when sparse), AC4 (approved pattern → new rule in the right sink, reachable only via the operator gate), AC5 (writes only C20-declared fields), AC6 (native hooks only, no custom hook engine), AC7 (no override exists only in chat — all retrievable by type).
- **Per-task DoD:** each task's artifact (hook handler, surfacing pack, config, handoff) ships in a Gas City pack (C02), version-controlled, exercised by at least one run against a real or seeded `override` log.
- **Component DoD:** a real operator override flows detect → why → log → (after seeded recurrence) surface → operator-approve → a proposed rule registered in C10/C15/C30; and the G43 maturity reconciliation (automated scope = detect→surface, conversion = human-gated; F10 valid from Phase 3a) is written to `_meta/review-log.md` — closed by escalation, not silent assumption.
