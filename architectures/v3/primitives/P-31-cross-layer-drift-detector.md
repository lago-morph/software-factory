# P-31 — Cross-layer drift detector

**Dispatch tier.** per-primitive (research-grade-uncertainty).
**Claimed by.** [U-B Pace-Layered Escrow Factory](../tracks/unified-B.md) (§1 Watchdog; §2.5 F34 coverage; §5.5 silent-failure protection; OQ-PLEF-3).

## Contract restatement

A periodic / on-event-triggered substrate primitive holding typed-object snapshots of every pace-layer artifact (L0 Standards, L1 Architecture, L2 Spec, L3 Plan, L4 Code) and running a **per-layer-pair invariant checker** across each adjacent pair (L0↔L1, L1↔L2, L2↔L3, L3↔L4). On a drift signal it emits a typed `LayerDriftEvent` carrying `(layer-pair, invariant-id, drifted-artifact-handle, severity, recommended-handback-layer)` to the Patrol watchdog (P-06) and to the U-B escrow primitive, which converts the event into an operator handback at the appropriate layer-transition escrow interval. Triggers: Patrol cadence; any commit to an L0–L3 typed object; any L4 builder cycle touching a symbol the dependency graph (P-23) traces to an upper-layer invariant tag. Partition: read-only against artifacts; write-only against its own event log; never edits a pace-layer artifact.

## Construction path

Three candidate constructions, **none of which is buildable today** because the layer-pair invariants are not specified (see §Research-grade-uncertainty below). Sketched anyway so Phase-4 can pick a direction.

**Construction A — Deterministic invariant-DSL + graph-walk checker.** Each L0 standards object declares a machine-readable invariant set (e.g., "every L3 plan node must trace via `derives-from` edges to ≥1 L2 spec section"; "every L4 symbol touched must appear in the L3 plan's `expected-touch` list"). The detector graph-walks the typed-object link graph using a rules engine (OPA or Cedar) with invariants compiled to Rego/Cedar policies and the artifact graph loaded as input data. **Integration sentence:** OPA's `data.invariants.layer_pair.l2_l3.violation` rule evaluated against the typed-object graph returns the violating triples, which the substrate wraps as `LayerDriftEvent` records and posts to Patrol; OPA's bundle API lets L0 standards updates push new invariant policies without redeploying.

**Construction B — LLM-judge cross-layer consistency check.** A judge call via P-14 (cross-family shape) reads the L_i + L_{i+1} artifacts and returns a structured `DriftVerdict {drifted, locations, rationale, confidence}`. **Integration sentence:** LiteLLM's `response_format={"type": "json_schema", "json_schema": DriftVerdict}` plus `model_group=cross-family` gives a typed judge call per layer pair, scheduled once per pair per Patrol cycle.

**Construction C — Hybrid.** Standards-declared invariants run through A; the residue (drift no declared invariant catches) is sampled and routed to B; Patrol policy decides escalation.

## Research-grade-uncertainty

**The load-bearing gap is upstream of the detector: Brier's pace-layer framework does not enumerate per-layer-pair invariants.** Brier (`followup/12-brier-pace-layers`) names the layers and asserts that fast layers innovate while slow layers stabilize, but offers no algorithmic specification of *what* must be invariant between L_i and L_{i+1}. The corpus has fragments — INCOSE GtWR constrains L2 internally; AILCCP controls anchor L0; El Kaim 9-field intent block structures L2 — but none of these are framed as cross-layer invariants the substrate can check. U-B (§5.5) asserts "layer-invariant checks are deterministic, not LLM-judged" but does not supply the invariant set; its examples (GtWR / EARS / AILCCP presence) are intra-layer.

Concretely: a detector that checks "every L3 plan traces to an L2 spec section" is buildable today (Construction A), but that single invariant is a referential-integrity check, not drift detection. The *substantive* pace-layer drift signals (L4 code violating L1 architecture invariants the architecture only describes in prose; L2 spec contradicting an L0 standard expressed as policy not predicate) require invariants **no corpus source has authored**. P-31's contract depends on a Phase-4 *invariant-authoring program* that does not yet exist. U-B's OQ-PLEF-3 implicitly concedes the gap (it asks about cross-instance drift, presupposing per-instance detection works).

A second uncertainty: Construction B's reliability is bounded by the Larbi MCC ≤ 0.55 result for LLM-as-judge semantic divergence (F37), so the LLM-judge fallback cannot rescue Construction A from invariant-spec gaps without inheriting F37's structural unreliability — the F52 *tempting-wrong-hybrid* trap U-B's OQ-PLEF-8 names.

## Falsifiability

The claim "a cross-layer drift detector for the pace-layer stack can be built" is falsified by either: (a) a Phase-4 invariant-authoring effort producing fewer than ~3 non-trivial machine-checkable invariants per layer pair across L0↔L1, L1↔L2, L2↔L3 after a bounded effort budget (~2 expert-weeks) — at which point Construction A degenerates to referential-integrity checking and Construction B inherits F37 unreliability with nothing to fall back on; or (b) empirical evidence from a Construction-C prototype showing the LLM-judge residue catches drift at MCC > 0.55 on a held-out drift-corpus (would falsify F37-bound pessimism and support buildability). Either outcome resolves the research-grade flag.

## Corpus-why citation

Load-bearing failure mode: **[F34 — Cross-layer drift](../failure-modes-v3.md#f34--cross-layer-drift)** (greenfield **high**; brownfield **critical**) — locally-satisfied spec/plan/code that silently violates upper-layer invariants. U-B (§2.5) names F34 as Patrol's primary signal. Secondary: **F52 Tempting-Wrong-Hybrid** (OQ-PLEF-8) — the detector risks being an F52 instance if it deterministically wraps an under-specified invariant set. Tertiary: **OQ-PLEF-1** (layer count is empirical; invariants depend on the chosen count) and **OQ-PLEF-3** (cross-instance drift presupposes per-instance detection works). U-B §1 watchdog + §5.5 silent-failure protection are the candidate-side commitments this primitive must satisfy.

## Buildability verdict

**`research-grade-uncertainty`.** The detector's scaffolding (typed-object snapshots, graph-walk, OPA evaluation, LLM-judge dispatch) is commodity. The detector's *contract* cannot be honored because **the invariants it would check do not exist in the corpus and have not been authored**. Per the registry: "Brier's pace-layer framework is a description, not a tool — needs substrate-side detector implementation" — and the substrate-side implementation needs a methodology-side invariant catalog Phase-3.5 cannot produce. **For U-B to defend P-31 at Phase-4, U-B must commit to an invariant-authoring sub-track: per layer-pair, ≥3 machine-checkable invariants with corpus citations.** Without that commitment, P-31 is an empty primitive whose construction path is real but whose subject matter is undefined.
