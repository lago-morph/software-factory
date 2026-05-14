---
name: retro-coverage-audit-and-backfill
description: Find PR ranges in a repo's history that aren't covered by any retrospective ("dark zones"), and optionally produce synthetic back-filled retros for them from PR descriptions and surrounding contemporaneous retros. Use when the user asks "what's the coverage of retrospectives?", "which PRs aren't covered by any retro?", "find the dark zones", "back-fill the missing retro", "audit retro coverage", or wants a timeline of which retros covered which PRs. Pairs with the `self-retrospective` skill — this skill audits and back-fills; that skill authors contemporaneously. Synthetic retros produced by this skill are mandatorily flagged `SYNTHETIC / BACK-FILLED` in metadata and dated to the merge time of the last PR they cover, not the authoring date.
---

# Skill: retro-coverage-audit-and-backfill

Find PR ranges with no retrospective coverage in a repo's history. Optionally produce synthetic back-filled retros from PR descriptions and surrounding contemporaneous retros, with explicit provenance flags so readers can never mistake a reconstruction for a contemporaneous record.

The motivating problem: retrospectives are written at convenient checkpoints, not at deterministic session boundaries. Work that lands between checkpoints — especially during multi-PR bursts or weekend sprints — gets no narrative record. Three days later, no one remembers why a particular skill was authored, why a directory was reorganized, or what near-miss informed a tightened rule. The repo carries the PRs as audit trail but loses the *lessons*. A retro-coverage audit identifies these gaps mechanically; the back-fill capability lets you recover the narrative from PR descriptions while it's still reconstructable.

This skill earns its place because retrospectives are themselves a load-bearing primary source for the agents-file rules and ADRs that govern future sessions. Missing retros = missing rule-extraction = lessons get re-learned the hard way.

---

## Trigger detection

### Direct triggers — activate immediately

- "What's the coverage of retrospectives?"
- "Which PRs aren't covered by any retro?"
- "Find the dark zones in our retro history."
- "Back-fill the missing retro for [period]."
- "Audit retro coverage."
- "How many PRs did each retro cover?"
- "Give me a timeline of what retro covered what."
- `/retro-coverage` (and flag variants — see below).

### Proactive triggers — offer the skill without being asked

- User asks for "an approximate timeline of what retrospective covered what" (the audit half).
- User mentions a recent retro and asks whether earlier work has the same treatment.
- A retro is being authored and the previous retro is more than ~10 PRs behind the current PR head.

### Negative triggers — do NOT offer

- The repo has only one or zero retros (nothing to audit against).
- The repo has no `retrospective/` directory and no convention.
- The user is asking about a single PR, not coverage.

### Flag variants

| Invocation | Behavior |
|------------|----------|
| `/retro-coverage` | Default — produce the audit; ask the user before back-filling any zone. |
| `/retro-coverage --audit-only` | Audit and report; do NOT back-fill any zone regardless of size. |
| `/retro-coverage --zone <start>..<end>` | Skip audit; back-fill the named PR range directly. |
| `/retro-coverage --backfill-all` | Back-fill every dark zone the audit finds. Use with care; large zones produce large retros. |

---

## Mandatory output invariants

Two invariants apply to **every** synthetic retro this skill produces. Treat them as load-bearing — readers and future audit tooling depend on them.

### Invariant 1 — Synthetic retros are flagged in metadata.

Every synthetic retro must include the following line in its metadata block, near the top:

```markdown
- **Provenance**: SYNTHETIC / BACK-FILLED. Authored YYYY-MM-DD from PR descriptions and surrounding retros; not contemporaneous with the work it covers.
```

Replace `YYYY-MM-DD` with the authoring date (from `date -u +%Y-%m-%d`, NOT the retro's coverage date). The line is mandatory because a retro without the synthetic flag is indistinguishable from a contemporaneous record. That matters: contemporaneous retros report what the author observed; synthetic retros report what the author inferred from PR descriptions. Readers must be able to tell which they're looking at.

Also include an end-of-file marker that re-states the provenance:

```markdown
*End of synthetic retrospective `YYYY-MM-DD-NN`. Authored YYYY-MM-DD from PR descriptions and surrounding retros; not contemporaneous with the work it covers.*
```

### Invariant 2 — Date retros to coverage, not authorship; anchor the suffix to the last PR.

The synthetic retro's **filename date** and metadata **UTC date** field refer to the *work* the retro covers — specifically, the UTC date of the merge of the **last PR** in the coverage window. The authoring date appears only in the `Provenance` line.

The **filename suffix** is the number of the last PR in the coverage window — the same PR that anchors the coverage date. The two pieces of identity (date and last-PR) come from the same merge event, so the filename `retrospective/YYYY-MM-DD-PPP.md` reads as "the retro for the work that culminated in PR #PPP on YYYY-MM-DD".

A synthetic retro authored on 2026-05-14 covering PRs `#11..#25` (last PR `#25`, merged on 2026-05-11) is filed as `retrospective/2026-05-11-25.md`, NOT `retrospective/2026-05-14-25.md` and NOT `retrospective/2026-05-11-02.md`. The metadata block records both dates so future audits can attribute correctly:

```markdown
- **UTC date**: 2026-05-11 (dated to the merge time of the last PR covered: PR #25 merged 2026-05-11T12:48:03Z)
- **Last PR**: #25 (highest PR number in the zone — used as the filename suffix)
- **Provenance**: SYNTHETIC / BACK-FILLED. Authored 2026-05-14 from PR descriptions and surrounding retros.
```

**Filenames are append-only.** The PR-anchored suffix is mechanically derived from the zone's last PR; two synthetics for the same coverage date with different zones will naturally land on different filenames (different last PRs). If a synthetic happens to collide with an existing retro at the same date and same last-PR, append a lowercase letter suffix (`-a`, `-b`, …) — never rename or renumber an existing file. See the Step 8 collision handling.

---

## Step 0 — verify the UTC date (mandatory tool call)

The authoring date appears in the `Provenance` line; the coverage date is derived from PR merge times. Both must be correct. Verify the *authoring* date now via tool call before anything else:

```bash
date -u +%Y-%m-%d
```

```bash
python3 -c "import datetime; print(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d'))"
```

Prefer running both and confirming they agree. Save as `AUTHORING_DATE`. The retrospective must report which tool produced the date so a future reader can audit the provenance.

---

## Step 1 — inventory existing retros

```bash
ls retrospective/*.md
```

For each file, `Read` it and extract its **"Commit hashes by PR"** section. Build a mapping:

```
retro_file -> { covered: [PR#, PR#, ...], acknowledged: [PR#, ...] }
```

Where:
- **covered** = PRs explicitly named under an `### PR #N — <branch>` heading inside the retro's Commit-hashes section.
- **acknowledged** = PRs mentioned elsewhere in the retro body but not authored by that session (typically called out as "parallel-agent" work or "round-N PRs that landed on main between my sessions").

Also note **retro-commit-only PRs**: a PR whose sole purpose was to land a retrospective file. These are partially-covered — the retro discusses the work but the PR itself is the vehicle for the retro, not the work. They should not be flagged as dark.

---

## Step 2 — inventory all PRs

### Strategy A — GitHub MCP

```
mcp__github__list_pull_requests
  owner=<org>
  repo=<repo>
  state=all
  sort=created
  direction=asc
  perPage=100
```

### Handling oversized responses

If the result exceeds the tool-result token cap, the harness saves the full output to a file under `/root/.claude/projects/.../tool-results/`. The error message will name the path. **Do NOT re-run the call with narrower filters and accumulate partial pages — read the saved file out-of-band.**

```bash
python3 -c "
import json
data = json.load(open('/path/to/saved/file.txt'))
if isinstance(data, dict):
    data = data.get('pull_requests', data)
for pr in data:
    print(f\"#{pr['number']}\t{pr['state']}\tmerged={pr.get('merged_at','none')}\t{pr['head']['ref']}\t{pr['title']}\")
"
```

Extract the fields you need: `number`, `state`, `merged_at`, `head.ref`, `base.ref`, `title`. The saved file is the canonical source; the in-context partial result is not.

### Strategy B — `gh` CLI fallback

```bash
gh pr list --state all --limit 200 \
  --json number,title,headRefName,state,mergedAt,baseRefName \
  > /tmp/pr-list.json
```

---

## Step 3 — recognize the PR/issue namespace

GitHub PR numbers and issue numbers share a sequence. Gaps in the PR-number stream are not missing PRs — they are issues filed in those slots.

When the PR list shows `#1, #2, #3, #5, #7, #9, ...`, do NOT classify `#4, #6, #8` as missing. Confirm they are absent from the PR list itself (they will not appear with any state), then ignore them. They are not dark zones; they are issues.

This step is mechanical but easy to skip. The Step 5 dark-zone computation will produce false positives if you treat issue-number gaps as missing PRs.

---

## Step 4 — compute coverage

For each PR in the list, classify into one of:

- **Covered** — explicitly named in some retro's "Commit hashes by PR" section.
- **Retro-commit-only** — the PR landed a retrospective file (often partially-covered: the retro discusses the work but the PR itself is the retro-commit vehicle).
- **Acknowledged** — a retro mentions the PR in passing but doesn't author its work (e.g., parallel-agent PRs the session noted but didn't write).
- **Dark** — no retro discusses the PR at all.

A PR can be in only one category. Prefer the strongest classification (covered > retro-commit-only > acknowledged > dark).

---

## Step 5 — identify dark zones

Group contiguous dark PRs into **zones** by merge-time proximity. A zone break occurs when:

1. A covered, retro-commit-only, or acknowledged PR sits between two dark PRs; OR
2. A `> ~24 h` gap separates two dark PRs (likely a session boundary — the gap is silence, not a zone).

A zone of 1–2 dark PRs is usually not worth back-filling on its own. Surface it in the audit report, but suggest folding the brief mention into the next contemporaneous retro instead of authoring a synthetic.

A zone of `≥ 5` dark PRs is a strong back-fill candidate. The PR descriptions for ~5+ PRs typically carry enough narrative material to reconstruct a phase-decomposed retrospective.

---

## Step 6 — render the audit report (inline)

Standard shape, in this order:

1. **Per-retro coverage table.** Columns: retro file, UTC date, PRs directly covered, PRs acknowledged, window covered (first merge → last merge).
2. **Timeline view.** ASCII-art if useful; PR numbers in merge order with covered/dark/silence-gap markers.
3. **Dark-zones list.** For each zone: PR numbers, merge-time range, brief "what it looks like" line from PR titles.
4. **Headline numbers.** Total PRs, covered count, covered fraction, dark count, biggest gap duration.

Keep the report ~1 page of rendered output. If the user asked for audit-only (or didn't yet ask about back-filling), stop here and confirm before proceeding to Step 7.

---

## Step 7 — fetch PR descriptions for the zone (back-fill half)

Only run if back-filling is authorized — either by an explicit flag (`--zone`, `--backfill-all`), a follow-up user instruction, or proactive user confirmation.

Fetch each PR's description in a **single parallel block**:

```
mcp__github__pull_request_read method=get owner=<org> repo=<repo> pullNumber=<N>
```

One call per PR in the zone, all in one message. PR descriptions are the primary narrative source.

---

## Step 8 — determine date and last-PR anchor for the synthetic retro

```
COVERAGE_DATE = merged_at of the LAST PR in the zone, truncated to YYYY-MM-DD
PR            = number of the LAST PR in the zone
REPORT        = retrospective/${COVERAGE_DATE}-${PR}.md
SIBLING_DIR   = retrospective/${COVERAGE_DATE}-${PR}
```

Per Invariant 2, the **filename and metadata UTC-date both use `COVERAGE_DATE`**, NOT the authoring date. The authoring date appears only in the `Provenance` line. The **filename suffix is the last PR number** in the zone, not a per-day sequence counter.

### Collision handling

If `${REPORT}` already exists (i.e., a contemporaneous retro on that date already covered PR `#${PR}` as its last PR), append a lowercase letter suffix:

```bash
suffix=""
for letter in a b c d e f g h i j; do
  if [ ! -e "retrospective/${COVERAGE_DATE}-${PR}${suffix:+-$suffix}.md" ]; then break; fi
  suffix=$letter
done
REPORT="retrospective/${COVERAGE_DATE}-${PR}${suffix:+-$suffix}.md"
SIBLING_DIR="retrospective/${COVERAGE_DATE}-${PR}${suffix:+-$suffix}"
```

A collision is rare but possible — e.g., a contemporaneous retro on 2026-05-11 covered up through PR #25 and you're now synthesizing a *different* slice of that same range. In practice this almost always means your zone definition is wrong: re-examine the dark-zone bounds before back-filling, because the contemporaneous retro probably already covered the work. The letter-suffix fallback exists for genuine cases where two retros legitimately end at the same last PR (e.g., one narrative on infra, one on docs).

---

## Step 9 — synthesize the narrative

From the PR bodies, extract:

- **Phase decomposition** — group PRs by topic / branch / time-proximity into named phases. PRs on the same branch often form one phase; large bursts on related topics often form another.
- **Concrete numbers** — line diffs, commit counts, file counts, refutations caught, wall times, version bumps. PR descriptions are dense with these.
- **Lessons documented in the PR bodies** — anti-patterns the author called out, rule-tightenings, "we did X because we previously hit Y" reasoning. These transfer directly.
- **Inferred lessons** — when PR N+1 explicitly tightens a rule that PR N implicitly broke, the lesson is in that gradient. Self-reflection is reconstructable from these gradients even though PR descriptions are forward-looking. Flag inferred lessons as such ("inferable from PR-N+1's rule-tightening") rather than presenting them as observed.
- **Inferred meta-observations** — was the prior retro written mid-session? Compare its coverage window to the surrounding PR stream's continued activity.

---

## Step 10 — write the synthetic retro

Use the standard `self-retrospective` structure (Commit hashes by PR / Part 1 narrative / Metrics / Part 2 skills / Part 3 agents-file / Part 4 ADRs), with two synthetic-specific additions:

1. **The `Provenance` metadata line** (Invariant 1).
2. **A self-reflection section at the end**, narrating the lessons inferred from the PR gradients. This is where the synthesizer's own reading of the session lives — distinct from the phase narrative, which sticks to what the PRs documented.

Skip the per-skill spec authoring (and leave the sibling directory empty) **unless** the synthesized material directly demonstrates a skill the contemporaneous session never named. Synthetic retros should not fabricate skill specs from inferred material. If a candidate skill surfaces, list it in Part 2 with the priority but defer the spec to a future user-triggered authoring run. An empty sibling directory is acceptable for synthetic retros.

End the file with the synthetic-flagged end-of-file marker (Invariant 1).

---

## Step 11 — commit

```bash
git add retrospective/${COVERAGE_DATE}-${PR}.md retrospective/${COVERAGE_DATE}-${PR}/
git commit -m "retrospective: synthetic ${COVERAGE_DATE}-${PR} back-fill for dark-zone-N (PRs #<first>-#<last>)"
```

Do NOT open a PR unless the user has explicitly authorized one. Synthetic retros are local-history additions; the user typically wants to review on disk before they become a PR.

If the repo has a link checker (e.g., `.claude/skills/adr/scripts/check_adr_links.py`), run it on the new files before committing.

---

## Step 12 — echo inline summary

After writing artifacts:

- Path to the synthetic retro.
- PR range covered.
- Phase count + brief description.
- Skill / ADR candidates surfaced (titles only).
- Explicit reminder that the retro is flagged synthetic and dated to the coverage range.

Do not print the full retrospective inline — it's on disk; reference the path.

---

## Anti-patterns (never do these)

- **Synthesizing without the SYNTHETIC / BACK-FILLED flag.** Violates Invariant 1. Readers cannot distinguish reconstruction from contemporaneous record.
- **Dating the synthetic retro to the authoring date instead of the coverage date.** Violates Invariant 2. Breaks chronological browsing of `retrospective/*.md` against the PR stream.
- **Renaming a retro to reflect a different last-PR after authoring.** Filenames are immutable once written. A `2026-05-11-25.md` back-fill stays `-25` even if the zone is later re-examined and you'd anchor differently today. If you need to add a parallel retro for the same date and last-PR, use the letter-suffix collision rule (`-25-a`, `-25-b`, …).
- **Treating PR-number gaps as missing PRs.** GitHub PR and issue numbers share a namespace. Confirm absence from the PR list, then ignore.
- **Re-running an oversized MCP call with finer filters.** Parse the saved file out-of-band via `python3 -c ...`. The saved file is canonical; don't accumulate partial pages.
- **Over-relying on PR descriptions for self-reflection.** PR bodies describe what was done; they rarely confess what was botched. Self-reflection is *inferred* from gradients (PR-N+1 preventing what PR-N did) — mark inferences as such; do not present them as observations.
- **Authoring skill specs from inferred material.** A synthetic retro's sibling directory may legitimately be empty. Don't fabricate specs from material the synthesizer didn't witness; surface candidates in the user-facing summary instead.
- **Synthesizing for a zone of 1–2 PRs.** Surface in the audit; suggest folding into the next contemporaneous retro rather than authoring a low-content synthetic.
- **Opening a PR for the synthetic retro without explicit user authorization.** Synthetic retros are local-history additions; the user typically wants to review on disk first.
- **Hand-curating PR coverage from the GitHub UI.** The audit must run against the full PR-list response, not a hand-picked subset. Otherwise dark zones are easy to overlook.

---

## Acceptance criteria

1. **Coverage is computable.** After audit, every PR in the repo's history is classified into one of: covered, retro-commit-only, acknowledged, dark. The classification can be verified by `grep`-ing the relevant retro for the PR number.
2. **Dark zones are correctly bounded.** Zones don't span across covered/acknowledged PRs, and zones don't span across silence gaps > ~24 h.
3. **Synthetic retros are auditable.** Metadata block names the authoring date, the provenance, and the date of the work it covers (Invariant 1). The filename matches the coverage date (Invariant 2).
4. **PR/issue namespace is handled.** Numbers absent from the PR list are not flagged as missing PRs.
5. **Inline audit report is reviewer-friendly.** Per-retro table + timeline + dark-zone list + headline numbers, all in one reply, ~1 page of rendered output.

---

## See also

- `.claude/skills/self-retrospective/SKILL.md` — the canonical retro-authoring skill. This skill's output format mirrors that skill's structure exactly, with the added SYNTHETIC / BACK-FILLED metadata flag.
- `.claude/skills/adr/SKILL.md` — for any of the proposed ADRs surfaced by the audit or synthesis that the user decides to author.
- `spec/SPEC.md` — implementation-grade spec with extended rationale and worked examples.
