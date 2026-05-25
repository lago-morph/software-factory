# Spec: `decision-brief-adversarial-review-lifecycle`

- **ID**: SKILL-SPEC-34dd1d0274
- **Source retrospective**: ../2026-05-25-155.md

## Intent

Author autonomous-mode decision briefs in two rounds: Round 1 is the lead-agent best call with explicit implementation framing of any binding user direction; ≥2 real adversarial subagents review the framing per the AGENTS.md adversarial-review rule; Round 2 incorporates findings with Round 1 preserved (struck-through if rejected) for traceability. Drawn from the auto-001 through auto-004 progression where each Round-2 materially differed from Round 1 because of reviewer findings the lead agent had pre-defused inline. Without this lifecycle, autonomous-mode decision briefs anchor on the lead agent's initial framing; inline-simulated reviewers cannot catch their own author's blind spots.

## Trigger

- Lead agent is about to write a decision brief in an unattended / autonomous session.
- Brief filename pattern matches `auto-NNN-*.md`.
- User says "write a brief", "record this decision", "draft a decision brief".
- Proactive: when the lead agent is making a binding choice that affects multiple downstream files in an unattended run, this lifecycle applies even if user didn't ask for it explicitly.

Negative triggers: interactive sessions where the user is the reviewer; tactical commit-message-scale decisions; decisions the user has explicitly waved through.

## Inputs

- The decision question (user-direction binding choice, framing space, alternatives).
- ≥2 distinct reviewer angles (methodology-purist, cost/scope hawk, scoping-principle skeptic, aggregation-cost auditor, sequencing skeptic — angles drawn from the task's risk surface).
- Repository conventions: AGENTS.md rule on real-subagent review; auto-NNN file naming; relative-link discipline.

## Outputs

- `architectures/v3/decisions/auto-NNN-<kebab-title>.md` carrying Round 1 + adversarial review + Round 2 in one file.
- Adversarial review section preserved with verbatim findings from each reviewer.
- Round 1 decision struck through if rejected; Round 1 reasoning preserved under a "(preserved for traceability)" heading.

## Workflow

1. Number the brief: the next monotonic `auto-NNN` (check existing `architectures/v3/decisions/auto-*.md`).
2. Write Round 1: state the question, alternatives considered, lead-agent decision, downstream impact, rewind point.
3. Identify ≥2 reviewer angles tied to the task's actual risk surface (not generic "skeptic / hawk / advocate"). Example for an RG-primitive choice: methodology-purist + scoping-principle skeptic. Example for a dispatch shape: aggregation-cost auditor + sequencing skeptic.
4. Dispatch the reviewers as real subagents per the AGENTS.md rule. Each reviewer brief MUST present three admissible verdict tiers: `accept-as-is`, `accept-with-named-amendments`, `reject-with-counter-proposal`.
5. Commit Round 1 + push + open PR.
6. When all reviewers return, synthesize findings in a "Adversarial review — Round 1 (real subagents)" section. Preserve verbatim each reviewer's verdict + findings + amendments.
7. Write Round 2 incorporating findings. If any reviewer rejected with counter-proposal, the Round-2 default is to adopt the counter-proposal unless the lead agent has substantive counter-evidence.
8. Strike through Round 1's decision section with `~~strikethrough~~` and an inline "superseded by Round 2 below" pointer. Preserve Round 1's reasoning under a "Round 1 reasoning (preserved)" subheading.
9. If any waves authorized by Round 1 fired concurrent with the review, add a "Round-2 honest acknowledgements" section calling out the deviation + mitigation.
10. Commit Round 2 + push.

## Concrete examples

### Example 1: auto-003 — BF-L per-RG-view choice (this session)

- Round 1: option A (both views → (a) bounded sub-tracks with count-gates "≥20 patterns per language" + "≥5 invariants per language" + parallel research dispatch).
- Reviewers: methodology-purist (returned `reject-with-counter-proposal`) + scoping-principle skeptic (returned `accept-with-named-amendments`).
- Methodology-purist's counter-proposal: option A′ smoke-test-first per view (mirror auto-002 R2 pattern).
- Scoping-skeptic's findings: gate calibration asymmetric with U-B; (b) fallback is fig leaf without methodology-degradation clause; X_UNM_B framing inverted.
- Round 2 adopted A′ + 5 named amendments. Round 1's option A struck through; Round 1 reasoning preserved.

### Example 2: auto-004 — Phase-4 dispatch shape (this session)

- Round 1: per-candidate parallel fanout (Wave 4.1 ×10 + 4.3 ×2 + 4.4 ×2 + serial 4.2).
- Reviewers: aggregation-cost auditor + sequencing skeptic. Both returned `accept-with-named-amendments`.
- Aggregation-cost: schema-enforcement aids needed (exemplar + self-check rubric + required text-pulls + fixed contested-primitive headers).
- Sequencing: missing wave-ownership for BF-L sub-tracks + U-B authoring; Phase-4-close needs decomposition.
- Round 2 added Wave 4.5 (authoring sub-tracks) + Wave 4.6 (decomposed Phase-4 close) + all schema-enforcement aids. Honest acknowledgements section called out Wave 4.3 / 4.4 firing pre-Round-2.

## Anti-patterns

- **Inline-simulated reviewers as a substitute for real subagents.** Explicitly forbidden by AGENTS.md `## Adversarial review MUST be real subagents`. The pattern was deprecated after auto-001 R1 demonstrated its failure mode.
- **Two-tier verdict schema (accept / amendments only).** Lets reviewers default to amendments even when the underlying shape is wrong. The 3-tier schema with reject-with-counter-proposal was load-bearing in auto-003.
- **Round-1 deletion when revising.** Loses the audit trail of lead-agent anchoring. Strikethrough + preserved reasoning IS the audit trail.
- **Pre-defusing reviewer angles inline in Round 1.** Lead agent writes counter-arguments to anticipated objections; reviewers then have nothing to do. The brief should state the decision and reasoning, not pre-litigate.
- **Skipping the honest-acknowledgements section when waves fired pre-Round-2.** The deviation goes silent; future sessions can't reconstruct what happened.

## Acceptance criteria

- [ ] Brief at `architectures/v3/decisions/auto-NNN-<kebab>.md` with monotonic NNN.
- [ ] ≥2 real adversarial subagents dispatched (Agent tool calls, not inline prose).
- [ ] Three verdict tiers offered to each reviewer.
- [ ] Round 1 preserved struck-through if rejected, with reasoning under "(preserved)" heading.
- [ ] Round-2 honest acknowledgements section present if any wave fired pre-Round-2.

## Files this skill creates / modifies

- `architectures/v3/decisions/auto-NNN-<kebab-title>.md` — the brief itself.
- Optionally: stacked PR description referencing Round 1 + Round 2 status.
