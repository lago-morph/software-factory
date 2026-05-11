---
name: research-pipeline
description: Conduct disciplined multi-source research producing reports with full source-status traceability. Use this when the user asks to research a topic that spans multiple web sources (some likely blocked from the sandbox), wants written reports stored in the repo's `research/` folder, and wants future research opportunities tracked in a resumable plan. Handles: probing source reachability, bootstrapping a GitHub Actions URL-fetch workflow for blocked hosts, opening labelled fetch issues, merging fetched content back, writing reports with sources-status tables, cleaning up consumed fetched files, maintaining a research index, and recording promising referenced-source clusters as future research targets with justifications.
---

# Research Pipeline Skill

A disciplined methodology for multi-source research that produces audit-traceable reports and a self-extending research plan. Designed to work in any repo, on any topic, with or without an existing fetch-action infrastructure.

## When to invoke

Invoke when the user:
- Asks to research a topic spanning multiple web sources (blogs, docs, papers, GitHub repos).
- Wants the research output to live in the repo as durable markdown reports.
- Suspects (or you discover) that some sources are blocked from the sandbox.
- Wants future-research follow-ups recorded as the work surfaces new candidate sources.

Do NOT invoke for:
- Quick single-source lookups (one WebFetch is enough).
- Code reviews or implementation work (use a different skill).
- Tasks that don't produce a written artifact.

## Conventions and naming (consolidated)

All artifacts produced by this skill follow a small, deliberately rigid set of naming and structural conventions. These rules are not negotiable from inside the skill — if the repo already uses different paths, *follow the existing repo convention* and note the divergence at the top of the report; otherwise use these defaults exactly so future agents (and future you) can locate things mechanically.

### Filesystem layout

| Item | Default path | Notes |
|---|---|---|
| Research reports | `research/NN-<slug>.md` | NN is the next zero-padded sequence integer; `ls research/` to pick. Slug is short kebab-case noun phrase. |
| Round-specific partial reports | `research/NN-<slug>-partial.md` | When you intentionally cover only part of an originally larger scope; status field must say "Partial." |
| Research index | `research/INDEX.md` | Single-glance summary of every report; updated after each new/edited report. |
| Resumable plan | `research/PLAN.md` | The next-session handoff. Owns the §10 progress log + in-flight tracking (see [in-flight-workflow-tracking](../in-flight-workflow-tracking/SKILL.md)). |
| Blocked-URL inventory | `research/blocked-urls.md` (or per-round `blocked-urls-round-N.md`) | The status of every URL the research depends on. |
| Fetched raw content | `research/fetched/issue-<N>/` | One subdir per fetch issue; the workflow commits here directly. |
| Fetch workflow definition | `.github/workflows/fetch-blocked-urls.yml` | See the [fetch-blocked-urls](../fetch-blocked-urls/SKILL.md) skill for the canonical version. |
| Fetch trigger label | `fetch-urls` | Repo label. Auto-created on first `mcp__github__issue_write` that references it. |
| Branch for fetched content | `fetched/issue-<N>` | Created by the workflow. Merged into your working branch. |
| Branch for research work | `claude/<short-slug>` | Per [always-commit-skill-to-repo](../always-commit-skill-to-repo/SKILL.md). Never push to `main`. |

### Report file structure (every report)

The body of every report follows this skeleton. Sections may be added; **the four labelled blocks below must appear, in this order**:

```markdown
# Report NN — <Title>

**Date:** <YYYY-MM-DD>
**Author:** Lead agent  (or subagent-dispatch designation, if applicable)
**Status:** <one-line: ✅ complete / 🟡 partial / 📝 draft / ⏳ blocked-on-fetch>

## Lead question

<the one-paragraph question from Phase 1 — verbatim, not paraphrased>

## <Substantive sections — H2 each>

<Number them. Cite specific sources at the point of claim, not just at
the top of the report. Quote verbatim where the language matters;
paraphrase where structure matters.>

---

## Sources reviewed

<Status table at the BOTTOM of the report. See the legend below.
Non-negotiable: this is what makes the report auditable.>
```

### Sources-Reviewed table — legend and format

Every report ends with a "Sources reviewed" table. The legend is fixed:

- ✅ **Full review** — fetched and read end-to-end.
- 🟡 **Reconstructed** — synthesized from search snippets, summary descriptions, or partial extraction; some details inferred.
- ⏳ **Pending** — queued in a fetch issue, not yet returned.
- ❌ **Unavailable** — could not obtain (or not yet attempted; explicitly deferred to a follow-up).

Per-row columns: `Source URL | Status | Notes`. The Notes column should answer two questions at minimum: *what was actually read* and *which section of the report it informed*. For 🟡/⏳/❌ rows, also state *what's missing and where to recover it*.

### Index entry format

Every report gets one row in `research/INDEX.md`:

| # | Title | Status | Primary sources | Key conclusion (1 line) |
|---|---|---|---|---|
| NN | <slug> | ✅/🟡/📝/⏳/🗑️ | <count or short list> | <one-line headline> |

Status values: ✅ complete · 🟡 partial · 📝 draft · ⏳ blocked-on-fetch · 🗑️ deprecated.

The index is the entry point for anyone (including a future Claude session) trying to figure out where the research stands. Keep it accurate; if a report's status changes, update the index in the same commit.

### Fetched-file cleanup (when to `git rm`)

After a report has incorporated everything it's going to incorporate from a fetched source file, **remove the raw fetched file** from the repo:

```bash
git rm research/fetched/issue-N/<fully-consumed-file>.html
git rm research/fetched/issue-N/<fully-consumed-file>.md
```

Keep the `.fetch-work/urls.txt` manifest so a future reader can see what was originally requested.

Do **NOT** delete a fetched file if:

- The corresponding report is marked **partial** and the source is one of the still-pending pieces.
- The file failed to fetch (still has the 403/404 body) — keep as evidence of the failure.
- The file is the canonical reference for a section that doesn't quote it heavily (you may want to re-read it later).

When unsure, prefer to keep. Disk is cheap; lost provenance is expensive.

### Future-research clusters

Captured in `research/PLAN.md` under a "Future research" heading. Per-cluster format:

```markdown
### Future research: <single-phrase cluster name>

**Sources:**
- <url>
- <url>

**Justification:** <one paragraph — what decision could this change, what
gap could it fill, what claim could it confirm/refute>

**Effort:** <rough token cost, wall time, and any fetch dependencies>
```

This is what makes the research pipeline self-extending rather than one-shot.

### Cross-skill references (don't duplicate)

This skill assumes the existence of two siblings:

- **[`always-commit-skill-to-repo`](../always-commit-skill-to-repo/SKILL.md)** — the sandbox-persistence discipline. All reports and fetched content must be committed and pushed. Default to a feature branch named `claude/<slug>` and a PR at the end.
- **[`in-flight-workflow-tracking`](../in-flight-workflow-tracking/SKILL.md)** — tracking async work (the [fetch-blocked-urls](../fetch-blocked-urls/SKILL.md) workflow especially) when a session may end before completion. The PLAN.md "MANDATORY first action" block belongs to that skill.

If you don't find those two skills in `.claude/skills/`, the work is incomplete and either (a) you're in a fresh repo that doesn't yet have them — install or skip with explicit caveat in the report — or (b) the repo deliberately doesn't use them, in which case fall back to inline documentation in the report.

## Pipeline phases

Always work through these in order. Don't skip phases even when the source list is small — the discipline scales.

### Phase 1 — Scope

Before any tool use, write a one-paragraph **lead question** that names what the research is trying to decide. Surface it to the user for confirmation if it's at all ambiguous. The lead question goes at the top of every report.

Capture the user's initial source list verbatim in a working file (or use the conversation if it's small). Don't immediately dispatch subagents — first probe what's actually reachable.

### Phase 2 — Reachability probe

For each URL in the list, do a quick `WebFetch` (one URL at a time, batched in parallel where possible) with a minimal prompt like *"Return status or first 200 words"*. Categorize each result:

- **✅ Reachable** — content extracted cleanly.
- **🟡 Partial** — fetched but extraction was incomplete (e.g. heavy JS, paywall preview, html2text missed body).
- **❌ Blocked** — 403 / 404 / network refused / Cloudflare block / authenticated-only.

Specifically check `raw.githubusercontent.com` for any GitHub source — that host usually works even when `github.com` itself is restricted.

Record the categorization in `research/blocked-urls.md` (or the round-specific variant) with one row per URL.

### Phase 3 — Bootstrap fetch infra if needed

If Phase 2 produced any ❌s **and** the repo does not already have `.github/workflows/fetch-blocked-urls.yml`, bootstrap it now. The workflow + scripts are appended at the end of this skill — copy them in, validate the YAML parses (`python3 -c "import yaml; yaml.safe_load(open('.github/workflows/fetch-blocked-urls.yml'))"`), commit, and ask the user to merge to `main` before the workflow can fire (GitHub `issues`-event workflows always run from the default branch).

If the workflow already exists, verify the gate is **label-based** (`fetch-urls`) not `author_association`-based. The latter is unreliable; replace if needed. See the "Workflow lessons learned" section at the end of this skill for the failure history.

### Phase 4 — Open the fetch issue

Use `mcp__github__issue_write` (method=`create`) with:
- A title starting with the convention prefix (e.g. `[fetch-urls] <short description>`).
- A body containing one URL per line; markdown links are tolerated; ≤ 50 URLs per issue (the workflow caps at 50).
- `labels: ["fetch-urls"]` — this both gates and triggers the workflow. Applying the label at creation time fires the workflow immediately with no follow-up edit needed.

Important: `mcp__github__issue_write` with a previously-unknown label name auto-creates the label (default color `#ededed`). No separate label-bootstrap step is needed.

If asking the user to shut down the session at this point, **explicitly record in the plan** that the fetch is in-flight and what to do when it lands. Don't assume a future agent will figure it out.

### Phase 5 — Drain the fetch

Poll for the branch via `git ls-remote --exit-code --heads origin fetched/issue-<N>`. The workflow creates that branch when it succeeds and posts a per-URL summary as an issue comment.

When it lands:
1. `git fetch origin fetched/issue-<N>` and merge into your working branch.
2. Read the per-URL summary comment to see which URLs failed (still ❌ even after CI) — those become candidates for the next phase (Wayback Machine retry).
3. Update `research/blocked-urls.md` with the new statuses.

### Phase 6 — Wayback fallback (if needed)

For URLs that returned 403 from GitHub runners too (Substack, some news sites, sometimes arXiv direct), retry via the Internet Archive:

```
https://web.archive.org/web/<timestamp-or-year>/<original-url>
```

The `/web/2026/` redirect-to-latest form is the simplest. If that also fails, try a specific recent snapshot timestamp.

Open a second `[fetch-urls]` issue with the Wayback URLs. Sometimes a Wayback snapshot exists; sometimes not. Record both outcomes.

### Phase 7 — Read sources efficiently

For each ✅ source: `Read` it directly. For 🟡 sources: be explicit in the report about what was missed. For ❌ sources: don't infer content; either skip them, fetch via Wayback, or mark the dependent claims as "not directly evidenced."

When a source is too large to read in full (e.g. a 1 MB+ html2text dump), read the first ~200 lines, search/grep for the key terms you care about, and read those sections. Note in the report that the read was targeted, not exhaustive.

**PDFs caveat:** `html2text` does NOT extract PDF text. If you fetch a PDF and the result looks like `%PDF-1.7` + binary streams, fall back to the HTML render (arXiv has `/html/<id>v<version>`) or skip that source.

### Phase 8 — Write the report

File path: `research/NN-<slug>.md` where NN is the next zero-padded sequence number. Look at existing files to pick the next number.

Required structure:

```markdown
# Report NN — <Title>

**Date:** <YYYY-MM-DD>
**Author:** Lead agent (or subagent designation)
**Status:** <one-line: complete / partial / draft>

## Lead question

<the one-paragraph question from Phase 1>

## <Substantive sections>

<Number them. Use H2 for top-level sections. Cite specific sources at the
point of claim, not just at the top. Quote verbatim where the language
matters; paraphrase where structure matters.>

---

## Sources reviewed

<Table at the BOTTOM of the report — see legend.>
```

**Sources reviewed table format** (always at the bottom of the report):

| Source URL | Status | Notes |
|---|---|---|
| <url> | ✅ / 🟡 / ⏳ / ❌ | <what was actually read; which section of the report it informed; what's missing> |

Legend:
- ✅ **Full review** — fetched and read end-to-end.
- 🟡 **Reconstructed** — synthesized from search snippets, summary descriptions, or partial extraction; some details inferred.
- ⏳ **Pending** — queued in a fetch issue, not yet returned.
- ❌ **Unavailable** — could not obtain (or not yet attempted; explicitly deferred to a follow-up).

The table at the bottom is non-negotiable. It is what makes the report's claims auditable.

### Phase 9 — Cleanup consumed fetched files

After a report has incorporated everything it's going to incorporate from a fetched source, **remove the raw fetched file** from the repo. The report cites the source URL, not the local snapshot; keeping a 2 MB HTML dump committed indefinitely bloats the repo.

```bash
git rm research/fetched/issue-N/<fully-consumed-file>.html
git rm research/fetched/issue-N/<fully-consumed-file>.md
```

Keep the `.fetch-work/urls.txt` manifest so a future reader can see what was originally requested.

Do NOT delete a fetched file if:
- The corresponding report is marked **partial** and the source is one of the still-pending pieces.
- The file failed to fetch (still has the 403/404 body) — keep as evidence.
- The file is the canonical reference for a section that doesn't quote it heavily (you may want to re-read it later).

When unsure, prefer to keep. Disk is cheap; lost provenance is expensive.

### Phase 10 — Update the research index

Maintain `research/INDEX.md` as a single-glance summary of every report in the folder. After each new or updated report, edit the index:

```markdown
# Research Index

Last updated: <date>

| # | Title | Status | Primary sources | Key conclusion (1 line) |
|---|---|---|---|---|
| 01 | <slug> | ✅ complete | <count or short list> | <one-line headline> |
| ... |
```

Status values: ✅ complete · 🟡 partial · 📝 draft · ⏳ blocked-on-fetch · 🗑️ deprecated.

The index is the entry point for anyone (including a future Claude session) trying to figure out where the research stands. Keep it accurate.

### Phase 11 — Future-research clusters

This is the most-skipped phase and the highest-leverage one. As you read sources, you'll notice references to other sources, named tools, named methodologies, or named people that are likely worth investigating but aren't in scope for the current report.

Capture each cluster of related references in `research/PLAN.md` under a "Future research" section. For each cluster:

1. **Name the cluster.** Single phrase. e.g. *"Cisco LangChain enterprise control-plane case studies"* or *"Anthropic Skills SDK ecosystem"*.
2. **List the sources** with URLs.
3. **Justify** — one paragraph explaining how investigating this cluster would extend the knowledge base relative to the current project. Be specific: what decision could it change, what gap could it fill, what claim could it confirm/refute?
4. **Estimate effort** — rough token cost, rough wall time, fetch dependencies.

Example entry:

```markdown
### Future research: Anthropic MCP server ecosystem

**Sources:**
- https://modelcontextprotocol.io/
- https://github.com/modelcontextprotocol/servers
- (etc.)

**Justification:** Three reports in this round (NN, MM, KK) mention MCP
as the canonical pattern for exposing tools to agents, but none audit
the actual server inventory. Investigating this cluster would let us
populate our Architecture-3 "Phase 2 tool gateway" with concrete server
choices, and might surface security-policy templates we can reuse.

**Effort:** ~30 source files, mostly raw.githubusercontent.com (no fetch
action needed). One subagent dispatch, ~30 min wall time.
```

This phase is what makes the research pipeline *self-extending* rather than one-shot. Every round of research seeds the next.

## What this skill does NOT do

- Does not write code beyond the fetch-workflow bootstrap.
- Does not run subagents — those are dispatched separately when scale demands it. This skill describes the *pattern* a subagent would follow.
- Does not interact with the user's GitHub UI beyond what `mcp__github__*` tools allow (no checking workflow run logs directly — diagnose from issue comments + commit history instead).

## Workflow lessons learned (apply before bootstrapping the fetch workflow)

The fetch workflow described in this skill is the v4 design. Prior versions broke in instructive ways; the v4 design avoids each of these traps:

1. **Job-level `if:` skips are silent in the Actions UI.** Never gate at job level on values you can't observe from outside. Always gate via a step that *runs and exits cleanly* so the logs are visible.
2. **`length()` is NOT a GitHub Actions expression function.** The expression function set is small: `contains`, `startsWith`, `endsWith`, `format`, `join`, `toJSON`, `fromJSON`, `hashFiles`, plus the status checks. Anything else fails at workflow-parse time and disables the whole file.
3. **`author_association` is computed differently by the REST API and the webhook payload.** A user the REST API reports as `MEMBER` may appear as `CONTRIBUTOR` in the webhook payload for the same issue. Don't use it as a gate.
4. **Use a label as the security gate.** Only users with Triage role or higher can apply labels in GitHub, so the label IS the trust boundary. `mcp__github__issue_write` with `labels: ["fetch-urls"]` on an unknown label auto-creates the label.
5. **`issues`-triggered workflows always run from the default branch.** A fix on a feature branch is inert until merged.

## Bootstrap files

If the repo does not yet have the fetch infrastructure, create these files. They are deliberately small and self-contained.

### `.github/workflows/fetch-blocked-urls.yml`

```yaml
name: Fetch Blocked URLs

# Triggered by issues carrying the `fetch-urls` label. The label gate is
# the security boundary: only users with Triage role or higher can apply
# labels. See the research-pipeline skill for the v1-v4 design history.

on:
  issues:
    types: [opened, edited, labeled, reopened]
  workflow_dispatch:
    inputs:
      issue_number:
        description: "Issue number whose body contains the URLs to fetch"
        required: true
        type: string

permissions:
  contents: write
  issues: write

concurrency:
  group: fetch-blocked-urls-${{ github.event.issue.number || inputs.issue_number }}
  cancel-in-progress: false

jobs:
  fetch:
    name: Fetch URLs from issue body
    runs-on: ubuntu-latest
    # NO job-level if. Gates are step-level + logged.
    steps:
      - name: Show context for diagnostics
        env:
          EVENT_NAME: ${{ github.event_name }}
          ACTION: ${{ github.event.action }}
          ISSUE_TITLE: ${{ github.event.issue.title }}
          ISSUE_USER: ${{ github.event.issue.user.login }}
          ISSUE_LABELS_JSON: ${{ toJSON(github.event.issue.labels.*.name) }}
          ISSUE_BODY: ${{ github.event.issue.body }}
        run: |
          echo "event=$EVENT_NAME action=$ACTION"
          echo "issue title  = $ISSUE_TITLE"
          echo "issue user   = $ISSUE_USER"
          echo "issue labels = $ISSUE_LABELS_JSON"
          echo "body length  = ${#ISSUE_BODY}"

      - name: Enforce label gate
        id: label_gate
        if: github.event_name == 'issues'
        env:
          LABELS_JSON: ${{ toJSON(github.event.issue.labels.*.name) }}
        run: |
          set -euo pipefail
          if echo "$LABELS_JSON" | grep -q '"fetch-urls"'; then
            echo "proceed=true" >> "$GITHUB_OUTPUT"
          else
            echo "Label fetch-urls not present; exiting cleanly."
            echo "proceed=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Resolve issue number
        id: resolve
        if: github.event_name == 'workflow_dispatch' || steps.label_gate.outputs.proceed == 'true'
        env:
          ISSUE_NUMBER_FROM_EVENT: ${{ github.event.issue.number }}
          ISSUE_NUMBER_FROM_INPUT: ${{ inputs.issue_number }}
        run: |
          if [ -n "${ISSUE_NUMBER_FROM_EVENT}" ]; then
            echo "issue_number=${ISSUE_NUMBER_FROM_EVENT}" >> "$GITHUB_OUTPUT"
          else
            echo "issue_number=${ISSUE_NUMBER_FROM_INPUT}" >> "$GITHUB_OUTPUT"
          fi

      - name: Checkout
        if: steps.resolve.outputs.issue_number != ''
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Set up Python
        if: steps.resolve.outputs.issue_number != ''
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install deps
        if: steps.resolve.outputs.issue_number != ''
        run: pip install "html2text==2024.2.26"

      - name: Resolve issue body
        if: steps.resolve.outputs.issue_number != ''
        env:
          ISSUE_NUMBER: ${{ steps.resolve.outputs.issue_number }}
          BODY_FROM_EVENT: ${{ github.event.issue.body }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          mkdir -p .fetch-work
          if [ -n "${BODY_FROM_EVENT}" ]; then
            printf '%s' "$BODY_FROM_EVENT" > .fetch-work/body.txt
          else
            gh issue view "$ISSUE_NUMBER" --repo "${GITHUB_REPOSITORY}" --json body --jq '.body' > .fetch-work/body.txt
          fi
          echo "Body length: $(wc -c < .fetch-work/body.txt) bytes."

      - name: Extract URLs
        id: extract
        if: steps.resolve.outputs.issue_number != ''
        run: |
          set -euo pipefail
          BODY="$(cat .fetch-work/body.txt)" python3 .github/scripts/extract_urls.py > .fetch-work/urls.txt
          count=$(wc -l < .fetch-work/urls.txt | tr -d ' ')
          echo "url_count=$count" >> "$GITHUB_OUTPUT"
          [ "$count" -eq 0 ] && echo "no_urls=true" >> "$GITHUB_OUTPUT" || true
          [ "$count" -gt 50 ] && echo "too_many=true" >> "$GITHUB_OUTPUT" || true

      - name: Fetch URLs
        if: steps.resolve.outputs.issue_number != '' && steps.extract.outputs.too_many != 'true' && steps.extract.outputs.no_urls != 'true'
        env:
          ISSUE_NUMBER: ${{ steps.resolve.outputs.issue_number }}
        run: bash .github/scripts/fetch_urls.sh

      - name: Commit and push
        if: steps.resolve.outputs.issue_number != '' && steps.extract.outputs.too_many != 'true' && steps.extract.outputs.no_urls != 'true'
        id: commit
        env:
          ISSUE_NUMBER: ${{ steps.resolve.outputs.issue_number }}
          ISSUE_TITLE: ${{ github.event.issue.title }}
        run: |
          set -euo pipefail
          BRANCH="fetched/issue-${ISSUE_NUMBER}"
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git checkout -B "$BRANCH"
          git add research/fetched/ .fetch-work/urls.txt
          if git diff --cached --quiet; then
            echo "empty=true" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          git commit -m "Fetch URLs for issue #${ISSUE_NUMBER}: ${ISSUE_TITLE}"
          git push -u origin "$BRANCH" --force-with-lease
          echo "branch=$BRANCH" >> "$GITHUB_OUTPUT"

      - name: Comment results
        if: steps.resolve.outputs.issue_number != '' && steps.extract.outputs.too_many != 'true' && steps.extract.outputs.no_urls != 'true'
        uses: actions/github-script@v7
        env:
          BRANCH: ${{ steps.commit.outputs.branch }}
          ISSUE_NUMBER: ${{ steps.resolve.outputs.issue_number }}
        with:
          script: |
            const fs = require('fs');
            const branch = process.env.BRANCH || '';
            const issueNumber = parseInt(process.env.ISSUE_NUMBER, 10);
            const summaryPath = '.fetch-work/summary.md';
            const summary = fs.existsSync(summaryPath) ? fs.readFileSync(summaryPath, 'utf8') : '';
            const body = branch
              ? `Fetched URLs committed to branch \`${branch}\`.\n\n### Per-URL summary\n\n${summary}`
              : `Every fetch failed (or no commit). Run ${context.runId}.\n\n${summary}`;
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issueNumber,
              body,
            });
```

### `.github/scripts/extract_urls.py`

```python
#!/usr/bin/env python3
"""Extract URLs from env var BODY. Handles markdown links + bare URLs, dedups, strips trailing punctuation."""
from __future__ import annotations
import os, re, sys

BODY = os.environ.get("BODY", "")
MD_LINK = re.compile(r"\[[^\]]*\]\((https?://[^\s)]+)\)")
BARE = re.compile(r"(?<![\w(])(https?://[^\s)>\]'\"`]+)")
MAX_URL = 2048

def _clean(u: str) -> str:
    while u and u[-1] in ".,;:!?'\"":
        u = u[:-1]
    return u

def extract(body: str) -> list[str]:
    seen, out = set(), []
    for m in MD_LINK.finditer(body):
        u = _clean(m.group(1))
        if 0 < len(u) <= MAX_URL and u not in seen:
            seen.add(u); out.append(u)
    body_minus_md = MD_LINK.sub("", body)
    for m in BARE.finditer(body_minus_md):
        u = _clean(m.group(1))
        if 0 < len(u) <= MAX_URL and u not in seen:
            seen.add(u); out.append(u)
    return out

for u in extract(BODY):
    print(u)
print(f"Extracted {len(extract(BODY))} URLs.", file=sys.stderr)
```

### `.github/scripts/fetch_urls.sh`

```bash
#!/usr/bin/env bash
# Fetch each URL in .fetch-work/urls.txt; save raw HTML + html2text .md
# under research/fetched/issue-<N>/. Per-URL summary at .fetch-work/summary.md.
set -euo pipefail

ISSUE_NUMBER="${ISSUE_NUMBER:?ISSUE_NUMBER not set}"
OUT_DIR="research/fetched/issue-${ISSUE_NUMBER}"
WORK_DIR=".fetch-work"
URLS_FILE="${WORK_DIR}/urls.txt"
SUMMARY="${WORK_DIR}/summary.md"

[ ! -s "$URLS_FILE" ] && { echo "No URLs."; exit 0; }
mkdir -p "$OUT_DIR"; : > "$SUMMARY"
ua="Mozilla/5.0 (compatible; research-pipeline-fetch/1.0)"

slug_for() {
  local sha tail
  sha=$(printf "%s" "$1" | sha1sum | cut -c1-10)
  tail=$(printf "%s" "$1" | sed -E 's|^https?://||; s|[^A-Za-z0-9._/-]|_|g; s|/+|__|g' | cut -c1-80)
  printf "%s_%s" "$sha" "$tail"
}

i=0
while IFS= read -r url; do
  [ -z "$url" ] && continue
  i=$((i+1))
  slug=$(slug_for "$url")
  html_path="${OUT_DIR}/${slug}.html"
  md_path="${OUT_DIR}/${slug}.md"
  echo "[$i] $url" >&2
  http_code=$(curl --silent --show-error --location --insecure --max-time 30 \
    --user-agent "$ua" --output "$html_path" --write-out "%{http_code}" "$url" || true)
  bytes=0; [ -f "$html_path" ] && bytes=$(wc -c < "$html_path" | tr -d ' ')
  if [ "${http_code:-000}" = "200" ] && [ "$bytes" -gt 0 ]; then
    python3 - <<PY > "$md_path" 2>/dev/null || true
import html2text, sys
with open("$html_path", "r", encoding="utf-8", errors="replace") as f:
    html = f.read()
h = html2text.HTML2Text(); h.body_width = 0; h.ignore_images = True
sys.stdout.write(h.handle(html))
PY
    printf -- "- [%d] \`%s\` → \`%s\` (HTTP %s, %s bytes)\n" "$i" "$url" "$html_path" "$http_code" "$bytes" >> "$SUMMARY"
  else
    printf -- "- [%d] \`%s\` → FAILED (HTTP %s, %s bytes)\n" "$i" "$url" "${http_code:-000}" "$bytes" >> "$SUMMARY"
  fi
done < "$URLS_FILE"
exit 0
```

Make the scripts executable: `chmod +x .github/scripts/*.sh .github/scripts/*.py`.

## Recap — the discipline in one breath

> Probe reachability. Fetch what's blocked via CI labeled issues. Read what comes back. Write the report with the **sources-status table at the bottom**. Delete fully-consumed raw fetches. Update the index. Note referenced clusters as future research with justification. Resume-fidelity for the next session lives in PLAN.md.
