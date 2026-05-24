# Temporary working doc: Phase-2 plan update — execution checklist

**This is a transient file.** It captures the agreed plan from the PR #128 dialog so the executing agent (likely me, possibly with a compacted context) can follow it without re-deriving from conversation. **Delete or archive this file when all commits below have landed.**

**Authorization status (as of this writing):** User has authorized writing this plan to disk and committing it to PR #128. User has NOT yet authorized executing the commits below. After this file lands, wait for explicit go-ahead before commit 1.

---

## Decisions already locked (do not re-litigate)

1. **All contaminated and contamination-bearing artifacts get the "delete + permalink + guard" treatment.** No sanitize-in-place attempt for any of them.
   - 9 contaminated tracks (the original Phase-2 dispatch)
   - `architectures/v3/bias-guards/phase-2/axis-divergence-audit.md`
   - `architectures/v3/bias-guards/phase-2/anchor-detector.md`
   - `architectures/v3/bias-guards/phase-2/splitter.md`
   - `architectures/v3/bias-guards/phase-2/lumper.md`
   - `architectures/v3/tracks/unified-A-prime.md`
   - `architectures/v3/tracks/unified-C-prime.md`
   - `architectures/v3/tracks/unified-D-off-list.md`

2. **A single reference doc** (`architectures/v3/history/HISTORICAL-RECORD.md`) holds permalinks to all of the above. The doc carries a **guard warning at the top** explicitly telling agents not to read these files into context.

3. **D5/D6/D7 stay**, but with a **discrete sanitization step**. All examples in their text must use obviously-fictitious file/path/ID names (no `F57`, no `WEAK-5`, no `failure-modes-v3.md`, etc.).

4. **No retrospective commit.** The user invokes retrospective manually later. Handoff-confusion learnings stay in the session record.

5. **Stop-and-ask checkpoints restored** at major decision points only (before §3.6 dispatch; after subagents return / before §3.7 bias-guard re-run; before §3.8 PR open). Not at every step.

---

## Commit 1 — History dir + relocate contaminated artifacts

### Pre-commit checks

- Verify all 16 files listed in Decision 1 exist in the live tree at the commit base.
- Verify `architectures/v3/history/` does not already exist.

### File changes

1. **Create** `architectures/v3/history/HISTORICAL-RECORD.md` with the exact content below (under "Guard warning + permalink doc content").

2. **Delete** (via `git rm`) all 16 contaminated files from the live tree. Their content remains accessible via git history at the permalinks listed in HISTORICAL-RECORD.md.

### Guard warning + permalink doc content (exact text for `HISTORICAL-RECORD.md`)

```markdown
# Historical record — Phase-2 contaminated artifacts

## ⚠ STOP — Do not read these files into your context window

The artifacts listed below were produced during a Phase-2 dispatch that was
later identified as contaminated by lead-agent integration bias. They have
been removed from the active tree because reading them risks re-introducing
the bias they document into the current work.

This doc exists for one reason: to preserve permalinks so the artifacts
remain *retrievable* by a human reviewer or by an explicit user request.
Agents should NOT open the permalinks below or fetch the file contents
unless the user explicitly directs them to. Do not summarize the files.
Do not pass their contents to subagents. Do not include them in dispatch
briefs.

If you find yourself curious about what these files contain, that is the
exact failure mode this doc exists to prevent. Move on.

## Permalinks

Each entry: the file's original path, what it was, and a `git show` command
to retrieve it from history if absolutely needed. The commit hash is the
last commit at which the file existed in its original location.

### Contaminated Phase-2 tracks (9 files)

Original dispatch commit: `5c4deeb`. Last commit at original path: the
commit immediately before commit 1 of this plan (resolve at execute time
and update this doc before committing).

- `architectures/v3/tracks/greenfield-substrate-first.md` — Track 1 of the
  original Phase-2 9-track fanout. Greenfield mandate, substrate-first axis.
- `architectures/v3/tracks/greenfield-methodology-first.md` — Track 2.
  Greenfield, methodology-first.
- `architectures/v3/tracks/greenfield-cold-start-first.md` — Track 3.
  Greenfield, cold-start-first.
- `architectures/v3/tracks/brownfield-substrate-first.md` — Track 4.
  Brownfield, substrate-first.
- `architectures/v3/tracks/brownfield-methodology-first.md` — Track 5.
  Brownfield, methodology-first.
- `architectures/v3/tracks/brownfield-legacy-ingestion-first.md` — Track 6.
  Brownfield, legacy-ingestion-first.
- `architectures/v3/tracks/unified-A.md` — Track 7. Unified, picked a
  tier-based axis (contamination evidence).
- `architectures/v3/tracks/unified-B.md` — Track 8. Unified, picked
  Brier pace-layers.
- `architectures/v3/tracks/unified-C.md` — Track 9. Unified, picked a
  tier-based axis (contamination evidence).

### Phase-2 contamination-diagnosis audits (4 files)

- `architectures/v3/bias-guards/phase-2/axis-divergence-audit.md` —
  Diagnosed the F57 / tier-axis contamination. Quotes the contaminated
  wording verbatim; reading risks re-introducing the bias.
- `architectures/v3/bias-guards/phase-2/anchor-detector.md` — Classified
  the 11 cross-track convergences as honest / mixed / contaminated. Names
  specific framings; reading risks anchoring.
- `architectures/v3/bias-guards/phase-2/splitter.md` — Adversarial
  splitter argument over the (contaminated) outputs. Specific to the
  contaminated set; not relevant to the re-run.
- `architectures/v3/bias-guards/phase-2/lumper.md` — Adversarial lumper
  argument over the (contaminated) outputs. Same.

### Phase-2 follow-up diagnostic tracks (3 files)

- `architectures/v3/tracks/unified-A-prime.md` — Re-dispatch of unified-A
  with tier-axis prohibited. Found a defensible non-tier axis
  (verification-topology). Reading pre-biases new unified subagents
  toward that specific answer.
- `architectures/v3/tracks/unified-C-prime.md` — Re-dispatch of unified-C
  with tier-axis prohibited. Same risk.
- `architectures/v3/tracks/unified-D-off-list.md` — Off-list supplementary
  unified track. Proposed trust-topology axis. Same risk.

### Retrieval (only if user explicitly requests)

```
git show <commit>:<path>
```

Resolve `<commit>` from the commit immediately before this commit lands.
```

### Commit message draft

```
phase-2 cleanup: relocate contaminated artifacts behind permalink-only history

Per the agreed plan in tmp-updates.md, all contamination-bearing Phase-2
artifacts are removed from the active tree. They remain accessible in
git history via permalinks listed in architectures/v3/history/
HISTORICAL-RECORD.md, which carries a guard warning telling agents not
to read them.

Removed (16 files):
  - 9 contaminated Phase-2 tracks
  - 4 Phase-2 bias-guard audits (axis-divergence, anchor-detector,
    splitter, lumper)
  - 3 follow-up diagnostic tracks (unified-A-prime, -C-prime, -D-off-list)

The next session executes Phase 2 against the clean source files and
produces a fresh 9-track dispatch. The historical artifacts are
preserved for human archaeology but explicitly fenced off from agent
context.
```

### Post-commit verification

- `architectures/v3/tracks/` is empty.
- `architectures/v3/bias-guards/phase-2/` is empty (or contains only `contaminated-tracks-index.md` if it exists from an earlier commit — check).
- `architectures/v3/history/HISTORICAL-RECORD.md` exists with the guard at top.
- Push lands; PR #128 reflects the deletion.

---

## Commit 2 — Clean source files + sanitized D5/D6/D7

### Pre-commit checks

- Verify `architectures/v3/failure-modes-v3.md` F57 mechanism field still contains the contaminated wording (`"the factory classifies work units into automation-eligible vs human-required by stakes / risk tier"`).
- Verify `architectures/v3/contradictions.md` does not yet carry a bias-guard-sharpening citation discipline note.
- Verify `architectures/v3/decisions-captured.md` ends at D4.

### File changes

1. **`architectures/v3/failure-modes-v3.md` F57**: rewrite the Mechanism field to the neutral version. Use exact text:

   ```
   **Mechanism:** The factory has some mechanism for distinguishing
   automation-eligible work from human-required work — whichever
   organizing principle the architecture chose. Over time, convenience
   pressure (latency, cost, headcount) shifts that distinction's
   threshold without explicit policy change. The eligibility *system*
   drifts; the *audited eligibility decision* at any given moment
   looks consistent. Distinct from F7 (normalisation of deviance) —
   F7 is the *acceptance threshold* drifting; this is the
   *eligibility-classification mechanism itself* drifting. Distinct
   from F24 (trust creep) — F24 is gates being loosened; this is
   work-units crossing the gate boundary.
   ```

   Do NOT include a "bias-guard note" subsection in F57. The clean
   mechanism stands on its own; calling out the prior contamination
   inside F57 re-introduces the framing.

2. **`architectures/v3/contradictions.md`**: add a header note immediately after the existing "Provenance discipline" paragraph. Use exact text:

   ```
   **Bias-guard-sharpening citation discipline.** Each CTR entry's
   "Phase-1 bias-guard sharpening" paragraphs (WEAK-1 through WEAK-5)
   were authored by an auditor and are critic framings, not corpus
   references. Cite the underlying corpus material (the reports,
   followups, sections referenced *inside* the sharpening), not the
   `WEAK-N` ID itself.
   ```

   Do NOT single out WEAK-5 by name in this note — that re-introduces
   the framing the original contamination relied on.

3. **`architectures/v3/decisions-captured.md`**: append D5, D6, D7. **Sanitization is a discrete sub-step — see below.**

### D5/D6/D7 sanitization protocol (sub-steps inside commit 2)

**Sub-step 2a — Draft using fictitious examples only.** Write D5/D6/D7 with placeholder file/path/ID names. Use the following fictitious vocabulary:

- Failure-mode IDs: `F-EXAMPLE-1`, `F-EXAMPLE-2` (NOT `F57`)
- File paths: `widgets/example-catalog.md`, `widgets/example-register.md` (NOT `failure-modes-v3.md`, `contradictions.md`)
- Bias-guard finding IDs: `EXAMPLE-FINDING-N` (NOT `MISSED-3`, `WEAK-5`, `CANDIDATE-6`)
- Architectural patterns referenced as examples: `pattern-Q`, `pattern-R` (NOT `tier-classification`, `pace-layers`)

The text should describe the *rule shape* without ever referencing the specific real-repo artifacts that prompted the rule.

**Sub-step 2b — Sanitization audit.** After drafting, dispatch a single subagent (general-purpose, sonnet model — this is a small audit, opus is overkill) with the brief:

> Read `/home/user/software-factory/architectures/v3/decisions-captured.md` sections D5, D6, and D7. Flag every reference to a real file path in this repository, real failure-mode ID (`F<N>` format), real contradiction-register ID (`CTR-<N>` format), real bias-guard finding ID (`MISSED-N` / `WEAK-N` / `CANDIDATE-N`), or real architectural-pattern term (`tier-classification`, `pace-layers`, `verification-topology`, `trust-topology`, `invariant-body-split`). For each, quote the surrounding sentence and propose a fictitious replacement. Do not fix the file; report findings only. If zero findings, say so explicitly.

**Sub-step 2c — Apply fixes.** If the audit flagged items, apply the proposed fictitious replacements. Re-run the audit if uncertain.

**Sub-step 2d — Commit.**

### Commit message draft

```
phase-2 cleanup: neutralize F57 + add bias-guard citation discipline + D5/D6/D7

F57 mechanism field rewritten to remove the tier-classification
presupposition. The failure mode now describes the eligibility-mechanism-
drift phenomenon without smuggling in an architectural commitment.

contradictions.md gains a citation-discipline note: bias-guard
sharpenings (WEAK-1 through WEAK-5) are critic framings, not corpus
references. Cite the underlying corpus material instead.

decisions-captured.md adds D5/D6/D7 with examples sanitized to use
fictitious file/path/ID names (no real-repo references). The decisions
are durable safeguards:
  D5 — bias-guard integration discipline
  D6 — full re-run after contamination discovery
  D7 — off-list / blind-axis test as standing safeguard

Sanitization audit ran as a subagent pass before commit. <Update with
audit findings count.>
```

### Post-commit verification

- `git diff` shows F57 mechanism field changed; no other F-mode altered.
- `contradictions.md` has the new note; no CTR entries edited.
- `decisions-captured.md` ends at D7; grep confirms no real-repo file paths or real `F\d+` / `WEAK-\d+` / `MISSED-\d+` / `CANDIDATE-\d+` IDs in D5/D6/D7 text.

---

## Commit 3 — Restructure PHASE-2-RERUN-PLAN.md

### Pre-commit checks

- Commits 1 and 2 have landed.
- Verify the plan's §1 still contains the contamination-detail bullets (F57 / WEAK-5 / MISSED-3 explanations).
- Verify the plan's §2 still contains the "Important contamination references" list.

### File changes

1. **Remove the contamination-detail bullets from §1.** Replace with a single line: "See `architectures/v3/history/HISTORICAL-RECORD.md` for the contamination diagnosis (do not read those files into context)."

2. **Remove the "Important contamination references" list from §2.**

3. **Mark steps 3.1, 3.2, 3.3, 3.4, 3.5 as DONE** (since commits 1 + 2 executed them). The next session starts at 3.6. Use a "DONE — see commit `<hash>`" annotation at the top of each step.

4. **Embed the 9 subagent dispatch prompts in step 3.6.** Use the original briefs as the template (recoverable via `git log --all` for Agent calls; or re-derive from the brief + synthesis plan). For each of the 9 tracks, include the actual prompt text the next session will use, in a fenced markdown block, labeled by track.

5. **Restore stop-and-ask at major points only:**
   - **Step 3.6** (before dispatching 9 subagents): add a stop-and-ask checkpoint. "Surface the 9 dispatch prompts + dispatch plan; wait for go-ahead before invoking the Agent tool."
   - **Step 3.7** (after subagents return, before bias-guard re-run): add a checkpoint. "After all 9 tracks return and have been committed, surface the bias-guard plan; wait before dispatching the new bias guards."
   - **Step 3.8** (before opening Phase-2 PR): add a checkpoint. "Surface the proposed PR title and body; wait before opening."
   - No other steps get checkpoints.

6. **Delete §4 entirely** ("After Phase 2: where this work joins back to the main plan"). It's confusing for the next session.

7. **Replace §6 Appendix** with a single line: "Historical artifacts: `architectures/v3/history/HISTORICAL-RECORD.md`. Do not read those files into context." Renumber subsequent sections if any.

8. **Per-file references**: scan the plan; any reference to a contaminated file (F57, WEAK-5, MISSED-3, tracks/unified-A-prime, etc.) by name should either be removed or moved into the specific step that uses it. The new agent's startup reading (§0–§2) should not name any contaminated artifact.

### Commit message draft

```
phase-2 plan: restructure for clean handoff

Plan structure changes:
  - §1 contamination-detail bullets removed; one-line pointer to
    history/HISTORICAL-RECORD.md replaces them.
  - §2 "Important contamination references" list removed.
  - Steps 3.1-3.5 marked DONE (executed in commits 1 + 2).
  - Step 3.6 gains the actual subagent dispatch prompts inline, so
    the next session has them ready to invoke.
  - Stop-and-ask checkpoints restored only at major points (3.6, 3.7,
    3.8). Other steps execute under the §0 rule alone.
  - §4 "After Phase 2" removed (was confusing; the main synthesis
    plan covers Phase 3+).
  - §6 Appendix reduced to a single pointer at history doc.

Per-startup-reading scan: no contaminated artifact names remain in
§0-§2. The new agent opens to a clean view.
```

### Post-commit verification

- Read §0, §1, §2 of the plan end-to-end. Confirm: no real failure-mode IDs, no real bias-guard finding IDs, no contaminated-track filenames.
- Steps 3.1-3.5 visibly marked DONE.
- Step 3.6 contains 9 dispatch prompts in fenced blocks.
- §4 is gone; §6 is a one-liner; section numbering still coherent.

---

## After commit 3

The PR #128 branch contains the clean handoff. The next session can pick up at step 3.6 with the user's per-step approval.

`tmp-updates.md` (this file) gets cleaned up — either deleted in a follow-up commit, or rolled into the plan's step 3.9 cleanup.

---

## Operating rule for executing this plan

Follow this file. Stop and ask before each of the three commits. Do not execute any commit without the user's explicit go-ahead for that specific commit.

If at any point the conversation diverges from this plan (user changes mind, new constraint surfaces), update this file BEFORE acting on the change.

**End of tmp-updates.md.**
