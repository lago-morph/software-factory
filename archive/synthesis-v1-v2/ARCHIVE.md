# Archive — v1 and v2 syntheses

**Archived 2026-05-23** as Phase 0.5 of the [v3 synthesis plan](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md). The two synthesis documents in this directory are preserved verbatim so the Phase-7 back-fill audit can deliberately compare v3's three syntheses (greenfield + brownfield + unified, per [`decisions-captured` D1](../../architectures/v3/decisions-captured.md)) against them.

**Status:** superseded. The v3 syntheses live in [`architectures/v3/`](../../architectures/v3/) once Phase 3 lands.

---

## Contents

| File | What it was | Coverage | Why archived |
|---|---|---|---|
| [`00-synthesis`](00-synthesis.md) | Round-1 synthesis (v2, post-primary-source-access) | 7 source reports (Round-1: `research/01-` through `07-`). Canonical entry for **F1-F20**. | Pre-Round-2; lacks substrate-stack framing, Agent=Model+Harness vocabulary (C10/C11), and 24 reports of post-Round-1 evidence. |
| [`13-round-2-synthesis`](13-round-2-synthesis.md) | Round-2 synthesis | Reports 08-12. Promoted **F21-F33** + Round-2 consensus tags **C10-C16**. Proposed the OpenHands+Overstory substrate stack as §6.2 / §8 recommendation. | Round-2 only. F34, F35, F36/F37 collision, and F40-F49 (Rounds 9-10) are *not* in this synthesis. Its substrate-stack conclusion is a *recommendation*, not a *user constraint* — explicitly excluded from the v3 brief per [`constraints-extracted` "explicitly NOT a constraint"](../../architectures/v3/constraints-extracted.md). |

## What v3 inherits from these syntheses — explicitly

A subset of consensus claims from these documents was carried forward into the v3 brief as **Round-1/Round-2 defaults** ([`00-brief-v3` §4](../../architectures/v3/00-brief-v3.md#4-round-1round-2-defaults-carried-forward-per-d3)). Defaults are *not invariants* — every Phase-2 track must mark each as `accepted with justification` or `challenged`.

The defaults carried forward:

- D-1. Specs are the durable artifact ([`00-synthesis`](00-synthesis.md) §2.1).
- D-2. Scenarios live outside the codebase as a holdout set ([`00-synthesis`](00-synthesis.md) §2.2). *Flagged fragile for brownfield.*
- D-3. Agent = Model + Harness ([`13-round-2-synthesis`](13-round-2-synthesis.md) §1.1 C10). *Flagged fragile for graph-node and population architectures.*
- D-4. Holdout discipline ([`13-round-2-synthesis`](13-round-2-synthesis.md) §1.1 C13).
- D-5. Hard cost ceilings ([`13-round-2-synthesis`](13-round-2-synthesis.md) §1.1 C15).
- D-6. Tiered watchdog ([`13-round-2-synthesis`](13-round-2-synthesis.md) §1.1 C14).
- D-7. Trajectory capture ([`13-round-2-synthesis`](13-round-2-synthesis.md) §1.1 C16).

Anything *else* in these syntheses (failure-mode definitions, substrate-stack recommendations, regime classifications, hybridization suggestions, etc.) is **not inherited** until Phase 7's back-fill audit explicitly absorbs or rejects it.

## Provenance pointer

Phase-7 back-fill audit treats every claim in this directory the same way it treats archived architectures: `absorbed` / `rejected (reason)` / `TBD`.

---

*Index for [`archive/synthesis-v1-v2/`](.). See [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) Phase 0 and Phase 7.*
