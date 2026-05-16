# Spec: `mhtml-image-pass`

## Intent

When the agent drains an MHTML (or any web-archive format that wraps a page's resources alongside the HTML — `.mht`, `.eml`, Save-Page-As-Complete) into a research report, the natural first move is `html2text` on the body. That move silently strips every `image/*` MIME part. For technical blog posts — Anthropic engineering, Kiro deep-spec-analysis, arXiv html renderings — the diagrams routinely carry operational details (named solvers, sample counts, decision shapes, taxonomies) that the prose around them does not. A "drain" that processes the text and deletes the source file is *not* complete; the agent has thrown away the load-bearing half without knowing it.

This skill makes the image-pass mandatory: before any MHTML source file is deleted, the agent walks its MIME parts for embedded images, extracts the substantive ones, views them via the `Read` tool's native image rendering, and folds any image-only details into a clearly-demarcated "Image-anchored details" sub-block of the consuming report. Then — and only then — the source file is removed.

The cost is small (one Python extraction script + N image reads, where N is typically 3–10). The cost of skipping it is high: the Kiro session's first drain looked complete and was committed; the user had to push back to recover six figures' worth of mechanizable detail (per-bug-class detection-mechanism mapping, Z3-as-named-solver, N=10-sample semantic-entropy classifier, Tier-1 abductive-refinement vocabulary, three named SMT finding types). Each of those is portable beyond Kiro; missing them silently is the precise failure mode this skill prevents.

## Trigger

**Direct user phrases:**

- *"use image analysis tools on the images"*
- *"extract figures from this MHTML"*
- *"the figures matter"*
- *"why did you miss the diagrams?"*

**Proactive triggers — activate without being asked:**

- Any drain that processes a `.mhtml` / `.mht` / `.eml` / web-archive source file.
- Any drain whose source URL is on a host known to embed figures (Anthropic engineering, Kiro, arXiv `/html/`, Substack-with-images, vendor blog posts about ML/SE mechanics).
- Any drain whose subagent report-back says "skimmed past navigation chrome" but doesn't mention figures.

**Negative triggers — do NOT activate:**

- Sources that are demonstrably text-only (plain `.txt`, transcripts, IETF RFCs, code).
- Sources whose figures are demonstrably decorative (author headshots, logos, wordmarks).
- PDFs — the `Read` tool handles those natively when invoked with the `pages` parameter; image-pass discipline doesn't apply.

## Inputs

- **Source path**: absolute path to the MHTML file (or to a directory containing one or more MHTML files). May be inside the repo or in a scratch path like `/tmp/`.
- **Target report path**: the consuming `research/NN-*.md` (or `research/followup/NN-*.md`) the image content will fold into.

## Outputs

- A scratch directory (default `/tmp/<source-stem>-images/`) holding the extracted images as files. Each filename embeds a sha1 prefix + the original `Content-Location` slug.
- A printed manifest line per image listing its filename, content type, byte count, and source URL.
- Updates to the target report:
  - A new sub-block titled **"Image-anchored details"** appended to (or inserted near the end of) the section the report-author was already writing about this source.
  - The target report's revision-notes block at the top updated with the image-drain entry.
  - The target report's sources-reviewed row for the source URL updated to note the image pass.
- Cleanup: the scratch directory is removed once the report edits are committed.

## Workflow

1. **Locate the source MHTML.** If the source was already deleted in an earlier commit, restore it to `/tmp/` with `git show HEAD~N:"<path>" > /tmp/<stem>.mhtml`. Prefer `git show` over `git checkout` — restoring to a scratch path keeps the working tree clean.

2. **Run the extraction script** (canonical form below) to dump every `image/*` part to a scratch directory. The script must (a) walk every part via `email.walk()`, (b) skip non-image parts, (c) decode via `part.get_payload(decode=True)`, (d) save with a sha1-prefixed filename that preserves the original `Content-Location` for traceability, and (e) print a manifest of what was extracted.

   ```python
   import email, hashlib, mimetypes
   from pathlib import Path

   src = Path("/tmp/<stem>.mhtml")
   out = Path(f"/tmp/{src.stem}-images")
   out.mkdir(exist_ok=True)
   with src.open("rb") as f:
       msg = email.message_from_bytes(f.read())
   i = 0
   for part in msg.walk():
       ctype = part.get_content_type()
       if not ctype.startswith("image/"):
           continue
       payload = part.get_payload(decode=True)
       if not payload:
           continue
       loc = part.get("Content-Location", "")
       ext = mimetypes.guess_extension(ctype) or ".bin"
       if ext == ".jpe": ext = ".jpg"
       digest = hashlib.sha1(payload).hexdigest()[:10]
       i += 1
       name = f"img-{i:02d}-{digest}{ext}"
       (out / name).write_bytes(payload)
       print(f"{name:30s} {ctype:15s} {len(payload):>9} bytes  src={loc}")
   ```

3. **Triage the manifest.** Author headshots (filenames containing `authors/`, `team/`, `avatar/`, dimensions ≤ ~25 KB) and brand assets (`wordmark`, `logo`, `favicon`) are skipped. Everything else is substantive until proven otherwise.

4. **View each substantive image** via `Read` on its filesystem path. The `Read` tool renders PNG/JPG natively as a vision input — no OCR, no vision-API wrappers. Send the reads in parallel where possible (one tool-use block, N calls).

5. **Synthesize image-only details.** For each figure, ask: *what does this figure show that the prose drain didn't?* Capture: named entities (specific solvers, libraries, model names), quantitative shapes (sample counts, before/after counts, threshold values), decision structures (classifier buckets, taxonomy mappings), worked-example diagnostics (specific scopes, witness scenarios), vocabularies (named classifications used in trees or tables).

6. **Update the target report** by inserting an **"Image-anchored details"** sub-block at the end of the section that was already drafted from the text drain. Use a bulleted list, one bullet per figure. Each bullet starts with the figure title in italics so a reader can locate the original. Quote verbatim where the figure carries language; tabulate where the figure carries structure.

7. **Update the revision-notes block** at the top of the target report with a one-paragraph entry naming the image-drain follow-up and listing the load-bearing details added.

8. **Update the sources-reviewed table row** for the source URL with an "Image-drain follow-up <DATE>" note describing what was extracted and where it landed in the report.

9. **Commit** the report-only edits as a focused follow-up commit. Suggested message: `<Source-slug> image drain: fold figure-only details into <report-path>`.

10. **Clean up** the scratch directory: `rm -rf /tmp/<stem>.mhtml /tmp/<stem>-images`. Scratch artifacts are never committed.

## Concrete examples

### Example 1 — Kiro deep-spec-analysis MHTML (the session that produced this skill)

**Input:** `research/manual/Requirements analysis_ catching requirement bugs before they become code - Kiro.mhtml` (2.3 MB).

**Step 1 — restore from git** (the file had already been deleted in the prior commit):

```bash
git show HEAD~1:"research/manual/Requirements analysis_ catching requirement bugs before they become code - Kiro.mhtml" > /tmp/kiro-deep-spec.mhtml
```

**Step 2 — extract** produced 12 images at `/tmp/kiro-images/`. Manifest:

```
img-01-ddff02b45d.png   image/png   251207 bytes  src=.../4_logical_analysis.png
img-02-d52da4030e.png   image/png   152738 bytes  src=.../5_semantic_entropy.png
img-03-971544afe8.png   image/png   300530 bytes  src=.../2_refinement_before_after.png
img-04-d35a1f7eea.png   image/png   270551 bytes  src=.../diagram-vertical.png
img-05-b489cb2ec3.png   image/png   100291 bytes  src=.../3_pipeline_overview.png
img-06-634c92a499.png   image/png   183333 bytes  src=.../1_bug_taxonomy.png
img-07-3ad1562eb3.jpg   image/jpeg   20285 bytes  src=.../authors/remi-delmas.jpg
... (5 more author headshots + 1 wordmark)
```

**Step 3 — triage:** 6 substantive PNGs (the `_bug_taxonomy`, `_refinement_before_after`, `_pipeline_overview`, `_logical_analysis`, `_semantic_entropy`, and `diagram-vertical` figures); 5 author headshots + 1 wordmark skipped.

**Step 4 — view:** six parallel `Read` calls on the PNG paths.

**Step 5 — synthesize:** six image-only details surfaced:

1. Per-bug-class → detection-mechanism 1:1 mapping (LLM Rewriting / Semantic Entropy / SMT Solver bound to the four bug classes).
2. Per-stage toolchain attribution: `LLM + Abductive`, `LLM + SMT Clustering`, **Z3** SMT Solver.
3. BEFORE→AFTER 5→8 (2U/3A/3A) refinement count on the Delete-Property worked example, with three machine-emitted lint flags (`conflict`, `impl`, `EARS`).
4. Semantic-entropy three-bucket TRUST/CLARIFY/ABSTAIN classifier over N=10 LLM samples → 2 clusters, plus an A/B disambiguation-question template + semantic-diff row pattern.
5. Three named SMT finding types (direct contradiction / case-split contradiction / completeness gap) with minimal scopes and witness scenarios.
6. Tier-1 abductive-refinement classification vocabulary (Test Blocker / State Definition / Precision Gap) bound to NEW vs AMENDED criteria.

**Step 6 — fold:** added an "Image-anchored details" sub-block to `research/12-adjacent-ecosystem.md` §2.5, ending with a "Why this matters for the corpus" paragraph naming each detail's portability hook.

**Steps 7–9 — bookkeeping + commit:** revision-notes block updated; sources-reviewed row updated; commit `733d910`.

**Step 10 — cleanup:** `rm -rf /tmp/kiro-deep-spec.mhtml /tmp/kiro-images`.

### Example 2 — Anthropic engineering post drain (hypothetical but parallel)

**Input:** an `.mhtml` of an Anthropic engineering blog post with a system-architecture diagram and a performance-comparison chart.

**Expected outputs:**

- 2 substantive PNGs (the architecture diagram and the chart), saved to `/tmp/<post-slug>-images/`.
- Both viewed via `Read`; the architecture diagram likely surfaces a named middleware component or queueing model the prose only hints at; the chart surfaces specific p50/p95 numbers and the model versions compared.
- "Image-anchored details" sub-block in `research/23-anthropic-engineering-trilogy.md` listing the architecture-component name + the p50/p95 numbers as a verbatim table.

The skill's discipline doesn't change with the host — Kiro, Anthropic, arXiv, vendor blog X — only the triage step changes (different naming conventions for headshots and wordmarks per host).

## Anti-patterns

- **Don't delete the source file before the image pass runs.** The Kiro session got rescued only because the deletion was recoverable from `HEAD~1`. If the source had been deleted across multiple intervening commits the recovery would have taken more effort. Image-pass before delete is the cheap version.
- **Don't try to `Read` the `.mhtml` itself expecting embedded images to render.** The `Read` tool sees the MIME envelope as text; the images are base64 blobs inside it. Extraction to filesystem paths is the only path that triggers the visual rendering.
- **Don't ship a half-quality image pass to look thorough.** If a figure is illegibly low-resolution or chopped, name that limitation in the sub-block ("Figure showed an N×M table; cells too small to read; numbers reported are from the prose context") rather than fabricating details.
- **Don't fold image-only details inline with the prose drain.** Keep them in a clearly-demarcated **"Image-anchored details"** sub-block. The provenance distinction matters for any future audit pass that asks *"which claims came from the text vs the figures?"*
- **Don't commit the scratch directory.** It contains potentially-copyrighted vendor images; the report's verbatim quotes + structural descriptions are fair-use synthesis, but the raw figures themselves should stay out of the repo.

## Acceptance criteria

1. After running the skill, every `image/*` part of the source MHTML appears in the manifest (count matches `grep -c "Content-Type: image/" <source>`).
2. Every substantive figure (i.e., every image not classified as a headshot, logo, or wordmark) has a corresponding bullet in the target report's "Image-anchored details" sub-block.
3. The target report's revision-notes block at the top has an entry naming the image-drain follow-up dated to the day of the work.
4. The target report's sources-reviewed row for the source URL has an "Image-drain follow-up" annotation.
5. The scratch directory is removed before the session ends; `git status` shows no untracked files under `/tmp` or outside the report path.

## Files this skill creates / modifies

- `/tmp/<source-stem>.mhtml` — restored source (scratch, deleted at end).
- `/tmp/<source-stem>-images/` — scratch directory with extracted images (deleted at end).
- `research/NN-<slug>.md` or `research/followup/NN-<slug>.md` — appended "Image-anchored details" sub-block + revision-notes-block update + sources-reviewed-row update.

Nothing is added to `research/manual/`, `research/fetched/`, or any other persistent repo path. The image pass is non-destructive to the rest of the corpus.
