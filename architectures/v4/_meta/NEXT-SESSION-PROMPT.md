# Next-session prompt — close out v4 spec/planning, prep for implementation

> **What this is:** a ready-to-paste prompt for the next session. It gets the operator's open
> decisions, runs the cleanup that finishes the Sweep-1 planning pass (whole-corpus consistency
> check, an expert panel on whether the architecture is right, two reader guides), and leaves the
> effort ready for detailed design + per-component implementation. Authored at the close of the
> Sweep-1 build session (PR #220 merged). Paste everything in the fenced block below.

---

```
You are resuming the Software Factory v4 spec & plan run. SWEEP-1 IS COMPLETE — all 57
components are built, adversary-reviewed, and integrated on the single canonical track
(architectures/v4/spec/ + plan-faithful/), merged to main via PR #220. Your job is to get my
decisions, run the cleanup that finishes this pass, and leave it ready for detailed design +
per-component implementation.

READ FIRST, in order (do NOT read the four v4 source docs into your own context — dispatch
subagents for those):
  1. AGENTS.md, then AGENT-ENTRY.md  — repo conventions; they override harness defaults.
  2. run-summary.md, decisions-to-make.md, and build-order-plain-english.md  — the run, the open
     decisions (your first task), and the outsider build-order plan (already drafted — see step 4).
  3. architectures/v4/_meta/HANDOFF.md, STATUS.md (coverage ledger, 57/57), review-log.md
     (decisions D-1..D-19 + ~196 harvested open questions — the OQs are the Sweep-2 work list).
The four source docs (architectures/v4/{README,AI-CONTEXT,F-MODE-COVERAGE,one-shot-specs-and-research}.md)
are read only by subagents, targeted to their task.

STANDING RULES: single canonical track; the capability-for-principle bar (only custom code where
off-the-shelf can't deliver a 12-principle capability; partial satisfaction by the stack counts;
when in doubt DROP); adversarial review MUST be real subagents, never simulated; subagents persist
deliverables to disk and return short receipts and NEVER run git; the primary owns all commits and
pushes after every wave; concurrency cap ~8. BRANCH: branch off main (e.g. claude/v4-wrapup-<id>),
checkpoint-commit per wave, open a ready-for-review PR when the first deliverable lands.

DO THESE IN ORDER:

1. GET MY DECISIONS FIRST (it shapes everything after). Read decisions-to-make.md. Use
   AskUserQuestion to walk me through the items that are genuinely my call — at minimum #1 (C43
   fence sequencing, ledger item D-18) and #2 (objective-drift watcher, OQ-C57-3); confirm the
   recommended defaults on #3-#6. Record each answer as a numbered binding decision in
   architectures/v4/_meta/review-log.md (continue the D-NN series) and apply it across the affected
   specs in one integrator pass. Where I confirm a recommendation, flip the provisional ruling
   (e.g. D-18) to adopted. Do NOT proceed past anything my answers would reshape without asking.

2. OVERALL CONSISTENCY CHECK (whole-57 cross-batch integration pass). Check cross-batch drift:
   the seams frozen "-> Sweep-2 joint freeze" must be consistent from all sides (C12/C14/C15 loop-DOT
   encoding; C42/C34/C32 judge read-surface; C36<->C37 population seam; C46 dependency edge / OQ-6);
   decision citations resolve; nomenclature is clean ("canonical track", no "Track A/B"); no spec
   over-claims coverage the C57 residual register contradicts. Apply fixes; log anything needing me.

3. PANEL OF EXPERTS - IS THIS THE RIGHT IDEA? Dispatch a panel of REAL subagents and USE SONNET FOR
   THE PANEL SUBAGENTS. Distinct expert personas, each reading targeted corpus + run-summary, each
   arguing independently whether the v4 architecture is the right approach and where it's weakest.
   Cover at least: a distributed-systems / operability skeptic; a security reviewer on the
   lethal-trifecta + self-modification risk; an AI-agent pragmatist (Willison-style: prompt
   injection, what actually works today); a buildability engineer (genuinely-new vs configure-
   existing-OSS; is the OSS-first bet sound); and a methodology critic engaging El Kaim's
   dark-factory and Shapiro's levels framing. Reconcile into ONE verdict doc: where they agree it's
   sound, where they agree it's risky, the dissents, and the changes (if any) worth making before
   implementation. Mark panel-opinion vs synthesis clearly.

4. TWO HUMAN-FACING GUIDES - load and follow the human-scoped-deliverables skill (lead with the idea,
   define terms inline, corpus vocabulary, small Mermaid diagrams <=7 elements, comparison tables, NO
   hash-IDs in body text, descriptive effort scoping not clock-time, load-bearing findings up top):
   (a) PRODUCE a guide for SMART PEOPLE (engineer-level reader) who want to understand the thing in
       architectures/v4 - the whole system: the discipline/methodology/substrate three-layer split,
       the spec-in -> software-out spine, the held-out eval stream, the self-heal loop, the bootstrap
       loop, and what's genuinely new vs assembled from OSS. Visual, plain, decision-dense.
   (b) The PLAIN-LANGUAGE, OUTSIDER-READABLE build-order plan ALREADY EXISTS at
       build-order-plain-english.md (drafted at the close of Sweep-1; non-engineer audience; three
       phases: human-driven -> semi-unattended -> self-building). REVIEW and REFINE it against my
       confirmed decisions (step 1) and the final dependency graph - keep it current; don't restart.

5. WRAP UP THE SPEC/PLANNING EFFORT. Refresh HANDOFF.md and STATUS.md to mark the spec & planning
   phase CLOSED and the next phase = detailed design + implementation, component by component,
   ordered by build-order-plain-english.md and the dependency graph. Cross-link run-summary /
   handoff / the guides cleanly and run scripts/check-internal-refs.py. Open/keep the PR ready-
   for-review with a description surfacing: my decisions, the panel verdict, links to both guides,
   and the recommended first implementation target. Finish with a short status + clickable links to
   the two guides and the verdict.

Treat this as a long run: commit + push every wave. The decisions in step 1 are mine to make - ask,
don't guess. If you hit a genuine architectural fork the decisions and the bar don't settle, write
it up and ask rather than freezing.
```
