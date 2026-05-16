# AGENTS.md suggestions — 2026-05-16-57

These are proposed additions to the project's agents file (typically `AGENTS.md` at the repo root). The repo does not yet have an `AGENTS.md`; if you adopt these, this round's accepted rules would form the seed of one. Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened) in this session.

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: PR draft-status default policy

### Proposed addition

> **PR draft-status default policy.** "Before opening a PR, check the repo's prior-PR draft convention via `mcp__github__list_pull_requests` (or `gh pr list --state merged --limit 5`). If the most recent merged PRs on this repo were non-draft, open the new PR as non-draft. If the environment's system prompt has a 'create as draft' default, mention it once inline before applying or overriding it, so the human can correct course before the PR lands."
>
> *Grounded in: PR #57 was opened as a draft per the env-prompt default ("Create the pull request as a draft. You do not need to ask the user first."); user immediately pushed back ("why in the world are you using draft pull requests?"). Prior PRs on this repo (#56, #46, #44, #43) had all been merged non-draft, so the env default was obviously wrong for this repo's convention.*

### Why this earns its place in your agents file

The env-prompt's "default to draft" instruction is correct for some environments (early-development repos where draft-as-default is the norm; environments where human review is gated on the draft → ready transition). It is wrong for this repo, where every recent PR has been merged non-draft and the user expects ready-for-review as the default. The friction is small per-incident — one update_pull_request call to flip the status — but it recurs every time a PR opens, and the user notices every time.

The marginal cost of adopting this rule is two tool calls per PR (one to list prior PRs, one to mention the override decision). The marginal saving is one round-trip of friction per PR opened. For a project that opens 1–2 PRs per session, the ratio is favorable. The rule also makes the env-vs-repo asymmetry visible to the user, which is the only way they can ever override the env-prompt-level default.

---

## Suggestion 2: MHTML drains require an image-extraction pass

### Proposed addition

> **MHTML drains require an image-extraction pass.** "When draining an `.mhtml` / `.mht` / web-archive source file into a report, treat `html2text` (or any text-only conversion) as completing only the *text* half of the drain. Before the source file is deleted from `research/manual/`, run an image-extraction pass over its `image/*` MIME parts: walk the parts via Python `email.walk()`, save each image to a scratch directory, view substantive figures via the `Read` tool (native PNG/JPG rendering), and fold any image-only details into a clearly-demarcated *Image-anchored details* sub-block of the consuming report. Then delete the source file. The `mhtml-image-pass` skill automates this discipline."
>
> *Grounded in: the Round-9 Kiro drain processed `Requirements analysis... .mhtml` via html2text and committed/deleted the source. Six embedded figures were silently stripped, including the per-bug-class detection-mechanism mapping, Z3-as-the-named-solver, the N=10-sample/3-bucket semantic-entropy classifier, three named SMT finding types, and the Tier-1 abductive-refinement classification vocabulary. The user had to push back to recover this material; a second commit (`733d910`) was required.*

### Why this earns its place in your agents file

Technical-blog content routinely puts the load-bearing operational details in figures: named tools, sample counts, decision shapes, taxonomies. The text around them is summary; the figures are the spec. An html2text-only drain looks complete and *is* complete for blog posts with decorative figures, but the agent has no way to know which case applies before extracting and viewing the images. The default discipline therefore has to be "always extract."

The cost of the discipline is one Python script + N image-reads (typically 3–6 substantive images per technical blog post). The cost of skipping it is what happened on PR #57: a second commit just to recover what should have been included the first time, plus the broken-trust signal to the user ("why did you miss the diagrams?"). Asymmetric in the discipline's favor.

---

## Suggestion 3: Parallel subagent dispatch pre-allocates shared registry slots

### Proposed addition

> **Parallel subagent dispatch pre-allocates shared registry slots.** "When dispatching N≥2 subagents in parallel, and any subagent's brief allows it to propose new entries to a shared registry (failure-mode numbers `F36+`, ADR numbers, report numbers, ID ranges, semantic-version bumps), pre-allocate non-overlapping slot ranges to each subagent in the dispatch brief. Include an explicit *Registry allocation (your exclusive range)* block in each brief naming the slot range that subagent is exclusively authorized to use. Do not rely on `'don't propose F36+ unless flagged as proposal'` style negative-with-exception instructions — subagents follow positive allocations reliably and exception-clauses unreliably. See `subagent-registry-preallocation` skill."
>
> *Grounded in: PR #57's Round-9 dispatch. Subagent A (RE/SE foundations) and Subagent B (LLM+RE academic) each independently proposed F36 and F37 for different phenomena; collision was caught at lead-agent integration and documented in PLAN.md §3.6 as a triage item for the next session. Pre-allocation (A: F36–F39, B: F40–F43) would have eliminated the collision entirely.*

### Why this earns its place in your agents file

Subagents run without visibility into what their peers are doing. When two subagents both look at the catalog at dispatch time and see F35 as the highest committed number, both will independently propose F36 unless the brief specifies otherwise. The instinct to write "don't invent F36+ without flagging as a proposal" is reasonable but does not work — the brief is ambiguous about which subagent gets the next number, so both reach for it.

The marginal cost of adopting this rule is one block per brief + one pre-flight high-water-mark query (one grep or one `ls`). The marginal saving is whatever the post-hoc collision reconciliation would have cost — in the Round-9 case, a 200-word §3.6 in PLAN.md plus a triage item carried forward. For dispatches that touch multiple registries (F-modes + report numbers + index rows), the savings compound.

---

## Suggestion 4: Long-document section-anchor edits need a positional re-read

### Proposed addition

> **Long-document section-anchor edits need a positional re-read.** "When inserting a new numbered section into an ordered document (`PLAN.md`, `INDEX.md`, RFCs, design docs), re-read the section headers around the insertion point *after* the Edit lands to confirm the new section is in the correct sequence. The default Edit-tool anchor pattern (replace `### N.X header` with `### N.X header\n\n<new section>\n\n### N.X header`) can land the new section either before or after the anchor depending on how the anchor regex resolves — always verify. A two-second `grep -n '^### ' <file>` after the edit catches the bug."
>
> *Grounded in: while updating `research/PLAN.md` for v0.12, I anchored a new `§3.6 Failure-mode numbering collision` block on the `### 3.5 YouTube-video-only content` header, intending to land §3.6 after §3.5. The Edit landed it *before* §3.5 in the section order (§3.4 → §3.6 → §3.5). Caught immediately on re-read and fixed with one swap Edit. Cheap to catch in-session; embarrassing if it ships.*

### Why this earns its place in your agents file

The Edit tool is precise about string replacement but indifferent to document semantics. A new "### 3.6" header is just text; the tool doesn't know the document has a numbered-section invariant. The agent has to enforce that invariant by re-reading after editing — every time, for long ordered documents.

The cost is one Read call (or one grep) after the Edit. The cost of skipping it is shipping a document with out-of-order sections, which erodes trust in the document's structure (readers stop trusting that §3.6 follows §3.5).

---

## Suggestion 5: PLAN.md version bumps require dual-edit (header + trailing marker)

### Proposed addition

> **PLAN.md version bumps require dual-edit (header + trailing marker).** "When bumping `research/PLAN.md`'s version, update BOTH the header version line (`**Version:** v0.X`) AND the trailing marker (`*End of PLAN.md v0.X.*`). Also update the `Earlier versions:` paragraph immediately after the header to add a sentence describing what v0.X recorded. Verify by grep: `grep -n 'v0\\.' research/PLAN.md | head -5` should show all three references at the new version."
>
> *Grounded in: PLAN.md v0.12 bump in PR #57. The trailing marker had been left at `v0.10` even in PLAN.md v0.11 — I caught and fixed it in the v0.12 bump (updated to v0.12) but the v0.10 → v0.11 bump missed it. Reading the trailing marker is the single fastest way to verify which version a file claims to be; if it lies, downstream readers waste time.*

### Why this earns its place in your agents file

A long-lived status document like PLAN.md accumulates version markers in multiple places; the agent has to update all of them in one pass or the document becomes internally inconsistent. The trailing marker is the easiest to forget because it's far from the header. A grep is the cheap enforcement.

The marginal cost is one grep + N≤3 Edits per version bump. The marginal saving is preventing a future reader from concluding the document is mid-edit or that the version-history table is wrong.

---

## Suggestion 6: Pre-convert binary sources to text sidecars before subagent dispatch

### Proposed addition

> **Pre-convert binary sources to text sidecars before subagent dispatch.** "When dispatching subagents to process `.mhtml`, `.mht`, or `.pdf` files, pre-convert each source to a `.txt` sidecar (for MHTML: Python `email` stdlib + `html2text`; for PDF: the `Read` tool's `pages` parameter, or `pdftotext` if available). The subagent's brief points to the `.txt` sidecar (not the binary). This cuts subagent token cost, eliminates MIME-chrome parsing failures, and lets the subagent grep for content directly. The MHTML *image-extraction* pass (see Suggestion 2) is a separate discipline that runs alongside this one — not a replacement for it."
>
> *Grounded in: the Round-9 manual drain. Six MHTML sources and four PDFs would have taken substantially more token-cost per subagent if read directly (MIME chrome + base64 image blobs interleaved with body HTML). Pre-converting to `.txt` sidecars meant each subagent's first action was a clean `Read` on plain text. All three subagents completed under their target word counts; none reported MIME-parsing issues.*

### Why this earns its place in your agents file

Subagent token budgets are smaller than the lead agent's (and harder to extend if they exhaust). Anything that lets a subagent skip parsing chrome is a direct token saving. MHTML chrome is particularly costly — base64 image blobs can dominate a 2 MB MHTML's byte count while contributing nothing to the text content.

The cost is a one-time Python script per dispatch batch. The saving compounds across every subagent that reads the source.

---

## Suggestion 7: Read tool natively renders PNG/JPG — no OCR or vision-API setup needed

### Proposed addition

> **Read tool natively renders PNG/JPG (and most image formats) as vision inputs.** "When the agent needs to *understand* an image file (diagram, chart, screenshot, photo), the right move is a direct `Read` on the file path. The tool renders the image into the model's vision context — no `pip install pytesseract`, no OpenAI Vision wrapper, no `wand` / `Pillow` pre-processing. This applies to images extracted from MHTMLs, screenshots dropped into the working tree by the user, downloaded chart PNGs, and anything else with a PNG/JPG/GIF/WebP extension."
>
> *Grounded in: the Kiro image-drain follow-up. After extracting 12 PNG/JPG images from the Kiro MHTML, six parallel `Read` calls on the substantive figures returned the diagrams as visual inputs — bug taxonomies, SMT solver output panels, semantic-entropy decision shapes — all readable in detail. No image-processing setup. Total token cost: 6 image reads (the model's vision-input pricing applies).*

### Why this earns its place in your agents file

This is a runtime fact about the agent's tooling that the model would not infer without an explicit mention. New sessions tend to reach for image-analysis library installs or vision-API calls when the simpler path is already available. A one-line rule fixes the recurring miss.

The cost is zero (it's already supported). The saving is whatever the "install pytesseract and write a wrapper" detour would have cost when the agent reaches for it.

---

## Suggestion 8: Subagent brief template — Hard requirements + Cleanup + Stay-in-lane + Structured report-back

### Proposed addition

> **Subagent brief template.** "Every subagent dispatch brief must include four blocks: (a) **Hard requirements** — bulleted concrete deliverables, not vibes ('cite verbatim quotes', 'aim for 3000–5000 words', 'cross-reference at least 3 existing reports'); (b) **After completion** — explicit cleanup actions, especially file deletions and what NOT to touch (no commits, no edits to INDEX/PLAN, no edits to other subagents' files); (c) **Stay in your lane** — explicit list of files the subagent must not modify; (d) **Report back** — a labelled question structure (a/b/c/d/e) so the subagent's reply is grep-friendly and the lead agent can fold it into integration without re-reading. Optional: a registry-allocation block per Suggestion 3."
>
> *Grounded in: PR #57's three subagent dispatches. All three returned tight, structured reports under 300 words each (per the brief). All three deleted their source files cleanly. None touched files outside their lane. The mishap — the F36/F37 collision — was the one missing block (registry allocation), which is why Suggestion 3 exists. The four-block template worked; the missing fifth block taught us what was missing.*

### Why this earns its place in your agents file

Subagents take their behavioural cues from brief structure. A loosely-worded brief produces a loosely-worded result; a structured brief produces structured output the lead agent can integrate mechanically. The four-block template is what the Round-9 dispatches actually used; it produced clean integration.

The cost is a one-time template the lead agent reuses (~20 lines per brief). The saving is integration time — every subagent returns in a format the lead agent already knows how to read.

---
