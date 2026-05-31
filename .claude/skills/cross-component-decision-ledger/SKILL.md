---
name: cross-component-decision-ledger
description: Keep a parallel-authored corpus internally consistent by recording every cross-component conflict resolution as a numbered, adopted decision in a shared ledger file, then propagating each decision id into later subagent briefs and applying it corpus-wide via a single integrator pass. Use whenever multiple subagents (or sessions) author interdependent artifacts and surface conflicting cross-cutting choices — naming/namespaces, ownership ("who defines X"), dependency direction, shared contracts, shared invariants — or when the user asks to reconcile drift across components, or asks "which decision governs X?". Pairs with `disk-fanout-orchestration`.
---

# Skill: cross-component-decision-ledger

When many subagents author interdependent artifacts in parallel, they drift on
cross-cutting choices — each makes a locally-reasonable decision that conflicts
with a sibling's. This skill is the consistency mechanism: a single shared
**decision ledger** where every conflict resolution becomes a numbered, adopted
decision; the decision id is then fed into later briefs so subsequent work
self-aligns, and a final **integrator** pass applies each ruling across the
already-written corpus.

Origin: in the dual-track v4 spec/plan run, independent builders produced **four**
different identity namespaces and **two** conflicting "who owns the bead schema"
answers. Capturing the resolutions as decisions D-1…D-5 in `review-log.md` — and
feeding the ids into later briefs — made components built *after* a ruling
reproduce it unprompted, and one integrator pass made the foundation internally
consistent (see [`retrospective/2026-05-30-214.md`](../../../retrospective/2026-05-30-214.md)).

---

## When to use

- Any time `disk-fanout-orchestration` (or `parallel-subagent-fanout`) authors
  ≥~8 interdependent units and adversaries/reviewers surface cross-component
  conflicts.
- When the same concept is defined differently in two artifacts (namespace,
  schema owner, dependency direction, shared contract, shared invariant).
- When the user says "reconcile the drift", "make these consistent", "which
  decision governs X?", or "stop relitigating this".
- Across sessions: the ledger is the durable record a future session reads to
  avoid re-deciding settled questions.

Negative trigger: a single-author artifact, or a decision local to one file with
no cross-component reach — that is a normal inline choice, not a ledger entry.

---

## The ledger file

One file, conventionally `_meta/review-log.md`, with a clearly-marked **adopted
decisions** section at the top and the open issues below it. Each adopted decision:

```
- **D-N (ADOPTED[ — basis]) — <short title>.** <One-sentence ruling, declarative.>
  <Why this resolution; what it rejects.> Apply across <component ids>. Owner: <who>.
  (Resolves: <XC-id / gap-id>.)
```

Rules for the ledger:

- **Stable ids.** Decisions are `D-1, D-2, …`; cross-component issues are
  `XC-1, XC-2, …`. Ids are append-only and never reused.
- **Declarative ruling.** The decision sentence must be a binding statement ("C20
  authors bead-type schemas; C22 owns the registration mechanism only"), not a
  discussion.
- **Adoption basis.** Note how it was decided: `user`, `integrator`, or
  `both adversaries independently concur` (independent convergence is a strong
  signal an agent may adopt without escalating). Genuinely architectural or
  ambiguous calls go to the **user** via `AskUserQuestion`, not silent choice.
- **Scope of application.** List the component ids the ruling touches, so the
  integrator pass knows where to apply it.
- **Open vs resolved.** Keep unresolved conflicts in an open section with severity;
  promote to an adopted `D-N` the moment they're settled, and mark the originating
  `XC-id` resolved.

---

## Workflow

### Step 1 — detect
During review/integration, every time two artifacts disagree on a cross-cutting
choice, log it as an open `XC-N` in the ledger (one-line statement, the components
involved, severity). Reviewers should flag these explicitly rather than silently
picking a side in their own component.

### Step 2 — resolve
For each `XC-N`, decide the ruling:
- If the source/charter or an existing decision settles it → adopt directly.
- If **independent reviewers converge** on the same fix → adopt (cite the
  convergence as the basis).
- If it is genuinely architectural, ambiguous, or a value call → escalate to the
  user with `AskUserQuestion` (give enough context to answer without scrolling).
Record the result as an adopted `D-N` and mark `XC-N` resolved.

### Step 3 — propagate
Feed the decision id and its one-line ruling into the briefs of any **not-yet-built**
units it affects (e.g. "Per D-2, use namespace `softwarefactory.v4.beads`"). New
work then conforms by construction — no rework. Components built after a ruling
should reproduce it; if one doesn't, that's an integrator fix.

### Step 4 — apply (integrator pass)
Dispatch a single **integrator** subagent (the one agent permitted cross-component
edits) to apply the adopted decisions across **already-written** artifacts:
minimal edits realizing each ruling, preserving each artifact's structure and
track discipline. It writes an `INTEGRATION-PASS-N.md` report (per-decision: files
edited + what changed; residual conflicts; a consistency verdict) and edits ONLY
the listed files — never review files, never git.

### Step 5 — verify
Spot-check that no artifact still treats a resolved issue as open (grep for the old
namespace/owner/term). Plan docs and downstream artifacts are a common miss — the
integrator may have swept specs but not their plans. Run a targeted cleanup if so.

---

## Integrator brief (template)

```
You are the Integrator — the one agent permitted cross-component edits, to make the
corpus internally consistent by applying the ADOPTED decisions in <ledger path>.
Read: <ledger path> (decisions D-1..D-N are authoritative), the charters/templates.
For each decision, apply the MINIMAL edits across the listed component artifacts
(both tracks/variants). Preserve structure, marks, and track discipline; for a
faithful track record a ruling as an ambiguity-resolution citing the decision id,
do not turn it into an optimized doc. Touch ONLY the artifacts the decisions name.
Do NOT edit review files. NEVER run git.
Write <_meta>/INTEGRATION-PASS-N.md: per-decision files edited + change; residual
conflicts; consistency verdict.
Return a ≤16-line receipt: files edited (count, per decision), anything not cleanly
applied, residual conflicts for a human, consistency verdict.
```

---

## Concrete examples

**Example A — namespace sprawl (the origin).** Four artifacts used four reverse-DNS
namespaces for the same identity space. Logged as `XC-4`; both Persistence
adversaries independently recommended one factory-owned root. Adopted as
**D-2**: `softwarefactory.v4.{beads,trajectory,packs}`, vendor root dropped. Fed
into later briefs (a subsequent builder adopted it unprompted) and applied across
C02/C20/C21/C22 by the integrator; a follow-up cleanup caught a stale plan doc.

**Example B — ownership fork.** Two components both claimed to author the same
schema (a blocker). Logged `XC` → adopted **D-3**: "C20 authors the schema; C22
owns the registration mechanism only." The integrator removed C22's authoring
claim and wired the documented seam; both specs now agree.

---

## Anti-patterns

- **Silently picking a winner** inside one component when a cross-cutting conflict
  is detected — log it and resolve it in the ledger so the choice is visible and
  applied everywhere.
- **Relitigating a settled decision** in a later wave — the id exists precisely so
  it doesn't get re-decided; cite `D-N` and move on.
- **Escalating convergent or charter-settled calls to the user** (noise), or
  **silently adopting genuinely architectural calls** (overreach). Match the
  adoption basis to the call.
- **Skipping the integrator pass** — propagation fixes *future* work; the
  integrator fixes *already-written* work. You need both.
- **Forgetting downstream artifacts** — plans, indexes, and tests often still cite
  the pre-decision value after specs are swept. Verify (Step 5).

---

## Acceptance criteria

1. Every cross-component conflict is a ledger entry (`XC-N`), not a silent local choice.
2. Every resolution is an adopted, declaratively-stated `D-N` with a scope and basis.
3. Decision ids are propagated into later briefs (new work conforms by construction).
4. An integrator pass + verification leaves no artifact treating a resolved issue as open.

---

## See also

- [`disk-fanout-orchestration`](../disk-fanout-orchestration/SKILL.md) — the fan-out this keeps consistent (Step 6 there).
- [AGENTS-MD-831d547873](../../../AGENTS.md#drive-cross-component-rulings-through-a-decision-ledger) — the universal trigger rule.
- [`retrospective/2026-05-30-214.md`](../../../retrospective/2026-05-30-214.md) — the session this skill was extracted from.
