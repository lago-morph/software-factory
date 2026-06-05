# Spec: `unverified-substrate-doc-factcheck`

- **ID**: SKILL-SPEC-0ae6873900
- **Source retrospective**: ../2026-06-05-247.md

## Intent

Documents that explain an external substrate or format whose details have **not been verified by
running it** are uniquely prone to a silent, high-cost error: an illustrative example gets read as
verified fact and propagates. This skill adds a dedicated real-subagent fact-check whose sole job is to
hunt for claims stated as verified that the source specs actually hedge — over-claimed syntax, an
unbuilt safety property asserted as present, a borrowed example's field passed off as native — and to
confirm every example is flagged as illustrative. In PR #247 a methodology doc described Gas City
"formulas" (a TOML format nobody has run); the fact-check caught the judge node labelled a "different
model family" as flat fact when the spec relaxes that to advisory at the relevant phase, plus invented
`$slot`/`[loop]` keys not flagged as illustrative. Without the pass, those would have shipped as truth.

## Trigger

- **Proactive (primary)**: you are about to ship a deliverable whose load-bearing claims rest on an
  external substrate, tool, config format, or API behavior that has **not been verified in this
  environment** (the source specs themselves carry hedges like "unverified", "native claim", "FAITHFUL-
  FILL", or an open conformance question).
- **Direct**: "fact-check this", "did I over-claim the syntax?", "is anything here asserted as fact that
  we haven't verified?".
- **Negative**: docs about a substrate you *did* run/verify in-session; pure opinion/strategy docs with
  no factual substrate claims; code with tests that already verify behavior.

## Inputs

- The target document (the deliverable to audit).
- The ground-truth source specs (which carry the real hedges), pointed to explicitly.
- The list of substrates/claims considered unverified.

## Outputs

- A fact-check findings file with a verdict tier (accept-as-is / accept-with-named-amendments /
  reject-with-counter-proposal) and a numbered list of required fixes, each citing the spec line that
  supports or contradicts the doc.
- (After the author applies fixes) the corrected deliverable with every illustrative example flagged
  and every hedge cited.

## Workflow

1. Identify the **unverified substrate claims** in the target doc — anything about an external format's
   syntax, an external tool's behavior, or a safety/capability property that has not been run/verified.
2. Dispatch **one real subagent** as a skeptical fact-checker. Brief it with: the target doc, the
   ground-truth source specs, and the explicit instruction to hunt for (a) syntax asserted as verified,
   (b) unbuilt properties stated as present fact, (c) borrowed-example details passed off as native,
   (d) examples not flagged as illustrative. Require it to quote the supporting/contradicting spec line
   per finding and to return a verdict tier + numbered fixes.
3. Apply the sensible fixes: add an "illustrative shape, unverified" banner to each example, replace
   asserted-as-fact details with the spec's own hedge + citation, and downgrade unbuilt properties to
   "the aim / relaxed at this phase".
4. Re-check internal consistency across any sibling docs that repeated the same claim (a single over-
   claim is often echoed in 2–3 places).
5. Keep the fact-check file as part of the reasoning trail.

## Concrete examples

### Example 1: the Gas City formula doc (PR #247)

The methodology companion showed an illustrative `build-component-v1` TOML formula. A fact-check
subagent, given the doc + the C12 formula spec, returned `accept-with-named-amendments` and caught: the
judge node's comment "AI (DIFFERENT model family)" stated as fact, contradicted by C32 §9 / C29
(`cross_family_required: false` at Phase-0); the `$slot` parameter style borrowed from non-Gas-City DOT
exemplars (C12 §3.1 FAITHFUL-FILL); and the `[loop]` keys invented (C12 OQ-2, loop primitive
unverified). Fixes: reword the judge to "separate rig; different family is the aim, relaxed to
advisory", and add three honesty notes flagging `$slot`/`[loop]`/family as illustrative — and the same
family wording was reconciled in the sibling next-steps report where it had been echoed.

### Example 2: a doc claiming a cloud SDK's retry behavior

A how-to asserts "the SDK retries idempotent calls 3× with exponential backoff." Nobody ran it; the
claim came from memory. The fact-check subagent checks the vendor doc, finds the default is 2 retries
and only for specific status codes, and flags the "3×/all idempotent calls" claim as unverified-as-
stated. Fix: cite the vendor default + version, or label the number "illustrative — confirm against
your SDK version."

## Anti-patterns

- **Self-fact-checking inline.** The author who wrote the over-claim is anchored on believing it; the
  check must be a *real* subagent with the source specs, not the author re-reading.
- **Flagging only the obvious syntax and missing unbuilt-property claims.** The most dangerous error is
  a safety/capability property asserted as present when it's actually aspirational — hunt for those
  specifically.
- **Fixing the target doc but not its echoes.** An over-claim repeated in a sibling doc must be fixed in
  both, or the corpus stays inconsistent.
- **Treating "illustrative" as a blanket disclaimer.** A single global "this is illustrative" line does
  not license asserting specific false details; each invented detail still needs its own flag.

## Acceptance criteria

- [ ] Every example of an unverified format carries an explicit "illustrative, unverified" flag.
- [ ] No format detail, borrowed-example field, or capability/safety property is stated as present fact
      where the source spec hedges it; each such claim cites the spec's hedge.
- [ ] The fact-check was a real subagent dispatch with a verdict tier and spec-cited findings.
- [ ] Any echo of a caught over-claim in sibling docs is reconciled in the same pass.

## Files this skill creates / modifies

- `<meta-dir>/NN-factcheck.md` — the fact-check findings (verdict + spec-cited fixes).
- The target deliverable (and its sibling echoes) — corrected with flags + citations.
