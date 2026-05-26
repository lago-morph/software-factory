# ADR 0016: P-14 judge router

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a)

## Context

Four candidates claim P-14 (judge router) as a load-bearing substrate primitive: [GF-S/S6](../../architectures/v3/tracks/greenfield-substrate-first.md#1s6--judge-routing-multi-shape-model-family-tagged-substrate-typed), [BF-M (Stage 6 cross-family review)](../../architectures/v3/tracks/brownfield-methodology-first.md), [U-A (escrow-interval judge diversity)](../../architectures/v3/tracks/unified-A.md), and [U-B (per-layer judge routing)](../../architectures/v3/tracks/unified-B.md). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-14-judge-router.md) verdicts the primitive `designed-system` — provider abstraction and tagged routing are commodity, but the family-taxonomy registry, judge-shape typing rules, and holdout-handle enforcement are load-bearing design content.

The forcing failure mode is [F46 — Single-Model Review Blindspot](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) (greenfield **high**, brownfield **high**), with the broader [F1/F27/F46/F48 correlated-error cluster](../../architectures/v3/failure-modes-v3.md) as the design target. The router must enforce *distinct-family-required* policies mechanically (not by agent discipline, which would be F53-fragile) and must reject calls whose declared judge-shape mismatches the prompt-template's registered typed I/O signature.

## Decision

**Build P-14 on [LiteLLM Router](https://docs.litellm.ai/docs/routing) as the provider-abstraction substrate, with (a) a Postgres-backed capability registry mapping `(judge_role × provider × model_family) → eligibility`, (b) per-judge-role [Pydantic](https://docs.pydantic.dev/) typed input/output schemas enforced on every call, and (c) builder-family exclusion computed at routing time so a builder agent in the active cycle cannot also serve as that cycle's judge.** The substrate exposes a single `judge(shape, judge_role, prompt_template_id, input, holdout_ref) → TypedVerdict` call surface. The `judge_shape` tag (`same-model-different-task` / `same-model-different-role` / `cross-model-different-task` / `cross-family`) selects a `model_group_alias` whose `tags` carry family identifiers; LiteLLM's tag-routing + `fallbacks` machinery refuses to land a call back inside the originating family when `judge_shape: cross-family` is declared. Typed output uses provider-native structured-output (`response_format={"type": "json_schema", ...}`) validated against the role's Pydantic `BaseModel` on return; type-mismatch is a router-level rejection, not a downstream parse error. The router does not pick a shape — methodology does; the router types the choice, logs it immutably, and enforces the typing.

## Alternatives considered

**B. Bespoke router (hand-rolled provider dispatch + retry + tag logic).** *Why rejected:* re-invents LiteLLM Router's tag-routing, fallback policy, and structured-output passthrough — features that are mature, multi-provider-tested, and maintained externally. A bespoke router would carry the same family-exclusion code paths LiteLLM already exposes, plus the maintenance cost of keeping per-provider SDK shims current. See the [P-14 construction path](../../architectures/v3/primitives/P-14-judge-router.md#construction-path).

**C. [LangChain `LLMRouter`](https://python.langchain.com/docs/how_to/routing/) as the substrate.** *Why rejected:* LangChain's router is content-routing-oriented (route by input semantics to a destination chain) rather than provider-family-policy-oriented; typed input/output shape support is thinner than LiteLLM's per-provider `response_format` passthrough, and tag-based exclusion of an originating family is not a native concept. The substrate would need to layer family-exclusion logic on top of LangChain's content router — i.e., reintroduce most of option B's bespoke work.

## Consequences

**Easier:** F46 mitigation becomes substrate-enforced — methodology layers consume `judge(shape='cross-family', ...)` and trust the substrate to land the call on a non-originating-family provider. The four claiming candidates' family-diversity requirements are met by one substrate. Typed envelopes per judge role surface schema drift at the router boundary, not in downstream verdict consumers.

**Harder:** the Postgres capability registry needs operational discipline — model-family eligibility entries must be kept current as providers add/retire models. Builder-family exclusion requires the router to know the cycle's active builder identity (passed as a call-time argument from the orchestration layer); this is one extra contract on the caller.

**Explicitly NOT promising — P-33 stays DISTINCT.** Per the [Phase-4.2 overlap verdict](../../architectures/v3/primitives/overlap.md#p-33-vs-p-14--opposing-side-router-vs-judge-router): "**DISTINCT primitives** despite shared underlying tool. Both use LiteLLM Router at the construction layer, but: **P-14 (judge router)** is a *router over LLM judge endpoints* with provider-family-diverse routing and typed input/output shapes per judge role. The handler universe is LLM judges (with optional deterministic-judge inclusion as a degenerate case). **P-33 (opposing-side router)** is a *router over the full opposing-side handler universe* — LLM judges (with unconditional builder-family exclusion), deterministic checkers (Python predicates), named-human approvers, population votes. The router's load-bearing value-add is the *exclusion logic* (three-layer denylist: call-time computed + LiteLLM tag-exclusion + registry family-allowlists) and the *kind-dispatch logic* (FC-shaped: routes by `refutation-attempt.method`). P-14 → P-33 is NOT a generalization-specialization relationship at the substrate level; the routers have different *contract surfaces*. A deployment could share LiteLLM Router infrastructure but the routing-policy layer is per-primitive." D7-U-1's *do-not-unify* discipline rests on this distinction; collapsing the two would lose it. A separate Wave-5.1 ADR covers P-33's routing-policy contract.

**Explicitly NOT promising:** multimodal structured-output guarantees across families. Per the [P-14 sketch RGU flag](../../architectures/v3/primitives/P-14-judge-router.md#research-grade-uncertainty-flag), typed-output shape for vision-bearing artifacts judged cross-family may be best-effort. Substrate flag, not a buildability blocker.

## References

- [P-14 buildability sketch](../../architectures/v3/primitives/P-14-judge-router.md) — full construction path, corpus-why citation, per-candidate notes.
- [Phase-4.2 overlap verdict on P-33 vs P-14](../../architectures/v3/primitives/overlap.md#p-33-vs-p-14--opposing-side-router-vs-judge-router) — DISTINCT-primitive verdict quoted verbatim in Consequences.
- [F46 — Single-Model Review Blindspot](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) — forcing failure mode.
- Substrate-requirements summaries claiming P-14: [GF-S](../../architectures/v3/substrate-requirements/gf-s.md), [BF-M](../../architectures/v3/substrate-requirements/bf-m.md), [U-A](../../architectures/v3/substrate-requirements/u-a.md), [U-B](../../architectures/v3/substrate-requirements/u-b.md).
- [ADR 0015: P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — Wave-5.1a exemplar this ADR mirrors in shape.
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.1a binding-rule-table source.
