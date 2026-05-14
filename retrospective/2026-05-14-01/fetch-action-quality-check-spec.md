# Spec: `fetch-action-quality-check`

## Intent

The `fetch-blocked-urls` GitHub Actions workflow reports HTTP 200 for many URLs that did not actually succeed: Cloudflare JS-challenge bodies ("Enable JavaScript and cookies to continue", "Just a moment..."), 404 pages disguised by CSS/JS bloat (the page body is empty but the HTML is 26 KB), JS-rendered SPA shells (the document has `Loading...` placeholders where the body should be), gzip-compressed tarballs misclassified as HTML (4.6 MB of binary noise as the `.md` sibling). Every drain pass in this project has wasted subagent tokens reading these stubs before noticing they were empty. This skill inserts a mandatory body-inspection pass between the fetch-action's deposit and the drain subagents' dispatch, classifying each file as `valid | stub | binary | unreadable` and feeding only `valid` files to the drain.

In the 2026-05-14 round-8 drain, this check (run by the orchestrator manually) saved at least 4 subagent dispatches and unlocked the CaMeL paper body recovery (the e-print archive was a gzip mis-extracted as HTML — invisible to a status-code-only check). Codifying the check makes it standard.

## Trigger

**Direct triggers:**
- "Quality-check the fetched files"
- "Inspect what's in `research/fetched/issue-N`"
- "Before drain, check for stubs"

**Proactive triggers (use without being asked):**
- Immediately after a `fetched/issue-N` branch is merged or cherry-picked into the working branch and before any drain subagent is dispatched.
- When iterating on a fetch issue that previously returned mixed-quality content.

**Negative triggers (skip):**
- Single-URL ad-hoc fetches via WebFetch (the body is in the tool result already).
- Files that have already been classified by a prior session and recorded in `research/blocked-urls-round-N.md`.

## Inputs

- A directory of fetched files (typically `research/fetched/issue-<N>/`) containing paired `.html` + `.md` files produced by `.github/scripts/fetch_urls.sh`.
- Optional: the issue body text from the fetch issue, listing the original URL → filename mapping (useful when filenames are slug-truncated).

## Outputs

For each file, a classification: `valid | stub_404 | stub_cloudflare | stub_js_spa | binary_mis_extracted | unrecoverable`. Plus:

- A per-file disposition: feed-to-drain, delete-as-documented-failure, escalate-to-manual-recovery (e.g. gunzip+tar for gzip mis-extractions).
- A row appended to `research/blocked-urls-round-<N>.md` for every non-`valid` file documenting what went wrong and what recovery is possible.
- Deleted stub files (via `git rm`) staged for the orchestrator's next commit.
- Optional: extracted content moved to `reference-only/<slug>/` for content that was recovered out-of-band (e.g. arXiv e-print → see `arxiv-e-print-recovery` skill).

## Workflow

1. **List candidate files**:
   ```bash
   ls research/fetched/issue-<N>/*.html
   ```
2. **Identify pairs and singletons**: for each `.html`, check whether a `.md` sibling exists.
   - `.html` without `.md` sibling → the action's html2text extraction failed; this is a strong signal of a JS-challenged body or binary content. Investigate first.
   - Paired `.html` + `.md` → likely succeeded but still needs body inspection.

3. **Inspect `<title>` and visible body** for each file:
   ```bash
   grep -oE "<title>[^<]+</title>" <file>
   wc -c <file>
   ```
   Patterns to flag:
   - `<title>Just a moment...</title>` → Cloudflare JS challenge (`stub_cloudflare`).
   - `<title>404 ...</title>`, `<title>Not Found</title>`, body containing `Page not found`, `HTTP Status: 404` → 404 page (`stub_404`).
   - Body containing `Enable JavaScript and cookies to continue` → Cloudflare JS challenge (`stub_cloudflare`).
   - Body length under ~2 KB AND no useful headings/text → likely a stub.
   - `.md` content is mostly nav chrome + footer + repeated `Loading...` strings → JS-SPA shell (`stub_js_spa`).

4. **Detect binary mis-extraction**:
   ```bash
   file <file>.html
   ```
   - If output contains `gzip compressed data` → the action mis-classified gzip as HTML. Escalate to manual recovery (see `arxiv-e-print-recovery` for arXiv; analogous routes for other hosts).
   - If output contains `PDF document` → PDF binary; html2text cannot extract. Recovery requires pdfminer/pdf2text or a different fetch route.

5. **Verify titles match expectations**: a deceptive 404 page may have a non-404 title set by JavaScript (e.g. factory.ai's product 404 has `<title>Factory.ai</title>`). Always corroborate with the visible body, not just the title.

6. **Classify each file**:
   - `valid` → keep, feed to drain subagent.
   - `stub_404`, `stub_cloudflare`, `stub_js_spa` → record in `research/blocked-urls-round-<N>.md` with HTTP status + body class + recovery route (Path B browser-save / Wayback / etc.), then `git rm`.
   - `binary_mis_extracted` → escalate to manual recovery skill; don't delete the `.html` until recovery is attempted.
   - `unrecoverable` → record in blocked-urls log + `unfetched-sources.md`; `git rm`.

7. **Emit a per-file table** for the orchestrator + subagents:
   ```markdown
   | File | URL | Classification | Disposition |
   |---|---|---|---|
   | 461d7478ae_...cognition.ai...devin.html | https://www.cognition.ai/blog/devin | stub_404 | git rm + log |
   | 29366c44d4_arxiv.org__e-print__... | https://arxiv.org/e-print/2503.18813 | binary_mis_extracted | escalate to arxiv-e-print-recovery |
   ```

8. **Commit the cleanup** (orchestrator may batch this with the drain commits — the skill stages but does not commit).

## Concrete examples

### Example 1 — round-8 issue #41 quality check (real session material)

Input: `research/fetched/issue-41/` containing 27 paired `.html`+`.md` files and 4 singleton `.html`s.

Inspection:
- 4 singletons: 3× `openai.com/index/*` and 1× `pli.princeton.edu`. Visible text in each: "Enable JavaScript and cookies to continue" (the OpenAI three) or `<title>Just a moment...</title>` (the Princeton one). All `stub_cloudflare`.
- 27 paired files: titles look real, bodies have substantial markdown headings. All `valid`.

Output table:
```
| openai.com/index/harness-engineering | stub_cloudflare | git rm + record in round-8 log |
| openai.com/index/unlocking-the-codex-harness | stub_cloudflare | git rm + record |
| openai.com/index/introducing-swe-bench-verified | stub_cloudflare | git rm + record |
| pli.princeton.edu/...swe-bench | stub_cloudflare | git rm + record |
| (27 valid files) | valid | feed to drain |
```

Recorded in `research/blocked-urls-round-8.md` under "Lesson R8.2 — `openai.com/index/*` returns HTTP 200 but with a Cloudflare JS-challenge body."

### Example 2 — round-8 issue #42 CaMeL discovery (real session material)

Input includes `29366c44d4_arxiv.org__e-print__2503.18813.html` (2.5 MB) and its `.md` sibling (4.6 MB of binary noise).

Inspection:
- `file 29366c44d4_..._e-print__2503.18813.html` → `gzip compressed data, last modified: Wed Jun 25 00:30:46 2025, from Unix, original size modulo 2^32 4157440`. Classification: `binary_mis_extracted`.
- `.md` content is binary garbage (html2text on gzip).

Disposition: escalate to `arxiv-e-print-recovery`. After recovery, `git rm` both files.

This was the round's biggest unlock — the CaMeL paper body had been documented as "accept the gap" in round 7 R7.2; the body-inspection check surfaced it as a recoverable gzip mis-extraction rather than an unrecoverable failure.

## Anti-patterns

- **Status-code-only validation.** HTTP 200 is necessary but NEVER sufficient. Always inspect body. (Session: 4 `openai.com/index/*` 200s were Cloudflare stubs.)
- **Trusting `<title>` alone.** Modern SPAs set the title via JavaScript before the body fails to load. (Session: `factory.ai/product` had `<title>Factory.ai</title>` but body was "These are not the droids you are looking for…")
- **Treating size as a quality signal.** A 26 KB 404 page is just a 404 page with CSS bloat. (Session: cognition.ai/blog/devin was 26 KB and entirely useless.)
- **Reading the `.md` file without sanity-checking it.** html2text on gzip produces 4.6 MB of noise that *looks* like content if you only sample the first 100 chars without `od -c` or `file`.
- **Skipping the body-inspection because "the file is big enough to be real."** The skill exists to catch silent failures; the cost of running it is seconds; the cost of skipping it is subagent tokens.

## Acceptance criteria

1. Every file in `research/fetched/issue-<N>/` is classified before any drain subagent is dispatched.
2. Every non-`valid` file has a row in `research/blocked-urls-round-<N>.md` recording its classification, HTTP status, body class, and recovery route.
3. No drain subagent receives a stub or binary-mis-extracted file as an input.
4. The classification table is printed inline (or referenced) so the orchestrator can audit per-file decisions before commit.
5. The fetch-action's misclassification of gzip-as-html is detected at the body-inspection stage 100% of the time (use `file` not extension).

## Files this skill creates / modifies

- **Modifies**: `research/blocked-urls-round-<N>.md` — appends one row per non-valid file plus a "Lessons" subsection if a new failure class is observed.
- **Modifies (deletes)**: `research/fetched/issue-<N>/<stub-file>.{html,md}` — staged for orchestrator's commit.
- **Reads only**: `research/fetched/issue-<N>/*.{html,md}` — content for inspection.
- **May escalate to**: `arxiv-e-print-recovery` skill (when a gzip is detected at an arXiv URL).
