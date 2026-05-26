# Spec: `phase-A-fresh-context-verification`

- **ID**: SKILL-SPEC-ad9a173772
- **Source retrospective**: ../2026-05-25-170.md

## Intent

When a stacked-PR Phase ships navigation docs, TL;DR sections, or cross-document linkage changes, dispatch real subagents with fresh context to verify the changes did not silently break semantic meaning, document linkage, or pointer staleness — before declaring the Phase closed. This skill operationalizes the verification step the 2026-05-25 user pre-emptively added to `next-agent-prompt-phase-5.md`. In that run, three parallel fresh-context Explore subagents (semantic-preservation, cross-document linkage, pointer-staleness) caught one real quality issue (the candidate-registry TL;DR's "withdrawn" line restated a policy conclusion). Without the skill, that bug would have shipped to main; with the skill, it was fixed in a single follow-up PR before Phase A closed.

## Trigger

Activate when a Phase or stacked-PR group has produced:

- A new top-level navigation doc (`AGENT-ENTRY.md`, `README.md`, etc.) that other docs will link into.
- TL;DR sections, summaries, or other condensed views of larger docs.
- Skill / SKILL.md or convention file updates that other agents read at session start.
- A renamed or relocated load-bearing doc.

Direct triggers: "verify Phase X", "are the changes safe to merge", "run the verification step", "fresh-context review". Proactive trigger: any stacked PR group whose changes affect navigation, summaries, or cross-document linkage. Negative trigger: changes that touch only one self-contained file with no cross-document consumers (e.g., an isolated ADR draft).

## Inputs

- The branch tip of the stacked PR group (e.g., the last PR's HEAD).
- The list of files modified across all PRs in the group (`git diff --name-only origin/main..HEAD`).
- The repo's `scripts/check-internal-refs.py` (or equivalent link checker).

## Outputs

- Three parallel adversarial-review subagent dispatches (real `Agent` tool calls; no inline simulation per `AGENTS-MD-d72e1a4f3c`).
- A consolidated findings report. If clean: a short "verification clean — no fixes required" note for the next handoff. If findings: a single stacked fix-PR addressing all findings, named per the convention (e.g., `claude/auto-<date>-A5-verification-fixes`).

## Workflow

1. List files modified across the stacked PR group: `git diff --name-only origin/main..<top-of-stack>`. Group by file class (navigation, TL;DR-bearing, linkage-affecting, pointer-target).
2. Compose three subagent briefs in parallel (one Agent tool message, multiple Agent invocations):
   - **Semantic-preservation reviewer** (one per file whose body was substantively edited): "Diff before-vs-after; confirm only the intended additions are present; report any reordering, deletion, or rewording of pre-existing content."
   - **Cross-document linkage reviewer**: "Enumerate every internal markdown link in modified docs + in files that may reference modified docs; confirm each resolves to an existing file/anchor; distinguish pre-existing-broken-on-main from newly-introduced."
   - **Pointer-staleness reviewer**: "grep the repo for bare-text or stale-path references to any file whose canonical role shifted; report findings with file:line + recommended fix."
3. Use `Explore` subagent_type (read-only) for all three. Brief each with the AGENTS.md rule and the file list explicitly. Cap each subagent's return at ~500 words.
4. Read the three return digests. Categorize findings: high-confidence fix needed, judgment-call, false-positive.
5. If zero high-confidence findings: write a one-line "verification clean" note to the next handoff doc; skip the fix-PR.
6. If ≥1 high-confidence finding: branch a fix-PR off the top of the stack; address each finding in one commit; push; open the PR with a body that summarizes the three subagents' reports.
7. Declare the Phase closed only after either the verification reports clean OR the fix-PR is merged.

## Concrete examples

### Example 1: PR A5 fix from 2026-05-25 run

The 2026-05-25 Phase-A run shipped PRs A1–A4 modifying `AGENT-ENTRY.md`, `ARCHITECTURE-V3-SYNTHESIS-PLAN.md`, `architectures/v3/candidate-registry.md`, the `autonomous-run` skill files, and `CLAUDE.md`. The lead agent dispatched 4 parallel Explore subagents (semantic-preservation × 2, cross-document linkage, pointer-staleness). Reports:
- Semantic-preservation on synthesis plan: `clean` — 145 words, only-addition discipline held.
- Semantic-preservation on candidate-registry: `concerns` — TL;DR line "GF → BF continuity matrix is withdrawn per DEC-1.b" restated a policy conclusion.
- Linkage: `clean` — 29 links verified.
- Staleness: `clean` — no stale references.

The single finding produced PR A5 (#164), which rephrased the line to name the structural element (presence of a strikethrough section in the registry) rather than the verdict. 5-minute fix; preserved Phase-A close discipline.

### Example 2: No-finding case (hypothetical)

A run ships AGENT-ENTRY.md only (Phase A1 from the same plan, no TL;DR changes yet). Verification subagents run; all three report `clean`. Lead agent writes "verification clean — no PR A5 needed" in the next handoff and proceeds to Phase B. No fix-PR opened.

## Anti-patterns

- **Inline-simulating the reviewers** instead of dispatching real Agent subagents. The lead agent's anchoring on the chosen wording defeats the verification (per AGENTS.md `AGENTS-MD-d72e1a4f3c`). Always use the `Agent` tool.
- **Using `general-purpose` subagent_type** when `Explore` (read-only) suffices. Verification is strictly read-only; using a write-capable subagent invites accidental edits during the review.
- **Dispatching after merge.** Verification must fire BEFORE the Phase is declared closed. Post-merge "verification" is just a follow-up bug report.
- **Folding fix work into the next Phase's PR.** Keep PR A5 (or its analog) as a single targeted fix PR. Mixing verification fixes into Phase-B work hides the audit trail.

## Acceptance criteria

- [ ] Verification dispatches use `Agent` tool with `Explore` subagent_type, 3 parallel calls in one message.
- [ ] Each subagent's return digest is captured in the consolidated findings note (handoff or fix-PR body).
- [ ] If findings exist, the fix-PR is stacked on the top of the original PR group, not branched off main.
- [ ] The Phase is not declared closed until verification reports clean OR the fix-PR is merged.

## Files this skill creates / modifies

- `<phase-tail-branch>/...-verification-fixes` — new branch + PR if findings exist.
- The handoff doc — a short verification-status note.
- No retrospective sibling artifacts (verification is too tactical to retro-spec on its own; the broader pattern lives in the autonomous-run skill).
