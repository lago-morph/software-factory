# Archive — v1/v2 architectures

**Archived 2026-05-23** as Phase 0.4 of the [v3 synthesis plan](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md). The files in this directory are the *immediate predecessors* of the v3 architecture set; they are preserved verbatim so the Phase-7 back-fill audit can compare v3 against them deliberately, instead of inheriting their framings silently during v3 authorship.

**Status of these files:** superseded. Read for archaeology, not for current architectural guidance. The current architecture set lives in [`architectures/`](../../architectures/) (v3-derived).

**Why archived (per [`00-brief-v3` UC6](../../architectures/v3/00-brief-v3.md)):** archive-and-rebuild prioritizes anchor-avoidance over insight-preservation. The user-stated risk: silent anchoring on prior recommendations (e.g., "Compound Atelier as baseline" — [`00-comparison`](00-comparison.md) §7.1) would bias the v3 synthesis. The mitigation: physical removal from the active tree until Phase 7. The mitigation's own risk (recency bias against archive material in Phase 7) is acknowledged in [`00-brief-v3` OQ-B10](../../architectures/v3/00-brief-v3.md#8-open-questions-surfaced-by-this-brief-deliberate).

---

## Contents

| File | What it was | Why it mattered |
|---|---|---|
| [`00-comparison`](00-comparison.md) | v2 comparison + decision guide across the four architectures | Carried the "Compound Atelier as baseline + selective borrows" recommendation in §7. Pre-Round-2; lacks the substrate-stack framing. |
| [`01-specification-refinery`](01-specification-refinery.md) | Architecture 1: "the spec is the product; the implementation is a probe" | Layered spec discipline, revelation cycle, 5-mode failure classification. |
| [`02-compound-atelier`](02-compound-atelier.md) | Architecture 2: "each unit of work makes the next easier" | Queue + workpad + persona panel + accumulated `docs/solutions/`. v2's recommended baseline. |
| [`03-phase-gated-foundry`](03-phase-gated-foundry.md) | Architecture 3: "pre-agile structured methodologies become the right shape when agents make them fast" | Phase-bound experts, formal templates (SRS, SAD, DD), RTM, gate boards. |
| [`04-evolutionary-tournament`](04-evolutionary-tournament.md) | Architecture 4: "the factory does not specify the right answer; it sets up the conditions under which the right answer wins" | Genome library, predator agent, tournament bracket, model-family diversity. |
| [`failure-modes`](failure-modes.md) | Canonical F1-F20 per-architecture coverage matrix | Seed of the failure-mode catalog. F21-F49+ accumulated after this file was last updated; v3 consolidates everything into a new [`failure-modes-v3`](../../architectures/v3/failure-modes-v3.md). |

## Provenance pointer (for back-fill)

The v3 Phase-7 back-fill audit will enumerate every claim, framing, primitive, and recommendation in the files above. Each will be marked:

- `absorbed` — v3 carries an equivalent (cite v3 location).
- `rejected (reason)` — v3 deliberately did not carry it; reason cited.
- `TBD` — back-fill audit could not classify; surfaced to user.

Until Phase 7 completes, nothing in this directory binds v3 decisions.

---

*Index for [`archive/architectures-v2/`](.). See [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) Phase 0 and Phase 7 for the surrounding process.*
