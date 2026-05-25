# P-21 — Paraphrase divergence primitive

**Dispatch tier.** per-primitive (designed-system).
**Claimed by.** [GF-M (Regime A Phase-2 paraphrase divergence; substrate consequence in §1.3)](../tracks/greenfield-methodology-first.md#13-the-methodologysubstrate-derivation-what-the-cycle-requires).

## Contract restatement

The paraphrase-divergence primitive exposes a typed `paraphrase_and_score(intent_block, N, family_policy) -> [Paraphrase × N, divergence_report]` call. Given one intent / requirement / spec fragment, it dispatches **N parallel paraphrasers across distinct model families** (Anthropic / OpenAI / Google / Mistral / open-weights are canonical families per F46), each driven by a **deterministic prompt-paraphrase generator** (seeded Jinja2 templates varying register, framing, and explicit-vs-implicit articulation without changing semantic content), and returns N paraphrases plus a **divergence report** measuring inter-paraphrase distance (cosine over sentence-transformer embeddings as the substrate default; assertion-graph overlap as the typed-semantic alternative). Partition discipline: refuses calls whose `family_policy.required_distinct` cannot be satisfied by live providers; refuses to return a verdict without recording all N paraphrases plus seeded template IDs immutably (so verdicts are reproducible); carries no methodology opinion on what divergence threshold means "underspecified" — that decision is methodology-layer (GF-M Regime A Phase-2 escalates to operator at semantic disagreement).

## Construction path

**Primary tool: LiteLLM proxy as the multi-provider parallel-dispatch substrate, Jinja2 with deterministic seeded macros as the prompt-paraphrase generator, and sentence-transformers (`all-mpnet-base-v2`) cosine similarity as the divergence-measurement layer.** LiteLLM's `Router` with `model_group_alias` keys an `N-paraphraser` group across provider families (Anthropic + OpenAI + Google + Mistral); `acompletion` with `asyncio.gather` realises parallel dispatch in one round-trip. Deterministic prompts are Jinja2 templates with a registry of `(register, framing, articulation_style)` triples; the substrate carries a seeded RNG that picks N distinct triples per call so variation is reproducible from `(template_id, seed)`. Divergence uses `sentence-transformers` to embed each paraphrase and returns mean / min / max plus the pairwise cosine-distance matrix. **Integration sentence:** LiteLLM's `Router.acompletion` over a tagged `model_group` plus `asyncio.gather` realises N-parallel-family dispatch in one substrate call, and the sentence-transformers cosine matrix realises divergence-as-a-typed-output — together they discharge GF-M's §1.3 requirement that "N model-family-diverse paraphrasers callable in parallel" be a substrate primitive rather than agent-layer composition.

**Alternative tool: Hugging Face `text-generation-inference` clusters for open-weights paraphrasers + native SDKs for closed providers, composed behind a typed dispatcher.** Integration sentence: a `ParaphraseDispatcher` class registers per-family adapters, `asyncio.gather` parallelises the N calls, and `scipy.spatial.distance.pdist` on embeddings produces the divergence matrix.

**Prior art reference.** The multi-provider parallel-dispatch shape is the same machinery as P-14 judge router ([P-14 §Construction path](P-14-judge-router.md#construction-path)) with a different output contract.

## F37 MCC-ceiling engagement

GF-M's [OQ-T6](../tracks/greenfield-methodology-first.md#7-open-questions-surfaced-by-this-track) names the paraphrase-divergence MCC (Matthews Correlation Coefficient) ceiling vs [F37](../failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) as a Phase-8 lean-eval candidate. Construction above is commodity; what is **not** commodity is the calibration question: **how high must N be, and what divergence-threshold is meaningful** for the multi-paraphraser configuration to actually beat the single-judge MCC ≤ 0.55 ceiling Larbi measured. The corpus does not measure the multi-paraphraser case. This is a **calibration-level research-grade-uncertainty flag** — the primitive is buildable today; whether its output is trustworthy as an F37 mitigation is open. Substrate consequence: N, family policy, and divergence metric must be first-class configurable parameters so Phase-8 lean-evals can sweep them.

## Corpus-why citation

GF-M's Regime A explicitly requires this primitive as the **cycle's defense against F37** ([greenfield-methodology-first §1.1 step 2](../tracks/greenfield-methodology-first.md#11-regime-a--spec-discovery-the-malleable-phase)): rather than relying on a single LLM judge (Larbi MCC ≤ 0.55, disqualifying), GF-M detects contradiction by behavioural disagreement across paraphrasers. Empirical anchor: [F37](../failure-modes-v3.md#f37--silent-contradictory-prompt-collapse) (Larbi arXiv:2507.20439v1; GPT-4 Pass@1 drops 73.8% → 6.7% on contradictory HumanEval prompts). The primitive also supports GF-M's K=5 prompt-paraphrase robustness bar ([report 09 §5.5](../../../research/09-jaymin-book-harnesses-practices-mental-models.md)) — paraphrase divergence *is* the K-sample test, computed in-cycle at no separate-audit cost.

## Research-grade-uncertainty flag

**Calibration-level only.** Construction is commodity multi-provider dispatch + commodity embedding-distance — no research-grade gap in *building*. Open empirical questions: (i) how many paraphrasers (N) are required for divergence to exceed the single-judge MCC ceiling against F37; (ii) which divergence metric (embedding cosine vs assertion-graph overlap vs LLM-judge-rated semantic-equivalence) best predicts true contradiction; (iii) how divergence thresholds should be set per intent class. Flagged as Phase-8 lean-eval candidates per GF-M OQ-T6, not buildability blockers.

## Buildability verdict

**`designed-system`.** The multi-provider parallel-dispatch + seeded-prompt + embedding-distance ingredients are commodity; the designed-system content is the family-policy registry, the deterministic prompt-paraphrase generator (seeded template variation preserving semantic content), the typed divergence-report envelope, and immutable-log integration for reproducible calibration sweeps. Registry: Medium. Calibration is the open question, not construction.
