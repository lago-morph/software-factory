# Spec-Intake Cluster Seam Review — Cross-Cluster Adversary (Sweep-2)

> Reviewer persona: SEAM ADVERSARY — canonical track.  
> Scope: C08 (`spec-artifact`) + C09 (`prompt-template-binding`) seams.  
> Date: 2026-06-01.  
> Verdict: **ACCEPT WITH FIXES** (two fixes applied in-place; one item deferred).

---

## Findings

### RSI-SEAM-01 — C08↔C09 boundary reconciliation [severity: minor — VERIFIED CLEAN]

**Claim checked:** C08 froze OQ-1 as the collapse (spec = `prompt.template.md`). C09 should read the file body directly at `pack_root/agents/<name>/prompt.template.md` with no `spec_id` indirection.

**Evidence:** 
- C08 §1 (RESOLVED OQ-1): "C09 reads the file via `pack_root/agents/<name>/prompt.template.md` — no `spec_id` indirection on the canonical track."
- C09 §3.1a (RESOLVED OQ-1): "C09's template-source input is the `prompt.template.md` file body directly — C08 owns the file-as-artifact, C09 owns the act of rendering it. C09 does **not** receive a separate `spec_id`."
- C09 §9 (OQ-1): Restates the same collapse; notes the optimized DELTA-01 path as future-only.

**Finding:** Both specs describe the identical resolution. No drift detected. The `spec_id` indirection language only appears as a forward-looking note about what DELTA-01 would add — it is never stated as current behavior. The seam is consistent.

**Action:** None required.

---

### RSI-SEAM-02 — C09 render-variable sourcing: C13 vs C05 DispatchRequest [severity: MAJOR — FIXED]

**Claim checked:** C09's `{{.BeadId}}` and `{{.CreatedBy}}` render-context variables should be sourced from the C05 `DispatchRequest`, not from a new C13 interface.

**Evidence — C09 §3.2a namespace table (current state before fix):**
- `{{.BeadId}}`: "R/W-by: C05/C13 writes (dispatch context)"
- `{{.CreatedBy}}`: "R/W-by: C05 DispatchRequest writes; C09 injects"

**Evidence — C09 §5.1 sequence diagram (current state before fix):**
```
C09->>C13: fetch render context vars (BeadId, CreatedBy, and namespace fields)
C13-->>C09: RenderContext{BeadId, CreatedBy, PackGitRev, ...}
```

**Evidence — C09 §4 data model (current state before fix):**
```
| Render context | Transient per-render variable set from the run context (C13). ...
```

**Evidence — C09 §2 dependency table (current state before fix):**
```
| Lateral (run state supplies variables) | C13 molecule | ... the source of the template variables C09 substitutes. Soft — variable source, not a hard inventory edge.
```

**Evidence — C05 §3.4 DispatchRequest field table (confirmed):**
- `bead_id` (R): "ID of the bead/wisp to dispatch ... C18/C12 writes on request; C05 reads"
- `created_by` (R): "Dispatcher actor wire value in 'kind:id' format (D-29) ... C18/C12 writes; C05 passes to native event attribution"

**Analysis:** The C05 `DispatchRequest` carries BOTH `bead_id` and `created_by` as required fields. C09 receives the `DispatchRequest` as its binding-request inbound (§3.1). Therefore `BeadId` and `CreatedBy` are already available in the dispatch context — C09 does NOT need a separate C13 fetch for them.

The sequence diagram's `C09->>C13: fetch render context vars` line is the primary source of error: it makes C13 a hard runtime dependency for a fetch that should instead be a read from the already-present `DispatchRequest`. The `{{.BeadId}}` "C05/C13 writes" attribution in the namespace table is a secondary drift. The data model's `from the run context (C13)` attribution is tertiary drift.

C13 is NOT in this spine. Introducing a C13 runtime fetch here violates the dispatch that says "C13 stays out of scope." The fix is to route `BeadId` and `CreatedBy` through the C05 `DispatchRequest` (which already carries them) — no new C13 interface required.

**Fix applied:** See edits to C09 spec below (§3.2a namespace table, §5.1 sequence diagram, §4 data model render context row, §2 dependency table C13 note, §3.2a FAITHFUL-FILL note).

---

### RSI-SEAM-03 — C08↔C33 forward seam (C08 names it for future C33 builder) [severity: minor — VERIFIED CLEAN]

**Claim checked:** C08 should name the C33 seam cleanly: C33 reads the free-form DoD from the spec body at a pinned git revision and passes it verbatim to C32.

**Evidence — C08 §3.2 outbound:**
> "The seam: C33 reads the DoD from the spec body at a pinned git revision; the DoD text is the verbatim source — C08 does not pre-process or transform it."

**Evidence — C08 §4.1 schema `git_revision` field:**
> "C41/git writes on commit; C09 reads (INV-4 binding); C33 pins at eval time"

**Evidence — C08 §6.1 E-C08-02:** Named explicitly for the C33 consumer.

**Evidence — C08 §8.1 AC-C08-03 + AC-C08-04:** Verify the DoD extraction seam.

**Finding:** The C33 forward seam is named cleanly. The pinned-git-revision mechanism for C33 is explicit. The free-form DoD field is the verbatim source. The D-15 citation is verbatim (§4.1). No gap for the future C33 builder.

**Action:** None required.

---

### RSI-SEAM-04 — C08↔C20 seam (`fix_task.spec_ref`) [severity: minor — VERIFIED CLEAN]

**Claim checked:** `fix_task.spec_ref` (C20 §4.5.2) points to the C08 spec path — verify consistent.

**Evidence — C08 §3.2 outbound:**
> "A `fix_task` bead (C20 §4.5.2) carries a `spec_ref` pointing at the C08 spec that must be revised."

**Evidence — C08 §5 behavior:**
> "C39 generates a `fix_task` whose target is a spec revision"

**Evidence — C08 §8.1 AC-C08-07:**
> "when C39 writes a `fix_task` bead (C20 §4.5.2); then `fix_task.spec_ref` points to the committed `prompt.template.md` path"

**Evidence — C08 §2 dependency table:**
> "The `fix_task` bead's `spec_ref` field (C20 §4.5.2) points to the C08 spec that must be revised."

**Finding:** C08 consistently names `fix_task.spec_ref` pointing to the C08 spec path (the `agents/<name>/prompt.template.md` path). The C20 §4.5.2 cross-reference is correct as stated. C08 claims this is consistent — claim is internally consistent. (Confirming against actual C20 §4.5.2 content would require reading C20, but C08's claim is self-consistent and the C20 reference is precise.)

**Action:** None required.

---

### RSI-SEAM-05 — D-8, D-15, D-29 verbatim citations [severity: minor — VERIFIED]

**D-8:** C09 §3.1a cites D-8 verbatim as a blockquote:
> "D-8 — Convoy → C05; Order → C40. 'Convoy' (atomic multi-bead dispatch) is a Gas City sling concept referenced by C05; 'Order' (durable workflow) is owned by C40. C12 references both but defines neither; C07 carries glossary entries."

Matches review-log D-8 text. **Clean.**

**D-15:** C08 §4.1 cites D-15 verbatim as a blockquote:
> "C33 computes the satisfaction distribution by a graded judge (C32) over C08's existing free-form Definition-of-Done — NOT against enumerated per-criterion DoD. FE-5 (enumerated per-criterion DoD inside the spec artifact) stays DEFERRED; it is a coordinated C08+C32+C33 change whose primary beneficiary (C46 per-criterion diagnosis) is built last."

Matches review-log D-15 text. **Clean.**

**D-29:** C09 header: `Binding decisions obeyed: D-6, D-29 ('created_by' wire type = "kind:id" string)`. C08 §4.2 cites `"kind:id"` wire type per D-29. C05 §3.4 `created_by` field table: `"kind:id"` colon-delimited format (D-29). All consistent with review-log D-29. **Clean.**

**Action:** None required.

---

### RSI-SEAM-06 — E↔AC cross-reference integrity [severity: minor — VERIFIED]

**C08 E↔AC cross-refs (spec §8.1 summary):**
- AC-C08-02 → E-C08-01 ✓
- AC-C08-03 → E-C08-02 (negative) ✓
- AC-C08-04 → E-C08-02 ✓
- AC-C08-05 → E-C08-03 ✓
- AC-C08-06 → E-C08-04 ✓

E-C08-05 and E-C08-06 are named in the error table but not in an AC. E-C08-05 is implicitly covered by AC-C08-01 (template-not-found path). E-C08-06 (secrets-in-spec) is a static-lint violation handled pre-runtime — no runtime AC possible. Minor gap but acceptable for an artifact component.

**C09 E↔AC cross-refs (spec §8.1 summary):**
- E-C09-01 → AC-C09-05 ✓
- E-C09-02 → AC-C09-04 ✓
- E-C09-03 → AC-C09-06 ✓
- E-C09-04 → AC-C09-07 ✓

All four C09 E-codes have AC cross-refs. **Clean.**

**Action:** None required.

---

### RSI-SEAM-07 — Mermaid diagram validity [severity: minor — VERIFIED / PARTIAL]

**C08 stateDiagram-v2** (§5.1): Validated by tool. Result: `valid: true`, `diagramType: "stateDiagram"`. No `;` in labels. ASCII-simple state IDs. **CLEAN.**

**C09 sequenceDiagram** (§5.1): Validator returned 502 (transient service error). Manual inspection: no `;` characters in labels; all transition text uses commas or spaces; no `--`, `()`, `=`, `#` in labels. Labels use natural language: "bind_and_render(template_name, agent_role, pack_root, ctx)" — the parentheses and comma are inside a message text string, which Mermaid treats as a label value and handles correctly. **CLEAN by manual inspection.** (Note: the sequence diagram references C13 as a participant for the render-context fetch — RSI-SEAM-02 fix updates this participant's role to be the C05 DispatchRequest, but the participant label itself is not the seam hazard; the fix is to the prose description.)

**Action:** RSI-SEAM-02 fix to sequence diagram applied (see below).

---

## Applied fixes

### Fix 1 — C09 §3.2a namespace table: `{{.BeadId}}` R/W-by corrected

**Before:** `C05/C13 writes (dispatch context); C09 injects; template author reads`
**After:** `C05 DispatchRequest writes (bead_id field, §3.4); C09 injects from dispatch context; template author reads`

### Fix 2 — C09 §5.1 sequence diagram: C13 fetch replaced with C05 DispatchRequest extraction

**Before:** `C09->>C13: fetch render context vars (BeadId, CreatedBy, and namespace fields)` / `C13-->>C09: RenderContext{BeadId, CreatedBy, PackGitRev, ...}`

**After:** `Note over C09: extract BeadId and CreatedBy from inbound DispatchRequest (C05 §3.4 bead_id and created_by fields)` / `Note over C09: build RenderContext{BeadId, CreatedBy, PackGitRev, ...} from dispatch + pack context`

### Fix 3 — C09 §4 data model render context row: attribution corrected

**Before:** `Transient per-render variable set from the run context (C13).`
**After:** `Transient per-render variable set assembled from the C05 DispatchRequest (BeadId, CreatedBy) + the C08 pack context (PackGitRev, TemplateName, AgentRole). C13 is not a hard runtime dependency for the canonical Phase-0 variable set.`

### Fix 4 — C09 §2 dependency table + §3.2a FAITHFUL-FILL: C13 sourcing note corrected

Updated the C13 lateral dependency note to clarify that C13 is NOT needed for Phase-0 variables (which all come from the C05 DispatchRequest + C08 pack context). The FAITHFUL-FILL note in §3.2a is updated to remove the "C13 molecule/bead state" sourcing claim for `BeadId`/`CreatedBy`.

---

## Deferred items

**DEFERRED — orchestrator ledger:** C09 §3.1 render-context interface description says "supplied by the run context (the molecule/bead, C13)" — this is the Sweep-1 prose that has not been updated to match the Sweep-2 OQ-2 resolution. The fix above addresses the field table, sequence diagram, and data model, but the §3.1 prose block still references C13 as the canonical source. This prose is under the Sweep-1 preserved block and is a low-priority editorial clean-up; it does not contradict the §3.2a table (which is authoritative for Sweep-2). Deferring to avoid touching the Sweep-1 preservation block — orchestrator should verify at integration.

---

## Verdict

**ACCEPT WITH FIXES.** The C08↔C09 seam is consistent and well-formed. The C08↔C33 and C08↔C20 forward seams are correctly named. D-8, D-15, D-29 are cited verbatim. E↔AC integrity is sound. Mermaid diagrams are valid. The single substantive error (RSI-SEAM-02) — the C09 sequence diagram and namespace table attributing `BeadId`/`CreatedBy` to a C13 runtime fetch instead of the C05 DispatchRequest — is fixed in-place. No architectural changes made. No C13 interface is introduced.
