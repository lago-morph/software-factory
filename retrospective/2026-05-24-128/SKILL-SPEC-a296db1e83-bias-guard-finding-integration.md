# Spec: `bias-guard-finding-integration`

- **ID**: SKILL-SPEC-a296db1e83
- **Source retrospective**: ../2026-05-24-128.md

## Intent

When promoting a bias-guard finding (CANDIDATE/MISSED/WEAK) into a primary artifact (catalog entry, register, decision record), neutralize architectural-commitment language in the entry, replace any illustrative example that names a real artifact with a fictitious placeholder, and quarantine the bias-guard ID from downstream citation. A dedicated sanitization-audit subagent pass verifies the result before commit. This skill exists because in the v3 work, the integration of one bias-guard CANDIDATE into a primary failure-mode entry used wording that named a specific architectural pattern as "the factory's mechanism" — that wording propagated through 9 downstream subagents and caused two of three independent unified-mandate tracks to converge on the same architectural pattern. The contamination required a full Phase-2 re-dispatch from cleaned source files. The skill captures the minimum discipline that would have prevented that.

## Trigger

**Direct user phrases:**
- "Promote this CANDIDATE to F-mode"
- "Integrate this bias-guard finding into the catalog / register"
- "Add this WEAK sharpening to the contradictions register"
- Any phrase pattern of "add the bias-guard / audit output to [primary artifact]"

**Proactive triggers (offer the skill without being asked):**
- A bias-guard subagent has just returned findings that propose new entries for a catalog, register, or inventory.
- The lead agent is about to write a PR that includes "promote / integrate / absorb / merge" in the commit message and the change touches a primary artifact.

**Negative triggers (skill does NOT apply):**
- Integrating bias-guard findings into other bias-guard reports or session retrospectives (the audience is the user / human reviewer, not downstream agents).
- Quoting a bias-guard finding inline in a comment or chat reply.

## Inputs

- The bias-guard finding to integrate (file path or inline text).
- The target primary artifact path (e.g., `architectures/v3/failure-modes-v3.md`).
- The proposed insertion location in the target artifact (section or sibling entry).

## Outputs

- An updated target artifact with the integration applied.
- A short audit report (returned in chat) summarizing what the audit subagent flagged and how it was resolved.
- One git commit per integration batch (multiple findings in one pass can share a commit).

## Workflow

1. Draft the integration in the target artifact's format. Use the existing entries as the template (e.g., for F-modes: ID + Definition + Source + Mechanism + Severity + Severity-rationale).
2. For each field that quotes or paraphrases the bias-guard finding, apply the **neutralization self-check**: would this field still convey the underlying phenomenon if all architectural-commitment language were stripped? If no, rewrite.
3. For any illustrative example in the entry, **replace real artifact references with fictitious placeholders**: real file paths → `widgets/example-catalog.md`; real numeric IDs → `EXAMPLE-FINDING-7`; real pattern names → `pattern-Q` / `pattern-R`.
4. **Quarantine the bias-guard ID**: the primary artifact entry must not contain a citation of the bias-guard finding's ID (`MISSED-N`, `WEAK-N`, `CANDIDATE-N`). If the substance of the finding needs to be cited, cite the underlying corpus source (the report, the section, the primary quote) that the finding itself was derived from.
5. **Dispatch the sanitization-audit subagent** (sonnet-class is sufficient) with the brief: "Read [target file] section [name]. Flag every reference to a real file path, real numbered ID, real bias-guard finding ID, or real project-specific term. For each, quote the surrounding sentence and propose a fictitious replacement. Report only; do not fix." See "Concrete examples" below for the audit brief template.
6. Apply the audit's proposed replacements. If extensive replacements were needed, re-dispatch the audit on the corrected version.
7. Commit. The commit message describes what was integrated, that the sanitization audit ran, and the audit's finding count.

## Concrete examples

### Example 1: Promoting a CANDIDATE to a new F-mode

Input: bias-guard report's CANDIDATE-6 entry, describing "operators gradually relax their human-review threshold as automation succeeds."

Step 1 draft (lead-agent first pass):

```
### F57 — Design-authority erosion

- **Definition:** "Convenience steadily reclassifies higher-stakes
  decisions as lower-stakes, hollowing out human-judgment layers."
- **Mechanism:** The factory classifies work units into
  automation-eligible vs human-required by stakes / risk tier. Over
  time, convenience pressure reclassifies higher-stakes decisions
  downward without explicit policy change.
```

Step 2 neutralization self-check: strip the architectural-commitment language. The mechanism says "by stakes / risk tier" — that names tier-classification as the factory's mechanism. Remove.

Step 3 fictitious-placeholder pass: no examples in this entry (the entry itself names a real F-mode number, which is correct).

Step 4 ID quarantine: the entry does not cite CANDIDATE-6. The underlying source is the governance-literature report; that's what the Source field cites.

Step 5 audit subagent brief:

```
Read /path/to/failure-modes-v3.md section "F57 — Design-authority
erosion". Flag every reference to a real file path, real F-mode ID, real
contradiction-register ID (CTR-*), real bias-guard finding ID, or real
architectural-pattern term (tier-classification, pace-layers,
verification-topology, trust-topology, regime, etc.). For each, quote
the surrounding sentence and propose a fictitious replacement. Report
only; do not fix. Zero findings is a valid result.
```

Step 5 audit returns: "Mechanism field still says 'by stakes / risk tier' — this is the contamination pattern. Proposed replacement: 'whichever organizing principle the architecture chose.'"

Step 6 apply: rewrite mechanism to neutral form.

Step 7 commit: "phase-1: promote CANDIDATE-6 to F57 with neutralized mechanism. Sanitization audit ran (1 finding, fixed)."

### Example 2: Absorbing a WEAK sharpening into a contradictions-register entry

Input: bias-guard auditor's WEAK-5 sharpening on CTR-D4, naming a specific architectural pattern as a "third F1-mitigation position."

Step 1 draft (lead-agent first pass):

```
**Phase-1 bias-guard sharpening (WEAK-5):** Anthropic same-model-
different-role is a third F1-mitigation position alongside RouterLLM
and kevin/carl topology. (Anchor-detector flagged this as the most
contamination-suspect framing.)
```

Step 2 neutralization self-check: the sharpening names three specific architectural patterns as a "trichotomy." If the goal is to surface the auditor's framing, naming the patterns is OK; if the goal is to teach the next agent how to mitigate F1, the trichotomy is itself a framing-bias risk.

Step 3 ID quarantine: the entry calls out "WEAK-5" by ID. Downstream subagents reading this register entry may cite "WEAK-5" as if it were a corpus reference. Quarantine: remove the `WEAK-5` ID from the entry; add a header note to the register file explaining that sharpening paragraphs are critic framings, not corpus.

Step 4 audit: dispatch the same brief.

Step 5 audit returns: "The entry calls out WEAK-5 by ID; downstream subagents will cite this as a corpus reference. Recommendation: the register's top-of-file note already explains the quarantine rule; the individual entry should not name the ID."

Step 6 apply: remove `(WEAK-5)` from the entry; rely on the top-of-file note.

Step 7 commit: "phase-1: absorb WEAK-5 sharpening into CTR-D4 with ID quarantined. Sanitization audit ran (1 finding, fixed)."

## Anti-patterns

- **Single-author integration with no audit.** This is what produced the F57 contamination. The lead agent under load does not reliably notice when their illustrative example names a real architectural pattern.
- **Sanitizing only the most-obvious cases.** "F57's mechanism field" was the only field anyone noticed during the original Phase-1 work; WEAK-5's ID-citation pattern was discovered later by the Phase-2 anchor-detector. The audit subagent's brief must scan for the *full class* of patterns, not just the case in front of the lead agent.
- **Using the audit as a substitute for the neutralization self-check.** Steps 2-4 are still the lead-agent's responsibility; the audit catches what the lead agent missed, not what the lead agent skipped.
- **Citing the audit's findings to the user without applying them.** The audit returns findings; the lead agent applies fixes. Reporting findings to the user before applying them invites the user to triage the audit, which is the lead agent's job.

## Acceptance criteria

- [ ] After integration, the target artifact's affected fields pass the neutralization self-check (lead-agent verifies).
- [ ] After integration, the target artifact contains no real-artifact references in illustrative examples (audit subagent verifies).
- [ ] After integration, the target artifact does not contain `MISSED-N`, `WEAK-N`, or `CANDIDATE-N` IDs as citations.
- [ ] The audit subagent's findings (count + brief summary) appear in the commit message.
- [ ] The commit lands without a follow-up "but the integration is contaminated" PR comment within 24 hours.

## Files this skill creates / modifies

- The target primary artifact (one of: `architectures/v3/failure-modes-v3.md`, `architectures/v3/contradictions.md`, `architectures/v3/corpus-inventory.md`, or the project equivalent) — modifies.
- No new files. The audit subagent's report is returned in chat and summarized in the commit message; no on-disk artifact is created for the audit itself.
