# Adversarial reviewer angles — ready-to-use menu

A non-exhaustive catalog of reviewer angles to dispatch when running adversarial review on a decision brief, design proposal, plan, or other lead-agent artifact. Per the autonomous-run skill, **≥3 real subagent reviewers per round**, **2 rounds minimum** for substantive decisions.

Pick from this list, or invent angles specific to the brief. The goal: independent attacks from different directions so the brief is pressure-tested rather than rubber-stamped.

---

## Core angles (general-purpose; usable on almost any brief)

- **Skeptic / contrarian methodologist** — "What assumptions am I making?" Challenges premises rather than implementations.
- **Red-teamer** — Attacks the strongest claims of the brief using corpus / project evidence. Looks for the worst-case failure mode.
- **Pre-mortemer** — "6 months later, this decision failed. Why?" Generates the failure-cause story before the failure happens.
- **Cost/scope hawk** — Is the chosen option's cost / scope justified? Could a cheaper or smaller-scope variant achieve equivalent outcome?
- **Plan-shape minimalist** — Could this be done with fewer artifacts / fewer steps / fewer subagents without losing rigor?
- **Naive newcomer** — Identifies jargon, hidden anchors, smuggled-in assumptions, places the brief assumes context the reader doesn't have.

## Discipline-specific angles

- **Scoping-principle skeptic** — Does the decision honor or covertly weaken the project's scoping principle (whatever that is — preserving candidates, retaining alternatives, etc.)?
- **Methodology-purist** — Is the brief consistent with the project's methodology / framework / design philosophy? Or does it sneak in expedient deviations?
- **Buildability-rule enforcer** — Does the brief's construction path actually satisfy the project's buildability bar (e.g., named tool + integration sentence; corpus citation; etc.)?
- **Single-source-of-truth enforcer** — Does the brief introduce a list / config / convention that violates the project's SSOT discipline?
- **Backwards-compatibility auditor** — Does the brief break prior assumptions, contracts, or artifacts in ways the brief doesn't address?

## Regulatory / external-perspective angles

- **Regulator** — Compliance / audit / liability lens. Would an external auditor accept this decision's documentation?
- **10-year on-call engineer** — Maintainability, debuggability under pressure. Will the next person inheriting this be able to operate it?
- **Domain practitioner** — Does this actually ship value, or just produce artifacts that look like value?
- **Historian / prior-art auditor** — What earlier work / prior art did the brief miss? Where's the corpus thin?

## Cross-cutting angles for synthesis / candidate-set work

- **Splitter** — "Everything is different; over-sharing is the bug. These primitives / candidates / artifacts should NOT collapse."
- **Lumper** — "Everything is the same; over-splitting is the bug. These primitives / candidates / artifacts should collapse."
- **Cross-mandate advocate** — "This works for the OTHER mandate / use case too — find the case the brief missed."
- **Cross-mandate attacker** — "This CANNOT work for the other mandate / use case — find why the brief is wrong to claim it can."
- **Anchor-detector** — Reads the brief and flags places where independent prior artifacts suspiciously agree (suggests they inherited the same prior anchor).
- **Silent-absorption auditor** — Compares the brief's output to archived / superseded artifacts; flags content that leaked in unintentionally.

## Quality-control angles for design / spec work

- **Cell-defender / cell-attacker** — For any matrix the brief proposes, defend or attack specific cells. Every "both" cell, every "n/a" cell, every "designed-system" cell gets at least one attack.
- **Alternatives advocate** — Argue for the strongest alternative to the brief's chosen option. If the brief can't defend, it goes back for revision.
- **Falsification designer** — Names the result that would falsify the brief's central claim. If the brief can't articulate a falsifying outcome, it's too soft.
- **Hypothesis-falsifier** — For a brief that's testing a hypothesis, names in advance the result pattern that would falsify it (prevents post-hoc reinterpretation).

## Process / governance angles

- **Process-skill triggers auditor** — Does the brief require a process skill (issue-management, always-commit, etc.) that hasn't been loaded? Per AGENTS.md, all process skills must be loaded eagerly.
- **Audit-trail-integrity reviewer** — Does the brief's commit / branch / PR structure preserve a clean audit trail? Or does it bury rewind points where the user can't find them?
- **Context-window hawk** — At what stage of an autonomous run does this brief land? Will the reviewer subagents have enough budget to do their job?

## Selecting angles per round

**Round 1** typically benefits from 3 *different* core angles — e.g., skeptic + hawk + buildability-enforcer. These catch the lead agent's initial blind spots.

**Round 2** should use *different* angles from Round 1 (where possible) to avoid Round-2 reviewers inheriting Round-1's framing. Good Round-2 angles: regulator + on-call + cross-mandate-attacker (if Round 1 was core angles); or splitter + lumper + cell-defender (if Round 1 was discipline angles).

**Don't repeat angles across rounds** unless you have a specific reason — Round-2's value is bringing *new* attack vectors, not re-running the same attack with a fresh subagent.

## Anti-patterns

- **All Round-2 angles same as Round 1** — Round-2 inherits Round-1's framing; the second round adds little.
- **Angles that are too similar to each other in one round** — three skeptics is one skeptic with redundancy.
- **Angles incompatible with the brief's surface** — e.g., dispatching a "regulator" reviewer on a brief about subagent dispatch shape; the reviewer has no surface to attack.
- **Inventing a "supportive" reviewer angle** — every reviewer is adversarial. There are no "supportive" reviewers; if you want validation, the brief itself should provide it.
