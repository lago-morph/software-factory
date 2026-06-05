# Panel review 07 — Adversarial fact-check: methodology & formulas report

**Target:** [`methodology-and-formulas-plain-english.md`](../../../../../methodology-and-formulas-plain-english.md)
**Reviewer lens:** over-claim / fabrication / mis-grounding hunter.
**Verdict:** `accept-with-named-amendments`.

The report is unusually disciplined about its central risk: the up-front honesty flag
([report L12–18](../../../../../methodology-and-formulas-plain-english.md)) and the in-code banner
`ILLUSTRATIVE SHAPE (exact keys are Gas City's, confirm at Gate 0)` correctly inherit C12's top open
question ([C12 §9.1](../../spec/C12-formula-pipeline-file.md): "C12's entire field model … is **Gas
City's**, asserted 'Native' but unverified"). The four node kinds, "methodology = file edit," bounded
loops, the discipline linter, and the same-scenarios/same-judge experiment are all genuinely grounded.
The amendments below are real but bounded; none requires a counter-proposal.

## Required fixes (each with the cited spec line)

1. **The "DIFFERENT model family" judge comment over-claims Phase-0 reality.** Report L123 asserts the
   judge node is a *different model family* as flat fact (`# AI (DIFFERENT model family)`), echoed in
   Part 4/Part 3 prose ("a separate step (and a different model family)", L141). The spec says the
   opposite **for the phase this report covers**: cross-family is **RELAXED to advisory (D-1)** — at
   Phase 0 "the judge is the *same agent family* exercised in a **separate rig**"
   ([C32 §1, L96](../../spec/C32-judge-harness.md); [C32 §9 G08, L703](../../spec/C32-judge-harness.md)
   "RELAXED to advisory"; [C29 L66](../../spec/C29-model-floor-stylesheet.md)
   `cross_family_required: bool — false at Phase-0`). The main report hedges this correctly ("otherwise
   they share the same blind spots" — [next-steps L153](../../../../../next-steps-plain-english.md)).
   **Fix:** change the comment to "different *rig/role* (cross-family is the FE-1 aspiration; Phase-0 is
   same-family, rig-isolated)" or drop the parenthetical. This is the single most dangerous over-claim:
   it states an unbuilt safety property as a present fact, and it is the kind of thing the reader will
   act on.

2. **`$slot` parameter syntax is illustrated without inheriting C12's specific NON-Gas-City caveat.**
   The general banner covers "exact keys," but the report uses `params = [...]`, `$spec_path`,
   `$scenario_set` (report L95, L102, L126) — exactly the `$slot` shape C12 flags as drawn from
   **non-Gas-City DOT exemplars, not a real Gas City formula**
   ([C12 §3.1 param row + FAITHFUL-FILL, L100–111](../../spec/C12-formula-pipeline-file.md): the
   `$epic_id`-style slots are "DOT `pipeline.dot` files from attractor-pi-dev / Fabro — **not** Gas City
   formulas … explicitly **not** assumed to match"). A lay reader cannot tell that the `$`-syntax is
   borrowed from a *different system*. **Fix:** one clause noting the `$`-slot notation specifically is
   borrowed from non-Gas-City DOT pipelines and is not confirmed Gas City syntax.

3. **The `after = [...]` / `[loop]` edge-and-loop keys read as confirmed schema.** The bounded-loop
   framing is correctly grounded ([C12 §3.1 loop FAITHFUL-FILL, L113–122](../../spec/C12-formula-pipeline-file.md):
   "iteration is a **bounded loop construct** … The exact loop primitive is Gas City's and unverified"),
   but the concrete `[loop "fix_cycle"] / from / to / condition / max_iterations` block (report L134–139)
   and `after`/`in` keys are invented field names presented inside a runnable-looking TOML file. The
   banner says "exact keys are Gas City's," which technically covers it, but the loop block is the most
   fabricated-looking element and deserves an inline marker. **Fix:** add `# invented key names — loop
   primitive unverified (C12 OQ-2)` on the `[loop]` block, or move the banner's "confirm at Gate 0" note
   adjacent to the loop.

## Verified-correct (no change needed)

- **Four node kinds** `{agent, tool, gate, sub_formula}` (report L65–72) — exact match to
  [C12 §3.1 / §1, L30](../../spec/C12-formula-pipeline-file.md) (D-7 taxonomy home = C12). Plain-meaning
  glosses (`gate` = wait/human-approval; `sub_formula` = call another recipe) match the spec.
- **"Methodology lives in the file, not prompts" / "edit the file to change how it builds"** (report
  L57–62) — [C12 §1 README:128](../../spec/C12-formula-pipeline-file.md); "methodology change = formula
  edit" ([C12 §5, L209](../../spec/C12-formula-pipeline-file.md)).
- **Discipline linter "flags an `agent` step where a `tool` step would have done the job"** (report
  L76–78) — exact match to [C16 §1, L9–14](../../spec/C16-discipline-linter.md). Good restraint: the
  report doesn't over-claim it proves misuse (C16 is advisory, raises falsifiable flags). Minor: the
  report omits C16's load-bearing falsifying-scenario obligation, but that is acceptable simplification
  for a lay reader, not an over-claim.
- **Same scenarios + same judge; GF-M-first ≠ winner; per-work-type selection** (report L168–197) —
  [C55 INV-2/INV-3, L161–167](../../spec/C55-methodology-experiment.md) and §6 G05 resolution. The
  report's "you run the experiment per work-type and let the satisfaction numbers tell you" matches
  C55's empirical-per-work-type criterion. Code/config work-type split is consistent with C55 OQ-2.
- **`gc formula export <name> --format dot`** (report L144) — verbatim from
  [C12 README:385 / §5.2](../../spec/C12-formula-pipeline-file.md). Correct.
- **"molecule = recipe with real work attached"** (report L156) — matches
  [C12 §1, "Molecule = instantiated bead-tree"](../../spec/C12-formula-pipeline-file.md).

## Co-implementation feasibility (Part 6/7)

The "factory builds its own next piece" recursion (report L216–225) is consistent with **C52**, but the
report is slightly *too breezy* about how automatic it is. C52 imposes three hard constraints the report
underweights: (a) **gene-transfusion is mandatory** — every self-build needs ≥1 real exemplar, "no
invention from scratch" ([C52 §1, README:496](../../spec/C52-self-bootstrap.md)); the report's "build the
DOT visualizer / recalibrate the judge" examples (L219) silently assume exemplars exist. (b) **A mandatory
human design review gates every deploy** ([C52 §1, README:498](../../spec/C52-self-bootstrap.md)) — the
report says "reviewed by you" (L220) which is fine, but should name it as a *required* gate, not a
courtesy. (c) **Transfusion reliability is an unhedged bet (G14)** and the bootstrap "deploy if it works"
has **no rubric (G23)** ([C52 §3 source brief](../../spec/C52-self-bootstrap.md)). **Recommended (not
blocking):** one sentence in Part 6 noting that a factory self-build is *not* free — it needs an exemplar
and clears the same human gate, and "often a self-build" is "when an exemplar exists." This keeps the
loop from reading as more automatic than C52 warrants. Consistent with the main report and grounding
brief on single-seat/serial reality (report L199–201, L199 "one AI seat working serially"), the
spec-completion pass (report L150–152), and the triangle (report Part 7 defect ledger).

*Internal consistency with [`next-steps-plain-english.md`](../../../../../next-steps-plain-english.md)
and [`00-grounding-and-exemplar.md`](../00-grounding-and-exemplar.md): clean except fix #1 above.*
