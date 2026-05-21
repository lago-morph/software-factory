# agent instruction

**No source-availability tracking in plan docs.** Wanted URLs, outstanding sources, and fetch-status tables go into reference-only/sources.json as records (wanted, have, partial, etc.), not into PLAN.md or research-plan.md. Plan docs carry decisions and concrete tasks; sources.json carries source state.

*Grounded in: user feedback on cleanup-plan v1 — "the status should always reside in sources.json, not in a plan."*

# justification

Twice in this session, content I had drafted in PLAN.md was the wrong shape: a "manual fetch instructions" section (§4) with a Path-B-only / retry-eligible URL table, and an "in-flight tracking" table that mixed source-status rows with decision-status rows. Both produced the same failure mode — readers had to consult two documents to know what was actually outstanding, and the plan doc inevitably drifted from sources.json (the `platform.claude.com` URLs I listed as outstanding were in fact `have+complete` per the catalog).

The marginal cost of the rule is zero: every source-tracking action that would have gone into a plan doc instead goes through the existing research-pipeline skill catalog flow (`_catalog/edit.md`). The cost of not having the rule is permanent drift between two registers of truth, and stale items that look actionable but were resolved months ago. The cleanup PR removed an entire ~30-line §4 from PLAN.md because every row was either obsolete or duplicated catalog state.
