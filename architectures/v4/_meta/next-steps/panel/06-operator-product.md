# Panel review 06 — operator / product / cognitive-load advocate

> Reviewer 6 of 6. I speak for the human principal (jonathan@manton.com), a
> non-coder whose real goal is **building `agent-os`**, with the factory only as
> the means. Plan under review: [`10-unified-plan.md`](../10-unified-plan.md).
> Grounding: [`00-grounding-and-exemplar.md`](../00-grounding-and-exemplar.md).

## 1. Verdict

**`accept-with-named-amendments`.**

The plan keeps the operator's real goal genuinely load-bearing, not bolted on.
Every gate's exit criterion ships or measures something against real `agent-os`
work: Gate 0 ships a B22 design draft, Gate 3 ships "a real passing B12 repo,"
Gate 5 exits on "3–4 more factory-built `agent-os` components in their repos"
([`10-unified-plan.md` §2](../10-unified-plan.md)). That is exactly the A0 framing
— "point the factory at agent-os's own backlog"
([§A0](../00-grounding-and-exemplar.md)) — made operational. Success is defined in
terms the operator cares about (components shipped), not internal factory vanity
metrics. So I do not reject.

But three things will unpleasantly surprise the operator, and they are fixable
without rewriting the plan. Hence: accept *with amendments*.

## 2. Top three named amendments

**A. The plan never names a number the operator must personally set — yet it
hides one in plain sight.** Gate 1's exit says the judge must "clear a stated
bar" and that "the bar value and sample size are operator policy `[PROPOSED — not
in source]`" ([§2 Gate 1](../10-unified-plan.md)). That is the single most
consequential decision in the whole 2–3 weeks — it gates whether `tri_alignment`
is ever trusted — and it is buried in a parenthetical as the operator's job, with
no recommended default. The decisions doc models the right pattern: every item
carries "my recommendation (clearly marked as opinion)"
([`decisions-to-make.md` intro](../../../../decisions-to-make.md)). *Fix:* add a
short "Decisions only you can make" box up front, listing the false-green bar +
sample size with a recommended starting value, the same way decision #1/#2/#4 are
surfaced. Why it matters: the operator cannot drive Gate 1 without it, and right
now they would hit Gate 1 and stall, not knowing a decision was waiting for them.

**B. The jargon load at the front door is too high for a non-coder.** A7 is
explicit: the reader "does not write code… plain language, no unexplained jargon,
every local term translated on first use"
([§A7](../00-grounding-and-exemplar.md)), and vocabulary lock-in (cities, rigs,
formulas, beads…) is named as "real cognitive load"
([§A6](../00-grounding-and-exemplar.md)). The unified plan's one-paragraph version
(§0) opens with `judge_self_trust = uncalibrated`, PF-2, C46, C32 OQ6, `root_cause`
corner — five undefined terms in three sentences. The plain-English build order
proves the bar is achievable: it explains the same machinery with zero raw
component codes ([`build-order-plain-english.md`](../../../../build-order-plain-english.md)).
*Fix:* precede §0 with a five-line plain-language gloss (instrument = the test
that scores a build; calibrate = check the scorer against human judgement before
trusting it; the fence = the safety guardrail), and translate each term on first
use. Why it matters: §0 is the paragraph the operator actually reads; if it reads
as spec-ese, they lose the thread on page one.

**C. Week 3 holds a starvation surprise that is stated as a risk, not as a plan.**
Risk #3 admits "after ~6–8 B-components, the highest-value `agent-os` work is
twin-gated" ([§5](../10-unified-plan.md)), and Gate 5 already marks B3's
Chainsaw/ArgoCD layer and B16/B6 runtime halves as twin-gated
([§2 Gate 5](../10-unified-plan.md)). So the operator's honest week-3 experience is:
the clusterless backlog runs dry and the line stops. The plan frames this as "a
*good* problem" — correct intellectually, but the operator will feel it as "we ran
out of things to build." *Fix:* state in Gate 5's exit that the expected and
*intended* outcome is hitting the twin wall, and that the deliverable when it
hits is a one-page "twins are now the next factory-build" decision brief (twins
are already named the near-certain next build, [§4](../10-unified-plan.md)). Make
the wall a planned milestone, not a risk that "happens to" the operator.

## 3. The single biggest mismatch

**The plan's center of gravity is *validating the instrument*, but the operator's
center of gravity is *shipping `agent-os` components*.** Two of the first three
gates (Gate 1 calibration, Gate 2 holdout) produce no `agent-os` software — only a
"judge false-green rate" and a "holdout-integrity verdict"
([§2](../10-unified-plan.md)). The reasoning is sound (an uncalibrated instrument
makes every shipped component a lie, [§0](../10-unified-plan.md)) and I do not want
it removed. But to the operator it reads as: week 1 is mostly factory plumbing, and
the first real code component (B12) doesn't ship until Gate 3 — a *felt*-progress
gap. Amendment C (and shipping B22 at Gate 0, which the plan does well) partly
absorbs it, but the plan should say out loud, near the top: "weeks 1–2 earn the
right to trust the factory; the agent-os component count climbs from Gate 3 onward."

## 4. What the plan gets right and must be preserved

- **The agent-os connection is genuine, not decorative.** Real components (B22,
  B12, B3, B16, B6, B9), real specs, real repos, real exit criteria
  ([§2](../10-unified-plan.md)) — preserve this end to end.
- **"One trustworthy nail, then the line"** ([§1](../10-unified-plan.md)) is the
  right operator-facing sequencing: it refuses to scale a process the operator
  can't yet trust, which protects the operator from a confident-but-wrong factory.
- **Honesty about uncertainty.** "Unproven by construction" ([§0](../10-unified-plan.md))
  and the accepted fail branch ("the factory needs more substrate before Phase 3,"
  [§2 Gate 3](../10-unified-plan.md)) mean the operator will not be sold a false
  green. That candor matches the decisions doc's tone and must survive editing.
- **Gates, not day-counts** ([§2](../10-unified-plan.md)), honoring A7's "no
  fabricated time estimates" — keep.
