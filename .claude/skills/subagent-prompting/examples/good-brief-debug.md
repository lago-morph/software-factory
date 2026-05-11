# Good brief example: workflow debug

This is a real subagent brief from the session. The dispatcher suspected
something was blocking GitHub writes but didn't know what. The brief
enumerated 7 specific hypotheses and assigned a 30-minute budget. The
subagent found the root cause (GitHub's repository lock feature blocking
token-based writes) in 13 minutes. Notable strengths:

- Numbered hypothesis list: subagent had a concrete search agenda, not "poke
  around until something turns up."
- Explicit file paths and diagnostic commands per hypothesis.
- Side-effect constraint ("at most ~10 new comments") — prevented the
  subagent from spamming the repo while probing.
- Token guidance: subagent knew to check for usable tokens in env before
  trying API calls.
- 30-minute hard cap with a required pivot if not resolved.
- Structured report format: findings + evidence + remediation path.

---

## Illustrative brief (reconstructed from session patterns)

You are debugging a workflow failure in the agent-job-protocol POC at
`/home/user/poc-github-ai-sandbox`. The dispatcher has confirmed the test
suite passes locally but writes to the GitHub repo are silently failing. Your
job is to find the root cause and propose a remediation — not to fix it.

### Context
- Branch: `main` (read-only investigation; do not commit)
- Spec: `SPEC.md` (skim §4 — GitHub integration section — for context)
- Prior findings: `mcp__github__add_issue_comment` calls return 200 but the
  comment doesn't appear in the UI. Direct `gh` CLI also fails with a
  non-obvious error. Token is set in the environment.

### Hypotheses to investigate (in order)

1. **Repo lock active** — check if the repository has GitHub's "lock" feature
   enabled (Settings → Danger Zone → Lock repository). A locked repo allows
   reads but blocks all writes including comments.
2. **Token scope** — run `gh auth status` and confirm the token has
   `repo` scope. A `read:org`-only token can authenticate but not write.
3. **Branch protection rule** — check if a branch protection rule on `main`
   is blocking force-push or PR merges that would appear as write failures
   upstream.
4. **MCP trailer parsing** — `mcp__github__add_issue_comment` appends a
   Claude Code trailer to comment bodies. Check if a downstream parser is
   calling `json.loads()` on the raw comment; this would raise on the
   trailer. Use `JSONDecoder().raw_decode()` instead.
5. **Rate limiting** — check `gh api rate_limit`. If core remaining < 10,
   writes may be queued or dropped.
6. **Wrong repo target** — verify the MCP tool is pointing at the correct
   owner/repo (not a fork or a stale env var).
7. **App vs PAT auth** — if the env has both a GitHub App token and a PAT,
   check which one the MCP layer is using. App tokens have installation-level
   permission grants that may not cover this repo.

### Diagnostic steps

For each hypothesis:
- State which tool or command you used to check it.
- Paste the relevant output (truncated to ≤10 lines per check).
- Record CONFIRMED / RULED OUT / INCONCLUSIVE.

Stop investigating once you have a CONFIRMED hypothesis. Do not continue
through all 7 if you've already found the root cause.

### Side-effect constraint

You may post at most ~10 new comments or API calls during investigation.
Do not open PRs, push commits, or modify any files.

### Token check

Before any API calls: `echo $GITHUB_TOKEN | cut -c1-8` to confirm a token is
present. If empty, stop immediately and report "no token available."

### Time budget

Cap effort at 30 minutes. If you have not confirmed a hypothesis by then,
report the top 2 INCONCLUSIVE candidates and your recommended next diagnostic
step. Do not dig deeper past the budget.

### Report format

Under 400 words. Sections:
1. Root cause (one sentence, or "not found" with top candidates)
2. Evidence (the output that confirms it, ≤10 lines)
3. Hypotheses ruled out (list with one-line reason each)
4. Remediation path (specific steps to fix, but do not execute them)
5. Estimated fix time

---

## Why this worked

- **Numbered hypotheses.** The subagent had a concrete agenda rather than
  open-ended exploration. It stopped at hypothesis 1 (repo lock), confirmed
  it, and reported — total elapsed: 13 minutes.
- **"Stop early" instruction.** Without "stop once you have a CONFIRMED
  hypothesis," the subagent might have checked all 7 out of diligence,
  wasting 10+ minutes.
- **Side-effect constraint.** Capping at ~10 API calls prevented spamming the
  repo with probe comments. This matters in repos with human reviewers.
- **Token pre-check.** Checking the token up front prevents the subagent from
  spending 5 minutes debugging a "no auth" situation that could be diagnosed
  in 5 seconds.
- **Pivot requirement.** The 30-minute cap with mandatory "top 2 candidates"
  output means the dispatcher gets signal even if the subagent doesn't fully
  resolve the issue.
- **Evidence-based report.** Asking for the raw output that confirms the
  finding means the dispatcher can verify the diagnosis without re-running the
  investigation.
