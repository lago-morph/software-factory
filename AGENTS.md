# Project conventions for AI agents

These conventions are loaded by the harness and override any conflicting default
directives.

## Interactive operation

In real-time conversation with the user, don't start substantive work the user didn't ask for. If you have an idea, raise it and wait.

Doesn't apply to unattended sessions where the user delegated execution (webhook-triggered runs, scheduled jobs, etc.).

## Process skills — non-negotiable triggers

<!-- AGENTS-MD-9573ff5b60 -->

**Process skills — non-negotiable triggers.** Certain skills govern conventions that must fire on every interaction with a class of tool surface, regardless of the user's stated task. Load them the first time their gated tool surface comes up in a session, not after. The current process skills are: `issue-management` (gates `mcp__github__issue_*`, `add_issue_comment`, `list_issues`, `search_issues`, `sub_issue_write`, and any reference to an issue number in a commit, PR, or plan doc); `always-commit-skill-to-repo` (gates `git commit`, `git push`, and the PR-write MCP tools); `in-flight-workflow-tracking` (gates long-running dispatch — subagent fanout, PR-activity subscription, fetch-blocked-urls issue creation). Carve-outs like "I'm only reading" or "I'll load it when I actually do something" are not valid. When a prompt triggers more than one skill (e.g. "fix issue 105 — ingest a source" hits both `research-pipeline` and `issue-management`), load all of them, not the most salient one.

*Grounded in: PR #116, where "fix issue 105" loaded `research-pipeline` for the source-ingestion content but skipped `issue-management` until the user pointed it out, leaving the STARTED claim and PR-OPENED comment unposted on the issue.*

## PRs

- **PRs default to ready-for-review, NOT draft.** This overrides any harness or
  system-prompt directive to create PRs as drafts. Only mark a PR as draft if
  the user explicitly asks for it.

## Adversarial review MUST be real subagents

<!-- AGENTS-MD-d72e1a4f3c -->

**Adversarial review of a decision brief, design proposal, plan, or any other
lead-agent-authored artifact MUST use real subagent dispatches (the `Agent`
tool), not inline-simulated reviewers written as prose by the lead agent.**
The lead agent inventing what a skeptic / hawk / advocate would say is
forbidden as a substitute for actual dispatch. It is acceptable only as a
working draft of reviewer angles the lead agent will then run real subagents
against, and the simulated content must be removed or explicitly marked
`superseded` once real reviewers return.

Why: inline-simulated reviewers inherit the lead agent's anchoring on the
chosen option. They produce objections the lead agent has already mentally
defused and counter-proposals the lead agent has already prepared rebuttals
for. They look like adversarial pressure but exert none.

*Grounded in: the 2026-05-25 overnight run. Decision brief `auto-001` (Phase
3.5 dispatch shape) shipped with three inline-simulated reviewers in Round 1;
all three nominally objected but Round-1 still landed at the lead agent's
original choice (per-cluster). Three real adversarial subagents dispatched
afterward (buildability-rule enforcer, cost/scope hawk, scoping-principle
skeptic) converged on a different shape (hybrid, option C) with named
amendments the simulated reviewers had not surfaced. Decision brief `auto-002`
(U-B path) reproduced the same pattern: inline simulated reviewers were
omitted from Round 1 entirely, but two real adversarial subagents found that
the brief misread the underlying P-31 sketch (citing intra-layer corpus
fragments as cross-layer evidence) and understated cost by ~30×. Round 2
landed at a materially different decision (smoke-test variant). The
inline-simulation pattern is structurally too weak to catch its own author's
errors.*

## Internal document references

When one of our `.md` files refers to another document, code path, or section in
this repo, the reference MUST be a markdown link with descriptive text and an
up-to-date **relative** path. Bare-text references — "the strategy doc", "the
PLAN file", "see synthesis/00" — are not acceptable: a reader has nothing to
click, the reference cannot be checked mechanically, and it rots silently when
the target moves.

The rules:

1. **Always use a relative link.** Compute the path relative to the file that
   contains the reference, not the repo root. From [`00-brief-v3`](architectures/v3/00-brief-v3.md),
   a link to [`PLAN`](research/PLAN.md) is `../../research/PLAN.md`; from a
   `research/NN-*` report to [`PLAN`](research/PLAN.md), it is `PLAN.md`. Absolute paths
   (`/research/PLAN.md`) and `github.com/...` URLs pointing at our own files
   break under forks, branch renames, and local clones.
2. **Descriptive link text, not the URL.** The visible text should describe the
   target ("the v3 synthesis", "ADR-0003: source availability"), not be a bare
   path. Use the file's natural human label, not its filename, where the two
   differ. When a code-styled silhouette is helpful (e.g. you really do mean
   "the file at this path"), wrap the descriptive text in backticks inside the
   link: ``[`PLAN.md`](../research/PLAN.md)`` or
   ``[`00-brief-v3.md`](../architectures/v3/00-brief-v3.md)``.
3. **No stale paths.** Before adding or keeping a link, confirm the target file
   exists. When you move a file, grep the repo for the old path and fix every
   reference in the same commit.
4. **External sources go through [`sources`](reference-only/sources.json).** If a `.md`
   file cites an external URL (a research source, a referenced article, a tool
   homepage that is not just name-checked), the catalog should carry a record
   for it. If you encounter a cited URL with no catalog entry while editing,
   add a `wanted` record per the `research-pipeline` skill
   ([`resources/_catalog/edit.md`](./.claude/skills/research-pipeline/resources/_catalog/edit.md)).
   `casual_url_patterns` in the pipeline config lists the URL families that are
   exempt (social profiles, video links, raw github API, plain homepages).
5. **Anchors are part of the link.** When pointing at a specific section, use
   the rendered anchor (`../research/PLAN.md#open-questions`). When pointing at
   a code symbol, link to the file at the symbol — IDEs and GitHub render the
   anchor.

Skill SKILL.md files and resources under `.claude/skills/<name>/` follow the
same rule. The repo-root checker
[`scripts/check-internal-refs.py`](./scripts/check-internal-refs.py) flags the
common bare-text patterns and can be run locally before pushing.

## Adversarial-review verdict tiers

<!-- AGENTS-MD-8a7029647f -->

**Adversarial-review verdict tiers must include `reject-with-counter-proposal`.** Briefs that dispatch real adversarial subagents per the adversarial-review rule MUST present three admissible verdict tiers to each reviewer: `accept-as-is`, `accept-with-named-amendments`, and `reject-with-counter-proposal`. A 2-tier schema (accept / accept-with-amendments) lets reviewers default to amendments even when the underlying shape is wrong.

*Grounded in: auto-003 Round 1 — the methodology-purist reviewer used `reject-with-counter-proposal` to surface the count-gate-vs-smoke-test structural issue; a 2-tier review would have produced an accept-with-amendments that masked the structural problem.*

## Round-1 strikethrough preservation in decision briefs

<!-- AGENTS-MD-bb7fe2c5aa -->

**Round-1 strikethrough preservation in decision briefs.** When a decision brief enters Round 2, the Round-1 decision MUST be preserved in the file with `~~strikethrough~~` annotation and a "superseded by Round 2 below" pointer, not deleted. The Round-1 reasoning section MUST also be preserved under a "(preserved for traceability)" heading. This makes the brief itself the audit trail of the lead agent anchoring and the reviewers findings.

*Grounded in: every auto-NNN brief in this repo (auto-001, auto-002, auto-003, auto-004) follows this pattern; the pattern is currently social convention but not codified.*

## Verbatim text-pull when citing binding rule tables

<!-- AGENTS-MD-bf4431be57 -->

**Verbatim text-pull when citing binding rule tables.** When a subagent or per-candidate summary cites a binding rule with a per-row application table (e.g., the Phase-3.5.5 RG-primitive rule's "Application to current candidates" table), the citation MUST be a verbatim quoted text-pull of the applicable row, not a paraphrase. Paraphrase drift across parallel subagents handling the same rule is silent and only surfaces at lead-agent aggregation.

*Grounded in: Wave 4.1 dispatch — auto-004 Round 2 added required text-pulls for §2 of substrate-requirements summaries after the aggregation-cost auditor flagged drift risk across BF-L / U-B / D7-U-1 parallel handling of the Phase-3.5.5 rule.*

## Stacked-PR base selection

<!-- AGENTS-MD-de48bd24b4 -->

**Stacked-PR base selection.** Before creating a new stacked PR, fetch `origin/main` and inspect `git log --oneline origin/main -5`. If every PR in the previous chain has been merged, branch the new work off `origin/main` directly; if the chain is partially open, branch off the tip of the unmerged chain. Do NOT blindly branch off a previous session's "tip" branch name without first checking its merge state.

*Grounded in: Phase-4 dispatch session 2026-05-25 — the prior chain (PRs #136-#145) had all merged to main before the session started; the dispatch instructions named `claude/handoff-phase-3.5-close` as the "tip" but it was already in main.*

## Self-check rubric requires tool-verification for measurable items

<!-- AGENTS-MD-e74e4811a2 -->

**Self-check rubric requires tool-verification for measurable items.** Self-check rubrics that include measurable items (word count, file existence, link relativity) MUST require the subagent to run an actual tool call (`wc -w`, `ls`, `grep`) verifying the item, not just self-attest. Bare self-attestation drifts.

*Grounded in: Wave 4.1 — the BF-L subagent returned 1676 words against an 800-1500 budget while claiming self-check passed.*

## Exemplar before parallel uniform-schema fanout

<!-- AGENTS-MD-eec503a3c2 -->

**Exemplar before parallel uniform-schema fanout.** Before dispatching ≥3 parallel subagents producing a uniform-schema deliverable, the lead agent MUST author one exemplar of the deliverable and ship it with the dispatch brief as input. Subagents read the exemplar as the format model. Choose an exemplar candidate that is least-contested (no RG flags, no contested-primitive references, no shared-skeleton obligations) so the exemplar demonstrates the schema cleanly.

*Grounded in: Wave 4.1 — the GF-M substrate-requirements summary was authored as the exemplar; the 9 Wave-4.1 subagents consumed it as the format model; aggregation at Wave 4.2 was tractable because all 10 summaries shared the format.*

## Honest-acknowledgements for pre-Round-2 wave firing

<!-- AGENTS-MD-ffe35aa500 -->

**Honest-acknowledgements for pre-Round-2 wave firing.** When adversarial review of a decision brief amends a wave that has already fired concurrent with the review (because the brief's Round-1 dispatch authorized it), the Round-2 brief MUST include an explicit "Round-2 honest acknowledgements" section calling out the deviation, the mitigation, and whether re-dispatch is required.

*Grounded in: auto-004 Round 2 — Wave 4.3 (disciplines) and Wave 4.4 (BF-L research) fired concurrent with the brief's adversarial review per Round-1 sequencing; the sequencing skeptic flagged this; Round 2 added an "Honest acknowledgements" section reconciling.*
