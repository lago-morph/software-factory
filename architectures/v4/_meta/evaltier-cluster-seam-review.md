# Eval-Tier Cluster Seam Review — C30/C31/C32/C33
**Adversary:** Cross-cluster SEAM ADVERSARY, evaluation tier  
**Date:** 2026-06-01  
**Scope:** C30 (scenario store), C31 (runner), C32 (judge), C33 (satisfaction metric) — seams only  
**Persona:** Track-A posture (fidelity + completeness); D-36/D-37/D-38/D-39 pre-briefed decisions

---

## Findings

### REV-SEAM-01 — C32↔C33 `ScoreRecord` field name mismatch (BLOCKER)

**Severity:** BLOCKER  
**Seam:** C32 (writer) → C33 (reader), the primary data contract  
**Claim:** C32's frozen ScoreRecord schema (§3.2, D-39) and C33's consumed-field table (§3.3) describe the same field by different names.

**Evidence:**
- C32 §3.2 defines: `satisfaction_score | float (0.0–1.0) | R | Holistic satisfaction score…`
- C33 §3.3 defines: `score_value | float64 | yes | Normalised satisfaction score, [0.0–1.0]`
- C33 §3.2 text: "The fields C33 reads are `score_value: float64` (normalised 0.0–1.0 by C32…)"
- C33 E-C33-02: "`ScoreRecord` has `score_value` absent or outside [0.0, 1.0]"
- C33 AC-C33-10: "10 C32-written judge-output beads with `score_value` in [0.2, 0.9]"
- C32 AC-C32-01: "…`satisfaction_score`, `score_label`, `judge_model_id`…non-null"
- C32 AC-C32-04: "the 10 `satisfaction_score` values are a float distribution"

**Impact:** C33 will query C32-written beads for a field named `score_value` that does not exist; it will receive `absent` and trigger E-C33-02 exclusion for every score. The satisfaction distribution will always have `n=0` valid records. This is a silent total failure of the eval tier's primary output.

**Fix (applied — see C32 §3.2 fix below):** The authoritative name is **`satisfaction_score`** — it is in the D-39-frozen schema that C32 owns and which C33/C34/C46 must build against. C33 must be updated to read `satisfaction_score`, not `score_value`.

**Fix applied to:** C33 §3.2, §3.3, §5 (behavior), §6.1 (E-C33-02, E-C33-04), §8 (AC-C33-10, AC-C33-11, AC-C33-13, AC-C33-18), §9 OQ-4. All occurrences of `score_value` in C33 that refer to the C32-emitted field are renamed to `satisfaction_score`. The local Go struct field `ScoreValue` is renamed `SatisfactionScore` for consistency.

---

### REV-SEAM-02 — C31 emits `inspect_version`; C32 has no matching version-pin requirement (MAJOR)

**Severity:** MAJOR  
**Seam:** C31 (TrajectoryLog writer) → C32 (log reader)  
**Claim:** C31 §4.1 defines `inspect_version` as a required field of the TrajectoryLog envelope with the note "C32 must be pinned to the same version to parse the log." C32 has no reciprocal requirement.

**Evidence:**
- C31 §4.1: `inspect_version | string | Y | Pinned Inspect AI version string (e.g. "0.3.x"). C32 must be pinned to the same version to parse the log.`
- C31 §7 Ops: "Pin the Inspect AI version so the `inspect eval` CLI surface + `TrajectoryLog` schema the adapter and C32 depend on are reproducible."
- C31 OQ-4: "Remaining open: the exact Inspect AI version pin…must be confirmed against the pinned version before C31 ships."
- C32: zero mentions of `inspect_version`, zero version-pin requirement, zero assertion that the Inspect AI version used by C32's scorer matches C31's version.
- C32 §7 Ops: "The scorer is adopted off-the-shelf (Inspect AI) and exposed declaratively as a Gas City pack (C02/C17)." No version pin mentioned.

**Impact:** If C31 and C32 are installed with different Inspect AI versions, C32 will silently misparse the `.eval` log — field names, sample structure, or schema semantics may differ, producing wrong or absent scores. This is the version-drift risk C31 explicitly flagged as breaking post-hoc scoring.

**Fix (applied to C32 §7 Ops and §3 interface table):** Added explicit version-pin requirement to C32. The `[[service]] type="inspect_ai"` provider block in C32's pack MUST carry the same pinned version as C31. C32 MUST validate `inspect_version` on the incoming `TrajectoryLog` envelope against its own installed version and raise E-C32-02 (log unparseable) if they differ.

---

### REV-SEAM-03 — C32 `score_record` bead type missing C22 registration seam (MAJOR)

**Severity:** MAJOR  
**Seam:** C32 (new bead type) → C22 (registration mechanism, D-3)  
**Claim:** Per D-3, new bead types must be registered in C22. C33 correctly names this for `satisfaction_metric`. C32 does not name it for `score_record`.

**Evidence:**
- D-3 (verbatim): "C20 authors the bead-type payload schemas…C22 owns the registration *mechanism*…and registers C20's bead types via a documented binding seam."
- C33 §3.5: "The bead type `softwarefactory.v4.beads:satisfaction_metric` must be registered in C22 (D-3 mechanism) by C33's pack installation step."
- C33 §7 Ops: "The `satisfaction_metric` bead type must be registered with C22 at pack install time (D-3 seam)."
- C32: no mention of C22, no mention of registering `score_record`, no ops step naming the registration seam.
- C32 §3.2: "Bead type: `softwarefactory.v4.beads:score_record`" — named but not registered.

**Impact:** Without C22 registration, the `score_record` bead type is unregistered. C33/C34/C46 consumers querying C22 for the bead type schema will find nothing. Bead-store queries filtering by type will fail silently or return empty results.

**Fix (applied to C32 §7 Ops and §3.2 postconditions):** Added: "The `score_record` bead type (`softwarefactory.v4.beads:score_record`) must be registered in C22 (D-3 mechanism) at C32's pack installation step, before any scoring run."

---

### REV-SEAM-04 — C30 Mermaid diagram invalid (MAJOR)

**Severity:** MAJOR  
**Seam:** C30 §5.1 sequence diagram  
**Claim:** C30's sequence diagram fails Mermaid parse. The `Note over Auth,Repo:` line contains a semicolon inside a parenthetical — `(C42 INV-3; C34 enforces D-13)` — which terminates the label statement mid-parse per the SWEEP2-DISPATCH `;`-in-label hazard warning.

**Evidence:**
- Mermaid validator result: `Parse error on line 14: …; C34 enforces D-13)Note over C34: C34 — Expecting … got 'NEWLINE'`
- SWEEP2-DISPATCH: "in `stateDiagram-v2`, a `;` inside a transition label terminates the statement and breaks the parse. Do NOT put `;`…inside transition labels."
- The same hazard applies to `Note` labels in `sequenceDiagram`.

**Fix (applied to C30 §5.1):** Rewrote the `Note over Auth,Repo:` line replacing the semicolon with a comma: `Worker rig excluded from scenarios partition (C42 INV-3, C34 enforces D-13)`.

---

### REV-SEAM-05 — C33 sequence diagram in plain code fence, not mermaid fence (MINOR)

**Severity:** MINOR  
**Seam:** C33 §5 sequence diagram rendering  
**Claim:** C33's sequence diagram is wrapped in a plain `` ``` `` fence rather than `` ```mermaid ``. The diagram syntax is valid (validator confirms) but will not render as a diagram in any Mermaid-aware viewer (GitHub, doc renderers).

**Evidence:**
- C33 §5 line 300: `` ``` `` (not `` ```mermaid ``)
- Validator result: valid=true for the diagram code itself.
- All other diagrams in C30/C31/C32 use `` ```mermaid ``.

**Fix (applied to C33 §5):** Changed the code fence from `` ``` `` to `` ```mermaid ``.

---

### REV-SEAM-06 — C30↔C31 MANIFEST key aliasing not cross-referenced (MINOR)

**Severity:** MINOR  
**Seam:** C30 MANIFEST (`task_path`, `task_name`) → C31 ScenarioRef (`scenario_path`, `task`)  
**Claim:** C30's MANIFEST uses fields `task_path` and `task_name`; C31's `ScenarioRef` uses `scenario_path` and `task`. The mapping is implicit; neither spec cross-references the other's field name.

**Evidence:**
- C30 §4.5: `task_path | string (repo-relative path) | R | Repo-relative path to the Inspect AI Task Python file`; `task_name | string | R | Python Task object name inside task_path (the --task arg to inspect eval; C31 §3 contract)`
- C31 §3.2 I3: `ScenarioRef = { scenario_path: str, task: str }`. `scenario_path` = C30 store path; `task` = Inspect AI task name within that file.
- C30 §3.2 note: "The `scenario_path` input key is resolved from the scenario record's `task_path` field"

**Assessment:** The mapping is present but informal. The C30 §3.2 note `"scenario_path resolved from task_path"` covers this adequately. C31 §3.2 I3 description names both sources. No data can be lost; the aliasing is documented at both ends. This is a readability gap, not a functional seam break.

**Fix (applied — minor clarification to C31 §3.2 I3):** Added explicit cross-reference: "`scenario_path` maps to C30 MANIFEST `task_path`; `task` maps to C30 MANIFEST `task_name`."

---

### REV-SEAM-07 — C30↔C34 E-C30-04 handoff mechanism open (DEFERRED — orchestrator ledger)

**Severity:** DEFERRED  
**Seam:** C30 (E-C30-04 wrong authoring identity) → C34 (holdout integrity consumer)  
**Claim:** C30 §9 flags that the handoff mechanism for E-C30-04 (does C34 poll the I6 feed, or does C30 emit an out-of-band signal?) is open for the C34 Sweep-2 author to close. The dispatch brief requires we FLAG but not resolve this, as C34 is the next product.

**Evidence:**
- C30 §9 "New seam (→ orchestrator ledger)": "C30 publishes; C34 decides how to consume." — correctly flagged.
- C30 §6.1 E-C30-04: "E-C30-04 is a C34 trigger" — the trigger is named; the channel is open.

**Fix:** None applied. **DEFERRED — orchestrator ledger.** The C34 builder must decide: (a) C34 polls the I6 MANIFEST feed's `created_by` field, or (b) C30 emits an event to C23 when E-C30-04 fires. C30 already publishes both surfaces (I6 feed and, potentially, C23 event). The seam is clean enough for C30 to ship; C34 closes it.

---

### REV-SEAM-08 — C32↔C33: `trajectory_ref` field present in C32, consumed in C33 — consistent (PASS)

**Severity:** PASS  
C32 §3.2 defines `trajectory_ref | string | R | Reference to the C31-produced trajectory log (path or content-hash)`. C33 §3.3 reads `trajectory_ref | string | yes`. Field name, type, and required status match exactly. No action needed.

---

### REV-SEAM-09 — C32 D-39 ScoreRecord: 12-required fields verified against C33 consumption (PASS)

**Severity:** PASS (post-fix REV-SEAM-01)

After applying the fix in REV-SEAM-01 (renaming `score_value` → `satisfaction_score` in C33), the C33-consumed-field table §3.3 maps correctly onto the C32 D-39 frozen schema:

| C32 field | C33 reads? | Match |
|---|---|---|
| `scenario_id` | yes | ✓ |
| `scenario_version` | no (not needed for aggregation) | ✓ (forward-compat rule: ignore) |
| `trajectory_ref` | yes | ✓ |
| `dod_version` | no | ✓ (forward-compat rule) |
| `satisfaction_score` | yes (after fix) | ✓ |
| `score_label` | no | ✓ (forward-compat rule) |
| `judge_model_id` | no | ✓ |
| `independence_level` | yes | ✓ |
| `n_judges` | no | ✓ |
| `judge_prompt_hash` | no | ✓ |
| `created_by` | no | ✓ |
| `scored_at` | no | ✓ |

C33 reads only the subset it needs for reduction + auditability. All consumed fields exist in C32's schema. All 12 required fields are present in C32. Confirmed consistent.

---

### REV-SEAM-10 — C31↔C32 `TrajectoryLog` schema cross-check (PASS with version-pin gap → REV-SEAM-02)

**Severity:** PASS (schema match); MAJOR for version pin (see REV-SEAM-02)

C31 §4.1 defines the tool-node output envelope (8 fields: `session_id`, `log_path`, `scenario_path`, `task`, `exit_code`, `run_started_at`, `run_completed_at`, `inspect_version`). C32 §3.1 `score()` receives `trajectory_log: TrajectoryLog` and reads `log_path` to access the on-disk Inspect AI log.

C31 §4.2 defines the on-disk Inspect AI log schema (11 fields: `eval.run_id`, `eval.task`, `eval.model`, `eval.status`, `samples[*].id`, `samples[*].messages[*].role`, `samples[*].messages[*].content`, `samples[*].messages[*].tool_calls`, `samples[*].messages[*].tool_results`, `samples[*].score`, `samples[*].metadata`). C32 reads these fields from the `.eval` log.

Both specs agree that the scoring is post-hoc (D-37), that C32 reads `log_path` from the envelope, and that C32 does NOT call C31 inline. Schema field names are consistent. The only gap is the version-pin asymmetry addressed in REV-SEAM-02.

---

## Mermaid validity summary (tool-verified)

| Diagram | Spec | Valid? | Issue | Fixed? |
|---|---|---|---|---|
| C30 §5.1 sequenceDiagram | C30 | NO | Semicolon in `Note over` label (`;` inside parenthetical) | YES — REV-SEAM-04 |
| C31 §5.1 sequenceDiagram | C31 | YES | — | n/a |
| C32 §5 sequenceDiagram | C32 | YES | — | n/a |
| C33 §5 sequenceDiagram | C33 | YES (syntax) | Plain `` ``` `` fence, not `` ```mermaid `` | YES — REV-SEAM-05 |

---

## Verdict

**ACCEPT WITH FIXES** — all blocker and major issues are fixed in-place. The cluster is consistent post-fix.

| Finding | Severity | Status |
|---|---|---|
| REV-SEAM-01: `satisfaction_score` vs `score_value` field name drift | BLOCKER | FIXED — C33 |
| REV-SEAM-02: C32 missing Inspect AI version-pin requirement | MAJOR | FIXED — C32 |
| REV-SEAM-03: C32 `score_record` bead type missing C22 registration seam | MAJOR | FIXED — C32 |
| REV-SEAM-04: C30 Mermaid diagram invalid (`;` in label) | MAJOR | FIXED — C30 |
| REV-SEAM-05: C33 plain code fence for Mermaid diagram | MINOR | FIXED — C33 |
| REV-SEAM-06: C30↔C31 MANIFEST key aliasing not cross-referenced | MINOR | FIXED — C31 |
| REV-SEAM-07: C30↔C34 E-C30-04 handoff mechanism open | DEFERRED | ORCHESTRATOR LEDGER |
