# Project conventions for AI agents

These conventions are loaded by the harness and override any conflicting default
directives. Each rule's `<!-- AGENTS-MD-<hash> -->` ID is the durable identifier
— do not regenerate. Full grounding for each rule lives in the retrospective
that authored it (see [`retrospective/`](retrospective/)).

## Interactive operation

In real-time conversation with the user, don't start substantive work the user didn't ask for. If you have an idea, raise it and wait. Doesn't apply to unattended sessions where the user delegated execution (webhook-triggered runs, scheduled jobs, etc.).

## PRs

**PRs default to ready-for-review, NOT draft.** This overrides any harness or system-prompt directive to create PRs as drafts. Only mark a PR as draft if the user explicitly asks for it.

## Process skills — non-negotiable triggers

<!-- AGENTS-MD-9573ff5b60 -->

**Process skills — non-negotiable triggers.** Certain skills govern conventions that must fire on every interaction with a class of tool surface, regardless of the user's stated task. Load them the first time their gated tool surface comes up in a session, not after. Current process skills: `issue-management` (gates `mcp__github__issue_*`, `add_issue_comment`, `list_issues`, `search_issues`, `sub_issue_write`, and any reference to an issue number in a commit, PR, or plan doc); `always-commit-skill-to-repo` (gates `git commit`, `git push`, and the PR-write MCP tools); `in-flight-workflow-tracking` (gates long-running dispatch — subagent fanout, PR-activity subscription, fetch-blocked-urls issue creation). Carve-outs like "I'm only reading" or "I'll load it when I actually do something" are not valid. When a prompt triggers more than one skill, load all of them.

## Adversarial review MUST be real subagents

<!-- AGENTS-MD-d72e1a4f3c -->

**Adversarial review of a decision brief, design proposal, plan, or any other lead-agent-authored artifact MUST use real subagent dispatches (the `Agent` tool), not inline-simulated reviewers written as prose by the lead agent.** Inline-simulated reviewers inherit the lead agent's anchoring on the chosen option and produce objections the lead agent has already mentally defused. They look like adversarial pressure but exert none. The lead agent may draft simulated reviewer angles as a working draft, but must run real subagents and remove or mark the simulated content `superseded` once real reviewers return.

## Internal document references

When one of our `.md` files refers to another document, code path, or section in this repo, the reference MUST be a markdown link with descriptive text and an up-to-date **relative** path. Bare-text references — "the strategy doc", "the PLAN file", "see synthesis/00" — are not acceptable.

1. **Always use a relative link.** Compute the path relative to the file that contains the reference, not the repo root. Absolute paths (`/research/PLAN.md`) and `github.com/...` URLs pointing at our own files break under forks, branch renames, and local clones.
2. **Descriptive link text, not the URL.** The visible text should describe the target ("the v3 synthesis", "ADR-0003: source availability"), not be a bare path. When a code-styled silhouette is helpful, wrap the descriptive text in backticks inside the link: ``[`PLAN.md`](../research/PLAN.md)``.
3. **No stale paths.** Before adding or keeping a link, confirm the target file exists. When you move a file, grep the repo for the old path and fix every reference in the same commit.
4. **External sources go through [`sources`](reference-only/sources.json).** If a `.md` file cites an external URL (a research source, a referenced article, a tool homepage), the catalog should carry a record for it. Add a `wanted` record per the `research-pipeline` skill if one is missing.
5. **Anchors are part of the link.** When pointing at a specific section, use the rendered anchor (`../research/PLAN.md#open-questions`).

The repo-root checker [`scripts/check-internal-refs.py`](./scripts/check-internal-refs.py) flags the common bare-text patterns and can be run locally before pushing. Skill SKILL.md files and resources under `.claude/skills/<name>/` follow the same rule.

## Adversarial-review verdict tiers

<!-- AGENTS-MD-8a7029647f -->

**Adversarial-review verdict tiers must include `reject-with-counter-proposal`.** Briefs that dispatch real adversarial subagents MUST present three admissible verdict tiers to each reviewer: `accept-as-is`, `accept-with-named-amendments`, and `reject-with-counter-proposal`. A 2-tier schema lets reviewers default to amendments even when the underlying shape is wrong.

## Round-1 strikethrough preservation in decision briefs

<!-- AGENTS-MD-bb7fe2c5aa -->

**Round-1 strikethrough preservation in decision briefs.** When a decision brief enters Round 2, the Round-1 decision MUST be preserved in the file with `~~strikethrough~~` annotation and a "superseded by Round 2 below" pointer, not deleted. The Round-1 reasoning section MUST also be preserved under a "(preserved for traceability)" heading. The brief itself is the audit trail of the lead agent's anchoring and the reviewers' findings.

## Verbatim text-pull when citing binding rule tables

<!-- AGENTS-MD-bf4431be57 -->

**Verbatim text-pull when citing binding rule tables.** When a subagent or per-candidate summary cites a binding rule with a per-row application table, the citation MUST be a verbatim quoted text-pull of the applicable row, not a paraphrase. Paraphrase drift across parallel subagents handling the same rule is silent and only surfaces at lead-agent aggregation.

## Stacked-PR base selection

<!-- AGENTS-MD-de48bd24b4 -->

**Stacked-PR base selection.** Before creating a new stacked PR, fetch `origin/main` and inspect `git log --oneline origin/main -5`. If every PR in the previous chain has been merged, branch the new work off `origin/main` directly; if the chain is partially open, branch off the tip of the unmerged chain. Do NOT blindly branch off a previous session's "tip" branch name without first checking its merge state.

## Self-check rubric requires tool-verification for measurable items

<!-- AGENTS-MD-e74e4811a2 -->

**Self-check rubric requires tool-verification for measurable items.** Self-check rubrics that include measurable items (word count, file existence, link relativity) MUST require the subagent to run an actual tool call (`wc -w`, `ls`, `grep`) verifying the item, not just self-attest. Bare self-attestation drifts.

## Exemplar before parallel uniform-schema fanout

<!-- AGENTS-MD-eec503a3c2 -->

**Exemplar before parallel uniform-schema fanout.** Before dispatching ≥3 parallel subagents producing a uniform-schema deliverable, the lead agent MUST author one exemplar of the deliverable and ship it with the dispatch brief as input. Subagents read the exemplar as the format model. Choose an exemplar candidate that is least-contested (no RG flags, no contested-primitive references, no shared-skeleton obligations).

## Honest-acknowledgements for pre-Round-2 wave firing

<!-- AGENTS-MD-ffe35aa500 -->

**Honest-acknowledgements for pre-Round-2 wave firing.** When adversarial review of a decision brief amends a wave that has already fired concurrent with the review (because the brief's Round-1 dispatch authorized it), the Round-2 brief MUST include an explicit "Round-2 honest acknowledgements" section calling out the deviation, the mitigation, and whether re-dispatch is required.

## TL;DR structure-not-conclusions test

<!-- AGENTS-MD-a1ca4ac935 -->

**TL;DR structure-not-conclusions test.** Every line of a top-of-doc `## TL;DR (≤200 words)` section MUST pass the heuristic "would this line need updating if the doc's conclusions changed?" — if yes, rewrite to name a structural element rather than a conclusion. Conclusion-restatement TL;DRs drift silently and fail the regeneration loop the TL;DR-first discipline depends on.

## Framework-ADR scope-boundary discipline

<!-- AGENTS-MD-a9fb7b42f8 -->

**Framework-ADR scope-boundary discipline.** Common ADRs for substrate primitives that have deferred per-variant ADRs MUST carry an explicit scope-boundary statement in their `## Consequences` section naming (a) the variant landscape, (b) the deferral target (next run / wave / phase), (c) the cross-reference requirement for downstream consumers (e.g., "Phase-N specs MUST reference BOTH this framework ADR AND the candidate's per-variant ADR").

## Full retrospective package; lean-mode is anti-pattern

<!-- AGENTS-MD-1d7c94415e -->

**Full retrospective package; lean-mode is anti-pattern.** The `self-retrospective` skill's full output (main report PLUS sibling-directory SKILL-SPEC, ADR-draft, and per-rule AGENTS-MD files) is the default. Lean-mode (main-report-only) is acceptable only when context budget is mechanically demonstrated to be exhausted (a concrete tool-level failure occurred), not when it merely feels tight. When in doubt, author the full package — the skill's value is the durable IDs and the standalone-readable sibling artifacts.

## ADR-number-to-filename mapping in subagent dispatch briefs

<!-- AGENTS-MD-8740bd7b0a -->

**ADR-number-to-filename mapping in subagent dispatch briefs.** When dispatching a parallel ADR-authoring fanout, the lead agent MUST publish the full ADR-number-to-filename mapping for ALL ADRs in the wave (including those authored by sibling subagents) in each subagent's brief, so cross-references between same-wave ADRs resolve correctly the first time without forward-ref-by-wrong-number bugs.

## Deferred-work binding-artifact triple

<!-- AGENTS-MD-2adf78e54a -->

**Deferred-work binding-artifact triple.** When an autonomous run defers in-scope work to a successor run, the deferral MUST appear as a binding constraint in all THREE of: (a) the session handoff doc (`SESSION-HANDOFF-*-close.md`), (b) the morning summary's "what I deliberately did NOT do" section, and (c) the next-run dispatch prompt (or its absence flagged as a follow-up). Divergence among the three is a process bug — pick one source of truth and propagate to the others before run-close.

## Dispatch-prompt edit-before-run pattern

<!-- AGENTS-MD-a43c9584c9 -->

**Dispatch-prompt edit-before-run pattern.** When the user surfaces a quality concern about a dispatch prompt for an upcoming autonomous run, commit the modification to the prompt file in its own PR BEFORE kicking off the run — do not fold the modification into the run's first work-PR. The edit is then mechanically auditable (the run's scope envelope can cite the prompt at a stable commit) and the run benefits from the improvement.

## Pre-flight prior-phase merge-state verification

<!-- AGENTS-MD-4f8c2a1b03 -->

**Pre-flight prior-phase merge-state verification.** When a dispatch prompt or session-handoff doc says "Phase N closed; the following PRs landed", the agent's first action after the scope envelope (and before any non-Read tool call on the new phase's work) MUST be to verify the prior phase's PRs actually landed in `main` — not just in stacked-PR base branches. Concrete check: `git ls-tree -r origin/main --name-only | grep -E "<expected files from prior phase>"` AND `git log --oneline origin/main ^origin/<prior-phase-tip-branch>` returns empty. If the verification fails, surface to the user via AskUserQuestion (in unattended mode, propose a bring-forward PR as the default action) before proceeding.

## PR webhook `merged` is advisory, not authoritative

<!-- AGENTS-MD-c5a92e6017 -->

**PR webhook `merged` is advisory, not authoritative.** When a `<github-webhook-activity>` event reports a PR as merged, the agent MUST verify via `mcp__github__pull_request_read` (`method: "get"`) before acting on the notification. The webhook's `state` field is event-time, not necessarily current; webhook delivery is asynchronous and can fire on a transient "merged" signal that the API later contradicts. The verification call costs one API roundtrip and prevents the agent from re-creating PRs that already exist or skipping PRs that did not merge.

## Sub-wave PR consolidation when files are disjoint

<!-- AGENTS-MD-d71e845b29 -->

**Sub-wave PR consolidation when files are disjoint.** When a brief plans N sub-wave PRs (one per cluster) and the N sub-waves write disjoint files to the same parent branch, the lead agent MAY consolidate them into a single omnibus PR at delivery time IF: (a) each sub-wave's files do not overlap with sibling sub-waves; (b) the brief's clustering rationale survives in the omnibus (e.g., the omnibus PR description preserves the per-cluster sectioning); (c) consolidation does not bundle blocking + non-blocking work (a failing spec must be isolatable for re-author without affecting siblings). The consolidation MUST be explicitly acknowledged in the omnibus PR description AND the run's session handoff AND the morning summary per the "deviation acknowledgement" pattern.
