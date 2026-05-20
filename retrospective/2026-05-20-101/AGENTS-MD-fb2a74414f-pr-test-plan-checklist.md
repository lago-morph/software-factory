# agent instruction

**PR descriptions for research contributions include a numbered reviewer test plan.** Pull request descriptions for research-corpus contributions (reports, followups, synthesis, INDEX updates) must include a numbered reviewer test plan that names specific files and specific claims to spot-check, plus a "notes for reviewers" section calling out provenance caveats (blocked URLs, subagent authorship, supersedes-prior-report notes). Generic "verify the new files look right" descriptions defer the audit-burden onto the reviewer; explicit checklists make the audit cheap.

*Grounded in: PR #101 — reviewer test-plan with 5 specific spot-check items + "notes for reviewers" provenance block earned a fast merge.*

# justification

PR #101 included an explicit reviewer test plan with five specific checkboxes — verify the three new files are at expected paths and INDEX rows are present; spot-check three architectural claims in followup/13 against cited `gascity/...` paths; spot-check three claims in followup/14 against `gastown/...` paths; sanity-check the two mapping tables against the source reports; confirm the deployment-sketch sections cite Gas City features that actually exist at v1.0.0+. The "notes for reviewers" section also surfaced the blocked-URL caveat (docs.gascityhall.com → HTTP 403 from sandbox; analysis worked from in-repo Mintlify source), the subagent-authorship caveat (each deep-dive ran ~12 minutes with full read-only filesystem access; outputs spot-checked against foreground reads before commit), and the supersedes-prior-report note (followup/14 supersedes followup/04 on internal-package structure while remaining consistent on the Attractor-comparison axis).

The user merged the PR fast. The audit cost was concretely scoped — five tests, named files, named claims — and the provenance caveats meant no reviewer-side investigation was needed to understand why certain claims looked the way they did. Compare to a generic "Adds Gas City + Gas Town analysis" description: the reviewer would have to either trust the diff or open a 27k-word read to verify. Either outcome is worse.

The marginal cost is ~5 minutes of PR-description authorship per dense contribution. The benefit is the audit becomes a 10-minute reviewer pass instead of a 30-minute reviewer pass, and the provenance caveats are visible at decision time rather than discoverable only by re-reading the diff. Generalises to any research-corpus PR whose diff is denser than a reviewer can plausibly inspect line-by-line.
