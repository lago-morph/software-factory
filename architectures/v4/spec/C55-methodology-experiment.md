# C55 — Methodology-as-Config Experiment Loop  (Spec, canonical track)

> Source: README §Part 1 "The hypothesis" (L25 "Build a runtime that supports the 12 principles. The
> methodology question becomes empirical, second-order, swappable."; L27 "The v3 work produced **ten candidate
> methodologies** … which one do we build? … that's the wrong question to ask first."; L29 "methodology is the
> variable; substrate is convergent"; L31 "the ten v3 candidates collapse from 'ten architectural decisions' to
> '**ten pipeline configurations to run on the same platform with the same scenarios and the same judge**.' You
> don't choose; you experiment."; L33 "**you discover which methodology suits which kind of work — empirically,
> with evidence, instead of by debate**"); README §Part 2 table (L48–53 "Methodology | Architectural commitment
> | **Empirical experiment**"; L50 "wrong methodology means a new pipeline file"); README §Part 3 P3 (L128 "The
> methodology lives in the file, not in agent prompts"); README §Part 7 "the bets" (L512 "**Methodologies will
> emerge empirically.** Once Layer 2 is up, running v3's **GF-M (the cheapest candidate)** on the runtime is a
> few days of pack work. The bet is that empirical results will tell us which methodologies are worth pursuing,
> and that the substrate cost amortizes across all of them."; L525 "**No specific methodology choice.** v4
> deliberately doesn't pick from v3's ten candidates. They become experiments."; L550 "the ten candidates … the
> catalog of methodology experiments to run on the v4 runtime"; L553 "The first methodology you'll run is
> whichever v3 candidate has the **smallest custom-pack scope (GF-M)**, to validate that the runtime can host
> them at all."); AI-CONTEXT §0 pivot table (L15–19 "Methodologies | Compete for selection | **Become pipeline
> files on the runtime**"; L19 "Risk on misfit | High (rewrites substrate) | **Low (rewrites pipeline file)**");
> AI-CONTEXT §11.1 (L462 "Pivot … Methodology is variable; substrate is convergent"); AI-CONTEXT §11.2 (L482
> "**Which v3 candidate methodology to pursue first | After Phase 2 | Pick whichever has smallest custom-pack
> scope (likely GF-M)**"); AI-CONTEXT §11.3 (L501 "Pick a v3 methodology and build for it | **Wrong question per
> pivot rationale**"); AI-CONTEXT §3.3 vocab (L101 "formula | pipeline file / workflow DAG template"; L103 "pack
> | distributable **methodology** bundle"); component-inventory C55 row (L67 "v3's 10 candidates run as swappable
> pipeline files; empirical results select methodology per work type"; maps A88/A188/B08/B81; **depends on C12,
> C30, C33**; gap **G05**; foundational: no; Batch 4); ambiguities-and-gaps **G05** (L19 "'10 candidate
> methodologies' … the actual **selection criterion is never pinned**" — cheapest / smallest-scope / 'likely'
> are three different commitments); review-log **D-6** (canonical track), **D-7/D-8** (methodologies ARE C12
> formula/pipeline files; node-kind=C12), **D-15** (selection uses C33 holistic satisfaction), and the routing
> ruling (A/B *significance* is **C48**, Batch 5, **not** C55); the dependency specs `spec/C12-formula-pipeline-file.md`
> §1 ("the methodology-experiment loop (C55) swaps the formula"), `spec/C30-scenario-store.md` §1 (the held-out
> scenario corpus C55 runs the candidates against), `spec/C33-satisfaction-metric.md` §1 (the satisfaction
> distribution C55 selects on; C55 is named there as a C33 consumer).
> Inventory ID: C55   Kind: control-loop   Status: sweep-1

## 1. Purpose & responsibility

C55 is the factory's **methodology-as-config experiment loop**: the thin control-loop that takes **v3's ten
candidate methodologies — each expressed as a swappable C12 pipeline file (formula)** — runs each over the
**same held-out scenarios (C30)** with the **same judge**, reads the resulting **satisfaction distribution
(C33)**, and from that evidence **selects a methodology per *kind of work*** (README:31, :33). It is the
component that operationalises v4's **central pivot / hypothesis** — *"methodology is the variable, substrate is
convergent; you don't choose, you experiment"* (README:29–31; AI-CONTEXT §0/§11.1 "Pivot"; the empirical bet is
README:512 "**Methodologies will emerge empirically**", Bet 5). (Informal shorthand below:
*methodology-experimentation* — v4's **pivot/hypothesis**, **not** one of the El Kaim 12 principles; the
12-principle set is P1–P12 with P12 = self-optimization.) Where v3 asked "which of the ten methodologies do we build the substrate
for?", v4 makes that the **wrong first question** (README:27; AI-CONTEXT:501): the substrate is built once for
the 12 principles, the ten candidates become **ten pipeline configurations on one platform**, and the choice
becomes **empirical, per work type, with evidence instead of debate** (README:33).

The load-bearing capability — the genuine KEEP — is exactly this: **methodology-as-data**. The ten v3 candidates
are *not* ten code paths to be designed; they are **ten formula files** (C12 artifacts) that the loop swaps,
runs through the **existing eval tier** (C30 scenarios → C32 judge → C33 satisfaction), and **empirically ranks
per work type**. C55 owns the **experiment-and-selection contract** that turns "ten architectural commitments"
into "ten configurations and a satisfaction comparison." Everything that makes a methodology *runnable* and
*measurable* already exists in the stack (C12 swaps formulas; C30 holds the held-out scenarios; C33 yields the
satisfaction distribution; C48 — Batch 5 — decides A/B significance); C55 is the small loop that **binds those
into a per-work-type methodology selection** and is the **spec-of-record for the selection criterion (G05)**
v4 left unpinned.

C55 is deliberately **thin** — a control-loop, not an engine. It invents no runner, no scorer, no statistics:
it is the orchestration + the selection *contract* over capabilities the eval tier already provides.

**Responsibilities (what C55 is the spec-of-record for):**
- **The methodology *catalog* as swappable pipeline files (I1; D-7/D-8).** Treat each of v3's ten candidate
  methodologies as a **C12 formula file** (a TOML DAG; methodology lives in the file, not in prompts —
  README:128). C55 owns the *register* of which formula files are the candidate methodologies under
  experiment; it does **not** author the formula format (that is C12) and does **not** invent the candidates
  (they are v3's catalog, README:550). The first candidate registered is **GF-M** (smallest custom-pack scope,
  README:553; AI-CONTEXT:482).
- **The *work-type* dimension (I2; addresses G05).** Define the **work-type** key along which methodology is
  selected — "**which methodology suits which kind of work**" (README:33). A work type is a named class of work
  (e.g. greenfield vs brownfield — F-MODE F20; or a scenario family from C30). C55 owns the *concept and the
  binding* of `work_type → selected methodology`; the canonical taxonomy of work types is **sweep-2** (OQ-2).
- **The experiment *run* (I3).** For each candidate methodology (formula) × work type, run the candidate over
  the **held-out scenarios (C30)** through the **same judge**, producing a **C33 satisfaction distribution**
  per (methodology, work-type) cell. C55 *orchestrates* these runs; it does **not** run scenarios itself
  (the runner is C31, driven by C30's scenarios) and does **not** judge (C32).
- **The empirical *selection* (I4; D-15).** From the C33 satisfaction distributions across candidates **for a
  given work type**, select the methodology — the *"empirical results select methodology per work type"* of the
  inventory (C55 row). Selection is on **C33 holistic satisfaction** (D-15); **whether one candidate's advantage
  over another is statistically real is C48's** significance test (Batch 5), which C55 *consults*, not
  re-implements (§6 routing).
- **The selection *output* (I5).** Emit the `work_type → methodology` mapping (plus the supporting satisfaction
  evidence and sample sizes) as the loop's typed result — the artifact that tells the factory *which formula to
  dispatch for which kind of work*, replacing the "debate" with "evidence" (README:33).

**Explicitly NOT (boundaries):**
- **NOT the formula / pipeline-file format.** The methodology *is* a C12 formula (D-7/D-8); the TOML DAG
  format, the node-kind set `{agent,tool,gate,sub_formula}`, and the swap mechanism are **C12's** (C12 §1 names
  C55 as the component that "swaps the formula"). C55 *references and swaps* candidate formulas by name; it does
  not define what a formula is. **Authoring** a given candidate's formula file (porting GF-M etc. into a C12
  formula + pack) is methodology-pack work, not a C55-owned engine.
- **NOT the scenario corpus or its isolation.** The held-out scenarios the candidates are measured against are
  **C30**'s (authored in the isolated rig, read-isolated from the implementer — C30 §1). C55 runs candidates
  *against* the same scenario set ("same scenarios and the same judge", README:31) but neither authors nor
  stores nor isolates them.
- **NOT the runner or the judge.** Executing a scenario is **C31**; scoring a trajectory is **C32**. C55 invokes
  the eval tier; it renders **no** model call and **no** per-trajectory score of its own. It is judge-blind in
  the same sense C31 is verdict-blind.
- **NOT the satisfaction metric.** The satisfaction *distribution* per cell is **C33**'s output (C33 §1 names
  C55 as a consumer). C55 *reads* the distribution to compare candidates; it neither computes nor re-defines
  satisfaction, and it inherits C33's **threshold-free invariant** (C33 INV-3 / D-15 — an upstream property C55
  relies on, not one it establishes; the "is this good enough" cutline is not C55's).
- **NOT the A/B statistical-significance engine.** Deciding **whether a methodology variant is actually better**
  (the significance test) is **C48** (a/b-routing + scipy/Evidently, Batch 5; inventory C48 "determines whether
  a variant was actually better"). C55 *poses* the comparison and *consults* C48's verdict; it builds **no**
  bespoke significance machinery (C55's significance→C48 scope boundary — §6). C55's own selection is the
  per-work-type *mapping* given that evidence.
- **NOT the general self-optimization / variant-search loop.** Open-ended prompt/hyperparameter variant
  *discovery* (DSPy/Optuna) is **C47**; A/B *traffic routing* is **C48**; the *promotion gate* is **C50**;
  *counterfactual replay* is **C49**. C55 is the narrower, v3-grounded **methodology-experiment** loop over a
  *fixed catalog of ten candidates*, selecting per work type — not the continuous meta-optimizer. (C55 is a
  *consumer* of C48's comparison verdict, an upstream of nothing in Batch 5.)
- **NOT community publishing of pipeline files.** The original El Kaim P12 ("pipeline files worth sharing") is
  **deferred** (README:98; AI-CONTEXT:27); C55 selects *for internal use*, it does not publish or socialise
  methodologies.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (the candidates) | **C12** Formula / pipeline-file | Each candidate methodology **is** a C12 formula file (D-7/D-8). C55 registers + swaps candidate formulas by name; C12 owns the format + swap. Inventory C55 `depends on C12`; C12 §1 names C55 as the swapper. |
| Upstream (held-out test set) | **C30** Scenario store | The **same held-out scenarios** every candidate is measured against (README:31). C55 runs candidates over C30's corpus; C30 authors/stores/isolates them. Inventory C55 `depends on C30`. |
| Upstream (the metric) | **C33** Satisfaction metric | The **satisfaction distribution** per (methodology, work-type) cell that C55 selects on (D-15). C33 §1 names C55 as a consumer. Inventory C55 `depends on C33`. |
| Eval-tier (run + score) | **C31** Scenario runner, **C32** Judge harness | The runner that executes a candidate over a scenario and the judge that scores it. C55 drives them via the eval tier; "same … judge" (README:31). *(Transitive through C30/C33's contracts; C55's direct deps are C12/C30/C33.)* |
| Significance (consulted) | **C48** A/B routing & statistical comparison | **Decides whether a candidate is actually better** (the significance test, Batch 5). C55 **consults** C48's verdict; it implements no significance machinery (C55's scope boundary, §6). *(Forward reference: C48 is unbuilt — Batch 5; C55 names the seam, does not block on it.)* |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C55's loop is realised as pack-delivered tool nodes invoked via the tool-node ABI (mirrors C33's packaging note). *(Related interface, not a dependency edge.)* |
| Config gate | **C03** Layered config | C55 exists only when the experiment capability is enabled (section-presence flag); the candidate-catalog + work-type config live in pack TOML. *(Related interface.)* |
| Downstream (the choice) | the **factory dispatch** (C05 sling, via C12) | Consumes the `work_type → methodology` selection to dispatch the chosen formula for a kind of work. *(C55 produces the mapping; acting on it — which formula to dispatch — is the dispatch tier's, via the chosen C12 formula name.)* |

**Position in the system.** C55 is **Batch 4** (component-inventory L113; HANDOFF §1), built in **Phase 3**
("factory builds factory"), and is explicitly **post-Phase-2** work — selection happens **"After Phase 2"**
once Layer 2 (the eval tier) is up (AI-CONTEXT:482; README:512 "Once Layer 2 is up"). It is **not foundational**
(inventory C55: Foundational? = no): it is a *leaf consumer* of the formula artifact + the eval tier, adding
the selection loop on top. Its whole reason to exist is v4's **methodology-experimentation pivot** (the
hypothesis / Bet 5, README:512 — **not** a numbered 12-principle): the methodology decision should be
**empirical and swappable** rather than an architectural commitment (README:25–33). It is **feature-flag-gated** (C03): the factory runs fine without it; C55 is the apparatus that,
*when enabled*, turns the ten-candidate catalog into evidence-based per-work-type selection.

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete candidate-registry schema, the work-type taxonomy, the
per-cell run contract, and the selection-record shape defer to sweep 2 (and bind to C12's real formula grammar,
C30's scenario record, C33's distribution shape, and C48's significance verdict).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Candidate methodology registry** | input (config) | The set of **candidate methodologies under experiment, each a named C12 formula file** (D-7/D-8). v3's ten candidates as ten formulas; GF-M registered first (README:553). C55 registers/swaps by formula name; it does not author the format or the candidates. | C55 (register); **C12** (formula + swap) |
| I2 | **Work-type key** | input (config) | The **`work_type`** dimension along which methodology is selected — "which methodology suits which kind of work" (README:33). A named class of work (e.g. greenfield/brownfield; or a C30 scenario family). Sweep-1 names the key + its role; canonical taxonomy is sweep-2 (G05/OQ-2). | C55 (this) |
| I3 | **Experiment run (per cell)** | outbound (drives eval tier) | For each (candidate formula × work_type): run the candidate over the **same held-out C30 scenarios** through the **same judge**, yielding a **C33 satisfaction distribution** for that cell. C55 orchestrates; C31 runs, C32 judges, C33 aggregates. | C55 (orchestrate); **C30/C31/C32/C33** (run+score+metric) |
| I4 | **Per-work-type selection** | internal | Given the C33 satisfaction distributions across candidates **for one work type**, select the methodology (on **holistic satisfaction**, D-15), **consulting C48** for whether an advantage is statistically real. C55 owns the *mapping rule*; **C48** owns the *significance verdict*. | C55 (selection rule); **C48** (significance) |
| I5 | **Selection output** | outbound (data) | The loop's declared output: the **`work_type → methodology` mapping** + the supporting satisfaction evidence (per-cell distribution summaries, sample counts) + the significance verdicts consulted. Consumable by the dispatch tier (which formula to run for a kind of work). | C55 (this); C02/C17 (surfacing) |
| I6 | **Tool-node / loop lifecycle (pack)** | inbound (ops) | Packaged + invoked as Gas City tool node(s) (C02/C17 ABI); configured via pack TOML (candidate registry I1, work-type set I2, selection policy). Feature-flag-gated (C03). | C02/C17 (ABI); C03 (gate); C55 (config) |

**Invariants C55 must uphold:**
- **INV-1 (methodology-as-data — D-7/D-8).** Every candidate methodology is a **swappable C12 formula file**,
  never bespoke C55 code. Adding/removing/changing a candidate is **a formula-file change** (README:50 "wrong
  methodology means a new pipeline file"), not a C55 code change. C55 holds *references* to formulas, never an
  embedded methodology.
- **INV-2 (same scenarios, same judge — fair comparison).** All candidates for a given work type are measured
  against the **same held-out C30 scenario set** through the **same judge/C33 metric** (README:31). C55 must not
  let candidates be scored on different scenarios or different judges — that would make the comparison invalid.
- **INV-3 (empirical selection only — anti-debate).** The `work_type → methodology` choice is made **from C33
  satisfaction evidence**, never by a hard-coded preference or by debate (README:33). "GF-M first" is a
  *registration/ordering* convenience (cheapest to stand up, README:553), **not** a pre-decided winner — the
  winner is whatever the satisfaction evidence selects (G05 resolution, §6).
- **INV-4 (significance is consulted, not computed — routing).** Whether one candidate genuinely beats another
  is **C48**'s significance verdict (Batch 5). C55 **poses** the comparison and **reads** C48's answer; it
  computes **no** p-value, CI, or bespoke estimator. (Until C48 exists, C55 surfaces the raw per-cell
  distributions and defers the *significance* claim — it never fabricates one. §6.)
- **INV-5 (sample-honest selection).** Every selection carries the **per-cell sample counts** (how many
  scenarios/runs each candidate was measured over for that work type) — a methodology "selected" on n=3 must be
  legible as thin evidence, not presented as settled (inherits C33 INV-4 population-honesty).
- **INV-6 (re-derivable, owns no truth).** C55 owns no source-of-truth: the **formulas** live in C12/packs, the
  **scenarios** in C30, the **satisfaction** in C33. Re-running the experiment over the same candidates +
  scenarios + judge re-derives the evidence; the selection is a function of that evidence + the selection
  policy. C55 may *record* its selection as an artifact, but it is reproducible from inputs.

## 4. Data model / state

C55 **owns the experiment + selection contract**, not durable source-of-truth data. The **formulas** are
C12/pack files; the **scenarios** are C30's; the **satisfaction distributions** are C33's; the **significance
verdicts** are C48's. State C55 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Candidate registry** | The set of candidate methodologies under experiment, each a **named C12 formula** (I1); GF-M first. Maps a candidate name → its formula-file reference + (optionally) its pack. | Pack TOML / config (C03 model); the formulas themselves live in C12/packs. | C55 (registry); **C12** (formula) |
| **Work-type set** | The named `work_type` classes selection is computed per (I2). | Pack TOML (C03). | C55 (concept); sweep-2 (taxonomy) |
| **Experiment result (per cell)** | Per (candidate, work_type): the **C33 satisfaction distribution** + sample count + the C30 scenario set used + (when available) the **C48 significance verdict** vs other candidates. The loop's working evidence. | Derivable on demand from C33 over the candidate's runs; optionally recorded for audit/trend. | C55 (shape); **C33** (distribution), **C48** (significance) |
| **Selection record** | The **`work_type → methodology` mapping** + the supporting evidence + sample counts (I5). The loop's output artifact. | Emitted as tool-node output; optionally recorded (e.g. as a bead/CXDB result) for audit — re-computable (INV-6). | C55 (shape) |

> [FAITHFUL-FILL] v4 specifies the *behavior* ("ten candidates as pipeline configs … run on the same platform
> with the same scenarios and the same judge … discover which methodology suits which kind of work",
> README:31–33) but not C55's persisted state or record schemas. The minimal faithful set is **none that is
> source-of-truth**: the experiment is a **re-derivable** orchestration over C12 formulas + C30 scenarios + C33
> satisfaction (INV-6), so C55 holds no independent store. Persisting the selection as an artifact is at most an
> *audit/trend convenience*, not required state. The exact candidate-registry schema, the **work-type taxonomy**
> (G05), the per-cell experiment-result record, and the selection-record shape are **sweep-2** — frozen against
> C12's real formula grammar (G11), C30's scenario record, C33's distribution shape, and C48's significance
> verdict (the principal contracts C55 binds to).

**Consistency / lifecycle.** C55 stands up in **Phase 3**, *after* the eval tier (Layer 2) exists
(AI-CONTEXT:482). It owns no durable truth: the formulas (C12), scenarios (C30), and satisfaction (C33) all
persist elsewhere, so a re-run of the experiment re-derives the evidence and the selection (INV-6). C55 is
therefore a **stateless, re-derivable control-loop** over the eval tier — which is exactly why the bar keeps it
thin (no runner, no scorer, no statistics engine; §6).

## 5. Behavior

**Stand up (Phase 3).** The experiment pack is enabled (C03). The **candidate registry (I1)** is populated with
v3's candidate methodologies **as C12 formula files** — GF-M first (smallest scope, README:553) to validate the
runtime can host a candidate at all. The **work-type set (I2)** is configured. C55 is wired to the eval tier
(C30 scenarios → C31 runner → C32 judge → C33 satisfaction) and, when available, to C48 (significance).

**Experiment-and-select path (the control loop).**
1. **Enumerate cells (I1×I2):** for each candidate methodology (formula) × work type, form an experiment cell.
2. **Run each candidate (I3):** dispatch the candidate **formula** over the **same held-out C30 scenarios** for
   that work type, through the **same judge** (C31 runs, C32 judges); collect the per-trajectory scores.
3. **Aggregate satisfaction (I3→C33):** obtain the **C33 satisfaction distribution** + sample count for the
   cell (C55 reads C33's output; it computes no metric — INV-4/§1 boundary).
4. **Compare within a work type (I4):** across candidates for one work type, rank by **holistic satisfaction**
   (D-15) and **consult C48** for whether a leading candidate's advantage is **statistically real** (INV-4); if
   C48 is not yet available, surface the raw distributions and **withhold** the significance claim (never
   fabricate one).
5. **Select (I4) + emit (I5):** record the **`work_type → methodology`** choice with its supporting evidence +
   sample counts (INV-5), and emit the selection for the dispatch tier to act on (which formula to run for which
   kind of work). The choice is **empirical** (INV-3) — "GF-M first" is ordering, not a pre-decided winner.

**Re-experimentation.** Because C55 owns no source-of-truth (INV-6), the experiment can be re-run any time —
when a new candidate formula is registered, when C30's scenario corpus grows (README:526 "the broader scenario
library grows over time"), or when more runs accumulate — and the selection is re-derived from the current
evidence. There is no checkpoint to recover; the loop is restartable from its inputs.

> The exact orchestration signatures, the candidate-registry + selection-record schemas, the **work-type
> taxonomy** (G05), and the precise selection rule (e.g. argmax-satisfaction subject to C48 significance, with a
> tie/insufficient-evidence policy) are **sweep-2+** — frozen against C12 (real formula grammar, G11), C30
> (scenario record), C33 (distribution shape), and C48 (significance verdict). C55 invokes **no** model, runs
> **no** scenario itself, computes **no** satisfaction, and runs **no** significance test.

## 6. Failure modes & handling

C55 owns the **methodology-selection** gap (G05) at this component, and the **routing of significance to C48**.

**G05 (minor) — methodology selection criterion. ADDRESSED HERE.** G05 flags that v4 names "ten candidate
methodologies" and calls GF-M "**the cheapest**" (README:512), "**smallest custom-pack scope**" (README:553),
and "**likely**" (AI-CONTEXT:482) — *three different commitments to the same choice* — so the **actual selection
criterion is never pinned**. Faithful resolution:
- **The selection criterion — RESOLVED (empirical, per work type).** C55 pins the criterion exactly as the v4
  hypothesis states it: **methodology is selected *empirically*, by comparing the C33 satisfaction distribution
  each candidate produces over the same held-out C30 scenarios and the same judge, separately for each work
  type** (README:31–33; D-15). This dissolves the cheapest/smallest/likely confusion: those three are **not**
  selection criteria at all — they describe **which candidate to *stand up first*** (the one cheapest to host),
  which is an **ordering/bootstrapping** decision, *not* the winner. **"GF-M first" means "GF-M is the first
  experiment," not "GF-M is the choice"** (INV-3). The choice for any work type is *whatever the satisfaction
  evidence selects* — "you don't choose; you experiment" (README:31).
  > [AMBIGUITY: G05] v4 conflates three phrasings — GF-M "cheapest" (README:512) / "smallest custom-pack scope"
  > (README:553) / "likely" (AI-CONTEXT:482). Two readings: **(a)** GF-M is the *intended methodology* (a
  > soft pre-commitment); **(b)** GF-M is only the *first candidate to run* (cheapest to host), and the actual
  > methodology is selected **empirically per work type** from satisfaction evidence. **Chosen: (b)** — it is the
  > only reading consistent with the rest of v4: the entire Part-1 thesis is "you don't choose; you experiment"
  > (README:31), "empirically, with evidence, instead of by debate" (README:33), and "v4 deliberately doesn't
  > pick from v3's ten candidates — they become experiments" (README:525). Reading (a) would re-introduce the v3
  > "pick a methodology" framing that AI-CONTEXT:501 calls the **wrong question**. So **C55's criterion is
  > empirical-satisfaction-per-work-type (INV-3)**; GF-M's "cheapest" is *only* its standing-up order.
- **The selection *granularity* — RESOLVED (per work type).** Selection is **per `work_type`**, not one global
  winner — "**which methodology suits which kind of work**" (README:33; inventory "select methodology per work
  type"). C55 owns the `work_type` concept + the per-work-type binding (I2/I4); the **canonical work-type
  taxonomy** is **sweep-2** (OQ-2) — v4 names the dimension but not its values (only F-MODE F20's
  greenfield/brownfield split is named in the corpus as one such axis).
- **The *threshold* (what counts as "good enough" to select) — DEFERRED, not C55's.** C55 *ranks* candidates by
  satisfaction and *selects the best for each work type*; it inherits C33's **threshold-free invariant**
  (C33 INV-3 / §6, G09 — and the threshold *value* is undefined in v4): the "is this methodology good enough in
  absolute terms" cutline is a **decision-site gate** question (C50 promotion gate / C53 / C39, or operator
  policy — C33's stated owner-set), not C55's. C55 selects the **relatively** best candidate per work type from
  the evidence; an absolute go/no-go cutline is out of scope (OQ-1).

**Routing — A/B *significance* is C48, not C55 (C55's binding scope boundary).** Whether a leading candidate's
satisfaction advantage for a work type is **statistically real** is the **A/B statistical-comparison** question,
owned by **C48** (a/b-routing + scipy/Evidently; inventory C48 "determines whether a variant was actually
better"; Batch 5). **C55 builds no significance machinery** — it *poses* the candidate-vs-candidate comparison
and *consults* C48's verdict (INV-4). This routing is grounded in C48's inventory mandate and mirrors C33's own
significance→C48 boundary; it is **C55's binding scope boundary and should be recorded as a numbered
review-log decision** (OQ-4) — not (yet) a pre-existing logged ruling.
> [FAITHFUL-FILL] **C48 is unbuilt (Batch 5)** and C55 is **Batch 4** — C55 must not block on it. Sweep-1
> contract: C55 **names the C48 significance seam** (I4) and, until C48 lands, surfaces the **raw per-cell C33
> distributions + sample counts** and **withholds** any "statistically better" claim (it never fabricates a
> p-value or rolls its own test — that would be the exact scope creep the bar forbids). The significance verdict
> binds at sweep-2 when C48 exists. This mirrors how C33 routes significance to C48 rather than owning a stats
> engine.

**Other failure cases.**
- **A candidate formula fails to run / errors mid-experiment (I3).** Record the candidate as
  *failed-to-evaluate* for that cell (with the error) and **exclude it from selection** for that work type —
  do not let a broken candidate's missing scores be read as low satisfaction or poison the comparison.
  *[FAITHFUL-FILL]: v4 silent; excluding-with-reason is the minimal honest choice and keeps the comparison fair
  (INV-2).*
- **Insufficient / unequal evidence across candidates (INV-5).** If candidates were measured over different
  scenario counts, or a cell has too few runs, surface the **sample counts** and treat the selection as
  *provisional* (or withhold it) rather than declaring a winner on thin/uneven evidence — re-run when more
  evidence accumulates (INV-6). *[FAITHFUL-FILL]: inherits C33 INV-4 population-honesty; minimal.*
- **C30 corpus changes between candidate runs (fairness).** If the held-out scenario set changed, candidates
  measured against different versions are **not comparable** (INV-2) — re-run the affected candidates against
  the current corpus before selecting. *[FAITHFUL-FILL]: the "same scenarios" guarantee (README:31) requires
  this; minimal.*
- **Holdout integrity (running candidates against held-out scenarios).** C55 runs candidate *implementers*
  against the **held-out** C30 scenarios — the read-isolation that keeps the implementer from reading those
  scenarios is **C30/C34/C42**'s (enforcement + audit is C34, partition is C42, store is C30 — D-13). C55
  *relies on* that isolation; it does **not** enforce it. *(Boundary, not a C55 mechanism.)*

> F-mode applicability is owned by **C57** (coverage map). C55 underwrites the **methodology-experimentation**
> posture some modes lean on — notably **F20** (maintenance-vs-greenfield asymmetry: "v4 deliberately does not
> pick a mandate; both greenfield and brownfield methodologies can run on the runtime … methodology-level, not
> runtime-level", F-MODE-COVERAGE L115) — by making "which methodology for which kind of work" an **empirical,
> per-work-type** selection rather than a fixed architectural commitment. C55 also surfaces the
> **methodology-misfit** risk (v4's whole pivot rationale, AI-CONTEXT:19: misfit is "Low — rewrites a pipeline
> file") as a *measured* signal (a low-satisfaction candidate is visible, not silently shipped). C55 defers the
> canonical F-mode mapping to C57.

**The bar — what got DROPPED.** Per the ruthless bar, C55 is held to *only* the P-methodology-experimentation
capability — the **methodology-as-data** loop: ten v3 candidates **as swappable C12 formula files**, run through
the **existing** eval tier, **empirically selected per work type**. **Dropped / refused as non-principle or
already-in-the-stack:** (1) any **methodology *engine* / new runner or scorer** — candidates run on the existing
C12 formula swap + C30/C31/C32/C33 eval tier; C55 adds *orchestration*, not an engine; (2) any **bespoke
statistical-significance machinery** — "was the variant actually better" is the v4-named **C48** scipy/Evidently
stack (Batch 5), not a new C55 estimator (the significance→C48 scope boundary, §6); (3) any **absolute satisfaction
threshold / go-no-go cutline** — that re-introduces test-pass (anti-P6) and is a C50/operator decision-site
concern (C33's threshold-free posture inherited); (4) the **general self-optimization / variant-search** loop
(C47 variant ID, C48 routing, C49 replay, C50 gate) — C55 is the narrower fixed-catalog methodology-experiment,
not the continuous meta-optimizer; (5) **authoring the candidate formulas themselves** (porting GF-M etc.) —
that is methodology-pack/C12 work, not a C55-owned deliverable; (6) **community publishing** of selected
methodologies — the original P12 "pipeline files worth sharing" is **deferred** (README:98). What is **kept**:
the candidate-as-formula **registry** (I1), the **work-type** selection dimension (I2, the G05 resolution), the
experiment **orchestration** over the eval tier (I3), and the empirical **per-work-type selection** contract
(I4/I5) — the small loop that turns ten architectural commitments into evidence-based selection, which **no
single existing component provides**.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C55 reads **satisfaction distributions** (C33) and **selection evidence** — not raw
  prompts/outputs — and runs candidates through the eval tier. It introduces **no new credential** (no model
  call of its own; the judge tokens are C32's). It **relies on** C30/C34/C42 holdout isolation when running
  candidates against held-out scenarios (it does not enforce it — §6 boundary).
- **Cost.** This is the **one genuine cost force** for C55, and it is a *flagged risk*, not a C55-owned
  mechanism: running **ten candidates × multiple work types × the held-out scenario suite** through the judge is
  a **multiplicative** token/compute cost on the single Max seat (the unmodelled **G32 cost / G34 throughput**
  gap — ambiguities-and-gaps). v4 asserts "the substrate cost amortizes across all of them" (README:512) **with
  no number**. C55's design response is to keep the loop *thin* and *incremental* (re-derivable, INV-6 — run a
  candidate when ready, accumulate evidence over time, don't re-run all cells eagerly) and to **surface sample
  counts** (INV-5) so cost-vs-evidence is legible; the **cost model itself is C46/G32's**, not C55's. *[FLAG:
  over-budget risk — experiment fan-out × single-seat throughput is the real scaling tension; quantify with C46
  before running the full ten-candidate × work-type grid. → OQ-3 / review-log.]*
- **Scale.** Experiment cells fan out as (candidates × work-types × scenarios); the honest scale posture is
  **incremental, evidence-accumulating** runs (INV-6) rather than an eager full-grid sweep — a sweep-2/ops
  concern, not a Sweep-1 design force. No bespoke scaling machinery is warranted (the bar).
- **Observability.** C55's selection evidence (per-cell satisfaction, sample counts, the chosen mapping) *is*
  the headline P-methodology-experimentation signal and is worth emitting as events for auditability (why a
  methodology was selected for a work type). C55 is mostly a *reader* of C33's signal, not a heavy emitter.
- **Ops.** Pack-delivered loop, enabled in Phase 3 after Layer 2 (AI-CONTEXT:482). Pin the eval-tier versions
  (Inspect AI via C30/C33) so cross-candidate comparisons are reproducible (inherits the eval-tier version-pin
  discipline). Selection is re-runnable as the candidate catalog or scenario corpus grows.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (methodology-as-data — INV-1, D-7/D-8):** each candidate methodology is a **swappable C12 formula
   file**; registering/swapping a candidate is a **formula-file change**, not a C55 code change (README:50).
2. **AC-2 (same scenarios + same judge — INV-2):** all candidates for a work type are measured against the
   **same held-out C30 scenario set** through the **same judge/C33 metric** (README:31); C55 rejects/flags a
   comparison where the scenario set or judge differs.
3. **AC-3 (experiment over the eval tier — I3):** C55 produces a **C33 satisfaction distribution per
   (candidate, work-type) cell** by driving C30/C31/C32/C33; it makes **no** model call and computes **no**
   metric of its own.
4. **AC-4 (empirical per-work-type selection — INV-3, addresses G05):** the `work_type → methodology` choice is
   made **from satisfaction evidence**, per work type; "GF-M first" is *ordering only* and does **not**
   pre-determine the winner.
5. **AC-5 (significance routed to C48 — INV-4, C55's scope boundary §6):** C55 computes **no** p-value/CI; it
   **consults C48** for "is the variant actually better," and — until C48 exists — surfaces raw distributions +
   sample counts and **withholds** the significance claim (never fabricates one).
6. **AC-6 (sample-honest — INV-5):** every selection carries the **per-cell sample counts**; a selection on thin
   or uneven evidence is legible as provisional, not settled.
7. **AC-7 (re-derivable, owns no truth — INV-6):** re-running over the same candidates + scenarios + judge
   re-derives the evidence and selection; C55 holds no source-of-truth (formulas in C12, scenarios in C30,
   satisfaction in C33).
8. **AC-8 (engine-reuse, no custom machinery — the bar):** C55 contains **no** runner, scorer, satisfaction
   metric, or significance engine — it orchestrates C12 (swap) + C30/C31/C32/C33 (run+score+metric) + C48
   (significance); the only custom surface is the registry + work-type + selection contract.
9. **AC-9 (selection output consumable — I5):** the emitted `work_type → methodology` mapping (+ evidence +
   sample counts) is consumable by the dispatch tier (which formula to run for which kind of work).

**Test strategy.** A **methodology-experiment pack** that registers ≥2 candidate **formula files** (one being a
GF-M stand-in) over ≥2 work types, drives them against a synthetic held-out C30 scenario set + synthetic C33
satisfaction outputs (varied, including a clearly-better candidate, a tie, a failed-to-evaluate candidate, and a
thin-evidence cell), and exercises AC-1…AC-9 — in particular that the candidate is a **swapped formula** (AC-1),
that the comparison is **same-scenarios/same-judge** (AC-2), that selection is **empirical per work type** with
**GF-M-first ≠ GF-M-wins** (AC-4), that **significance is consulted from C48 / withheld until C48** (AC-5), and
that the loop is **re-derivable** with **no custom engine** (AC-7/AC-8). This suite validates the
**methodology-as-data** capability without C55 acquiring any engine the stack already provides.

## 9. Open questions

- **OQ-1 (→ review-log, top): G05 — selection criterion confirmed + the "GF-M first ≠ GF-M chosen" reading.**
  §6 pins the criterion as **empirical satisfaction per work type** (reading (b)) and treats GF-M's
  "cheapest/smallest-scope" as *standing-up order only*. Confirm the operator/integrator intends **empirical
  per-work-type selection** (not a soft GF-M pre-commitment), and that the **absolute "good enough" cutline** is
  a C50/operator decision-site concern, not C55's (C55 selects *relatively* best per work type).
- **OQ-2 (→ review-log): the work-type taxonomy.** v4 names the *dimension* ("which kind of work", README:33)
  but not its **values** (only F-MODE F20's greenfield/brownfield axis is named in the corpus). Freeze the
  canonical `work_type` set at sweep-2 (its source — C30 scenario families? a separate axis?) before C55's
  per-work-type selection record is schematised.
- **OQ-3 (→ review-log): experiment fan-out cost vs single-seat throughput (G32/G34).** Running ten candidates ×
  work-types × the held-out suite through the judge is a **multiplicative** cost on one Max seat, and v4's "cost
  amortizes" claim (README:512) carries **no number**. Quantify with **C46** (cost-per-satisfaction) before
  running the full grid; confirm C55's incremental/evidence-accumulating posture (INV-6) is the intended cost
  control and that the **cost model lives in C46/G32**, not C55.
- **OQ-4 (→ review-log): the C48 significance seam (forward dependency).** C48 is **Batch 5** (unbuilt); C55 is
  Batch 4. Confirm the **C55→C48** consultation contract (what comparison C55 poses; what verdict C48 returns)
  to be frozen at sweep-2 when C48 is authored, and that C55's interim behavior (raw distributions + withheld
  significance) is acceptable until then. **Also record the significance→C48 routing as a numbered review-log
  decision** — it is C55's binding scope boundary (grounded in C48's inventory mandate + the C33 precedent) but
  is not yet a logged D-x ruling.
