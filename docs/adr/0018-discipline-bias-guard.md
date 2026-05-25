# ADR 0018: Discipline — bias guard

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.2)

## Context

Bias-guard / adversarial-review is one of the most heavily cross-referenced disciplines in the v3 corpus. The [disciplines index](../../architectures/v3/disciplines/index.md) lists `D-Bias-Guard` first by claim-strength; the per-discipline write-up at [`disciplines/bias-guard.md`](../../architectures/v3/disciplines/bias-guard.md) names eight tracks that claim it explicitly and motivates it as the single mechanism behind the F1 / F27 / F46 / F48 cascade — *no opposing side was committed to falsifying the output*.

The forcing concern is correlated-error blindspot during high-stakes decision points. Same-model self-review inherits the author's anchoring; single-perspective adversarial review by a lead agent inherits the lead agent's defused-objection set (the [adversarial-review-must-be-real-subagents rule](../../AGENTS.md#adversarial-review-must-be-real-subagents) is grounded in two PRs where inline-simulated reviewers nominally objected but converged on the author's original choice). Without a discipline that *binds named decision points* to persona-diverse subagent dispatch, bias-guard degenerates into voluntary-discipline-fragility per [F53](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class).

Bias-guard sits *between* the substrate routers ([P-14 judge router](../../architectures/v3/primitives/P-14-judge-router.md), [P-33 opposing-side router](../../architectures/v3/primitives/P-33-opposing-side-router.md), [P-34 independence auditor](../../architectures/v3/primitives/P-34-independence-auditor.md)) and the methodology layer: the substrate routers are the **enforcement mechanism** (they type the judge call, exclude builder-family models, audit independence); this discipline is the **methodology contract** that names which decision points trigger fanout, the minimum persona set, and the verdict-tier rules. The 15-persona catalog this discipline operationalizes lives in [`ARCHITECTURE-V3-SYNTHESIS-PLAN.md` §3 Bias-guard catalog](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#3-bias-guard-catalog).

## Decision

**The bias-guard discipline binds every methodology to invoke persona-diverse real-subagent review at named decision points, dispatched through the substrate's judge / opposing-side routers, with a fixed verdict-tier schema.** The named decision points are: (a) architecture authoring, (b) phase-close checkpoints, (c) ADR adoption, (d) lean-eval design. At each, the methodology MUST dispatch ≥3 personas drawn from the [15-persona catalog](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#3-bias-guard-catalog), each as a real subagent (no inline-simulated reviewers per [AGENTS.md](../../AGENTS.md#adversarial-review-must-be-real-subagents)). Each reviewer returns one of three verdict tiers — `accept-as-is`, `accept-with-named-amendments`, `reject-with-counter-proposal` — per the binding [verdict-tier rule](../../retrospective/2026-05-25-155/AGENTS-MD-8a7029647f-adversarial-review-verdict-tiers.md). A 2-tier schema is forbidden because reviewers default to amendments when "reject" is unavailable, masking structural problems.

Methodology layers DECLARE per-cycle bias-guard touchpoints (which cycle stages map to which decision-point class, which persona slate, what triggers a Round-2 dispatch); the substrate ([P-14](../../architectures/v3/primitives/P-14-judge-router.md) / [P-33](../../architectures/v3/primitives/P-33-opposing-side-router.md) / [P-34](../../architectures/v3/primitives/P-34-independence-auditor.md)) PROVIDES the routing, builder-family exclusion, and independence audit; this discipline BINDS them by specifying the contract surface. Independence is **measured, not declared** (P-34 Patrol-tier) — methodologies that assert independence without an audit handle violate the discipline.

Architecture-spec authors (Phase 6) write the per-decision-point persona slate and Round-2 escalation rule for each candidate. Phase-8 lean-evals MUST include a bias-guard pressure-test (e.g., inject a structurally-wrong proposal and verify the persona slate surfaces a `reject-with-counter-proposal`).

## Alternatives considered

**B. Optional bias-guard (encouraged but not contract-bound).** *Why rejected:* this is exactly the [F53 voluntary-discipline-fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) class. Under time-pressure / fatigue / token-budget pressure — the conditions where bias-guard matters most — the voluntary action is the first thing dropped. The [bias-guard write-up](../../architectures/v3/disciplines/bias-guard.md) cites D7-U-1's entire architecture being organized around making this *not* voluntary; eight tracks name bias-guard as constitutive. An optional discipline is a non-discipline.

**C. Single-persona adversarial review (one strong skeptic per decision point).** *Why rejected:* defeats the diversity requirement that motivates the discipline. The F1 / F27 / F46 / F48 cascade mechanism is *correlated* error — a single reviewer, however strong, shares a single set of priors. The 15-persona catalog exists because different personas detect different failure classes (CFO catches cost-stacking; pre-mortemer catches 6-month drift; cross-mandate attacker catches over-generalization). Empirical evidence from the auto-001 / auto-002 / auto-003 decision-brief cycles: each landed at a materially different decision after multiple real adversarial subagents than the lead agent's first draft proposed — and the *kind* of objection that mattered varied across briefs.

## Consequences

**Easier:** Uniform contract surface for every methodology candidate to declare bias-guard touchpoints; Phase-8 lean-evals have a defined pressure-test (inject structurally-wrong proposal, verify `reject-with-counter-proposal` returns). Candidates that already type judge-diversity per-interval (U-A) or per-layer (U-B) inherit the discipline cleanly; D7-U-1's `FalsificationCommitment` typed object becomes the canonical realization.

**Harder:** Each architecture spec carries an explicit per-decision-point persona slate (non-trivial Phase-6 authoring work). Real-subagent dispatch is meaningfully more expensive than inline simulation; methodology shapes that fan out aggressively need to budget for bias-guard cost in their [cost-ceiling table](./0020-discipline-cost-ceiling.md).

**Explicitly NOT promising:** which persona-slate-of-3 is correct for which decision point. This discipline is the contract shape — the persona slate is per-candidate, lives in each candidate's architecture spec, and is itself subject to a phase-close bias-guard pass.

## References

- [Bias-guard discipline write-up](../../architectures/v3/disciplines/bias-guard.md)
- [Disciplines index — `D-Bias-Guard`](../../architectures/v3/disciplines/index.md)
- [15-persona bias-guard catalog (`ARCHITECTURE-V3-SYNTHESIS-PLAN.md §3`)](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#3-bias-guard-catalog)
- [P-14 judge router](../../architectures/v3/primitives/P-14-judge-router.md)
- [P-33 opposing-side router](../../architectures/v3/primitives/P-33-opposing-side-router.md)
- [P-34 independence auditor](../../architectures/v3/primitives/P-34-independence-auditor.md)
- [F53 voluntary-discipline-fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)
- [Adversarial-review verdict-tier rule (AGENTS-MD-8a7029647f)](../../retrospective/2026-05-25-155/AGENTS-MD-8a7029647f-adversarial-review-verdict-tiers.md)
- [AGENTS.md — adversarial review MUST be real subagents](../../AGENTS.md#adversarial-review-must-be-real-subagents)
- [auto-005 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.2 dispatch context.
