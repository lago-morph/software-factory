# Decisions from this run — in plain language

**What this is:** every decision this overnight session touched, written for you, not for the machine. Two of them need your call; the rest I either made with a clear undo path or you'd already made up front. Skim the table, then read the two at the top.

A few terms, defined once (all from material you've read):

- **The factory** — the whole system: a written spec goes in, working software comes out; a separate stream of held-out tests measures how good the result is; a self-healing loop turns failures into fix-tasks.
- **Gas City** (the `gc` runtime) — the off-the-shelf runtime the factory sits on (Steve Yegge's "Gas Town" lineage). A working prototype of it now exists in a sandbox like this one.
- **The fence** — the factory labels every action by whether it touches production, an isolated sandbox, or a fake stand-in, and refuses the dangerous combinations. It's the defence against Willison's *lethal trifecta* (read private data + take in untrusted text + send data out, all at once).
- **Block vs. notice** — a safety control can either *block* a bad access in the moment, or *notice* it in the audit afterward. Blocking is strictly stronger.
- **The autonomy ladder** — El Kaim's framing, from fully manual up to lights-out. "Human-in-the-loop" means a person reviews batches; "lights-out" means nobody does.

## At a glance

| # | The decision | Who | Status |
|---|---|---|---|
| 1 | If the runtime only *notices* bad access instead of *blocking* it, does that **stop** unattended running until fixed? | **You** | **Needs your call** (my rec: yes, stop) |
| 2 | Can the **safe parts** of the factory run unattended even before that's settled? | **You** | **Needs your call** (my rec: yes) |
| 3 | Prepare the Gas City test rather than run a live factory overnight | You (up front) | Settled |
| 4 | Do the full build-detail run (not just the test) | You (up front) | Settled |
| 5 | Stack the work as several small pull requests | You (mid-run) | Settled |
| 6 | Four small naming/wiring fixes between the data components | Me (from review) | Settled (housekeeping) |
| 7 | Fold the prototype's verified facts into the specs | Me | Settled (informational) |

---

## 1. If the runtime only *notices* instead of *blocks*, does the factory stop?

**This is the big one, and it's yours.**

**Background.** You already decided to put the fence up *before* the factory runs unattended. But a fence only works if the runtime actually *blocks* the dangerous combination at the moment it's attempted. If Gas City only *notices it afterward*, the fence is a sign, not a wall — and nobody has tested which one Gas City does yet (the prototype skipped that test to save token spend). I wrote the test; it just needs a machine with Docker.

**The decision.** Not *which way Gas City behaves* — that's a fact we'll go get. The decision is *what the plan does about each possible answer.* I settled it as a rule, after two rounds of adversarial review:

> If the runtime only notices instead of blocks, the factory **does not run unattended** — it stays at human-in-the-loop review — until either the runtime is shown to block, or someone makes a deliberate, costed case for adding a blocking layer. We don't pre-approve building one.

**Why a rule, not an answer.** Pre-deciding the test's result is exactly the mistake the project is built to avoid ("verify the substrate, don't assume it"). So the rule says *here's how we'll judge whatever the test finds*, and — importantly — it **fails safe**: if the test can't be run, or comes back ambiguous, we treat it as "doesn't block" and keep a human in the loop. Better to be too cautious than to run unattended behind a fence that isn't really there.

**What happened in review (worth knowing).** My *first* draft answered "if it only notices, we build our own blocking layer." Three reviewers independently shot that down: building custom blocking (sandbox syscall filters, network policy, and so on) is precisely the hardening you told the whole project to drop and let the existing stack handle. The second draft removed it. I kept the struck-out first version in the record so you can see the reasoning move.

**The options, plainly:**

| Option | What it means | Trade-off |
|---|---|---|
| **A — Stop (my rec)** | A "notice-only" runtime blocks unattended running until it's fixed or a human stays in the loop | Honest; matches your own "no detect-only at this boundary" stance. Costs: if the runtime *does* block, the stop never fires, so no real cost |
| **B — Just a caveat** | Note the weakness, keep running unattended anyway | Simplest; but on a factory that edits its own code, "we noticed after it happened" is the wrong failure mode |

> **My recommendation:** **A — treat it as a stop.** A fence that doesn't block is a sign, not a wall, and this factory rewrites itself. But this is a genuine risk-tolerance call, which is yours. **Undo path:** revert pull request #231 and the original "caveat" posture is back.

Because this reframes a decision you'd already adopted (the fence as an unconditional precondition → now conditional on the runtime actually blocking), I did **not** quietly write it into the specs. It waits for your yes/no.

---

## 2. Can the *safe parts* run unattended even before that's settled?

**Background.** "Stop unattended running" sounds like it kills the lights-out-factory goal entirely if the runtime turns out to only notice. But not every part of the factory can leak data in the first place. The trifecta needs all three of: private data + untrusted input + a way out. A job that has *none of one of those* — say, a job that only ever touches a fake stand-in and never reaches production — can't assemble the trifecta no matter what the runtime does.

**The decision.** Let those structurally-safe jobs run unattended even under a notice-only runtime; keep humans in the loop only on the jobs that *could* assemble the trifecta. Plus two bits of hygiene: write down whether human-in-the-loop review is actually workable at the volumes we're targeting (so it's not a bottleneck nobody costed), and name a point where we revisit "can we go fully unattended yet" (so "stay human-in-the-loop" doesn't quietly become "forever").

**The options:**

| Option | What it means | Trade-off |
|---|---|---|
| **A — Allow the safe parts (my rec)** | Unattended where the trifecta can't form; human-in-the-loop only on risky jobs | Keeps real autonomy value alive under a notice-only runtime, with no new building |
| **B — All-or-nothing** | One global switch: either everything runs unattended or nothing does | Simpler to reason about; but throws away the autonomy you *could* safely have |

> **My recommendation:** **A.** It preserves the whole point of the project — leverage from unattended work — without building any of the risky blocking machinery. **Undo path:** drop this clause from the same decision record; you're back to the simpler global switch.

---

## 3–5. The three you decided up front (settled)

- **#3 — Prepare the test, don't run a live factory overnight.** You chose this when I asked. Running a live Gas City spins up real agents and spends real money; the prototype's own authors deferred that test for the same reason. I wrote the test and harvested everything the existing prototype already proves, instead.
- **#4 — Do the full build-detail run.** You chose the broad pass (turn sketches into build-ready detail), not just the narrow Gas City check. I did the check first, then the first cluster of detailed components.
- **#5 — Stack the work as several small pull requests.** You told me mid-run you didn't want one giant lump at the end. So the night is five small, ordered pull requests, each reviewable on its own.

## 6. Four small fixes between the data components (settled, housekeeping)

When five components are written in parallel, they can drift at their shared edges. A reviewer whose only job was the *seams between* them caught four mismatches — the important one being that two components had agreed on a rule but disagreed on the exact shape of a shared field (one used a structured `{stream, number}` pair, the other a bare number), which would have broken at build time. All four are reconciled and written down. No judgement needed from you — flagged only because they touch shared contracts.

## 7. Folding the prototype's verified facts in (settled, informational)

The prototype already worked out a dozen real facts about how Gas City behaves. I wrote those into the specs, marked "verified against a real `gc`," and closed several open questions. The helper that harvested them flagged three as *contradicting* our design — I checked each against what the specs actually say, and **all three were false alarms** (our design had deliberately left those things unspecified until we could check them). Nothing for you to do; it's a good-news result — the project's "don't assume the runtime" discipline held up under a real test.

---

## The short version

- **Two real decisions are yours** (1 and 2), both about how cautious to be on safety; I've recommended on both and either is one revert to undo.
- **Everything else is either your earlier call or low-regret housekeeping** I've already handled with an undo path.
- **One fact is still genuinely unknown** — does the runtime block or only notice — and I refused to guess it. The test is written and waiting for a machine with Docker.
