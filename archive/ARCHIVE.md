# Archive — pre-v3 synthesis material

**Archived 2026-05-23** as Phase 0.4-0.6 of the [v3 synthesis plan](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md). This directory holds work-product from the pre-v3 phase of the project — primarily lead-agent recommendations and prior-synthesis conclusions that were specifically *not* carried forward as user constraints into v3.

**Why this directory exists.** Per [`00-brief-v3` UC6](../architectures/v3/00-brief-v3.md), the user instructed: *"we have that stuff in our git history, just get it out of the way so we don't confuse things. We might also want to consider doing that with the existing syntheses. Get rid of them, and then after we are done, see if there are any things in there that can be added. But start fresh."* This directory is the controlled archive that supports that workflow.

**What is here / what is not.**

- **Here:** documents that carried *recommendations* or *frame-imposing conclusions* from pre-v3 work, where leaving them in the active tree risks silently anchoring the v3 synthesis.
- **Not here:** the underlying research reports (`research/01-` through `research/38-` + `research/followup/`). Those are *evidence*, not recommendations, and remain in the active tree as the primary corpus for the v3 synthesis.

---

## Contents

| Path | What | Index |
|---|---|---|
| [`architectures-v2/`](architectures-v2/) | The four v2 architecture specs + the v2 comparison doc + the v2 failure-modes coverage matrix | [`ARCHIVE.md`](architectures-v2/ARCHIVE.md) |
| [`synthesis-v1-v2/`](synthesis-v1-v2/) | The Round-1 synthesis and the Round-2 synthesis | [`ARCHIVE.md`](synthesis-v1-v2/ARCHIVE.md) |
| [`research-plan.md`](research-plan.md) | The 2026-05-14 "research → action plan" proposal | (this file; see note below) |

### Note on [`research-plan.md`](research-plan.md)

The original [`research-plan.md`](research-plan.md) carried two kinds of content:

1. **User-stated constraints** (lights-out greenfield mandate; archive-and-rebuild discipline; cold-start as a dedicated risk for greenfield; named cold-start inputs).
2. **Lead-agent recommendations** (collapse to Atelier+Refinery; one chosen architecture + rejected-alternatives appendix).

The user-stated constraints were extracted into [`constraints-extracted`](../architectures/v3/constraints-extracted.md) (UC1, UC4 via Historian M4, UC5, UC6) and *then* the file as a whole was archived per UC6. The recommendations remain available here for the Phase-7 back-fill audit, but they are *not* binding on v3.

---

## Phase 7 back-fill scope

The v3 [Phase 7 back-fill audit](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) enumerates every claim, framing, primitive, or recommendation in this directory and classifies each as:

- `absorbed` — v3 carries an equivalent (cite v3 location).
- `rejected (reason)` — v3 deliberately did not carry it; reason cited.
- `TBD` — back-fill audit could not classify; surfaced to user.

A **silent-absorption auditor** subagent runs alongside the lead-agent audit to flag content that may have slipped into v3 unintentionally (the inverse direction).

Per [`00-brief-v3` OQ-B10](../architectures/v3/00-brief-v3.md#8-open-questions-surfaced-by-this-brief-deliberate), Phase 7 is the explicit mitigation for the archive-and-rebuild discipline's known weakness (recency bias against archive material). Lead agent should be especially generous toward archive items in Phase 7.

---

*See [`ARCHITECTURE-V3-SYNTHESIS-PLAN`](../ARCHITECTURE-V3-SYNTHESIS-PLAN.md) Phase 0 and Phase 7 for the surrounding process.*
