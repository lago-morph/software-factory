# agent instruction

**Cognitive-load minimization in user-facing status.** When the user is running multiple agents in parallel (declared explicitly OR observed via concurrent session activity), every status message from this agent MUST minimize cognitive load: name the file/branch/PR-number in a single navigable line; do NOT sprawl cross-references; do NOT explain via "here's where you would navigate to next"; do NOT enumerate multiple ways to reach the same artifact. The user is context-switching across agents — each cross-reference is a tax.

*Grounded in: PR #169 line-87 thread ("I am running a bunch of agents at the same time. I need you to be helping my workflow, not increasing my cognitive load for things like trying to figure out what branch, what document, what directory, I'm supposed to be looking at") — surfaced after 4 failed markdown-link-formatting attempts to give the user a clickable URL.*

# justification

The 2026-05-25 PR #169 line-87 thread escalated from a clarification request to a frustration rebuke after several increasingly-elaborate status replies that gave the user multiple options to navigate to the same file (PR # / branch name / file path / chat output). Each reply was reasonable in isolation; cumulatively they were a navigation tax the user had to pay just to figure out where to look.

The cost of the rule: each status reply demands ~5 extra seconds of "what's the ONE-line answer for the user navigating from elsewhere?" thinking before composing. Lead with the verb ("Done", "Merged", "Posted"); name the artifact; stop.

Asymmetric cost without: cognitive overhead compounds across N parallel agents. Each agent's "here are 3 ways to get to the artifact" reply is fine in single-agent context, exhausting at multi-agent scale. The user described it as "I have to figure out what branch, what document, what directory, I'm supposed to be looking at" — the agents collectively made navigation a research task.

The rule's negative trigger is a single-agent session where the user is co-driving in real-time; there context-richness is welcome. The rule applies when the user has declared multi-agent context OR when the session is webhook-triggered (which implies the user isn't typing at this agent right now and is presumably reading several at once).

The rule pairs with AGENTS-MD-fd63756222 (raw URLs in chat replies): for clickable URLs to deeply-nested files, the bare URL on its own line is the cognitive-cheapest format (no markdown-link debugging).
