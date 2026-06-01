# Historian / Prior-Art Auditor — Phase 0 findings

**Role.** I am the Historian persona. My job was to search the project history more thoroughly than the lead agent did during Phase 0.1, and surface user-stated constraints that the v3 brief may have missed.

**Method.** Reviewed [`constraints-extracted.md`](../../constraints-extracted.md) and [`00-brief-v3.md`](../../00-brief-v3.md); then searched: [`AGENTS.md`](../../../../AGENTS.md), [`CLAUDE.md`](../../../../CLAUDE.md), [`research-plan.md`](../../../../research-plan.md), [`initial-sources.md`](../../../../archive/PR-180-initial-sources.md), [`research/PLAN.md`](../../../../research/PLAN.md); all 30 retrospective files under [`retrospective/`](../../../../retrospective/) with grep filters for `user said|asked|wants|explicit|direction|request|instructed|feedback`; all ten ADRs under [`docs/adr/`](../../../../docs/adr/); commit messages via `git log --all --format="%h %an %s" --no-merges`; user-authored commits via `git log --author=jonathan`; the only OPEN GitHub issue (#118) and the comment history on issue #105; PR #124 (the v3 plan PR), PR #46 (research-plan.md), PR #117, PR #106, PR #113, PR #114.

**Result preview.** I confirm all 8 captured constraints (C1–C8). I find **6 additional user-stated constraints** the lead agent missed, most of which sit in retrospectives that quote the user verbatim. I flag **2 lower-confidence items** and **1 mild contamination concern**. Two coverage gaps remain.

---

## Section 1 — Confirmed constraints (already captured)

| ID | Confirmed by | Additional supporting quotes found |
|----|---|---|
| **C1** (lights-out, greenfield, software factory) | Yes — [`research-plan.md`](../../../../research-plan.md) opening sentence stands. | None new. |
| **C2** (brownfield as co-equal) | Yes — only the in-session user message; not contradicted anywhere in history. | None new (this is a recent addition; predates no commit material). |
| **C3** (explicit mandate-fit on every recommendation) | Yes — only the in-session user message. | None new. |
| **C4** (user hypothesis as falsifiable) | Yes — in-session message. | None new. |
| **C5** (accuracy ≫ speed ≫ tokens) | Yes — in-session. | **Indirectly strengthened** by [`retrospective/2026-05-21-106.md`](../../../../retrospective/2026-05-21-106.md) Phase 2: user repeatedly chose "write to a temp file and commit just in case" and accepted six plan-revision rounds before execution — behavioural confirmation that the user trades wall-clock and tokens for correctness as a standing preference, not just for this synthesis. |
| **C6** (post-Round-12 corpus, archive-and-rebuild) | Yes — in-session. | **Strengthened** by [`research/PLAN.md`](../../../../research/PLAN.md) §10 round-by-round table (Rounds 1–12 enumerated, all ✅ except Round 11 stage-5 deferred). The post-Round-12 corpus is the only complete-corpus snapshot the project has. |
| **C7** (frozen seed list in [`initial-sources.md`](../../../../archive/PR-180-initial-sources.md)) | Yes — [`research/PLAN.md`](../../../../research/PLAN.md) §2 explicitly tags it `(frozen)`. | None new. |
| **C8** (process skills, PR-ready, internal-refs, sources.json) | Yes — [`AGENTS.md`](../../../../AGENTS.md) verbatim. | Strengthened by [`retrospective/2026-05-20-101.md`](../../../../retrospective/2026-05-20-101.md) Phase 1, which independently confirms the PR-draft policy was a user-imposed override. |

All eight captured constraints survive the broader search.

---

## Section 2 — Missed constraints (new findings)

### M1 — `based-on-commit` + `based-on-date` header on every synthesis and every architecture file

- **Source.** [`retrospective/2026-05-21-106.md`](../../../../retrospective/2026-05-21-106.md) Phase 2 and Suggestion 8; codified in [`docs/adr/0004-synthesis-subdir-and-based-on-commit-header.md`](../../../../docs/adr/0004-synthesis-subdir-and-based-on-commit-header.md) (Accepted 2026-05-21).
- **Quote.** *"Metadata at the top indicating commit on which we based our syntheses. Put that same information in all files in architecture directory."* — user, during cleanup-plan v2 review.
- **Constraint.** Every v3 synthesis file (greenfield-synthesis, brownfield-synthesis, shared-substrate, divergence, contradictions, failure-modes-v3, corpus-inventory, every Phase-2 track, every Phase-6 architecture spec) **must carry a YAML frontmatter header** of the form:
  ```
  ---
  based-on-commit: <short-hash>
  based-on-date: YYYY-MM-DD
  ---
  ```
  The hash records the corpus state the document is grounded in, not when the header was added. ADR-0004 makes this binding for `architectures/*.md` and `research/synthesis/*.md`.
- **Why the v3 brief should carry this.** The brief currently does not mention the header convention at all. Phase 2's 6 parallel tracks will produce 6 new files; Phase 6 will produce N more. Without an explicit reminder in the brief, the subagents will not author the header, and the discipline will rot at the moment the v3 set is largest.
- **Confidence.** **High.** Direct user quote; Accepted ADR; precedent of backfilling all five existing architecture files.

### M2 — Concrete-task criterion ("if you can't tell me exactly what to do, it isn't a task")

- **Source.** [`retrospective/2026-05-21-106.md`](../../../../retrospective/2026-05-21-106.md) Phase 2; codified as [`docs/adr/0005-concrete-task-criterion-for-plan-doc-entries.md`](../../../../docs/adr/0005-concrete-task-criterion-for-plan-doc-entries.md).
- **Quote.** *"there is only work if you can tell me exactly what to do. Otherwise it isn't a task. Use this criteria for all steps."* — user, during cleanup-plan v2 review.
- **Constraint.** Plan / task / TBD / DECISIONS-PENDING entries in v3 artifacts must each name an explicit next action ("who does what to which file"). Vague "we should consider X" entries are not tasks; they either become concrete or get deleted. This binds the way the v3 plan's checkpoints, the Phase-2 track outputs, and the Phase-3 DECISIONS-PENDING markers are written.
- **Why the v3 brief should carry this.** The current [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) has several entries (e.g. Phase-3 "DECISIONS-PENDING items surfaced to user via `AskUserQuestion`") that are concrete; others (e.g. Phase 7 "TBD items surfaced to user") are not. The brief should be explicit that v3 inherits this discipline.
- **Confidence.** **High.** Direct user quote; Accepted ADR.

### M3 — Three-layer pipeline contract (reports → synthesis → architectures → ADRs) is binding

- **Source.** [`docs/adr/0002-three-layer-research-pipeline.md`](../../../../docs/adr/0002-three-layer-research-pipeline.md) (Accepted 2026-05-21); user-authored [`research-plan.md`](../../../../research-plan.md) §"the-three-layer-pipeline" is the cited source the ADR extracts.
- **Quote.** From [`research-plan.md`](../../../../research-plan.md) §The three-layer pipeline: *"The repo is already structured as a funnel; the funnel just isn't closed yet."* and the named layers (Reports / Synthesis / Architectures). ADR-0002 makes the contract binding ("Flow direction is strictly one-way: reports → synthesis → architectures → ADRs").
- **Constraint.** v3 architecture specs **cite synthesis, not raw reports** for justification. The Phase-6 specs cannot footnote a report number directly when making a load-bearing claim; the claim must trace through a synthesis section. The brief lists ADRs and architecture specs as outputs but does not say "architectures cite synthesis, ADRs do not cite reports at all."
- **Why the v3 brief should carry this.** ADR-0002 §"Consequences" lists this as a guardrail. Phase 5's ADRs and Phase 6's specs will violate it by accident otherwise (especially when subagents have the corpus-inventory file in front of them and the synthesis files freshly-written).
- **Confidence.** **High.** Accepted ADR plus user-authored source document.

### M4 — Catch the cold-start problem for greenfield as its own design question

- **Source.** [`research-plan.md`](../../../../research-plan.md) §"One specific risk for the greenfield mandate".
- **Quote (user-authored, verbatim).** *"The four architectures were designed against a 'general execution environment, solo→small team' brief. *Lights-out greenfield* is a different shape — no existing issue queue, no codebase to learn from, no prior scenarios. Atelier's strongest assets (the queue, the workpad, accumulated `docs/solutions/`) do not exist on day one. The cold-start problem for a greenfield factory is its own design question and is not directly addressed in the current comparison. Worth a dedicated synthesis section before v3 of the architectures."*
- **Constraint.** The cold-start problem must be addressed as a **dedicated synthesis section** in the greenfield mandate, not folded into a generic methodology track. The brief addresses this partially (OQ-B5, the "G-cold-start-first" track in Phase 2) but treats it as one of three framings rather than as the user-flagged primary risk. The user's [`research-plan.md`](../../../../research-plan.md) language is stronger: a dedicated synthesis section is required, before v3 of the architectures.
- **Why the v3 brief should carry this.** Currently in [`00-brief-v3.md`](../../00-brief-v3.md) §8 OQ-B5 it is listed as one of six open questions. The user's source ranks it as the load-bearing risk of the greenfield mandate. Promote it from "open question" to "mandatory synthesis section of every greenfield track output."
- **Confidence.** **High.** Direct user-authored text in [`research-plan.md`](../../../../research-plan.md).

### M5 — Round-3 RE/SE + governance threads (reports 25/26 + followup/10 + reports 30/31) must feed the cold-start treatment

- **Source.** [`research-plan.md`](../../../../research-plan.md) §"One specific risk", final paragraph.
- **Quote.** *"Rounds 9–11 added an RE/SE-methodology thread (reports 25/26) and a governance thread (followup/10 + reports 30/31) that weren't on the radar when this doc was first written; both should feed the cold-start treatment."*
- **Constraint.** The Phase-2 greenfield cold-start track and the Phase-3 merge step **must explicitly engage with reports 25, 26, 30, 31, and followup/10**, not just the corpus-inventory's tagged-greenfield subset. The user has flagged these as the specifically-relevant threads.
- **Why the v3 brief should carry this.** The brief currently says "the synthesis inputs are the post-Round-12 corpus" generically (C6). It does not name the user-flagged threads that must touch cold-start. Phase-1 corpus inventory may not surface this if the per-report anchor is brief; an explicit pointer in the brief prevents the threads from being skipped.
- **Confidence.** **High.** Direct user-authored text.

### M6 — F36/F37 numbering collision triage is a lead-agent call, not a subagent call

- **Source.** [`research/PLAN.md`](../../../../research/PLAN.md) §3.6 and §6.2.
- **Quote.** *"Required triage: lead agent decides numbering."* (§3.6) and *"Lead agent triage decision"* (§6.2 table).
- **Constraint.** In Phase 1B (failure-mode consolidation), the F36/F37 resolution **must be done by the lead agent**, not delegated to a subagent. The brief and plan currently say "F36/F37 collision resolved per [`PLAN`](research/PLAN.md) §3.6 (lead-agent judgment, not subagent)" — so it IS captured in the plan. But it is **not in [`constraints-extracted.md`](../../constraints-extracted.md) or in [`00-brief-v3.md`](../../00-brief-v3.md)**. The brief should mirror it because the brief is the document the Phase-1 subagents will read; if they read the brief alone they will not know.
- **Why the v3 brief should carry this.** Subagents read the brief; the plan is for the lead agent. The constraint needs to appear in both.
- **Confidence.** **Medium-high.** The user's text in PLAN.md says "lead agent decides", which is a user-given task assignment. Whether it rises to a hard constraint or stays a procedural note is judgement; I am flagging it because the failure mode (a subagent silently triaging a numbering decision) is invisible.

---

## Section 3 — Suspected lead-agent contamination

### Mild concern — C4's "spec-malleability vs existing-architecture-as-given" framing

The user's actual words (verbatim, captured in C4):

> "My suspicion is that we won't find one that works best with both, because a brownfield one will focus on analyzing what is there and growing it, whereas a greenfield approach is going to strongly depend on the spec, and will have a malleable architecture during refinement of the spec, whereas brownfield will not."

This is preserved accurately. But [`00-brief-v3.md`](../../00-brief-v3.md) §3 paraphrases it as: *"Greenfield is **spec-malleable** (architecture changes during spec refinement). Brownfield is **code-archaeological + existing-architecture-as-given** (architecture is largely fixed by the existing codebase; the factory analyses what is there and grows it)."*

The phrases **"spec-malleable"** and **"code-archaeological + existing-architecture-as-given"** are crisp lead-agent labels for what the user said in longer prose. They are accurate compressions, not distortions — but they are now anchor terms that downstream tracks will inherit. The risk is that **the labels become load-bearing in their own right**, and Phase-3 cross-mandate adversarial subagents test the *labels* rather than the user's *underlying claim*.

**Recommendation.** Add a footnote in the brief: "The labels 'spec-malleable' and 'code-archaeological' are lead-agent shorthand for the user's longer prose (C4). Adversarial subagents should challenge the underlying claim, not the labels."

**Confidence that this is contamination.** **Low–medium.** The labels are accurate; the concern is downstream anchoring, not misquotation.

### No other contamination detected

The "explicitly NOT a constraint" list at the bottom of [`constraints-extracted.md`](../../constraints-extracted.md) is well-policed: I checked the five items and all five are correctly attributed to lead-agent or prior-synthesis sources, not the user. In particular:

- "Compound Atelier as baseline" — confirmed from [`architectures/00-comparison.md`](../../../00-comparison.md) §7.1, which carries no user quote.
- "Atelier + Refinery's layered-spec discipline" — from [`research-plan.md`](../../../../research-plan.md) §"What 'enough research' should trigger" item 2, hedged with "likely" and "probably" — clearly a lead-agent recommendation in a user-authored document. Correctly excluded.
- "Four architectures as a count" — correctly excluded.

---

## Section 4 — Coverage gaps

Areas where user-stated constraints might exist but I could not exhaustively search:

1. **PR review-comment threads.** `mcp__github__pull_request_read` for `get_comments` and `get_review_comments` returned empty for PR #124, #117, #106, #46 — but the user's standing pattern (per [`retrospective/2026-05-21-106.md`](../../../../retrospective/2026-05-21-106.md)) is to give feedback in **chat**, not on the PR itself. I did not exhaustively grep all 30 retros for every chat-quoted user-line; I sampled the high-signal ones (101, 106, 113, 114, 117, 122). **Risk.** A user constraint stated in a chat session that produced a retro I did not open is missing from my findings. Mitigation: a follow-up grep `for "user said\\|user explicit\\|user request" across all retros, with a human (not me) ranking which quotes are constraints` would close the gap cheaply.

2. **The harness/runs/ directory.** I did not search [`harness/runs/`](../../../../harness/) for user-authored notes — these directories are dispatched-run reports, predominantly subagent output, but the run-launching session text may carry user direction. Low-probability source of new constraints.

3. **Issue bodies for closed issues.** I read the only OPEN issue (#118) and the comment history on the closed-issue #105. There are ~100 closed issues; the user-authored ones (filter `author:jonathanmanton`) may carry constraints. I did not enumerate them. The user's commit history shows only six user-authored commits, so the user predominantly directs via chat and PR-review rather than via filing issues; I judged this gap low-risk but it is real.

4. **`/tmp/cleanup-plan-revised.md`** (deleted in commit `0d2272d`). This was the live user-vs-agent negotiation surface for PR #106. Its final state is gone; only the v3-derived ADRs survive. If there were constraints in v4 or v5 of that file that did not make it into ADRs 0004–0006, they are lost. Probability of missed material is medium — but recoverable via `git show 0d2272d^:cleanup-plan-revised.md` if a follow-up wants to read it.

---

## Summary report (for the parent agent)

- **Constraints confirmed (C1–C8):** 8 of 8. All survive the broader history search. C5 and C6 are additionally strengthened by behavioural and structural evidence not in the extraction note.
- **New constraints found:** 6.
  - **High confidence (4):** M1 (based-on-commit header), M2 (concrete-task criterion), M3 (three-layer pipeline citation discipline), M4 (cold-start as a dedicated greenfield synthesis section), M5 (named reports 25/26/30/31 + followup/10 must feed cold-start).
  - **Medium-high confidence (1):** M6 (F36/F37 triage is a lead-agent call; needs to migrate from the plan into the brief so subagents see it).
- **Contamination flags:** 1 mild — the "spec-malleable" and "code-archaeological" shorthand in the brief §3 are accurate compressions of C4 but risk becoming load-bearing anchor terms downstream; recommend a footnote clarifying the labels are paraphrase, not user-authored.
- **Coverage gaps:** 4, none judged blocking — (a) un-sampled retros may carry quoted user constraints, (b) `harness/runs/` not searched, (c) closed-issue bodies not exhaustively searched, (d) the deleted `cleanup-plan-revised.md` v4/v5 negotiation surface is gone from the live tree but recoverable from git.

*End of historian-findings.md.*
