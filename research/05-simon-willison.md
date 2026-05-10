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

**Date:** 2026-05-10

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
14. **Lenny Rachitsky podcast with Simon (Apr 2026)** and **Heavybit High Leverage podcast with Simon (May 2026)** — these are where Simon thinks out loud about the vibe-coding/agentic-engineering convergence; the May 6 post excerpts the second.

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
