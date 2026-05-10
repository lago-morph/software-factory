# Simon Willison — Software Factory & Agentic Engineering Patterns
**Sources covered:**
- https://simonwillison.net/2026/Feb/7/software-factory/ — "How StrongDM's AI team build serious software without even looking at the code"
- https://simonwillison.net/guides/agentic-engineering-patterns/ — guide index
- https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/
- https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/ — "Writing code is cheap now"
- https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/
- https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/
- https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/
- https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/
- https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/
- https://simonwillison.net/guides/agentic-engineering-patterns/interactive-explanations/
- https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/
- https://simonwillison.net/guides/agentic-engineering-patterns/subagents/
- https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/
- https://simonwillison.net/guides/agentic-engineering-patterns/prompts/
- https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/ — meta-post about the guide
- https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
- https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ — "Embracing the parallel coding agent lifestyle"
- https://simonwillison.net/2025/May/22/tools-in-a-loop/ — "Agents are models using tools in a loop"
- https://simonwillison.net/2025/Sep/18/agents/ — agent definition
- https://simonwillison.net/2025/Apr/19/claude-code-best-practices/
- https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/
- https://simonwillison.net/tags/evals/ — evals tag
- https://simonwillison.net/tags/agentic-engineering/

**Date:** 2026-05-10

**Methodological note:** simonwillison.net was unreachable from the research sandbox (HTTP 403, host not allowed), and the Substack mirror was similarly blocked. All content below was reconstructed from web search snippets, Mastodon/X cross-posts authored by Willison, and quotation in third-party coverage. Where I am confident in verbatim wording I quote it; where I have only paraphrase, I indicate that. A pass with direct page access would tighten quotations and could surface chapters I have not enumerated.

## Executive summary

Simon Willison's overall thesis across these sources is that we are at a real inflection point in software engineering: coding agents — defined narrowly as "models using tools in a loop" — are now capable enough that an experienced engineer can use them to attempt much more ambitious projects than they otherwise would. He calls the resulting craft **agentic engineering**, deliberately distinguishing it from **vibe coding** (which he reserves for "unreviewed, prototype-quality LLM-generated code"). Agentic engineering is what a professional does: still on the hook for security, maintainability, operations, and performance, but using agents to amplify their own existing expertise rather than to replace it.

What's distinctive about Simon's framing relative to other "AI-native development" writers:

1. **The agent definition is mechanical, not aspirational.** "An LLM agent runs tools in a loop to achieve a goal." That single sentence does most of his explanatory work — agents are not magic, the harness is a few hundred lines, and the design problem is choosing the right tools and the right termination condition.
2. **He treats the patterns book as a living guide.** "Agentic Engineering Patterns" is loosely modeled on the 1994 Gang of Four *Design Patterns* — chapter-shaped, each a focused pattern with a name, a problem, a remedy — but published as a continuously updated web guide rather than a frozen book. The format itself is a methodology argument: agentic practice changes too quickly for static deliverables.
3. **He is bullish on tests-as-spec, bearish on unreviewed output.** Test-first / red-green TDD and "first run the tests" are the load-bearing patterns. The single anti-pattern he has so far named is "inflicting unreviewed code on collaborators."
4. **He is fascinated but skeptical of the StrongDM "software factory."** The Feb 7, 2026 post is admiring of StrongDM's ambition and craft (specs as the entire repository, a Digital Twin Universe of fake third-party services, satisfaction scoring instead of green/red tests) but calls the no-human-review principle "wildly irresponsible" outside StrongDM's specific niche, and is unimpressed by the implied $20k/engineer/month token bill.
5. **Cognitive debt is his core worry.** The most distinctive Simon-ism in the agentic engineering guide is his concern that you can lose the ability to reason about code an agent built for you. Several patterns (linear walkthroughs, interactive explanations, agentic manual testing) exist specifically to keep the human in cognitive contact with the system.
6. **He believes humans must remain the reviewer.** Even as he documents StrongDM admiringly, his own practice is firmly that an engineer reviews what the agent produces. Agents make "inhuman mistakes"; humans need to catch them.

Where he is bullish: massive uplift in personal productivity for an engineer who knows what they're doing; the cost of trying speculative ideas has collapsed; small parallel agent fleets are now practical for one person; tests + sandboxes + good prompts are sufficient for most real work.

Where he is bearish / cautious: unreviewed code in production, especially shared with collaborators; teams treating agents as code reviewers; spending $1k+/day on tokens as a default; the "satisfaction" scoring of LLM-judged scenarios as a sole quality bar; the assumption that StrongDM's pattern generalizes outside its specific high-margin, high-stakes context.

## The software factory post — main argument

The post is titled "How StrongDM's AI team build serious software without even looking at the code" (February 7, 2026). It's a reported piece — Simon visited the team in person in October 2025. He frames StrongDM's work as "the most ambitious form of AI-assisted software development I've seen yet."

**The setup.** StrongDM's three-person AI team (Justin McCarthy, Jay Taylor, Navan Chauhan) had been working three months when Simon visited. Even at that age they had: a coding agent harness ("Attractor"), a "Digital Twin Universe" of behavioral clones of third-party services, and a swarm of simulated test agents driving scenarios. Their charter is captured in two principles Simon highlights as the most provocative:

> "Code must not be written by humans"
> "Code must not be reviewed by humans"

**What's in the spec.** The Attractor repository contains *no code at all*. It contains three markdown files describing the spec in meticulous detail, plus a README telling you to feed those files into your coding agent of choice. (Third-party coverage of the same post puts the spec at "6,000–7,000 lines of natural language specification driving the entire system" — Simon's own post mentions the markdown-only structure but I cannot verify the line-count quote without direct page access.)

**Scenarios.** StrongDM borrowed and re-purposed the term *scenario* from Cem Kaner's 2003 scenario testing work. Per StrongDM's own description, which Simon quotes:
> "We repurposed the word scenario to represent an end-to-end 'user story', often stored outside the codebase (similar to a 'holdout' set in model training), which could be intuitively understood and flexibly validated by an LLM."

Scenarios are the holdout set. Critically, they're stored *outside* the codebase so the coding agents can't see them — preserving the QA-team intuition of "evaluator must not be the same person as the implementer."

**Digital Twin Universe (DTU).** StrongDM built behavioral replicas of Okta, Jira, Slack, Google Docs, Google Drive, and Google Sheets. Their construction strategy: dump the full public API documentation of the target service into the agent harness, have it produce an imitation API as a self-contained Go binary, then build a simplified UI on top to complete the simulation. The point is that "thousands of test scenarios per hour" can run with no rate limits, no third-party API costs, and no risk of damaging real services or data.

**Satisfaction scoring.** Because the system itself has agentic components whose outputs are non-deterministic, StrongDM "transitioned from boolean definitions of success ('the test suite is green') to a probabilistic and empirical one." They use the term *satisfaction* — "of all the observed trajectories through all the scenarios, what fraction of them likely satisfy the user?" The judgment is performed by LLMs, not human reviewers.

**The most consequential question.** Simon names what he sees as the central question this approach forces onto the field:
> "How can you prove that software you are producing works if both the implementation and the tests are being written for you by coding agents?"

StrongDM's answer is the spec / scenarios / DTU / satisfaction-score loop, treated as the ground truth.

**Simon's verdict.** He's clearly impressed by the engineering — but his commentary, including a section he added in an update to the post, is hedged in three specific ways:

1. *Cost.* "If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement." Simon flags that if the pattern truly costs $20,000/month per engineer, "this becomes more of a business model exercise: can you create a profitable enough line of products that you can afford the enormous overhead of developing software in this way?"
2. *Generalization.* He hopes "these patterns can be put into play with a much lower spend" and writes that "there's a lot to learn from StrongDM even for teams and individuals who aren't going to burn thousands of dollars on token costs." But he is careful not to advocate the no-human-review rule outside StrongDM's specific context.
3. *Risk.* In follow-up commentary he refers to the unreviewed-code stance as "clear insanity" and "wildly irresponsible" in general — but worth paying attention to *because* StrongDM is a security company, which raises the bar of how seriously they must already be taking adversarial review.

The post is reportage + admiration + warning. Simon is not endorsing the pattern; he is naming it as the maximum-ambition reference point.

## Pattern catalog

Below is every pattern I could identify in the Agentic Engineering Patterns guide hierarchy and the surrounding posts. Where my information is inferred or partial, I say so.

### From the guide hierarchy

**1. What is agentic engineering? (foundational, not strictly a pattern)**
- *URL:* /guides/agentic-engineering-patterns/what-is-agentic-engineering/
- *What:* Defines agentic engineering as the practice of developing software with the assistance of coding agents — agents that can both write and execute code (Claude Code, OpenAI Codex, Gemini CLI). Distinguishes it from vibe coding (Karpathy, Feb 2025: prompting LLMs to write code while you "forget that the code even exists"). Vibe coding for Simon is reserved for unreviewed prototype output; agentic engineering is what a professional engineer does.
- *Key claim:* "Code execution is the defining capability that makes agentic engineering possible. Without the ability to directly run the code, anything output by an LLM is of limited value."
- *Solves:* terminology confusion; gives the field a name distinct from "AI coding."

**2. Writing code is cheap now**
- *URL:* /guides/agentic-engineering-patterns/code-is-cheap/
- *What:* The core mindset shift. The cost to produce initial working code has dropped to almost nothing.
- *When to use:* Always, as a personal and team posture.
- *Concrete heuristic:* "Any time your instinct says 'don't build that, it's not worth the time' fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens."
- *Solves:* Engineers under-using agents because they bring legacy intuitions about effort cost.

**3. How coding agents work**
- *URL:* /guides/agentic-engineering-patterns/how-coding-agents-work/
- *What:* Mechanical explanation. The harness extracts tool-call requests from model output (often via regex), executes them, and feeds results back. A simple loop is dozens of lines of code; a *good* loop is much more.
- *Solves:* Demystification. If you understand the loop, you can debug it, instrument it, and design tools for it.

**4. Red/green TDD**
- *URL:* /guides/agentic-engineering-patterns/red-green-tdd/
- *What:* "Use test driven development, write the tests first, confirm that the tests fail before you implement the change that gets them to pass."
- *When:* Whenever you're asking an agent to make a behavioral change you can describe as a test.
- *Solves:* Two huge agent failure modes — code that doesn't actually do what was asked, and code that builds unnecessary scaffolding. Forces concrete success criteria and a stopping condition. Confirming red first ensures the test actually exercises the new behavior; otherwise you can ship a test that was already passing and proves nothing.

**5. First run the tests**
- *URL:* /guides/agentic-engineering-patterns/first-run-the-tests/
- *What:* A four-word starting prompt for any session against an existing project. (For Python: "Run 'uv run pytest'.")
- *When:* The opening move of any agentic engineering session in an existing repo.
- *Solves:* Forces the agent to discover the test harness, gives it a rough complexity estimate, and primes a "testing mindset" so it will both run and extend tests later. "A four word prompt that encompasses a substantial amount of software engineering discipline that's already baked into the models."

**6. Agentic manual testing**
- *URL:* /guides/agentic-engineering-patterns/agentic-manual-testing/
- *What:* Have the agent itself "manually" exercise the code, frequently catching issues automated tests don't.
- *Substrate techniques:*
  - *Python libraries:* Tell the agent to use the `python -c` trick.
  - *Web APIs:* Tell the agent to "explore" the API.
  - *Web UIs:* Tell the agent to "test that with Playwright."
- *Documentation tool:* Simon built **Showboat** to capture an agentic-manual-testing flow as a markdown document — `note` appends a markdown note, `exec` records a command and its output, `image` adds a screenshot.
- *Solves:* Behaviors that automated tests miss; gives the human a reviewable artifact of what the agent actually did.

**7. Linear walkthroughs**
- *URL:* /guides/agentic-engineering-patterns/linear-walkthroughs/
- *What:* Have the agent produce a structured top-to-bottom walkthrough of a codebase, written into a `walkthrough.md` (often via Showboat).
- *When:* New codebase, code you wrote a long time ago, or code you let an agent build that you no longer fully understand.
- *Prompt sketch:* "Read the source and then plan a linear walkthrough of the code that explains how it all works in detail."
- *Solves:* "Cognitive debt" — when the core of an application is a black box you can no longer confidently reason about.

**8. Interactive explanations**
- *URL:* /guides/agentic-engineering-patterns/interactive-explanations/
- *What:* Have the agent build small, custom, interactive (often animated) explanations of an algorithm or system on demand. Example given: a word-cloud animation that visualizes each word being placed by spiral search outward from the centre, making the algorithm legible.
- *When:* Code is correct but obscure; team needs to onboard; an algorithm needs to be communicated.
- *Solves:* Same cognitive-debt problem as walkthroughs, but for individual algorithms or subsystems rather than whole codebases.

**9. Hoard things you know how to do**
- *URL:* /guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/
- *What:* A career-style pattern: keep a personal accumulating library of recipes, prompts, and known-good techniques you've gotten an agent to execute. Simon frames it as "general career advice which also happens to help when working with coding agents."
- *Solves:* Prompt amnesia, repeated rediscovery, and the fact that the highest-leverage moments with agents come from already knowing the shape of the task.

**10. Subagents (with sub-chapters: Claude Code's Explore subagent, Parallel subagents, Specialist subagents)**
- *URL:* /guides/agentic-engineering-patterns/subagents/
- *What:* When a coding agent uses a subagent it dispatches a fresh copy of itself, with a new context window and a fresh prompt. The principal advantage is preserving the parent's valuable root context and managing token-heavy operations without burning through the top-level budget.
- *When:* Long-running sessions where context exhaustion is the risk; tasks like wide code search or document ingestion that consume tokens but yield small outputs.
- *Solves:* Context pollution; runaway token spend on the main loop; task isolation.

**11. Prompts I use (collection, not a single pattern)**
- *URL:* /guides/agentic-engineering-patterns/prompts/
- *What:* A continually updated section of prompts Simon uses himself, linked from the chapters they support. Examples mentioned: extracting quoted highlights from podcast transcripts (Claude Project), HTML/JS-only Claude artifact instructions for static hosting, the prompt that produced his GIF-compression web UI on top of a WebAssembly Gifsicle build.

**12. Anti-patterns** (chapter started, currently lists one)
- *URL:* /guides/agentic-engineering-patterns/anti-patterns/
- *Anti-pattern:* **Inflicting unreviewed code on collaborators** — "dumping a thousand line PR without even making sure it works first."
- *Solves:* The single sharpest social pathology of agentic engineering — pushing the cost of agent slop onto your teammates.

### Additional patterns from adjacent posts (same author, same site)

**13. Designing agentic loops**
- *URL:* /2025/Sep/30/designing-agentic-loops/
- *What:* The deliberate practice of choosing tools, sandboxes, and termination conditions for an agent. "Coding agents are brute force tools for finding solutions to coding problems — if you can reduce your problem to a clear goal and a set of tools that can iterate towards that goal, a coding agent can often brute force its way to an effective solution." Calls this "a critical new skill to develop."
- *Specific guidance:* Prefer an `AGENTS.md` file describing packages the agent may use over leaning on MCP. Run agents in sandboxes to make YOLO mode survivable.

**14. YOLO-mode-with-a-sandbox**
- *URL:* /2025/Sep/30/designing-agentic-loops/
- *What:* Agents are inherently dangerous; that danger is what makes them productive. The mitigation is environmental, not behavioral: a sandbox that restricts file/secret access and network reach. Simon's preferred substrate is GitHub Codespaces (free tier, fresh container per task, browser-accessible). He also points at Anthropic's Safe YOLO documentation (use `--dangerously-skip-permissions` inside a container with no internet).
- *The three risks named:* (a) bad shell commands deleting/mangling things you care about, (b) exfiltration of files or env-var secrets, (c) the agent's machine being used as a proxy for attacks on third parties.

**15. Parallel coding agent lifestyle**
- *URL:* /2025/Oct/5/parallel-coding-agents/
- *What:* Run multiple Claude Code / Codex CLI instances at once — sometimes in the same repo, sometimes in fresh checkouts or git worktrees. Simon himself does fresh checkouts into `/tmp` rather than worktrees.
- *Solves:* The single-agent serial bottleneck; lets one human run a small fleet and pick winners.

**16. Tools-in-a-loop framing**
- *URL:* /2025/May/22/tools-in-a-loop/ and /2025/Sep/18/agents/
- *What:* Simon's preferred definition: "An LLM agent runs tools in a loop to achieve a goal." This is the substrate definition behind the entire guide. He explicitly likes that this definition is mechanical and falsifiable — you can point at any system and ask, "is there a tool loop and a goal?"

## Agents and roles

Simon does not propose a multi-role *human* taxonomy in the way StrongDM or Every.to do. The implicit agent/role distinction in his writing is:

- **The human engineer** — still on the hook for review, security, maintainability, performance. Operates above the code, not below it.
- **The coding agent** (parent / root context) — the one you converse with directly. Owns the plan and the durable context.
- **Subagents** — dispatched copies, each with a fresh context window. Three named flavors:
  - *Explore subagent* (Claude Code's, used for codebase reconnaissance)
  - *Parallel subagents* (fan-out for independent work)
  - *Specialist subagents* (configured for a recurring task type)
- **Test/scenario agents** (in the StrongDM post, not in the guide) — agents whose only job is to drive scenarios against the system under test in the DTU.

The most useful Simon-ism here: subagents are not primarily about division of labor; they are about *context preservation*. The reason to spin a subagent is that the parent's context is precious and should not be polluted with token-heavy exploration.

## Workflows and cycles

Simon's writing implies (rather than diagrams) a default workflow for agentic engineering on an existing repo:

1. **First run the tests.** Ground the agent in the project, the test harness, and the rough size of the codebase.
2. **Plan / spec.** Often a markdown spec or a TDD red phase. (Simon doesn't have a dedicated "plan mode" chapter at the snapshot I can see, though he uses Claude Code's plan mode in practice.)
3. **Red.** Write the failing test that captures the desired change. Confirm it fails.
4. **Green.** Let the agent iterate on the implementation in a tool loop until tests pass.
5. **Manual agentic testing.** Have the agent exercise the new behavior (Playwright for UIs, `python -c` for libraries, "explore" for APIs). Capture in Showboat.
6. **Walkthrough or interactive explanation** if the change is non-trivial — to keep the human in cognitive contact.
7. **Human review.** This step is the unstated default in everything except the StrongDM post.

For *new* projects he leans on the parallel-agent lifestyle: spawn several attempts in fresh checkouts under `/tmp`, evaluate, keep the best. The "writing code is cheap" mindset says: try, don't deliberate.

For *long-running* tasks the inner loop is augmented by:
- A sandbox (Codespaces) so YOLO mode can run.
- Subagents (especially Explore) to keep the root context clean.

The StrongDM software factory loop, as Simon describes it, is a different cycle entirely — closer to: spec → agent writes code → swarm of test agents runs scenarios in DTU → satisfaction scored → spec/scenarios edited based on misses → repeat. Humans never touch the code.

## Specification methodology

What Simon thinks makes a good spec for an AI agent (synthesized from across the corpus):

1. **Tests are the most reliable form of spec.** Red/green TDD is his strongest single recommendation. A failing test is an unambiguous, machine-checkable specification that also forces the human to be precise about success criteria.
2. **Markdown specs are a real artifact, not a stepping stone.** The StrongDM post celebrates a repo that *is* its spec — three markdown files, no code. He doesn't endorse that as a default but he treats specs-as-source as legitimate engineering output, not as scaffolding.
3. **Scenarios as holdout sets.** From StrongDM (Simon doesn't claim this as his own pattern, but he reports it approvingly): keep evaluation scenarios *outside* the codebase the agent can read. Same logic as a model holdout — if the implementer (the agent) can see the scenarios, the scenarios stop measuring generalization.
4. **An `AGENTS.md` file at repo root.** Names tools, packages, and conventions the agent should use. Simon prefers this to MCP server configuration for most cases.
5. **Specs include start-of-session prompts.** "First run the tests" is a four-word spec for "I want you to engage with this project's test discipline." Specs for agents are partially behavioral, not purely declarative.
6. **Specs should include cognitive scaffolding.** Linear walkthroughs and interactive explanations are spec artifacts in a non-traditional sense — they are the spec the *next* engineer (or agent) will read to maintain the system.
7. **Be precise about success.** The implicit warning across the guide is that vague specs produce code that "looks right" but fails on the cases you didn't articulate. Tests, scenarios, and explicit prompts are all forms of forcing precision.

What Simon does *not* endorse: pure satisfaction-scored LLM-judged spec compliance without a human in the loop. He admires StrongDM's bet but does not generalize it.

## Review and feedback patterns

- **Tests as the primary review surface.** The agent's work passes a runnable bar before a human looks at it. Without that bar, every PR is a 1000-line slop dump (the named anti-pattern).
- **Manual agentic testing as a second-pass review.** Playwright traces, `python -c` runs, and Showboat-captured exec/note/image artifacts give the human a *narrative* of what the agent did, not just a diff to read. This is one of Simon's most distinctive contributions — review the *trajectory*, not only the artifact.
- **Linear walkthroughs and interactive explanations as ongoing review of accumulated code.** This treats review as a continuous comprehension activity, not a discrete PR-stage event.
- **Plan-mode-style review (implicit).** Simon uses Claude Code's plan mode in practice (which proposes a plan before touching disk, requiring human approval), and parallel-agent runs serve a similar gating purpose — the human selects among attempts.
- **Eval-driven development.** Simon's evals tag is a substantial body of related writing. His central claim there: "the boring yet crucial secret behind good system prompts is test-driven development. You don't write down a system prompt and find ways to test it. You write down tests and find a system prompt that passes them." He also pushes against waiting for big test suites — "start with small-scale testing right away with a few examples, rather than delaying until you can build more thorough evals." LLM-as-a-judge, in his survey, "worked well" for many evaluation tasks.
- **The StrongDM "satisfaction" pattern.** Simon reports it as a fascinating data point — converting boolean tests into a probabilistic LLM-judged trajectory score — but does not adopt it as a recommended practice. His own review posture remains a human reading agent output through tests, walkthroughs, and manual-testing captures.

## Human leverage techniques

Specific Simon-isms about how a single human stays efficient with agents:

- **"Fire off a prompt anyway."** The cost of trying is so low that the old gating instinct ("not worth the time") is now itself wasteful. Default to attempt.
- **Run a fleet.** Multiple agents, in parallel, in fresh checkouts under `/tmp` (or worktrees). The bottleneck has moved from execution to selection.
- **Use plan mode / planning artifacts.** Approve a plan before code touches disk. Cheap to read, expensive to undo.
- **Use subagents to protect root context.** The parent's context is the scarcest resource; offload exploration.
- **YOLO inside a sandbox.** GitHub Codespaces is his default. The point is to remove permission prompts without absorbing the blast radius.
- **`AGENTS.md`** beats per-task tool config most of the time.
- **Hoard your prompts and recipes.** Don't re-derive the same successful prompt twice; build a personal library.
- **Make the agent narrate its work.** Showboat-captured manual tests, walkthroughs, and interactive explanations are how a human stays cognitively in contact with a codebase that grew faster than they could read.
- **Test-first to give the agent a stopping condition.** This is leverage *for the human* as much as discipline for the agent: it removes the supervisory burden of deciding when the agent is done.

## What doesn't work / pitfalls

Simon is unusually candid here. Aggregated:

1. **Inflicting unreviewed code on collaborators.** The named anti-pattern. A 1000-line PR you didn't run yourself is socially toxic and pollutes the team's review pool.
2. **No-human-review as a default.** Repeatedly characterized as "wildly irresponsible" outside StrongDM's specific niche. LLMs make "inhuman mistakes"; humans need to catch them.
3. **Cognitive debt.** Letting agents build code you no longer understand makes future planning harder and erodes confidence in the system.
4. **Vague specs / no tests.** Without a runnable success criterion, agents will produce something plausible that doesn't actually solve your problem, and you won't notice until it matters.
5. **Skipping the red phase of TDD.** If you don't watch the test fail first, you may have written a test that already passed — proving nothing about the new behavior.
6. **Over-relying on LLM-as-judge / satisfaction scoring as your only quality bar.** Simon reports StrongDM's pattern with admiration but does not adopt it; the implicit warning is that probabilistic acceptance criteria are not yet sufficient on their own for most teams.
7. **Cost denial.** $1k/day/engineer is the StrongDM floor and is not generalizable. If your business doesn't sustain that overhead, the pattern won't sustain you.
8. **Unsandboxed YOLO mode.** Three concrete failure modes: rm-rf-style mistakes, secret/source-code exfiltration, your machine becoming a DDoS hop.
9. **Treating MCP as the answer to tool configuration.** Simon prefers an `AGENTS.md` for most cases; MCP is overkill or under-specified depending on the task.
10. **The "vibe coding" trap.** When you're shipping code for *other people*, vibe coding is grossly irresponsible — they take the hit from bugs, not you. Vibe coding is fine for personal prototypes; agentic engineering is required for production.

## Notable quotes

(All attributed to Simon Willison; I have higher confidence in the StrongDM-post quotations than in some of the guide-page paraphrases.)

1. "An LLM agent runs tools in a loop to achieve a goal." — https://simonwillison.net/2025/May/22/tools-in-a-loop/
2. "Code execution is the defining capability that makes agentic engineering possible." — https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/
3. "How can you prove that software you are producing works if both the implementation and the tests are being written for you by coding agents?" — https://simonwillison.net/2026/Feb/7/software-factory/
4. "If you haven't spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement." — quoted from StrongDM in https://simonwillison.net/2026/Feb/7/software-factory/
5. "I think there's a lot to learn from StrongDM even for teams and individuals who aren't going to burn thousands of dollars on token costs." — https://simonwillison.net/2026/Feb/7/software-factory/
6. "Coding agents are brute force tools for finding solutions to coding problems — if you can reduce your problem to a clear goal and a set of tools that can iterate towards that goal, a coding agent can often brute force its way to an effective solution." — https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
7. "The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that writing code is cheap now." — https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/
8. "Any time your instinct says 'don't build that, it's not worth the time' fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens." — https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/
9. "First run the tests" (the four-word session-opening prompt that "encompasses a substantial amount of software engineering discipline that's already baked into the models"). — https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/
10. "Inflicting unreviewed code on collaborators, aka dumping a thousand line PR without even making sure it works first." — https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/

## Recommended additional sources

These appear in or adjacent to Simon's writing and are worth following up *outside* this report's brief:

1. **StrongDM's own factory site** — https://factory.strongdm.ai/ (Simon links to and quotes them; this is the primary source for spec/scenario/DTU/satisfaction).
2. **Cem Kaner, *Scenario Testing* (2003)** — the intellectual ancestor of StrongDM's "scenario" reuse. Simon names Kaner explicitly via the StrongDM quote.
3. **Andrej Karpathy's original "vibe coding" tweet (Feb 2025)** — Simon repeatedly anchors his agentic-engineering / vibe-coding distinction against Karpathy's coinage.
4. **Anthropic's "Safe YOLO mode" docs for Claude Code** — Simon cites them in "Designing agentic loops" as the canonical reference for sandboxed unattended runs.
5. **Cal Newport / Dan Shapiro on the "Dark Factory" framing** — Simon attributes the "Dark Factory" level-of-AI-adoption framing to Dan Shapiro in the StrongDM post; worth reading the original framing for the levels taxonomy.
6. **Microsoft Playwright** — Simon's recommended substrate for any agent-driven UI testing.
7. **Showboat** (Simon's own tool) — https://github.com/simonw/showboat (inferred location); the artifact format that captures agentic manual testing as reviewable markdown.

## Open questions for synthesis

1. **Where does Simon's "human always reviews" stance reconcile with StrongDM's "no human reviews"?** The synthesis needs to position these as endpoints on a spectrum, with the deciding variables likely being: stakes (security software vs. internal tooling), business margin (can you sustain $20k/engineer/month?), team size (human review scales sublinearly), and verification stack maturity (do you have a DTU-equivalent?).
2. **Is "satisfaction scoring" a complement to or a replacement for human review?** Simon's writing strongly implies complement; StrongDM's writing strongly implies replacement. The factory designer needs to pick one stance per work-stream.
3. **How do Simon's patterns compose with StrongDM's pipeline?** Most of Simon's patterns (red/green TDD, first run the tests, subagents, manual agentic testing, walkthroughs) read like they could *live inside* the StrongDM agent harness without changing StrongDM's outer loop. The factory architecture should likely treat Simon's patterns as the inner-loop methodology and StrongDM's as the outer-loop topology.
4. **What's the right artifact for "the spec"?** Simon endorses tests, markdown specs, `AGENTS.md`, and scenarios. The synthesis needs a default — probably a layered spec (markdown intent + AGENTS.md operational config + tests as machine-checkable acceptance + scenarios as holdout).
5. **How do parallel agents and subagents interact with a multi-human team?** Simon writes for one human + many agents. Scaling to a small team raises questions of context sharing across humans and agents that he doesn't directly address.
6. **Cognitive-debt patterns at team scale.** Linear walkthroughs and interactive explanations are personal practices in Simon's framing. The factory needs a mechanism that makes them *team artifacts* — versioned, discoverable, and authoritative.
7. **The Every.to "compound engineering" framing vs. Simon's "agentic engineering."** Simon does not directly engage with Every.to in the sources I covered. The synthesis should locate them: Every.to leans into role specialization across multiple agent personas; Simon leans into one engineer leveraging their own expertise via an agent fleet. These are different bets on where the leverage lives.
8. **Cost as a first-class architectural constraint.** Simon's $1k/$20k framing should anchor any factory design. A factory architecture that requires StrongDM-level token spend to function is a different product than one that targets a 10x-cheaper budget envelope.
