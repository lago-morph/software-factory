# Spec: `subagent-deliverable-contract`

## Intent

Subagent change reports drive everything downstream: PLAN.md surprise transcription, PR body composition, retrospective surprise-extraction, cross-corpus propagation flags. When a subagent's change report is too short, the orchestrator has nothing to transcribe and must re-read every touched file. When it's too long, it defeats the context-preservation reason the subagent was dispatched in the first place. This skill codifies the contract — what a subagent change report must contain, in what shape, at what length — and produces a brief snippet the orchestrator can paste into every cluster brief.

Grounded in PR #67: 13 cluster subagents, change reports ranged from ~200 to ~1000 words; the longer ones (Cluster F, J, N, O) drove the most useful PLAN updates; the shorter ones (Cluster E) required orchestrator re-reads to find the surprises.

## Trigger

Direct:
- "Write me a brief that asks the subagent for a change report"
- "What should the subagent's change report contain?"

Proactive:
- Composing a brief for a subagent that will edit ≥2 files.
- The session involves multiple sequential subagents whose outputs need transcription into a tracking document.

Negative:
- One-shot lookup subagents (Explore-style) — the *result* is the deliverable; no separate change report.

## Inputs

- The subagent's planned scope: which files it will touch + what it will produce.
- The orchestrator's downstream consumers (PLAN.md? PR body? retrospective?).

## Outputs

- A boilerplate brief snippet to paste into every multi-file-edit subagent dispatch.
- (If the user opts) An AGENTS.md rule documenting the contract project-wide.

## Workflow

1. **Decide the change-report length window.** Default 300–600 words. Adjust based on scope: small (1-2 files, <50 lines changed) → 200–400; large (5+ files, >300 lines or new report) → 500–800.
2. **Specify the required sections.** Use this canonical six-section structure:
   - **Files modified** (one bullet per absolute path, line-delta if applicable).
   - **New artifacts** (any new files / figures / directories).
   - **Section structure** (per new doc / per major edit: which sections, what each contains).
   - **Cross-references added** (which other files were touched to point at the new work).
   - **Refutations / refinements** (any prior corpus claim corrected — *load-bearing*).
   - **Surprises** (3–8 non-obvious findings the orchestrator could not predict from the brief).
3. **Specify "DO NOT" boundaries**: don't touch PLAN.md, don't touch unrelated files, don't commit, don't delete sources. These vary per session but should be explicit in every brief.
4. **Require concrete numbers**: line-counts, word-counts, file-sizes for figures, specific quotes verbatim where available. Numbers anchor the audit trail.
5. **Require provenance markers**: every new sources-table row must include where the source was drained from and on what date.
6. **Paste the brief snippet at the END of the per-cluster brief**, after the actual task instructions, under a heading like "## Deliverable".

## Concrete examples

### Example 1: A well-shaped change report (drawn from PR #67 Cluster J)

```
## Cluster J drain — change report

### New reports created

**`research/30-cognitive-escrow.md`** (3,677 words; target 3,500–4,500 ✅)

Section structure:
- §1 The phenomenological state — Kahana's definition; latency/wait-time ruled inadequate; ...
- §2 The Human-Centered principle's three current questions — and the missing fourth
- §3 STIR as structural trigger — corpus' adjacent review disciplines ...
- §4 Latency-minimisation is the wrong reflex — interval-as-design-site ...
- §5 Cross-corpus impact — F42 proposal + cross-references into reports 09/28/25/26/05, followup/10
- §6 Sources table (1 row)

**`research/31-caremark-rsi-board-exposure.md`** (4,493 words; target 4,000–5,000 ✅)

Section structure: §1 RSI three-part test + corpus-novel mid-market-scope framing ...
... [continues]

### Cross-references added
- **Report 18** (Codex substrate) §4.4 — new "Cross-reference — AILCCP controls vocabulary" paragraph ...
- **Report 02** (StrongDM Attractor) §5 — new "Cross-reference — Caremark-line board-exposure framing" paragraph ...

### Failure-mode proposals
- **F42 — Cognitive-Escrow Negligence**: ...
- **F43 — RSI Board-Visibility Gap**: ...

### Surprises / findings
1. **Mid-market RSI scope-claim** is the most corpus-disruptive single sentence in the cluster: ...
2. **Trustworthy is compositional, not standalone** (AILCCP primary): the followup/10 §1.1 prior reading treats Trustworthy as substantive. ...
3. **Eight of 37 AILCCP principles have no mapped standard** — corpus-novel coverage-gap metric ...
... [8 items total]
```

This is reusable verbatim by orchestrator into PLAN.md and PR body.

### Example 2: A poorly-shaped change report and the fix

Poor: *"Updated report 18 with the .rules DSL and the operational posture section. Also did some cross-reference work. Let me know if you want anything else."*

Fix:
1. Reject silently — orchestrator must Re-read the diff.
2. In the next subagent brief, include the explicit six-section requirement and a worked example like the one above.
3. Add a sentence: *"Reports under 300 words will be rejected and re-issued."*

## Anti-patterns

- **Open-ended "tell me what you did."** Always specify sections.
- **No length window.** Subagents will under-deliver (saving turns) or over-deliver (padding) without guidance.
- **No surprises section.** Surprises are the highest-value output. Without an explicit slot they get lost.
- **No refutations section.** Refutations of prior corpus claims are load-bearing and easy for the subagent to leave out unless asked.
- **Asking for the change report inline in the body of the brief.** Always at the end, under a clearly-named heading, in a list format so the subagent has a template to fill.
- **Accepting "I also updated PLAN.md."** The orchestrator owns PLAN.md exclusively. The brief must explicitly forbid subagent writes to PLAN.md.

## Acceptance criteria

1. Every subagent dispatched returns a change report in the canonical six-section format.
2. Word counts land within the specified window for ≥90% of dispatches.
3. The orchestrator can transcribe surprises directly into a PLAN.md update without re-reading the subagent's diff.
4. Refutations are surfaced *as refutations*, not buried in prose.
5. Every new sources-table row has provenance.

## Files this skill creates / modifies

- `AGENTS.md` (or equivalent) — a rule documenting the six-section contract.
- Per-session: every subagent brief gets a "## Deliverable" section using the contract.
- Optionally a checked-in template at `.claude/templates/subagent-change-report.md`.
