# Claude Max Cluster — Cross-Seam Adversary Review (Sweep-2)

**Reviewer persona:** Cross-cluster seam adversary (ADVERSARY-BRIEF.md, convergence-banner track-A posture).
**Scope:** C28 (Claude Code agent loop) + C29 (model floor & stylesheet) + claudemax-integration-runbook;
  deps checked: C04 (session provider), C02 (pack & tool-node ABI).
  Binding decisions checked: D-1, D-10, D-30, D-34.
**Cannot edit:** other cluster docs; review-log.md (append-only by lead/collector).
**Date:** 2026-06-01

---

## Findings

### RCM-SEAM-01 — BLOCKER  
**Seam:** C28↔C04 — `CLAUDE_CODE_OAUTH_TOKEN` delivery mechanism is ambiguous and creates a latent
contradiction between C28 §3.3 ("set in `[[agent]] env = {…}`") and the runbook/prototype ("container
env inheritance")

**The two readings:**

- **Reading A — explicit `[[agent]] env` declaration:** C28 §3.3 header states injected env vars are
  "set in `[[agent]] env = { … }`"; the table immediately below lists OTEL vars and `IS_SANDBOX` but
  does NOT list `CLAUDE_CODE_OAUTH_TOKEN`. C04 §8 likewise lists only `IS_SANDBOX` in its `.env /
  container environment` block. C04 I3 says "injects the OAuth-derived auth + full OTEL env block."
  The implication is that `CLAUDE_CODE_OAUTH_TOKEN` is one of the env vars C04 *explicitly* injects
  through the `[[agent]] env` path.

- **Reading B — container-env inheritance:** The runbook §1.1 shows the prototype delivery mechanism:
  `export CLAUDE_CODE_OAUTH_TOKEN=$(cat /home/claude/.claude/remote/.oauth_token)` set in the
  *container environment* (`docker-compose env:` section). The prototype's `gc start --foreground`
  then spawns tmux panes whose processes **inherit** the container env, so `CLAUDE_CODE_OAUTH_TOKEN`
  reaches the `claude` process without being explicitly declared in `[[agent]] env`. The runbook §2.1
  explicitly says "pass via container env for Phase-0" and notes the `[[agent]] env = {…}` form is
  deferred to G11 for key-spelling verification.

**The operational risk:** If a builder reads C28 §3.3 and concludes `CLAUDE_CODE_OAUTH_TOKEN` must be
in `[[agent]] env = {…}`, but the actual `gc` implementation does NOT relay `[[agent]] env` keys into
the tmux pane spawn (or STRIPS vars matching `TOKEN`/`OAUTH` patterns for security), the agent will
boot without auth and fail silently (every API call returns 401 → E-C28-03, session stalls). The
runbook's Phase-0 workaround (container-env inheritance) works *only if* `gc` passes through container
env to pane subprocesses — which is unverified (`[needs G11 verification]`). Whether `gc`'s
`internal/execenv` strips or filters `TOKEN`/`OAUTH`-bearing vars before spawning operator commands is
also unknown.

**This is the "needs-G11" env-forwarding seam the dispatch brief identified as the sharpest one.**

**Required fix:** Explicitly name this as an `[OPEN SEAM: needs-G11]` in BOTH C28 §3.3 AND C04 §8,
with both readings and the operational risk stated. Do not invent the answer.

**Status:** Applied — see C28 §3.3 and C04 §8 seam note additions below.

---

### RCM-SEAM-02 — MAJOR  
**Seam:** C28 — E-code cross-reference error: E-C28-03 (Auth-expiry) used in sequence diagram and
AC-C28-04 to denote ToolDenied (hook-deny), which is a different failure condition

**Evidence:**
- E-code table §6.1: `E-C28-03` is defined as **Auth-expiry** (Max OAuth token expired; API returns 401).
- Sequence diagram §5.1, line `CC->>C25: ToolDenied event (E-C28-03)` — uses E-C28-03 for a
  PreToolUse hook-deny event. This is NOT an auth error.
- AC-C28-04: "…C25 records a ToolDenied event | **E-C28-03** hook-deny path" — again misattributes
  E-C28-03 as the hook-deny code.
- AC-C28-09 correctly references E-C28-03 for auth-expiry: "Claude Code emits an auth-error OTLP
  event" — this is the correct usage.

**Impact:** The ToolDenied failure path (PreToolUse hook exit non-zero) has no dedicated E-code.
E-C28-03 is overloaded with two different conditions. The sequence diagram and AC-C28-04 would mislead
an implementer into thinking hook-deny and auth-expiry are the same event class. D-30's prevent-gate
surface specifically depends on the hook-deny path being correctly surfaced.

**Fix (applied):** Added E-C28-09 "Hook-deny: PreToolUse hook exit(non-zero)" to E-code table §6.1;
updated the sequence diagram §5.1 and AC-C28-04 to reference E-C28-09 for the ToolDenied path.

---

### RCM-SEAM-03 — MAJOR  
**Seam:** C28↔C02 — hook/MCP registration shapes: C28 §3.4 correctly references C02 §3.3 but the
`[needs-G11]` tag per D-34 is inconsistently applied

**Evidence:**
- D-34 (ADOPTED, 2026-06-01): "Tool-node command-key field name is a source contradiction, G11-gated.
  Specs MUST carry the spelling note and MUST NOT claim either spelling as verified."
- C02 §3.3 hook registration: `[[hook]] command = "bin/override-gate"` — correctly marked `[inferred —
  needs G11]`.
- C28 §3.4: The example `pack.toml` fragment uses `[[hook]] command = …` with the inline comment
  `# Hook registrations — [inferred field shape, needs G11]` — this is correct.
- However, C28 §3.4 closure note says: "No conflict identified at Sweep-2; the C02 contract as specced
  is sufficient for C28's hook/MCP surface." This is correct *today* but does not explicitly name D-34
  as the authority requiring both specs to carry the spelling uncertainty.
- C28 §3.4 does not cite D-34 by name. The runbook §6.3 mentions the seam conflict risk but also does
  not cite D-34.

**Impact:** Minor — the `[needs G11]` tags are present. The missing D-34 citation is a traceability
gap, not a behavioral error. A builder following D-34's mandate would look for its citation and not
find it in C28/the runbook.

**Fix (applied):** Added D-34 citation to C28 §3.4 closure note and to runbook §6.3.

---

### RCM-SEAM-04 — MAJOR  
**Seam:** C29↔C28 — C29 §5.2 sequence diagram shows `crossFamilyRule` called for ALL routing
decisions, but C29 §5.1 step 4 and worked example §5.3 Case A show it is only called for
`role=judge`; the diagram is inconsistent

**Evidence:**
- C29 §5.1 step 4: "If `role=judge`: … `crossFamilyRule` is called…" — judge-conditional.
- C29 §5.3 Case A (coder): "`crossFamilyRule` not called (role != judge)" — explicit exclusion.
- C29 §5.2 sequence diagram: Shows `C29->>C29: crossFamilyRule(coder_model, independence_level=L1)`
  after the `alt role == "coder"` branch, as if it is *always* called regardless of role.
  The diagram's placement suggests it fires on every resolution.

**Impact:** A builder reading the sequence diagram alone would implement `crossFamilyRule` as always
invoked. The prose (§5.1) and worked example (§5.3 Case A) are correct; the diagram is wrong. In
Phase-0 this is a correctness bug for any coder-node routing implementation.

**Fix (applied):** Added `alt role == "judge"` guard around the `crossFamilyRule` call in C29 §5.2
sequence diagram; added a note that for `role != "judge"` the constraint is not emitted.

---

### RCM-SEAM-05 — MINOR  
**Seam:** C28 — D-30 verbatim citation is paraphrased, not fully verbatim per SWEEP2-DISPATCH

**Evidence:**
- SWEEP2-DISPATCH: "quote the **verbatim** decision text from review-log.md … not a paraphrase."
- review-log.md D-30 (full verbatim):  
  "unattended operation (P2) and self-modification (P3b) require the substrate to BLOCK (prevent at
  the tool-call/process boundary) — not merely detect — out-of-boundary access on the relevant
  blast-radius face."
- C28 §2 binding decisions block cites D-30 with this same text — this IS verbatim.
- C28 §6.2 re-uses the term "D-30 prevent-gate" without re-quoting; this is a reference, not a
  re-citation, and is acceptable.

**Assessment:** C28's D-30 citation at the top binding-decisions block IS verbatim. The §6.2 usage is
a shorthand reference, not a claim to be a verbatim cite. No fix required; the verbatim requirement is
met.

**Status:** No action.

---

### RCM-SEAM-06 — MINOR  
**Seam:** C29 — D-1 citation is close but the full impact sentence is truncated vs review-log verbatim

**Evidence:**
- review-log.md D-1 verbatim (relevant portion):  
  "implement the judge with the SAME provider/family as the coder for now; a different-provider judge
  moves to the future-enhancements bucket. Impact: C29 cross-family rule becomes advisory/relaxed;
  C32/C34 build against same-provider judging with holdout-integrity provided by rig partitioning +
  prompt/role isolation rather than family diversity."
- C29 §6.2 blockquote for D-1:  
  "implement the judge with the SAME provider/family as the coder for now; a different-provider judge
  moves to the future-enhancements bucket. Impact: C29 cross-family rule becomes advisory/relaxed;
  C32/C34 build against same-provider judging with holdout-integrity provided by rig partitioning +
  prompt/role isolation rather than family diversity."

**Assessment:** This IS verbatim. The full impact sentence is present.

**Status:** No action — D-1 citation verified correct.

---

### RCM-SEAM-07 — MINOR  
**Seam:** C29 — D-10 citation is verbatim and complete

**Evidence:**
- review-log.md D-10:  
  "`modeldb` fields = {id, family, cost_tier}. Per the SURVIVOR-PASS apply outcome (binding). No
  separate `independence_class` field; judge independence is expressed by the L0–L3 policy (L1
  same-family default, D-1), not a registry field."
- C29 §4.2 blockquote: identical text.

**Assessment:** D-10 is quoted verbatim. The `{id, family, cost_tier}` field set and the
no-`independence_class` ruling are both present.

**Status:** No action — D-10 citation verified correct.

---

### RCM-SEAM-08 — MINOR  
**Seam:** C29 — C34:OQ-C34-4 forward seam needs clearer ownership signal for future C34 builder

**Evidence:**
- C29 §9 final bullet: "[C34:OQ-C34-4 — open, inherited] When FE-1 lands, does the family-difference
  check move into C34 (holdout enforcement) or stay advisory in C29? Today relaxed per D-1. The
  `cross_family_enforce` boolean in `[judge_policy]` is the clean FE-1 seam; the enforcement *owner*
  at FE-1 is a cross-component question (C29 emits the constraint; C34 enforces it — the split is
  already implied by D-13, but the FE-1 wiring is deferred)."
- The seam IS named and flagged as inherited. The `cross_family_enforce` bool is clearly identified
  as the switch. However, the note does not explicitly tell the C34 builder *what to look for* in
  C29's output contract when FE-1 arrives.

**Fix (applied):** Added a clarifying sentence to C29 §9 C34:OQ-C34-4 bullet: "For the C34 builder
at FE-1: the signal is `IndependenceConstraint.cross_family_required == true`; when that is true and
`judge.family == coder.family`, C34 (or its enforcement layer) must reject the dispatch — C29 emits
the constraint, enforcement ownership is the unresolved FE-1 question. DEFERRED — orchestrator
ledger."

---

### RCM-SEAM-09 — MINOR  
**Seam:** E↔AC integrity check — C29 E-C29-06 has no dedicated AC

**Evidence:**
- C29 §8.2 E↔AC cross-reference table: E-C29-06 (invalid-judge-policy) is noted as "verified
  implicitly by AC-C29-08" with a `[FAITHFUL-FILL]` deferral note.
- SWEEP2-DISPATCH depth bar: "Each AC that exercises a failure path **cross-references the E-code** it
  asserts." AC-C29-08 tests a *missing* `[model_floor]` section (E-C29-05), not a malformed
  `independence_level` (E-C29-06). The implicit coverage claim is weak.

**Assessment:** The deferral note ("dedicated AC is a sweep-3 item") is honest. The gap is flagged.
Since SWEEP2-DISPATCH says "Depth is for surface the component actually has. Don't invent surface to
fill a table," and C29 correctly flags this as sweep-3, this is a tracked known gap, not an error to
fix here.

**Status:** Noted; C29's existing [FAITHFUL-FILL] note is sufficient for sweep-2.

---

### RCM-SEAM-10 — MINOR  
**Seam:** Mermaid diagram validity — C28 §5.2 state diagram label with `exit(non-zero)` contains
parentheses in a transition label

**Evidence:**
- SWEEP2-DISPATCH Mermaid syntax warning: "in `stateDiagram-v2`, a `;` inside a transition label
  terminates the statement and breaks the parse. Do NOT put `;` `/` `--` `:` `()` `=` `#` inside
  transition labels."
- C28 §5.2 state diagram:  
  `HookGate --> Reasoning : PreToolUse exit(non-zero) — tool denied`  
  Contains `()` (parentheses) and `—` (em dash) in a transition label.

**Assessment:** The parentheses `()` and the em dash `—` could break Mermaid's `stateDiagram-v2`
parser. Per the dispatch warning, `()` is explicitly listed as breaking. However, since the validator
tool is not available in this run environment, we apply the conservative fix: reword to avoid `()`.

**Fix (applied):** Changed transition label in C28 §5.2:  
`HookGate --> Reasoning : PreToolUse exit(non-zero) — tool denied`  
→ `HookGate --> Reasoning : PreToolUse non-zero exit, tool denied`

---

## Summary Table

| ID | Severity | Component | Fixed? |
|---|---|---|---|
| RCM-SEAM-01 | BLOCKER | C28↔C04, runbook | Applied (seam note + [OPEN SEAM: needs-G11] added) |
| RCM-SEAM-02 | MAJOR | C28 | Applied (E-C28-09 added; diagram + AC updated) |
| RCM-SEAM-03 | MAJOR | C28, runbook | Applied (D-34 citation added) |
| RCM-SEAM-04 | MAJOR | C29 | Applied (sequence diagram guard corrected) |
| RCM-SEAM-05 | MINOR | C28 | No action (D-30 verbatim is correct) |
| RCM-SEAM-06 | MINOR | C29 | No action (D-1 verbatim is correct) |
| RCM-SEAM-07 | MINOR | C29 | No action (D-10 verbatim is correct) |
| RCM-SEAM-08 | MINOR | C29 | Applied (C34 builder signal named) |
| RCM-SEAM-09 | MINOR | C29 | No action (sweep-3 deferral is correct) |
| RCM-SEAM-10 | MINOR | C28 | Applied (Mermaid label reworded) |

**Deferred to orchestrator ledger:**
- C28↔C04 env-forwarding seam (RCM-SEAM-01): the question of whether `gc`'s `internal/execenv`
  strips TOKEN/OAUTH-bearing vars and whether the tmux Provider forwards container env to panes is
  OPEN pending G11 spike. Both specs now explicitly name the two readings and the operational risk.
  Cannot be resolved without a pinned-`gc` run.
- C34:OQ-C34-4 / FE-1 enforcement ownership (RCM-SEAM-08): C29 names the seam; resolution is
  cross-component and requires C34 builder + FE-1 wiring decision. DEFERRED — orchestrator ledger.

---

## Verdict

**accept-with-fixes**

C28 and C29 are internally well-structured, with correct Sweep-2 depth (signatures, schemas, diagrams,
E-codes, ACs, verbatim D-citations). The three MAJOR findings (E-code mislabeling, sequence diagram
guard error, D-34 citation gap) are corrected in-place. The BLOCKER env-forwarding seam
(RCM-SEAM-01) is now explicit in both C28 §3.3 and C04 §8 (with both readings, the operational risk,
and a `[OPEN SEAM: needs-G11]` marker), satisfying the dispatch requirement that this be "an explicit,
clearly-marked `needs-G11` seam in BOTH C28 and C04." The seam cannot be *resolved* (only a pinned-`gc`
run can do that), but it is no longer a latent contradiction — it is a documented open question.

The C34:OQ-C34-4 forward seam in C29 is clean for the future C34 builder: the `cross_family_enforce`
bool and the `IndependenceConstraint.cross_family_required` signal are the named triggers; enforcement
ownership at FE-1 is deferred without false resolution.
