# agent instruction

**Strict session-bullet format in PLAN.md.** Session/round bullets under §1 use exactly three components and nothing else: date (YYYY-MM-DD), 24-hour time, the run's short name, and the PR hyperlink. Format: `**YYYY-MM-DD HH:MM <Run-name>** [#nn](pr-url)`. No prose narrative. No content summary. No semicolon-joined multi-clause sentences pretending to be one. Anyone who wants the content reads the PR.

*Grounded in: user feedback on cleanup-plan v2-v3 — "you are cheating and turning three sentences into 1 with semicolons. The new one in your example should only have date and time (24 hour format), round 11 manual drain, and link to pr. That's it."*

# justification

PLAN.md's pre-cleanup §1 was a chronological log of 17+ session bullets, each one a 100-200 word paragraph describing what the drain did, what files it touched, what surprises surfaced, and what was deferred. The result was a ~600-word block paragraph for the most recent session alone, accreted from the research-pipeline skill's drain-time auto-append. Two versions of compression were tried in cleanup-plan: v2 used "one short sentence + PR hyperlinks" (still 30-50 words per bullet); v3 used the strict three-component form (under 10 words).

The user's correction surfaced a general failure mode: when an LLM is told "one sentence," it tends to maximize what fits in one sentence (joined clauses, parentheticals, semicolons). The cure is to specify the components, not the sentence count. Marginal cost of the strict format: zero (the drain pipeline can emit it as easily as the verbose form). Cost of not having it: every drain expands PLAN.md §1 by a paragraph that nobody re-reads after the first week.
