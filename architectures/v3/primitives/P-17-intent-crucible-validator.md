# P-17 — Intent Crucible validator

**Claimed by.** [GF-C §1 + §3](../tracks/greenfield-cold-start-first.md) (primitive #1; typed-object intake capturing the human's day-0 intent; authoring is human-only, substrate provides template + validator + version-control).

**Dispatch tier.** per-primitive (designed-system).

## Contract restatement

A typed-object intake for a single Intent block keyed by a **9-field schema** from [`research/14-el-kaim`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3 — fields verbatim from [GF-C §1](../tracks/greenfield-cold-start-first.md): **identity, statement, business outcomes, capability scope, policy references, invariants, non-goals, decision seeds, guardrails, feedback sources** (GF-C lists ten labels for a 9-slot schema because guardrails + feedback sources sometimes fold into one "operational-bindings" field). Three surfaces: (1) **schema-validate**(blob) → `(parsed_block, [violations])` — required fields present, type-correct, with cross-field invariants (`non-goals ∩ capability-scope = ∅`; each invariant cites a policy reference; each decision seed names its deferral target); (2) **submit**(block, author_id) → versioned commit to the RSI Ledger ([P-18](index.md)) with HMAC so the bench ([P-11](index.md)) binds scenarios to a frozen Intent version; (3) **diff**(va, vb) → typed diff for Council + version-control. Nothing reaches Council, bench, or downstream cycle without passing it.

## Construction path

Build with **Pydantic v2**: one `IntentBlock` root model with nine sub-models, each carrying declarative constraints (`Literal[...]` for enums like risk-class; `AnyUrl` for policy URIs; `conlist(..., min_length=1)` for required lists; `Annotated[str, StringConstraints(...)]` for text bounds). **Integration sentence:** Pydantic v2's `@model_validator(mode='after')` is the exact API for cross-field rules — one validator on `IntentBlock` runs non-goals/scope disjointness, invariant→policy referential-integrity, and decision-seed deferral-target checks, raising `ValidationError` with per-rule violation locations the caller renders as authoring feedback. **JSON Schema export** is free via `IntentBlock.model_json_schema()`, giving Council subagents, bench-builders, and downstream stages one cross-language contract. `invariants` and `statement` delegate form-checks to [P-16](P-16-ears-gtwr-linter.md). **Intake-form filling** uses **Anthropic/OpenAI structured outputs** (Claude `tool_use` or GPT `response_format={'type':'json_schema'}`) against that same schema, so Council clarifying passes propose well-formed candidate field values for human accept/edit.

## Per-field validator difficulty assessment

The 9 fields split into three strata:

- **Fully deterministic (5).** `identity` (enum + UUID + author), `policy references` (URI + registry-resolvability), `non-goals` (string-list + scope disjointness), `decision seeds` (`{question, deferral-target, owner}` records), `guardrails` (enum-keyed: rate limits, cost ceilings, kill-switches). Pure Pydantic.
- **Deterministic via P-16 (2).** `invariants` (EARS form + GtWR R7/R8/R9) and `statement` (GtWR vague-term / escape-clause / open-ended).
- **LLM-assisted-judging required, open question (2).** `business outcomes` (whether *measurable* and *plausibly attributable* — F41/F50-class semantic judgment, not deterministically decidable) and `capability scope` (whether *bounded* enough that non-goals disjointness is meaningful). The validator presents the *structural* check deterministically and **defers substance to the Council pass** (GF-C §3 sub-phase A — family-diverse model interrogation). Open question: *can a substrate-resident judge ensemble produce a stable plausibility verdict on these two fields, or must substance-check ride the human-in-the-loop Council surface?* The [greenfield pre-mortem](../bias-guards/phase-3/greenfield/pre-mortem.md) names this gap as an "intent-richness probe" and proposes it as DPG-10 / Phase-5 wave-1 ADR — surface unresolved at sketch time.

## Corpus-why citation

**GF-C OQ-6** ([§5 q.6](../tracks/greenfield-cold-start-first.md)) — operator-intent-illiteracy is GF-C's biggest unresolved exposure; this validator is the *only* substrate-resident structural defense. **F41** ([`failure-modes-v3` §5a](../failure-modes-v3.md), Under-Defined-Intent Debt, greenfield `critical`) — code syntactically correct but poorly thought-out because intent was never disciplined; the 9-field schema *is* the discipline. **F50** (§4a, architecture/spec confusion in typed objects) motivates the cross-field rules keeping the Crucible from absorbing architectural decisions. **Prior-art:** [`research/14-el-kaim`](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §3 ships the 9-field block as a worked authoring template; this primitive mechanizes it. Cross-anchored to [`research/25`](../../../research/25-requirements-engineering-foundations.md) §3 (INCOSE GtWR C1–C15) for invariants (via P-16).

## Research-grade-uncertainty flag

`partial` — the **structural validator** (7 fields fully + 2 EARS-delegated form checks) is commodity Pydantic + JSON Schema. The **substance-check surface for `business outcomes` and `capability scope`** is research-grade-uncertain: no construction is known that deterministically distinguishes "form-correct + substance-thin" from "form-correct + substance-rich" intent, and the pre-mortem walks the 18-month thin-intent failure cascade this gap produces. The validator-as-built ships without this surface; an intent-richness probe is a Phase-5/6 design problem flagged here, not solved.

## Buildability verdict

**`designed-system`** — Pydantic + JSON Schema + cross-field validators + P-16 delegation is commodity shape; **design content** is (a) the 9-field type-decomposition, (b) the cross-field rules (non-goals/scope disjointness, invariant→policy referential integrity, decision-seed deferral-target), and (c) the structured-output integration letting Council propose well-formed candidate field values to the human. Matches index.md. The substance-check gap is an open question, not a research-grade verdict on the primitive as a whole — *structural* contract is fully buildable today.
