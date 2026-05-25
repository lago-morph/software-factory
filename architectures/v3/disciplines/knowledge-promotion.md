# Discipline: Knowledge-promotion / pattern-promotion

Patterns, insights, corrections, and skills accumulated per-cycle are *promoted* through typed gates (provisional → durable; pattern → standard; reversible → frozen-anchor; survived → load-bearing) rather than committed silently. F8 (stale-knowledge inversion) and F55 (behavioural drift / self-reference loop) are the failure modes when knowledge accumulates without explicit promotion gates. Compound-Knowledge's four-way classification (insight / playbook / correction / pattern, followup 11) plus `kw:confidence` tagging is the corpus shape.

## Named-by

- `GF-M` — Regime A's *promote-or-reverse* is the cycle's Phase-4 gate. *"If the probe satisfies the operator's reaction, the intent + scenario pair is promoted from `reversible` to `durable`; otherwise both are reversed (deleted, not amended). Reversal is cheap by design; this is what makes spec-malleable productive rather than paralytic."* [greenfield-methodology-first.md](../tracks/greenfield-methodology-first.md) §1.1 phase 4.
- `BF-S` — *"Knowledge promotion. Decides what becomes a persistent skill / pattern / knowledge entry (Compound-Knowledge-shaped, followup 11 brownfield-primary; Beads `discovered-from` edges from report 38)."* [brownfield-substrate-first.md](../tracks/brownfield-substrate-first.md) §1.2 / §1.3 step 8.
- `BF-M` — knowledge typing (followup 11 four-way) with `kw:confidence`; stale-knowledge handling is *the next reader's obligation*, not a curator daemon. [brownfield-methodology-first.md](../tracks/brownfield-methodology-first.md) §1.2.
- `U-B` — pattern → Skill → enforced standard pace-layer promotion (Brier). Each cycle's repeatable pattern is candidate for promotion to `anchor.kind=standards-rule`. Promotion is an `anchor-edit` work unit (always L4). [unified-B.md](../tracks/unified-B.md) §1 knowledge store + §5 days 7-30.
- `U-C` (`explicit-named`) — *"Pattern → standard promotion (Brier pace-layers, followup 12 §6: 'project doc → Skill → enforced standard'). Each cycle's repeatable pattern is candidate for promotion to `anchor.kind=standards-rule`. Promotion is an `anchor-edit` work unit (always L4)."* [unified-C.md](../tracks/unified-C.md) §5 step 2.
- `GF-C` — graduation protocol promotes work-unit-classes from Cold-Start (L3-Augmentation) to Steady-State (L4-eligible). [greenfield-cold-start-first.md](../tracks/greenfield-cold-start-first.md) §1.3.
- `D7-U-1` — survival-window registrar: when a window expires, downstream artifacts that depended on the expired FC are flagged for re-falsification. [d7-u-1-prohibit-interval-escrow.md](../bias-guards/phase-3/d7-blind-axis/d7-u-1-prohibit-interval-escrow.md) §1.3 primitive 5.
- `GF-S` (`inferable`) — knowledge accumulation deferred to methodology layer per CTR-C3 stance ("methodology evolution as methodology concern"). [greenfield-substrate-first.md](../tracks/greenfield-substrate-first.md) §2.H.
- `BF-L` — Loop-3 maintenance reconciles model with reality; promotion is methodology-side on top of substrate-stored knowledge. [brownfield-legacy-ingestion-first.md](../tracks/brownfield-legacy-ingestion-first.md) §1.

## Corpus motivation

- **Followup 11** — Compound Knowledge plugin (brownfield-primary): typed-learnings four-way classification (insight / playbook / correction / pattern) + `kw:confidence`.
- **F8 (stale-knowledge inversion) / F55 (behavioural drift) / F54 (goal subversion across cycles)** in [failure-modes-v3.md](../failure-modes-v3.md).
- **Report 38** — Beads `discovered-from` edge; "corpus' strongest candidate compounding-of-knowledge primitive at the engine level."
- **Followup 12 §6** — Brier pace-layer promotion: project doc → Skill → enforced standard.
- **Report 03** — Compound Engineering's plan→work→review→compound loop, with knowledge accumulating in `docs/solutions/`.
- **[CTR-C3](../contradictions.md)** — self-improvement / methodology-evolution as substrate primitive vs methodology pattern.
- **[CTR-H2 / H3](../contradictions.md)** — knowledge-store split (events lazily vs summaries eagerly with cadence-controlled refresh).

## Open questions

- **Promotion as methodology or substrate?** GF-S, BF-S, BF-M put it methodology-side. U-C makes anchor-edit a typed work-unit-class (substrate-typed). D7-U-1 substrate-types it as survival-window. The split mirrors the broader CTR-C3 disagreement.
- **Knowledge-curator placement.** BF-M §7 #9 contests CTR-H2/H3: this track makes stale-knowledge the next reader's obligation, not a curator daemon's.
- **F55 acute at cold-start.** GF-C: *"Self-referential drift (F55) is most acute at cold-start because all 'knowledge' is from a tiny number of cycles. Accumulation begins only after Regime B has produced enough cycles to be evaluable."* — but this is *temporal* gating, not a substrate-typed promotion.

## Substrate-enforcement options

- `BF-S` `S-4 attribution + Compound-Knowledge store` — durable facts vs durable practices that change.
- `U-C` `anchor mutation queue` — anchor-edit work-units carry cooling-off windows, multi-author requirement, Caremark-style immutable logging.
- `D7-U-1` `survival-window registrar` — substrate-typed expiry-and-re-falsification.
- `U-B` knowledge-store + curated `docs/solutions/`-style summaries (CTR-H2 split resolved by carrying both).

Disciplines are distinct from primitives.
