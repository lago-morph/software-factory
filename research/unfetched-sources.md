# Unfetched sources — manual browser retrieval needed

**Date:** 2026-05-11 (revised after first manual browser-cookie retrieval pass)
**Purpose:** URLs that survived all automated retrieval attempts (direct fetch, GitHub Actions runner with curl, Wayback Machine). The user has read several of these interactively and can recover them via a real browser session.

**2026-05-11 retrieval-pass outcomes** — a first round of manual browser-cookie fetches landed in `research/manual/` and was drained per the research-pipeline skill's Phase 0. Outcomes:

- ✅ **every.to/source-code/my-ai-had-already-fixed-the-code-before-i-saw-it** — fully unlocked; post-paywall content incorporated into report 03. Removed from this list.
- ⚠️ **Both Lenny URLs** (Cherny + Willison) — browser cookies did NOT bypass Substack's paid-subscriber gate. Manual fetches returned the same paywall-truncated body that's already incorporated into report 06. Need a *paid* Lenny subscription to unlock; remain on this list with the disposition updated below.
- ❌ **All three el-kaim / Medium URLs** — browser-cookie fetches still hit the Cloudflare interactive JavaScript challenge (cookies don't help when the gate is an active JS challenge). The only remaining recovery path is Path B below (Save Page As → Web Page, Complete from a real browser session that has solved the challenge).

**Companion script:** `research/fetch-from-browser.sh` — runnable from the user's local machine with their browser cookies (see usage block at the top of the script).

---

## Currently unfetched

| URL | Why automated fetch fails | What we need from it | Affects |
|---|---|---|---|
| https://el-kaim.com/the-dark-factory-how-software-is-learning-to-build-itself-6496a69ba14e | Cloudflare interactive challenge; Wayback never archived; cookies-with-curl also stubbed (2026-05-11) | Verbatim primary-source quotes for the "Dark Factory" framing (currently reconstructed from secondary sources). **Use Path B (Save Page As) from a browser that has solved the challenge.** | `research/07-dark-factory.md` |
| https://medium.com/@welkaim/about | Cloudflare interactive challenge; cookies-with-curl also stubbed (2026-05-11) | Author bio / context for el-kaim attribution. **Path B only.** | `research/07-dark-factory.md` (background only) |
| https://welkaim.medium.com/ | Cloudflare interactive challenge; cookies-with-curl also stubbed (2026-05-11) | Author profile / other articles by same author. **Path B only.** | `research/07-dark-factory.md` (background only) |
| https://www.lennysnewsletter.com/p/an-ai-state-of-the-union | Paywall; visible portion is editorial summary + reference list only. Wayback retry confirmed paywall persists. Manual browser-cookie fetch (2026-05-11) also paywall-truncated — cookies present but *not paid-subscriber* cookies. | Full Simon Willison interview body (the strongest single artifact in the corpus for the Round-1 thesis). **Needs a paid Lenny subscription** + Path A or Path C below. | `research/06-hn-and-lenny.md` |
| https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens | Same as above; manual browser-cookie fetch (2026-05-11) also paywall-truncated. | Full Boris Cherny interview body — the strongest scaling data point in the corpus. **Needs a paid Lenny subscription** + Path A or Path C below. | `research/06-hn-and-lenny.md` (and `research/PLAN.md` §11.3 thread) |

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
