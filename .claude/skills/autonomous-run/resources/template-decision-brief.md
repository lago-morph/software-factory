# auto-NNN — `<short slug>`

**Author.** Lead agent, autonomous-run session `<YYYY-MM-DD>`.
**Status.** `Round 1 in flight` / `Round 2 in flight` / `Decided after Round 2` / `Decided after Round N (>2)`.
**Rewind point.** Commit `<SHA-or-TBD>` on branch `<branch>`. Reverting it returns the project to `<state>`; the morning user can re-adjudicate.

---

## Question

One paragraph stating the decision precisely. Name the artifact / phase / candidate / primitive the decision affects. Avoid loaded framings.

## Alternatives considered

At least 3 options. For each:

### Option A — `<name>`

- Description (one paragraph).
- **Pros.** Bulleted.
- **Cons.** Bulleted.

### Option B — `<name>`

- Same structure.

### Option C — `<name>`

- Same structure.

(Add Options D, E… if natural; do not invent weak alternatives just to fill the list.)

## Decision (Round 1 — write before any adversarial review)

**Selected: Option `<X>`.**

Reasoning:

- Numbered list of why this option dominates.
- Cite specific evidence (file paths, F-ids, corpus references) wherever possible.

## Downstream impact

- **Phase N.M:** `<concrete change>`.
- **Phase N+1.M:** `<concrete change>`.
- (Continue per affected phases / artifacts.)

## If-user-overrides rewind point (Round 1)

Specific commit SHA to revert. What survives the revert (so the user knows what they keep) and what gets restored (so they know the prior state).

---

## Adversarial-review round 1

Per [`AGENTS.md` `AGENTS-MD-d72e1a4f3c`](../../../../../AGENTS.md#adversarial-review-must-be-real-subagents) and the autonomous-run skill, dispatched ≥3 real adversarial reviewer subagents. **Inline-simulated reviewers are forbidden.**

### Reviewer angles dispatched

(Pick from [`resources/adversarial-reviewer-angles.md`](adversarial-reviewer-angles.md) or invent new ones if the brief needs them.)

- Reviewer 1: `<angle>` — `<one-line goal>`.
- Reviewer 2: `<angle>` — `<one-line goal>`.
- Reviewer 3: `<angle>` — `<one-line goal>`.
- (Add reviewers as needed.)

### Findings (after reviewers return)

For each reviewer, summarize their main objection in 1-3 paragraphs. Cite specific evidence they brought (file paths, line numbers, counter-examples). Distinguish:

- **Strong objections that change the decision** — these convert Round-1 to `superseded` and produce a Round-2 revision.
- **Amendments that strengthen the decision without changing the option** — fold into the revised brief.
- **Weak objections / accepted as-is** — record briefly but do not block.

### Verdict status (per reviewer)

- Reviewer 1: `accept as-is` / `accept with amendments` / `reject and switch option`.
- Reviewer 2: same.
- Reviewer 3: same.

---

## Decision (Round 2 — revised after Round 1)

If Round-1 reviewers converged on `accept as-is` and all engaged the hardest objection: **mark Round 2 skippable, decision is final.** (Rare; usually only for low-stakes decisions where Round-1 reviewers don't surface significant amendments.)

Otherwise:

**Revised selected: Option `<Y>`** (or Option `<X>` with amendments).

Reasoning for the change (or for the strengthened option):

- Numbered list of how Round-1 findings reshape the decision.
- Explicit statement of which Round-1 amendments are folded in and which are recorded-but-not-adopted.

### Revised downstream impact

(Update per affected phases.)

### Revised if-user-overrides rewind point

(Specific commit SHA + what survives / restores.)

---

## Adversarial-review round 2

Dispatched ≥3 MORE real adversarial reviewer subagents on the **revised brief**. Round-2 reviewers must read the revised brief cold; do not include Round-1 transcript in their context (this prevents Round-2 from inheriting Round-1's anchoring).

### Reviewer angles dispatched

- Reviewer 4: `<angle>`. (Different from Round 1 where possible.)
- Reviewer 5: `<angle>`.
- Reviewer 6: `<angle>`.

### Findings

(Same structure as Round-1 findings.)

### Verdict status

- Reviewer 4: `accept as-is` / `accept with amendments` / `reject and switch option`.
- Reviewer 5: same.
- Reviewer 6: same.

---

## Final decision (after Round 2)

If Round-2 reviewers `accept as-is` (unanimously, or with only weak amendments): **decision is final.**

If Round-2 reviewers converge on another change: **mark Round 2 superseded, write Round 3.** (Should be rare. If you find yourself writing Round 3, consider whether the question itself is malformed — sometimes the right answer is to re-frame the question rather than keep iterating the option choice.)

State the final decision in one sentence at the top: **"Final: Option `<Z>`, decided 2026-MM-DD after `<N>` rounds of adversarial review."**

---

## Notes on Round count

The autonomous-run skill mandates two rounds minimum for substantive decisions. Round 1 catches the lead agent's initial blind spots; Round 2 catches the revised brief's blind spots. Round 3+ is allowed but should be rare — if you can't converge in two rounds, the question is likely malformed.

Skipping Round 2 is acceptable only when:

1. Round-1 reviewers all return `accept as-is`.
2. Each Round-1 reviewer demonstrably engaged the hardest objection (not just surface ones).
3. The decision is reversible at low cost if Round-2-style objections surface later.

If any of those three fail, run Round 2.
