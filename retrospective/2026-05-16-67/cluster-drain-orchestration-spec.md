# Spec: `cluster-drain-orchestration`

## Intent

When a corpus drain spans many clusters of sources (a "round-N manual drain"), the orchestrator's context window is the binding constraint, not subagent compute. This skill makes the **serial cluster-by-cluster** pattern reproducible: one subagent per cluster, orchestrator commits + updates a per-cluster checklist between returns, and the resulting PR's commit log becomes a reviewable cluster-by-cluster audit trail.

Grounded in PR #67 (Round-10 manual drain): 71 sources across 15 clusters, 13 active subagent runs producing 11 new numbered reports + 8 existing-report upgrades + 10 failure-mode promotions, executed serially over a single overnight session without orchestrator context exhaustion.

## Trigger

Direct triggers:
- "Drain the manual folder via clusters"
- "Process the index cluster by cluster"
- "Round-N manual drain"

Proactive triggers:
- A `research/manual/` (or equivalent drop-zone) directory has >20 indexed sources organized into clusters.
- A `new-index.md` (or equivalent) explicitly enumerates per-cluster target reports.
- Orchestrator has a multi-hour window and the user has signaled "I'm going to sleep" / "work on this overnight."

Negative triggers (skip the skill):
- Fewer than 3 clusters / fewer than 10 sources — direct drain by orchestrator is cheaper.
- Sources don't fit into clusters (mix of unrelated topics) — fan-out parallel skill is better.
- The user wants synthesis, not ingestion.

## Inputs

- A path to a transient drop-zone directory (typically `research/manual/`).
- An index file in that directory (typically `new-index.md`) that:
  - groups sources into alphabetic clusters (A, B, C, …),
  - per-source: filename + URL + summary + image-inventory + target report + recommendation,
  - per-cluster: a header block.
- A PLAN.md file with a "Done" history list and an "in progress" status surface.
- Author-determined decisions on any ambiguities flagged by the indexing pass (`fold into X / alternative scope`).

## Outputs

- One new commit per cluster on a feature branch.
- One PLAN.md update per cluster (cluster-checklist row flipped ⬜ → ✅ + bullet list of surprises).
- A draft PR opened at start, promoted to ready-for-review at end.
- A retrospective summarizing the round (this skill's sibling).
- A non-draft PR with detailed body summarizing all clusters.

## Workflow

1. **Read the full index** (in chunks if needed — large indexes commonly exceed Read token limit; use `offset`/`limit`).
2. **Make ambiguity-resolving decisions** (the "fold into X / alternative scope" rows). Write them as an explicit `Orchestrator decisions` table near the top of the index file. **Forward-allocate report numbers** for every new report the round will create. Commit + push this decision document **before** dispatching any subagent — it anchors every brief.
3. **Open a draft PR** immediately after the decisions commit. Use a placeholder body promising the full body once clusters complete.
4. **For each active cluster** (skip clusters whose every source is a deleted duplicate from prior rounds):
   a. Write a per-cluster brief enumerating: source files (absolute paths), target reports (existing + new), what to add (specific sections, specific numbers), what NOT to touch, image-extraction instructions (if any kept MHTMLs), the exact `mhtml_extract.py` location, the 1-based-info / 0-based-save off-by-one warning, the AVIF-inside-`.png` warning, the deliverable format (300–600 word change report).
   b. Spawn ONE `general-purpose` subagent. Do not parallelize — context preservation, not throughput, is the goal.
   c. Wait for completion. Do not poll or do other unrelated work during the wait; if the subagent's results don't return, you can't update PLAN.md.
   d. On return: run `git status --short` and `git diff --stat HEAD` to verify the change scope matches the deliverable claim.
   e. Update PLAN.md: flip the cluster checkbox; inline 3–8 surprises from the change report into a Surprises bullet list under the checkbox.
   f. Stage every changed file by absolute path; commit with a multi-line message — subject line summarizing the cluster (e.g. `research: drain Cluster N → new reports 34/35/36`), body summarizing what each file got and the key surprises.
   g. Push.
5. **After the final cluster** lands: run the `self-retrospective` skill, then update the PR body (long-form) and flip the PR draft → ready.
6. **Subscribe to PR activity** so review comments / CI events route into the session.

## Concrete examples

### Example 1: Round-10 manual drain (PR #67) — the canonical run

- 15 clusters indexed; 2 skipped (all sources already-deleted duplicates).
- Orchestrator-decisions table written + committed before any subagent dispatch (`2624f01`). Reserved report numbers 27–37 for 11 new reports.
- 13 active subagents dispatched serially. Each ran 5–18 minutes.
- One commit per cluster (13 cluster commits + 1 orchestrator-decisions commit + 1 retrospective commit on the same branch).
- PLAN.md's `Round-10 manual drain` block updated 13 times, each time recording 3–8 cluster-specific surprises (e.g. for Cluster F: "harness-engineering author is Ryan Lopopolo, not Celia Chen et al. — mirror-era byline was wrong"; for Cluster N: "Three-source per-employee org-primitive convergence Feb–May 2026").
- Final PR body lists every cluster with what landed where + every failure-mode promotion (F40–F49) + every primary-source upgrade (5 Cloudflare-blocked URLs closed).

### Example 2: A round you should NOT run with this skill

- User drops 6 unrelated sources into `research/manual/` with no index. There are no clusters to drain — direct read + write by the orchestrator is faster. **Skip this skill; just do the drain.**

## Anti-patterns

- **Parallelizing the subagents.** Defeats the purpose. The orchestrator's context window is the binding constraint, not subagent compute. Serial.
- **Batching commits across clusters.** Loses the cluster-by-cluster audit trail. One cluster, one commit.
- **Dispatching without an orchestrator-decisions table.** Subagents will collide on report numbers and overlapping framings.
- **Letting a subagent edit PLAN.md.** The orchestrator owns PLAN.md exclusively. Subagents return change reports; the orchestrator transcribes the surprises.
- **Skipping the post-return git diff check.** Subagents sometimes overstate (or understate) their changes. Always verify.
- **Skipping the cross-section drift check on multi-section edits.** Use the `post-edit-reread-pass` skill or its discipline after any subagent that modified more than 3 sections of a long-lived document.
- **Trusting "this section was already present" claims from subagents** when the diff says +176 lines.
- **Forgetting to push between clusters.** Keep the remote current — if the session terminates, the work survives.
- **Letting the PR stay draft after the final cluster lands.** Flip to ready-for-review and subscribe.

## Acceptance criteria

1. Every cluster in the index either lands as a single commit OR is explicitly justified as a skip (e.g. "all sources are deleted duplicates from prior rounds").
2. The PR's commit log is a 1:1 mirror of the cluster sequence (no commits cross cluster boundaries).
3. PLAN.md's cluster checklist is fully ✅ at end of session, with surprise bullets under each.
4. Every new numbered report has a unique number, allocated up-front in the orchestrator-decisions table.
5. The final PR body covers every cluster + every new report + every primary-source upgrade + every failure-mode promotion, with cross-references.
6. The retrospective lands on the same branch as the drain, anchored to the PR number.

## Files this skill creates / modifies

- `research/manual/new-index.md` — gets an `Orchestrator decisions` section added at the top by Step 2.
- `research/PLAN.md` — gets a "Round-N manual drain" block added under §1 with per-cluster checklist; updated after each subagent return.
- New report files under `research/NN-<slug>.md`.
- Existing reports / followups under `research/*.md` and `research/followup/*.md`.
- `research/figures/NN-<slug>/` directories with PNG figures embedded by relative path.
- `research/INDEX.md` — gets new rows per new report.
- `retrospective/YYYY-MM-DD-PPP.md` + `retrospective/YYYY-MM-DD-PPP/` — produced by the sibling `self-retrospective` skill at end.
