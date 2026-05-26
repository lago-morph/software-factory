# ADR 0042: GF-C P-11 Cold-Start Bench

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: Wave 5.3a subagent (lead-agent dispatch)

## Context

[P-11 — Cold-Start Bench](../../architectures/v3/primitives/cluster-C3.md#p-11--cold-start-bench-hmac-signed-scenario-store) is a [GF-C](../../architectures/v3/tracks/greenfield-cold-start-first.md) orphan primitive — claimed by exactly one candidate per the [overlap registry](../../architectures/v3/primitives/overlap.md#orphan-claimed-by-1-candidate-16-primitives). Per [GF-C substrate-requirements §P-11](../../architectures/v3/substrate-requirements/gf-c.md), the bench is the *only* out-of-distribution signal that exists before code exists on day 0 of a cold-start project (greenfield, no prior spec, no prior corpus, no prior agent trajectory). It underwrites the five-`critical`-F-mode convergence ([F1](../../architectures/v3/failure-modes-v3.md#f1--hallucination-loop) / [F25](../../architectures/v3/failure-modes-v3.md#f25--design-starvation) / [F40](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) / [F41](../../architectures/v3/failure-modes-v3.md#f41--under-defined-intent-debt) / [F46](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot)) GF-C's track-axis defends against.

The [cluster-C3 sketch](../../architectures/v3/primitives/cluster-C3.md#p-11--cold-start-bench-hmac-signed-scenario-store) and [ADR 0015](0015-p-08-scenario-storage-with-runner-contract.md) together pin the *storage + signing + freeze* half of P-11 (HMAC-SHA256 envelope, OPA append-policy gate, `bench-frozen` event). What remains undecided — and what this ADR records — is the **catalog-construction and calibration** half: where the cold-start scenarios *come from*, how they accumulate over time, and how P-11's value as a benchmark is measured. Without this, "the bench" is a typed-object store with no scenarios to anchor.

## Decision

**The cold-start scenarios are stored as a [P-08](0015-p-08-scenario-storage-with-runner-contract.md) partition tagged `scenario.kind=cold-start`, with GF-C owning the catalog content; the bench-runner reuses P-08's runner-API verbatim; scenarios are operator-authored plus community-contributed via pull request against the catalog; and the calibration metric is `% of cold-start scenarios reaching automation-eligible regime by cycle N`.**

Concretely:

1. **Storage = P-08 partition.** Every cold-start scenario is a typed-object entry in P-08's substrate, carrying the `scenario.kind=cold-start` tag alongside the existing `partition: train | holdout` field from ADR 0015. The HMAC-SHA256 envelope + `bench-frozen` event (cluster-C3 P-11 sketch) compose on top of P-08's content-addressed backend — no new storage substrate.
2. **Runner = P-08 runner-API.** The bench-runner is P-08's `read(partition='holdout', scenario.kind='cold-start', judge-role=...) → ScenarioResult` contract from ADR 0015 with a `kind` filter. No P-11-specific runner subprocess.
3. **Authoring = operator + community PRs.** Day-0 scenarios are operator-authored (Kaner-shaped, ≥1 EARS criterion, ≥1 [Intent Crucible](../../architectures/v3/primitives/P-17-intent-crucible-validator.md) invariant binding, per GF-C [§1.2 sub-phase B](../../architectures/v3/tracks/greenfield-cold-start-first.md#12-the-cold-start-methodology--three-sub-phases)). Subsequent scenarios arrive as PRs against the catalog from operators of other cold-start projects; each PR must include the same Kaner+EARS+invariant fields and is gated by [P-19's eligibility-regime classifier](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md) so contributions stay regime-coherent.
4. **Calibration metric = automation-eligible-by-cycle-N.** P-11's benchmark value is reported as `% of catalog scenarios reaching automation-eligible regime within N cycles` (N a published constant per release). This metric is published alongside the bench and re-computed every catalog revision.

## Alternatives considered

**B. Dynamic scenario generation per cycle.** Each cold-start cycle generates fresh scenarios on the fly from operator intent + a generation model, so the bench is never stale and never seen by builders. *Why rejected:* a benchmark whose contents change per cycle is not a benchmark — it cannot anchor cross-cycle trend reporting, cannot be cited in retrospectives, and offers no defense against [F46](../../architectures/v3/failure-modes-v3.md#f46--single-model-review-blindspot) (a single generator's blindspots become the bench's blindspots). The whole point of P-11 is reproducibility of the day-0 anchor; dynamic generation gives that up.

**C. Adopt a commercial / academic cold-start benchmark.** Reuse an existing third-party scenario suite (SWE-bench-class, HumanEval-class) rather than curating our own. *Why rejected:* no surveyed benchmark covers *cold-start* specifically — they all assume a pre-existing codebase or pre-existing spec, which is the precondition cold-start denies by definition (per GF-C [§1.1 ¶3](../../architectures/v3/tracks/greenfield-cold-start-first.md#11-the-five-day-0-primitives-substrate)). SWE-bench instances start from a real repository; HumanEval starts from a function signature. Neither matches the "no prior spec / no prior corpus / no prior trajectory" axis P-11 must measure against.

## Consequences

**Easier:** P-11 inherits ADR 0015's holdout discipline ([F28 mitigation](../../architectures/v3/failure-modes-v3.md#f28--holdout-leakage--acceptance-criteria-seen-by-builders)) at zero substrate cost — `scenario.kind=cold-start` is a tag on the same partitioned store, not a parallel system. The runner-API is uniform with the rest of P-08's consumers, so judge-side tooling needs no P-11-specific code path. Community PR contribution gives the catalog a natural growth path without bench-frozen immutability being violated (new entries land in a successor partition; the frozen partition stays frozen, per cluster-C3).

**Harder:** Catalog curation becomes a sustained GF-C operator commitment — PR review against Kaner+EARS+invariant rubric is a per-contribution cost, and the eligibility-regime gate adds CI surface. The calibration metric requires a stable definition of "automation-eligible regime" (depends on [P-19](../../architectures/v3/primitives/P-19-eligibility-regime-classifier.md)) and a published N; both are config-level decisions left to architecture-spec time.

**Explicitly NOT promising:** the *content* of the day-0 scenarios. This ADR records the storage/runner/authoring/calibration contract; the substantive cold-start scenarios themselves are methodology-layer artifacts authored per GF-C [§1.2](../../architectures/v3/tracks/greenfield-cold-start-first.md#12-the-cold-start-methodology--three-sub-phases) and are not enumerated here. HMAC-key custody (Yubikey vs cloud KMS vs Vault Transit) is also deferred — flagged as a Phase-5 ADR seed in [GF-C substrate-requirements](../../architectures/v3/substrate-requirements/gf-c.md).

## References

- [ADR 0015 — P-08 scenario storage with runner contract](0015-p-08-scenario-storage-with-runner-contract.md) — the substrate this ADR composes on top of.
- [P-11 cluster-C3 sketch](../../architectures/v3/primitives/cluster-C3.md#p-11--cold-start-bench-hmac-signed-scenario-store) — HMAC + freeze-policy half of the primitive.
- [GF-C substrate-requirements §P-11](../../architectures/v3/substrate-requirements/gf-c.md) — contract delta and day-0 process locus.
- [GF-C track §1.1 ¶3 day-0 primitives](../../architectures/v3/tracks/greenfield-cold-start-first.md#11-the-five-day-0-primitives-substrate) and [§1.2 sub-phase B bench construction](../../architectures/v3/tracks/greenfield-cold-start-first.md#12-the-cold-start-methodology--three-sub-phases).
- [Overlap registry — P-11 orphan](../../architectures/v3/primitives/overlap.md#orphan-claimed-by-1-candidate-16-primitives) and [primitives index — P-11 commodity verdict](../../architectures/v3/primitives/index.md).
