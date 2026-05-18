# agent instruction

**Ground-truth-first when auditing status docs.** When the user asks for an audit of a long-lived status document (PLAN.md, ROADMAP.md, INDEX.md, RFC, design doc), run filesystem / catalog / git ground-truth queries (`ls research/ | wc -l`, `jq 'length' reference-only/sources.json`, `ls -d retrospective/*/`) BEFORE reading the doc's narrative claims. Counting first, reading second, fixing third catches drift that content-first reading internalizes and propagates.

*Grounded in: PR #98 PLAN.md audit caught report-count drift 26→37 only after running `ls research/ | wc -l`; the prose claim had survived two prior PRs that nominally updated PLAN.md.*

# justification

The dominant failure mode for long-lived status docs is that prose claims drift while the underlying counts move. PLAN.md said "26 numbered reports" in §1 status, "26 numbered reports + 12 followup" in §2 layout, and "5 retrospectives" in §3.4 — none of which matched ground truth (37 / 12 / 22). Two prior PRs (#94 plan-update-discipline, #97 single-source-normalize) both bumped the Version line but didn't recount, because they read-and-edited rather than count-and-edit; the wrong numbers carried forward each time. Cost of *not* having the rule: each subsequent audit re-discovers and re-fixes the same drift; readers learn to distrust the doc. Cost of adopting the rule: 30 seconds at the start of an audit to run 5 shell commands. The asymmetry is enormous — the rule pays for itself the first time it's followed.
