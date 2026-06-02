# Integration-Adversary Fixes — Sweep-2

Applied 2026-06-01. Resolves all four findings from `04-integration-adversary.md`.

---

## FIX 1 — INT-1 (BLOCKER) — C52↔C53 circular hand-off broken

**Files:** `spec/C52-self-bootstrap.md`, `spec/C53-bootstrap-validation.md`

**What changed:**
- C52 §3.4 already had the two-phase structure (Phase A → ReviewVerdict → Phase B). The stale
  `§3.0 Outbound type — RubricResult` block in C53 still described the OLD framing where C52's
  `submit_for_review` took `c53_rubric_result: RubricResult` as an input — the exact wording that
  encoded the cycle. That block is replaced with `§3.0 Call-graph ordering (INT-1 fix)` which
  documents the one-directional graph: C52.phase_A → ReviewVerdict → C53.decide() →
  GoNoGoDecision → C52.phase_B. The `RubricResult = GoNoGoDecision` alias is retired.
- C52 state diagram and step 6b prose already reflect the two-phase ordering; no further C52
  diagram changes needed for INT-1 beyond what was already in place.

**Call graph now:** C52.submit_for_review → ReviewVerdict → C53.decide(satisfaction_distribution,
review_verdict, transfusion_verdict) → GoNoGoDecision → C52.deploy_if_approved. One-directional;
no cycle.

**Panel finding:** INT-1 (BLOCKER)

---

## FIX 2 — INT-2 (BLOCKER) — `factory_build` status enum collision resolved

**Files:** `spec/C20-bead-schema.md`, `spec/C52-self-bootstrap.md`

**What changed:**
- C20 §4.5.3: `status enum{in_progress, completed}` → `enum{in_progress, closed}`. Added INT-2
  reconciliation note in the D-40 block explaining that `completed` is not in the envelope's
  `{open, in_progress, closed}` and the go/no-go outcome lives in `milestone_verdict` instead.
- C20 §4.5.3 three-writer seam note: "advances `status` from `in_progress` to `completed`" →
  "advances `status` from `in_progress` to `closed`"; added clarification that `milestone_verdict`
  carries the go/no-go outcome.
- C52: all occurrences of `status=completed`, `advance_to_completed`, `enum{in_progress,completed}`
  updated to `status=closed` / `advance_to_closed` / `enum{in_progress,closed}`.
- C52 §5.1 state diagram: `advance_to_completed (status=completed)` → `advance_to_closed
  (status=closed)`; note updated to show `milestone_verdict=go set by C53`.
- C52 §3.5 Contract 7, §4.1 data table, §5.2 step 7, §6.1 loop-failure handling, §7 ops,
  §8/9 acceptance criteria and OQ3 all updated consistently.
- Resume/cold-start query unchanged: `gc bd find --type factory_build --status in_progress`
  (already correct). Finished builds now have `status=closed` + `milestone_verdict` on the bead.

**Enum now consistent:** envelope `{open, in_progress, closed}` ⊇ factory_build
`{in_progress, closed}`; no `completed` value anywhere.

**Panel finding:** INT-2 (BLOCKER)

---

## FIX 3 — INT-3 (MAJOR) — C09↔C05 ordering fixed to DispatchRequest-first

**Files:** `spec/C09-prompt-template-binding.md`

**What changed:**
- C09 §5.1 sequence diagram replaced entirely. Old diagram showed C12 calling `bind_and_render`
  first (C09 as entry point), then C05 building the DispatchRequest afterward — contradicting
  both C05 §5.1 (DispatchRequest-first) and D-35 (C09 reads `bead_id`/`created_by` FROM the
  DispatchRequest). If C09 ran first there is no DispatchRequest to read from.
- New diagram: C18/C12 caller assembles the DispatchRequest (with `bead_id` and `created_by`
  already present); C05.dispatch is the entry point; C05 calls C09 mid-dispatch; C09 extracts
  `BeadId`/`CreatedBy` from the already-present DispatchRequest; C09 returns RoutingKey +
  InstructionString to C05; C05 issues `gc sling` to C28. INT-3 fix note added above the diagram.
- AC-C09-10 updated to describe the DispatchRequest-first ordering explicitly (C05 has the
  DispatchRequest BEFORE C09 is called).

**Ordering now:** C05.dispatch(DispatchRequest) → C05 calls C09.bind_and_render → C09 reads
bead_id/created_by from DispatchRequest → C09 returns (RoutingKey, InstructionString) → C05
issues gc sling. Consistent with C05 §5.1 and D-35.

**Panel finding:** INT-3 (MAJOR)

---

## FIX 4 — INT-4 (MAJOR) — C41 actor-kind enum widened to include `tool`

**Files:** `spec/C41-identity-attribution.md`

**What changed:**
- C41 §3.1 `ActorRef.kind` enum: `"city" | "rig" | "agent"` → `"city" | "rig" | "agent" | "tool"`.
  INT-4 fix note added explaining why: C17 tool-nodes emit `created_by = "tool:inspect_eval"`;
  without `tool` in the enum `resolve_actor` raises E-C41-03 and breaks universality.
- C41 §4.1 field table `kind` column updated to `enum{"city","rig","agent","tool"}`.
- C41 §4.1 FAITHFUL-FILL note updated: explains `tool` as the fourth kind for automated tool-node
  actors, distinct from city/rig/agent personas.
- C41 §1 Responsibilities, §3 actor-kind-closure invariant, §6.1 E-C41-03 description, §8
  acceptance criterion 2, AC-C41-1 all updated to name `{city, rig, agent, tool}`.

**Enum now:** `{city, rig, agent, tool}`. `resolve_actor("tool:inspect_eval")` → `{kind="tool",
id="inspect_eval"}` without error (AC-C41-1 updated to test this).

**Panel finding:** INT-4 (MAJOR → canonically-required)

---

## Mermaid diagram validation

All touched diagrams validated with `validate_and_render_mermaid_diagram`:
- C52 §5.1 main recursion state diagram: **valid** (stateDiagram)
- C52 §5.1 resume sub-flow state diagram: **valid** (stateDiagram)
- C09 §5.1 template resolution sequence diagram: **valid** (sequence)
- C20 §5.1 bead lifecycle diagram: unchanged (not touched by these fixes)
- C53 §5.1 lifecycle diagram: unchanged (not touched by these fixes)

No `;` characters in any diagram label — SWEEP2-DISPATCH hazard clear.
