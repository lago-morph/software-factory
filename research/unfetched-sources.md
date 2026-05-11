# Unfetched sources — manual browser retrieval needed

**Date:** 2026-05-11
**Purpose:** URLs that survived all automated retrieval attempts (direct fetch, GitHub Actions runner with curl, Wayback Machine). The user has read several of these interactively and can recover them via a real browser session.

**Companion script:** `research/fetch-from-browser.sh` — runnable from the user's local machine with their browser cookies (see usage block at the top of the script).

---

## Currently unfetched

| URL | Why automated fetch fails | What we need from it | Affects |
|---|---|---|---|
| https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e | Cloudflare interactive challenge; Wayback never archived | Verbatim primary-source quotes for the "Dark Factory" framing (currently reconstructed from secondary sources) | `research/07-dark-factory.md` |
| https://medium.com/@welkaim/about | Cloudflare interactive challenge | Author bio / context for el-kaim attribution | `research/07-dark-factory.md` (background only) |
| https://welkaim.medium.com/ | Cloudflare interactive challenge | Author profile / other articles by same author | `research/07-dark-factory.md` (background only) |
| https://www.lennysnewsletter.com/p/an-ai-state-of-the-union | Paywall; visible portion is editorial summary + reference list only. Wayback retry confirmed paywall persists. | Full Simon Willison interview body (the strongest single artifact in the corpus for the Round-1 thesis) | `research/06-hn-and-lenny.md` |
| https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens | Paywall; same as above | Full Boris Cherny interview body — the strongest scaling data point in the corpus | `research/06-hn-and-lenny.md` |
| https://every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it | Paywall after the visible "10-minute investment" section | Concrete worked examples past the introduction (frustration detector, etc.) | `research/03-every-compound-engineering.md` |

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

## Disposition after retrieval

Once new files appear under `research/manual/` (or any subdirectory of `research/`), the next research-pipeline-skill activation will scan and dispatch subagents to incorporate them into the relevant reports, then delete the raw files. See the `research-pipeline` skill (Phase 0 — Drain pending content).

If you want to trigger that drain explicitly, prompt: *"check `research/` for new content and incorporate it"* — the skill will pick it up.
