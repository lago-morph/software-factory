# Spec: `conversational-adjudication-for-stuck-decisions`

- **ID**: SKILL-SPEC-ee35b95172
- **Source retrospective**: ../2026-05-25-180.md

## Intent

When a decision brief presents A/B/C options and the user wants discussion rather than a vote, dispatch the conversation through chat (not subagents) until both parties converge, then post the agreed-on outcome as a resolution comment on the brief PR so the durable record captures the decision. Conversations are for surfacing missing frames (e.g., the substrate/methodology/discipline layering question that emerged from the 2026-05-25 plain-language brief discussion), not for swapping options. In that session, the user's "I want to engage with you on them to figure out the best solution" reply opened a 5-question dialogue that converged on Option A by clarifying the ADR-vs-architecture-spec scope distinction — material that wasn't in the original brief but turned out to be the decisive frame.

## Trigger

Activate when, after the agent posts a decision brief, the user replies:
- "I want to discuss"
- "Let me brainstorm with you"
- "I want to engage with you on them"
- "Help me think through this"
- Asks substantive questions about the brief's framing rather than picking an option
- Any semantic equivalent expressing "talk this through with me"

Negative trigger: a user replying "A" / "B" / "C" / "go with your recommendation" — that's a direct adjudication, not a conversation request.

## Inputs

- The decision brief (already posted).
- The user's discussion-opening reply with whatever questions they raised.
- The underlying analysis material the brief was drawn from (for confirming claims under conversational pressure).

## Outputs

- A multi-turn chat conversation (no subagent dispatches in the conversation itself; this is direct user-agent exchange).
- A resolution comment on the brief PR capturing: the decision converged on, the substantive frames that surfaced during conversation that weren't in the original brief, the user-agreed reasoning.

## Workflow

1. Read the user's discussion-opening reply for: (a) what questions are raised; (b) which questions challenge a brief framing vs. which ask for more detail.
2. Identify the frames the brief implicitly assumed but didn't state. The user's questions are usually probing one of these (e.g., "are ADRs supposed to be architecture description AND parameter? — that probes the substrate/methodology/discipline layering frame).
3. Answer each question substantively in one reply. For each:
   - Acknowledge the question explicitly (don't paraphrase past it).
   - Surface the missing frame the user is probing.
   - Re-frame the original brief's content in light of the new frame.
   - Concede where the user's pushback shifts your view; do NOT over-defend.
4. End the reply with a clear "this is unchanged from my original recommendation" OR "this shifts my view to <new option>" statement, with reasoning.
5. Invite continued conversation — "What would help me close this out is your view on X, Y" — explicitly. Don't push for a decision.
6. Iterate until the user says "I support the revised view" / "we converged" / "go with X" or equivalent.
7. Once converged, post a resolution comment on the brief PR with:
   - The decision (Option N or "no change").
   - 3-5 substantive bullets from the conversation that sharpened the brief.
   - Any caveats / known limitations.
8. Note any new frames worth codifying as ADRs or AGENTS-MD rules in the next retrospective.

## Concrete examples

### Example 1: 2026-05-25 PR #172 conversation

After PR #172 posted, user replied with 6 substantive questions: P-25/P-27 parameterization concerns, P-24 ADR-split question, "do ADRs contain methodology decisions?", P-30 risk statement confusion, "could we follow the P-30 pattern for P-25/P-27?", explicit "I want to engage with you on them". The agent's reply: (a) named the three-layer ADR model (substrate / discipline / methodology decisions) — the missing frame; (b) re-framed P-25/P-27 under that frame (parameterization is architecture-spec content); (c) noted P-24's "more involved structure" concern was already addressed by ADR 0047 P-26 separation; (d) conceded the P-30 risk statement was overstated; (e) explained why P-30 IS the right asymmetric case (structural divergence). Closed with "I'm not converging until you're satisfied". User replied "we have converged on understanding and intent. I like your revised lead-agent view." Resolution comment posted on PR #172.

### Example 2: Hypothetical Phase-6 mandate-fit matrix shape

User asks "should it be one matrix or per-candidate row?" with discussion-opening phrasing. The agent responds with the implicit frame (the matrix's purpose is cross-candidate comparison; one shared matrix is the design intent, per-candidate rows defeats it). User says "but the per-candidate matrices give each candidate's spec author room to argue mandate-fit independently". The agent surfaces the frame: cross-candidate comparison VS per-candidate argumentation. Re-frames: argue mandate-fit independently is the spec body's job; the matrix is the comparison. Converges on a shared matrix authored at Phase-6 close + each spec's mandate-fit argument lives in its own body.

## Anti-patterns

- **Treating the conversation as a vote.** "OK so are you picking A or B?" pushes the user to vote before they've finished exploring. Let the conversation run; the convergence is on the FRAME, not the option.
- **Defending the original brief over-vigorously.** The user is engaging because they think there's something worth probing. Conceding where they're right is the whole point.
- **Forgetting to post the resolution comment.** The chat conversation is ephemeral; the PR comment is durable. Without it, the next reader sees "PR #172 was opened, no decision recorded".
- **Spawning subagents during the conversation.** The conversation is direct user-agent exchange. Dispatching adversarial reviewers mid-conversation breaks the flow and the user's expectation that they're talking to the agent.

## Acceptance criteria

- [ ] Conversation lasts ≥2 user-agent exchanges (otherwise it wasn't a real conversation; the user just adjudicated).
- [ ] A frame not in the original brief surfaces during conversation.
- [ ] Resolution comment posted on the brief PR with: decision + 3-5 substantive bullets + caveats.
- [ ] Any new frame worth codifying is noted for the next retrospective.

## Files this skill creates / modifies

- The decision brief PR's comment thread — adds a resolution comment.
- The next retrospective — adds proposals for any frame-level lessons that surfaced.
