# Adversarial review — C08 Spec artifact & format (Track A, sweep 1)

Reviewer persona: Subsystem Adversary (C08/C17)
Target: spec/C08-spec-artifact.md (+ plan-faithful/C08-spec-artifact.md)

Track A attacks **fidelity & completeness only** — not the design. The question is never "is collapsing
spec into `prompt.template.md` a good idea" (that is Track B's fight) but "is it the *most faithful*
reading of v4, and is it labelled honestly as an inference rather than a fact."

## Findings

### RC08A-01 — major — The artifact=`prompt.template.md` collapse is presented as the faithful reading, but v4's own corpus contradicts it; the [FAITHFUL-FILL] under-states the conflict.
- **Claim.** §1's [FAITHFUL-FILL] (line 24) treats "the prompt-template file IS the canonical spec artifact"
  as "the minimal consistent reading" because README:106 maps the "Spec format" row onto Gas City prompt
  templates. But the *same* source set v4 cites — `one-shot-specs-and-research.md` Part 1 — shows real
  dark-factory specs (StrongDM's three markdown files; Kilroy `spec.md`+`DoD.md`) as **standalone
  target-system documents distinct from agent prompt templates**. OQ-1 (line 120) honestly names this as
  "the load-bearing ambiguity," yet §1/§3/§4 commit fully to the collapse without an `> [AMBIGUITY: G-?]`
  block at the point of commitment.
- **Evidence/reasoning.** Track-Charter A rule 3: "Where v4 is contradictory or ambiguous, you do not pick
  a winner silently — you record both readings under `> [AMBIGUITY]` and pick the one most consistent."
  Here the spec picks a winner (collapse) in §1 and only surfaces the competing reading 110 lines later in
  §9. README:106 equating "spec format" with prompt templates is a *placement-table* statement; the
  one-shot corpus is *primary evidence of practice*. A faithful spec should weight these explicitly, not
  bury the conflict in an open question.
- **Suggested fix (APPLIED).** Promote the conflict to an `> [AMBIGUITY: OQ-1]` block at the §1 point of
  commitment, stating both readings and *why* the collapse is chosen as the faithful floor (README:106 is
  the only statement that names a concrete on-disk spec *format/path*; the corpus shows *practice* but v4's
  substrate section never reconciles them — so the collapse is the smallest choice that yields a single
  named artifact). This keeps the pick but makes it charter-compliant.

### RC08A-02 — major — INV-2 ("MUST parse as a Go `text/template`") is a real faithful inference, but the spec also calls the body "free-form Markdown" — these are in tension and the tension is unflagged.
- **Claim.** INV-2 (line 53) requires the artifact parse as a Go `text/template`. §4's [FAITHFUL-FILL]
  (line 70) says the body is "free-form Markdown … nothing stronger." A document can be free-form Markdown
  yet still contain a stray `{{` that breaks Go-template parsing — so "free-form" and "must parse as a Go
  template" are not jointly free. A human authoring plain Markdown with literal `{{handlebars}}` or a JSON
  example containing `{{` would violate INV-2 without realizing it.
- **Evidence/reasoning.** This is a completeness gap, not a design critique: the faithful spec asserts both
  constraints but never states that template-significant characters are reserved, so AC-2 ("renderable") is
  not actually decidable from the format rules as written.
- **Suggested fix (APPLIED).** Add a one-line faithful note to §4 that "free-form" means *free-form within
  Go-template lexical rules* — literal `{{`/`}}` must be escaped — and cross-reference INV-2. This is the
  minimal consistent reconciliation; it invents no new structure.

### RC08A-03 — minor — F36 mitigation ("one `prompt.template.md` per agent role") silently assumes a fact the spec elsewhere flags as unverified.
- **Claim.** §6 F36 row + its [FAITHFUL-FILL] (line 98) assert the natural chunk boundary is "one
  `prompt.template.md` per agent role." But if OQ-1 resolves the other way (spec is a standalone doc the
  template references), the chunk unit is the *spec doc*, not the template. The F36 mitigation is therefore
  contingent on the very ambiguity OQ-1 leaves open.
- **Evidence/reasoning.** Internal consistency: a faithful spec should not present a mitigation as settled
  when it depends on an unresolved load-bearing ambiguity it itself raises.
- **Suggested fix (APPLIED).** Add a clause to the F36 fill noting the chunk-unit claim is contingent on
  OQ-1's resolution.

### RC08A-04 — minor — Dependency table lists C03 as the *only* hard upstream, but §3.1 storage and §7 attribution lean on C41, and §1 names C11 as authoring input — C41 is absent from §2's upstream rows in a way the inventory does not require but the prose does.
- **Claim.** §2 marks C11 "Upstream (authored by)" but C41 (actor identity for attribution, load-bearing
  for INV-3/AC-3) appears only inline in §3.1/§7, not as a dependency row. The inventory lists only `C03`
  as C08's dependency, so adding C41 as a *hard* dep would over-state; but the prose relies on C41 for a
  stated invariant.
- **Evidence/reasoning.** Minor completeness/traceability issue: an invariant (INV-3) depends on a
  component not surfaced in the dependency context section.
- **Suggested fix (APPLIED).** Add C41 to §2 as a soft "Upstream (attribution)" row matching the inventory
  (which does not list it as a hard dep), so the dependency picture matches the invariants.

### RC08A-05 — minor — G16 disposition is correct and well-argued, but AC/§8 does not include an acceptance check that the disposition was recorded — the plan (DoD §6.3) does, the spec does not. Cosmetic traceability gap, noted, not blocking.
- **Suggested fix (NOT APPLIED — cosmetic).** Optional: add an OQ/§9 cross-pointer. Left to author.

## Verdict

**accept-with-fixes.** The faithful spec is fidelity-sound on the core P1 mapping, the INV set, and the
F-mode coverage, and its G16 disposition is exactly right (P1 is not the contested principle). Its one
real fidelity weakness is RC08A-01: it picks the spec=`prompt.template.md` collapse as "the" faithful
reading while its own cited corpus shows the opposite practice, and defers the conflict to §9 instead of
flagging it at the point of commitment per Charter A rule 3. Fixed in place by promoting the conflict to an
`[AMBIGUITY]` block (keeping the same pick, now charter-compliant). RC08A-02/03/04 fixed in place. None are
architectural — the collapse-vs-standalone *decision* is correctly left as the top open question for the
integrator and is where Track B's DELTA-01 attacks.

**Integrator note (C08 spec-vs-template):** Track A's collapse is the *defensible faithful floor* (it is
the only reading that yields a single v4-named artifact + path); Track B's DELTA-01 standalone-bundle is
the *better engineering* and is corpus-supported. The two are a clean faithful-vs-optimized split, not a
faithful error. The real decision the integrator must make is the **C08↔C09 boundary**: who owns the
reference seam (see C08-optimized OQ1). DEFERRED to integrator.
