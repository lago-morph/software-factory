# agent instruction

**Grep before recall when asked whether prior session work covered a topic.** When the user asks "did I do X?" or "does the prior analysis cover Y?", answer by running `grep` / `Read` against the actual file, not by reconstructing from session memory. Session memory after 50k+ tokens is unreliable; grep is one tool call. If the answer is "yes but in a different section than expected," point to the actual section and cite the lines.

*Grounded in: PR #101 follow-up Q1 — answered "did the gas city deep-dive include pack composability examples?" by grep + targeted Read, not by memory.*

# justification

After PR #101 merged, the user asked whether the Gas City deep-dive covered pack composability with examples. The session had been running ~60k tokens deep, with two ~10k-word subagent outputs in scrollback. Reconstructing "did the analysis cover X" from memory at that depth is unreliable — the boundary between "I saw a section like that" and "I added that to the synthesis report instead" blurs.

The cheap and correct move was: `grep -nE "pack|Pack" research/followup/13-gas-city-deep-dive.md | head -40`, followed by a targeted `Read` of the two sections most likely to be relevant (§4 Pack Composition, §14 Pack Ecosystem). That produced a precise, citation-rich answer in ~2 tool calls: the deep-dive covers the mechanics in §4 and §14; the use-case scenarios live in the synthesis report §4 and §5; here are the line numbers. The user got verifiable structure instead of "yes I think we covered it."

The marginal cost is one grep + one targeted Read — under a minute. The cost of recall-from-memory is either confidently-wrong assertions (which the user can catch but then loses trust) or hedged "I think we covered it" responses (which force the user to grep anyway). The discipline generalises far beyond the retrospective context — any time the user asks a question whose ground truth is on disk, the right answer pulls from disk.
