# agent instruction

**Audit-trail URLs in plan docs go in `casual_url_patterns`, not in the catalog.** GitHub PR / issue / commit URLs used as audit-trail links inside `research/PLAN.md`, retrospectives, ADRs, and other plan documents are navigation aids, not citations of substantive sources. When `check-source-refs.py` (URL-vs-reports lint) flags such URLs, add the appropriate regex to `casual_url_patterns` in `.claude/skills/research-pipeline/SKILL.md` — don't create wanted catalog records for them.

*Grounded in: PLAN.md rewrite added a `#nn` PR link per session bullet; check-source-refs.py flagged twenty PR URLs until `https?://github\.com/[^/]+/[^/]+/pull/\d+` was added to casual_url_patterns.*

# justification

The new strict short bullet format mandated by the cleanup plan puts a GitHub PR link on every session bullet under `§1` and on every row of the `§10` lookup table. With ~25 PR links in a fresh PLAN.md, the URL-vs-reports lint check flagged twenty errors on the first pass — every PR URL became a "URL cited in research/PLAN.md but no record in catalog" failure.

Creating catalog records for PR URLs would be wrong (they're not sources; they're navigation), and silencing the error would be worse (the check is load-bearing for catalog hygiene). The right answer is a one-line addition to `casual_url_patterns`. The pattern is already there for `api.github.com`, social media, and homepage URLs — the rule just makes "PR URLs in plan docs" explicit so future plan-doc authors know to apply the same treatment, instead of rediscovering the lint failure each time.

Marginal cost of adopting the rule: a single regex line. Cost of not adopting: every PR-link-heavy plan doc rewrites trips the lint check until someone re-derives the fix.
