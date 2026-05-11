# Unfetched sources — manual browser retrieval needed

**Date:** 2026-05-11 (revised after first manual browser-cookie retrieval pass)
**Purpose:** URLs that survived all automated retrieval attempts (direct fetch, GitHub Actions runner with curl, Wayback Machine). The user has read several of these interactively and can recover them via a real browser session.

**2026-05-11 retrieval-pass outcomes** — two rounds of user-supplied manual content landed in `research/manual/` and were drained per the research-pipeline skill's Phase 0. Outcomes after both rounds:

- ✅ **every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it** — fully unlocked in round 1 (browser-cookie fetch). Post-paywall content incorporated into report 03. **Removed from this list.**
- ✅ **el-kaim.com/the-dark-factory-...** — fully unlocked in round 2 ("Save Page As" text export from a browser that had solved the Cloudflare challenge). Primary-source incorporation into report 07 in progress as of 2026-05-11. **Removed from this list.**
- ❌ **medium.com/@welkaim/about** and **welkaim.medium.com** — still Cloudflare-blocked across all routes attempted. Listed below for completeness; user has not retrieved manually.
- 🎬 **Both Lenny URLs** (Cherny + Willison) — **the pages are video-only; there is no text article body at the URL.** Round 1 manual fetches captured the editorial preface + references list (already in report 06). Round 2 user note explicitly confirmed: *"this was just a video. Here are references at end."* and *"only content here was a video. However there were references."* So the "interview body" the corpus has been chasing through three paywall attempts does not exist as text. The references list is the only canonical text content; everything else is in the YouTube/Spotify/Apple Podcasts audio. Listed below with a revised recovery instruction.

**Companion script:** `research/fetch-from-browser.sh` — runnable from the user's local machine with their browser cookies (see usage block at the top of the script).

---

## Currently unfetched

| URL | Why automated fetch fails | What we need from it | Affects |
|---|---|---|---|
| https://medium.com/@welkaim/about | Cloudflare interactive challenge; cookies-with-curl also stubbed (2026-05-11) | Author bio / context for el-kaim attribution. Low priority now that the primary-source article (report 07) has been unlocked. **Path B only.** | `research/07-dark-factory.md` (background only) |
| https://welkaim.medium.com/ | Cloudflare interactive challenge; cookies-with-curl also stubbed (2026-05-11) | Author profile / other articles by same author. Low priority now that the primary-source article (report 07) has been unlocked. **Path B only.** | `research/07-dark-factory.md` (background only) |
| https://www.lennysnewsletter.com/p/an-ai-state-of-the-union | **The page is video-only.** No text interview body exists at the URL — round-2 user note confirmed this directly. Direct fetch, Wayback, and manual browser-cookie fetch all returned the same paywall-stub-pretending-to-be-an-article structure; the actual content is the audio/video on YouTube/Spotify/Apple Podcasts. | Full Willison interview body — requires a **transcript-extraction service** against the YouTube video (`https://youtu.be/wc8FBhQtdsA`), not a paywall bypass. | `research/06-hn-and-lenny.md` |
| https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens | Same as above — **video-only**. The page is a podcast landing with a paywall-stubbed "biggest takeaways" summary, not a transcript. | Full Cherny interview body — requires a transcript-extraction service against the YouTube video (`https://youtu.be/We7BZVKbCVw`), not a paywall bypass. **The "10–30 PRs/day" and "10–15 parallel sessions" claims that the corpus quotes are still un-primary-sourced** — they came from secondary summaries and remain so. | `research/06-hn-and-lenny.md` (and `research/PLAN.md` §11.3 thread) |

---

## How to recover

Pick whichever path is least friction for you:

### Path A — `curl` with browser cookies (fastest if you already have a cookies file)

1. Export cookies from your browser to a Netscape-format file:
   - **Firefox:** the `cookies.txt` extension (or read directly from `~/.mozilla/firefox/<profile>/cookies.sqlite`).
   - **Chrome / Brave / Edge:** the `Get cookies.txt LOCALLY` extension.
2. Save as `~/cookies.txt` (or any path you'll point the script at).
3. Run `bash research/fetch-from-browser.sh ~/cookies.txt`.
4. Output lands in `research/manual/`. Commit and push; a future Claude session will see the new files and incorporate them.

### Path B — browser "Save Page As → Web Page, Complete"

For pages where cookies-with-curl still fails (e.g. Cloudflare's interactive JavaScript challenge on el-kaim.com), no headless tool will get past it. Open the page in your browser, use **File → Save Page As → Web Page, Complete**, and drop the resulting `.html` (and the companion `_files/` folder if you want assets) into `research/manual/`. Then commit and push.

### Path C — Reader View → text export

For paywalled articles where you've already read the body, your browser's Reader View typically exposes the full text (paywalls are usually CSS overlays that Reader View bypasses). Copy the rendered article text and paste into `research/manual/<short-slug>.txt`. Less faithful than HTML but enough for verbatim quoting.

---

## Deferred fetch-action candidates (added 2026-05-11 post-drain)

These were blocked from the sandbox during the 2026-05-11 parallel-fanout run (`harness/runs/20260511-054258/`) but the subagent did **not** file a `[fetch-urls]` issue. Each is a candidate for the GitHub Action's runner IP — historically the action retrieves these even when the sandbox can't. No user action required; a future Claude session can batch them into 2–3 grouped issues. Listed here so the next-session orchestrator can pick them up without re-deriving the catalog.

| URL family | Reports affected | Filing strategy |
|---|---|---|
| `danshapiro.com/blog/2026/01/the-five-levels-...` (+ `/2026/02/you-dont-write-the-code/`) | `research/followup/01-shapiro-five-levels.md` | One issue; small. Includes Path B fallback in case Cloudflare blocks the action too. |
| `anthropic.com/engineering/` × 4 — `effective-harnesses-for-long-running-agents`, `equipping-agents-for-the-real-world-with-agent-skills`, `building-c-compiler`, `harness-design-long-running-apps` | `research/23-anthropic-engineering-trilogy.md`, `research/followup/07-evals-deepdive.md`, `research/followup/08-security-primitives.md` | One issue; high leverage. Anthropic posts have been retrievable by the action in prior rounds. |
| `hamel.dev/blog/posts/` (evals-faq, llm-judge, field-guide, evals) + `simonwillison.net/2025/Jul/3/faqs-about-ai-evals/` + `simonwillison.net/2025/Jun/14/multi-agent-research-system/` | `research/followup/07-evals-deepdive.md` | One issue grouped with Anthropic engineering posts. |
| `simonwillison.net/2025/Apr/11/camel/` + `…/2025/Jun/16/the-lethal-trifecta/` + `…/2023/Apr/25/dual-llm-pattern/` + `arxiv.org/abs/2503.18813` (+ `/html/2503.18813v2`) + `anthropic.com/engineering/claude-code-sandboxing` | `research/followup/08-security-primitives.md` | One issue. arXiv reachable from the action. |
| `kaner.com/pdfs/ScenarioIntroVer4.pdf` + Wikipedia PDCA + Deming Institute PDSA | `research/followup/09-methodology-ancestors.md` | Optional — structural conclusions firm without verbatim passage-level fidelity. |
| `devin.ai` + `factory.ai` + `8090.inc` + `superconductor.io` + `blog.fsck.com/2025/10/09/superpowers/` | `research/followup/06-competitor-landscape.md` | One issue; Cloudflare-heavy hosts. Action may also 403; if so, escalate to Path B. |
| `docs.replit.com/*` + `blog.replit.com/*` (~20 URLs across both — see `research/20-replit-agent.md` blocked-URL list) | `research/20-replit-agent.md` | One issue; Cloudflare-gated. Action success uncertain — `blocked-urls.md` v5 catalogs `*.openai.com` 403s; Replit may behave similarly. |
| `developers.openai.com/codex/*` + `openai.com/index/harness-engineering/` + `openai.com/index/unlocking-the-codex-harness/` | `research/18-openai-codex-substrate.md` | Listed in `blocked-urls.md` v5 as known-blocked from action too — would need Path B if filed. |
| `docs.github.com/en/copilot/*` (Copilot cloud agent + Autofix + CodeQL pages) | `research/19-github-copilot-cloud-agent.md` | One issue. GitHub's own docs site is normally reachable from a GH-hosted runner. |
| `every.to/chain-of-thought/*` (3 Klaassen siblings) | `research/followup/05-klaassen-siblings.md` | Likely action-blocked too (every.to consistently 403s GH IPs); Path B is the realistic recovery — not a fetch-issue candidate. **Defer to user.** |

**How to action this list:** prompt a future session *"file fetch-urls issues for the deferred candidates in `research/unfetched-sources.md`"*. The session will produce 2–3 batched issues (group by host/likelihood), wait for the action's `fetched/issue-N` branches, drain them per the `research-pipeline` skill, then update this section.

## Disposition after retrieval

Once new files appear under `research/manual/` (or any subdirectory of `research/`), the next research-pipeline-skill activation will scan and dispatch subagents to incorporate them into the relevant reports, then delete the raw files. See the `research-pipeline` skill (Phase 0 — Drain pending content).

If you want to trigger that drain explicitly, prompt: *"check `research/` for new content and incorporate it"* — the skill will pick it up.

For the deferred fetch-action candidates above, the analogous prompt is: *"file fetch-urls issues for the deferred candidates in `research/unfetched-sources.md`"*.
