# ADR 0048: BF-L P-13 maintenance loop

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3b subagent — BF-L orphan ADR)

## Context

[BF-L](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md) is defined as three loops over a single durable [Codebase Model (P-26)](../../architectures/v3/primitives/P-26-codebase-model.md): Loop 1 ingestion, Loop 2 per-cycle query, Loop 3 maintenance. P-13 names the third loop. Per the [Phase-3.5 buildability sketch for P-13](../../architectures/v3/primitives/cluster-C3.md#p-13--maintenance-loop-continuous-reconciliation) the substrate engineering is `commodity` (cron + reconciliation worker + diff), but the *binding policy content* — what signals trigger a maintenance cycle, how regions are prioritized, which downstream substrate fires on a drift event — is BF-L-specific and not addressed by the commodity verdict.

Per the [overlap analysis](../../architectures/v3/primitives/overlap.md#orphan-claimed-by-1-candidate-16-primitives), P-13 is a BF-L orphan (no other candidate claims it). Per the [substrate-requirements summary §3](../../architectures/v3/substrate-requirements/bf-l.md#§3-candidate-specific-contracts-on-each-primitive), BF-L runs the cadence on the Codebase Model itself (delta-version ingestion + reconciliation + [F34 cross-layer drift](../../architectures/v3/failure-modes-v3.md) detection). Per [ADR 0026 the three-loop discipline](./0026-discipline-three-loop.md#decision), the maintenance loop is the canonical **per-codebase cadence** (distinct from per-cycle and per-session); the discipline binds methodologies to declare each loop's substrate touchpoints, escalation policy, and evidence-retention horizon. P-13 is BF-L's per-codebase declaration. The forcing failure modes are [F34 (cross-layer drift)](../../architectures/v3/failure-modes-v3.md), [F55 (behavioural drift)](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop), and [F57 (design-authority erosion)](../../architectures/v3/failure-modes-v3.md), plus [F20 (maintenance-vs-greenfield asymmetry)](../../architectures/v3/failure-modes-v3.md) which the loop directly operationalises.

## Decision

**Build P-13 as a cron-driven cycle inspector that polls the Codebase Model (per [ADR 0047 P-26 integrated six-view artifact](./0047-p-26-codebase-model.md)) for drift signals, prioritizes affected regions, and triggers BF-L maintenance cycles via the [ADR 0036 P-30 event-registrar substrate](./0036-p-30-event-registrar-substrate.md).** Concretely:

- **Cadence.** Per-codebase, not per-cycle — per [ADR 0026](./0026-discipline-three-loop.md#decision) the loop runs on the slow axis (default: nightly inspection, weekly full reconciliation; per-deployment-tunable per the three-loop discipline's deliberate non-promise on cadence values).
- **Drift signals (three classes).** (1) **Test-coverage decay** — the runtime view of P-26 reports per-region coverage; the inspector flags regions whose coverage delta exceeds a per-region threshold since the last reconciliation. (2) **Runtime telemetry anomalies** via the [ADR 0014 P-07 telemetry ingestor](./0014-p-07-telemetry-ingestor.md) — error-rate spikes, latency shifts, exception-class introductions on previously-stable code paths. (3) **Churn cadence shift** — the historical view reports per-region commit frequency; a region whose churn rate changes materially (e.g. >2σ from its rolling baseline) is flagged regardless of coverage or telemetry.
- **Per-region prioritization.** Flagged regions are ranked by composite weight = drift-signal magnitude × debt-cluster membership (debt view of P-26) × Caremark/RSI exposure tag (debt+structural views). Regions with declared [RSI-track](./0044-p-18-rsi-declaration-ledger.md) work or Caremark tags are surfaced first; pure-coverage decay on commodity regions is rate-limited.
- **Cycle triggering.** The inspector does not run reconciliation work itself. It emits typed `maintenance-trigger` events to [P-30 event-registrar substrate](./0036-p-30-event-registrar-substrate.md), carrying region-ID + drift-signal-class + priority weight + reconciliation-budget; the BF-L methodology's maintenance-cycle handler subscribes and dispatches a per-region reconciliation cycle that re-ingests deltas, refreshes the affected P-26 views, and emits attribution per [ADR 0035](./0035-p-24-attribution-store.md).
- **Evidence-retention horizon.** Per-codebase loop trajectories (drift-event log + triggered-cycle outcomes) retained for the codebase's lifetime, not per-session, per [ADR 0026 §Decision](./0026-discipline-three-loop.md#decision).

## Alternatives considered

**B. Human-operator-driven maintenance schedule** — operators decide when to re-ingest and reconcile; the substrate provides only the reconciliation worker on demand. *Why rejected:* does not scale beyond a single team holding the codebase model in working memory. BF-L's load-bearing claim is that the model is the *durable* artifact methodology reasons over (per the [BF-L track §1](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md)); leaving drift-detection to operator vigilance reintroduces exactly the [F20 maintenance-vs-greenfield asymmetry](../../architectures/v3/failure-modes-v3.md) the loop exists to defeat. Also incompatible with [ADR 0026's binding declaration](./0026-discipline-three-loop.md#decision) that per-codebase cadence be a first-class loop with declared substrate touchpoints, not a discretionary stage cost.

**C. Event-driven only — no scheduled inspection** — the loop fires only when other substrate (commits, deploys, telemetry alerts) raises an event. *Why rejected:* misses **slow-burn drift between events**. Coverage decay and conventional-view drift are precisely the failure shapes that accumulate silently between observable events (no commit fires when a test silently goes stale; no deploy fires when a code region's idiom diverges from the codebase convention). The [cluster-C3 sketch's construction path](../../architectures/v3/primitives/cluster-C3.md#construction-path) explicitly names the loop as a *low-cadence continuous job* over a *re-ingestion sample*, not an event handler. A hybrid is the correct shape — the cron inspector is the scheduled half; P-30 events are the dispatch half.

## Consequences

**Easier:** BF-L's per-codebase cadence is concretely substrated; [F20](../../architectures/v3/failure-modes-v3.md) / [F34](../../architectures/v3/failure-modes-v3.md) / [F55](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop) defences are mechanical, not aspirational. Per-region prioritization aligns maintenance budget with debt-cluster + RSI/Caremark tags, so the loop's cost stays proportional to where the methodology already declares attention is owed. The [ADR 0036 P-30 event-registrar](./0036-p-30-event-registrar-substrate.md) gives the loop a uniform dispatch surface — other substrate consumers (per-session trajectory store, per-cycle judges) can subscribe to the same `maintenance-trigger` events for cross-loop awareness.

**Harder:** The drift-signal thresholds (coverage delta, telemetry anomaly, churn σ) are deployment-tunable and the [BF-L track §7 OQ-3](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md) flags maintenance-loop cadence calibration as a Phase-8 lean-eval candidate. Per-region prioritization weights need empirical calibration against real codebases — the formula here is a documented starting shape, not a derived optimum.

**Explicitly NOT promising:** the *specific* cadence values (nightly vs weekly vs on-trigger) or the *specific* drift thresholds. Per [ADR 0026's non-promise](./0026-discipline-three-loop.md#consequences), those live at architecture-spec / per-deployment time. This ADR fixes the **shape** of the loop (cron inspector + three signal classes + P-30 dispatch + debt-weighted prioritization), not the **values** of its tuning knobs.

## References

- [P-13 buildability sketch (cluster-C3 § P-13)](../../architectures/v3/primitives/cluster-C3.md#p-13--maintenance-loop-continuous-reconciliation)
- [BF-L substrate-requirements summary § P-13](../../architectures/v3/substrate-requirements/bf-l.md#§3-candidate-specific-contracts-on-each-primitive)
- [BF-L track (three-loop architecture)](../../architectures/v3/tracks/brownfield-legacy-ingestion-first.md)
- [ADR 0026: three-loop discipline](./0026-discipline-three-loop.md#decision) — names per-codebase cadence
- [ADR 0047: P-26 Codebase Model](./0047-p-26-codebase-model.md) — the drift target read by the inspector
- [ADR 0036: P-30 event-registrar substrate](./0036-p-30-event-registrar-substrate.md) — the dispatch surface for `maintenance-trigger` events
- [ADR 0014: P-07 telemetry ingestor](./0014-p-07-telemetry-ingestor.md) — runtime anomaly signal source
- [F34 / F55 / F57 cross-cycle drift cluster](../../architectures/v3/failure-modes-v3.md) and [F20 maintenance asymmetry](../../architectures/v3/failure-modes-v3.md) — forcing failure modes
- [overlap.md § orphan list](../../architectures/v3/primitives/overlap.md#orphan-claimed-by-1-candidate-16-primitives) — BF-L P-13 orphan classification
