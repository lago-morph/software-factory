# C07 — Vocabulary & Glossary  (Spec, canonical track)

> Source: README §Part 4 (Gas City placement tables, lines ~104–278), README §Part 5 (risk register: "Vocabulary lock-in to Gas City", line 516; mitigation "Glossary; pair sessions", line 622), README line 384 (gene-transfusion def), README line 664 (v3 vocabulary reference); AI-CONTEXT §3.2 ("nine concepts" table, lines 79–93), §3.3 (vocabulary translation table, lines 95–112), §3.4 (smallest-install term inventory, lines 114–122), §3.6 (vocabulary-free runtime, lines 131–135); component-inventory C07 row (line 19); ambiguities-and-gaps §G06 (line 23); v3 `architectures/v3/build-guide/01-vocabulary.md` (corpus-name discipline + translation tables).
> Inventory ID: C07   Kind: cross-cutting   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C07 is the **single canonical glossary** for the Software Factory v4 / Gas City vocabulary. It is the
authoritative definition of every load-bearing term — `city`, `rig`, `formula`, `molecule`, `pack`,
`sling`, `wisp`, `convoy`, `Order`, `bead`, `Health Patrol`, `convergence gate`, `model stylesheet`,
`gene transfusion`, etc. — each paired with its **generic equivalent** and its **corpus provenance**.
Its job is to give every other spec, prompt, human-facing doc, and linter **one agreed meaning per
term**, so that no two components drift on what (e.g.) "molecule" means, and so a reader of README alone
can resolve a Gas City term without holding the AI-CONTEXT companion in their head (the G06 defect).

It exists because v4 explicitly names two pieces of vocabulary debt as risks:
1. **Vocabulary lock-in to Gas City** — "Cities, rigs, formulas, molecules. Real cognitive load.
   Recoverable but irreversible without major rework." (README:516). The stated mitigation is a
   **glossary** + pair sessions; the cost is "front-loaded and recoverable" (AI-CONTEXT:112, README:622).
2. **Undefined-term debt** — G06: ~13 load-bearing Gas City terms are used in README Part 4 *before*
   AI-CONTEXT §3.2/§3.3 defines a subset, and the vocabulary table "lives only in the companion."

C07 is the component that **discharges both** by being the one place the definitions live.

### What C07 is NOT
- **Not a runtime component.** It owns no process, no port, no control loop, no live state. It is a
  *cross-cutting reference artifact* (inventory `Kind: cross-cutting`), consumed at author-time and
  lint-time, not at request-time.
- **Not the spec linter, the workflow linter, or the discipline linter.** C07 *supplies the term
  registry* those linters key against; the lint *rules* live in C10 / C15 / C16. F38 ("Vocabulary lint
  debt") is owned by C10's EARS linter (F-MODE-COVERAGE:74), not C07. C07 is the data; the linters are
  the enforcement.
- **Not a translation/rename layer.** v4 keeps the Gas City terms as primary surface vocabulary
  (AI-CONTEXT §3.3 maps Gas City → generic *for understanding*, it does not rename the runtime). C07
  records both columns; it does not mandate which column code uses. The runtime stays
  "vocabulary-free" at the `runtime.Provider` interface (AI-CONTEXT:133) — that is a property of C01,
  and C07 merely documents it.
- **Not a methodology/principle definition store.** Principles (P1–P12) and F-modes (F1–F58) have their
  own canonical homes (AI-CONTEXT principle map; F-MODE-COVERAGE). C07 may *cross-reference* them but
  does not redefine them.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Depends on | **C01** (`gas-city-substrate`) | C01 is the source of the runtime terms C07 catalogs (the "nine concepts", AI-CONTEXT §3.2). C07 documents C01's vocabulary; it does not change it. (inventory: C07 `Depends on → C01`) |
| Consumed by | **C08** (`spec-artifact`), **C09** (`prompt-template-binding`) | Specs and prompt templates use the canonical terms; C07 is the dictionary they resolve against. |
| Consumed by | **C10** (`spec-linter-ears`), **C15** (`workflow-linter`), **C16** (`discipline-linter`) | Linters key vocabulary checks (e.g. EARS vocab-lint, F38) against C07's term registry. |
| Consumed by | **C12/C13** (`formula` / `molecule`) | The formula/molecule artifacts *are* two of the glossary's load-bearing terms; their specs must agree with C07's definitions. |
| Consumed by | every human-facing doc | README and onboarding material link to C07 so a reader resolves terms in one hop (the G06 fix). |

C07 sits at the **foundation tier** (inventory: `Foundational? yes`; build Batch 1, component-inventory
line 107) precisely because everything downstream references its terms. It is authored early and frozen
early so dependents build against a stable vocabulary.

## 3. Interfaces / contracts

C07's "interface" is a **document + a machine-readable term registry**, plus the conventions for using
them. At sweep 1 these are *named and described*; concrete schema/signatures are sweep 2.

### 3.1 The canonical glossary document (human-facing)
A single Markdown artifact (the human face of C07) containing, for each term: the **Gas City term**, a
**definition**, the **generic equivalent**, the **corpus provenance** (which corpus author/source the
term comes from), and the **principles** it serves where applicable. This is the README-resolvable
table that G06 says is missing from the human doc. Provenance discipline follows the v3 vocabulary
convention (`v3/build-guide/01-vocabulary.md`): prefer corpus names, record the mapping, never silently
invent jargon.

### 3.2 The machine-readable term registry (tool-facing)
> [FAITHFUL-FILL] v4 prescribes "a glossary" (README:622) but does not name a file format. The minimal
> consistent choice is a **single TOML term registry** (one entry per term), because v4's entire
> extension/config surface is TOML (AI-CONTEXT §3.2 row 4 "Layered TOML"; §3.4 `pack.toml`/`city.toml`;
> packs are "TOML + tool-node binaries + templates", C02). Using TOML keeps C07 inside the established
> substrate format and lets linters (C10/C15/C16) load it the same way they load other config. Each
> entry: `term`, `definition`, `generic_equivalent`, `provenance`, `principles[]`, `aliases[]`,
> `status` (active|deprecated). The human glossary in §3.1 is generated from / kept in sync with this
> registry (single-source-of-truth discipline).

### 3.3 Consumption contract
- **Author-time:** spec/prompt authors look up a term, use it with C07's meaning. One term → one meaning
  (invariant below).
- **Lint-time:** linters load the registry, flag terms used outside the registry or with a non-canonical
  alias. C07 supplies the allow-list; the linter supplies the verdict.
- **Read-time (human):** README/onboarding link to the glossary doc; a single hop resolves any term.

### 3.4 Invariants
- **One canonical meaning per term.** No term has two definitions across the corpus; collisions are a
  defect C07 must resolve (e.g. the "layer" collision G01, the "phase" collision G02 — see Open
  Questions; C07 records but does not unilaterally re-architect those).
- **Every load-bearing Gas City term in README Part 4 appears in C07.** This is the G06 acceptance bar.
- **Bidirectional completeness with AI-CONTEXT §3.2/§3.3.** Every term in the "nine concepts" table and
  the translation table appears in C07 with at least the same content (C07 is a superset, never a
  subset).
- **Provenance is recorded for every term** (which corpus source it traces to), per v3 discipline.

## 4. Data model / state

C07 owns **definitional state only** — the term registry — and no runtime/mutable state.

### 4.1 The canonical term set (v4-sourced)

From **AI-CONTEXT §3.2 "nine concepts"** (5 primitives + 4 derived) and **§3.3 translation table**, plus
the load-bearing README Part 4 terms named in **G06**. The authoritative seed set:

| Term | Definition (v4-sourced) | Generic equivalent | Source |
|---|---|---|---|
| Session | Stable runtime backed by Provider (tmux/k8s/subprocess/exec) | runtime/session | AI-CONTEXT §3.2 #1 |
| Bead / Bead Store | Durable typed work-graph (Dolt or file); a `bead` is a node of typed work | work item / work-ledger | AI-CONTEXT §3.2 #2; v3 "work ledger" |
| Event Bus | Append-only JSONL with monotonic seq | event log | AI-CONTEXT §3.2 #3 |
| Config | Layered TOML; section presence = feature flag | config / feature flags | AI-CONTEXT §3.2 #4 |
| Prompt Template | Go `text/template` markdown | prompt template | AI-CONTEXT §3.2 #5 |
| Messaging (Mail + Nudge) | Mail = durable; Nudge = ephemeral | inter-agent messaging | AI-CONTEXT §3.2 #6 |
| Formula | TOML DAG template (a workflow) | pipeline file / workflow DAG template | AI-CONTEXT §3.2 #7, §3.3 |
| Molecule | A formula instantiated into a live bead-tree | instantiated workflow / bead-tree | AI-CONTEXT §3.2 #7, §3.3 |
| Sling (Dispatch) | Routes a bead/wisp to an agent or pool | dispatch / route | AI-CONTEXT §3.2 #8, §3.3 |
| Health Patrol (Controller + Convergence) | Per-tick reconciler; bounded convergence with gates | reconciler / control loop | AI-CONTEXT §3.2 #9 |
| Convergence gate | The bounded gate inside Health Patrol that admits/blocks a tick's progress | gating / sync primitive | AI-CONTEXT §3.2 #9; §3.3 "wait" |
| City | A workspace | workspace | AI-CONTEXT §3.3 |
| Rig | An agent worker role | agent worker role | AI-CONTEXT §3.3 |
| Pack | Distributable methodology bundle (TOML + tool-node binaries + templates) | methodology bundle / plugin | AI-CONTEXT §3.3; C02 |
| Convoy | Batched workflow (atomic multi-bead dispatch — a Gas City sling concept referenced by C05) | batched workflow | AI-CONTEXT §3.3; C05 (D-8) |
| Wisp | Unit of dispatchable work | dispatchable work unit | AI-CONTEXT §3.3 |
| Wait | Gating / synchronization primitive | sync primitive | AI-CONTEXT §3.3 |
| Order | Event-triggered workflow (survives crashes/retries) | durable/event-triggered workflow | AI-CONTEXT §3.3; C40 (Gas City Orders) |
| Polecat | A specific role in the Gas Town pack (not in the interface) | (pack-specific role) | AI-CONTEXT §3.3 |
| Mayor | Senior coordinator agent role (Gas Town pack vocab) | senior coordinator role | AI-CONTEXT §3.3 |
| Model stylesheet | CSS-like syntax for routing pipeline nodes to different models (cost/family-aware) | model routing rules | README:189; v3 vocab (Fabro); C29 |
| Gene transfusion | Applying a working pattern by pointing the agent at a concrete exemplar and asking it to reproduce the behavior, instead of describing it from scratch. **Definition is analogy-only (G07):** v4 gives no operational success/completeness predicate for "behaves like the exemplar"; that predicate is owned and unresolved at **C51**. The one-liner is not a complete definition. | transfusion / pattern-from-exemplar | README:384, :496; v3 vocab; G07 → C51 |
| Gas City placement | (README authoring convention) where a v4 component maps onto the Gas City substrate | "where this lives in Gas City" | README Part 4 tables |
| Layer (overloaded — G01) | **Two readings, both recorded, no winner picked (faithful).** *Sense 1 — three-layer architecture:* (1) LLM client, (2) agent loop, (3) pipeline engine, + persistence (README Part 3). *Sense 2 — numbered "Layer 0–6" principle tier* (AI-CONTEXT §6/§7; README Part 6 "Layer 2/5/6"). | sense 1: architecture tier; sense 2: principle grouping | README Part 3 / Part 6; AI-CONTEXT §6/§7; G01 |

> [FAITHFUL-FILL] **"Gas City placement"** appears in G06's term list but in v4 it is a *column header /
> authoring phrase* in README Part 4 tables, not a Gas City runtime primitive. The minimal faithful
> treatment is to record it as a **documentation convention** ("where component X slots into the Gas
> City + Claude Code substrate"), not as a runtime noun. Recording it satisfies G06's enumeration while
> not inflating it into a primitive v4 never defined as one.

> [FAITHFUL-FILL] Several terms (`bead`, `Order`, `convergence gate`, `model stylesheet`) carry their
> deeper definition in *other* component specs (C19/C20 for beads, C40 for Orders, C18 for convergence,
> C29 for the stylesheet). C07's faithful job is to hold the **one-line canonical definition + a pointer
> to the owning component**, not to duplicate those specs. This is the smallest choice that keeps one
> meaning per term without C07 becoming a second copy of the substrate.

### 4.2 Provenance / corpus-name discipline
Per `v3/build-guide/01-vocabulary.md`: v4 deliberately prefers corpus names over invented jargon, and
records the mapping. C07 inherits this discipline — each term notes whether it is (a) Gas City runtime
vocabulary, (b) a corpus term (Vincent / StrongDM / Shapiro / Willison / El Kaim / every.to), or (c) a
v4 documentation convention. The v3 translation tables (v3-pipeline jargon → plain name, lines 56–81)
are carried as **historical aliases** so older artifacts remain resolvable.

### 4.3 Lifecycle
- Born in Batch 1 (foundational), authored alongside C01/C02/C03 (inventory line 107).
- Versioned with the architecture; AI-CONTEXT §3.5 warns of "1–2 breaking pack-schema or formula-format
  changes per quarter," so terms can be **deprecated** (status flag), never silently deleted — old
  artifacts must still resolve a retired term to its replacement.

## 5. Behavior

C07 has no control loop. Its only "behavior" is the **resolve** and **lint-support** operations:

1. **Resolve(term) → definition** — a lookup against the registry, returning canonical definition +
   generic equivalent + owning component + provenance.
2. **Validate(text/spec) → vocabulary findings** — the linters (C10/C15/C16) iterate the terms used in
   an artifact and check each against the registry; unknown or non-canonical usage is a finding. C07
   provides the data; the linter performs the walk.
3. **Sync(registry) → human glossary doc** — regenerate / verify the README-facing glossary from the
   registry so the two never drift (single-source-of-truth).

## 6. Failure modes & handling

| F-mode / risk | Applies? | C07's role |
|---|---|---|
| **Vocabulary lock-in to Gas City** (README:516) | Yes (primary) | C07 *is* the named mitigation ("Glossary", README:622): records the generic equivalent for every Gas City term so the lock-in is documented and recoverable, never silent. |
| **G06 undefined-term debt** | Yes (primary) | C07 makes every README Part 4 term resolvable in one hop; closes the "table lives only in the companion" gap. |
| **F38 — Vocabulary lint debt** (F-MODE-COVERAGE:74) | Indirect | Owned by C10's EARS linter; C07 *supplies the term registry* the linter checks against. C07's failure here would be an incomplete/ambiguous registry. |
| **Term drift / dual meaning** (e.g. "layer" G01, "phase" G02) | Partial | C07 records the collision and the chosen canonical reading where v4 resolves it; where v4 does not, C07 flags it and defers to the owning doc (see Open Questions). C07 must not unilaterally re-architect a contested term. |

**Degraded behavior:** because C07 is author-time/lint-time, a stale or missing entry degrades gracefully
— a linter raises an "unknown term" finding rather than a runtime crash. The mitigation is registry
completeness (the acceptance bar below), not a runtime fallback.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security:** none direct; C07 is a read-only reference artifact with no privileged surface.
- **Cost:** addresses the *cognitive* cost v4 calls out — "Vocabulary is real cognitive cost but
  front-loaded and recoverable" (AI-CONTEXT:112). C07 is precisely the front-loading: pay once,
  resolve forever.
- **Scale:** trivial; the term set is on the order of tens of entries.
- **Observability/ops:** the only ops concern is **drift** — the registry and the human glossary and the
  per-component specs must agree. A CI check (sweep 2) verifies registry ⊇ {AI-CONTEXT §3.2/§3.3 terms}
  and that each owning-component spec's definition matches C07.

## 8. Acceptance criteria & test strategy

C07 is correct (sweep-1) when:
1. **Completeness — G06 bar.** Every load-bearing Gas City term used in README Part 4 (the G06 list:
   Gas City placement, pack, formula, bead, rig, molecule, sling, convoy, wisp, Order, Health Patrol,
   convergence gate, model stylesheet) appears in C07 with a definition + generic equivalent.
2. **Superset of the companion tables.** Every entry in AI-CONTEXT §3.2 ("nine concepts") and §3.3
   (translation table) appears in C07, with content at least as complete.
3. **One meaning per term.** No term resolves to two conflicting definitions; collisions are either
   resolved (with the v4-consistent reading + rationale) or explicitly flagged + deferred to the owning
   doc.
4. **Provenance recorded.** Each term notes its source (Gas City runtime / corpus author / v4
   convention), per v3 discipline.
5. **README-resolvable.** A reader of README alone can resolve every Part 4 term via a single linked
   glossary (the G06 fix is operationally verifiable: the glossary is linked from README and contains
   the term).

**Test strategy (sweep 1 = high-level):** a checklist test that diff's the C07 term set against
(a) the G06 list, (b) AI-CONTEXT §3.2/§3.3, and (c) a grep of README Part 4 for capitalized/code-spanned
Gas City nouns; any term in (a)/(b)/(c) absent from C07 is a failing case. (Concrete registry schema +
automated CI gate are sweep 2.)

## 9. Open questions

- **OQ-C07-1 (→ review-log):** The "layer" collision (G01: three-layer vs Layer 0–6) and the "phase"
  collision (G02) are vocabulary defects that surface in C07's scope, but resolving them re-architects
  meaning owned by other docs. Should C07 (a) record both readings and defer, or (b) be granted
  authority to pin the canonical reading? The canonical track's faithful default is (a) — record + defer — but this
  leaves two genuinely ambiguous terms in the canonical glossary. **Top open question.**
- **OQ-C07-2:** Registry file format and location (TOML registry assumed as [FAITHFUL-FILL]) needs
  ratification with C03 (config) so linters load it uniformly. Deferred to sweep 2.
- **OQ-C07-3:** Deprecation/versioning policy for retired terms given AI-CONTEXT §3.5's "1–2 breaking
  changes per quarter" — how long must a retired term remain resolvable? Deferred to sweep 2 / ops.

---

**[D-23 substrate-verified — gascity-prototype@b14c278, 2026-05-25]**

**F11 — Gastown pack concrete role names ↔ v4 generic vocabulary (CONFIRMS-CLAIM; vocabulary table addendum):**
Verified against the Gas City prototype (lago-morph/gascity-prototype@b14c278, 2026-05-25):
the bundled `gastown` pack instantiates v4's generic agent-role vocabulary with these concrete
names: `mayor` = coordinator; `deacon` = health-patrol; `boot` = bootstrap agent; `witness` =
per-rig observer; `refinery` = per-rig reviewer (spawned on demand); `polecat` / `crew` = worker
variants; `dog` = pool worker (min=0, spawned on dispatch). All six city-scope named agents were
verified running as real `claude` processes in distinct tmux panes under the controller (2026-05-25
stand-up). The `gastown` pack is the Phase-0 reference implementation of v4's role taxonomy.
C07's vocabulary table (§4.1) notes `Polecat` and `Mayor` as pack-specific roles; this fact
extends those entries: `deacon`, `boot`, `witness`, `refinery`, `crew`, and `dog` are equally
`gastown`-specific concrete names for v4's generic roles.
