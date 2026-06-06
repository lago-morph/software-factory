# agent instruction

**Docs-only PRs trigger no CI in this repo.** This repo's GitHub Actions workflows are all path-scoped (e.g. `architectures/0N-*.md`, `sources.json`, research-pipeline scripts). A PR that touches only documentation (root `*.md`, `architectures/v4/**`, `AGENT-ENTRY.md`) produces zero check runs, so a `pending`/0-checks status is the terminal state, not a queue to wait on. Confirm via `actions_list` / `get_check_runs` and do not arm a CI wait for such a PR.

*Grounded in: PRs #249/#250/#251 each returned 0 check runs; listing the 5 repo workflows confirmed none match docs paths.*

# justification

Subscribed to three docs-only PRs this session, each showing combined status `pending` with zero checks. That looks like "CI is still queued" but it is actually "no workflow matches these paths" — a terminal state. Listing the five workflows confirmed all are path-scoped away from docs. Without this rule an agent waits (or worse, polls) indefinitely for checks that will never appear; with it, one `get_check_runs` plus a glance at the workflow paths settles it and the agent moves on.
