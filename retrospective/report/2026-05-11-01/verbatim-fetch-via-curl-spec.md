# Spec: `verbatim-fetch-via-curl`

## Intent

When an agent needs verbatim content from the web (SKILL.md files for adoption, source files for citation, quote material for research), `WebFetch` cannot be trusted to return raw bytes — it passes the response through a small model that may summarize or paraphrase. For verbatim content, use `curl` (or equivalent) via `Bash` to retrieve raw bytes.

In this session, three SKILL.md files were fetched in parallel via WebFetch. Two returned verbatim content. The third returned a paraphrased summary that read as: *"This is a reference guide that helps with..."* — clearly a third-party description rather than the file's own first-person voice. The agent caught this and re-fetched the file via `curl`. Had the agent missed the substitution, an incorrect / paraphrased SKILL.md would have been installed.

This skill captures the operating rule and the verification step.

## Trigger

**Direct user requests:**
- "Fetch the raw file"
- "Get the verbatim content"
- "curl this for me"

**Proactive triggers (the agent should reach for curl, not WebFetch, when):**
- Fetching a file whose content will be saved to disk or quoted verbatim.
- Fetching `SKILL.md`, `README.md`, source-code files, or any markdown intended for round-trip use.
- A previous WebFetch result looked summarized, paraphrased, or shorter than expected.
- Fetching multiple files where any divergence between them would be hard to spot.

**Negative triggers (WebFetch is fine):**
- The agent needs the gist of a long article ("summarize this blog post").
- The agent needs to navigate a directory listing on github.com (the HTML tree page renders short and uniformly).
- The agent is researching, not transcribing.

## Inputs

- A URL (or list of URLs).
- An expected target path on disk (so the file can be saved + size-checked).

## Outputs

- One file on disk per URL fetched, with verified byte count.
- A short log line per fetch: `URL → path → size`.

## Workflow

1. **Choose the right tool.** If the user needs verbatim content, use `curl` via `Bash`. If they need a summary, use `WebFetch`. Default to curl when in doubt.
2. **Issue the fetch.** Use a realistic User-Agent if the source is sensitive to one:
   ```bash
   curl -sf -o "$DEST/$NAME" "$URL"
   # or with retries:
   curl -sf --retry 3 --retry-delay 2 -o "$DEST/$NAME" "$URL"
   ```
3. **Verify size.** A suspiciously small response usually means a 404 or block page.
   ```bash
   size=$(wc -c < "$DEST/$NAME")
   if [ "$size" -lt 200 ]; then
     echo "ERROR: fetched file suspiciously small: $size bytes" >&2
     head -c 500 "$DEST/$NAME"
     exit 1
   fi
   ```
4. **Verify content.** For SKILL.md / source files, the first line should match expectations (frontmatter delimiter `---`, shebang, etc.). Bail out if it doesn't.
5. **For parallel fetches**, use background subshells and `wait`:
   ```bash
   for f in $URLS; do
     curl -sf -o "$DEST/$(basename $f)" "$f" &
   done
   wait
   ```
6. **If the response looks like a Cloudflare challenge** (HTML with `<title>Just a moment...</title>` or "challenge-platform" markers), do NOT save it as the intended file. Fall back to the `fetch-blocked-urls` skill instead.

## Concrete examples

### Example 1 — three skills in parallel (this session)

```bash
BASE="https://raw.githubusercontent.com/lago-morph/ai-skills/main/skills"
DEST=".claude/skills"
mkdir -p "$DEST"/{self-retrospective,parallel-subagent-fanout,subagent-prompting}

# Parallel fetch
for s in self-retrospective parallel-subagent-fanout subagent-prompting; do
  curl -sf -o "$DEST/$s/SKILL.md" "$BASE/$s/SKILL.md" &
done
wait

# Verify
for s in self-retrospective parallel-subagent-fanout subagent-prompting; do
  size=$(wc -c < "$DEST/$s/SKILL.md")
  echo "$s: $size bytes"
  if [ "$size" -lt 1000 ]; then
    echo "  WARNING: smaller than expected"
  fi
done
```

Output (this session's actual numbers):

```
self-retrospective: 12735 bytes
parallel-subagent-fanout: 12278 bytes
subagent-prompting: 8564 bytes
```

All three within expected range. If one had come back at 200 bytes, the script would have flagged it.

### Example 2 — when WebFetch fails verbatim

A WebFetch call to `https://raw.githubusercontent.com/lago-morph/ai-skills/main/skills/subagent-prompting/SKILL.md` returned:

> *"This skill orchestrates parallel multi-agent workflows by decomposing goals into independent subtasks..."*

That's a summary, not the file. The file itself starts with a YAML frontmatter block:

```
---
name: subagent-prompting
description: Reference card and brief generator...
---
```

After switching to curl, the file came back verbatim. The summary form does NOT preserve frontmatter, doesn't preserve the exact wording, and would have failed both the harness's skill-registration parser and any down-stream copy-paste use.

### Example 3 — directory listing via WebFetch is OK

For listing files in a GitHub directory, WebFetch is fine because the output is short and uniform:

```
# WebFetch on https://github.com/lago-morph/ai-skills/tree/main/skills/parallel-subagent-fanout
Returns: spec, README.md, SKILL.md
```

This is the right tool for that job — the small model summarizes the HTML directory page into bare names, which is what you wanted. Don't use curl here unless you specifically need the HTML.

## Anti-patterns

- **Trusting WebFetch output without size verification.** The summarized SKILL.md looked reasonable until the first-person voice was missing.
- **Using WebFetch when you have curl available.** Curl is faster, deterministic, and saves a file on disk. WebFetch is for "give me the gist of this page" — a different problem.
- **Mixing the two for the same file.** Don't have curl save it then WebFetch the same URL "to confirm". Two truths, one file. Whichever you save is the one used downstream.
- **Skipping the size check.** A 200-byte file where you expected 6000 means failure. The check catches 404s, Cloudflare challenges, and silent truncations.

## Acceptance criteria

1. For verbatim content, curl is used via `Bash`, not WebFetch.
2. Every fetched file is size-verified against a sensible minimum.
3. Cloudflare-challenge responses are detected (via title / body markers) and re-routed to the `fetch-blocked-urls` skill rather than being saved as the intended file.
4. Parallel fetches use background subshells + `wait`, not sequential calls.
5. The agent's working notes / commit message names which tool (curl vs WebFetch) was used per fetch.

## Files this skill creates / modifies

- The fetched content (one file per URL, at agent-specified paths).
- Optionally: an entry in the agent's working notes log per fetch.
