# Adversarial review — C12 Formula / Pipeline-File Format (Track A, sweep 1)

Reviewer persona: Subsystem Adversary — Workflow Engine
Target: spec/C12-formula-pipeline-file.md + plan-faithful/C12-formula-pipeline-file.md
Charter: Track A (single canonical track) → attack FIDELITY and COMPLETENESS only, not the design,
**plus** the capability-for-principle bar (HANDOFF §2): flag any addition that hardens existing Gas City
stack capability rather than delivering NEW capability tied to a 12-principle. G11 posture: every "Gas City
native" claim is unverified; the spec must NOT bind to invented `gc` schema details.

## Findings

### RC12-01 — major — `$epic_id`/`$rfc_path`/Ralph-loop/human-gate exemplars are NOT Gas City; the spec leans on them as if they constrain the Gas City TOML formula format
**Claim.** §3.1, §3.1 [FAITHFUL-FILL] (parameters), §3.1 [FAITHFUL-FILL] (loop topology), §3.1 gate-nodes
row, and §5/§8 repeatedly cite "the exemplar pipeline files it cites (`"Implement epic $epic_id"`,
`"Break $rfc_path into an epic"`, one-shot-specs:62–63)" and the "Ralph-loop one issue at a time" /
"human-gate pipeline" (one-shot-specs:62, :65) as evidence for what a *Gas City formula* declares
(parameters, bounded loops, gate nodes).
**Evidence.** one-shot-specs lines 62–65 are `pipeline.dot` / `branching.dot` / `human-gate.dot` files from
**attractor-pi-dev (James Hugman, TypeScript/pi.dev)** and the `$epic_id`/`$rfc_path` strings live in those
**`.dot`** exemplars — not in any Gas City TOML formula. one-shot-specs:81, which the same spec cites for the
"design→plan→implement→review→test chain," explicitly states: *"Gas Town / Gas City / Wasteland publish no
one-shot application specs."* So the parameter syntax (`$slot`), the loop construct, and the gate-as-node
shape are inferred from a **different tool's DOT format** and asserted onto Gas City's TOML grammar. This is a
G11-class fidelity risk one layer deeper than the spec's own G11 note: the spec correctly flags that the *key
names* are Gas City's-and-unverified, but it still imports concrete *exemplar evidence* from a non-Gas-City
source to justify that the elements exist at all.
**Fix (applied, partial).** Re-tagged the parameters / loop / gate FAITHFUL-FILLs and §3.1 source cells to
state that the `$epic_id`/Ralph-loop/human-gate exemplars are **DOT pipeline files from attractor-pi-dev /
Fabro, not Gas City formulas** (one-shot-specs:81 "Gas City publish no one-shot specs"), so they are read as
*cross-implementation evidence that DAG-pipeline formats carry these elements* — not as proof of the Gas City
TOML shape. The minimal-fill reasoning (a template must carry slots; iteration must be bounded/lintable)
stands on its own; only the misattributed "Gas City cites these" framing was corrected.

### RC12-02 — major — "DAG validation on load / acyclicity invariant" is presented as a C12-defined property, risking a HARDENING addition over what Gas City + C15 already do
**Claim.** §3.3 outbound ("acyclicity guaranteeing a topological execution order"), §4 ("the **acyclicity
invariant** (DAG) and **node-binding resolvability** … are the static invariants a formula must satisfy"),
§6 ("C12's contribution is to define the **acyclicity + binding-resolvability invariants**"), and §8 AC-1
("declares nodes + edges, and **is acyclic**").
**Evidence.** Two faithfulness concerns. (a) v4 names the artifact a "DAG file" (README:128) as a
*description*, and assigns structural rule-checking to the **Mammoth 21-rule workflow linter (C15)** via DOT
(README:134) — it does not state that the *format spec* C12 carries a load-time validator or that C12
"defines invariants." The spec is mostly careful (§6 says detection is C15/C16/C13, "not a C12 runtime
check"), but the repeated "C12 defines the acyclicity invariant" framing drifts toward C12 owning a
validation capability. (b) Under the capability bar: DAG well-formedness / acyclicity checking is precisely
the kind of structural guarantee Gas City's loader + C15 already provide; a C12-owned "invariant the format
enforces" would be **hardening on existing stack capability**, not a new principle-tied capability. The
faithful position is that C12 *names* acyclicity as the defining graph property (so C13/C14/C15 can rely on
the word "DAG") and **defers all enforcement** to the runner-load + C15.
**Fix (applied).** Reworded §3.3, §4, §6, and §8 AC-1 so that acyclicity/binding-resolvability are described
as **properties a well-formed formula has** (the defining DAG property the format names), with enforcement
explicitly owned by the Gas City loader (C01) + C15 (structure) + C16 (discipline) + C13 (instantiation),
and C12 introducing **no validator of its own**. Removed the "C12 defines the invariants the linters check
against" phrasing that implied a new C12 capability.

### RC12-03 — minor — "Node kind tag" risks being read as a C12-invented field (the same `[FAITHFUL-FILL]` C17 already carries); needs to be scoped as a single shared, unverified tag, not a C12 addition
**Claim.** §3.1 "Node kind tag" row + §1 responsibilities ("the per-step node kind … all live *in the
formula*") + §8 AC-4 present a per-node `kind` field as something C12 records.
**Evidence.** v4 never gives an explicit node-kind field (correctly tagged [FAITHFUL-FILL] in C17 §3.1 and
cross-referenced here). The risk is double-counting: C12, C16, and C17 each describe "the node-kind tag," and
C17's own review/OQ already flags that the tag's *home* (C12 formula-node entry vs. C02 `[[tool]]` block) is
an **open reconciliation** (C17 §3.1 consistency note; C17 OQ-2). C12 asserts the field lives "in the
formula" as if settled. Under the capability bar this is not new capability — it is the minimal machine-
readable distinction the C16 discipline linter (a principle-P4 capability) needs; that is legitimate, but it
must be presented as *one shared, sweep-2-reconciled, Gas-City-unverified tag*, not a C12-owned fact.
**Fix (applied).** Qualified §3.1 node-kind row and §1 to mark the per-node kind tag as the **shared
[FAITHFUL-FILL] tag co-owned with C16/C17** whose field home is an open reconciliation (C12 §9 item 4 / C17
OQ-2), not a settled C12 field, and that its existence is justified solely because C16's F52 discipline check
(P4) is undefinable without it. The existing §9 item 4 already raises the reconciliation; this just stops §3
from over-asserting.

### RC12-04 — minor — §2 dependency table lists C50 promotion-gate as a downstream consumer "depending on C12," but C12 does not actually carry that as a stated C12 contract; the cite is fine, the framing slightly overreaches
**Claim.** §2 row "Downstream (gate) | C50 promotion gate | A promotion gate is itself 'a Gas City formula
with a statistical gate' (README:276; inventory C50 depends on C12)."
**Evidence.** README:276 and the inventory (C50 `Depends on: C48, C12`) both check out — this is a *correct*
citation. The minor issue: it is listed identically to first-order consumers (C13/C14/C15/C16) when C50's
dependence is "a promotion gate happens to be authored as a formula," i.e. C50 is *an instance of* the C12
format, not a component C12 exposes a distinct interface to. Not a fidelity error; a precision nit.
**Fix (applied).** Left the row (citation is correct) but appended a half-clause clarifying C50 is *an
instance of* the formula format (like any other formula), not a consumer of a dedicated C12 interface —
parallel to how C17 §2 distinguishes "instances" (`a tool node`) from interface consumers.

### RC12-05 — minor — G06 resolution is sound and correctly scoped, but one sentence asserts the vocabulary table lists convoy/order/formula as "distinct terms with distinct generic equivalents" — verify-clean, keep
**Claim.** §3.3 [AMBIGUITY: G06] picks Reading A (C12 = single-formula DAG only; convoy/order owned
elsewhere) on the strength of the inventory routing orders to C40 and "the vocabulary table (AI-CONTEXT §3.3)
lists *convoy*, *order*, and *formula* as **distinct** terms with distinct generic equivalents."
**Evidence.** Verified against AI-CONTEXT §3.3: `formula | pipeline file / workflow DAG template`,
`convoy | batched workflow`, `order | event-triggered workflow` are indeed three separate rows. Inventory C40
is "Durable workflow engine (Orders)." The G06 resolution is faithful, minimal, and correctly defers the full
glossary to C07 (which owns G06 system-wide). **No fix needed** — recording as a positive check so the
verdict reflects that C12's only assigned gap is properly addressed.

### RC12-06 — minor — "version-controlled" is faithful, but the spec must not let it slide into a "versioned schema" capability claim; check-clean with one guard added
**Claim.** §1/§4/§7 repeatedly call the formula "version-controlled" and note formulas "ship in packs."
**Evidence.** "version-controlled" (README:128) and packs as "distributable methodology bundle" (AI-CONTEXT
§3.3) are both accurate. The capability-bar watch-item: this must remain *the file lives in git / a pack*
(an existing-stack property — git + Gas City packs), **not** an invented per-formula schema-version field or
a C12-owned migration contract. The spec does **not** currently invent a schema-version field (good; the
migration tail is correctly left to C01/AI-CONTEXT §3.5). Flagging only to ensure sweep-2 does not add one
under the banner of "hardening the format."
**Fix (applied, light).** Added a one-line guard in §4 (lifecycle) that version-control is git + pack
(existing stack), and C12 introduces **no schema-version field of its own** at sweep-1 (any such field would
be a sweep-2 decision gated on the real `gc` format, not a faithful addition here).

## Deferred (needs orchestrator decision)

- **DEFERRED — node-kind field home (C12 vs C02).** RC12-03 corrects the *over-assertion*, but the actual
  ruling — does the canonical node-kind tag live in the C12 formula-node entry or the C02 `[[tool]]` block? —
  is a cross-component contract spanning C12/C16/C17/C02 and is architecturally significant. It is already an
  OQ in C12 §9 (item 4) and C17 OQ-2. Left for the integrator pass; not unilaterally resolved here.
- **DEFERRED — convoy/order ownership confirmation.** RC12-05 confirms C12's Reading-A *scoping* is faithful,
  but the binding confirmation that C40 (Orders) and an as-yet-unassigned convoy owner accept the boundary
  (C12 §9 item 3 / plan T7) is a cross-component sign-off, not a C12-local edit. Deferred to integrator.

## Verdict
**accept-with-fixes.** The spec is faithful, well-traced, and correctly identifies its own top risk (G11 —
the Gas City formula schema is unverified) and its only assigned gap (G06 — resolved minimally, Reading A,
deferring the glossary to C07). No invented architecture, no relitigation of D-1..D-5, no violation of a
binding decision. The fixes are all of one kind: *stop asserting an adopted/inferred property (acyclicity
enforcement, the node-kind field, the `$epic_id` exemplars' provenance) as a settled C12-owned fact or a new
C12 capability*, keeping C12 a thin format-naming artifact whose enforcement and schema details defer to Gas
City (C01) + the linters (C15/C16) + sweep-2 verification. Two cross-component rulings (node-kind home,
convoy/order ownership) are deferred to the integrator as architecturally significant. No fidelity blockers.
</content>
</invoke>
