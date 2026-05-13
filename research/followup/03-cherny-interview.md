# Boris Cherny on Lenny's Podcast — "What happens after coding is solved"

**Status: 🟡 PARTIAL primary-source-anchored.** Manual transcript of the **first 30 minutes** of a ~90-minute podcast is integrated below. The remaining ~60 minutes are still un-transcribed. This was previously a 🔴 blocked-on-fetch report relying entirely on secondary write-up snippets; several of the most-cited Cherny claims in the corpus are now verbatim-anchored to a primary source. Drain note (issue #36 extras) at top documents what flipped and what is still missing.

**Round-3 follow-up thread 3 (per `research/PLAN.md` §11.3).** Cherny is the head of Claude Code at Anthropic and, by most accounts, the practitioner operating closest to the "Dark Factory" end of the human-role axis.

---

## Drain note (issue #36 extras) — 2026-05-13

A manual transcript of the Lenny × Cherny YouTube episode (`https://youtu.be/We7BZVKbCVw`) landed in `research/manual/lenny-Head of Claude Code.txt`. Per the user, it covers **only the first ~30 minutes of the ~90-minute podcast** — the remaining 60 minutes are not yet transcribed (overnight long-transcription run was offered). The transcript has the usual ASR artifacts ("quad code" = "Claude Code", "1020, 30" = "10, 20, 30", "Boris Turney" = "Boris Cherny", "cowork" = "Cowork", "ant" = "Anthropic", "Ben Manton" = "Ben Mann").

**Status flipped:** This report was 🔴 blocked-on-fetch; it is now **🟡 partial primary-source-anchored** for the topics covered in minutes 0–30. Anything attributed to minutes 30–90 is still un-sourced.

**Corpus claims now verbatim-anchored to Cherny himself:**

1. **"10–30 PRs/day"** (was in `research/06-hn-and-lenny.md` and various secondary snippets) — Cherny, cold open: *"Every day I ship like 10, 20, 30 pull requests, something like that... every day."* (Confirmed every-day cadence; not week-totaled.)
2. **"100% of my code is written by Claude Code"** — Cherny, cold open and again later: *"100% of my code is written by Claude Code. I have not edited a single line by hand since November."*
3. **"Productivity per engineer has increased 200%"** — Cherny, in discussion of Anthropic-wide numbers: *"Productivity per engineer has increased 200% in terms of, like, pull requests, and this number is just crazy for anyone that actually works in the space."* (Was flagged 'single unverified snippet' in the prior version of this report. Now verbatim-anchored, and Cherny explicitly contrasts it against his Meta dev-productivity experience where year-over-year gains were "a few percentage points.")
4. **"Coding is largely solved"** — Cherny: *"I think at this point it's safe to say that coding is largely solved, at least for the kinds of programming that I do."*
5. **"Software engineer title is going to start to go away... replaced by builder"** — Cherny, cold open: *"I think by the end of the year, everyone's gonna be a product manager, and everyone codes. The title software engineer is going to start to go away. It's just going to be replaced by builder, and it's going to be painful for a lot of people."*
6. **November 2025 stop-editing date** — Cherny: *"It only crossed 100% in November... I have not edited a single line by hand since November."* This is the single strongest dated data point for Willison's "November 2025 inflection point" claim in the entire corpus, and it comes from inside Anthropic.
7. **"Underfund things a little bit"** principle — Cherny: *"You want to under-resource things a little bit at the start"* and *"if you underfund everything a little bit, because then people are kind of forced to quantify [creativity]... so I think that's kind of like one principle is underfunding things."*
8. **"Unlimited tokens" perk / token spend rivaling salary** — Cherny: *"At Anthropic, we're starting to see some engineers that are spending, you know, like hundreds of thousands a month in tokens."* This is a corpus-first concrete dollar figure for per-engineer token spend.
9. **Cursor-to-Anthropic two-week return story (PLAN.md topic 7)** — Now covered. Cherny: *"It's the fastest job change I've ever had... what I really missed about Anthropic was the mission... it's all about safety."* No more drama than that — no product dispute, no equity story; just mission pull. Topic resolved.
10. **Claude reviews 100% of Anthropic PRs** — Cherny: *"We have Claude doing automatic code review for everything. So here at Anthropic, Claude reviews 100% of pull requests. There's still a layer of human review after it."* This pins down the merge-gate question this report had flagged as open: **two-stage review — Claude on every PR, then a human checkpoint, except for pure prototype code.**

**Corpus claims NOT verifiable in minutes 0–30 (likely in the un-transcribed 30–90):**

- **"5–10 sessions open at a time" / "I run 5 Claudes in parallel"** — NOT spoken in minutes 0–30. Cherny mentions *"I have like five agents running while we're recording this"* in the cold open but does not detail the 5-local + 5–10-web architecture in the transcribed segment. The detailed parallel-session, `/loops`, `/batch`, and "thousands of overnight agents" material from the `ociubotaru` Threads clip is presumably in minutes 30–90.
- **Three principles for new team members** — Only two of the three appear in minutes 0–30 ("underfund things a little bit" and "encourage people to go faster"). The third ("What's better than doing something? Having Claude do it") is *referenced by Lenny* in passing but Cherny does not enumerate the three as a list in this segment.
- **Cowork 10-day build timeline** — Mentioned that Cowork exists and Cherny uses it daily (parking ticket, project management, spreadsheet/Slack/email syncing), but the "~10 days to build" timeline is NOT in minutes 0–30.
- **4% of public GitHub commits / DAU doubling** — Lenny references the SemiAnalysis 4% number; Cherny confirms *"4% of all commits in the world is just way more than I imagined"* and *"if you look at private repositories, it's quite a bit higher than that."* The "DAU doubling last month" line from the Lenny preface is referenced only by Lenny, not quantified by Cherny in this segment.
- **20% projection for end of 2026** — Lenny cites it; Cherny doesn't push back but doesn't independently restate the number either.
- **Cost-per-day for Cherny's own setup** — Still open. The "hundreds of thousands a month" figure is for some Anthropic engineers in aggregate, not specifically Cherny's daily spend.

**New primary claims surfaced (not previously in the corpus):**

- **Quad code's *internal launch* got two likes.** Cherny: *"I made a post about it, and I announced it internally, and I got two likes. That's the sense of the reaction at the time."* Internal Anthropic adoption was not preordained — this contradicts the implicit corpus narrative of "Anthropic obviously knew what they had."
- **The actual ramp curve, by Cherny's own use:** *"In February [public release], it was writing maybe 20% of my code. In May, maybe 30%. I was still using Cursor for most of my code. It only crossed 100% in November."* This is a **clean 9-month 30%→100% ramp for Anthropic's own Claude Code lead, on Anthropic's own product**. Significantly more granular than anything we had.
- **May 2025 prediction story:** At Code with Claude (May 2025), Cherny predicted "you might not need an IDE to code anymore by end of year" and the room *"audibly gasped."* Useful corroboration of the "exponential-thinking is intuitively wrong even to AI insiders" point.
- **Anthropic engineering team ~4x'd in the year, productivity per engineer +200%.** Combined: roughly **8x total team throughput year-over-year** at Anthropic.
- **Claude is now suggesting *what to build*, not just *how to build*.** Cherny: *"Quad is starting to come up with ideas. It's looking through feedback. It's looking at bug reports. It's looking at, you know, like telemetry, and it's starting to come up with ideas for bug fixes and things to ship... it's just starting to get a little more like a co-worker."* This is the next-frontier claim in the cold open and is the strongest signal yet that Anthropic sees the *PM/prioritization* role as next-to-be-disrupted.
- **The "memory leak that the new grad solved faster than Cherny" anecdote** — A real worked example of veteran engineers being out-paced by AGI-native new grads because the veterans *forget to delegate to Claude*. Strong supporting evidence for the "the binding constraint is human habit, not model capability" theme.
- **Two-stage merge gate (Claude review + human review)** — see above; this pins the merge-gate question the previous draft flagged as open.
- **"Latent demand" as the Claude Code product principle** — Cherny: *"part of the reason quad code works is this idea of latent demand, where we bring the tool to where people are, and it makes existing workflows a little bit easier."* Connects directly to PLAN.md's `Cowork` thread; same operating principle.

**Top 3 most-quotable Cherny lines** (verbatim, from minutes 0–30):

1. *"100% of my code is written by Claude Code. I have not edited a single line by hand since November. Every day I ship like 10, 20, 30 pull requests."*
2. *"I think by the end of the year, everyone's gonna be a product manager, and everyone codes. The title software engineer is going to start to go away. It's just going to be replaced by builder, and it's going to be painful for a lot of people."*
3. *"Productivity per engineer has increased 200%... back in a previous life I was at Meta and... in a year with hundreds of engineers working on it, you would see a gain of like a few percentage points of productivity. So nowadays, seeing these gains of just hundreds of percentage points, it's just absolutely insane."*

(Honorable mention: *"I made a post about it, and I announced it internally, and I got two likes."*)

**Recommendation on overnight full-transcription:** **Worth it.** The 30–90 segment almost certainly contains the parallel-session architecture, the third principle, the Cowork 10-day timeline, the cost-per-day question, and Cherny's direct take on human-role-axis questions — all of which are open in this report and central to PLAN.md §11.3. The user should kick off the overnight long-transcription run.

---

## Source status

| Source | Status | Note |
|---|---|---|
| `https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens` | **VIDEO-ONLY, BLOCKED** | Confirmed video-only per `research/06-hn-and-lenny.md` and `PLAN.md §11.3`. No text interview body — the "biggest takeaways" stub is a paywall placeholder. **HTTP 403** to WebFetch. |
| `https://youtu.be/We7BZVKbCVw` (YouTube video) | 🟡 **PARTIAL** | Manual transcript (first 30 of 90 min) at `research/manual/lenny-Head of Claude Code.txt`; remaining 60 min outstanding (overnight long-transcription run on the table). See drain note above. |
| Secondary write-ups (Medium, Roger Wong, mejba.me, pjfp.com, ernestchiang.com, waydev.co, podwise.ai, DEV.to, aol.com, dnyuz.com) | **BLOCKED 403** | All returned 403 to WebFetch. |
| Lenny's LinkedIn takeaways post; Anish Moonka X thread; Threads posts | **BLOCKED 403** | All 403. |
| WebSearch result *snippets* over the above | **REACHABLE** | The only primary-quality material this report is built on. Treat as summaries-of-summaries. |
| `research/06-hn-and-lenny.md` (Wayback editorial preface + topic list + references) | **REACHABLE** | Already integrated. |

**Provenance rule:** every number and quote is tagged **primary** (Cherny's own X/Threads), **secondary** (third-party blog/note snippet from WebSearch), or **reconstructed** (paraphrase without verbatim quote). No quotes invented. Contested numbers flagged.

---

## What the Lenny post itself confirms (already in report 06)

From the Wayback editorial preface, "We discuss" list, and references section: episode published **Feb 19, 2026**. Topics (verbatim): Claude Code growth to **4% of public GitHub commits, DAU doubling last month**; counterintuitive product principles; "Why Boris believes coding is 'solved'"; latent demand that shaped Claude Code and **Cowork**; practical tips; "underfunding teams and giving them unlimited tokens leads to better AI products"; "Why Boris briefly left Anthropic for Cursor, then returned after just two weeks"; "Three principles Boris shares with every new team member." References include *The Bitter Lesson*, the SemiAnalysis "Claude Code is the Inflection Point" piece, the Spotify TechCrunch story, Mike Krieger's interview, Ben Mann's interview, and the Anthropic Cowork webinar page.

The **only quantitative claim paywall-visible** from the Lenny post itself is "**4% of public GitHub commits, DAU doubling last month.**" Everything else is reconstructed from third-party coverage.

---

## Cherny's daily workflow (reconstructed)

Richest snapshot: **`ociubotaru` on Threads** (`/post/DX72_bFjMEi/...`), captioning a video clip from the Lenny interview (**secondary**):

- "Claude mobile app is the primary work interface."
- "Has 5–10 sessions open at a time, each session can have multiple agents running."
- "Runs thousands of agents on deeper tasks overnight."
- "Dozens of /loops running for babysitting PRs, fix CI, auto-rebase, detects flaky tests, monitors Twitter."
- "He basically runs an always-on team of AI agents that monitor, fix, summarize, and improve things continuously."

Corroborated by Cherny's own Threads post (`@boris_cherny/post/DTBVlq0kobo`, **primary**): *"I run 5 Claudes in parallel in my terminal. I number my tabs 1-5, and use system notifications to know when a Claude needs input."*

Synthesized picture:

1. **Local layer.** 5 numbered iTerm tabs, each its own git checkout. Each Claude starts in **plan mode** (Shift+Tab twice). Boris iterates the plan; once good, he switches to auto-accept-edits and lets Claude one-shot the implementation. System notifications signal when input is needed.
2. **Cloud layer.** Additional **5–10 sessions on `claude.ai/code`** running in parallel with local. He "hands off local sessions to web, manually kicks off sessions in Chrome, and teleports back and forth."
3. **Mobile layer.** The **Claude mobile app is his primary interface** — starts sessions on phone in the morning, checks at night.
4. **Sub-agent fan-out.** Each session can spawn sub-agents. A `/batch` command "interviews you, then has Claude fan out the work to as many worktree agents as it takes (dozens, hundreds, even thousands)." Overnight, "a few thousand" agents run deeper work.
5. **Ambient automation.** "Dozens of `/loops`" run continuously — babysit PRs, fix CI, auto-rebase, detect flaky tests, monitor Twitter/Threads for mentions. Agents are participants in social workflows (PRs).

The **"10–15 parallel sessions"** figure from `research/06-hn-and-lenny.md` resolves as *5 local + 5–10 web*, ~10–15 top-level sessions, each fanning out sub-agents. Consistent with Cherny's primary 5-local Threads post.

---

## The PRs/day claim — what counts, what the merge gate is

**Resolved (primary, minutes 0–30):** Cherny: *"Every day I ship like 10, 20, 30 pull requests, something like that... every day."* Verbatim phrasing recovered. The "10–30 PRs/day" range in `research/06-hn-and-lenny.md` is correct; the higher 100/week snippet is consistent with the upper end of Cherny's stated range.

**Merge gate — resolved (primary):** Cherny: *"We have Claude doing automatic code review for everything. So here at Anthropic, Claude reviews 100% of pull requests. There's still a layer of human review after it, but you kind of like — you still do want some of these checkpoints. You still want a human looking at the code, unless it's like pure prototype code that you know it's not going to run anywhere."*

So the merge gate is a **two-stage review**:
1. Claude reviews 100% of PRs (gating).
2. Human review (still required, except for prototype code that won't run).

This is short of StrongDM's "no humans review code" charter — Cherny still has humans reviewing, just at higher leverage and after an AI pre-review pass.

---

## "No hand-edited code since November 2025"

**Primary (minutes 0–30):** Cherny: *"100% of my code is written by Claude Code. I have not edited a single line by hand since November."* Plus the personal ramp curve: *"In February [public release], it was writing maybe 20% of my code. In May, maybe 30%. I was still using Cursor for most of my code. It only crossed 100% in November."*

This corroborates Willison's "November 2025 inflection point" (GPT-5.2 and Opus 4.5). Cherny's November-2025 stop-editing date is the **strongest single dated data point** for the inflection-point claim anywhere in the corpus, and from inside Anthropic. The 9-month 30%→100% personal ramp is now verbatim-anchored.

---

## Cowork — the 10-day build

**Cowork** is an Anthropic product not in the Round-1 corpus. From WebSearch snippets and Cherny's Threads (`@boris_cherny/post/DTbJbe3kpr9`, **primary**):

- **Build timeline: ~10 days**, small team using Claude Code.
- **Growing faster than Claude Code's launch.**
- **Origin: latent demand** — non-engineers (data scientists, finance, sales) were already hacking with Claude Code.
- **Engineering complexity mostly safety, not product logic:** model-based command-safety classifier (auto-approval mode), a shipping VM for isolation, OS-level protections against accidental file deletion, re-thought permission model for non-technical users.
- **Features:** browser automation out of the box, claude.ai data connector support, ask-for-clarification when unsure.

The 10-day timeline is the eye-catching number. If accurate, it is the most aggressive small-team-cycle-time data point in the corpus — faster than StrongDM's "team of 3 in 3 months." Caveat: most of the 10 days went to safety infrastructure, not feature work — the model knew how to write the feature code in hours; the human-design loop was the binding constraint.

---

## Quality and review discipline

No verbatim quote available, but workflow shape is consistent:

- **Plan-mode iteration before code.** Plans reviewed by Cherny, not code.
- **`/loops` background CI/test/rebase babysitting** — catches issues before human sees the PR.
- **Sub-agent fan-out** for deep tasks suggests explore-many / verify-against-harness, not human review of each branch.
- **"When an engineer reads a PR, the code is already in good shape"** (secondary paraphrase) is the cleanest summary.

This is **scheduler mode**, not supervisor mode, per `architectures/00-comparison.md` human-role axis. Cherny picks *what* to build, agents pick *how*, human review happens at PR-as-artifact level, not at every-edit level.

---

## Cost numbers

**Cherny's personal $/day still not stated** (and not present in minutes 0–30 of the transcript). However, a corpus-first concrete number for *some* Anthropic engineers' token spend is now anchored:

- **Primary (minutes 0–30):** Cherny: *"At Anthropic we're starting to see some engineers that are spending, you know, like hundreds of thousands a month in tokens."* That is **$100,000+/month per engineer in tokens** for the heaviest users at Anthropic. At a typical staff-eng total comp of ~$300–500K/yr (~$25–42K/mo), this means **token spend can be 2–5× monthly comp** for the top users.
- The normative framing: *"Don't try to cost-cut at the beginning. Start by just giving engineers as many tokens as possible... It's not a huge cost. As the thing scales up, that's the point at which you want to optimize."*

**Still open:** Cherny's own daily/monthly figure specifically; corporate aggregate token spend; cost of the dozens-of-`/loops` and overnight-thousands-of-agents setup.

---

## Predictions / normative claims

Reconstructed from secondary snippets (`pjfp.com`, `aol.com`, `dnyuz.com`, Medium pieces):

- **"Coding is largely solved."** **PRIMARY-ANCHORED (minutes 0–30):** Cherny: *"I think at this point it's safe to say that coding is largely solved, at least for the kinds of programming that I do, is just a solved problem because Claude can do it."* Plus the forward-looking complement: *"Over the next few months, I think what we're going to see is just, across the industry, it's going to become increasingly solved."*
- **"Software Engineer" title disappearing**, replaced by **"Builder"**. **PRIMARY-ANCHORED (minutes 0–30):** Cherny: *"I think by the end of the year, everyone's gonna be a product manager, and everyone codes. The title software engineer is going to start to go away. It's just going to be replaced by builder, and it's going to be painful for a lot of people."* "End of the year" = end of 2026 (this is the Feb-2026 episode).
- **Engineering productivity at Anthropic up 200% per engineer.** **PRIMARY-ANCHORED (minutes 0–30):** Cherny: *"Productivity per engineer has increased 200% in terms of, like, pull requests."* He also notes the team has roughly ~4x'd in headcount in the year — so total team throughput is ~**8x**. He explicitly contrasts: at Meta managing code quality for FB/IG/WhatsApp, a year of hundreds of engineers' work produced "a few percentage points of productivity" gain. The 200% figure was previously flagged as a single unverified snippet; now confirmed.
- **Claude Code projected to reach 20% of public GitHub commits by end of 2026** (up from 4%). Traces to SemiAnalysis piece referenced in the bibliography; Cherny appears to endorse it.
- **Role boundaries dissolving:** *everyone* on the Claude Code team codes — PM, engineering manager, designer, finance person, data scientist. (Reconstructed.)

### Three principles for new team members

(WebSearch snippets of AOL / DNYUZ / dev.ua coverage):

1. **"What's better than doing something? Having Claude do it."** (Lenny quoted this back at Cherny per snippet.)
2. **"Underfund things a little bit."** — keep teams small to force Claude reliance.
3. **"Encouraging people to go faster."**

Maps onto The Bitter Lesson framing in the references — scale-of-compute (token spend per engineer) beats clever engineering at the team-building level.

### Polls Lenny cited

- 70% of engineers and PMs enjoy their jobs more with AI.
- Only 55% of designers do; 18% enjoy their jobs less.

(Secondary; useful K-shaped-disruption corroboration.)

---

## Implications for our architecture work

1. **Refine the human-role axis.** `architectures/00-comparison.md` currently has "supervises vs. schedules." Cherny is a clean instance of **schedules at scale** (5 local + 5–10 web + thousands of overnight sub-agents + dozens of always-on `/loops`). Atelier (Arch 2) and Compound (Arch 3) docs should explicitly note which mode they target — scheduler mode appears to be *the* productivity ceiling-breaker.

2. **The "10-day Cowork build" is a planning benchmark.** A small team using Claude Code shipped a launchable product with novel safety/VM infrastructure in ~10 days. Architecture roadmaps proposing multi-month substrate cycles should justify why, given Cowork did it in 10 days with much harder safety surface.

3. **"No hand-edited code since November 2025"** crosses a threshold we have not yet decided to adopt. StrongDM's charter ("Code must not be written or reviewed by humans") is the only stricter version. Cherny is at "Code not hand-written, PRs still human-reviewed." We should pick a level on this continuum and write it into the architecture docs.

---

## Open follow-ups

1. **Complete the YouTube transcript (minutes 30–90).** First 30 min landed 2026-05-13; remaining ~60 min not yet transcribed. Overnight long-transcription run was offered by the user — **recommended.** Likely contents include the parallel-session architecture, the third "principles for new team members," the Cowork 10-day timeline detail, the human-role-axis discussion, cost-per-day specifics, and any "what's next for Claude Code roadmap" beats.
2. **Cost-per-day for Cherny's own setup** — still not in minutes 0–30; we have only the "hundreds of thousands a month" figure for some Anthropic engineers in aggregate.
3. **What counts as a PR for 10–30/day** — Cherny stated the cadence verbatim but didn't define PR granularity. Spec-driven mini-PRs vs. feature-complete still unanswered.
4. ~~**The Cursor-to-Anthropic two-week return story**~~ — **RESOLVED.** Verbatim from minutes 0–30: he left for Cursor because "they saw where AI coding was going... before a lot of people did" and joined a team he respected; came back to Anthropic in two weeks because *"what I really missed about Anthropic was the mission... it's all about safety."* No drama, no equity story.
5. **Cherny's direct view on the human-role axis** — still open; expected in minutes 30–90.
6. **The full third "new team member principle"** — Lenny references it in passing in minutes 0–30 but Cherny doesn't enumerate the three as a list in this segment. Likely in minutes 30–90.

---

## Word count

~3,300 words including 2026-05-13 drain note (up from ~1,350 pre-drain).
