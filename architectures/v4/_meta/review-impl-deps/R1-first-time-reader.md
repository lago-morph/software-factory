# R1 — First-time-reader adversarial review of `implementation-dependencies.md`

Persona: a sharp engineer reading the document for the first time, with no knowledge of any prior version. Findings are ordered by the two goals (products-first-class; zero change-narration), then cross-references, then clarity/structure.

---

## Goal 2 — change-narration / conversation-anchoring sweep (highest priority)

**Result: clean.** A full-text sweep for `you asked`, `your example`, `you flagged`, `replaces`, `corrected`, `now leads`, `unchanged`, `see split`, `used to`, `previously`, `formerly`, `earlier version`, `old version`, `as before`, `as noted` returned **zero** hits. The document states what the build IS throughout and never narrates its own history. No defects under goal 2.

One phrase to flag only so it is consciously cleared, not as a violation:

[MINOR] line 253 — "the moment the backbone closes, this is the list that **starts the conversation**" — this is the English idiom "begins the discussion (among the build team)," not an anchor to *this* conversation with a user. A first-time reader parses it correctly. No change required; logged so a future sweeper does not mistake it for conversation-anchoring.

---

## Goal 1 — is "products first-class" actually felt?

**Result: yes, strongly.** The opening sentence defines *product* before anything else; the backbone is introduced as "seven products, not twenty-five components" (line 22); "## The products" (line 66) is the literal spine; every table's first column is a product; the cross-product build order (line 213) and the top-ten (line 251) are both keyed to products. Phase/wave language is correctly suppressed.

Two residual leaks where non-product framing competes:

[MINOR] lines 245 / 58 — "lands in the **builds-itself phase**" and "deferred to the **builds-itself phase**" — "phase" is exactly the vocabulary goal 1 wants suppressed. A first-time reader has not been told what "the builds-itself phase" is — it is named twice as if already defined but never introduced. Suggested fix: replace with a product/capability reference, e.g. "deferred until the digital-twins product is built" or "deferred to after the first self-build closes," so the framing stays in products and milestones, not phases.

[MINOR] line 20 — "defer all the **breadth** (extra linters, full observability, twin fidelity, self-optimization) until the slice closes" — "breadth" vs "the backbone slice" is a clean product-neutral framing and is fine; noting only that the document leans on "the slice" / "the vertical slice" as an undefined-on-first-use shorthand (line 20) before the seven-product breakdown that gives it meaning arrives two paragraphs later (line 22). Minor reading-order friction; acceptable.

---

## Cross-references — orphaned / broken anchors

[MAJOR] line 128 — "defers the *contract* … to the [bead-type schema product](**#bead-type-schema**) (C19/C20)" — **broken anchor.** There is no heading whose slug is `bead-type-schema`; "Bead-type schema" exists only as a *table-row label* (lines 89, 194), which does not generate an anchor. The link resolves to nothing. Suggested fix: either promote the bead-type schema to its own `###`/`####` heading and link to that, or repoint the link to `#the-remaining-custom-products` (where C20's edge actually lives) or `#two-cycles-broken-by-an-interface-freeze` (which discusses C19/C20). 

[MAJOR] line 154 — "the [counterfactual-replay](**#counterfactual-replay**) driver (C49)" — **broken anchor.** Same failure mode: "Counterfactual replay" is only a table-row label (lines 98, 182), not a heading, so `#counterfactual-replay` resolves to nothing. Suggested fix: repoint to `#observability-self-heal-and-self-optimization-products` (the section containing C49 at line 182) or `#the-remaining-custom-products`, or give C49 a heading.

[MINOR] line 245 — "[digital-twins product](#the-remaining-custom-products)" — the anchor *resolves* (the heading exists at line 185) but the **link text and target disagree**: a reader clicking "digital-twins product" lands on a generic "remaining custom products" table and must hunt for the C44/C45 rows. Mildly misleading but not broken. Suggested fix: make the link text match the destination ("the remaining custom products"), or split out a digital-twins heading.

Verified-good anchors (no action): `#build-order-across-products` (line 5 → 213), `#gas-city--gc-binary-mit` (line 24 → 106; em-dash-with-spaces correctly slugs to `--`, backticks and parens dropped), `#two-cycles-broken-by-an-interface-freeze` (line 112 → 132).

---

## Clarity defects

[MINOR] lines 58 / 245 / 276 — "**decision D-20**" is cited three times as load-bearing (it is *the* reason the fence splits and is mandatory before unattended runs) but is **never glossed in this document**. A first-time reader of this doc alone has no idea what D-20 is or where to find it. It is a real corpus-wide decision ID (used across `_meta/`), so this is a navigation gap, not a fabrication. Suggested fix: on first use (line 58) add a half-clause — "decision D-20 (the boundary-typing-first ruling in the decision ledger)" — or link it, so the reference is self-sufficient.

[MINOR] line 12 vs line 39 — the doc states two different "depth" numbers without distinguishing them on first read: line 12 "the deepest chain is **ten**" (component depth) vs line 39 caption "Depth is **~5 product-levels**, not 25 steps" (product depth). Both are correct and measure different things, but a newcomer hits "ten" then "~5" within 30 lines and cannot tell whether one supersedes the other. Suggested fix: label each explicitly — "ten *components* deep" at line 12 (line 237 already does this well) and "~5 *product*-levels" reads fine; the fix is just to add "components" at line 12.

[MINOR] line 57 — "C53's milestone is 'scenario set (C30) **run (C31)** + judged (C32) → satisfaction (C33)' (**C53 §AC-9**)" — the inline acceptance-criterion citation `C53 §AC-9` (and `AC-2` at line 130) is corpus shorthand a first-time reader cannot resolve from this doc. Same class as D-20. Low severity since the surrounding prose conveys the meaning without needing to chase the citation. Suggested fix: none required, or one-time note that §AC-N refers to acceptance criteria in the component inventory.

[MINOR] line 162 — the Inspect AI table's "Needs" column lists raw component IDs (e.g. "C17, C42") with no in-row gloss, whereas the Gas City table (lines 110-126) pairs every "Needs" entry with prose. Mostly fine because the IDs are defined elsewhere, but the columns are never explicitly explained at the table head ("Needs" = depends-on; "Notes" = what adoption means). Suggested fix: one sentence before the first product subsection table explaining the shared `Component | Needs | Notes` column contract.

[MINOR] line 3 — "(the two functional run-flow edges that the strict graph misses are called out explicitly where they appear)" — forward-references a concept ("run-flow edges the strict graph misses") that is not explained until line 59 (Ring 2). A first-time reader hits a promissory parenthetical they cannot yet cash. Acceptable as a teaser; flagged only as reading-order friction.

---

## Human-scoped-deliverables lens (applied lightly)

[MINOR] lines 239-242 — the critical-path Mermaid diagram has **10 nodes**, exceeding the ≤7-element guideline. Mitigating: it is a single linear chain whose entire point is to show "ten deep," so collapsing it would defeat its purpose. Diagram 1 (6 nodes) and diagram 2 (7 nodes) are within bounds. Suggested fix: optional — keep as-is given the chain's pedagogical role, or render the middle of the chain as a condensed "… ×N …" segment if strict compliance is wanted.

[OK] Vocabulary discipline — terms are corpus terms (Gas City, beads, rigs, the fence, gene-transfusion, the hinge), not invented jargon. No quantitative time estimates anywhere; effort is consistently "abstract effort" / tiny-low-medium-high (lines 253, 255-266). Both pass.

---

## Verdict

**accept-with-named-amendments.**

Rationale: The document achieves both stated goals well — "products first-class" is structurally felt, not merely asserted (every table is product-keyed, the backbone is reframed as seven products before any component list), and the change-narration sweep is genuinely clean, with no conversation-anchoring residue. It is not, however, accept-as-is: two cross-references (`#bead-type-schema` at line 128 and `#counterfactual-replay` at line 154) are **broken anchors** pointing at table-row labels that generate no heading slug — a first-time reader who clicks them goes nowhere, and these are the highest-priority fixes. The two "builds-itself **phase**" mentions (lines 58, 245) reintroduce exactly the phase vocabulary goal 1 suppresses and should be reworded to product/milestone language. The remaining items (undefined D-20, the ten-vs-~5 depth labels, unexplained table columns) are minor clarity polish. Fix the two broken anchors and the two "phase" leaks and the document is fully accept-as-is.
