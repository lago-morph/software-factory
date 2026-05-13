# Blocked URLs — Round 7 (issue #36 follow-up batch)

**Date:** 2026-05-13. Single batched `[fetch-urls]` issue filed at the end of round 6 to chase the 8 follow-ups identified in `research/blocked-urls-round-6.md` §"Follow-ups" (corrected slugs and new canonical paths). Drained the same day.

**Outcome at a glance:** 5 of 7 URLs returned HTTP 200 with usable content; 1 returned HTTP 200 but the content was a JS-rendered SPA shell (3 URLs, same problem); 1 returned HTTP 200 as a binary PDF with no extractable body; 1 returned HTTP 404. The two productive returns (Shapiro five-levels canonical, Superconductor.com) were drained immediately into `research/followup/01` and `research/followup/06`.

---

## Per-URL outcomes

| # | URL | HTTP | Outcome |
|---|---|---|---|
| 1 | https://danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ | 200 (97 KB) | ✅ **Drained into `research/followup/01-shapiro-five-levels.md`.** Closes the four-round-old gap of having only El Kaim's restatement of Shapiro's framework. |
| 2 | https://arxiv.org/pdf/2503.18813 | 200 (5.5 MB) | 🟡 **Metadata only.** PDF binary; html2text dump is 5.5 MB of stream data (skill notes "html2text does NOT extract PDF text"). The first ~1500 bytes of the PDF carry the title and authorship metadata, which is the only useful content extracted. **Authors confirmed (10):** Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr. **Title:** *Defeating Prompt Injections by Design*. **DOI:** `10.48550/arXiv.2503.18813`. **arXiv ID:** `2503.18813v2`. License: CC-BY-4.0. Body of paper still unrecoverable via this path. |
| 3 | https://arxiv.org/html/2503.18813v1 | 404 | ❌ **Same outcome as the v2 html attempt in #29.** arxiv's HTML render does not exist for either v1 or v2 of this paper. Recovery candidates: (a) parse the PDF with a real PDF library (pdfminer / pdf2text — neither installed in the action runner; would need workflow change); (b) Wayback search for an archived v2 html render; (c) fetch the LaTeX source from `arxiv.org/e-print/2503.18813` and run pandoc — also requires workflow change; (d) accept the gap and use only abstract + Willison's writeup. **Decision:** accept the gap; the abstract + Willison together cover the architecture; the formal proofs and AgentDojo evaluation details are interesting but not load-bearing for any decision in our four candidate architectures. |
| 4 | https://www.superconductor.com/ | 200 (318 KB) | ✅ **Drained into `research/followup/06-competitor-landscape.md` §4.** Replaces the wrong-domain `superconductor.io` parking-page hit from #31. |
| 5 | https://platform.claude.com/docs/en/agent-skills/overview | 200 (505 KB raw / 143 lines extracted) | ❌ **JS-rendered SPA — no usable content.** The fetched body is nav chrome + footer + ~17 `Loading...` placeholders. Same outcome for the next two rows. |
| 6 | https://platform.claude.com/docs/en/agent-skills/best-practices | 200 (505 KB raw / 143 lines extracted) | ❌ Same SPA-shell outcome. |
| 7 | https://platform.claude.com/docs/en/agent-skills/security | 200 (505 KB raw / 143 lines extracted) | ❌ Same SPA-shell outcome. **All three platform.claude.com pages render their body client-side via JS that the curl-based action cannot execute.** Recovery requires either (a) a headless-browser fetch (Playwright/Puppeteer in the action), (b) Path B (user does Save Page As after the JS has run), or (c) finding a non-JS canonical mirror (none known). **Decision:** flag as Path B-only in `research/unfetched-sources.md`; the security-quote attribution gap in report 23 §3 stays open until the user provides a browser-saved copy. |

---

## Key lessons (corpus-wide)

**Lesson R7.1 — `platform.claude.com` is JS-rendered.** Unlike `code.claude.com/docs/...` (which renders server-side and was successfully fetched in an earlier round) and unlike `anthropic.com/engineering/...` (server-rendered, fetchable as of round 6), the developer-platform docs at `platform.claude.com/docs/...` are a single-page application that returns 505 KB of HTML with only nav and footer text plus `Loading...` placeholders where the body should be. **Add to `research/unfetched-sources.md` under "Action 200s but no body."** Any future `[fetch-urls]` issue targeting `platform.claude.com` should include a note that the action will return content-free 505KB shells; either skip or escalate to Path B immediately.

**Lesson R7.2 — arXiv PDFs need a different toolchain.** When `arxiv.org/html/<id>v<v>` returns 404 (as it does for many recent papers — the html render is not always generated), the PDF is the only direct route, and the action's html2text extractor cannot read it. The fallback chain in priority order: (a) try the abstract page (always works, gives summary); (b) check Wayback for an html render at any version; (c) for papers we genuinely need verbatim, install pdfminer or poppler-utils in the action and add a per-content-type extractor branch. We have not hit (c) yet — the abstract has been sufficient for everything except the CaMeL paper, and the CaMeL paper is well-summarized by Willison's writeup.

**Lesson R7.3 — Some 404s reflect "this slug never existed" not "this URL was removed."** Issue #29's `the-five-levels-of-agentic-coding` 404 was a slug-guess miss (we invented the slug from the corpus's paraphrase of the title); the real slug `the-five-levels-from-spicy-autocomplete-to-the-software-factory` was discovered by reading the sidebar of a sibling post that DID fetch successfully. **Heuristic:** when a target URL 404s but a sibling URL on the same domain returns 200, ALWAYS read the sibling for cross-links to the missing target. Costs nothing; can save a round.

---

## Follow-ups (queued for next round if motivated)

These survived round 7 with known recovery routes:

1. **`platform.claude.com/docs/en/agent-skills/overview` + `/best-practices` + `/security`** — Path B only (Save Page As after JS renders). User action required. Affects `research/23-anthropic-engineering-trilogy.md` §3 (security-quote attribution still open).
2. **CaMeL paper body** — accepted as gapped; not actively pursued. If a researcher wants the formal proofs they should run pdfminer locally on the already-fetched PDF (not committed; was deleted in this round's cleanup since the action runner can't extract it anyway).
3. **The 6 GitHub Copilot docs URLs from round 6 (#30 404s)** — still need new canonical paths identified via WebSearch. Not picked up in #36.
4. **The Cognition Devin announcement URL** — still need to find the new canonical path. Not picked up in #36.
5. **El Kaim's broader Medium corpus (10+ posts)** — see `research/PLAN.md` §"Future research" cluster. Not yet filed as a fetch issue; one batched issue would cover all 10.

---

## Files retained on disk

After this round's cleanup, only `research/fetched/issue-36/80e2d2ebd8_arxiv.org__html__2503.18813v1.html` is retained — as 404 evidence so the next session doesn't re-attempt the v1 HTML render. All other issue-36 files were deleted (the 5 productive ones consumed by drain subagents; the 4 unproductive ones — arxiv PDF .md/.html and the 3 platform.claude.com SPA pairs — deleted because they contain no recoverable content).

The retained issue-29/30/31 evidence files (11 files total documenting prior 404s and slug-guess misses) are unchanged; the round-6 doc explains why each is kept.
