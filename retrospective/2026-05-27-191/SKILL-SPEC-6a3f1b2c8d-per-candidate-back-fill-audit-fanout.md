# Spec: `per-candidate-back-fill-audit-fanout`

- **ID**: SKILL-SPEC-6a3f1b2c8d
- **Source retrospective**: ../2026-05-27-191.md

## Intent

When a project has accumulated a body of "prior art" (archived synthesis material, superseded architectures, previous-version designs) AND has a current candidate set (specs, designs, ADR-bound primitives) that's supposed to have either absorbed or deliberately rejected each piece of prior art, the per-candidate-back-fill-audit-fanout skill produces an independent audit of every (prior-art-item × candidate) cell. It surfaces silent absorption (the candidate carries the substance but didn't cite it), explicit rejection (with reason), structural inapplicability, and genuine gaps. Phase 7 of the v3 architecture synthesis ran this pattern at scale: 9 archive files × 10 candidates ≈ 945 cells of record, fanned out across 9 per-candidate subagents + 2 bias-guard subagents in one concurrent wave.

## Trigger

Direct user phrases:
- "audit X against archived Y per candidate"
- "back-fill audit"
- "what's in the archive that didn't make it into the current set?"
- "check for silent absorption from prior work"

Proactive triggers (offer the skill unprompted when):
- The project plan names a "back-fill" or "prior-art audit" phase.
- The project has just closed a per-candidate spec-authoring phase AND has an archive directory the specs were supposed to engage with deliberately.
- A user asks "did we lose anything from the old version?" after a synthesis pivot.

Negative triggers (do NOT use this skill when):
- The audit is single-candidate (no fanout justified — just author one notes file inline).
- There is no archive — the project has nothing prior to audit against.
- The audit is content-rework, not citation-rework (this skill produces *audit* artifacts, not patches; spec patches are a separate, conditional follow-up).

## Inputs

At invocation the skill receives:
- A canonical candidate set (e.g., the 10 v3 specs at `architectures/v3/specs/<id>.md`).
- An archive scope, enumerated as a finite file list (Phase-7: 9 files across two directories + one top-level pre-v3 plan).
- A classification taxonomy. Phase-7 used 4 tokens: `absorbed | rejected (reason) | not-applicable-to-candidate-mandate | tbd`. The taxonomy is project-specific; the 4-token shape is the recommended default.
- A bias direction. Phase-7 used "be generous toward archive items" per [00-brief-v3 OQ-B10](architectures/v3/00-brief-v3.md), because archive-and-rebuild discipline has a known recency-bias-against-archive weakness.
- Known-rejected v3 items (if any) that MUST classify `rejected (verbatim verdict text)` regardless of be-generous bias. Phase-7: OpenHands+Overstory substrate stack; Compound Atelier as baseline.
- A dispatch brief skeleton (`auto-NNN`) following the project's decision-brief precedent.

## Outputs

The skill produces:
- One per-candidate notes file per candidate (Phase-7: `architectures/v3/backfill-notes/<id>.md` × 10). Each file carries YAML frontmatter (with self-check results + exemplar-budget-flag if applicable), a §1 lineage statement, a §1.5 prior-phase-defaults verification subsection, §2..§N per-archive-file audits (with §N.0 file header + §N.1 enumeration + §N.2 classification table + §N.3 notes), §summary, §references.
- Two bias-guard audit files (`audit-silent-absorption.md` + `audit-historian.md`) fired concurrent with the per-candidate fanout.
- One lead-agent-authored aggregation matrix (`backfill-notes.md`) that views the audit cross-candidate.
- Optionally: conditional spec-patch PRs (Wave 7.3 in Phase-7 — but NOT fired by default; see [the matrix-flag-over-spec-patches ADR draft](./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md) for the decision pattern).
- One close handoff document carrying the next-phase entry posture + any deferrals.

## Workflow

1. **Author a dispatch brief (`auto-NNN`)** with two rounds of real adversarial review per [`AGENTS-MD-d72e1a4f3c`](AGENTS.md#adversarial-review-must-be-real-subagents). Round-1 reviewers from core angles (pre-mortemer / cost-hawk / regulator); Round-2 reviewers from different angles (naive-newcomer / scoping-skeptic / historian-prior-art). Pre-fold the prior `auto-(NNN-1)`'s amendments per [`AGENTS-MD-4a7c2e9f6b`](AGENTS.md#adversarial-review-amendment-inheritance).
2. **Pre-author one exemplar inline** per [`AGENTS-MD-eec503a3c2`](AGENTS.md#exemplar-before-parallel-uniform-schema-fanout). Pick a candidate with the clearest single-lineage assignment so the §1 template is mechanically reproducible. Run self-check (a)-(g) on the exemplar; document any budget overrun in an `exemplar-budget-flag:` YAML block.
3. **Dispatch (N-1) per-candidate workers + 2 bias-guards concurrent** in one parallel wave. Each worker writes to its candidate's notes file; bias-guards write to fixed audit filenames. All return ≤500-word digests; the file is the deliverable, not the return text.
4. **At fanout-close, author the aggregation matrix** with cross-candidate views + bias-guard reconciliation. Apply the precedence rule + confidence threshold per [`AGENTS-MD-5b3e8a1c2f`](AGENTS.md#silent-absorption-confidence-threshold) — only high-confidence bias-guard findings override per-candidate verdicts; medium triggers `tbd`; low is informational. Per-candidate `not-applicable-to-candidate-mandate` is NEVER overridden.
5. **Decide the spec-patch question.** If per-candidate-patch fire-count would exceed the deferral threshold AND a bias-guard's recommendations name a matrix-flag alternative, adopt the matrix-flag-only path per [`AGENTS-MD-7d9c4e1b3a`](AGENTS.md#matrix-flag-over-spec-patches) — document the decision inline in the aggregation file. Otherwise, fire the conditional spec-patch sub-wave.
6. **Write the close handoff** carrying the next-phase entry posture + load-bearing inputs the next phase must honor (cite obligations, reconciliation TBDs, historian load-bearing gaps).

## Concrete examples

### Example 1: Phase-7 back-fill audit (actual session)

- **Candidates**: 10 v3 architecture specs (GF-S, GF-M, GF-C, BF-S, BF-M, BF-L, U-A, U-B, U-C, D7-U-1) at `architectures/v3/specs/<id>.md`.
- **Archive**: 9 substantive files (~33K total words) across `archive/synthesis-v1-v2/` + `archive/architectures-v2/` + `archive/research-plan.md`.
- **Dispatch brief**: `architectures/v3/decisions/auto-007-phase-7-dispatch-shape.md` — Round 1 returned 3 × `accept-with-named-amendments`; Round 2 returned 3 × `accept-with-named-amendments`. No Round 3.
- **Exemplar**: lead-agent-authored `backfill-notes/bf-s.md` at 5698 words (Light tier 5000; flagged with `exemplar-budget-flag` documenting +14% overrun root cause).
- **Wave**: 9 per-candidate workers + 2 bias-guards = 11 subagents in one wave. All returned `accept-as-is` or `accept-with-named-amendments`.
- **Aggregation**: `architectures/v3/backfill-notes.md` carries the cross-candidate matrix + bias-guard reconciliation + Wave-7.3 decision.
- **Wave-7.3 decision**: NOT FIRED (matrix-flag + Phase-8 cite-obligation per silent-absorption auditor recommendation #5).
- **Result**: Phase 7 closed in 6 PRs against the 15-PR cap; 0 morning-review items required; Phase-6-followup carry-forwards #1/#2/#3 all closed in-run.

### Example 2: How the §1.5 D-1..D-7 verification surfaced explicit challenges

Round-1 of `auto-007` instructed all per-candidate subagents to skip D-1..D-7 (the v3 Round-1/Round-2 defaults inherited from `archive/synthesis-v1-v2/ARCHIVE.md`) as "already-inherited material." Round-2 Reviewer 5 (scoping-skeptic) and Reviewer 6 (historian) independently caught this: `archive/synthesis-v1-v2/ARCHIVE.md` line 18 explicitly says *"Defaults are not invariants — every Phase-2 track must mark each as `accepted with justification` or `challenged`."* Reviewer 6 then `grep`-ed the BF-L spec and confirmed: BF-L's §4 discipline binding explicitly challenges D-1 (substrate-displaces-spec) AND D-2 (scenarios-from-model, not out-of-tree) AND partially D-3.

The Round-2 fix added §1.5 to every per-candidate notes file: a mechanical `grep`-based verification of each D-default against the candidate's spec content, with one of 4 verdict tokens per default. The fanout surfaced 5 explicit-challenge findings across BF-L, BF-M, BF-S, U-C, D7-U-1 — every one of which would have been silently mis-classified as `absorbed (v3 default D-N)` under the Round-1 blanket-skip.

## Anti-patterns

- **Blanket-skip prior-phase defaults.** Phase-7 Round-1 brief told per-candidate subagents to skip D-1..D-7 as "already-inherited." This violated the per-candidate engagement principle and would have hidden BF-L's explicit challenges. Use §1.5 verification instead; see [`AGENTS-MD-2f8a6c9d51`](AGENTS.md#per-candidate-engagement-over-blanket-skip).
- **Speculative lineage mappings in the dispatch brief.** Phase-7 Round-1 brief Glossary suggested `GF-S~A4 tournament-flavored`, `GF-M~A1 refinery-flavored`, etc. Reviewer 6 (historian) demonstrated these contradicted the candidate-registry content (GF-S has zero tournament lineage). Delete speculative mappings; instruct each subagent to derive lineage from candidate-registry verbatim cites.
- **Bias-guards-after-fanout.** Wastes a full fanout's wall-clock and tempts the auditor to inherit per-candidate verdicts (loses independence-of-read). Fire bias-guards concurrent when input streams are independent per [the bias-guards-concurrent ADR draft](./ADR-3f8c1e5b7a-bias-guards-concurrent-with-fanout.md).
- **Sub-fanning bias-guards by archive file.** The historian's value is cross-file pattern detection ("zero specs touch this item") which requires all archive files in one head. Sub-fanning destroys the property.
- **Firing 4+ spec patches by default when threshold-breached.** Triggers the Phase-N-followup deferral mechanism — which is the wrong tool for citation gaps. See [the matrix-flag ADR draft](./ADR-b4e7c2a9d6-matrix-flag-over-spec-patches.md).

## Acceptance criteria

- [ ] Each candidate produces a notes file at the canonical path with all required sections (§1, §1.5, §2..§N per archive file, §summary, §references) and self-check-results YAML.
- [ ] Bias-guard subagents fire concurrent (not after) with the per-candidate fanout when input streams are independent.
- [ ] The aggregation file applies the silent-absorption precedence rule with confidence-threshold gating; per-candidate `not-applicable` cells are not overridden.
- [ ] No spec patches fire when matrix-flag alternative was named by an audit subagent AND patch-count would exceed the deferral threshold.
- [ ] Close handoff names the next-phase load-bearing inputs the audit produced (cite obligations, TBDs, historian gaps).

## Files this skill creates / modifies

- `architectures/v3/decisions/auto-NNN-<phase>-dispatch-shape.md` — the dispatch brief.
- `architectures/v3/backfill-notes/<candidate-id>.md` × N — per-candidate notes files.
- `architectures/v3/backfill-notes/audit-silent-absorption.md` — bias-guard.
- `architectures/v3/backfill-notes/audit-historian.md` — bias-guard.
- `architectures/v3/backfill-notes.md` — lead-agent aggregation matrix.
- `architectures/v3/SESSION-HANDOFF-<UTC-DATE>-phase-N-close.md` — close handoff.
