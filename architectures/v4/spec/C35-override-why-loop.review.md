# Adversarial review — C35 Override → pattern → rule loop (canonical track, sweep 1)

Reviewer persona: Adversary / critic-fixer — Override Discipline (C35)
Target: spec/C35-override-why-loop.md + plan-faithful/C35-override-why-loop.md
Charter: canonical single-track (D-6). Track-A posture — attack FIDELITY + COMPLETENESS, not design;
**plus** the capability-for-principle bar (flag hardening-on-existing-capability vs new principle-tied
capability). THE BAR for C35: native Claude Code hooks only; rule-conversion operator-gated, not
autonomous; no bespoke clustering engine / real-time alerting; D-3 schema deference; G43 addressed.

## Findings

### RC35-01 — major — Two of the three rule-conversion sinks (C10 spec-linter, C15 workflow-linter) are invented; v4 names only the Inspect AI rubric, and the C10/C15 claim is mis-attributed to "brief:"
**Claim.** §1 (last responsibility), §2 (Downstream rule sinks row), §3 (outbound contract 6), §5 (step 6),
§8 (AC4), and the plan (T6, §2, §3, §4.4, §5.2, DoD) all assert a **three-way** rule-conversion fan-out:
spec-structural → a new **C10** (EARS/INCOSE) rule, workflow-structural → a new **C15** (Mammoth) rule,
satisfaction-class → a **C30** Inspect-AI rubric. The §2 row cites this as `(brief: "validation rules C35
produces feed C10 / C15")`.
**Evidence.** v4's *only* named rule-conversion target is the single L216 table row: "Rule conversion |
Turn recurring overrides into validation rules | **Manual review + new Inspect AI rubric** | … | Operator
workflow" (README:216). v4 names **no** C10 or C15 conversion path for overrides. The component-inventory
C35 row lists dependencies as exactly **C28, C20, C30** — **C10 and C15 are not C35 dependencies**. The
attributed `brief:` text ("validation rules C35 produces feed C10 / C15") does **not exist** in the
dispatch brief, the BUILDER-BRIEF, or anywhere in `_meta/` (the only C10/C15 sink references in `_meta/`
are C07's *vocabulary-lint* DELTA, unrelated to C35). So the C10/C15 sinks are a **faithful inference at
best** (C10/C15 are indeed "validation rules" in the system, and README L208's thesis says generically
"you've described a validation rule") but are presented as **sourced fact with a fabricated citation** —
the exact Track-A failure (invent architecture v4 doesn't state + mis-cite a source). The C30 Inspect-AI
rubric sink **is** v4-grounded (README:216) and correct.
**Fix (applied).** (1) Demoted the C10/C15 sinks from asserted fact to an explicit `[FAITHFUL-FILL]`
inference, stating that v4's L216 names **only** the Inspect-AI rubric and that routing *spec-structural* /
*workflow-structural* override classes to C10/C15 is the minimal faithful reading of L208's generic
"validation rule" (since those linters are where such rules live), not a v4-stated sink. (2) Removed the
false `(brief: …)` attribution. (3) Kept the Inspect-AI/C30 sink as the v4-named path and made it primary.
The dependency-direction wrinkle (inventory has C35 dep on C30 only, yet C35 *emits to* C10/C15/C30) is
noted as inference, not inventory fact.

### RC35-02 — minor — Header cites D-1 as "relevant" but the cited relevance (judge/rubric same provider/family) does not bear on C35's rule-conversion
**Claim.** The spec header lists "**D-1** (judge/rubric runs on the same provider/family — relevant to the
§3 rule-conversion handoff)" among binding decisions obeyed.
**Evidence.** D-1 settles the *judge provider* question (judge = same provider/family as coder; cross-family
judging → FE-1). C35's rule-conversion *emits a new Inspect-AI rubric* into C30's store (README:216); it
does **not** invoke the judge, choose a judge provider, or run a judge. The dispatch brief lists only
**D-6** and **D-3** as relevant to C35. D-1 is at most tangential (a rubric C35 emits is later *consumed* by
a judge that D-1 governs), and citing it as a binding decision "obeyed" by C35 slightly overstates C35's
relationship to it. Not a fidelity error in substance (the spec doesn't act on D-1), but an over-broad
header citation.
**Fix (applied).** Softened the header line to note D-1 is **contextual** (governs the judge that later
consumes a C35-emitted rubric), not a decision C35 itself implements; left D-3/D-6 as the binding ones.

### RC35-03 — minor — §6 F-mode table claims F52 "Applies" to C35, but v4's F52 is the self-heal loop's mode; the C35 linkage is an inference
**Claim.** §6 lists **F52** "More controller patches / runaway loop" as a failure mode that "Applies" to
C35, mitigated by I4 + operator gate.
**Evidence.** This is the correct *risk* (auto-shipped rule conversion could oscillate) and the mitigation
(operator gate, I4) is exactly the F52/G35 safety bar the brief asks for — so the **handling is right**. But
F-MODE-COVERAGE maps F52 to the *self-healing* loop ("more controller patches", §8), not to C35; C35
applying F52-by-analogy to its own conversion step is a faithful *extension*, not a v4-stated mapping (C57
owns the canonical F-mode→component map). The spec presents it in the same table as F10 (which **is**
v4-mapped to the P8 component, F-MODE L31 — verified correct) without distinguishing the v4-stated mapping
(F10) from the analogical one (F52).
**Fix (applied).** Tagged the F52 row as a **faithful analogy** (C35's conversion step is structurally the
same self-modifying-control trap F52 names; canonical mapping owned by C57), distinct from F10 which is
the v4-stated P8 mapping. Handling unchanged.

### RC35-04 — minor — §2 labels C30 "Upstream"; inventory direction is C35 → depends on C30, and C30 is functionally a downstream rule *sink*
**Claim.** §2 dependency table lists C30 under "**Upstream** (rule sink for satisfaction-class overrides)".
**Evidence.** The inventory has C35 `depends on C28, C20, C30`, so C30 is formally upstream of C35 — but
the *dataflow* is C35 **emitting a rubric into** C30 (README:216), which is a downstream-sink relationship.
Calling a sink "upstream" is defensible only because C30's rubric schema constrains C35's handoff format;
the label is confusing as written and conflates "dependency direction" with "dataflow direction." (C30's
own spec §2 lists C35 as a *downstream consumer* of its corpus — the inverse framing.)
**Fix (applied).** Reworded the C30 row to state the relationship precisely: C35 **depends on** C30
(inventory) because C30 owns the Inspect-AI rubric schema C35 must target, **and** C35 emits new rubrics
*into* C30 (a sink) — i.e. it is both an upstream schema-constraint and a downstream emission target. No
direction invented; the dual relationship is made explicit.

### RC35-05 — minor — "C20 spec §4.2" / "C28 §3 / AC3" citations verified exact; one over-strong "verbatim" qualifier on the thesis is accurate but flagged for the record
**Claim.** §1 says README L208 "states the thesis verbatim" and quotes it; §1/§2 cite "C20 spec §4.2",
"C28 §3 'Hooks'", and "C28 AC3".
**Evidence (verification, not a defect).** All four check out exactly: README L208 is quoted verbatim
("If you can articulate why something looks wrong, you've described a validation rule. Capture overrides,
surface patterns, convert to rules."); C20 §4.2 does author the `override` type with a "why"/rationale
field + overridden-action reference (D-3 honored); C28 §3 lists Hooks (PreToolUse/PostToolUse/SessionStart/
Stop); C28 AC3 reads "…override-detection surface for C35" verbatim. **No fix needed** — recorded so the
verdict rests on a checked citation base, not assumed accuracy.

### RC35-06 — informational — THE BAR is satisfied; capability-for-principle scope is correct
**Claim/verification.** Native-hooks-only (I5, AC6, §1 NOT-list, §7) — **pass**; detection rides C28's
native PreToolUse/PostToolUse with no custom hook engine. Operator-gated conversion, no autonomous
auto-promote (I4, AC4, §6 F52 handling, §7) — **pass**; matches the F52/G35 safety bar. No bespoke
clustering engine (reuse C37/DuckDB), no real-time alerting/dashboard (surfacing is periodic by design),
no auto-enforce path — all explicitly **dropped** on the capability bar (§7). D-3 schema deference (I3,
AC5, §1/§4 NOT-author, §3 contract 4) — **pass**; C35 logs against C20's schema, change-requests new
fields rather than extending locally. G43 addressed (§6 AMBIGUITY block + OQ1: automatable scope =
detect→why→log→surface; conversion operator-gated; F10's "Addressed" valid only from Phase 3a) — **pass**,
and the G43 override-recognition predicate is correctly identified as the one genuine custom piece (§1,
§7, OQ2). Transfusion sources (CloudTrail/git-reflog log shape; Honeycomb BubbleUp/Datadog Watchdog
surfacing) cited correctly vs AI-CONTEXT L400–401. **No fix; no over-build found.**

## Verdict
**accept-with-fixes.** Strong, well-traced, and dead-on the bar: native hooks only, operator-gated
conversion (no autonomous promote), D-3 schema deference, no bespoke clustering/alerting over-build, and a
crisp G43 reconciliation that correctly fences C35's automatable scope to detect→why→log→surface with the
predicate as the lone custom piece. The one **major** fidelity defect is RC35-01 — C35 invents the C10
spec-linter and C15 workflow-linter rule-conversion sinks (v4 names only the Inspect-AI rubric at L216, and
the inventory lists neither as a C35 dependency) and props them up with a non-existent `brief:` citation;
fixed in place by demoting them to a marked faithful inference and removing the false attribution, keeping
the v4-grounded C30 rubric sink primary. Remaining fixes are citation-precision / direction-labeling
qualifiers (D-1 contextual not binding; F52 analogical not v4-mapped; C30 dual up/down relationship). No
architectural item required deferral; nothing left `DEFERRED`. The two load-bearing open questions (OQ2
predicate boundary, OQ4 per-sink rule encoding) are correctly routed to sweep-2/review-log.
