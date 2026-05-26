# ADR 0011: P-02 cost ceilings (hard, multi-axis)

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.1a subagent

## Context

P-02 is one of the most broadly-claimed substrate primitives in the v3 corpus: the [Phase-4.2 overlap analysis](../../architectures/v3/primitives/overlap.md) lists P-02 as **claimed by all 10 candidates** (explicitly by GF-S, GF-M, BF-M, implicit-required by the remaining seven). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/cluster-C1.md#p-02-cost-ceilings) verdicts P-02 `commodity`: the kill-not-degrade semantics are uncontroversial once a mediator wraps the model-call surface; the only research-grade content is *which axes to count*, and that question lives in the methodology layer — specifically in the cost-ceiling [discipline ADR 0020](./0020-discipline-cost-ceiling.md).

This ADR is the **substrate-layer enforcement mechanism** referenced by that discipline. ADR 0020 names *which axes matter per regime* and *which breach behaviors* a methodology is contractually obliged to declare; this ADR commits to *how the substrate counts, evaluates, and acts on those caps*. The two ADRs MUST be read together: ADR 0020 without P-02 is a fragile [F53 voluntary-discipline](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) shape; P-02 without ADR 0020 enforces vendor-friendly defaults that no methodology authored.

The forcing failure mode is [F53](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class): if cap enforcement is operator-discipline rather than substrate-resident, every long-running cycle drifts toward unbounded spend. [CTR-E6](../../architectures/v3/contradictions.md) (refusal of CaMeL utility-tax-style graceful degradation) and [CTR-E1](../../architectures/v3/contradictions.md) (observed 10× cost variance — Cherny $100K+/mo vs. independents $500–$5000/day) frame the design space.

## Decision

**Build P-02 as a deny-by-default multi-axis cap evaluator co-located with the LLM-client wrapper and the [P-01 sandbox](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime) supervisor.** Concretely:

1. **Token counting.** Token counts are taken from the upstream provider's `usage` field on each response (Anthropic Messages API `usage.input_tokens` + `usage.output_tokens`; OpenAI-compatible `usage.prompt_tokens` + `usage.completion_tokens`). For *pre-flight* estimation (caps evaluated before dispatch), use the provider's native token-counting endpoint (Anthropic `count_tokens`; OpenAI `tiktoken` for known model families). Estimator drift is treated as an axis-counter error budget, not a free pass.

2. **Call counting.** A counter-middleware in the LLM-client wrapper increments a per-cycle tool-call counter and a per-cycle model-call counter on every dispatch boundary. Counters live in a substrate-resident store (not the cycle's writable filesystem) so an agent cannot reset them.

3. **Wall-clock.** Per-cycle `started-at` is captured at [P-01](../../architectures/v3/primitives/cluster-C1.md#p-01-sandbox-runtime) `launch(cycle-manifest)`. A supervisor process polls elapsed wall-clock against the manifest cap and signals breach via SIGTERM/SIGKILL to the cycle's process group.

4. **Dollar spend.** A per-model unit-cost table (USD per million input/output tokens) is updated weekly by an out-of-band job that scrapes provider pricing pages. Dollar spend is computed at each LLM-call boundary as `tokens × unit-cost`; the table version is recorded in the cycle's trajectory so post-hoc audits can replay the math.

5. **Evaluation point.** The multi-axis cap is evaluated **at each LLM-call boundary** (both pre-flight, against the estimator, and post-response, against the actual `usage`). The wall-clock axis is additionally evaluated continuously by the supervisor. The first axis to breach wins; further axes are not consulted.

6. **Breach handling.** On breach the substrate **aborts the cycle** (kill-not-degrade per CTR-E6) and emits a typed `breach-event` to the trajectory (axis, threshold, observed, table-version). No graceful-degradation, no in-cycle operator override; cap-table edits for future cycles are an out-of-band methodology decision per [ADR 0020](./0020-discipline-cost-ceiling.md).

## Alternatives considered

**B. Proxy-only enforcement (LiteLLM-style HTTP 429).** A reverse-proxy in front of the provider API enforces the cap by returning HTTP 429 when counters exceed the manifest cap. *Why rejected:* the proxy sees one axis (token / dollar derived from `usage`) and cannot evaluate wall-clock or non-LLM tool-call axes without a second supervisor; the resulting two-surface design has more cap-evaluation seams than necessary. The chosen design co-locates *all four* axes in one evaluator at the LLM-client wrapper boundary, with the supervisor handling only the wall-clock continuous case. The proxy shape remains available as a *deployment option* for the LLM-client wrapper but is not the primary contract. See [P-02 sketch construction path](../../architectures/v3/primitives/cluster-C1.md#p-02-cost-ceilings).

**C. Soft caps with operator escalation.** Each axis emits a warning at threshold and continues running, escalating to operator on overage. *Why rejected:* soft caps invite [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) — methodologies hover near the cap accumulating cost over many cycles. Hard kill-not-degrade is mandated by [GF-S §1.S4](../../architectures/v3/tracks/greenfield-substrate-first.md#1s4--cost-ceilings-hard-multi-axis-substrate-enforced) and by [CTR-E6](../../architectures/v3/contradictions.md)'s refusal of CaMeL utility-tax-style hidden cost. The discipline-layer ADR 0020 separately rejected this option on the same grounds. See [ADR 0020 alternatives](./0020-discipline-cost-ceiling.md#alternatives-considered).

## Consequences

**Easier:** All 10 candidates' implicit cost-cap requirement is met by one substrate. Breach-event emission gives the methodology layer a typed signal for cap-table tuning and gives Phase-8 lean-evals a defined pressure-test surface (per [ADR 0020](./0020-discipline-cost-ceiling.md) lean-eval mandate). The single-evaluator design keeps cap-math auditable: one trajectory record carries all four axis counters and the unit-cost table version.

**Harder:** The unit-cost table is a per-deployment maintenance burden (weekly scrape job + version-tracking). Token-count estimator drift between pre-flight `count_tokens` and post-response `usage` introduces a small over-shoot window — the design accepts this rather than gating dispatch on a server round-trip; methodologies sensitive to over-shoot set tighter manifest caps.

**Explicitly NOT promising:** specific cap *values* (per-deployment, authored by the methodology per [ADR 0020](./0020-discipline-cost-ceiling.md)); which axes matter for which regime (methodology decision per ADR 0020); cross-cycle aggregate caps (this ADR is per-cycle only — per-day or per-tenant aggregation is a deployment-ops concern outside the substrate primitive).

## References

- [P-02 buildability sketch in cluster C1](../../architectures/v3/primitives/cluster-C1.md#p-02-cost-ceilings) — Phase-3.5 commodity verdict and construction path
- [Phase-4.2 overlap analysis — P-02 claimed by all 10 candidates](../../architectures/v3/primitives/overlap.md)
- [ADR 0020: Discipline — cost ceiling](./0020-discipline-cost-ceiling.md) — methodology-layer contract that names axes, regimes, and breach behaviors; P-02 is its substrate enforcement mechanism
- [GF-S §1.S4 — substrate-enforced multi-axis ceilings](../../architectures/v3/tracks/greenfield-substrate-first.md#1s4--cost-ceilings-hard-multi-axis-substrate-enforced)
- [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) and [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) — the failure modes P-02 closes
- [CTR-E1 cost order-of-magnitude](../../architectures/v3/contradictions.md) and [CTR-E6 CaMeL utility tax](../../architectures/v3/contradictions.md) — the contradictions framing kill-not-degrade
