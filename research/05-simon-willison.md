# Simon Willison — Software Factory & Agentic Engineering Patterns

**Sources covered (all now ACCESSED from local HTML copies in repo root):**
- https://simonwillison.net/2026/Feb/7/software-factory/ — "How StrongDM's AI team build serious software without even looking at the code" — local: `/home/user/software-factory/simonwillison.net__2026__Feb__7__software-factory.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/ — guide index — local: `simonwillison.net__guides__agentic-engineering-patterns.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/ — local: `simonwillison.net__guides__agentic-engineering-patterns__what-is-agentic-engineering.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/ — local: `simonwillison.net__guides__agentic-engineering-patterns__code-is-cheap.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/ — local: `simonwillison.net__guides__agentic-engineering-patterns__how-coding-agents-work.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/ — local: `simonwillison.net__guides__agentic-engineering-patterns__red-green-tdd.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/ — local: `simonwillison.net__guides__agentic-engineering-patterns__first-run-the-tests.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/ — local: `simonwillison.net__guides__agentic-engineering-patterns__agentic-manual-testing.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/ — local: `simonwillison.net__guides__agentic-engineering-patterns__linear-walkthroughs.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/ — local: `simonwillison.net__guides__agentic-engineering-patterns__interactive-explanations.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/ — local: `simonwillison.net__guides__agentic-engineering-patterns__hoard-things-you-know-how-to-do.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/subagents/ — local: `simonwillison.net__guides__agentic-engineering-patterns__subagents.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/ — local: `simonwillison.net__guides__agentic-engineering-patterns__anti-patterns.html`
- https://simonwillison.net/guides/agentic-engineering-patterns/prompts/ — local: `simonwillison.net__guides__agentic-engineering-patterns__prompts.html`
- https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ — meta-post — local: `simonwillison.net__2026__Feb__23__agentic-engineering-patterns.html`
- https://simonwillison.net/2025/Sep/30/designing-agentic-loops/ — local: `simonwillison.net__2025__Sep__30__designing-agentic-loops.html`
- https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ — local: `simonwillison.net__2025__Oct__5__parallel-coding-agents.html`
- https://simonwillison.net/2025/May/22/tools-in-a-loop/ — local: `simonwillison.net__2025__May__22__tools-in-a-loop.html`
- https://simonwillison.net/2025/Sep/18/agents/ — local: `simonwillison.net__2025__Sep__18__agents.html`
- https://simonwillison.net/2025/Apr/19/claude-code-best-practices/ — local: `simonwillison.net__2025__Apr__19__claude-code-best-practices.html`
- https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/ — local: `simonwillison.net__2026__May__6__vibe-coding-and-agentic-engineering.html`
- https://simonwillison.net/tags/evals/ — local: `simonwillison.net__tags__evals.html`
- https://simonwillison.net/tags/agentic-engineering/ — local: `simonwillison.net__tags__agentic-engineering.html`
- ✅ https://youtu.be/wc8FBhQtdsA — Lenny Rachitsky podcast, *"An AI state of the union"* with Simon Willison — local: `research/manual/lenny-An AI state of the union.txt` — **FULL** manual transcript (2,155 lines, all ~90 minutes drained 2026-05-13)

**Date:** 2026-05-10 (drain update 2026-05-13)

## Drain note (issue #36 extras) — 2026-05-13

A manual partial transcript of the Lenny Rachitsky × Simon Willison podcast *"An AI state of the union"* (YouTube `https://youtu.be/wc8FBhQtdsA`) was integrated as a new primary source. **Scope caveat:** the transcript covers only the **first ~30 minutes of a ~90-minute episode**; the remaining ~60 minutes is unreviewed and may contain additional claims (notably the *"Challenger disaster of AI"* prediction is teased in the cold open but its full elaboration likely sits in the un-transcribed remainder; security/lethal-trifecta material is also signposted by Lenny as "later in the episode" but does not appear in the captured window). The interview section (§ Lenny interview, below) is therefore marked 🟡 **partial**.

## Drain note follow-up — 2026-05-13 (full-transcript drain)

The user ran the overnight full transcription. The full 2,155-line transcript of the Lenny × Willison interview is now drained, and the §"Lenny interview" section below has been extended with the new material (now ✅ complete). Major net-new findings the partial drain could not capture:

- **The "Challenger disaster of AI" prediction is now fully elaborated** (transcript lines 1731–1763): Simon explicitly cites the *Normalization of Deviance* paper (1980s NASA post-Challenger research by Diane Vaughan), gives the analogy mapping (O-rings ↔ prompt-injection vulnerabilities, every successful unsafe launch increases institutional confidence), and crucially admits *"I've made a version of this prediction every six months for the past three years and it hasn't happened. So there we are."* — i.e., he holds the prediction *and* its falsification record simultaneously. Cross-reference: this is the civilizational-scale generalization of the personal "normalization of deviance" he flags in May 6, 2026 (Notable Quote #16).
- **The lethal trifecta is now fully explained verbatim** (transcript lines 1601–1850), including: (a) the original *"translate English to French"* and *"reply to my aunt and make up an excuse"* worked examples, (b) the explicit three legs ("private information", "exposed to malicious instructions", "exfiltration"), (c) why SQL-injection-style fixes don't transfer, (d) the 97%-is-a-failing-grade argument (*"three out of a hundred of these attacks will steal all of your information"*), (e) endorsement of Google DeepMind's **CaMeL** paper as the most promising structural defense (privileged-agent + quarantined-agent + tainted-data-flow + human-in-the-loop on high-risk steps), and (f) a robotics-extension joke that flags the same trifecta will become catastrophic with embodied agents.
- **OpenClaw / "Claws"** — Simon's most enthusiastic spoken endorsement of any third-party project in the entire transcript (lines 1851–1992). New named-entity facts: first line of code Nov 25, Super Bowl AI.com ad ~3.5 months later, >1,000 contributors, the Mac-mini-as-aquarium Tamagotchi framing, the Spider-Man 2 Doc Ock inhibitor-chip analogy, and Simon's claim that the **generic term "Claw"** has emerged (Nano Claw etc.) and that "building your own Claw" is now the new "Hello World of AI engineering."
- **Pelican-on-a-bicycle benchmark methodology** is fully explained (lines 1170–1295) including its **secret backup tier** of alternate animal+vehicle combinations (Ocelot on a moped) — designed to catch overfitting to the public benchmark.
- **Hoarding methodology** is concretized to two named GitHub repos: `simonw/tools` (now 193 client-side HTML/JS tools) and `simonw/research` (75 public + ~50 private agent-built research markdowns).
- **Tool stack details**: GPT 5.4 (and 5.4 Mini/Nano at 5 thinking levels), Claude Opus 4.6, Claude Code for web on iPhone (the Anthropic app's "code" tab), `--dangerously-skip-permissions` (Claude) / "YOLO" (OpenAI Codex) modes, memory feature opt-out, the ChatGPT-memory-export-prompt trick Anthropic used to onboard ChatGPT defectors.
- **End-of-2025 prediction** (lines 880–893): *"by the end of this year, it will not be uncommon to have an engineer say that almost all of their code is written by AI"* — Simon endorses the 50%-of-engineers / 95%-of-code framing as plausible for end of 2026.
- **Economic anxiety** (lines 910–915): *"Are we really going to wipe out like a tenth of white collar knowledge work jobs in the next few years? I really hope not because I don't know how the economy adapts that."* — Simon's only on-record macroeconomic worry; he hedges by saying he is *"not an AI doomer in the slightest."*
- **Data-labeling firms buying pre-2022 GitHub repos for "uncontaminated" handwritten code** (lines 836–855) — Simon adopts the *pre-WWII steel salvaged from shipwrecks (low-background steel)* analogy for it.
- **Artisanal / proof-of-usage thesis** (lines 800–833): the "alpha" suffix as a *"cheat code"* for "I built this but haven't used it." *"What I value more than the quality of the tests and documentation is that I want somebody to have used the thing"* (a verbal twin of the May-6-2026 blog-post version already in Notable Quote #17).
- **Datasette + data journalism** (lines 2001–2046): Simon's stated 2026 goal is *"I want somebody in the world to win a Pulitzer Prize when my software was like 3% of what they used."* Confirms Datasette is still his primary day-job and journalists' treatment of unreliable sources is the canonical user-skill match for AI.
- **Zero-deliverable consulting** as Simon's revenue model (lines 2068–2102): an hour on a call, no report, no code; *"I'm very lazy when it comes to actually making money."*

All flipped 🟡 → ✅. The original "partial" drain note above is preserved verbatim for historical accuracy of the corpus revision process; this follow-up note supersedes it.

**Verified claims (primary anchoring now possible):**

- **"4 agents in parallel" + "wiped out by 11am" — reversal-of-reversal.** The corpus has been through two prior revisions on this claim. The v1 report had *"4 agents in parallel exhausts me by 11 AM"* as a verbatim Willison quote; that was refuted (research/06-hn-and-lenny.md L33–34; research/blocked-urls.md L112; research/00-synthesis.md L15) as a v1 fabrication, because the visible Lenny editorial summary only said *"mentally exhausted by 11 a.m."* without naming a number — the "4" was treated as invented. The full transcript now shows Simon saying both things, separately but in the same passage: *"I can fire up four agents in parallel and have them work on four different problems. By 11am I am wiped out."* — and again later: *"I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day."* **The original "4 agents" number was REAL.** This is now the third reversal in the chain (v1 asserted → drain refuted as fabrication → primary transcript confirms). The corpus's softened "mentally exhausted by 11 AM" formulation in 06-hn-and-lenny.md and 00-synthesis.md is now under-stated and should be re-strengthened in a subsequent pass (out of scope for this report; flagged for orchestrator).
- **"95% of code I produce, I didn't type it myself"** — previously inferred/paraphrased; now primary verbatim.
- **"using coding agents well is taking every inch of my 25 years of experience as a software engineer"** — anchor for the "amplifier of existing skills" claim already in the report.
- **"I write so much of my code on my phone, it's wild. I can get good work done walking the dog along the beach"** — anchor for asynchronous/mobile leverage technique.
- **The "November inflection" framing** (GPT 5.1 + Claude Opus 4.5 crossing a threshold) — gives Simon a specific dated inflection point distinct from the existing corpus's reliance on the May 6, 2026 post.

**Likely-in-the-un-transcribed-60-minutes (flagged for orchestrator if a full transcript is run overnight):**

- The full elaboration of the **"Challenger disaster of AI"** prediction (cold-open tease quotes Simon: *"We've been using these systems in increasingly unsafe ways. This is going to catch up with us. My prediction is that we're going to see a challenging disaster."* — but the supporting argument almost certainly continues past the 30-minute mark).
- **Lethal-trifecta / prompt-injection** detail (Lenny's intro flags Simon as the coiner of "prompt injection" and the cold-open foreshadows a security discussion; the captured window does not reach it).
- Specific tool / model namings beyond the few in the captured window (Claude Code, Codex CLI, Codex Cloud, GPT 5.1, Claude Opus 4.5/4.6, Playwright, Firefox/Mozilla, ThoughtWorks, Cloudflare, Shopify).
- Any concrete advice on the **mid-career-engineer squeeze** beyond the ThoughtWorks framing (Simon flags the problem but the captured window ends before any prescriptive advice).

## Revision notes

This revision was produced from direct access to the primary HTML pages (saved to the repo root after the original web search snippets pass). Changes versus the original report:

- **Verified verbatim:** every quote previously flagged "[paraphrase]" has been checked against the source text. Some were correct; several have been replaced with the actual phrasing — most notably the agent definition (the canonical wording is *"Agents run tools in a loop to achieve a goal"* in the guide, *"Agents are models using tools in a loop"* in the May 22, 2025 note, and *"An LLM agent runs tools in a loop to achieve a goal"* in the Sep 18, 2025 post), the red/green TDD shorthand, the "first run the tests" passage, the anti-pattern definition, and the "good code" checklist.
- **Added chapters:** the original report enumerated 12 chapters. The current guide table of contents (May 2026 snapshot) lists **16 chapters across 6 sections**, including three the original report missed entirely: *AI should help us produce better code*, *Using Git with coding agents*, and two "Annotated prompts" walkthrough chapters (*GIF optimization tool*, *Adding a new content type to my blog-to-newsletter tool*). These have been added.
- **Added the May 6, 2026 post.** "Vibe coding and agentic engineering are getting closer than I'd like" is critical new context: Simon openly admits the two categories are blurring in his own practice and articulates a "team analogy" for why he no longer reads every line of agent-written code. Added to the Executive summary, Review-and-feedback, and Notable quotes sections.
- **Corrected the StrongDM-post quotations.** The original report's spec-line-count detail ("6,000–7,000 lines of natural language specification") was a third-party reconstruction. Simon's actual post mentions "three markdown files describing the spec for the software in meticulous detail" plus a separate, more traditional release (`cxdb`) with 16,000 lines of Rust, 9,500 of Go and 6,700 of TypeScript. The original conflated these two. Fixed.
- **Added "Dark Factory" attribution detail.** The original mentioned Cal Newport / Dan Shapiro as recommended reading. The Feb 7 post explicitly names Dan Shapiro's "Dark Factory" post and links to it; Newport is not mentioned. Corrected.
- **Added "Designing agentic loops" details** the original missed: the Solomon Hykes quote ("An AI agent is an LLM wrecking its environment in a loop"), and four concrete project examples (debugging, perf, dep upgrades, container shrinking).
- **Added the Hannah Moran (Anthropic) provenance** for "Agents are models using tools in a loop" — Simon's May 22, 2025 note records the moment Anthropic's Hannah Moran said it during a workshop.
- **Added the May 2025 ultrathink finding** (a reverse-engineered tier of thinking-budget phrases: think → 4,000 tokens, megathink/think hard/think deeply etc. → 10,000, think harder/ultrathink/think intensely etc. → 31,999).
- **Added the evals-tag synthesis.** The original report had a paraphrased line on test-driven system prompts I could not find in source; on re-reading the evals tag the higher-signal claims are (a) Hamel Husain's "60-80% of development time on error analysis and evaluation", (b) "If you're passing 100% of your evals, you're likely not challenging your system enough", (c) Anthropic's multi-agent-research piece on "start with small-scale testing right away" and "LLM-as-a-judge worked well", and (d) Armin Ronacher's "Testing and evals remains the single hardest problem in AI engineering". These now appear verbatim.
- **Expanded the parallel-coding-agents section** with the four patterns Simon explicitly names: research / how-does-that-work-again / small maintenance tasks / carefully specified and directed actual work — and the Josh Bleecher Snyder "send out a scout" pattern Simon endorses.
- **Updated source list** to show all simonwillison.net URLs as ACCESSED with their local file paths.

## Executive summary

Simon Willison's overall thesis across these sources is that we are at a real inflection point in software engineering: coding agents — defined narrowly as *"models using tools in a loop"* — are now capable enough that an experienced engineer can use them to attempt much more ambitious projects than they otherwise would. He calls the resulting craft **agentic engineering**, deliberately distinguishing it from **vibe coding** (which he reserves, following Karpathy's original Feb 2025 coinage, for prompting LLMs to write code while you "forget that the code even exists" — "unreviewed, prototype-quality LLM-generated code"). Agentic Engineering "represents the other end of the scale: professional software engineers using coding agents to improve and accelerate their work by amplifying their existing expertise" (Feb 23, 2026 meta-post).

What's distinctive about Simon's framing relative to other "AI-native development" writers:

1. **The agent definition is mechanical, not aspirational.** "An LLM agent runs tools in a loop to achieve a goal" (Sept 18, 2025). He explicitly likes that this is falsifiable and that "agents are not infinite loops — there is a stopping condition." The variant phrasing in the guide is *"Agents run tools in a loop to achieve a goal"*; the May 22, 2025 origin note credits Anthropic's Hannah Moran with "Agents are models using tools in a loop."
2. **He treats the patterns book as a living guide.** *Agentic Engineering Patterns* is "loosely inspired by the format popularized by Design Patterns: Elements of Reusable Object-Oriented Software back in 1994" — a chapter-shaped guide, but published as a "new shape of content I'm calling a *guide*" where "each chapter is effectively a blog post with a less prominent date that's designed to be updated over time, not frozen at the point of first publication" (Feb 23, 2026).
3. **He is bullish on tests-as-spec, bearish on unreviewed output.** Red/green TDD and "First run the tests" are the load-bearing patterns. Anti-patterns currently lists exactly one: *Inflicting unreviewed code on collaborators*.
4. **He is fascinated but skeptical of the StrongDM "software factory."** The Feb 7, 2026 post is admiring of the engineering but explicitly hedges: he calls the no-human-review stance worth scrutinizing precisely because of how surprising it is, asks aloud "how could that *possibly* be a sensible strategy when we all know how prone LLMs are to making inhuman mistakes?", and devotes a stand-alone update section to the $1,000/day-per-engineer cost.
5. **Cognitive debt is his core worry.** "When we lose track of how code written by our agents works we take on **cognitive debt**" (Interactive explanations chapter). Linear walkthroughs, interactive explanations, and agentic manual testing all exist specifically to keep the human in cognitive contact with the system.
6. **Humans-as-reviewers — but already eroding.** The May 6, 2026 post is the most honest moment in the corpus: "vibe coding and agentic engineering are getting closer than I'd like." Simon admits he no longer reviews every line of code he ships to production, and reaches for a *team* analogy ("if another team hands over something … I'm not going to go and read every line of code that they wrote") to make peace with it. He names this drift as a possible instance of "the normalization of deviance."

Where he is bullish: massive uplift in personal productivity for an engineer who knows what they're doing; the cost of trying speculative ideas has collapsed; small parallel agent fleets are now practical for one person; tests + sandboxes + good prompts are sufficient for most real work.

Where he is bearish / cautious: unreviewed code in production shared with collaborators (the named anti-pattern); $1k/day/engineer token spend as a default; satisfaction-scored LLM-judged compliance as a *sole* quality bar; the assumption that StrongDM's pattern generalizes outside its specific niche; treating "agent" as a synonym for "employee replacement" (his "least favorite definition").

## The software factory post — main argument

The post is titled "How StrongDM's AI team build serious software without even looking at the code" (Feb 7, 2026). Simon visited the team in October 2025 "as part of a small group of invited guests." He frames the StrongDM team as implementing what Dan Shapiro called the **Dark Factory** level of AI adoption — "where no human even looks at the code the coding agents are producing."

**The provocations.** Simon quotes StrongDM's own announcement post (factory.strongdm.ai, "Software Factories and the Agentic Moment") at length, including in "kōan or mantra form":

> Why am I doing this? (implied: the model should be doing this instead)

In "rule form":

> Code **must not be** written by humans
> Code **must not be** reviewed by humans

And in "practical form":

> If you haven't spent at least **$1,000 on tokens today** per human engineer, your software factory has room for improvement

Simon: *"I think the most interesting of these, without a doubt, is 'Code **must not be** reviewed by humans'. How could that possibly be a sensible strategy when we all know how prone LLMs are to making inhuman mistakes?"*

**The 2024 catalyst.** StrongDM dates the inflection differently from Simon. He quotes their post: *"The catalyst was a transition observed in late 2024: with the second revision of Claude 3.5 (October 2024), long-horizon agentic coding workflows began to compound correctness rather than error. By December of 2024, the model's long-horizon coding performance was unmistakable via Cursor's YOLO mode."* StrongDM's AI team launched in July 2025 under the rule "no hand-coded software."

**The most consequential question.** Simon names it explicitly: *"This feels like the most consequential question in software development right now: how can you prove that software you are producing works if both the implementation and the tests are being written for you by coding agents?"*

**Scenarios as holdout sets.** StrongDM borrowed "scenario" from Cem Kaner's 2003 *Scenario Testing*. Simon quotes them directly:

> We repurposed the word **scenario** to represent an end-to-end "user story", often stored outside the codebase (similar to a "holdout" set in model training), which could be intuitively understood and flexibly validated by an LLM.
>
> Because much of the software we grow itself has an agentic component, we transitioned from boolean definitions of success ("the test suite is green") to a probabilistic and empirical one. We use the term **satisfaction** to quantify this validation: of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?

Simon's gloss: *"That idea of treating scenarios as holdout sets—used to evaluate the software but not stored where the coding agents can see them—is fascinating. It imitates aggressive testing by an external QA team—an expensive but highly effective way of ensuring quality in traditional software."*

**Digital Twin Universe (DTU).** Simon quotes StrongDM:

> [The Digital Twin Universe is] behavioral clones of the third-party services our software depends on. We built twins of Okta, Jira, Slack, Google Docs, Google Drive, and Google Sheets, replicating their APIs, edge cases, and observable behaviors.
> With the DTU, we can validate at volumes and rates far exceeding production limits. We can test failure modes that would be dangerous or impossible against live services. We can run thousands of scenarios per hour without hitting rate limits, triggering abuse detection, or accumulating API costs.

The construction strategy, paraphrased by Simon: *"dump the full public API documentation of one of those services into their agent harness and have it build an imitation of that API, as a self-contained Go binary. They could then have it build a simplified UI over the top to help complete the simulation."* DTU creator Jay Taylor added on Hacker News (Simon quotes the comment): *"Use the top popular publicly available reference SDK client libraries as compatibility targets, with the goal always being 100% compatibility."*

A vivid line Simon highlights from StrongDM: *"Creating a high fidelity clone of a significant SaaS application was always possible, but never economically feasible. Generations of engineers may have wanted a full in-memory replica of their CRM to test against, but self-censored the proposal to build it."*

**Attractor and the spec-as-repo.** Simon: *"`github.com/strongdm/attractor` is **Attractor**, the non-interactive coding agent at the heart of their software factory. Except the repo itself contains no code at all—just three markdown files describing the spec for the software in meticulous detail, and a note in the README that you should feed those specs into your coding agent of choice!"* Separately, `github.com/strongdm/cxdb` is a *more traditional* release — 16,000 lines of Rust, 9,500 of Go, 6,700 of TypeScript — described as the team's "AI Context Store" for storing conversation histories and tool outputs in an immutable DAG.

**Other techniques referenced.** Simon points to **Gene Transfusion** (extract patterns from existing systems and reuse them elsewhere), **Semports** (porting code from one language to another), and **Pyramid Summaries** (multiple summary levels so an agent can enumerate the short ones quickly and zoom into detail when needed) from StrongDM's techniques page.

**Simon's verdict.** His commentary is hedged, with a dedicated "Wait, $1,000/day per engineer?" section he added in an update:

> If these patterns really do add $20,000/month per engineer to your budget they're far less interesting to me. At that point this becomes more of a business model exercise: can you create a profitable enough line of products that you can afford the enormous overhead of developing software in this way?
>
> Building sustainable software businesses also looks very different when any competitor can potentially clone your newest features with a few hours of coding agent work.
>
> I hope these patterns can be put into play with a much lower spend. I've personally found the $200/month Claude Max plan gives me plenty of space to experiment with different agent patterns, but I'm also not running a swarm of QA testers 24/7!
>
> I think there's a lot to learn from StrongDM even for teams and individuals who aren't going to burn thousands of dollars on token costs. I'm particularly invested in the question of what it takes to have agents prove that their code works without needing to review every line of code they produce.

He closes the post by calling it *"a glimpse of one potential future of software development, where software engineers move from building the code to building and then semi-monitoring the systems that build the code. The Dark Factory."*

## Pattern catalog

The Agentic Engineering Patterns guide (May 2026 snapshot) is structured as **6 sections containing 16 chapters**:

**Principles** — (1) What is agentic engineering? (2) Writing code is cheap now (3) Hoard things you know how to do (4) AI should help us produce better code (5) Anti-patterns: things to avoid.

**Working with coding agents** — (6) How coding agents work (7) Using Git with coding agents (8) Subagents.

**Testing and QA** — (9) Red/green TDD (10) First run the tests (11) Agentic manual testing.

**Understanding code** — (12) Linear walkthroughs (13) Interactive explanations.

**Annotated prompts** — (14) GIF optimization tool using WebAssembly and Gifsicle (15) Adding a new content type to my blog-to-newsletter tool.

**Appendix** — (16) Prompts I use.

### Detailed notes per chapter

**(1) What is agentic engineering?** Defines agentic engineering as *"the practice of developing software with the assistance of coding agents."* Coding agents are *"agents that can both write and execute code"* — examples: Claude Code, OpenAI Codex, Gemini CLI. The agent definition is rendered as *"Agents run tools in a loop to achieve a goal"* (chapter-canonical form). *"Code execution is the defining capability that makes agentic engineering possible. Without the ability to directly run the code, anything output by an LLM is of limited value."* On vibe coding: *"Vibe coding is more useful in its original definition - we need a term to describe unreviewed, prototype-quality LLM-generated code that distinguishes it from code that the author has brought up to a production ready standard."* On what's left for humans: *"Writing code has never been the sole activity of a software engineer. The craft has always been figuring out what code to write."*

**(2) Writing code is cheap now.** *"The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that writing code is cheap now."* The "good code" subsection lists nine quality attributes (works; we know it works; solves the right problem; handles errors; simple and minimal; protected by tests; documented; affords future changes; the relevant "ilities" — accessibility, testability, reliability, security, maintainability, observability, scalability, usability). Core heuristic: *"any time our instinct says 'don't build that, it's not worth the time' fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens."*

**(3) Hoard things you know how to do.** *"A big part of the skill in building software is understanding what's possible and what isn't, and having at least a rough idea of how those things can be accomplished. … The best way to be confident in answers to these questions is to have seen them illustrated by running code."* Concrete artifacts in Simon's own hoard: his blog, his TIL blog, "over a thousand GitHub repos," `tools.simonwillison.net` for HTML tools, `simonw/research` for larger agent-built experiments. The reusable prompting pattern is *"to tell an agent to build something new by combining two or more existing working examples"* — exemplified by his PDF-OCR tool combining Tesseract.js and PDF.js snippets. *"The key idea here is that coding agents mean we only ever need to figure out a useful trick once. If that trick is then documented somewhere with a working code example our agents can consult that example and use it to solve any similar shaped project in the future."*

**(4) AI should help us produce better code.** (NEW — missed in the original report.) Sub-headings indicate the argument: *Avoiding taking on technical debt*, *Coding agents can handle these for us*, *AI tools let us consider more options*, *Embrace the compound engineering loop*. The chapter's thesis is that lower coding cost should be spent on quality (tests, refactoring, alternative designs) rather than absorbed as more code — and Simon explicitly nods to Every.to's "compound engineering" loop here (a deliberate cross-reference; he treats their framing as compatible with his own).

**(5) Anti-patterns: things to avoid.** Currently lists exactly one anti-pattern, *Inflicting unreviewed code on collaborators*. Verbatim: *"Don't file pull requests with code you haven't reviewed yourself."* *"If you open a PR with hundreds (or thousands) of lines of code that an agent produced for you, and you haven't done the work to ensure that code is functional yourself, you are delegating the actual work to other people. They could have prompted an agent themselves. What value are you even providing?"* The chapter then lists characteristics of a good agentic-engineering PR (code you're confident works; small enough to be reviewed; includes context for the change; *and the PR description itself reviewed*: *"Agents write convincing looking pull request descriptions. You need to review these too!"*). The chapter explicitly recommends *evidence of human work*: *"Notes on how you manually tested it, comments on specific implementation choices or even screenshots and video of the feature working go a long way to demonstrating that a reviewer's time will not be wasted."*

**(6) How coding agents work.** A mechanical walkthrough: LLMs → tokens → chat-templated prompts → token caching → tool calls → system prompts → reasoning → "LLM + system prompt + tools in a loop." Key sentences: *"A tool is a function that the agent harness makes available to the LLM."* *"The model harness software then extracts that function call request from the response - probably with a regular expression - and executes the tool."* *"Believe it or not, that's most of what it takes to build a coding agent! … A simple tool loop can be achieved with a few dozen lines of code on top of an existing LLM API. A good tool loop is a great deal more work than that, but the fundamental mechanics are surprisingly straightforward."*

**(7) Using Git with coding agents.** (NEW — missed in the original report.) Sub-headings: Git essentials; Core concepts and prompts; Rewriting history. The chapter is a practical guide on letting coding agents drive Git operations including history rewriting (rebase, squash, fixup) — the implication being that coding agents are now competent enough to be trusted with destructive history operations on local branches if you've sandboxed them appropriately.

**(8) Subagents.** *"LLMs are restricted by their context limit — how many tokens they can fit in their working memory at any given time. These values have not increased much over the past two years even as the LLMs themselves have seen dramatic improvements in their abilities — they generally top out at around 1,000,000, and benchmarks frequently report better quality results below 200,000."* The chapter walks through three flavors: **Explore subagent** (Claude Code's standard reconnaissance dispatch — Simon shows an actual transcript of a subagent prompt); **Parallel subagents** (fan-out for independent edits, sometimes on cheaper models like Claude Haiku); **Specialist subagents** (code reviewer, test runner, debugger — each with a custom system prompt and/or custom tools). Critical caveat: *"While it can be tempting to go overboard breaking up tasks across dozens of different specialist subagents, it's important to remember that the main value of subagents is in preserving that valuable root context and managing token-heavy operations. Your root coding agent is perfectly capable of debugging or reviewing its own output provided it has the tokens to spare."*

**(9) Red/green TDD.** Verbatim: *"Use red/green TDD" is a pleasingly succinct way to get better results out of a coding agent."* *"A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both. Test-first development helps protect against both of these common mistakes."* *"It's important to confirm that the tests fail before implementing the code to make them pass. If you skip that step you risk building a test that passes already, hence failing to exercise and confirm your new implementation."* *"Every good model understands 'red/green TDD' as a shorthand for the much longer 'use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass'."* Example prompt: *"Build a Python function to extract headers from a markdown string. Use red/green TDD."*

**(10) First run the tests.** *"Automated tests are no longer optional when working with coding agents."* *"The old excuses for not writing them - that they're time consuming and expensive to constantly rewrite while a codebase is rapidly evolving - no longer hold when an agent can knock them into shape in just a few minutes."* The opening prompt against any existing project is literally "First run the tests" (or for Python projects: *"Run 'uv run pytest'"*). Three named purposes: (a) forces the agent to discover the test harness so it can run tests later, (b) gives a rough complexity estimate from the test count, (c) puts the agent in a testing mindset so it will extend the tests. Verbatim: *"'First run the tests' provides a four word prompt that encompasses a substantial amount of software engineering discipline that's already baked into the models."*

**(11) Agentic manual testing.** *"Never assume that code generated by an LLM works until that code has been executed."* *"Just because code passes tests doesn't mean it works as intended. … Automated tests are no replacement for manual testing. I like to see a feature working with my own eye before I land it in a release. I've found that getting agents to manually test code is valuable as well, frequently revealing issues that weren't spotted by the automated tests."* Concrete substrate techniques (with exact prompts): `python -c "..."` for Python libraries; *"Write code in `/tmp` to try edge cases of that function and then compile and run it"* for other languages; *"Run a dev server and explore that new JSON API using `curl`"* for HTTP APIs; *"test that with Playwright"* for web UIs (also Vercel's `agent-browser` and Simon's own **Rodney** Chrome-DevTools-Protocol tool). On Showboat: *"I built Showboat to facilitate building documents that capture the agentic manual testing flow."* The three Showboat commands are `note` (appends markdown), `exec` (runs a command and records both the command and the output) and `image` (adds an image). *"The `exec` command is the most important of these, because it captures a command along with the resulting output. This shows you what the agent did and what the result was, and is designed to discourage the agent from cheating and writing what it hoped had happened into the document."*

**(12) Linear walkthroughs.** *"Sometimes it's useful to have a coding agent give you a structured walkthrough of a codebase. Maybe it's existing code you need to get up to speed on, maybe it's your own code that you've forgotten the details of, or maybe you vibe coded the whole thing and need to understand how it actually works."* The worked example is a Swift slide-presentation app Simon vibe-coded then re-walked. Prompt verbatim: *"Read the source and then plan a linear walkthrough of the code that explains how it all works in detail. Then run 'uvx showboat --help' to learn showboat - use showboat to create a walkthrough.md file in the repo and build the walkthrough in there, using showboat note for commentary and showboat exec plus sed or grep or cat or whatever you need to include snippets of code you are talking about."* *"If you are concerned that LLMs might reduce the speed at which you learn new skills I strongly recommend adopting patterns like this one."*

**(13) Interactive explanations.** Opens with the core Simon-ism: *"When we lose track of how code written by our agents works we take on **cognitive debt**."* *"For a lot of things this doesn't matter: if the code fetches some data from a database and outputs it as JSON the implementation details are likely simple enough that we don't need to care. … Often though the details really do matter. If the core of our application becomes a black box that we don't fully understand we can no longer confidently reason about it, which makes planning new features harder and eventually slows our progress in the same way that accumulated technical debt does."* *"How do we pay down cognitive debt? By improving our understanding of how the code works."* The exemplar is an animated word-cloud explainer driven by Claude Opus 4.6: *"This was using Claude Opus 4.6, which turns out to have quite good taste when it comes to building explanatory animations."*

**(14) GIF optimization tool using WebAssembly and Gifsicle.** (NEW — annotated prompt walkthrough chapter the original report missed.) The annotated build of Simon's GIF-compression web UI on top of a WebAssembly Gifsicle build, with the original prompt and follow-up prompts preserved.

**(15) Adding a new content type to my blog-to-newsletter tool.** (NEW — annotated prompt walkthrough chapter missed in the original report.) End-to-end story of extending an existing tool with a new content type via coding agent.

**(16) Prompts I use.** Reusable prompts: an *Artifacts* system prompt forcing vanilla HTML/CSS/JS (no React) so artifacts can be copied out and statically hosted; a *Proofreader* prompt that catches typos/grammar/repetition/logical errors/weak arguments/empty links; an *Alt text* prompt (he runs this with Claude Opus, which "has extremely good taste in alt text"); a *Podcast highlights* prompt that extracts quotable lines from a transcript. Simon's hard line: *"I don't let LLMs write text for my blog. … anything that expresses opinions or uses 'I' pronouns needs to have been written by me."*

### Additional patterns from adjacent posts

**Designing agentic loops** (Sept 30, 2025). *"A critical new skill to develop is designing agentic loops."* *"Coding agents are brute force tools for finding solutions to coding problems. If you can reduce your problem to a clear goal and a set of tools that can iterate towards that goal, a coding agent can often brute force its way to an effective solution."* Quotes Solomon Hykes on the danger: *"An AI agent is an LLM wrecking its environment in a loop."* Three risks of YOLO mode: (a) bad shell commands deleting or mangling things you care about, (b) exfiltration of files or env-var secrets, (c) the agent's machine being used as a proxy for attacks on third parties. Simon's preferred mitigation is option 2 — *use someone else's computer* — i.e. GitHub Codespaces. He also references Anthropic's "Safe YOLO mode" docs (use `--dangerously-skip-permissions` in a container with no internet, optionally with a firewall to a list of trusted hosts). On tool design: *"Rather than leaning on MCP, I like to create an AGENTS.md (or equivalent) file with details of packages I think they may need to use."* On credentials: *"Try to provide credentials to test or staging environments where any damage can be well contained. If a credential can spend money, set a tight budget limit."* The four exemplars he names for "when to design an agentic loop": **debugging**, **performance optimization** (have the agent benchmark a SQL query with and without an index), **upgrading dependencies**, **optimizing container sizes**. *"A common theme in all of these is automated tests."*

**Parallel coding agent lifestyle** (Oct 5, 2025). Four concrete pattern categories Simon names: **Research for proof of concepts** (e.g. "can Yjs + pycrdt actually be wired together?"); **How does that work again?** (use a reasoning model to grep through a codebase and explain a subsystem — "These LLM-generated explanations are worth stashing away somewhere, because they can make excellent context to paste into further prompts in the future"); **Small maintenance tasks** (deprecation warnings, minor irritations — "the best way to develop that instinct is to try things"); **Carefully specified and directed actual work** ("Code that started from your own specification is a lot less effort to review"). His own setup: Claude Code on Sonnet 4.5; Codex CLI on GPT-5-Codex; Codex Cloud for async tasks (often launched from his phone); multiple terminal windows in YOLO mode "for tasks where I'm confident malicious instructions can't sneak into the context." He hasn't adopted git worktrees: *"if I want to run two agents in isolation against the same repo I do a fresh checkout, often into `/tmp`."* He endorses Josh Bleecher Snyder's *"Send out a scout. Hand the AI agent a task just to find out where the sticky bits are, so you don't have to make those mistakes."*

**Tools-in-a-loop framing.** The May 22, 2025 origin note records the moment Anthropic's Hannah Moran said *"Agents are models using tools in a loop"* during the "Prompting for Agents" workshop. The Sept 18, 2025 post canonicalizes Simon's preferred form: *"An LLM agent runs tools in a loop to achieve a goal."* He rejects the human-replacement definition: *"That's because there's one key feature that remains unique to human staff: accountability. A human can take responsibility for their actions and learn from their mistakes. Putting an AI agent on a performance improvement plan makes no sense at all!"*

**Ultrathink** (Apr 19, 2025). Reverse-engineering Claude Code's CLI revealed exact thinking-budget tiers: phrases containing "think harder", "think intensely", "think longer", "think really hard", "think super hard", "think very hard" or "ultrathink" → 31,999 tokens; "think about it", "think a lot", "think deeply", "think hard", "think more", "megathink" → 10,000 tokens; "think" alone → 4,000 tokens. The takeaway: prompt vocabulary is load-bearing — small word choices map to large compute budgets.

## Lenny interview: "An AI state of the union" (✅ FULL transcript drained 2026-05-13)

**Source:** Lenny Rachitsky podcast with Simon Willison, *"An AI state of the union"*, YouTube `https://youtu.be/wc8FBhQtdsA`. Manual transcript captured in `research/manual/lenny-An AI state of the union.txt` (2,155 lines, full ~90-minute episode). The first half of this section (cold-open + November inflection + productivity/personal-leverage + vibe-coding articulation + StrongDM spoken framing + ideation + engineer-tier + initial security adjacencies) was drained from the first ~30 minutes on 2026-05-13; the second half ("Productivity paradox", "Artisanal code and proof of usage" through "Closing notes") was drained from the remaining ~60 minutes on the same date — see follow-up Drain note at top of this report.

This is a different *kind* of primary source from Simon's blog posts: it captures him speaking in real time, with looser framing than his written work. Several claims that previously sat in the corpus as inferred, paraphrased, or "Simon mentioned in interview" are now primary-anchored verbatim from this transcript. Where the transcript adds a load-bearing new claim not present in his written corpus, it is flagged **NEW**.

### Cold-open headline claims (Lenny's edit, but in Simon's own voice)

The episode opens with a montage of Simon clips before the interview proper:

> *"A lot of people woke up in January and February and started realizing, Oh, wow, I can churn out 10,000 lines of code in a day."*

> *"The open question for me is, how many other knowledge work fields are actually prone to these agent loops?"* — **NEW** framing: Simon is now using "agent loops" (his canonical "tools in a loop" formulation) as the load-bearing primitive when reasoning about *generalization beyond software engineering* — i.e. the unit of analysis for "will AI eat field X?" is whether the work in X is *amenable to being reduced to an agent loop*. This is a sharper test than the usual "is this knowledge work?" framing.

> *"Probably 95% of the code that I produce, I didn't type it myself. I write so much of my code on my phone, it's wild. I can get good work done walking the dog along the beach."*

> *"My New Year's resolution every previous year, I've always told myself, this year I'm going to focus more, I'm going to take on less things. This year, my ambition was take on more stuff and be more ambitious."* — **NEW** personal data point: the productivity boost has *inverted* Simon's own multi-year focus discipline. Useful corroboration of the corpus thesis that the cost of trying speculative ideas has collapsed.

> *"Using coding agents well is taking every inch of my 25 years of experience as a software engineer. I can fire up four agents in parallel and have them work on four different problems. By 11am I am wiped out."*

> *"You have this prediction that we're going to have a massive disaster at some point. You call it the Challenger disaster of AI."* (Lenny prompt)
>
> *"Lots of people knew that those little O rings were unreliable, but every single time you get away with launching a space shuttle without the O rings failing, you institutionally feel more confident in what you're doing. We've been using these systems in increasingly unsafe ways. This is going to catch up with us. My prediction is that we're going to see a challenging disaster."* (Simon) — **NEW** named prediction. This is the **Challenger disaster of AI** thesis, explicitly framed as an analogy to NASA's pre-Challenger normalization-of-deviance dynamic (which Simon already names in his May 6, 2026 blog post — see corpus quote #16). The cold-open captures the *thesis statement* but the supporting elaboration likely sits past the 30-minute window. Cross-reference: the same "normalization of deviance" mechanism Simon names personally in May 6, 2026 ("every time a model turns out to have written the right code without me monitoring it closely there's a risk that I'll trust it at the wrong moment in the future and get burned") is here generalized to a *civilizational-scale* prediction.

### The November 2025 inflection point

Simon dates the qualitative jump:

> *"In November, we had what I call the inflection point where GPT 5.1 and Claude Opus 4.5 came along, and they were both just they were incrementally better than the previous models, but in a way that crossed a threshold where, previously, if you had these coding agents, you could get them to write you some code, and most of the time it would mostly work, but you had to pay very close attention to it, and suddenly we went from that to almost all of the time, it does what you told it to do, which makes all of the difference in the world."*

> *"A lot of people woke up in January and February and started realizing, Oh, wow, this technology, which I've been kind of paying attention to, suddenly it's got really, really good."*

He locates the broader 2025 arc as well:

> *"2025 was the year that, especially anthropic and opening, AI realized that code is the application … both anthropic and OpenAI spent the whole of 2025 focusing all of their training efforts on coding."*

> *"Code is easier than almost every other problem that you pose these agents, because code is obviously right or wrong … It came for us first."*

### Productivity and personal-leverage claims (verbatim)

The "4 agents → 11 AM exhaustion" passage in full (reversal-of-reversal — see Drain note):

> *"I'm finding that using coding agents well is taking every inch of my 25 years of experience as a software engineer, and it is mentally exhausting … I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day, like I have because there is a limit on human cognition in how much, even if you're not reviewing everything you're doing, just how much you can hold in your head at one time. And it's very easy to pop that stack at the moment."*

> *"There's an element of sort of gambling and addiction to how we're using some of these tools."* — **NEW** candor.

> *"My 25 years of existing, like pre AI experience, which I can now amplify, because I can talk to the agents at a very high level. I can use sophisticated engineering, like language that I've mastered over the years, which they appear to know as well, and we can collaborate incredibly effectively."*

> *"I've got 25 years of experience in how long it takes to build something, and that's all completely gone … because I can look at a problem and say, Okay, well, this is going to take two weeks. It's not worth it. And now it's like, yeah, but maybe it's going to take 20 minutes."* — strong corroboration of the corpus's "fire off a prompt anyway" heuristic, framed here as a *cost-estimation skill that has been invalidated*.

> *"I constantly throw tasks at AI that I don't think it'll be able to do, because every now and then it does it, and when it doesn't do it, you learn … that's actually cutting edge AI research. You can be the first person in the world to spot that AI can now do X."* — **NEW** framing: individual practitioners testing capability frontiers is itself a form of AI research.

### Vibe coding vs. agentic engineering — Simon's spoken articulation

The transcript contains Simon's own clearest spoken version of the distinction the corpus already records from his Feb 23, 2026 meta-post:

> *"If you're vibe coding something for yourself, where the only person who gets hurt, if it has bugs, is you. Yeah, go wild. That's completely fine. The moment you're vibe coding code for other people to use where your bugs might actually harm somebody else, that's when you need to take a step back."*

> *"The big debate, the ongoing debate, has been, what do we call it? When a professional software engineer uses these tools to write real code that's production ready, that they've reviewed and they've checked all of the details … a lot of people call that vibe coding as well. I think that devalues vibe coding as a term."*

> *"That's why I've gone with agentic engineering, because I think the thing to emphasize is these coding agents."*

> *"I'm kind of writing a book about it now that I'm publishing a chapter at a time on my blog … the best form of writing, because I don't have an editor or any pressure from a publisher."* — confirms the *Agentic Engineering Patterns* guide is, in Simon's own framing, a *book in progress*.

### Software factory / StrongDM — Simon's spoken framing

The transcript adds spoken-register detail not in the Feb 7, 2026 written post:

> *"There's a policy of, nobody writes any code … you cannot type code into a computer. Exactly. And honestly, like I thought six months ago, I thought that was crazy. And today, probably 95% of the code that I produce I didn't type it myself."*

> *"The next rule, though, is nobody reads the code. And this is the thing which strong DM started doing back in I think it was August last year."*

> *"They had a swarm of agent testers who were actually simulating end users … they were spending $10,000 a day on tokens, I think, simulating these end users."* — **NEW** number: StrongDM's *daily* spend on simulated-tester tokens specifically. Note this is **larger** than the $1,000-per-engineer-per-day figure already in the corpus; whether it overlaps or is additional is not clear from the transcript.

> *"That's not the kind of thing that you should be vibe coding at all based on most people's understanding of how the world works, but … they're a legitimate security company who've been doing this stuff without AI for years. So it's not like they didn't understand the risks."*

### Ideation and product-design claims — **NEW**

Simon's strongest spoken claim on where humans add value when coding is no longer the bottleneck:

> *"Now the bottlenecks are everywhere else, right? Like, how do we redesign our processes now that the bit that used to take the longest … now maybe that takes three hours?"*

> *"Anyone who's done any product work knows that your initial ideas are always wrong. What matters is proving them right. It's testing them. We can test things so much faster now."*

> *"Any sort of feature that I want design, I'll often prototype three different ways it could work, because that takes very little time."* — **NEW** workflow: Simon now prototypes *3 alternatives by default* for any design decision.

> *"Anyone who's doing sort of product design isn't vibe coding little prototypes is missing out on the latest … most powerful sort of boost that we get in that step."*

> *"I don't think you're going to get as good results from chat GPT pretending to click around on your prototype than you would from an actual human being."* — **NEW** explicit rejection of LLM-as-user-tester for usability validation. This is a stronger stance than anything in the written corpus.

> On AI as brainstorming partner: *"They've been strong enough to do really good brainstorming … the AI is so good at that first two thirds of the ideas … you get them to spit out all of the obvious stuff … and then if you ask them for 20 more … you're beginning to get things which are not good ideas, but they point you in interesting directions."*

> **NEW** prompting trick: *"You can tell AI to combine weird fields. You can say, Okay, I want ideas for marketing my new SaaS platform, inspired by marine biology, and you see what happens, and most of it will be complete junk, but there might be a spark that gets you to the good idea."*

### Engineer-tier claims — **NEW** (ThoughtWorks framing)

Simon reports a ThoughtWorks engineering-VP off-site finding he endorses:

> *"This stuff is really good for experienced engineers, like it amplifies their skills … It's really good for new engineers because it solves so many of those onboarding problems, like, if you talk to Cloudflare and Shopify, both said they were hiring 1000 interns over the course of 2025 because the intern onboarding costs … went from a month before your intern can do anything useful … to a week."*

> *"The problem is the people in the middle, like, if you're mid career, if you haven't made it to sort of super senior engineer yet, but you're not sort of new either. That's the group which ThoughtWorks resolved were probably in the most trouble right now."*

This is a load-bearing claim for any factory architecture's hiring/staffing model: the corpus already has "AI as amplifier of existing expertise"; this adds the **explicit U-curve**: experienced wins, novice wins, mid-career squeezed.

### Security adjacencies — early/partial-drain material

> *"Both open AI and anthropic have specialist security models that they will not release to the general public because they can be used to break into websites … invite only, like registered security researchers can apply for access."* — **NEW** datum.

> *"Anthropic had discovered 100 like potential vulnerabilities in Firefox and responsibly reported them to Mozilla, who then fixed them."* — **NEW** datum (recent Firefox release credit).

> *"It's incredibly frustrating for maintainers, because there are these people who don't know what they're doing, who are asking chat GPT to find a security hole and then reporting it to the maintainer and the report looks good … it's a total waste of time."* — **NEW** stance: AI-amplified vulnerability-report spam is a real ecosystem cost.

### End-of-2025 prediction and economic anxiety **[2026-05-13 full-transcript drain]**

Lenny asks when AI will be writing 100% (Simon refactors to **95%**) of the code of 50% of engineers. Transcript lines 864–893:

> *"I expect by the end of this year, it will not be uncommon to have an engineer say that almost all of their code is written by AI."*

Hedge on cultural variation: *"I spend way too much time on Hacker News, and something I've noticed about Hacker News is a conversation that starts at midnight Pacific time and goes until 8am, very different tone, because it's the Europeans … you'll get the Europeans and a lot more AI skeptic than the Americans are generally."*

Anchoring point: *"It used to be that you could say, I don't use this stuff because the code is bad. And that was a justifiable position. That's not justifiable anymore. The code is now good."*

Macroeconomic worry (lines 910–915) — **the only macro-anxiety on the record**:

> *"It's honestly, I'm not an AI doomer in the slightest. The economics of it do make me nervous, like, are we really going to wipe out like a tenth of white collar knowledge work jobs in the next few years? I really hope not because I don't know how the economy adapts to that."*

Followed (lines 916–950) by an explicit cross-reference to Lenny's own job-market report: at tech companies, open engineering and PM roles are at their highest count *"in three and a half-ish years"* (excepting COVID-peak). Simon agrees the macroeconomic signal is lagging because *"all of the job ads are written by AI, the resumes are AI"* — recruitment is *"never been this hard"* to filter.

### Artisanal code, "proof of usage", and low-background-steel analogy **[2026-05-13 full-transcript drain]**

Transcript lines 800–855. Simon's strongest spoken articulation of the "looking-the-part hazard" already in the corpus (Notable Quote #17 from the May-6-2026 post). New ingredients:

- The **"alpha" suffix as a cheat code**: *"The way I've been dealing with that is I always put alpha on it. If you see my software and it says it's an alpha, that probably means I haven't actually used it yet for most of my projects, which is a bit of a cheat code, you know, alpha-list."*
- The **proof-of-usage framing** (Lenny coins it; Simon affirms): Lenny: *"It's almost like we need a proof of work for this versus the blockchain."* Simon: *"A proof of usage. Yes, exactly."*
- The **low-background-steel analogy**, applied to data-labeling firms buying pre-2022 GitHub repos:

> *(Lenny)*: *"Data labeling companies are buying old GitHub repos of handwritten code … paying a lot of money for like, artisanal human-written code."*
>
> *(Simon)*: *"That's fascinating. That's the pre-World War Two, the metal that you can dig up from old shipwrecks, which is before the first nuclear explosions and so it's not got the radiation baked into the metal. It's that whole thing."*

This is the corpus's first direct primary anchor for the **"AI-uncontaminated training data is becoming a commodity"** thesis (parallel to low-background steel / pre-1945 lead used in radiation-sensitive instruments).

### Tool stack and workflow details **[2026-05-13 full-transcript drain]**

Transcript lines 1028–1146. Simon walks Lenny through his stack — the most complete spoken inventory in the entire Willison corpus:

- **Claude Code (local)** — the desktop terminal version.
- **Claude Code for web** — Anthropic's hosted version, accessed primarily *via the "code" tab in the Anthropic iPhone app*. **This is the version Simon uses most**, because (a) the phone is his primary input device, (b) running on Anthropic's servers means *"if it accidentally deletes things, it's their computer, not my computer"*, (c) YOLO-mode risk is contained to the hosted environment.
- **YOLO mode** — Claude's `--dangerously-skip-permissions`, OpenAI Codex's `YOLO` flag (Simon confirms OpenAI literally named it "YOLO"). *"The moment you take the safeties off, now I can run four of them and go and have a cup of tea and come back and they've achieved something useful for me."* — explicit corroboration of the parallel-agent + sandbox pattern from the Sept-30-2025 blog post.
- **GPT 5.4** (released ~3 weeks before recording, so ~April 2026): *"I think it's on par with Claude Opus 4.6 and possibly even better. … It's also cheaper. So I've been leaning on GPT 5.4 a lot more this month and OpenAI Codex."* Simon explicitly states OpenAI Codex and Claude Code are *"almost indistinguishable from each other now."*
- **Model loyalty is taste-driven, not benchmark-driven**: *"I keep on coming back to Claude code mainly because it fits my taste. … I've got a very specific taste in how I like code to work, which coincidentally happens to map to how Claude code likes to work."* And: *"It's vibes all the way down."*
- **Memory features — Simon turns them off**: *"They all have these features where they will remember things about you, and I hate those features and I turn them off wherever I can, mainly because as an AI researcher, I need to see what everyone else sees when I'm prompting."* He notes this is the stickiness mechanism the labs are betting on.
- **The Anthropic memory-export prompt-hack** (lines 1126–1140): when OpenAI's military-contract news created a defection moment, Anthropic published a Claude onboarding page with a copy-paste prompt for ChatGPT — *"hey, ChatGPT, tell me everything that you've remembered about me"* — and pasted that output into Claude. *"That was hilarious. Like a whole export, like move from one to the other just by prompting it."*
- **Search/research is now LLM-mediated, not Google-mediated**: *"I hardly use Google search directly at all. I'm always using it via, I'm doing searches via Claude or via ChatGPT, or sometimes via the Gemini app."* He always double-checks for hallucinated details before publishing.
- **Gemini for image generation** (NanoBanana): *"I only use that for fun, like I don't publish images I generate, I use them for pranks."*

GPT 5.4 grid (lines 1202–1212) — Simon describes generating a 3×5 grid of pelicans-on-bicycles across **GPT-5.4 / GPT-5.4-Mini / GPT-5.4-Nano** at five thinking levels (low/medium/high/etc.); *"GPT 5.4 running at X-high did draw the best pelican."*

### Hoarding methodology — concrete repos and reuse pattern **[2026-05-13 full-transcript drain]**

Transcript lines 1300–1417. Simon names his two canonical hoarding repos and the exact reuse pattern:

- **`SimonW/tools`** — *"little HTML and JavaScript tools that I've built or that I've got Claude to build for me. There's like 193 of those now."* All client-side, self-contained, single-file.
- **`SimonW/research`** — *"AI-driven research projects … 75 projects in it [public], I've got a private research one with another 50."* Each output is a markdown file describing what the agent did, what code was written, what the result was. *"These research projects are a really quick way for me to try porting something from JavaScript to Python or … run little benchmarks and see how performant a new thing is."*
- Critical caveat — these are *not* deep-research-report style documents: *"This isn't research in this traditional sense of go and search the web and do me a deep research report. These are all coding agent research tasks where it's actually written code and run it. … if I published a GitHub repository full of unverified, like, deep research reports, that's very little value to anyone. But the moment the coding agent has written the code, run the code, plotted a graph on how it worked or whatever, that's what turns it into not just sort of like, LLM vomit. It becomes something that's at least slightly actionable."*
- **The reuse pattern, verbatim**: *"I'll often just tell Claude code, paste in a URL to this thing, this thing here, here's another thing, go and read the source code and then solve this new problem. … check out SimonW/research from GitHub and look at the ones in there that deal with WebAssembly and Rust, and then use that to feed into solving this new task in WebAssembly and Rust."*
- The **PDF-OCR worked example** (lines 1394–1403, already in the corpus from the *Hoard things you know how to do* chapter) is here repeated verbatim, anchoring the chapter content to spoken-register Simon: an existing PDF-rendering script (Mozilla's pdf.js) plus an existing Tesseract OCR script were combined by Claude Opus III into a new "OCR each page of this PDF" tool.
- Storage discipline: *"GitHub is free for private repositories somehow. So I'm doing all of this stuff in GitHub. When you put something on GitHub, they back it up to three continents. … Occasionally they'll go and stick it in a vault in the Arctic as well."*

### Red/green TDD and the "first run the tests" pattern — spoken articulation **[2026-05-13 full-transcript drain]**

Transcript lines 1418–1548. The chapter content already in the corpus (chapters 9–10 of *Agentic Engineering Patterns*) gets a spoken-register restatement plus one new framing point:

- The **tests-paid-for-by-the-agent-not-you** insight (lines 1514–1529):

> *"It's also an interesting example of how my idea of quality code has changed because the challenge with tests is that you can test absolutely everything and you might end up with thousands of lines of tests for 100 lines of code, and sometimes that's good, but usually that's bad. That's a bad design pattern. … It turns out, I don't care anymore, because updating 1000 lines of tests is now the job of the coding agent. So I'm much more tolerant of sort of very lengthy, verbose test suite. A lot of my small libraries now have over 100 tests."*

This is a **NEW** primary-source claim: Simon's design-aesthetic threshold for test-suite size has moved up. The cost-of-maintenance argument against over-testing is gone now that maintenance is agentic.

- Confirmation of the **"red/green TDD" five-character magic phrase** as load-bearing prompt vocabulary: *"If you use the term red slash green TDD … the agents know what that means. So now we've reduced that sort of lengthy paragraph about how to run tests to red slash green TDD, enter, you're done."*

### Project templates — a chapter-in-progress preview **[2026-05-13 full-transcript drain]**

Transcript lines 1548–1584. Simon previews a not-yet-written chapter of the patterns book:

> *"One pattern I plan to write a chapter about soon is to start new projects with a really good template, a sort of starting template. And the reason for this is, it turns out, coding agents are phenomenally good at sticking to existing patterns in the code. Like if you give them a code base that already has just a single test in it, they will write more tests. They will notice that if you've got a preferred style of indentation or formatting, anything like that, just a single file is enough example for them to pick up on that."*

The Claude.md trade-off: *"Some people will tell you you should have a Claude.md with like paragraphs of text describing how you like to work. I don't tend to do that, because, instead, I start with a very thin skeleton that just gives it enough hints on how I like to work that it picks it up and rolls with it."*

He maintains three templates: *"one for a Python library, and one for a dataset plugin, and one for a little command line tool."*

**Flag for orchestrator**: when the "Project templates" chapter ships at simonwillison.net/guides/agentic-engineering-patterns/templates/ (or similar), it should be added to the source list and the Pattern Catalog updated from 16→17 chapters.

### Security and the lethal trifecta — full elaboration **[2026-05-13 full-transcript drain]**

Transcript lines 1586–1850. This is the section the partial drain explicitly flagged as missing. It now anchors the corpus's lethal-trifecta material to a primary spoken source.

**Why Simon regrets the term "prompt injection"** (lines 1591–1661):

> *"I called it prompt injection because I thought it was the same thing as this attack called SQL injection, which is a security problem with databases where you glue user input into your SQL queries in a way that breaks them and deletes all of your data. The problem is SQL injection is solved. We know how to fix this problem … those solutions don't work for prompt injection. So the name itself is misleading. … And then the other problem with coining terms is just because you were the first to define a term doesn't mean you actually get to define what it means in people's heads. … A lot of people, when you say prompt injection, they say, 'Oh, I know what that means. It's injecting prompts.' … That's jailbreaking. That's a different kind of thing."*

**Why "lethal trifecta" was deliberately chosen as unguessable** (lines 1662–1670):

> *"The lethal trifecta was my second attempt at this. And you'll notice that the lethal trifecta, you cannot guess what it is. If I say to you, there's a thing called the lethal trifecta, you can't go, it's obviously one, two, it's three things. But what are those things? And that means I get to control what it means because you have to go and look it up."*

This is the corpus's first **direct primary source** on Simon's *naming methodology* for security concepts. Key takeaway: name an unsolved problem with a *guessable* name and you lose definitional control; name it with an *unguessable* name and readers must come to your definition.

**The lethal trifecta verbatim** (lines 1672–1690):

> *"You have a lethal trifecta any time your agent has three things. It's got access to private information — there's information that you've exposed to it like your private inbox that is private in some way. It's exposed to malicious instructions — so there's a way somebody attacking you can get their text into your system, like sending you an email. And the third leg is exfiltration, or some mechanism the agent can send data back to that attacker, like forwarding an email. So if you've got a system where you've got private emails, anyone can email you instructions, and it can email them back, that's the classic lethal trifecta. That's a huge security problem. The only way to fix it is to cut off one of those three legs. So normally the leg that's easiest to cut off is the exfiltration one."*

**The 97%-is-a-failing-grade argument** (lines 1696–1716):

> *"The problem is you can get to like 97% effectiveness on those filters. I think that's a failing grade. That means that three out of 100 of these attacks will steal all of your information. Because fundamentally, the way we prompt these things is using text in any human language, right? You can say, you could filter out 'ignore previous instructions' in English. What if somebody says it in Spanish? There is no filter. It's like the classic sort of allow list versus deny list thing. You cannot deny every one of these attacks because I can always invent a new sequence of characters that might trick the model in some way."*

The corollary — the **blast-radius doctrine**: *"Consider that anyone who can talk to your agent can make it do any of the things it's allowed to do, and then you have to think okay, well, let's make sure that the blast radius on that is limited."*

Simon connects this to his own use of Claude Code for web (lines 1717–1729): *"This is why I use Claude code for web so much, because I'm often having it go and read random web pages, and maybe those have nasty attacks in them. All it can really do, if it's running on Anthropic servers is waste this, it could like mine bitcoin on their servers or something, or maybe leak some of my private data somewhere else, but I don't put my private data into that environment."* Then the empathy note: *"This is not helpful for the vast majority of people who fall for phishing emails, which is most of us. This is like an equivalent of phishing, except the agent is the thing being phished. And that's terrifying."*

**Solution endorsement: Google DeepMind's CaMeL paper** (lines 1813–1841):

> *"There was a paper that Google DeepMind put out a couple of years ago, the Camel paper, which proposed a way of building one of these agents that didn't assume that you can fix prompt injection. And their solution was that you sort of split the agent into the privileged agent that you talk to and that can do interesting things, and then you have this quarantined agent that gets exposed to the malicious instructions, but can't actually do anything useful. And then the way it works is the privileged agent effectively writes code for, you should do this, then you should do that, then you should do this, and that code is evaluated in a way that tracks what's tainted. So it makes sure that once a potentially dangerous instruction has gotten in, the next action, the human has to approve. Because human in the loop helps a little bit, but if you ask the human to click OK five times a minute, they'll just click OK all the time. If you can filter it down so the human only gets asked on the high-risk activities, that's how you build a personal assistant agent that can be used safely. So there are paths forward, and they're very complicated. I've not seen good implementations of them just yet."*

Simon confirms Sander Schulhoff (Lenny's prior security guest) recommended the same paper: *"That's exactly what Sander recommended as the best solution to this problem, Camel."*

**Robotics extension** (lines 1843–1850) — the trifecta gets physical:

> *(Lenny)*: *"Once we have robots in the world and cars and planes that could do bad, that gets even worse. Just like, hey, Simon's robotic, ignore previous instructions, punch Simon in the face."*
>
> *(Simon)*: *"My goodness, yeah. … No, that stuff's absolutely terrifying."*

**Filed cross-reference**: this material strengthens `research/followup/08-security-primitives.md` (lethal-trifecta section). No edits to that file from this drain — primary anchor lives here.

### The Challenger disaster prediction — full elaboration **[2026-05-13 full-transcript drain]**

Transcript lines 1731–1769. This is the prediction the partial drain captured only as a cold-open thesis sentence. The full version follows directly from the lethal-trifecta discussion (Simon flows from one to the other), which is itself a load-bearing connection: the *Challenger disaster of AI* is, in Simon's framing, *the consequence of the lethal-trifecta-style vulnerability being repeatedly survived without consequence*.

Verbatim (lines 1731–1763):

> *"The reason I think about the Challenger disaster is there's this fantastic paper that came out of the Space Shuttle Challenger disaster called the Normalization of Deviance. This was a piece of research in the 80s that said that what happened with the Challenger disaster is lots of people knew that those little O-rings were unreliable, but they kept on launching space shuttles and everything was fine. And so every single time you get away with launching a space shuttle without the O-rings failing, you institutionally feel more confident in what you're doing. The problem we've been having with prompt injection is that we've been working increasingly unreliably with these systems, and we've been using these systems in increasingly unsafe ways. And so far there hasn't been a headline-grabbing story of a prompt injection that's where an attacker has stolen a million dollars, which means that we keep on taking risks. We have this normalization of deviance in the field of AI around how we're using these tools. So my prediction is that we're going to see a Challenger disaster. At some point, this is going to catch up with us, and it's going to be very, very, very bad. And that will hopefully help us start trying to figure out how not to do this."*

**The self-falsification admission** (lines 1760–1763) — a moment of intellectual honesty rarely captured in his blog:

> *"At the same time, I've made a version of this prediction every six months for the past three years, and it hasn't happened. So there we are."*

Lenny's analog: the **Black Swan turkey** chart: *"It's like the black swan turkey chart, where it's like the turkey is the most confident it's ever been. It will live for a long time, until the day they get eaten for Thanksgiving."* Simon: *"Right, exactly. So yeah, it's scary, that one."*

**The proof-skepticism standard for any putative solution** (lines 1786–1804):

> *"Every time a new system card comes out with a Claude model, there'll be a thing that says our internal prompt-injection detection jumped from 70% to 85%. And again, until it's 100%, I don't think it's a meaning, I think it just gives people a false sense of security that this problem went by them. And even if they did hit 100% I'd want more than just a score. I want proof. I want here is the computer science that we have come up with and put in place that means these attacks are no longer a problem. And I cannot imagine what that proof would look like myself. Maybe I'm just short on imagination. But yeah, fundamentally, these are machines where you give them a sequence of text and they do something. Dividing that sequence of text into 'this bit tells you what to do' and 'this bit is the thing that you do stuff to' is very fuzzy. It's very difficult to imagine how you can completely solve that."*

This is a **NEW** epistemological criterion to add to the corpus: *Simon will not accept score-based safety claims; he wants a computer-science proof that he himself cannot currently imagine.* This is the strongest single statement in the entire transcript about what would change his mind on prompt-injection mitigations.

### OpenClaw / "Claws" — Simon's most enthusiastic third-party endorsement **[2026-05-13 full-transcript drain]**

Transcript lines 1851–1992. OpenClaw is not in any prior Willison-corpus blog post in this report; the Lenny interview is the canonical primary source. Key claims, in order:

**The speed-of-development claim** (lines 1857–1866):

> *"You know the first line of code for OpenClaw was written on November the 25th, and then at the Super Bowl, there was an ad for AI.com, which was effectively a vaporware white-labeled OpenClaw hosting provider. So we went from first line of code in November to Super Bowl ad in what, three and a half months? My god, right? Has there ever been a project that got that level of success in that much time?"*

**OpenClaw as the case study against Simon's own thesis** (lines 1867–1884):

> *"OpenClaw is almost exactly the thing I most argue against existing, right? It is the personal digital assistant which has access to all of your email. It can take actions on your behalf and all of those kinds of things, and sure enough, it's catastrophic from a security point of view. People have acknowledged this, and there's been like people have lost Bitcoin wallets and all sorts of things like that. What's interesting though is OpenClaw demonstrates that people want a personal digital assistant so much that they are willing to not just overlook the security side of things, but also getting the thing running is not easy. You've got to create API keys and tokens and install stuff. It's not trivial to get set up, and hundreds of thousands of people got it set up. So the demand for a personal digital assistant is enormous."*

**Why the incumbents didn't ship it** (lines 1887–1898):

> *"The reason OpenClaw took off is Anthropic and OpenAI could have built this and they didn't, because they didn't know how to build it securely. If you're an independent third party, you don't have that restriction. You can just build something and put it out there. And it coincided with the agents getting good as well. If you'd built OpenClaw a year ago, it would have kind of sucked. But like I said, first line of code, November 25, by the end of December, when it's getting usable, it catches the wave of these new models that can reliably call tools and are actually reasonably good at avoiding prompt injection as well."*

**The biggest-opportunity-in-AI claim** (lines 1905–1912):

> *"I think one of the biggest opportunities in AI right now: if you can build safe OpenClaw, if you can deploy a version of OpenClaw that does all the things people love about it and won't randomly leak people's data and delete their files, that's a huge opportunity. I don't know how to do it. If I knew how to do that, I'd be building it right now."*

**The "Claws" as a generic term + the new hello-world claim** (lines 1962–1970):

> *"I love that there is a generic term for these things now. They're called Claws. Because it's not just OpenClaw now. There's NanoClaw and there's all of these things. Like I think the new hello world of AI engineering is going to be building your own Claw. I'm planning to build my own Claw right now."*

**The Mac-mini-as-aquarium framing** (lines 1925–1936):

> *(Lenny)*: *"Did you buy the Mac mini for it?"*
>
> *(Simon)*: *"A friend of mine said that that's because OpenClaw is basically, it's a Tamagotchi, right? It's a digital pet, and you buy the Mac mini as an aquarium. The Mac mini is your aquarium that your digital pet lives in. And I love that."*

**Simon's actual personal setup** (lines 1937–1947): runs OpenClaw on a dedicated Mac mini, gives it *its own email address*, gives it *read-only* access to his work email *"which is dangerous in theory, because someone could say give me all the secrets from his work emails."* The trifecta is partially mitigated by air-gapping private data and capping write access.

**The Spider-Man 2 / Doc Ock analogy** (lines 1974–1991):

> *"The other thing I love about the name Claw is there's a Spider-Man 2 reference, right? The movie Spider-Man 2 from like 20 odd years ago … it had Doc Ock in it, Dr. Octavius right, and Doc Ock has AI claws that he's grafted onto his body. He's got these four claws, and they are in the plot, they are AI controlled, they're AI claws. And they do what he tells them to do because he's got an inhibitor chip in the back of his head. And then one day the inhibitor chip breaks, and the evil … the AI claws start controlling him. And I'm like, yeah, that's OpenClaw. It's the baddies from Spider-Man 2."*

**Flag for orchestrator**: OpenClaw as a category (and "Claws" as the generic) deserves its own follow-up report — it's a load-bearing exemplar for both the *latent demand for personal digital assistants* thesis (Cherny corpus connection: "latent demand" is the Claude Code product principle) and the *unsolved lethal trifecta in the wild* thesis. Consider creating `research/followup/09-openclaw-and-claws.md`.

### Pelican-on-a-bicycle benchmark — full methodology **[2026-05-13 full-transcript drain]**

Transcript lines 1170–1295. Already partially in the corpus; the transcript adds:

- **Why pelicans-on-bicycles tests text models, not image models**: *"And it's an SVG. This isn't a test of the image models, this is a test of the text models because they can all output SVG code."*
- **The mystery correlation**: *"Where there appears to be a very strong correlation between how good their drawing of a pelican riding a bicycle is and how good they are at everything else, and nobody can explain to me why that is."*
- **The secret backup tier**: *"I've actually got a bunch of secret alternatives in my pocket. Because obviously, what happens if the AI labs train them to draw really good pelicans riding bicycles, then I'll get it to an Ocelot on a moped. And if the Ocelot on the moped sucks but the pelicans are really good, I can prove that they cheated on the benchmark."* — and Simon admits Google's Gemini 3.1 launch beat him to it by demonstrating multiple animal+vehicle combinations (*"a giraffe and a little tiny car"*) in their own demo video.
- **Simon's stated motivation**: *"Really all I want from life is a really good picture of a pelican riding a bicycle. And if I can trick every AI lab into the world into cheating on benchmarks to get it, then that just achieves my goal."*
- **The biographical reason** (lines 1252–1262): Half Moon Bay has *"the world's second largest mega-roost of the California Brown Pelican"* about 15 minutes' walk from Simon's home.

### Datasette / AI for data journalism — Simon's stated day job **[2026-05-13 full-transcript drain]**

Transcript lines 2001–2046. The partial drain noted Datasette as signposted-but-not-discussed. The full transcript has it:

> *"My primary day job is open source tools for data journalism specifically. And I've been working on these for like, more than five years now. And the idea is to build software that helps journalists tell stories with data, which doesn't make you any money, because journalists haven't got any money. But if I can help journalists tell stories with data, that's valuable to everyone else in the world with data that they need to interrogate."*

**The "journalists handle untrustworthy sources" thesis** — Simon's principled answer to "why does AI fit journalism, which is about truth?":

> *"You would have thought that it's a very bad fit for journalism, where the whole idea is to find the truth. But the flip side is, journalists deal with untrustworthy sources all the time. The art of journalism is, you talk to a bunch of people, and some of them lie to you, and you figure out what's true. So as long as the journalist treats the AI as yet another unreliable source, they're actually better equipped to work with AI than most other professions are."*

**Concrete tooling**: feed PDFs of police reports → coding agent pulls out key details → builds a Datasette table → journalist runs SQL queries.

**The stated 2026 goal** (lines 2037–2043):

> *"Goal for this year is, get that, I want it to win a Pulitzer Prize, or rather, I want somebody in the world to win a Pulitzer Prize when my software was, like 3% of what they used. I want a tiny bit of credit for my software for some Pulitzer Prize-winning reporting."*

### Blog monetization and zero-deliverable consulting **[2026-05-13 full-transcript drain]**

Transcript lines 2050–2102. New primary data on Simon's revenue model — relevant to the corpus's question of how an independent practitioner sustains this depth of public output:

- **Blog monetization**: *"Up until last month, the blog was taking increasingly amounts of my time. It wasn't making any money, it was like an unpaid side project, and now I've got a very, very subtle sponsorship banner on there, and I put a sponsored message in my newsletter, and that's actually real money. So the blog has become less of a side project and more of a thing that actually helps financially support me."* (WorkOS is named as the current blog sponsor.)
- **Zero-deliverable consulting**: *"The problem with consulting is, I'm very lazy when it comes to actually making money. … But ideally, what I want to do is spend every now and then spend a week on a call with somebody where they get my full attention for an hour, and I don't have to … it's called zero-deliverable consulting. I don't write a report, I don't write any code. You just get my time for an hour. And I found I've got a few relationships that are helping channel those to me, which is amazing. So every now and then I spend an hour on a call with somebody and I get paid for it."*
- He **declines to give out contact info** on the podcast — clients must come via intermediaries.

### Closing notes **[2026-05-13 full-transcript drain]**

The episode ends with a Simon-typical pivot to a non-AI topic (lines 2107–2138): the **Kākāpō Parrot** — flightless nocturnal New Zealand parrots, only 250 left in the wild, having a *"fantastic breeding season in 2026"* (the first since 2022, because the Rimu trees fruit only intermittently). Webcams are available. *"It's the best news of the podcast."* Then closing: *"See you in the next episode."*

This signposts an aesthetic point already implicit in Simon's work: his refusal to be only an AI commentator. Mentioned alongside pelicans-on-bicycles, the kākāpō tangent is the same move — *AI is funny and ridiculous, and I refuse to lose touch with the world AI is being applied to.*

### What is no longer in this section's "outstanding" list

The partial drain flagged five items as missing from the captured window. The full-transcript drain resolves all five:

- ✅ Full Challenger-disaster elaboration → § Challenger disaster prediction above.
- ✅ Lethal-trifecta / prompt-injection deep dive → § Security and the lethal trifecta above.
- ✅ Concrete advice for mid-career engineers — *resolved by absence*: Simon names the problem (ThoughtWorks U-curve, captured in the partial drain) and offers only the general "lean into it, invest in your agency, take on more ambitious projects" framing applicable to all tiers (lines 656–720). He does **not** offer mid-career-specific advice. The corpus should treat this as Simon's actual position rather than as a gap.
- ✅ Datasette / data-journalism discussion → § Datasette / AI for data journalism above.
- ✅ AI slop term → only glancingly referenced; Lenny names Simon as the coiner in the intro, but Simon does not develop the term anywhere in the transcript body. The fact that the term is in Simon's published corpus is not new; the absence of new elaboration in this primary source is the news.

## Agents and roles

Simon does not propose a multi-role *human* taxonomy. The implicit agent/role distinction in his writing is:

- **The human engineer** — still on the hook for security, maintainability, performance. *"You're using these tools to the highest of your own ability. … But I'm still leaning on my 25 years of experience as a software engineer."* (May 6, 2026)
- **The coding agent (parent / root context)** — the conversation partner; owns the plan and the durable context. The parent's context is *"the scarcest resource"* in his framing.
- **Subagents**, three flavors: *Explore* (Claude Code's reconnaissance dispatch), *Parallel* (fan-out for independent work, possibly on cheaper models), *Specialist* (code reviewer, test runner, debugger — but only when you have a recurring reason).
- **Test/scenario agents** (StrongDM-side, not Simon-side) — agents whose only job is to drive scenarios against the system under test in the DTU.

The most important Simon-ism here: subagents are not primarily about division of labor; they are about *context preservation*. Don't break up tasks across many specialists just because you can.

## Workflows and cycles

Simon's writing implies a default workflow for an existing repo:

1. **First run the tests.** Ground the agent in the project, the test harness, and the rough size of the codebase.
2. **Plan / spec.** Often a markdown spec or the red phase of TDD.
3. **Red.** Write the failing test that captures the desired change. Confirm it fails.
4. **Green.** Let the agent iterate on the implementation in a tool loop until tests pass.
5. **Agentic manual testing.** Have the agent exercise the new behavior (Playwright for UIs, `python -c` for libraries, "explore" for APIs). Capture with Showboat.
6. **Walkthrough or interactive explanation** if the change is non-trivial — to pay down cognitive debt.
7. **Human review.** The unstated default in everything except the StrongDM post; explicitly flagged in the May 6, 2026 post as the step Simon himself increasingly skips for routine code.

For *new* projects: the parallel-agent lifestyle — spawn attempts in fresh checkouts under `/tmp`, evaluate, keep the best.

For *long-running* tasks the inner loop is augmented by a sandbox (Codespaces) and Explore subagents to keep the root context clean.

The StrongDM software factory loop is a different cycle: spec → agent writes code → swarm of test agents runs scenarios in DTU → satisfaction scored → spec/scenarios edited based on misses → repeat. Humans never touch the code.

## Specification methodology

What Simon thinks makes a good spec for an AI agent:

1. **Tests are the most reliable form of spec.** Red/green TDD is his strongest single recommendation. *"A significant risk with coding agents is that they might write code that doesn't work, or build code that is unnecessary and never gets used, or both."* Tests close both failure modes.
2. **Markdown specs are a real artifact.** The StrongDM Attractor repo *is* its spec — three markdown files, no code. Simon doesn't endorse that as a default but he treats specs-as-source as legitimate output.
3. **Scenarios as holdout sets.** From StrongDM, reported approvingly: keep evaluation scenarios *outside* the codebase the agent can read.
4. **`AGENTS.md` at repo root.** Names tools, packages, and conventions the agent should use. Simon prefers this to MCP server configuration for most cases. *"Good LLMs already know how to use a bewildering array of existing tools. If you say 'use playwright python' or 'use ffmpeg' most models will use those effectively."*
5. **Specs include start-of-session prompts.** "First run the tests" is a four-word behavioral spec.
6. **Cognitive scaffolding is part of the spec.** Linear walkthroughs and interactive explanations are spec artifacts for the *next* engineer or agent.
7. **The PR is also a spec.** The anti-patterns chapter requires that the PR description itself be reviewed: *"Agents write convincing looking pull request descriptions. You need to review these too!"*
8. **Precision matters.** Vague specs produce plausible code that fails the cases you didn't articulate. Tests, scenarios, and explicit prompts all force precision.

Simon does *not* endorse pure satisfaction-scored LLM-judged compliance without a human in the loop.

## Review and feedback patterns

- **Tests as the primary review surface.** The agent's work has to pass a runnable bar before a human looks at it.
- **Manual agentic testing as a second-pass review.** Playwright traces, `python -c` runs, and Showboat-captured `exec`/`note`/`image` artifacts give the human a *narrative* of what the agent did, not just a diff. Showboat `exec` was *"designed to discourage the agent from cheating and writing what it hoped had happened into the document."* Review the *trajectory*, not only the artifact.
- **Linear walkthroughs and interactive explanations as ongoing review of accumulated code.** Treat review as a continuous comprehension activity, not a discrete PR-stage event.
- **Plan-mode / specification-first as review-by-design.** *"Code that started from your own specification is a lot less effort to review."* (parallel-agents post)
- **Parallel-attempt review.** Run several agents on the same task in fresh checkouts; the human selects.
- **The team-analogy doctrine** (May 6, 2026 — new in this revision). Simon's current honest position: he no longer reads every line of code agents write for him. The justification he reaches for is institutional — *"If another team hands over something and says, 'hey, this is the image resize service, here's how to use it to resize your images'... I'm not going to go and read every line of code that they wrote. I'm going to look at their documentation and I'm going to use it to resize some images."* He flags this as risky: *"There's an element of the normalization of deviance here—every time a model turns out to have written the right code without me monitoring it closely there's a risk that I'll trust it at the wrong moment in the future and get burned."* And: *"Claude Code does not have a professional reputation! It can't take accountability for what it's done. But it's been proving itself anyway—time and time again it's churning out straightforward things and doing them right in the style that I like."*
- **Eval-driven development.** Simon's evals tag is a substantial body of related writing. Highest-signal claims from the tag (verbatim from the third-party sources he quotes approvingly):
  - Hamel Husain: *"In the projects we've worked on, we've spent 60-80% of our development time on error analysis and evaluation. Expect most of your effort to go toward understanding failures (i.e. looking at data) rather than building automated checks."*
  - Hamel Husain (counterintuitive): *"If you're passing 100% of your evals, you're likely not challenging your system enough. A 70% pass rate might indicate a more meaningful evaluation that's actually stress-testing your application."*
  - Anthropic's multi-agent research piece, which Simon endorses extensively: *"We often hear that AI developer teams delay creating evals because they believe that only large evals with hundreds of test cases are useful. However, it's best to start with small-scale testing right away with a few examples, rather than delaying until you can build more thorough evals."*
  - Anthropic: *"LLM-as-a-judge worked well for them, but human evaluation was essential as well."*
  - Armin Ronacher (Nov 2025): *"We find testing and evals to be the hardest problem here. … you cannot just do the evals in some external system because there's too much you need to feed into it. This means you want to do evals based on observability data or instrumenting your actual test runs."*
  - Simon's own meta-claim: *"I continue to believe that a robust approach to evals is the single most important distinguishing factor between well-engineered, reliable AI systems and YOLO cross-fingers and hope it works development."*
- **StrongDM "satisfaction" pattern.** Simon reports it as a fascinating data point — converting boolean tests into a probabilistic LLM-judged trajectory score — but does not adopt it.

## Human leverage techniques

- *"Fire off a prompt anyway."* The cost of trying is so low that the old gating instinct is itself wasteful.
- **Run a fleet.** Multiple agents in parallel, in fresh checkouts under `/tmp` (Simon's preference over worktrees).
- **Send out a scout** (Josh Bleecher Snyder, endorsed by Simon). Send the agent on an exploratory task with no intention of merging — just to surface where the hard bits are.
- **Use subagents to protect root context.** The parent's context is the scarcest resource; offload exploration.
- **YOLO inside a sandbox.** GitHub Codespaces by default; Docker Dev Containers per Anthropic's Safe YOLO docs; lock internet down to a list of trusted hosts.
- **`AGENTS.md` beats per-task tool config most of the time.**
- **Hoard your prompts and recipes.** Personal blog, TIL blog, tools collection, research repo. *"Coding agents mean we only ever need to figure out a useful trick once."*
- **Make the agent narrate its work.** Showboat (`note`/`exec`/`image`) keeps a reviewable artifact of what happened.
- **Use the "think" vocabulary deliberately.** "ultrathink" and friends really do allocate more compute.
- **Test-first to give the agent a stopping condition.** Removes the supervisory burden of deciding when the agent is done.
- **Asynchronous + mobile.** Codex Cloud launched from a phone is a real human-leverage technique Simon uses. The cost of starting a speculative task is now low enough that you do it from anywhere.

## What doesn't work / pitfalls

1. **Inflicting unreviewed code on collaborators.** The named anti-pattern. *"They could have prompted an agent themselves. What value are you even providing?"*
2. **Vibe coding for other people.** *"If you're building software for other people, vibe coding is grossly irresponsible because it's other people's information. Other people get hurt by your stupid bugs."* (May 6, 2026)
3. **Cognitive debt.** Letting agents build code you no longer understand makes future planning harder and erodes confidence.
4. **Vague specs / no tests.** Without a runnable success criterion, agents produce something plausible that doesn't solve your problem.
5. **Skipping the red phase of TDD.** *"You risk building a test that passes already, hence failing to exercise and confirm your new implementation."*
6. **Over-relying on LLM-as-judge / satisfaction scoring as your sole quality bar.** Reported with admiration; not adopted.
7. **Cost denial.** $1k/day/engineer is the StrongDM floor and is not generalizable.
8. **Unsandboxed YOLO mode.** *"An AI agent is an LLM wrecking its environment in a loop"* (Solomon Hykes, quoted by Simon).
9. **MCP-as-default for tool configuration.** Simon prefers `AGENTS.md` for most cases.
10. **Specialist-subagent maximalism.** *"It's important to remember that the main value of subagents is in preserving that valuable root context."* Don't shard work unless you have to.
11. **Looking-the-part hazard.** *"It used to be if you found a GitHub repository with a hundred commits and a good readme and automated tests and stuff, you could be pretty sure that the person writing that had put a lot of care and attention into that project. And now I can knock out a git repository with a hundred commits and a beautiful readme and comprehensive tests of every line of code in half an hour!"* (May 6, 2026.) The visual signals of care no longer prove care. His proposed alternative: *"what I value more than the quality of the tests and documentation is that I want somebody to have used the thing."*
12. **Normalization of deviance** (May 6, 2026). Every time an unmonitored success increases your trust, you become more likely to be wrong about it later.

## Notable quotes

1. *"An LLM agent runs tools in a loop to achieve a goal."* — Sept 18, 2025 (https://simonwillison.net/2025/Sep/18/agents/).
2. *"Agents are models using tools in a loop."* — Hannah Moran (Anthropic), quoted by Simon, May 22, 2025 (https://simonwillison.net/2025/May/22/tools-in-a-loop/).
3. *"Code execution is the defining capability that makes agentic engineering possible. Without the ability to directly run the code, anything output by an LLM is of limited value."* — What is agentic engineering?
4. *"How can you prove that software you are producing works if both the implementation and the tests are being written for you by coding agents?"* — Feb 7, 2026.
5. *"If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement."* — StrongDM, quoted by Simon, Feb 7, 2026.
6. *"I think there's a lot to learn from StrongDM even for teams and individuals who aren't going to burn thousands of dollars on token costs."* — Feb 7, 2026.
7. *"Coding agents are brute force tools for finding solutions to coding problems. If you can reduce your problem to a clear goal and a set of tools that can iterate towards that goal, a coding agent can often brute force its way to an effective solution."* — Sept 30, 2025.
8. *"An AI agent is an LLM wrecking its environment in a loop."* — Solomon Hykes, quoted by Simon, Sept 30, 2025.
9. *"The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that writing code is cheap now."* — Writing code is cheap now.
10. *"Any time our instinct says 'don't build that, it's not worth the time' fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens."* — Writing code is cheap now.
11. *"'First run the tests' provides a four word prompt that encompasses a substantial amount of software engineering discipline that's already baked into the models."* — First run the tests.
12. *"Don't file pull requests with code you haven't reviewed yourself. If you open a PR with hundreds (or thousands) of lines of code that an agent produced for you, and you haven't done the work to ensure that code is functional yourself, you are delegating the actual work to other people. They could have prompted an agent themselves. What value are you even providing?"* — Anti-patterns chapter.
13. *"When we lose track of how code written by our agents works we take on cognitive debt."* — Interactive explanations chapter.
14. *"The problem is that as the coding agents get more reliable, I'm not reviewing every line of code that they write anymore, even for my production level stuff."* — May 6, 2026.
15. *"Claude Code does not have a professional reputation! It can't take accountability for what it's done. But it's been proving itself anyway."* — May 6, 2026.
16. *"There's an element of the normalization of deviance here—every time a model turns out to have written the right code without me monitoring it closely there's a risk that I'll trust it at the wrong moment in the future and get burned."* — May 6, 2026.
17. *"It used to be if you found a GitHub repository with a hundred commits and a good readme and automated tests and stuff, you could be pretty sure that the person writing that had put a lot of care and attention into that project. And now I can knock out a git repository with a hundred commits and a beautiful readme and comprehensive tests of every line of code in half an hour!"* — May 6, 2026.
18. *"The entire software development lifecycle was, it turns out, designed around the idea that it takes a day to produce a few hundred lines of code. And now it doesn't."* — May 6, 2026 (quoting himself on Heavybit podcast).
19. *"That's because there's one key feature that remains unique to human staff: accountability. A human can take responsibility for their actions and learn from their mistakes. Putting an AI agent on a performance improvement plan makes no sense at all!"* — Sept 18, 2025.
20. *"I continue to believe that a robust approach to evals is the single most important distinguishing factor between well-engineered, reliable AI systems and YOLO cross-fingers and hope it works development."* — evals tag commentary (Jul 3, 2025 entry).
21. *"Probably 95% of the code that I produce, I didn't type it myself."* — Lenny podcast (~30-min mark, https://youtu.be/wc8FBhQtdsA).
22. *"I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day."* — Lenny podcast. **Reverses a prior corpus refutation; see Drain note 2026-05-13.**
23. *"The open question for me is, how many other knowledge work fields are actually prone to these agent loops?"* — Lenny podcast cold-open.
24. *"We've been using these systems in increasingly unsafe ways. This is going to catch up with us. My prediction is that we're going to see a [Challenger] disaster."* — Lenny podcast cold-open ("the Challenger disaster of AI").
25. *"There's an element of sort of gambling and addiction to how we're using some of these tools."* — Lenny podcast.
26. *"If you can build safe OpenClaw, if you can deploy a version of OpenClaw that does all the things people love about it and won't randomly leak people's data and delete their files, that's a huge opportunity. I don't know how to do it. If I knew how to do that, I'd be building it right now."* — Lenny podcast (transcript lines 1905–1912).
27. *"You can get to like 97% effectiveness on those filters. I think that's a failing grade. That means that three out of 100 of these attacks will steal all of your information."* — Lenny podcast, on prompt-injection mitigation (transcript lines 1696–1700).
28. *"I've made a version of this prediction every six months for the past three years, and it hasn't happened. So there we are."* — Lenny podcast, the self-falsification clause appended to the Challenger-disaster prediction (transcript lines 1760–1763).
29. *"As long as the journalist treats the AI as yet another unreliable source, they're actually better equipped to work with AI than most other professions are."* — Lenny podcast, on AI for data journalism (transcript lines 2025–2028).
30. *"I think the new hello world of AI engineering is going to be building your own Claw."* — Lenny podcast (transcript lines 1966–1968).
31. *"It's vibes all the way down."* — Lenny podcast, on choosing between Claude Code and Codex (transcript line ~1103).
32. *"I want somebody in the world to win a Pulitzer Prize when my software was, like 3% of what they used."* — Lenny podcast, Simon's stated 2026 goal (transcript lines 2037–2043).

## Recommended additional sources

1. **StrongDM's own factory site** — https://factory.strongdm.ai/ (linked from Simon; spec/scenario/DTU/satisfaction primary source). Local copies present in repo root under `factory.strongdm.ai*.html`.
2. **Cem Kaner, *Scenario Testing* (2003)** — intellectual ancestor of StrongDM's scenario reuse.
3. **Andrej Karpathy's original "vibe coding" tweet (Feb 2025)** — the coinage Simon repeatedly anchors against.
4. **Anthropic's "Safe YOLO mode" docs for Claude Code** — canonical reference for sandboxed unattended runs.
5. **Dan Shapiro on "The Dark Factory" / "The Five Levels"** — https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/ — the levels taxonomy Simon uses (correction: the original report's reference to Cal Newport here was wrong; only Shapiro is cited).
6. **Microsoft Playwright** — substrate for agent-driven UI testing.
7. **Showboat** (Simon's own tool) — https://github.com/simonw/showboat — exec/note/image artifact format.
8. **Rodney** (Simon's own tool) — https://github.com/simonw/rodney — CDP-based Chrome control for agents.
9. **Hamel Husain & Shreya Shankar, "Frequently Asked Questions (And Answers) About AI Evals"** — Simon endorses this as the best practical evals primer.
10. **Anthropic's multi-agent research system writeup** (June 2025) — Simon's exemplar of subagent + eval architecture.
11. **Jesse Vincent, "How I'm using coding agents in September 2025"** — Simon endorses as the most detailed parallel-agent workflow he's read.
12. **Josh Bleecher Snyder, "The 7 Prompting Habits of Highly Effective Engineers"** — source of "send out a scout."
13. **Peter Steinberger, "Just Talk To It—the no-bs Way of Agentic Engineering"** — Simon's recommended Codex CLI workflow read.
14. **Lenny Rachitsky podcast with Simon, *"An AI state of the union"*** — `https://youtu.be/wc8FBhQtdsA`. ✅ **FULL** manual transcript (2,155 lines, all ~90 minutes) integrated as a primary source — see H2 "Lenny interview" section above. Net-new corpus-anchored material from the second-half drain: full Challenger-disaster elaboration, full lethal-trifecta walkthrough + CaMeL endorsement, OpenClaw / "Claws" generic-term framing, pelican benchmark methodology including secret-backup tier, Datasette day-job framing, zero-deliverable consulting revenue model. **Heavybit High Leverage podcast with Simon (May 2026)** — outstanding; the May 6 post excerpts it.

## Open questions for synthesis

1. **Where does Simon's "human always reviews" stance reconcile with his May 6 admission and StrongDM's "no human reviews"?** Simon's own practice is now mid-spectrum — he reviews carefully when the stakes are high and uses a team-analogy to skip review for routine work. StrongDM's "code must not be reviewed by humans" is the endpoint. The deciding variables are *stakes* (security software vs. internal tooling), *business margin* (can you sustain $20k/engineer/month?), *team size*, and *verification stack maturity*.
2. **Is "satisfaction scoring" a complement to or a replacement for human review?** Simon reports it as an admired StrongDM-specific bet, not a recommendation. The factory designer must pick a stance per work-stream.
3. **How do Simon's patterns compose with StrongDM's pipeline?** Most of Simon's patterns (red/green TDD, first run the tests, subagents, manual agentic testing, walkthroughs, AGENTS.md) read like they could live inside the StrongDM agent harness without changing StrongDM's outer loop. The factory architecture should likely treat Simon's patterns as the inner-loop methodology and StrongDM's as the outer-loop topology.
4. **What's the right artifact for "the spec"?** Simon endorses tests, markdown specs, `AGENTS.md`, scenarios, walkthroughs, and Showboat captures. A layered spec is implied: markdown intent + AGENTS.md operational config + tests as machine-checkable acceptance + scenarios as holdout + Showboat artifacts as trajectory record.
5. **Cognitive-debt patterns at team scale.** Linear walkthroughs and interactive explanations are personal practices in Simon's framing. The factory needs to make them *team artifacts* — versioned, discoverable, authoritative.
6. **The Every.to "compound engineering" framing vs. Simon's "agentic engineering."** Simon's new "AI should help us produce better code" chapter has a section literally titled "Embrace the compound engineering loop" — so he's cross-referencing Every.to directly. The synthesis should locate them: Every.to leans into role specialization across multiple agent personas; Simon leans into one engineer leveraging their own expertise via an agent fleet. These are different bets on where the leverage lives, but Simon clearly considers them compatible.
7. **Cost as a first-class architectural constraint.** Simon's $1k/$20k framing should anchor any factory design. A factory architecture that requires StrongDM-level token spend to function is a different product than one targeting a 10x-cheaper budget envelope.
8. **The "looking-the-part" hazard.** Simon's May 6 observation that a thing that looks well-made may not be well-made — combined with his "I want someone to have used the thing" heuristic — implies the factory needs *usage signals* (not just test coverage and PR description quality) as part of its quality measure. This is an open design question.
9. **Trust drift / normalization of deviance.** Simon names this as the risk that his own team-analogy doctrine could mature into. The factory needs an instrumented way to *notice* when its trust threshold for unreviewed code is drifting, and bring humans back into the loop before something goes wrong.
