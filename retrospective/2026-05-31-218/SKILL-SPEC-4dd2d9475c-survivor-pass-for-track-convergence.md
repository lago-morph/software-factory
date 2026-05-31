# Spec: `survivor-pass-for-track-convergence`

- **ID**: SKILL-SPEC-4dd2d9475c
- **Source retrospective**: ../2026-05-31-218.md

## Intent

When a design exploration has produced two or more parallel tracks (e.g., one faithful elaboration of upstream + one optimizer track with named deltas), and the time has come to converge to a single canonical track, this skill runs a per-element survivor pass: enumerate every divergent element, score each against an explicit principle-capability bar refined through dialogue with the operator, classify as DROP / KEEP-MINIMAL / ALREADY-IN, then apply by reading the canonical artifacts first. The apply phase often turns out to be a near-no-op when the canonical track was authored to a minimal-fills charter, which IS the right outcome — it confirms the canonical was already complete.

## Trigger

**Direct triggers:**
- "merge the tracks" / "converge to one track" / "drop track X"
- "raid Y into Z" / "cherry-pick from optimized into faithful"
- "we only need one track now"
- Operator expresses cost concerns about maintaining parallel tracks
- Operator wants to commit before authoring more divergent elements

**Proactive trigger:**
- Two or more tracks of similar artifacts exist for the same components, the divergent track lists named deltas (DELTA-NN), and the operator hasn't yet decided whether to keep both.

**Negative trigger:**
- The operator has just chosen to keep both tracks running; don't propose convergence.

## Inputs

- Both track roots and their artifact paths (e.g., `spec-faithful/` + `spec-optimized/`).
- An enumeration of the divergent elements (typically a research artifact that lists every named DELTA across all components, e.g., `optimized-deltas-enumeration.md`).
- The operator's bar — usually starts informal and is refined through dialogue. Capture it as a single quotable sentence.
- The 12 principles (or equivalent first-principles list) the system must implement.

## Outputs

- `SURVIVOR-PASS.md` ledger: per-element table with verdict + reason, plus a summary table by component, plus a list of dropped + deferred elements.
- Edits to canonical artifacts for the genuine KEEP gaps (often zero).
- Frozen-reference READMEs in the divergent-track directories pointing back at the canonical.
- `FUTURE-ENHANCEMENTS.md` entries (FE-N) for any element worth re-considering, each with its specific external trigger.
- Updates to tracking docs (STATUS, HANDOFF) reflecting the converged state.

## Workflow

1. **Confirm the bar via dialogue.** Don't lock in the bar from the operator's first articulation; expect 2–3 refinements. Capture the final form as a single quotable sentence. Examples that fit this pattern: "every element gets full implementation," "only what we MUST define for the system to work," "adds capability for a specific principle, partial satisfaction by upstream stack counts."
2. **Enumerate divergent elements.** Read the cartographer-style enumeration artifact (often pre-existing). Confirm the count and the per-component grouping.
3. **Score each element.** Three verdicts: DROP (scope creep under the bar), KEEP-MINIMAL (real capability gap; pull in *minimal* form, not the divergent track's full hardening), ALREADY-IN (e.g., adopted via prior integration pass). Write the ledger as you go.
4. **Sanity-check with the operator.** Present the ledger summary + 3–5 marginal-call examples. Iterate on bar interpretation if pushback comes. Refine again if needed.
5. **Apply by reading canonical first.** For each KEEP-MINIMAL, read the target canonical artifact in full before writing. Check whether the minimal form is already there. Check whether the divergent delta would overturn a deliberate decision the canonical author flagged. Apply only genuine gaps. Mark no-ops explicitly.
6. **Archive the divergent track in place.** Write a `README.md` in each divergent-track root pointing at the canonical and at the FUTURE-ENHANCEMENTS entries. Do NOT physically move the directory unless link-rewrite cost is genuinely low (it usually isn't — see the companion ADR).
7. **Record deferred items as FE-N with triggers.** Each deferred architectural bet, each dropped-but-real capability, gets an entry in `FUTURE-ENHANCEMENTS.md` with a specific external trigger that would warrant revisiting.
8. **Update tracking docs.** STATUS banner, HANDOFF resumption procedure, any briefs that referenced the multi-track structure. Add convergence banners; do not rewrite extensively.

## Concrete examples

**Example 1: v4 spec/plan run (this session, PR #218).** 23 components had been built on two tracks (faithful + optimized) with 148 named DELTAs in the optimized track. The operator's bar refined over a long dialogue from "drop optimized" → "what would we lose with optimized" → "does this addition give us MORE capability tied to a specific 12-principle?" The survivor pass scored: 25 KEEP-MINIMAL, 5 ALREADY-IN (via prior integration pass D-1..D-5), 118 DROP. The apply phase read all 12 keep-bearing canonical specs and found 21 of 25 keeps were already present in minimal form; the other 4 reclassified DROP (3) or DEFER (1, FE-5) on close read. Net spec-content edits: 0. The session committed the rename `spec-faithful/` → `spec/`, the SURVIVOR-PASS ledger, frozen-reference READMEs in the optimized directories, and an updated HANDOFF.

**Example 2: a hypothetical UI library convergence.** Two parallel UI component libraries — `ui-base/` (minimal accessible primitives) and `ui-themed/` (themed reskins of every base component plus 30 new "improved" variants). Operator's bar after refinement: "we only need one library; keep variants that are not expressible as a theme on a base component." Survivor pass: ~10 KEEP-MINIMAL (genuinely novel variants), 80% DROP (themed reskins that ARE expressible as theme variables on the base). Apply phase reads the base library and finds 6 of the 10 keeps are already expressible by composing existing primitives, so reclassify to DROP. Net additions to base library: 4 new primitives. `ui-themed/` archived in place with a README pointing at the theme variables documented in base.

## Anti-patterns

- **Locking in the bar from the operator's first articulation.** The bar refines through dialogue. The session that produced this skill went through three refinements; each tightened the bar and the operator caught me prematurely declaring decisions stable.
- **Skipping the read during apply because "I already scored it."** Pattern-matching from the ledger is not sufficient; the artifact's specific text can flip the decision. Re-reading is the cheap way to avoid silently overturning the canonical author's flagged decisions.
- **Treating "apply turned out to be a no-op" as failure.** It is the right outcome when the canonical was authored to a minimal-fills charter. Report the no-op explicitly — it is the proof the canonical was complete.
- **Physically moving the divergent track instead of archiving in place.** See the companion ADR. Cosmetic benefit of "all archives live in one place" rarely justifies the relative-link churn across the moved directory plus all inbound references.
- **Deferred items without specific external triggers.** "Revisit later" is not a trigger. "When G37 secrets store is chosen" is. "When concurrency outgrows manual management AND Max ToS clarity" is. Without triggers, deferred items rot.

## Acceptance criteria

1. The ledger lists every divergent element with verdict + one-sentence reason.
2. The bar is captured as a single quotable sentence at the top of the ledger.
3. The apply phase reports no-ops, edits, and reclassifications separately.
4. Every deferred item has a specific external trigger in `FUTURE-ENHANCEMENTS.md`.
5. Tracking docs (STATUS / HANDOFF / equivalent) reflect the converged state and point at the ledger for grounding.

## Files this skill creates / modifies

- Creates: `_meta/SURVIVOR-PASS.md` (or equivalently named ledger).
- Creates: `<divergent-track>/README.md` for each archived track (frozen-reference banner).
- Modifies: `_meta/FUTURE-ENHANCEMENTS.md` (appends FE-N entries with triggers).
- Modifies: `_meta/STATUS.md`, `_meta/HANDOFF.md` (or equivalent) — converged-state banners + updated resumption procedure.
- Modifies: canonical artifacts only when a genuine gap is found (often zero).
