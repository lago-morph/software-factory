# C07 — Vocabulary & Glossary  (Spec, Track A)

> Source: README §Part 4 (Gas City placement tables, lines ~104–259); AI-CONTEXT §3.2 ("nine concepts"), §3.3 (vocabulary translation table), §3.6 (vocabulary-free runtime); AI-CONTEXT §10/§9 (gene transfusion def, line 384); AI-CONTEXT §14 (risk register, line 622 "Vocabulary cost … Glossary"); v3 `build-guide/01-vocabulary.md` (corpus-name discipline, translation tables); component-inventory C07 row.
> Inventory ID: C07   Kind: cross-cutting   Status: sweep-1
> Track: A (faithful)

## 1. Purpose & responsibility

C07 is the **single canonical glossary** for the Gas City / Software Factory vocabulary. It is the
authoritative definition of every load-bearing term — `city`, `rig`, `formula`, `molecule`, `pack`,
`sling`, `wisp`, `convoy`, `Order`, `bead`, `Health Patrol`, `convergence gate`, `model stylesheet`,
`Gas City placement`, `gene transfusion`, etc. — together with each term's **generic equivalent** and
its **corpus provenance**. Its job is to make every other spec, prompt, and human-facing doc resolve a
term to one agreed meaning, so that no two components drift on what (e.g.) "molecule" means.

**Responsibilities**
- Hold one entry per term: canonical term, definition, generic equivalent, source citation, and the
  C-ID(s) that own/use the concept.
- Be the **lookup authority** every other component and the spec linter (C10) defer to for term
  resolution and undefined-term detection.
- Carry the **Gas City ↔ generic** translation table (AI-CONTEXT §3.3) and the **v3-jargon → corpus-name**
  translation table (v3 §52) so older docs and external readers map onto the canonical set.
- Mitigate two named debts from the inventory: **vocabulary lock-in** (terms with no escape hatch to a
  generic equivalent) and **undefined-term debt** (load-bearing terms used before definition — G06).

**Explicitly NOT**
- NOT a runtime component: it owns no live state, no control loop, no dispatch. It is a static,
  version-controlled reference artifact (cross-cutting "kind" per inventory).
- NOT the spec linter. C07 *supplies the term set*; C10 (spec-linter-ears) *enforces* usage. C07 does not
  run lint rules itself.
- NOT a vocabulary *inventor*. Per v3 §3 discipline, where the corpus already names a concept, C07 records
  the corpus name and demotes invented jargon to an alias — it does not coin new terms.
- NOT the formula/pack format definitions (C12/C02) — it defines the *words*, those components define the
  *artifacts* the words denote.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C01** Gas City substrate | Vocabulary derives from Gas City's nine concepts + term set; C07 is downstream of C01's existence but adds no runtime coupling. |
| Downstream (serves) | **C10** spec-linter-ears | Linter consumes the canonical term set for undefined-term / vocab-debt detection (F38). |
| Downstream (serves) | **C02, C12, C13, C05** | pack / formula / molecule / sling specs each cite C07 for their headline noun. |
| Downstream (serves) | All human-facing docs (README) | README Part 4 uses ~13 terms with no inline glossary (G06); C07 is the resolution target. |

C07 is **foundational** (inventory: yes) and sits in **Batch 1** — authored fully in parallel with the
other load-bearing primitives, because everything downstream references its terms.

## 3. Interfaces / contracts

Sweep 1 — interfaces named and described (signatures deferred to sweep 2).

1. **Glossary entry record** — the unit of the glossary. Named fields (described, not yet typed):
   `term` (canonical), `definition`, `generic_equivalent`, `source` (doc + section), `owning_components`
   (C-IDs), `aliases` (deprecated/jargon names mapping to this term), `principles` (Pxx the concept
   serves, where AI-CONTEXT supplies them).
2. **Lookup interface** — "resolve a term to its entry." Given a surface string, return the canonical
   entry or "unknown." Used by C10 and by doc-build tooling.
3. **Translation interface** — "map a generic or jargon term to the canonical Gas City term, and back."
   Backed by the two translation tables (AI-CONTEXT §3.3; v3 §52).
4. **Term-set export** — the closed set of canonical terms, consumed by C10's undefined-term rule.

**Invariants**
- Every canonical term has exactly one entry; every alias maps to exactly one canonical term.
- Every entry cites a v4 (or corpus) source — no uncited term may be canonical.
- Every Gas City term has a `generic_equivalent` (the anti-lock-in invariant: AI-CONTEXT §3.3 + §3.6
  "deliberately vocabulary-free" runtime makes the generic mapping always available).

## 4. Data model / state

C07 owns **one static, version-controlled artifact**: the glossary table. No mutable runtime state.

**Seed content (faithful, drawn directly from v4 + corpus sources):**

| Term | Definition (source) | Generic equivalent | Source |
|---|---|---|---|
| city | the workspace/runtime instance | workspace | AI-CONTEXT §3.3 |
| rig | an agent worker role | agent worker role | AI-CONTEXT §3.3 |
| formula | TOML DAG template describing a workflow | pipeline file / workflow DAG template | AI-CONTEXT §3.2/§3.3; C12 |
| molecule | a formula instantiated into a live bead-tree for one run | instantiated workflow / bead-tree | AI-CONTEXT §3.2/§3.3; C13 |
| pack | distributable methodology bundle (TOML + tool-node binaries + templates) | distributable methodology bundle | AI-CONTEXT §3.3; C02 |
| convoy | a batched workflow | batched workflow | AI-CONTEXT §3.3 |
| sling | dispatch — routes a bead/wisp to an agent or pool | dispatch / route | AI-CONTEXT §3.2/§3.3; C05 |
| wisp | a unit of dispatchable work | unit of dispatchable work | AI-CONTEXT §3.3 |
| wait | gating / synchronization primitive | gating / synchronization primitive | AI-CONTEXT §3.3 |
| Order / order | an event-triggered workflow | event-triggered workflow | AI-CONTEXT §3.3 |
| bead | a node in the durable typed work-graph (work ledger) | work-ledger task node | AI-CONTEXT §3.2 ("Bead Store"); v3 §34 |
| Health Patrol | per-tick reconciler; bounded convergence with gates | controller + convergence loop | AI-CONTEXT §3.2 (#9); C18 |
| convergence gate | a bounded gate inside Health Patrol convergence | reconciler gate | AI-CONTEXT §3.2 (#9); C18 |
| Gas City placement | where a capability slots into Gas City + Claude Code (native / pack / custom) | deployment-mapping note | README Part 4 placement tables |
| model stylesheet | CSS-like routing of pipeline nodes to models; cross-family enforcement lives here | model-routing config | README:189; v3 §50 |
| gene transfusion | reproduce a behavior by pointing the agent at a concrete exemplar | exemplar-driven pattern transfer | AI-CONTEXT line 384; v3 §45 |
| polecat / Mayor | specific Gas Town **pack** roles (not in the interface) | (pack-specific role) | AI-CONTEXT §3.3 |

> [FAITHFUL-FILL] The inventory and G06 name `wisp` and `convoy` as load-bearing, but the v4 docs give
> them only the one-line translation-table gloss. C07 records exactly that gloss as the definition and
> marks no richer meaning — the minimal consistent choice, since inventing detail would exceed what v4
> states. Their owning artifact-specs (e.g. C05 for sling/wisp routing) carry the operational detail.

> [FAITHFUL-FILL] `polecat`/`Mayor` are explicitly "Gas Town **pack** vocab, not in the interface"
> (AI-CONTEXT §3.3). C07 keeps them as entries but flags them **pack-scoped, not substrate** — the
> smallest faithful way to honor "not in the interface" while still resolving the term if a reader meets it.

> [FAITHFUL-FILL] The `source` and `owning_components` fields are an inferred entry shape; v4 never
> specifies a glossary *schema*, only the term/equivalent pairs. This is the minimal structure needed to
> make the artifact queryable by C10 and traceable per Track-A rule 5 (every claim cites a source).

## 5. Behavior

C07 has no runtime control loop. Its "behavior" is **build-time and authoring-time**:

- **Authoring**: when a component spec introduces a headline noun, it adds/updates the C07 entry rather
  than redefining the term locally.
- **Resolution at lint time**: C10 imports the term-set export; any load-bearing term in a spec/README
  not present in C07 (and not an alias) is an undefined-term finding (G06 / F38 mechanism).
- **Translation at read time**: doc tooling and external readers map jargon/generic terms to canonical
  terms via the translation interface.

(Sequence/state diagrams deferred to sweep 2 — sweep-1 altitude per BUILDER-BRIEF.)

## 6. Failure modes & handling

| F-mode | Relevance | Handling in C07 |
|---|---|---|
| **F38 — Vocabulary lint debt** (F-MODE-COVERAGE:74, "Addressed") | Directly C07's reason to exist. | C07 supplies the closed canonical term-set that C10's EARS-style linter checks against; deterministically detectable per F-MODE row. |
| **G06 — undefined-term debt** (ambiguities §"Undefined terms") | README uses ~13 Gas City terms before AI-CONTEXT defines a subset. | C07 is the inline-resolvable glossary; §4 seed table covers every G06-named term. **Resolved** (see §9 for the residual README-embedding question). |
| **Lock-in debt** (inventory C07 one-liner) | A term with no generic escape hatch traps the design in Gas City idiom. | Anti-lock-in invariant (§3): every Gas City term carries a `generic_equivalent`, enabling future substrate substitution per AI-CONTEXT §3.6. |
| Vocabulary cost / team friction (AI-CONTEXT:622) | Real cognitive cost. | Glossary is the named mitigation in v4's own risk register; cost is "front-loaded and recoverable" (§3.3). |

Degraded behavior: if a term is used but absent from C07, the failure is **detected** (C10 finding), not
silent — the desired faithful posture, since G06's core harm is *silent* undefined use.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security**: none owned; static reference, no secrets, no runtime surface.
- **Cost**: one-time authoring + per-term-addition upkeep; AI-CONTEXT frames vocabulary cost as
  front-loaded and recoverable.
- **Scale**: term set is small and human-bounded (tens of entries); no scale concern.
- **Observability**: C07 itself is the observability aid (it makes other docs legible). No telemetry.
- **Ops**: lives in version control alongside the specs; changes go through normal review. The glossary
  is the diff target when vocabulary changes (AI-CONTEXT §3.5 warns of 1–2 breaking schema/format
  changes per quarter — term renames flow through C07 first).

## 8. Acceptance criteria & test strategy

1. **Coverage**: every term enumerated in G06 and in AI-CONTEXT §3.2/§3.3 has exactly one C07 entry.
2. **Anti-lock-in**: every Gas City term entry has a non-empty `generic_equivalent`.
3. **Traceability**: every entry cites a v4 or corpus source (Track-A rule 5).
4. **Alias closure**: every v3-jargon term and generic synonym resolves through the translation interface
   to exactly one canonical term (no orphan aliases, no ambiguous mappings).
5. **Linter integration**: C10 can import the term-set export and flag a deliberately-injected
   undefined term in a test spec (validates the F38/G06 mechanism end-to-end).
(Concrete test cases / schema validation deferred to sweep 2.)

## 9. Open questions

- **OQ-C07-1** (→ review-log): G06 specifically faults the **README** for using terms with "no inline
  glossary; the vocabulary table lives only in the companion." Does faithful resolution require
  *embedding* a glossary (or glossary link) into README itself, or is a single canonical C07 artifact
  that the README points to sufficient? Faithful reading leans to "canonical artifact + README cross-link"
  (minimal change, no architectural alteration), but the README-embedding interpretation is also
  defensible. Flagged, not silently resolved.
