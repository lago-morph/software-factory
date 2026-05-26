# ADR 0013: P-06 watchdog tiers

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.1a)

## Context

P-06 is the three-tier observation-and-control primitive — Daemon, Triage, Patrol — claimed as load-bearing by [GF-S §1.S5](../../architectures/v3/tracks/greenfield-substrate-first.md), [GF-M D-6](../../architectures/v3/tracks/greenfield-methodology-first.md), and [BF-M §4 D-6](../../architectures/v3/tracks/brownfield-methodology-first.md), and inherited implicitly by most other candidates. Per the [Phase-4.2 overlap counts](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage), P-06 is shared by **≥7 candidates** and gets a common ADR in Wave 5.1.

The [Phase-3.5 cluster-C2 sketch](../../architectures/v3/primitives/cluster-C2.md#p-06-watchdog-tiers-daemon--triage--patrol) verdicts P-06 `commodity` *only on the condition that all three tiers exist together and escalate up the chain*. The composition discipline is the load-bearing design content; each tier individually is uncontroversial.

The forcing failure modes are tier-specific:

- **Daemon** mitigates process-death and stuck-but-not-dead conditions (resource-cap breach, OOM, wall-clock blowout) — substrate hygiene with no semantic load.
- **Triage** is the structural detector for [F22 (zombie agents)](../../architectures/v3/failure-modes-v3.md#f22--zombie-agents) and [F23 (stalled-vs-thinking)](../../architectures/v3/failure-modes-v3.md#f23--stalled-vs-thinking-ambiguity) — the semantic question "is this agent stalled or thinking?" no Daemon-tier check can answer.
- **Patrol** mitigates the cross-cycle drift cluster: [F8 stale-knowledge inversion](../../architectures/v3/failure-modes-v3.md#f8--stale-knowledge-inversion), [F55 behavioural drift](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop), [F57 design-authority erosion](../../architectures/v3/failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes), and (U-C / D7-U-1 variants) F47 Goodhart gaming. Patrol is also the last-mile defender against [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) — without escalation, observability alone leaves the drift unmitigated.

## Decision

**Build P-06 as three composed tiers with typed escalation events flowing up the chain on the coordination medium (P-10):**

1. **Daemon = systemd-cgroups + per-cycle resource limits.** A per-cycle sidecar supervisor enforces cgroup resource caps (CPU, RAM, wall-clock, FD count) and polls `/proc/<pid>/stat` plus the [P-05 trajectory](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture) log's last-event timestamp at 1 Hz. Cap breach or stuck-state emits a typed `daemon.escalate` event.
2. **Triage = signal-handler → operator notification (Slack / PagerDuty webhook).** A substrate-resident LLM judge consumes `daemon.escalate` events plus a fixed-cadence trigger, takes `{recent_trajectory_window, current_tool_invocation, elapsed_since_last_event}`, and emits `{stalled, thinking, escalate}`. `escalate` invokes the operator-notification handler (Slack/PagerDuty webhook with cycle ID, tier, evidence pointer); cross-family routing is inherited from [P-14 judge router](../../architectures/v3/primitives/overlap.md#p-14--p-33--judge-router--opposing-side-router).
3. **Patrol = cron-driven cycle inspector emitting typed alerts.** A `systemd.timer` (or Airflow/Prefect job) runs at hours cadence, reads the trajectory store across many cycles, applies deterministic distribution checks (KL-divergence of action distributions, monotone-trend tests on judge-agreement, signed-rank tests on cycle-cost), and emits typed `patrol.drift` alerts on threshold breach. Patrol is statistical, not LLM-based, *exactly because* it checks for drift that LLM-based detectors are themselves subject to.

Each tier's escalation surface is a typed event on the coordination medium; higher tiers consume lower-tier output. The three tiers must deploy together — partial deployment is rejected at substrate-init time.

## Alternatives considered

**B. External APM-only watchdog (Datadog / New Relic / Sentry).** A managed observability product would cover process metrics and offer alerting webhooks. *Why rejected:* APM products operate at host or container granularity, not per-cycle. They cannot bind escalations to the cycle ID that [P-05](../../architectures/v3/primitives/cluster-C2.md#p-05-trajectory-capture) uses for crash-resume and forensic reconstruction, so a Triage signal cannot reach back into trajectory context. They also have no analogue for the LLM-judge Triage tier — APM alerting fires on numeric thresholds, not the semantic stalled-vs-thinking question that F22/F23 require.

**C. Pure observability (Prometheus + Grafana alerts) without escalation.** Scrape metrics, set alert rules, render dashboards; rely on operators to read them. *Why rejected:* this leaves [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) unmitigated — drift detected on a dashboard nobody is currently watching is drift not acted on. The [Schillace Letter 7 framing](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift) explicitly names non-agent-shaped workflow as a *cause* of F40; an observability layer without typed escalation is exactly that. The escalation chain (Daemon → Triage → Patrol → operator) is the load-bearing content, not the metric collection.

## Consequences

**Easier:** F22/F23 get a structural detector rather than relying on operator vigilance. F8/F55/F57 get a periodic statistical check that does not itself drift (Patrol is deterministic). Process-level safety (OOM, runaway cost) is enforced before it cascades. The composition discipline is mechanically checked at substrate-init — a deployment missing a tier fails fast.

**Harder:** Three separate operational surfaces (systemd-cgroups config, judge prompt + routing, cron+stats job) must coexist. Patrol-tier threshold authoring is a judgement call per deployment (what KL divergence on action distributions counts as drift?) and will need tuning. Triage-tier judge cost is non-zero — every escalation invocation is an LLM call.

**Explicitly NOT promising:** the *same-vs-distinct* verdict on Patrol-tier checks across candidates. U-C's distance-keyed Patrol reads [P-32 distance estimator](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage) tuples; D7-U-1's Patrol reads independence-auditor outputs. The three-tier *shape* is uniform; the *Patrol-tier evidence stream* is per-candidate and is recorded in candidate-specific ADRs at Phase 5 Wave 5.3.

## References

- [P-06 buildability sketch (cluster-C2)](../../architectures/v3/primitives/cluster-C2.md#p-06-watchdog-tiers-daemon--triage--patrol)
- [Phase-4.2 overlap counts (P-06 shared by ≥7)](../../architectures/v3/primitives/overlap.md#2-primitive-overlap-counts-by-candidate-coverage)
- [GF-S §1.S5 watchdog requirement](../../architectures/v3/tracks/greenfield-substrate-first.md), [GF-M D-6](../../architectures/v3/tracks/greenfield-methodology-first.md), [BF-M §4 D-6](../../architectures/v3/tracks/brownfield-methodology-first.md)
- Failure modes: [F22 zombie agents](../../architectures/v3/failure-modes-v3.md#f22--zombie-agents), [F23 stalled-vs-thinking](../../architectures/v3/failure-modes-v3.md#f23--stalled-vs-thinking-ambiguity), [F40 last-mile drift](../../architectures/v3/failure-modes-v3.md#f40--last-mile-drift), [F55 behavioural drift](../../architectures/v3/failure-modes-v3.md#f55--behavioural-drift-self-reference-loop), [F57 design-authority erosion](../../architectures/v3/failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes)
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave-5.1a context
