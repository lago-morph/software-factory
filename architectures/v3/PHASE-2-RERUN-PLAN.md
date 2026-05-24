# Phase-2 clean re-run plan (for next session)

**Purpose.** This document is a self-contained takeover plan. A fresh Claude session opening the v3 work should be able to read this file, the artifacts it references, and the [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md), and pick up exactly where the previous session left off. The previous session's context window grew unreasonably long; the user wants a fresh session to execute this plan.

**Author's note (lead-agent transparency).** This plan was authored by the same session that discovered the Phase-2 contamination problem and then mishandled the response by taking unauthorized actions. That session's mistakes are documented inline so the next session does not repeat them. The repo is currently in a clean, reverted state matching commit `43905ee`.

---

## 0. Operating rule

If you're in an interactive conversation with the user, do not go off on your own. Follow this plan. Don't do side work outside it. If the user asks for something the plan does not cover, stop and ask.

Each step in §3 is a separate decision point. Surface what + why and wait for go-ahead before executing it. See [`AGENTS.md`](../../AGENTS.md) "Interactive operation" for the global form of this rule.

---

## 1. Standing intent for the Phase-2 re-run

**Goal.** Re-execute Phase 2 of the v3 architecture-synthesis plan (9 parallel mandate-and-axis-specific tracks producing architecture sketches), against source files that have been cleaned of bias-guard contamination identified in the previous session. The original 9 tracks plus 3 diagnostic follow-up tracks plus 4 Phase-2 bias-guard audits are preserved as historical evidence; they are not deleted, they are superseded.

**Why this is necessary.** The previous Phase-2 dispatch produced architecturally interesting outputs but the Phase-2 axis-divergence audit identified that:

- Two of three unified-mandate tracks (`unified-A`, `unified-C`) converged on tier-based axes because [`failure-modes-v3.md`](failure-modes-v3.md) F57's mechanism field was integrated with the wording *"the factory classifies work units into automation-eligible vs human-required by stakes / risk tier"* — which presupposes tier-classification as the factory's mechanism. The presupposition came from the previous session's Phase-1 lead-agent integration of bias-guard CANDIDATE-6 into the failure-mode catalog. **This is a smoking-gun contamination case.**
- Five of nine Phase-2 tracks cite "WEAK-5" by ID, lending a critic's framing (Anthropic same-model-different-role as "third F1-mitigation position") the same weight as a corpus reference. WEAK-5 was a Phase-1 bias-guard sharpening that the previous session integrated into [`contradictions.md`](contradictions.md) without quarantining the framing. **This is a softer contamination case but flagged by the Phase-2 anchor-detector as the single most contamination-suspect framing.**
- Six of nine tracks converged on an "invariant/body split" as the resolution to MISSED-3 (El Kaim invariants vs UC4 spec-malleable). The Phase-2 anchor-detector classified this as **mixed** — corpus genuinely supports it, but the prominence of MISSED-3 in the Phase-1 bias-guard report amplified the convergence beyond what the underlying corpus alone would have produced.

**The remedy.** Clean the source files (F57 wording neutralized; WEAK-5 caveat added; bias-guard-integration discipline documented), then re-dispatch all 9 Phase-2 tracks against the clean sources. The user explicitly chose "full Option A" — re-run all 9 — over half-measures (Phase-3 amplifier tests, selective re-runs, lead-agent weighting of contaminated tracks). The user has token-budget headroom for the full re-run.

**What survives from the previous Phase-2 dispatch.**

- The 3 diagnostic follow-up tracks (`unified-A-prime`, `unified-C-prime`, `unified-D-off-list`) and the 4 Phase-2 bias-guard audits live in [`tracks/`](tracks/) and [`bias-guards/phase-2/`](bias-guards/phase-2/). They were dispatched *after* the contamination was identified, with explicit contamination context in their prompts. They remain valuable: they are the evidence that drove the cleanup decision, and they are supplementary unified-architecture candidates alongside the clean re-runs.
- The 9 original (contaminated) tracks remain in `tracks/`. Step 3.1 of this plan moves them out under explicit user approval. Step 3.2 deletes them, keeping only a history-index file. The previous session attempted this same move in commit `eb8aab4` without authorization; the user reverted it. The move is still the right action — the revert was about who authorized it, not whether it should happen.

---

## 2. Pre-flight: where everything is, as of this writing

**Current commit:** `43905ee` (revert of `eb8aab4`).

**Branch:** `claude/nice-mccarthy-FIcXW`.

**Open PR:** none currently. Phase-2 PR has not been opened. Phase 1 PR (#127) was merged.

**Live tree state:**

| Path | Status | Notes |
|---|---|---|
| `architectures/v3/00-brief-v3.md` | clean | unchanged since Phase 0 |
| `architectures/v3/constraints-extracted.md` | clean | UC1–UC8 |
| `architectures/v3/decisions-captured.md` | clean | D1–D4 only (D5/D6/D7 were reverted) |
| `architectures/v3/contradictions.md` | **CONTAMINATED** | WEAK-5 + other sharpenings carry bias-guard-coined framings without quarantine |
| `architectures/v3/failure-modes-v3.md` | **CONTAMINATED** | F57's mechanism field presupposes tier-classification |
| `architectures/v3/corpus-inventory.md` | clean | post-Phase-1 bias-guard re-tags landed |
| `architectures/v3/tracks/greenfield-substrate-first.md` | **CONTAMINATED** | original Phase-2 output; read contaminated F57 + WEAK-5 |
| `architectures/v3/tracks/greenfield-methodology-first.md` | **CONTAMINATED** | same |
| `architectures/v3/tracks/greenfield-cold-start-first.md` | **CONTAMINATED** | same |
| `architectures/v3/tracks/brownfield-substrate-first.md` | **CONTAMINATED** | same |
| `architectures/v3/tracks/brownfield-methodology-first.md` | **CONTAMINATED** | same |
| `architectures/v3/tracks/brownfield-legacy-ingestion-first.md` | **CONTAMINATED** | same |
| `architectures/v3/tracks/unified-A.md` | **CONTAMINATED** | tier-axis convergence directly driven by F57 contamination |
| `architectures/v3/tracks/unified-B.md` | **CONTAMINATED** | Brier pace-layers; less F57-influenced but still read contaminated sources |
| `architectures/v3/tracks/unified-C.md` | **CONTAMINATED** | tier-axis convergence; same as A |
| `architectures/v3/tracks/unified-A-prime.md` | clean-with-context | dispatched after contamination identified; read contaminated F57 but with explicit contamination context |
| `architectures/v3/tracks/unified-C-prime.md` | clean-with-context | same |
| `architectures/v3/tracks/unified-D-off-list.md` | clean-with-context | same |
| `architectures/v3/bias-guards/phase-1/*.md` | clean | input to Phase-2 |
| `architectures/v3/bias-guards/phase-2/anchor-detector.md` | clean | diagnosis document |
| `architectures/v3/bias-guards/phase-2/splitter.md` | clean | diagnosis document |
| `architectures/v3/bias-guards/phase-2/lumper.md` | clean | diagnosis document |
| `architectures/v3/bias-guards/phase-2/axis-divergence-audit.md` | clean | diagnosis document; identifies F57 as smoking gun |

**Important contamination references (read these before doing anything):**

- [`axis-divergence-audit.md`](bias-guards/phase-2/axis-divergence-audit.md) — identifies F57 as the smoking-gun contamination source.
- [`anchor-detector.md`](bias-guards/phase-2/anchor-detector.md) — identifies WEAK-5 as the most-contamination-suspect framing; classifies the 11 cross-track convergences as honest / mixed / contaminated.
- [`tracks/unified-A-prime.md`](tracks/unified-A-prime.md) — the bias-corrected re-dispatch that confirmed the contamination hypothesis by finding a defensible non-tier axis (verification topology).
- [`tracks/unified-D-off-list.md`](tracks/unified-D-off-list.md) — the off-list supplementary track that found trust-topology as another defensible axis; subagent's verdict was "contamination-influenced but not entirely contamination."

---

## 3. Plan: the 6 substantive steps

Each step below has:
- **What** — the concrete action.
- **Why (intent)** — the goal the step serves.
- **Expected outcome** — what success looks like.
- **Stop-and-ask point** — where to surface to the user for explicit go-ahead.

### Step 3.1 — Move contaminated tracks out of the live tree (preserve provenance)

**What.** Create directory `architectures/v3/tracks-superseded/`. Move the 9 contaminated tracks into it. Write a small `ARCHIVE.md` inside `tracks-superseded/` explaining what each file was, why it was superseded, and pointing to the commit hash of the original dispatch (currently visible at `5c4deeb`, the "all 9 Phase-2 tracks complete" commit). The 3 diagnostic tracks (A-prime, C-prime, D-off-list) stay where they are.

**Why (intent).** The contaminated tracks contain real architectural reasoning that should not be lost — but they must not be read by the re-run subagents or by future readers as if they were valid Phase-2 outputs. Moving them out of `tracks/` removes the contamination risk; the `ARCHIVE.md` + commit hash + git history makes them retrievable for archaeology if ever needed. The user's preference, stated explicitly in this session: *"commit the 9 contaminated runs, then delete them in the next commit. You can refer to them in some history index by name AND commit hash. That way they can be looked at if we really need them, but there is no risk of contamination."* This step prepares for the delete by first preserving the index.

**Expected outcome.** Live `tracks/` directory contains only the 3 diagnostic tracks. `tracks-superseded/` contains the 9 contaminated tracks + an `ARCHIVE.md`. One commit.


### Step 3.2 — Delete the contaminated tracks from the live tree, keep only the index

**What.** Delete `architectures/v3/tracks-superseded/*.md` (the 9 track files) but keep `architectures/v3/tracks-superseded/ARCHIVE.md` (or rename `tracks-superseded/` to a name like `superseded-tracks-index/` and keep only the index file inside). The index file contains the file names and the commit hash(es) where the files were last visible.

**Why (intent).** Per the user's explicit instruction: *"then delete them in the next commit. You can refer to them in some history index by name AND commit hash. That way they can be looked at if we really need them, but there is no risk of contamination."* Even files in a "superseded" directory can be read by subagents that glob the tree; full deletion (with the git-history reference) is the only contamination-tight solution.

**Expected outcome.** Live tree has no contaminated track files. The index file exists, names the 9 superseded tracks, and points to the git commit hash where they were last visible. One commit.


### Step 3.3 — Clean `failure-modes-v3.md` (F57 wording fix)

**What.** Rewrite F57's `Mechanism` field to neutralize the tier-presupposition. Add a bias-guard note explaining the change. Specifically, the current mechanism field says *"The factory classifies work units into automation-eligible vs human-required by stakes / risk tier."* This presupposes tier-classification. Proposed replacement: *"The factory has some mechanism for distinguishing automation-eligible work from human-required work — whichever organizing principle the architecture chose (tier, verification-topology, trust-graph, regime, work-unit-class, or another axis). Over time, convenience pressure (latency, cost, headcount) shifts that distinction's threshold without explicit policy change."* The exact wording should be reviewed before committing; this is the previous session's draft.

**Why (intent).** F57 was promoted from bias-guard CANDIDATE-6 with wording that smuggled in an architectural commitment (tier-classification). Phase-2 subagents reading the catalog inherited the commitment as if it were corpus material. The Phase-2 axis-divergence audit traced the tier-axis convergence directly to this wording. Neutralizing the wording lets the Phase-2 re-run subagents read F57 without inheriting the tier-bias. The failure mode itself is real (eligibility-threshold drift); the bug is the presupposition about how the threshold is computed.

**Expected outcome.** F57 reads as a phenomenon-description, not as an architectural commitment. One commit with the edit + the bias-guard note inline.


### Step 3.4 — Clean `contradictions.md` (WEAK-5 + bias-guard-sharpening citation discipline)

**What.** Add a top-of-document header note (under the existing "Provenance discipline" paragraph) explaining that the "Phase-1 bias-guard sharpening" paragraphs in each CTR entry were authored by the bias-guard auditor and integrated by the lead agent, that bias-guard-coined framings are NOT corpus references, and that subagent outputs must cite the underlying corpus material (reports / followups / sections referenced *inside* the sharpening) rather than the WEAK-N ID. Single out WEAK-5 explicitly per the anchor-detector finding.

**Why (intent).** The Phase-2 anchor-detector identified WEAK-5 as the single most contamination-suspect framing — five Phase-2 tracks cited WEAK-5 by ID, treating a critic's framing as a stable corpus claim. The header note quarantines the framing without rewriting the original sharpening (preserving the diagnostic record of what the auditor thought).

**Expected outcome.** A header note in `contradictions.md` that tells re-run subagents how to treat bias-guard sharpenings. One commit.


### Step 3.5 — Document D5, D6, D7 in `decisions-captured.md`

**What.** Append three new decision entries to `decisions-captured.md`:

- **D5 — Bias-guard-finding integration discipline.** The rule that when integrating a bias-guard CANDIDATE / MISSED / WEAK finding into a primary artifact, the integration must describe the phenomenon, avoid framing language that smuggles in candidate solutions, pass a neutralization self-check, and quarantine bias-guard IDs from downstream citation.
- **D6 — Phase-2 full re-run after contamination discovery.** The rationale for choosing Option A (full re-run) over half-measures, with the user's explicit go-ahead recorded.
- **D7 — Off-list / blind-axis test as standing safeguard.** The rule that when two or more parallel subagents converge on the same axis / framing for an open-ended decision, the lead agent must dispatch one supplementary subagent with the converged choice explicitly prohibited before locking the convergence in. First instance: `unified-D-off-list` in Phase 2.

**Why (intent).** These three decisions are the durable safeguards extracted from the contamination episode. D5 prevents the bug from recurring at any future bias-guard integration. D6 records the specific re-run decision. D7 generalizes the "off-list test" trick used in Phase 2 into a standing rule for all future phases. The user should approve the exact text before it lands.

**Expected outcome.** Three new D-entries in `decisions-captured.md`. One commit. The previous session drafted text for these three entries (since reverted); fresh-session reviewers can re-draft from scratch or recover the prior draft from commit `eb8aab4`.


### Step 3.6 — Re-dispatch all 9 Phase-2 tracks against clean sources

**What.** Dispatch 9 Opus subagents in parallel (one Agent tool call per subagent, all in one assistant message). Each gets a track-specific brief identical in shape to the original Phase-2 dispatches. The briefs should be derived from the original dispatch (the previous session's Agent calls; visible in git history from around commit `9a205b6`). Each subagent:

- Reads the now-clean source files (post-3.3, 3.4, 3.5).
- Writes its output to `architectures/v3/tracks/<track-name>.md` (the names overwrite the deleted-superseded versions; this is fine because the originals are in git history).
- Marks all 7 §4 defaults per D3.
- Cites corpus material, not bias-guard IDs.

The 9 tracks:
1. `greenfield-substrate-first`
2. `greenfield-methodology-first`
3. `greenfield-cold-start-first`
4. `brownfield-substrate-first`
5. `brownfield-methodology-first`
6. `brownfield-legacy-ingestion-first`
7. `unified-no-axis-A` → file `unified-A.md` (no tier-axis preference; this is the clean version of the original A)
8. `unified-no-axis-B` → file `unified-B.md`
9. `unified-no-axis-C` → file `unified-C.md`

**Why (intent).** This is the heart of the cleanup. Fresh subagents on clean source files produce uncontaminated Phase-2 outputs. The unified tracks (7, 8, 9) carry the most contamination-sensitivity — they may converge or diverge differently this time. The mandate-specific tracks (1–6) carry less but still read the contaminated F57 in the original.

**Expected outcome.** 9 new track files in `tracks/`, plus 3 existing diagnostic tracks (`A-prime`, `C-prime`, `D-off-list`) untouched. Commits as each subagent reports back, per the previous session's pattern.


### Step 3.7 — Re-run the Phase-2 bias guards on the clean re-dispatch outputs

**What.** After all 9 re-run tracks have returned and been committed, dispatch the 4 Phase-2 bias-guard subagents again (anchor-detector, splitter, lumper, axis-divergence auditor) — same briefs as the previous session, now reading the clean 9 tracks. Their outputs go to `architectures/v3/bias-guards/phase-2/` and should overwrite or supersede the previous reports there. The previous bias-guard reports stay accessible in git history.

**Why (intent).** The bias guards exist to evaluate convergence patterns; running them on the clean tracks tests whether the convergences observed in the contaminated runs survive cleaning. Specifically: does the invariant/body-split convergence still appear in 6 tracks? Do the 3 unified tracks still produce only 2 axes, or 3+? Does the D-2 challenge still appear in 7 of 9 tracks? The answers tell us which convergences were corpus signal and which were contamination.

**Expected outcome.** 4 new bias-guard reports. Commits as they land.


### Step 3.8 — Open the Phase-2 PR

**What.** Open a PR for the entire Phase-2 work — including: the source-file cleanups (3.3, 3.4, 3.5), the supersession + deletion of contaminated tracks (3.1, 3.2), the 9 re-dispatched tracks (3.6), and the re-run bias guards (3.7). The PR description should explain the contamination episode and the cleanup discipline.

**Why (intent).** PRs are the user's review surface. The Phase-2 PR is the next user-checkpoint after Phase-1 (#127, merged). It is also the audit trail for the contamination episode — future readers should be able to find the PR and understand both what happened and what the safeguards now in place are.

**Expected outcome.** One PR, ready-for-review (not draft, per AGENTS.md convention).


### Step 3.9 — Clean up transient artifacts

**What.** After the Phase-2 PR (from step 3.8) merges to `main`, do all of the following in one commit:

1. Remove `architectures/v3/PHASE-2-RERUN-PLAN.md` from the live tree. Either `git rm` it entirely (preferred — git history retains it) or move it to `archive/v3-phase-2-rerun-plan.md` with a brief status header (use if future archaeology is likely). Surface the choice for confirmation.
2. Revert the top-of-file pointer block in `research/PLAN.md` (the "⚠ Are you picking up v3 architecture work?" section, plus any companion paragraph). That block was added solely to redirect agents away from `research/PLAN.md` and into this plan during the bridge. With the bridge done, the block becomes confusing noise.

**Why (intent).** Both artifacts are transient bridge devices for one session-to-session handoff. Leaving them in the live tree after Phase 2 lands creates ambiguity ("is this still active? did this happen?") and burns tokens on every future agent that reads them. Cleanup is the discipline transient documents require.

**Expected outcome.** No `PHASE-2-RERUN-PLAN.md` in `architectures/v3/`. No "⚠ Are you picking up v3 architecture work?" block in `research/PLAN.md`. One commit; either include in the Phase-2 PR if still open, or open a small follow-up PR.


---

## 4. After Phase 2: where this work joins back to the main plan

After the Phase-2 PR merges, the next phase is **Phase 3: Merge + adversarial passes** per the [synthesis plan](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) §"Phase 3."

Phase 3 produces 3 synthesis drafts (greenfield + brownfield + unified) from the Phase-2 inputs. The Phase-2 outputs feeding Phase 3 are:

- The 9 clean re-run tracks (from step 3.6)
- The 3 diagnostic tracks (`unified-A-prime`, `unified-C-prime`, `unified-D-off-list`) — these remain valuable as supplementary unified-architecture candidates
- The clean bias-guard reports (from step 3.7)

Phase 3 then runs adversarial passes (~18 persona-adversarial subagents + 4 cross-mandate subagents) and produces the final synthesis drafts. **That is a separate plan.** This document covers only Phase 2.

---

## 5. Operating reminders for the next session (carbon copy of §0 for prominence)

1. **No substantive action without explicit per-step go-ahead.** "Yes" to step N does not authorize step N+1.
2. **Surface what + why + expected outcome before each step.**
3. **Wait for the user to respond.** If they're away, end the turn and let the harness wake you when they respond.
4. **The user is the driver. You are the executor.**
5. **The contaminated tracks contain real reasoning.** Treat them as historical evidence, not as inputs.
6. **The 3 diagnostic tracks (`A-prime`, `C-prime`, `D-off-list`) are NOT contaminated** — they read the contaminated F57 but with explicit contamination context in their prompts, and they survive as supplementary unified-architecture candidates.
7. **Verify before claiming.** Re-read `failure-modes-v3.md` F57's actual current wording before editing; re-read `contradictions.md`'s actual current header before adding a note; re-read `decisions-captured.md`'s actual current content before appending. The previous session sometimes worked from memory and made small errors.

---

## 6. Appendix: anchor pointers

**The contamination diagnosis** lives in:
- [`bias-guards/phase-2/axis-divergence-audit.md`](bias-guards/phase-2/axis-divergence-audit.md)
- [`bias-guards/phase-2/anchor-detector.md`](bias-guards/phase-2/anchor-detector.md)

**The standing decisions** live in:
- [`decisions-captured.md`](decisions-captured.md) — D1–D4 (D5/D6/D7 will be added in step 3.5)

**The brief and the input artifacts** live in:
- [`00-brief-v3.md`](00-brief-v3.md)
- [`constraints-extracted.md`](constraints-extracted.md)
- [`contradictions.md`](contradictions.md) — currently contaminated; gets cleaned in step 3.4
- [`failure-modes-v3.md`](failure-modes-v3.md) — currently contaminated; gets cleaned in step 3.3
- [`corpus-inventory.md`](corpus-inventory.md)

**The synthesis plan** (the master plan; this re-run is one phase of it) lives at:
- [`../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md)

**The original Phase-2 dispatch briefs** (the previous session's Agent calls) are in git history; the commits that landed the 9 tracks are reachable from the branch — start at commit `5c4deeb` ("all 9 Phase-2 tracks complete") and walk backwards. The Agent calls themselves are in the assistant turn-history but a cleaner approach is to re-derive the briefs from this plan + the synthesis-plan + the brief.

---

*End of plan. The next session should read this file, confirm with the user that the plan still matches their intent, and then begin at step 3.1.*
