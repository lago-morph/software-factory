# ADR 0041: GF-M P-21 paraphrase divergence primitive

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3a subagent (GF-M orphan)

## Context

[GF-M (Greenfield, methodology-first)](../../architectures/v3/tracks/greenfield-methodology-first.md) is the sole candidate claiming [P-21 paraphrase divergence](../../architectures/v3/primitives/P-21-paraphrase-divergence.md) — a GF-M-orphan primitive per the [GF-M substrate-requirements summary § P-21](../../architectures/v3/substrate-requirements/gf-m.md#1-primitive-list-buildability-confirmed). The [Phase-3.5 buildability sketch](../../architectures/v3/primitives/P-21-paraphrase-divergence.md#buildability-verdict) verdicts the primitive `designed-system` — multi-provider parallel dispatch and embedding-distance are commodity; the family-policy registry, the deterministic seeded prompt-paraphrase generator, and the typed divergence-report envelope are load-bearing design content.

The forcing failure mode is [F37 — Silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md) (Larbi arXiv:2507.20439v1; single-judge MCC ≤ 0.55, disqualifying as a stand-alone contradiction detector). GF-M's Regime-A spec-discovery cycle defends against F37 by **behavioural disagreement across model-family-diverse paraphrasers** rather than a single LLM judge ([greenfield-methodology-first §1.1](../../architectures/v3/tracks/greenfield-methodology-first.md)). The substrate must (a) dispatch N paraphrasers in parallel across distinct provider families, (b) generate paraphrases from deterministically seeded templates so calibration sweeps are reproducible, and (c) emit a typed divergence report so methodology can gate intent-promotion on threshold rather than agent-discipline (which would be F53-fragile).

## Decision

**Build P-21 by reusing [ADR 0016 P-14 judge-router](0016-p-14-judge-router.md)'s LiteLLM Router substrate with a `paraphrase-role` token, configured for N=3–5 paraphrasers spanning Anthropic / OpenAI / Google model families and called concurrently via `Router.acompletion` + `asyncio.gather`.** Prompt variation is realised by a Jinja2 seeded-macro registry of `(register, framing, articulation_style)` triples; `(template_id, seed)` reproduces the exact paraphrase set. Divergence is measured by **pairwise cosine distance over Sentence-BERT (`all-mpnet-base-v2`) embeddings**, returned as a typed `DivergenceReport` (mean / min / max + full pairwise matrix) plus all N paraphrases and seeded template IDs persisted immutably. Threshold gating (what counts as "underspecified") is methodology-layer per GF-M Regime-A — the substrate emits the signal and refuses to verdict-without-recording.

`N`, family policy, divergence-metric, and threshold are **first-class configurable parameters** so [Phase-8 lean-eval](../../architectures/v3/substrate-requirements/gf-m.md#5-open-carries) can sweep them against the F37 / MCC-0.55 ceiling per GF-M's [OQ-T6](../../architectures/v3/tracks/greenfield-methodology-first.md#7-open-questions-surfaced-by-this-track).

**Cost-multiplier flag.** Per-cycle paraphrase fan-out is an Nx multiplier on every reversible-commitment cycle in Regime-A. [ADR 0020 — cost-ceiling discipline](0020-discipline-cost-ceiling.md) binds GF-M's Phase-6 architecture spec to pre-declare this multiplier in the per-regime cap-table, not to handle it as exceptional. The substrate exposes per-call token / dollar telemetry through the same [P-02 cost-ceilings](../../architectures/v3/primitives/cluster-C1.md) enforcement surface the router uses; methodology authors the cap.

## Alternatives considered

**B. Single-model paraphrasing (one provider, N temperature-varied samples).** *Why rejected:* defeats the divergence purpose. F37's empirical anchor is *correlated within-family failure modes* (Larbi MCC ≤ 0.55 measured on single-model judges); the F37 defense GF-M Regime-A relies on is exactly that *cross-family* disagreement uncorrelates the contradiction-detection error. A single-model N-sample paraphrase set inherits the family's biases and the divergence signal collapses to within-temperature-band noise. See [P-21 § Corpus-why citation](../../architectures/v3/primitives/P-21-paraphrase-divergence.md#corpus-why-citation).

**C. Ensemble vote (majority among N paraphrasers).** *Why rejected:* wrong output shape. Regime-A uses **divergence as the signal** — disagreement *is* the evidence that the intent is underspecified, triggering operator escalation. An ensemble-vote primitive emits consensus and discards exactly the disagreement Regime-A needs. The two are not interchangeable typed contracts: vote returns `Verdict`, divergence returns `DivergenceReport`. See [P-21 § Contract restatement](../../architectures/v3/primitives/P-21-paraphrase-divergence.md#contract-restatement).

## Consequences

**Easier:** GF-M's F37 defense is substrate-typed rather than agent-composed. The infrastructure cost of P-21 is near-zero given [P-14](0016-p-14-judge-router.md) already deploys LiteLLM Router — the family-policy registry is shared, only the `paraphrase-role` token and divergence-measurement layer are new. The seeded-template registry makes Phase-8 lean-eval sweeps reproducible from `(template_id, seed, N, metric, threshold)`.

**Harder:** per-cycle cost rises Nx; GF-M's Phase-6 architecture spec MUST pre-declare this in the per-regime cap-table per [ADR 0020](0020-discipline-cost-ceiling.md). Operational discipline on the family-policy registry (keeping live-provider eligibility current) is shared with P-14 but doubles the importance of registry hygiene.

**Explicitly NOT promising:** that paraphrase divergence actually clears the F37 / MCC ≤ 0.55 ceiling. Construction is commodity; **calibration is the open empirical question** — whether N=3–5, cosine-over-Sentence-BERT, and any chosen threshold actually beat the single-judge MCC ceiling is unmeasured in the corpus and carried as a Phase-8 lean-eval per [OQ-T6](../../architectures/v3/tracks/greenfield-methodology-first.md#7-open-questions-surfaced-by-this-track). This is a calibration-level research-grade-uncertainty flag, not a buildability blocker (per [GF-M substrate-requirements §2](../../architectures/v3/substrate-requirements/gf-m.md#2-rg-primitives)).

## References

- [P-21 paraphrase-divergence buildability sketch](../../architectures/v3/primitives/P-21-paraphrase-divergence.md) — construction path, corpus-why citation, RGU calibration flag.
- [GF-M substrate-requirements § P-21](../../architectures/v3/substrate-requirements/gf-m.md#3-candidate-specific-contracts-on-each-primitive) — N ≥ 3 cross-family contract; first-class parameterization for Phase-8 sweeps.
- [F37 — Silent contradictory-prompt collapse](../../architectures/v3/failure-modes-v3.md) — Larbi MCC ≤ 0.55 forcing anchor.
- [GF-M § OQ-T6](../../architectures/v3/tracks/greenfield-methodology-first.md#7-open-questions-surfaced-by-this-track) — Phase-8 lean-eval candidate for paraphrase-divergence-vs-F37 MCC ceiling.
- [ADR 0016: P-14 judge router](0016-p-14-judge-router.md) — LiteLLM Router substrate reused here under a `paraphrase-role` token.
- [ADR 0020: cost-ceiling discipline](0020-discipline-cost-ceiling.md) — Nx fan-out multiplier MUST appear in GF-M's Phase-6 per-regime cap-table.
