[ Home ](/) [GitHub ](https://github.com/addyosmani) [Press ](/press) [Biography ](/bio) [LinkedIn](https://www.linkedin.com/in/addyosmani/) [Twitter ](https://twitter.com/addyosmani) [Newsletter](https://addyo.substack.com) [Blog ](/blog)

# Agentic Engineering

## February 4, 2026

A year ago, Andrej Karpathy coined “vibe coding” to describe a gleefully reckless way of programming: you prompt, hand the keyboard to an AI, accept everything it spits out, don’t read the diffs, iterate by pasting error messages back in. It was a great label for a real thing - building quick prototypes or MVPs on pure AI autopilot.

The problem is that “vibe coding” has become a suitcase term. People now use it to describe everything from a weekend hack to a disciplined engineering workflow where AI agents handle implementation under human oversight. These are fundamentally different activities, and conflating them is causing real confusion - and real damage.

## **What vibe coding actually is**

Vibe coding means **going with the vibes** and **not reviewing the code**. That’s the defining characteristic. You prompt, you accept, you run it, you see if it works. If it doesn’t, you paste the error back and try again. You keep prompting. The human is a prompt DJ, not an engineer.

This is genuinely useful for:

  * **Greenfield MVPs, prototypes and hackathon demos.** You need something working by Sunday. Code quality is irrelevant.
  * **Personal scripts and one-off tools.** You’re the only user. If it breaks, you regenerate it.
  * **Learning and exploration.** Newcomers can build things they couldn’t otherwise, learning by example from the AI’s output.
  * **Creative brainstorming.** Deliberately over-generating to see what approaches the AI suggests, then throwing it away and building properly.



If vibe coding gives millions of people the ability to create custom software who otherwise couldn’t, that’s a genuine win. The technique has a legitimate place in the toolbox.

But the failure modes are well-documented at this point. The pattern is always the same: it demos great, then reality arrives. You try to modify it, scale it, or secure it, and you discover nobody understands what the code is actually doing. As one engineer put it, “This isn’t engineering, it’s hoping.”

## **We need a better term for the professional version**

Here’s the thing: a lot of experienced engineers are now getting massive productivity gains from AI - 2x, 5x, sometimes more - while maintaining code quality. But the way they work looks nothing like vibe coding. They’re writing specs before prompting. They’re reviewing every diff. They’re running test suites. They’re treating the AI like a fast but unreliable junior developer who needs constant oversight. I’ve personally liked “AI-assisted engineering” and have talked about how this describes that end of the spectrum where the human remains [in the loop](/agentic-engineering/human-in-the-loop/).

Simon Willison (whose work I adore) proposed “[vibe engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/)” for this - it reclaims “vibe” while adding “engineering” to signal discipline. But after watching the community debate this for months, I think the the word “vibe” carries too much baggage. It signals casualness. When you tell a CTO you’re “vibe engineering” their payment system, you can see the concern on their face.

Andrej Karpathy suggested “[agentic engineering](https://x.com/karpathy/status/2019137879310836075)” this week and I think I like it.

Here’s perhaps why it works:

**It describes what’s actually happening.** You’re orchestrating AI agents - coding assistants that can execute, test, and refine code - while you act as architect, reviewer, and decision-maker. You might write only a % of the code by hand. The rest comes from agents working under your direction. That’s agentic. And you’re applying engineering discipline throughout. That’s engineering.

**It’s professionally legible.** “Agentic engineering” sounds like what it is: a serious engineering discipline involving autonomous agents. You can say it to your VP of Engineering without embarrassment. You can put it in a job description. You can build a team practice around it.

**It draws a clean line.** Vibe coding = YOLO. Agentic engineering = AI does the implementation, human owns the architecture, quality, and correctness. The terminology itself enforces the distinction.

## **What agentic engineering looks like in practice, perhaps.**

The workflow isn’t complicated, but it requires discipline that vibe coding explicitly abandons:

**You start with a plan.** Before prompting anything, you write a design doc or spec - sometimes with AI assistance. You break the work into well-defined tasks. You decide on the architecture. This is the part vibe coders skip, and it’s exactly where projects go off the rails.

**You direct, then review.** You give the AI agent a well-scoped task from your plan. It generates code. You review that code with the same rigor you’d apply to a human teammate’s PR. If you can’t explain what a module does, it doesn’t go in.

**You test relentlessly.** The single biggest differentiator between agentic engineering and vibe coding is testing. With a solid test suite, an AI agent can iterate in a loop until tests pass, giving you high confidence in the result. Without tests, it’ll cheerfully declare “done” on broken code. Tests are how you turn an unreliable agent into a reliable system.

**You own the codebase.** You maintain documentation. You use version control and CI. You monitor production. The AI accelerates the work, but you’re responsible for the system.

Teams doing this well often report faster development - and those gains come from augmenting a solid process, not abandoning one. The AI handles boilerplate and grunt work. The human focuses on architecture, correctness, edge cases, and long-term maintainability.

The irony is that AI-assisted development actually rewards good engineering practices more than traditional coding does. The better your specs, the better the AI’s output. The more comprehensive your tests, the more confidently you can delegate. The cleaner your architecture, the less the AI [hallucinates](/agentic-engineering/hallucination/) weird abstractions. As one analysis noted, “AI didn’t cause the problem; skipping the design thinking did.”

## **The skill gap we’ve discussed**

Here’s an uncomfortable truth from the trenches: agentic engineering disproportionately benefits senior engineers. If you have deep fundamentals - you understand system design, security patterns, performance tradeoffs - you can leverage AI as a massive force multiplier. You know what good code looks like, so you can efficiently review and correct AI output.

But if you’re junior and you lean on AI before building those fundamentals, you risk a dangerous [skill atrophy](/agentic-engineering/skill-atrophy/). You can produce code without understanding it. You can ship features without learning why certain patterns exist. Several engineering leaders have flagged this as an emerging crisis: a generation of developers who can prompt but can’t debug, who can generate but can’t reason about what they’ve generated.

This isn’t an argument against AI-assisted development. It’s an argument for being honest about what it demands. Agentic engineering isn’t easier than traditional engineering - it’s a different kind of hard. You’re trading typing time for review time, implementation effort for orchestration skill, writing code for reading and evaluating code. The fundamentals matter more, not less.

## **Where we go from here**

The trajectory is clear: AI agents are getting more capable, and the agentic engineering workflow is becoming default for a growing number of professional developers. This is going to accelerate.

We need:

  * **Honest terminology.** Call it agentic engineering when you mean disciplined, agent-assisted development with human oversight. Call it vibe coding when you mean the fun, reckless, prototyping-only version. Stop using one term for both.
  * **Better evaluation frameworks.** We need systematic ways to measure whether AI-assisted workflows are actually producing reliable software, not just faster software.
  * **Investment in fundamentals.** As AI handles more implementation, the premium on architectural thinking, security awareness, and systems design goes up, not down. Training programs need to adapt.



The rise of AI coding doesn’t replace the craft of software engineering - it raises the bar for it. The developers who’ll thrive aren’t the ones who prompt the fastest. They’re the ones who think the clearest about what they’re building and why, then use every tool available - including AI agents - to build it well.

Vibe coding showed us what’s possible when you drop all conventions.

Now it’s time to bring the engineering back. Let’s call that what it is.

* * *

_I’ve written a new book with O’Reilly,[Beyond Vibe Coding](https://beyond.addy.ie/), that goes deeper into practical frameworks for AI-Assisted (and agentic) engineering. If you’ve been figuring this out in your own workflow, I’d love to hear what’s working._

[ Addy Osmani is a Software Engineer at Google working on Google Cloud and Gemini. ](http://twitter.com/addyosmani) [ Tweet](https://twitter.com/intent/tweet?text=https://addyosmani.com/blog/agentic-engineering/ - Agentic Engineering by @addyosmani) [ Bluesky](https://bsky.app/intent/compose?text=Agentic Engineering - https://addyosmani.com/blog/agentic-engineering/) [ Mastodon](https://mastodon.social/share?text=Agentic Engineering%0Ahttps://addyosmani.com/blog/agentic-engineering/) [ Threads](https://www.threads.net/intent/post?text=Agentic Engineering%0Ahttps://addyosmani.com/blog/agentic-engineering/) [ LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://addyosmani.com/blog/agentic-engineering/) Share

Want more? Subscribe to my free newsletter:
