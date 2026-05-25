# Discipline: Watchdog-tier escalation (Daemon / Triage / Patrol)

Three substrate-resident watchdog tiers monitor at different cadences and escalate by typed event: **Daemon** (substrate, seconds) — heartbeat, resource caps, liveness, detects process death; **Triage** (substrate-resident AI judge, seconds-to-minutes) — *"is this agent stalled or thinking?"*, detects zombie agents and stalled-vs-thinking ambiguity; **Patrol** (substrate, hours+) — cross-cycle drift detection, escalates to human, detects behavioural drift, design-authority erosion, stale-knowledge inversion. The discipline operationalises D-6 (brief §4.1) and Round-2 C14.

## Named-by

All 10 tracks (`accepted` or `accepted-with-justification` on D-6).

- `GF-S` — full primitive spec including greenfield-specific Patrol-against-invariants framing (no historical baselines yet). [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §1.S5.
- `BF-S` — *"F22 (zombie agents, brownfield-high), F23 (stalled-vs-thinking, brownfield-medium), F56 (guardrail-bypass under stress, brownfield-critical) all require the tiered watchdog."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §4 D-6.
- `BF-L` — *"The watchdog's Triage tier is parameterised by the codebase model (a 'stalled' agent in low-coverage area triggers earlier than in high-coverage area). The Patrol tier checks model drift against codebase reality."* [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §4 D-6.
- `BF-M` — *"All three tiers used: Daemon per-stage, Triage at stages 4/5/6, Patrol across cycles for F34/F54/F55/F57 drift."* [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §4 D-6.
- `GF-M` — Patrol tier is the drift-detection layer for the Regime A → Regime B transition. [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §4 D-6.
- `GF-C` — *"Cold-start has zero historical baseline for Patrol-tier strategic drift detection — Patrol is structurally muted during cold-start because there is nothing for it to compare against. Daemon and Triage operate from cycle 1."* [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §4 D-6.
- `U-A` — *"Daemon = liveness check on the in-flight interval (heartbeat / resource); Triage = AI reclassification of `lights-out` → `escalate` per F22/F23; Patrol = strategic drift detection across interval histories, feeding the AILCCP board-quarterly report (F43 mitigation)."* [unified-A.md](../tracks/unified-A.md) §4 D-6.
- `U-B` — Patrol's primary signal is cross-layer drift (F34) — the pace-layer model makes it natively detectable. [unified-B.md](../tracks/unified-B.md) §4 D-6.
- `U-C` — Patrol monitors the empirical distance distribution to detect F47 Goodhart (gaming the distance estimator). [unified-C.md](../tracks/unified-C.md) §4 D-6.
- `D7-U-1` — *"Daemon/Triage/Patrol map onto FC-monitoring tiers."* The Patrol-tier *independence auditor* is the substrate primitive. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §1.3 primitive 4 / §4 D-6.

## Corpus motivation

- **D-6** — brief §4.1 + [glossary §0](../00-brief-v3.md).
- **Round-2 C14** — the tier-architecture origin.
- **F22 (zombie agents), F23 (stalled-vs-thinking), F34 (cross-layer drift), F54 (goal subversion), F55 (behavioural drift), F57 (design-authority erosion)** in [failure-modes-v3.md](../failure-modes-v3.md).

## Open questions

- **Patrol's reference set varies sharply across tracks.** GF-S guards invariants (no historical baselines on day-0); BF-L guards model-against-reality; GF-C: Patrol structurally muted until graduation; U-B: cross-layer drift; U-C: distance-distribution gaming. Whether Patrol is one discipline or several is unclear.
- **What does Patrol watch when it itself can drift?** U-A §7 OQ-2 (classifier accountability) and D7-U-1 §7 OQ-1 (auditor-of-the-auditor) both surface this — Patrol's own decisions are themselves substrate-typed events, but the auditor's audit trail needs *its own* opposing side.
- **At cold-start, Patrol cannot operate as designed.** GF-C explicitly notes this; the graduation protocol *requires* Patrol-tier baselines to exist before steady-state regime declaration.

## Substrate-enforcement options

- `GF-S` `S5 watchdog tiers` — all three tiers as a single named substrate primitive.
- `BF-S` `S-4 attribution + S-2 dependency graph` as Patrol inputs.
- `BF-L` Patrol against codebase-model drift.
- `U-A` Patrol monitors interval history; tied to AILCCP board-quarterly report (F43).
- `D7-U-1` Independence auditor (Patrol-tier) monitors FC log for collusion patterns.

Disciplines are distinct from primitives.
