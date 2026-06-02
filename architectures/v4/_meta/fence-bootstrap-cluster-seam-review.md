# Fence + Bootstrap cluster — cross-cluster seam adversary review
# (C34 holdout, C43 boundary-typing, C51 transfusion, C52 self-bootstrap, C53 go/no-go apex)
# Reviewer: cross-cluster SEAM ADVERSARY, 2026-06-01

---

## Scope

Components reviewed: C20 (bead schema — factory_build D-40 refine), C34, C43, C51, C52, C53.
Deps checked: C20, C42, C30, C32, C33, C51, review-log D-1/D-13/D-15/D-20/D-21/D-30/D-38/D-39/D-40.
This review attacks SEAMS only — field-name drift, untyped hand-off surfaces, watcher-design bleed, D-30 posture consistency, C20 factory_build schema completeness per D-40.

---

## Findings

### RFB-SEAM-01 — BLOCKER — C20 `factory_build` schema missing ALL D-40 fields

**Claim:** D-40 (adopted 2026-06-01) rules that the in-progress→completed build advance is a STATUS transition on a single `factory_build` bead, and that C51 writes `transfusion_verdict`, C52 writes `gate_decision`, and C53 writes `milestone_verdict`/`milestone_evidence`/`milestone_decided_at` — all on the same bead. C53 §3.4 explicitly registers this as a NEW SEAM to the orchestrator ledger. However, C20 §4.5.3 still carries only the three pre-D-40 fields (`transfused_from`, `spec_ref`, `scenario_ref`) and the common envelope. The following required D-40 fields are entirely absent from the C20 schema:

- `status` enum `{in_progress, completed}` — the D-40 lifecycle field for `factory_build`
- `gate_decision` JSON slot — C52's human-review record
- `transfusion_verdict` JSON slot — C51's predicate verdict
- `milestone_verdict` string — C53's go/no-go outcome
- `milestone_evidence` JSON-blob — C53's GoNoGoDecision evidence bundle
- `milestone_decided_at` ISO-8601 string — C53's decision timestamp
- `workflow_handle` handle field — needed for D-40 `status=in_progress` resume

**Note:** C20 also retains a `factory_build_in_progress` as a distinct type, which directly conflicts with D-40's ruling that the transition is a status field, not a type-flip. C20 §4.1 FAITHFUL-FILL note and §4.5.4 section keep the pre-D-40 interpretation.

**Evidence:** C20 §4.5.3 field table (3 fields only); C52 §4.1 field table listing `gate_decision` as a C20 slot-request; C53 §3.4 "NEW SEAM" block requesting `milestone_verdict`, `milestone_evidence`, `milestone_decided_at`; review-log D-40 verbatim: "Applied: C20 (factory_build lifecycle + status slot), C52 (build-state advance), C53 (go/no-go record)."

**Fix:** Add all D-40 fields to C20 §4.5.3, update the `type` enum in §4.5.0 to remove `factory_build_in_progress` from the primary D-40 path (or annotate it per D-40 resolution), add `status enum{in_progress, completed}` specific to the `factory_build` bead, add `workflow_handle`, `gate_decision`, `transfusion_verdict`, and the three milestone slots. Bump the bead-type version note. **APPLIED** — see C20 §4.5.3-extended below.

---

### RFB-SEAM-02 — BLOCKER — C20 missing `score_record` and `satisfaction_metric` eval-tier bead types (D-3 per-D-39)

**Claim:** D-3 rules C20 authors bead-type payload schemas for ALL bead types in the factory, including eval-tier types. D-39 freezes `ScoreRecord` schema ownership at C32; C33 defines `satisfaction_metric`. Both C32 (§3.5 REV-SEAM-03) and C33 (§3.5/§7 Ops) note these types MUST be registered in C22 via the D-3 mechanism — but C20 §3.1 bundle table and the registered type list do not include `score_record` or `satisfaction_metric`. The bundle document C20 hands to C22 is therefore incomplete.

**Evidence:** C20 §3.1 `register_bundle` block lists only: `override`, `fix_task`, `factory_build`, `factory_build_in_progress`, `anomaly`, `diagnosis`, `resolution`. C32 §3.5 REV-SEAM-03 says `score_record` "MUST be registered in C22 (D-3 mechanism)". C33 §3.5/§7 Ops says `satisfaction_metric` bead type "must be registered with C22 at pack install time (D-3 seam)".

**Fix:** Add `score_record` (C32-owned schema, D-39) and `satisfaction_metric` (C33-owned schema) to C20 §3.1 bundle manifest with schema-ownership cross-references. These are REGISTRATIONS of externally-authored schemas, not new C20 schema inventions. **APPLIED** — see C20 §3.1 addendum.

---

### RFB-SEAM-03 — MAJOR — C52↔C53 `RubricResult` shape is undefined in C53; only `GoNoGoDecision` is defined

**Claim:** C52 §3.4 `submit_for_review` takes `c53_rubric_result: RubricResult` as a typed parameter. C53 defines `GoNoGoDecision` (the output of `decide()`) but does NOT define a type named `RubricResult`. The hand-off type from C53→C52 is therefore untyped — C52 references a type that C53 never defines. This is a seam-shape mismatch: `RubricResult` ≠ `GoNoGoDecision`.

**Evidence:** C52 §3.4 signature: `c53_rubric_result: RubricResult`. C53 §3.1: defines `GoNoGoDecision` and `GoNoGoInput` — no `RubricResult` struct defined anywhere in C53. C52 AC-C52-05 refers to "C53's `RubricResult`" as if it is C53's exported type, but C53 never exports it.

**Severity:** MAJOR (not BLOCKER) because the seam is logically coherent — `RubricResult` is plainly `GoNoGoDecision` by another name — but without an explicit alias the contract is unverifiable across component boundaries.

**Fix:** Add a `RubricResult` type alias to C53 (= `GoNoGoDecision` with a note that it is C53's outbound face toward C52's `submit_for_review` gate). **APPLIED** — see C53 §3.1 addendum.

---

### RFB-SEAM-04 — MAJOR — C51→C52 `transfusion_verdict` field name drift

**Claim:** C51 §4.1.2 defines `transfusion_verdict` as a sub-struct with fields `outcome`, `completeness_result`, `correctness_result`, `scenario_ids`, `verdict_time`, `signed`. C52 §4.1 lists `transfusion_verdict` as a field on the `factory_build` bead with type `TransfusionVerdict (JSON)`. The field name matches, but C52 §4.1 also lists a separate `gate_decision` field as `GateDecision (JSON)` with the note "C53 records go/no-go here (D-40)" — which contradicts C53 §3.4 where C53's three fields are `milestone_verdict`, `milestone_evidence`, `milestone_decided_at` (NOT `gate_decision`). C52 §4.1 conflates C52's gate record with C53's milestone record under a single `gate_decision` field.

**Evidence:** C52 §4.1: `gate_decision: GateDecision (JSON)` with R/W-by "C53 records; C52 reads to decide advance." C53 §3.4: C53 writes `milestone_verdict`, `milestone_evidence`, `milestone_decided_at` — NOT `gate_decision`. C52 §3.4 `GateDecision` struct is C52's output record from `submit_for_review`; it should be the C52 reviewer record, not the C53 milestone record.

**Severity:** MAJOR. The field `gate_decision` in C52 §4.1 conflates two distinct records: (a) C52's human-review result and (b) C53's go/no-go milestone verdict. These are separate schema slots per C53 §3.4.

**Fix:** Clarify in C52 §4.1 that `gate_decision` is C52's own human-review record (the reviewer_id/decision/timestamp), and add the three C53 milestone fields as a distinct entry. Also add the `workflow_handle` field that C52 §3.3/§3.5 references but §4.1 lists without explicit schema assignment. **APPLIED** — see C52 §4.1 clarification note.

---

### RFB-SEAM-05 — MINOR — C34 and C43 D-30 watcher: both correctly DEFERRED; confirm consistent

**Claim:** D-30 requires that both C34 and C43 hold the HumanGated posture for unattended (P2)/self-modification (P3b) until the D-23 spike resolves; neither designs the watcher. Both specs carry D-30 verbatim citations. Both specs explicitly state "DO NOT design the watcher here" or equivalent language.

**Evidence:**
- C34 §9 OQ-C34-1: "C34 does NOT design that watcher; its design is deferred until the spike result confirms it is needed."
- C34 tail: "[D-30 ADOPTED 2026-06-01 — prevent/block required for unattended]" with the verbatim D-30 decision text.
- C43 §3.2 OQ-C43-1: "DO NOT design the watcher here (D-30 deferred; AGENTS-MD-bf4431be57)."
- C43 tail: "[D-30 ADOPTED 2026-06-01 — prevent/block required for unattended]" with the verbatim D-30 decision text.
- Both OQ-C34-1 and OQ-C43-1 stay OPEN on the D-23 spike — consistent with review-log §D-23 harvest ("Prevent-vs-detect remains OPEN").

**Verdict:** CONSISTENT. No action required. Both cite D-30 verbatim; neither designs the watcher. The HumanGated posture is the operative state in C43's §5.1 state diagram. PASS.

---

### RFB-SEAM-06 — MINOR — C53 go/no-go rule shape correctly flagged as OPERATOR-JUDGMENT item with working default

**Claim:** The dispatch requires C53's go/no-go rule shape to be (a) flagged as an OPERATOR-JUDGMENT item and (b) carry a working default so it isn't blocked.

**Evidence:**
- C53 §3.1 OQ-1 RESOLVED: "**OPERATOR-JUDGMENT FLAG (OQ-1):** The choice of which statistics gate the FIRST SELF-MODIFICATION go/no-go — the apex point of bet #3 — is an architectural/safety value judgment, not a mechanical engineering choice. … The SHAPE selected here (p10+mean) is the recommended engineering default; **the operator MUST review and sign off on this rule shape** as a morning-review item before the milestone is armed."
- Working default is explicit: `p10 >= T_tail AND mean >= T_central` over N-scenario run, with all threshold VALUES as operator-policy knobs in MilestoneConfig §3.3.
- The milestone is NOT blocked — it has a concrete working default.

**Verdict:** CORRECT. Both requirements satisfied. PASS.

---

### RFB-SEAM-07 — MINOR — C20 `factory_build_in_progress` vs D-40 status-transition — faithful-vs-D-40 tension

**Claim:** D-40 rules that the transition is a `status` field on a single `factory_build` bead type, not a type-flip to/from `factory_build_in_progress`. However, C20 was written under the faithful-track (pre-D-40) interpretation and keeps `factory_build_in_progress` as a distinct registered type and §4.5.4 schema section. C52 and C53 are fully D-40-compliant (they use `--type factory_build --status in_progress`). C20 has a consistency obligation to reflect D-40.

**Evidence:** C20 §4.2 type table: `factory_build_in_progress` listed as a named type. C52 §3.1 Contract 2: `gc bd find --type factory_build --status in_progress` (D-40 corrected query). C20 §4.5.4 still has a `factory_build_in_progress` section with a separate schema.

**Severity:** MINOR (not BLOCKER) — the schema slot logic still works; the `factory_build_in_progress` type can remain as a registered legacy alias as long as C20 annotates the D-40 path and the status field on `factory_build` is the canonical lifecycle.

**Fix:** Annotate C20 §4.5.4 with the D-40 ruling that the canonical path is `factory_build + status=in_progress`; retain the section as a legacy-compatibility note per D-40 (XC-2 resolution). Add `status enum{in_progress, completed}` to §4.5.3. **APPLIED** — see C20 §4.5.3-extended.

---

### RFB-SEAM-08 — DEFERRED — C52 OQ5/G14 class-level fallback → C54

C52 §10 OQ5 and C51 OQ-C51-2 both note that the class-level fallback for "a whole high-value class (Healer/twins/self-opt) cannot be reliably transfused" is a C54 phase-plan decision. This is an architectural scope/sequencing question that the orchestrator must route to C54. **DEFERRED — orchestrator ledger** per the dispatch instruction (non-spine deferral, known from C51/C52).

---

## Applied fixes summary

1. **C20 §4.5.3** — Added D-40 extended fields: `status enum{in_progress, completed}`, `workflow_handle`, `gate_decision`, `transfusion_verdict`, `milestone_verdict`, `milestone_evidence`, `milestone_decided_at`. Added D-40 verbatim citation. Added bead-type-version bump note. (RFB-SEAM-01 fix.)
2. **C20 §3.1** — Added `score_record` (C32) and `satisfaction_metric` (C33) to the bundle manifest as eval-tier bead type registrations per D-3. (RFB-SEAM-02 fix.)
3. **C53 §3.1** — Added `RubricResult` as an explicit type alias for `GoNoGoDecision` (C53's outbound type toward C52's `submit_for_review` gate). (RFB-SEAM-03 fix.)
4. **C52 §4.1** — Added clarifying note distinguishing C52's `gate_decision` (human-review record) from C53's three milestone fields; added the C53 milestone fields explicitly to the bead field table. (RFB-SEAM-04 fix.)
5. **C20 §4.5.4** — Annotated `factory_build_in_progress` with D-40 ruling (canonical path = `factory_build + status=in_progress`; this type retained as legacy alias per XC-2). (RFB-SEAM-07 fix.)

## Deferred (not applied)

- **RFB-SEAM-08** (OQ5/G14 → C54 class-level fallback) — DEFERRED — orchestrator ledger. C54 must confirm it owns the class-level hedge so G14 is fully homed.

---

## Verdict

**ACCEPT WITH FIXES.** The five applied fixes resolve two blockers (C20 schema gaps — D-40 fields and eval-tier bead registrations) and three major/minor seam shape issues. The remaining deferred item is a known non-spine architectural question (C54 phase-plan ownership of G14 class-level fallback) appropriately deferred. The C34/C43 watcher-design posture is consistent (D-30 verbatim cited in both; watcher not designed; OQ-C34-1 ≡ OQ-C43-1 correctly left OPEN). The C53 operator-judgment flag is present with a working default. After the applied fixes the five-component cluster has consistent field names across the C51→C52→C53 `factory_build` bead record seam.
