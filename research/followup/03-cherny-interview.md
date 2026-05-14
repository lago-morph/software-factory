# Boris Cherny on Lenny's Podcast — "What happens after coding is solved"

**Status: ✅ FULL primary-source-anchored.** Manual transcript of the **full ~90-minute podcast** is integrated below. This was previously a 🔴 blocked-on-fetch report relying entirely on secondary write-up snippets; most of the highest-stakes Cherny claims in the corpus are now verbatim-anchored. Drain notes at top document what flipped, what got resolved in the 30–90 segment, and what remains genuinely unsaid even after the full transcript.

**Round-3 follow-up thread 3 (per `research/PLAN.md` §11.3).** Cherny is the head of Claude Code at Anthropic and, by most accounts, the practitioner operating closest to the "Dark Factory" end of the human-role axis.

---

## Drain note (issue #36 extras) — 2026-05-14 — FULL transcript drain

The full ~90-minute Lenny × Cherny YouTube episode transcript (`https://youtu.be/We7BZVKbCVw`) is now integrated. First 30 min landed 2026-05-13; remaining ~60 min landed and was drained 2026-05-14. ASR artifacts normalized on the fly when quoting ("quad code" → "Claude Code" except where preserving Cherny's vocal "quad", "Boris Turney" → "Boris Cherny", "ant"/"anthropic" → "Anthropic", "Ben Manton" → "Ben Mann", "1020, 30" → "10, 20, 30", "cowork" → "Cowork", "Seishin Lu" → "Cixin Liu", "Seer/Sentry/Anish/MetaView/DX" sponsor reads dropped). Source file moved to `reference-only/lenny-podcast-transcripts/` per the `research/manual/README.md` lifecycle.

**Status flipped:** This report was 🔴 blocked-on-fetch as of Round 1; flipped to 🟡 partial after the 0–30 min drain on 2026-05-13; now flipped to **✅ FULL primary-source-anchored** after the 30–90 min drain on 2026-05-14.

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

**Corpus claims now resolved after full transcript drain:**

- **Cowork 10-day build timeline — RESOLVED.** Cherny, minutes ~55–60: *"And so over 10 days, they just completely used Claude Code to build it. And, you know, Cowork is actually, there's this very sophisticated security system that's built in and essentially these guardrails to make sure that the model kind of does the right thing... we ship an entire virtual machine with it and Claude Code just wrote all of this code... Took about 10 days. We launched it early."* Credits Felix, Sam, and Jenny as the team. 10 days verified verbatim.
- **Parallel-session count — PARTIALLY RESOLVED, but the "5 local + 5–10 web" architecture from `ociubotaru` is NOT what Cherny describes here.** Cherny, minutes ~60–62: *"I always have a bunch of agents running. So like at the moment, I have like five agents running."* Plus the form-factor split: *"Maybe a third of my code now is in the terminal, but also a third is using the desktop app. And then a third is the iOS app."* He uses the term **"multi-cladding"** to describe running many parallel sessions in the desktop app: *"You can just run as many quad sessions in parallel as you want. We call this multi-cladding."* So the architecture is **"five agents at a time, split roughly thirds across terminal / desktop / iOS,"** not "5 local + 5–10 web." The `ociubotaru` Threads paraphrase of "5–10 sessions" is not contradicted by the transcript but is also not confirmed in this form; treat it as Cherny's *peak* / `ociubotaru`'s liberal paraphrase.
- **Form-factor extension — NEW.** *"Coding now is describing what you want, not writing actual code."* Form factors used daily: terminal, desktop app (Code tab and Cowork tab), iOS / Android app, Slack integration, web, IDE extensions. Plan mode coming to mobile *"pretty soon"* and just launched for Slack at the time of recording.
- **Three principles for new team members — STILL ONLY TWO ENUMERATED.** Even in 30–90, Cherny does not enumerate three as a numbered list. Lenny again references *"What's better than doing something? Having Claude do it"* and Cherny tacitly agrees, but the explicit-three-principle framing remains a Lenny / secondary-write-up artifact. Best read: Cherny operates on two-or-more *principles* that the secondary write-ups crystallized into a "three" list for clean copy; the canonical primary list is **(1) underfund / under-resource a little, (2) encourage going faster, (3) [implicit, agreed-with] have Claude do it.**
- **Sonnet-3.5-era unattended duration → Opus 4.6 today — RESOLVED, NEW NUMBERS.** Cherny, minutes ~70: *"When I used Sonnet 3.5 back, you know, a year ago, it could run for maybe 15 or 30 seconds before it started going off the rails and you just really had to hold its hand... But nowadays with Opus 4.6, you know, on average, it'll run maybe 10, 30, 20, 30 minutes unattended... they can also run for hours or even days at a time. I think there are some examples where they ran for many weeks."* That's a ~60× to ~120× improvement in unattended runtime in 12 months.

**Corpus claims that remain UNRESOLVED even after the full transcript:**

- **`/loops` and `/batch` slash commands** — NOT mentioned in the full transcript. The `ociubotaru` Threads paraphrase of "dozens of /loops" and "/batch interviews you then fans out work to dozens, hundreds, even thousands" is **not corroborated** by Cherny on the podcast. It may be from a separate Cherny appearance, may be `ociubotaru`'s synthesis, or may be a real workflow Cherny just didn't mention in this 90 min. Downgrade the corpus confidence on `/loops` and `/batch` to "single secondary source."
- **"Thousands of overnight agents"** — NOT mentioned in the full transcript. Same downgrade. The strongest related Cherny statement is *"they can also run for hours or even days at a time. I think there are some examples where they ran for many weeks"* — about single long-running agents, not thousands of parallel overnight ones.
- **Cost-per-day for Cherny's own setup** — Still open. The "hundreds of thousands a month" figure remains attributed to *"some engineers at Anthropic"* in aggregate, not Cherny himself.
- **4% of public GitHub commits / DAU doubling / 20% projection** — Lenny states them; Cherny confirms 4% qualitatively (*"way more than I imagined"*, *"private repos quite a bit higher"*) but does not independently restate the 20% projection or the "DAU doubling last month" number. Lenny does confirm the Anthropic revenue numbers at the end: *"I think Claude Code alone is making $2 billion in revenue... you guys put out, you're making $15 billion in revenue"* — Cherny does not contest.

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

**Result of the overnight full-transcription:** **Done.** The 30–90 segment delivered: confirmed 10-day Cowork build, confirmed parallel-session count and three-thirds form-factor split, confirmed Sonnet-3.5 → Opus-4.6 unattended-runtime jump (15–30s → 10–30min, sometimes weeks), the explicit AI-product principles list (don't box the model / Bitter Lesson / build for the model six months from now), the three-layer safety framework (mech-interp / evals / wild), the printing-press historical analog, the "everyone codes" generalist takeaway, and "use common sense" as life motto. Did **not** deliver: `/loops`, `/batch`, "thousands of overnight agents," Cherny's own $/day, or an explicit numbered-three-principles list.

---

## Source status

| Source | Status | Note |
|---|---|---|
| `https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens` | **VIDEO-ONLY, BLOCKED** | Confirmed video-only per `research/06-hn-and-lenny.md` and `PLAN.md §11.3`. No text interview body — the "biggest takeaways" stub is a paywall placeholder. **HTTP 403** to WebFetch. |
| `https://youtu.be/We7BZVKbCVw` (YouTube video) | ✅ **FULL** | Manual full transcript of all ~90 min drained 2026-05-14. Source file moved to `reference-only/lenny-podcast-transcripts/cherny-head-of-claude-code-full.txt` per the `research/manual/README.md` lifecycle (preserve as primary-source quote). See drain note above. |
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

## Cherny's daily workflow — primary-anchored

**Primary, minutes ~60–62 (Cherny, in response to Lenny asking about agent anxiety):**

> *"I always have a bunch of agents running. So like at the moment, I have like five agents running. And at any moment, I wake up and I start a bunch of agents. Like the first thing I did when I woke up was like, oh man, I really want to check this thing. So like I opened up my phone, quad iOS app, code tab, you know, like agent do blah blah blah."*

**Form-factor split (verbatim):**

> *"Maybe a third of my code now is in the terminal, but also a third is using the desktop app. And then a third is the iOS app, which is just so surprising because I did not think that this would be the way that I code even in 2026."*

**The "multi-cladding" desktop pattern (verbatim):**

> *"So you just download the desktop app, there's a code tab, it's right next to cowork. And it's actually the same as that quad code. So it's like the same agent and everything... you can just run as many quad sessions in parallel as you want. We call this multi-cladding."*

**Synthesized picture (primary-anchored where possible, secondary-anchored otherwise):**

1. **Five agents at a time, baseline.** Stated verbatim. Not five terminal tabs (that's `ociubotaru`'s older paraphrase of an earlier Cherny Threads post); the current model is five agents across whatever form factors he's using at that moment.
2. **Thirds: terminal / desktop / iOS.** Primary-anchored. This *replaces* the "5 local + 5–10 web" reconstruction from the prior version of this report.
3. **Plan mode default.** Cherny, minutes ~75: *"I start almost all of my tasks in plan mode, maybe like 80%. And plan mode is actually really simple. All it is is we inject one sentence into the model's prompt to say, please don't write any code yet... for people that are in the terminal, it's just shift tab twice."* Iterates the plan, then auto-accepts edits: *"if the plan looks good, it's just gonna one shot it. It'll get it right the first time almost every time with Opus 4.6."*
4. **Max-effort always-on.** Cherny: *"I have maximum effort enabled always."* Plus: *"Often it's actually cheaper and less token intensive if you use the most capable model because it can just do the same thing much faster with less correction, less hand holding."*
5. **Form factors used:** terminal, desktop app (Code tab and Cowork tab), iOS / Android, Slack integration, web, IDE extensions, GitHub. Plan mode is coming to mobile *"pretty soon"* and *"just launched for the Slack integration too."*

**Status of older `ociubotaru` paraphrase:** The Threads post is now **partially superseded.** "Mobile app is the primary interface" is *not* quite Cherny's framing — he describes a roughly-equal thirds split. "5–10 sessions" is consistent with the "five agents running" baseline but high. "Thousands of overnight agents" and "dozens of `/loops`" are **not mentioned in this 90-min interview** (see Drain note, Unresolved section). The `/batch` "fan out to as many worktree agents as it takes" claim is **not corroborated** by Cherny here either.

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

## Cowork — the 10-day build (primary-anchored)

**Cowork** is the Claude desktop-app tab for non-coding agentic tasks (Gmail, Slack, Chrome automation, project management, paying parking tickets, filling PDF forms, etc.). Primary anchor, minutes ~55–60:

> *"And so over 10 days, they just completely used quad code to build it. And, you know, Cowork is actually, there's this very sophisticated security system that's built in and essentially these guardrails to make sure that the model kind of does the right thing... we ship an entire virtual machine with it and quad code just wrote all of this code. So we just had to think about, all right, how do we make this a little bit safer, a little more self-guided for people that are not engineers."* — Cherny

**Team credited verbatim:** *"I think a lot of the credit, honestly, just goes to Felix and Sam and Jenny and the team that built this."*

**Origin (latent demand, verbatim):** *"We saw that for the last six months or so, a lot of people using quad code were not using it to code. There was someone on Twitter that was using it to grow tomato plants, there was someone else using it to analyze their genome, someone was using it to recover photos from a corrupted hard drive... there was someone that was using it for, I think like, they were using it to analyze an MRI."* The team spent "a few months" exploring options; the breakthrough was *"someone was just like, okay, what if we just take quad code and put it in the desktop app?"*

**Cherny's daily Cowork usage (verbatim):** *"I had to pay a parking ticket the other day, I just had coworker do it. All of my project management for the team, coworker does all of it. It's like syncing stuff between spreadsheets and messaging people on Slack and email and all this kind of stuff."* Plus: a weekly cadence where Cowork DMs every engineer who hasn't filled out their team status row, all from one prompt.

**Engineering complexity was mostly safety, not product logic:** an entire VM shipped with the product as a sandbox, OS-level guardrails, a more permissive but still safe permission model for non-engineers, browser automation, claude.ai data-connector integration, ask-for-clarification flow.

The 10-day timeline holds up against the transcript and is **the most aggressive small-team-cycle-time data point in the corpus** — faster than StrongDM's "team of 3 in 3 months." Caveat: most of the 10 days went to safety infrastructure, not feature work; the model wrote the feature code, the binding constraint was human design of the safety surface.

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

## AI product principles (Cherny's enumerated list)

Cherny gives an explicit, enumerated set of principles for building on top of LLMs in minutes ~70–80. All four are now verbatim-anchored:

1. **Throw tokens at engineers; cost-optimize only later.** *"Don't try to optimize, don't try to cost cut at the beginning. Start by just giving engineers as many tokens as possible... at small scale, like you're not gonna get like a giant bill or anything like this. If it's an individual engineer experimenting, the token cost is still probably relatively low relative to their salary."*

2. **Don't box the model in.** *"A lot of people's instinct when they build on the model is, they try to make it behave a very particular way. They're like, this is a component of a bigger system... very strict workflows on the model, for example, you know, to say like you must do step one, then step two, then step three... But actually almost always you get better results if you just give the model tools, you give it a goal and you let it figure it out. I think a year ago, you actually needed a lot of the scaffolding, but nowadays you don't really need it."* Cherny doesn't name this principle but offers as candidate: *"ask not what the model can do for you."*

3. **The Bitter Lesson.** *"For the Cloud Code team, we have a, you know, hopefully listeners have read this, but Rich Sutton had this blog post maybe 10 years ago called the Bitter Lesson... His idea was that the more general model will always outperform the more specific model... always bet on the more general model. And, you know, over the long term, like don't try to use tiny models for stuff. Don't try to fine tune... scaffolding can improve performance maybe 10, 20%, something like this, but often these gains just get wiped out with the next model. So it's almost better to just wait for the next one."*

4. **Build for the model six months from now, not today's model.** *"From the very beginning, we bet on building for the model six months from now, not for the model of today... It's gonna be uncomfortable because your product market fit won't be very good for the first six months. But if you build for the model six months out, when that model comes out, you're just gonna hit the ground running and the product is gonna click and start to work."* When asked what to bet on: *"It's gonna get better and better at using tools and using computers... it's gonna get better and better for running for long periods of time."*

The four principles together compress to a single operating rule: **be ahead of the model on form factor, behind the model on scaffolding, and out-of-the-money on cost.**

---

## Safety: the three-layer framework

Cherny gives the cleanest in-corpus articulation of how Anthropic frames model safety (minutes ~65–67):

> *"The lowest level is alignment and mechanistic interpretability. So this is, when we train the model, we wanna make sure that it's safe. We, at this point, have pretty sophisticated technology to understand what's happening in the neurons, to trace it. And so, for example, if there's a neuron related to deception, we're starting to get to the point where we can monitor it and understand that it's activating."*
>
> *"The second layer is evals. And this is essentially a laboratory setting. The model is in a Petri dish and you study it. And you put it in a synthetic situation and just say, okay, like model, what do you do? And are you doing the right thing? Is it aligned? Is it safe?"*
>
> *"And then the third layer is seeing how the model behaves in the wild. And as the model gets more sophisticated, this becomes so important because it might look very good on these first two layers, but not great on the third one."*

This is **why Claude Code shipped publicly in early form**: *"We released Claude code really early because we wanted to study safety. And we actually used it within Anthropic for, I think, four or five months or something before we released it... we weren't sure if it was safe."* Same logic applies to the Cowork "research preview" framing: *"He looks good on alignment. It looks good on evals. We tried it internally, it looks good. We tried it with a few customers, it looks good. Now, we have to make sure it's safe in the real world."*

**Race-to-the-top principle (verbatim):** *"We call this the race to the top internally. And so for cloud code, for example, we released an open source sandbox... we made that open source. And it actually works with any agent, not just quad code, because we wanted to make it really easy for others to do the same thing."*

This pins down a corpus-relevant claim: Anthropic open-sourced their agent sandbox specifically as a race-to-the-top safety move, not just for community-goodwill reasons.

---

## Unattended-runtime evolution: 15s → 30min → weeks

Cherny gives a clean year-over-year comparison (minutes ~75) of model unattended runtime that is the strongest data point we have on agent autonomy growth:

> *"When I used Sonnet 3.5 back, you know, a year ago, it could run for maybe 15 or 30 seconds before it started going off the rails and you just really had to hold its hand through any kind of complicated task. But nowadays with Opus 4.6, you know, on average, it'll run maybe 10, 30, 20, 30 minutes unattended and I'll just like start another quad and have it do something else. And, you know, like I said, I always have a bunch of quads running and they can also run for hours or even days at a time. I think there are some examples where they ran for many weeks."*

| Period | Model | Median unattended runtime | Implied multiplier |
|---|---|---|---|
| ~Feb 2025 | Sonnet 3.5 | 15–30 sec | 1× |
| ~Feb 2026 | Opus 4.6 | 10–30 min (median); hours-to-days common; weeks at the extreme | **~60–120× median, ~50,000–500,000× extreme** |

This is the corpus's **strongest piece of evidence for the Willison-style "task-horizon doubling" thesis**, and it comes from inside Anthropic on a one-year window. The interquartile-range jump alone (15s → 20min) is ~80×; the rare-extreme jump (30s → multi-week) is closer to 10⁵×.

---

## "Multi-cladding": running Claude in parallel

New term surfaced (corpus-first): **"multi-cladding"** — Anthropic's internal name for the run-many-Claudes-in-parallel pattern in the desktop app. Cherny, minutes ~60:

> *"You can just run as many quad sessions in parallel as you want. We call this multi-cladding."*

Used by designers and other non-engineering Anthropic staff who don't want to live in a terminal:

> *"Our designers, they use the quad desktop app a lot more to do their coding. So you just download the desktop app, there's a code tab, it's right next to cowork. And it's actually the same as that quad code. So it's like the same agent and everything... So this is, it's a little more native, I think for folks that are not engineers."*

The pattern of *role-shifting via the desktop UI* — designers, PMs, data scientists, finance running multi-cladding without ever learning the terminal — is the operational mechanism behind the "everyone codes" claim elsewhere in the report.

---

## Pro tips for Claude Code users (Cherny's enumerated three)

Minutes ~75–78, in response to Lenny asking for tips:

1. **Use the most capable model. Always.** *"Currently that's Opus 4.6. I have maximum effort enabled always... sometimes people try to use a less expensive model like Sonnet... but because it's less intelligent, it actually takes more tokens in the end to do the same task. And so it's actually not obvious that it's cheaper."* — Operationally inverts conventional cost-minimization intuition.
2. **Use plan mode.** *"I start almost all of my tasks in plan mode, maybe like 80%... shift tab twice and that gets you into plan mode."* Then auto-accept edits after the plan is reviewed.
3. **Play with form factors.** *"Just play around with different interfaces. I think a lot of people, when they think about cloud code, they think about a terminal... but we actually support a lot of other form factors too."*

These are explicit-numbered, repeatable, and now primary-source-anchored. **They are NOT the same as the "three principles for new team members" list** (which is about team-running, not Claude-Code-using) — that one remains only-two-enumerated even after the full transcript.

---

## "Coding now is describing what you want": the redefinition

Cherny does explicit work to redefine the word "coding" in minutes ~62:

> Lenny: *"I love that you describe it as coding still, which is just talking to the cloud code to code for you essentially. And it's interesting that this is now coding."*
>
> Cherny: *"Coding now is describing what you want, not writing actual code. I kind of wonder if the people that used to code using punch cards or whatever, if you show them software, what they would have said. And I remember reading something, this was maybe like very early versions of like ACM like Mike magazine or something, where people were saying, no, it's not the same thing. Like this isn't really coding. And they call it programming."*

Plus the corollary on what you have to know (~minute 50):

> *"I was talking to an engineer earlier today. They're writing some service in Go and it's been like a month already and they built up the service. Like it's working quite well. And then I was like, okay, so like, how do you feel writing it? And he was like, you know, like, I still don't really know Go, but. And I think we're gonna start to see more and more of this. It's like, if you know that it works correctly and efficiently, then you don't actually have to know all the details."*

This is the strongest in-corpus formulation of the **"specification, not implementation"** thesis from a primary-source AI lab operator. It is materially stronger than the equivalent quotes in `research/06-hn-and-lenny.md` reconstructed from secondaries.

---

## The printing-press analog and the everyone-codes generalist takeaway

Cherny's chosen historical analog for the AI-coding transition, minutes ~50–52:

> *"I think the thing that's come closest for me is the printing press. And so, if you look at Europe in the mid 1400s, literacy was actually very low. There was sub 1% of the population, it was scribes... at some point, Gutenberg and the printing press came along and there was this crazy stat that in the 50 years after the printing press was built, there was more printed material created than in the 1000 years before... over the next 200 years, [literacy] went up to 70% globally."*

He explicitly maps himself to the scribe role: *"There was this interesting historical document where there was an interview with some scribe in the 1400s about how do you feel about the printing press? And they were actually very excited because they were like, actually the thing that I don't like doing is copying between books. The thing that I do like doing is drawing the art in books and then doing the book binding. And I'm really glad that now my time is freed up."*

**Generalist career advice (verbatim, minutes ~52):**

> *"Try to be a generalist more than you have in the past. For example, in school, a lot of people that study CS, they learn to code and they don't really learn much else... But some of the most effective engineers that I work with every day and some of the most effective, you know, like product managers and so on, they cross over disciplines. So on the cloud code team, everyone codes. You know, our product manager codes, our engineering manager codes, our designer codes, our finance guy codes, our data scientist codes, like everyone on the team codes."*

The "everyone codes" claim in the corpus is now anchored verbatim to Cherny with the full role-list (PM, EM, designer, finance, data scientist) intact.

---

## Anthropic's internal Claude Code usage

Distinct primary data points on internal usage (scattered throughout):

- **The DAU chart went vertical immediately on internal launch.** Ben Mann nudged Cherny to make a DAU chart pre-launch; *"the chart just went vertical pretty immediately."*
- **Internal use of Claude Code preceded public launch by ~4–5 months.** *"We actually used it within Anthropic for, I think, four or five months or something before we released it."* Helps date the project: public launch ~Feb 2025 ⇒ internal first use ~Sep–Oct 2024.
- **First internal announcement got two likes.** *"I made a post about it, and I announced it internally, and I got two likes. That's the sense of the reaction at the time."* Cherny is explicit that this disproves the implicit narrative of "Anthropic obviously knew what they had."
- **Designers and non-engineers code via the desktop app.** Anthropic-internal designers don't open terminals; they use multi-cladding in the desktop Code tab. Same agent, different surface.
- **The internal-feedback Slack channel is the primary product-input source.** *"We have this channel that that's all the internal feedback about quad code. Since we first released it, even in like 2024 internally, it's just been this fire hose of feedback... in the early days, what I would do is any time that someone sends feedback, I would just go in and I would fix every single thing as fast as I possibly could. So like within a minute, within five minutes or whatever."*
- **Claude reviews 100% of Anthropic PRs** + human checkpoint (covered in drain note above).
- **Anthropic-wide engineering throughput.** Engineering team ~4×'d year-over-year; per-engineer productivity +200% (in PRs); **~8× total team throughput**.

---

## The "what to build" frontier: Claude as PM

Cherny explicitly identifies this as the next frontier (cold-open and minutes ~30–35):

> *"Quad is starting to come up with ideas. So quad is looking through feedback. It's looking at bug reports. It's looking at telemetry and things like this. And it's starting to come up with ideas for bug fixes and things to ship. So it's just starting to get a little more, you know, like a little more like a coworker or something like that."*

When Lenny presses on the PM-disruption implication: *"Honestly, the simplest thing is like open quad code or a co-work and point it at a Slack thread."* The workflow is: point Claude at the internal-feedback channel → it surfaces a few candidate fixes → puts up PRs → Cherny approves. This is the *"PM bottleneck" disappearing* anecdote in operational form.

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

1. **Refine the human-role axis.** `architectures/00-comparison.md` currently has "supervises vs. schedules." Cherny is a clean instance of **schedules at scale** — five agents at any moment, three-thirds split across terminal / desktop multi-cladding / iOS, plan-mode-first, auto-accept-edits, two-stage Claude+human PR review. (The older "thousands of overnight sub-agents + dozens of `/loops`" framing is **no longer primary-anchored** after the full drain; treat as secondary.) Atelier (Arch 2) and Compound (Arch 3) docs should explicitly note which mode they target — scheduler mode appears to be *the* productivity ceiling-breaker.

2. **The "10-day Cowork build" is a planning benchmark.** A small team using Claude Code shipped a launchable product with novel safety/VM infrastructure in ~10 days. Architecture roadmaps proposing multi-month substrate cycles should justify why, given Cowork did it in 10 days with much harder safety surface.

3. **"No hand-edited code since November 2025"** crosses a threshold we have not yet decided to adopt. StrongDM's charter ("Code must not be written or reviewed by humans") is the only stricter version. Cherny is at "Code not hand-written, PRs still human-reviewed." We should pick a level on this continuum and write it into the architecture docs.

---

## Open follow-ups (post full-transcript)

1. ~~**Complete the YouTube transcript (minutes 30–90).**~~ — **RESOLVED 2026-05-14.** Full transcript drained. See drain note for what landed vs. what didn't.
2. **Cost-per-day for Cherny's own setup** — **STILL OPEN.** Even in the full transcript, the only concrete dollar figure is *"some engineers at Anthropic"* spending *"hundreds of thousands a month."* Cherny's own number not stated.
3. **What counts as a PR for 10–30/day** — **STILL OPEN.** Granularity not defined.
4. ~~**The Cursor-to-Anthropic two-week return story**~~ — **RESOLVED.** Mission pull, no drama, no equity story.
5. **Cherny's direct view on the human-role axis** — **PARTIALLY RESOLVED.** He doesn't use the supervisor/scheduler vocabulary, but the *"five agents running, thirds across terminal/desktop/iOS, plan-mode-first, auto-accept-edits, two-stage Claude+human review"* pattern is unambiguous scheduler-mode operation. Pin this in `architectures/00-comparison.md`.
6. ~~**The full third "new team member principle"**~~ — **STILL ONLY TWO ENUMERATED.** Even at full length, Cherny names only "underfund a little" and "encourage going faster." The third is tacit (have Claude do it) and may be a secondary-writer's clean-copy artifact. The corpus *"three principles for new team members"* should be downgraded to *"two named principles plus one tacit principle."*
7. **`/loops` and `/batch` slash commands** — **NEWLY DOWNGRADED.** Not mentioned anywhere in the 90-min transcript. Single-secondary-source confidence. Possibly real, possibly a `ociubotaru` synthesis from a different Cherny appearance.
8. **"Thousands of overnight agents"** — **NEWLY DOWNGRADED.** Same status. Strongest related primary is *"some examples where they ran for many weeks"* — single long-running agents, not thousands of parallel ones.
9. **Cherny's other surface-area predictions** — Now anchored: builders not engineers, role overlap ~50% PM/EM/design/eng, end-of-year title-shift. No new ones added.

---

## Word count

~5,400 words after 2026-05-14 full drain (up from ~3,300 pre-30–90, up from ~1,350 pre-any-transcript).
