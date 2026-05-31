# C37 — Trajectory Embedding & Clustering  (Spec, canonical track)

> Source: README §"Principle 11 — Self-healing loop" (line 248 "Observability → anomaly → **diagnosis** → fix →
> ship, without human intervention"; placement table line 254 "Trajectory embedding | Embeds trajectories for
> clustering | **sentence-transformers** | Apache 2.0 | **Python tool node**"; line 255 "Trajectory clustering |
> **Groups similar failures** | **HDBSCAN, scikit-learn** | BSD | Python tool node"; line 256 "Diagnosis agent |
> LLM-driven root-cause analysis … over clustered failures"; line 261 "**P11 is the largest custom engineering
> effort**. CXDB + Temporal handle substrate; PyOD + **sentence-transformers + HDBSCAN handle clustering**; the
> diagnosis agent is the focused work"; license table lines 312–313 "sentence-transformers | Apache 2.0 |
> Clean", "HDBSCAN | BSD | Clean"; Phase 3b line 461 "**Trajectory clustering pack (transfusion from
> sentence-transformers + HDBSCAN)**"; line 466 "Build the simplest first (anomaly detection); save the
> diagnosis agent for after the substrate is proven"), AI-CONTEXT §"Layer 4 — self-healing loop (P11)" (line
> 329 "Trajectory embedding | **sentence-transformers** | Apache 2.0 | **Mature**"; line 330 "Clustering |
> **scikit-learn, HDBSCAN** | BSD/BSD | Mature"), §"Layer 4 — self-healing" exemplars (line 406 "Embedding +
> clustering: **sentence-transformers + HDBSCAN (standard recipe)**"), §15 repos (lines 649–650
> `github.com/UKPLab/sentence-transformers`, `github.com/scikit-learn-contrib/hdbscan`); component-inventory C37
> row (line 49 "Embeds trajectories (sentence-transformers) and clusters similar failures (HDBSCAN) for
> diagnosis"; maps A56b/A56c/B34/B35; depends **C21**; gaps **G32, G33**; foundational **no**) + Batch-4 note
> (line 113); spec/C21 (the CXDB trajectory store C37 reads — §2 lists C36/C37/C38 as P11 consumers, I6 replay/
> retrieval is C37's read seam); spec/C33 (the satisfaction-metric distribution C36 anomaly-detects on — the
> sibling Python-tool-node-in-a-pack shape C37 mirrors); F-MODE-COVERAGE §3 "Layer 4 (P11)" (F22 zombie agents,
> F23 stalled-vs-thinking, F40 last-mile drift, F54/F55 drift/subversion — the failure classes clustering makes
> diagnosable per-cluster) and §C57 ownership of the canonical mapping; ambiguities-and-gaps **G32** (cost
> unmodeled — embedding all trajectories), **G33** (no partial-failure story for the OSS Python tool nodes);
> review-log **D-6** (canonical track).
> Inventory ID: C37   Kind: component   Status: sweep-1

## 1. Purpose & responsibility

C37 is the factory's **trajectory embedding & clustering** stage of the P11 self-healing loop: the **Python tool
node (in a Gas City pack)** that **reads recorded trajectories (C21), embeds each into a vector with
sentence-transformers, and clusters the embeddings with HDBSCAN so that *similar failures group together*** for
diagnosis (README:254–255; AI-CONTEXT:329–330; inventory C37). It sits between the anomaly detector (**C36**,
which says *something is wrong*) and the diagnosis agent (**C38**, which says *why*), and its single
load-bearing job is to make C38 operate **per-cluster, not per-trajectory** — so the (expensive, LLM-driven)
root-cause analysis runs **once per family of similar failures** instead of once per raw trajectory. That
batching is the **P11/Ashby move** at this stage: collapse the variety of individual failing runs into a small
set of *failure modes* the Healer can reason about.

C37 is **deliberately thin glue over a standard recipe.** v4 states the engineering posture twice and bluntly:
"sentence-transformers + HDBSCAN (**standard recipe**)" (AI-CONTEXT:406) and, of the whole P11 layer,
"sentence-transformers + HDBSCAN **handle** clustering; the **diagnosis agent is the focused work**"
(README:261). Both named libraries are **mature, clean-licensed, off-the-shelf** (sentence-transformers Apache
2.0; HDBSCAN BSD — README:312–313; AI-CONTEXT:329–330). C37's *custom* surface is therefore **only the wiring**:
the read from CXDB, the choice of **what text of a trajectory gets embedded** (the trajectory→document
representation, G32-adjacent), and the **cluster representation handed to C38** — not any embedding or clustering
algorithm, which are the libraries' job.

**Responsibilities (what C37 is the spec-of-record for):**
- **Read the trajectory population to cluster (I1).** Pull the set of (typically failing/anomalous)
  trajectories to be grouped from **CXDB (C21)** via its replay/retrieval read seam (spec/C21 I6; inventory C37
  `depends on C21`). The *which* trajectories — typically the anomalous window C36 flags — is an input selector,
  not a judgement C37 makes.
- **Reduce each trajectory to an embeddable representation (I2, G32).** Project a trajectory (a turn-DAG path in
  CXDB) into the **document/text the embedder consumes**. This representation choice is C37's one genuinely
  load-bearing design decision (and the substance of **G32** at this component); see §4/§6.
- **Embed each trajectory into a vector (I3).** Apply **sentence-transformers** (the v4-named embedder,
  README:254; AI-CONTEXT:329) to produce a fixed-length embedding per trajectory. Off-the-shelf; C37 owns the
  *invocation + model-pin*, not the embedding model.
- **Cluster the embeddings into similar-failure groups (I4).** Apply **HDBSCAN** (the v4-named clusterer,
  README:255; AI-CONTEXT:330) over the embeddings to assign each trajectory a **cluster label** (HDBSCAN
  natively emits a **noise/outlier label** for points that belong to no dense cluster — kept, not suppressed).
  Off-the-shelf density clustering; C37 owns the *invocation + parameter binding*, not a clustering algorithm.
- **Emit the cluster set as the contract C38 consumes (I5).** Produce, per cluster, a **cluster record** — the
  member trajectory ids, a size, and a **representative/exemplar** (e.g. the medoid trajectory) — so **C38**
  diagnoses **per cluster**. This *cluster representation handed to C38* is, with I2, the **keep**: the wiring
  plus the shape of what crosses the C37→C38 seam.

**Explicitly NOT (boundaries):**
- **NOT the anomaly detector.** Deciding that a trajectory (or a metric) is *anomalous / worth investigating* is
  **C36** (numeric anomaly detection, PyOD/Anomalib — README:250; AI-CONTEXT:331-class). C37 does **not** detect
  anomalies; it **groups** a supplied set of trajectories. (Whether C36 selects the population C37 clusters, or
  C37 clusters a broader trajectory set and C36 scores numerically in parallel, is the C36↔C37 seam — OQ-1.)
- **NOT the diagnosis agent / root-cause.** Explaining *why* a cluster of failures happened — the LLM root-cause
  analysis (Tracker `Diagnose`/`Audit`/`Doctor` transfusion) — is **C38** (README:256; inventory C38 `depends
  on C37, C21`). C37 hands C38 *clusters*, makes **no** root-cause claim, and invokes **no** LLM. C37 is
  model-free (its only "model" is the sentence-transformers *embedding* model, which is not a judge or a
  reasoner).
- **NOT the fix-task / loop-closure owner.** Turning a diagnosis into a `fix_task` bead and tracking
  anomaly→diagnosis→fix→resolution is **C39** (fix-task & loop-closure — inventory; README:257–259). C37
  produces no beads of work; it produces a clustering.
- **NOT the trajectory store or its schema.** Trajectories live in **C21 (CXDB)**; the turn/payload schema is
  **C22**'s bundle over C21. C37 **reads** trajectories via C21's retrieval seam (spec/C21 I6) and owns
  **neither** the store **nor** the record format.
- **NOT a custom embedding or clustering algorithm.** The embedder is **sentence-transformers**; the clusterer
  is **HDBSCAN** — both v4-named, mature, off-the-shelf (README:254–255/312–313; AI-CONTEXT:329–330/406). C37
  introduces **no** bespoke vectorizer, distance metric engine, or clustering algorithm. Any such custom code
  would be flagged as exceeding scope (the bar; §6).
- **NOT a satisfaction/quality judge.** C37 groups trajectories by *embedding similarity*; it renders **no**
  pass/fail and **no** satisfaction score. Satisfaction is **C33** (over judge outputs); C37 may *cluster*
  trajectories that C33 scored low, but it does not itself score.

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (data source) | **C21** CXDB trajectory store | The content-addressed store C37 **reads trajectories from** via the replay/retrieval seam (spec/C21 I6; spec/C21 §2 lists C36/C37/C38 as P11 consumers). **The sole inventory dependency** (inventory C37 `Depends on: C21`). |
| Upstream (population selector) | **C36** Anomaly detection | Flags the anomalous trajectories fed to C37 via its **`anomaly` signal (spec/C36 I3)** — the carrier spec/C36 commits as "the anomaly→cluster trigger seam"; its record shape is co-frozen with C37 (spec/C36 data-model). *Seam, not an inventory dep edge of C37* (C37's only listed dep is C21); the open residual is the **granularity** (aggregated window vs per-anomaly signals) — OQ-1. |
| Trajectory schema | **C22** CXDB type registry/bundle | Owns the turn/payload schema C37's representation step (I2) reads. C37 uses the registered types; it does not define them. *(Referenced, not a C37 dep edge — mirrors how C21 names C22.)* |
| Embedding engine | **sentence-transformers** (`github.com/UKPLab/sentence-transformers`, Apache 2.0) | The v4-named, mature, clean-licensed embedder (README:254/312; AI-CONTEXT:329/649). Off-the-shelf; C37 pins + invokes it. |
| Clustering engine | **HDBSCAN** (`github.com/scikit-learn-contrib/hdbscan`, BSD) + scikit-learn | The v4-named, mature, clean-licensed density clusterer (README:255/313; AI-CONTEXT:330/650). Off-the-shelf; C37 pins + invokes it. |
| Packaging host | **C02** Pack/tool-node ABI, **C17** Tool-node abstraction | C37 is a **Python tool node in a Gas City pack** (README:254–255 "Python tool node"), invoked via the tool-node protocol. *(Related interface, not a dep edge; mirrors C33 naming C02/C17.)* |
| Downstream (consumer) | **C38** Diagnosis agent (Healer) | Consumes C37's **clusters** and diagnoses **per cluster** (inventory C38 `depends on C37, C21`; README:256). The C37→C38 cluster contract (I5) is the load-bearing seam. |

**Position in the system.** C37 is **Batch-4** (component-inventory line 113), the self-healing tier built in
**Phase 3b** ("Healer in pieces") with C36 anomaly detection, C38 diagnosis, C39 fix/loop-closure (README:459–
466). It is **not foundational** (inventory C37: Foundational? = no) — it is one stage of the P11 pipeline, not
a contract the rest of the system builds on; only **C38** depends on its output. v4's explicit build order is
"**build the simplest first (anomaly detection); save the diagnosis agent for after**" (README:466), placing
C37 *after* C36 (its population source) and *before* C38 (its consumer). It is **feature-flag-gated** with the
self-healing pack (it exists only when the P11 capability is enabled, C03), and stands up only **after C21 is
proven** (spec/C21 §8: the CXDB conformance suite "must pass before C22, C24, C36–C38 … build on C21").

## 3. Interfaces / contracts

Sweep-1: interfaces **named and described**; concrete embedding-model id, HDBSCAN parameter set, the
trajectory→document projection, and the cluster-record schema defer to sweep 2 (and the trajectory record to
C22, the read seam to C21 I6).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Trajectory population read** | inbound (read) | Retrieve the set of trajectories to cluster from **CXDB (C21)** via its replay/retrieval seam (spec/C21 I6); the *which* set is an input selector driven by **C36's `anomaly` signal (spec/C36 I3)** — typically C36's anomalous window. The selector's aggregation granularity (window vs per-anomaly signals) is OQ-1. | C37 (this); **C21** (store), **C36** (selector via I3) |
| I2 | **Trajectory → embeddable representation** | internal | Project each trajectory (a CXDB turn-DAG path) into the **document/text the embedder consumes** (the G32 representation decision — what part of a trajectory carries the failure signal). Sweep-1 names the seam + the default; the canonical representation is sweep-2. | C37 (this) |
| I3 | **Embed (sentence-transformers)** | internal | Embed each representation into a fixed-length vector with the v4-named **sentence-transformers** (README:254; AI-CONTEXT:329). C37 owns model-pin + invocation, not the model. | C37 (this); sentence-transformers (engine) |
| I4 | **Cluster (HDBSCAN)** | internal | Cluster the embeddings with the v4-named **HDBSCAN** (README:255; AI-CONTEXT:330) → a **cluster label per trajectory**, including HDBSCAN's native **noise/outlier** label. C37 owns parameter-binding + invocation, not the algorithm. | C37 (this); HDBSCAN (engine) |
| I5 | **Cluster-set output (→ C38)** | outbound (data) | The tool node's declared output: per cluster, a **cluster record** = member trajectory ids + size + a **representative/exemplar** (e.g. medoid); plus the noise set. The contract **C38** diagnoses per-cluster against (inventory C38 `depends on C37`). *Seam note:* spec/C38 §3.1 lists a per-cluster "**shared-failure signal**" among the cluster-level features it expects C37 to attach — beyond the structural fields above; the **sweep-2 cluster-record freeze (joint with C38, M2)** must reconcile whether such a shared-feature descriptor is in the contract. | C37 (this); C02/C17 (surfacing), C38 (consumer) |
| I6 | **Tool-node lifecycle (pack)** | inbound (ops) | Packaged + invoked as a **Python** Gas City tool node (C02/C17 ABI); configured via pack TOML (embedding-model id/pin, HDBSCAN params, the representation rule, the population selector). | C02/C17 (ABI); C37 (config) |

**Invariants C37 must uphold:**
- **INV-1 (off-the-shelf engines — the bar).** Embedding is **sentence-transformers**; clustering is **HDBSCAN**
  — no custom embedding/distance/clustering algorithm (README:254–255/261; AI-CONTEXT:406). The custom surface
  is I1/I2/I5 wiring only.
- **INV-2 (per-cluster output for C38 — the load-bearing P11 property).** C37's output is a **set of clusters**
  (each with members + a representative), so the downstream diagnosis (C38) runs **once per cluster**, not once
  per trajectory. A clustering that does not yield a per-cluster representative does not satisfy C37's purpose.
- **INV-3 (no diagnosis, no judgement).** C37 assigns **similarity-based cluster labels only**; it makes **no**
  root-cause claim (C38), **no** anomaly decision (C36), and **no** satisfaction/pass-fail score (C33). It
  invokes **no** LLM and writes **no** work bead.
- **INV-4 (noise is surfaced, not silently dropped).** HDBSCAN's **noise/outlier** points (trajectories in no
  dense cluster) are **reported as such** (an explicit noise set + count), never folded into a nearest cluster —
  so a singleton/odd failure is legible to C38/operators rather than mis-grouped. (Mirrors C33 INV-4
  sample-honesty: don't fabricate structure that isn't there.)
- **INV-5 (re-derivable view; owns no source-of-truth).** Given the same trajectory population + the same pinned
  models/params, C37 reproduces the same clustering. The **trajectories** live in CXDB (C21); C37 holds no
  independent store — its output is a **derived view**, re-runnable any time (caching is an optimization, §4).

## 4. Data model / state

C37 **owns the clustering contract + the representation choice**, not durable source-of-truth data. The
**trajectory** is C21/C22's; the **embedding model** is sentence-transformers'. State C37 is the spec-of-record
for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Cluster set (output)** | Per cluster: member trajectory ids, size, a **representative/exemplar** (e.g. medoid); plus the noise set + count. The component's *output*, derivable on demand from C21. | Emitted as tool-node output; optionally recorded (a bead/CXDB result) for C38/loop-closure trace — an *optimization*, re-computable (INV-5). | C37 (shape); C38/C39 (consumers) |
| **Trajectory→document representation rule** | What text/features of a trajectory get embedded (I2 / **G32**). Config + a default; the canonical rule is sweep-2. | Pack TOML (C02/C03 model). | C37 |
| **Clustering config** | Embedding-model id + **version pin**, HDBSCAN parameters (min cluster size, metric, …), the population selector, the representative rule. | Pack TOML (C02/C03 model). | C02/C03 (model); C37 (binding) |
| **Trajectories (read-only input)** | The runs to cluster — **owned by C21 (CXDB)**, schema by **C22**; read-only to C37 via C21 I6. C21 is C37's sole dep edge; C22 is a *referenced* schema owner. | C21 (CXDB). | **C21** (store), **C22** (schema) |
| **Embeddings (transient)** | The per-trajectory vectors between I3 and I4. Intermediate, not source-of-truth; may be cached to avoid re-embedding (optimization, not required state). | In-memory / optional cache. | C37 |

> [FAITHFUL-FILL] v4 names the *engines and their job* ("sentence-transformers + HDBSCAN … standard recipe",
> AI-CONTEXT:406; "Embeds trajectories … clusters similar failures", inventory C37) but **does not specify the
> trajectory→document representation** (what text of a turn-DAG is embedded) nor the **cluster-record schema**.
> The minimal faithful position: C37 owns **no source-of-truth state** — it is a **derived view over CXDB**
> (INV-5), so a re-run reproduces the clustering; the only persisted things are **config** (pack TOML) and the
> **emitted cluster set** (re-computable, optional to store). The concrete representation (I2/G32), the HDBSCAN
> parameter set, the embedding-model id, and the cluster-record fields are **sweep-2**, frozen with **C38** (the
> consumer) and **C22** (the input record).

**Consistency / lifecycle.** C37 stands up in **Phase 3b** with the self-healing pack, **after C21 is proven**
(spec/C21 §8). It owns no durable truth: the **trajectories** survive in CXDB, so a re-run of C37 reproduces the
clustering (INV-5). C37 is therefore a **stateless, re-derivable transform** — read trajectories → embed →
cluster → emit — which is exactly why the bar keeps it thin (no store, no custom algorithm; §6).

## 5. Behavior

**Stand up (Phase 3b).** The Python tool node is packaged and configured: the embedding-model id (pinned), the
HDBSCAN parameters, the trajectory→document representation rule, and the population selector. It is wired
**downstream of C36** (the anomalous window it clusters) and **upstream of C38** (which diagnoses its clusters).
It comes up only **after C21's conformance suite passes** (spec/C21 §8).

**Cluster path (steady state).**
1. **Select population (I1):** resolve the set of trajectories to cluster (typically C36's anomalous window) and
   **read them from CXDB (C21)** via the replay/retrieval seam (spec/C21 I6).
2. **Represent (I2 / G32):** project each trajectory's turn-DAG into the **document/text** the embedder consumes
   (the representation decision; default below).
3. **Embed (I3):** run **sentence-transformers** over each representation → one fixed-length vector per
   trajectory (no LLM call, no judgement — INV-3).
4. **Cluster (I4):** run **HDBSCAN** over the vectors → a **cluster label per trajectory**, with HDBSCAN's
   native **noise/outlier** label preserved (INV-4).
5. **Emit (I5):** for each cluster, produce a **cluster record** (members + size + representative/medoid) plus
   the noise set; surface it as the tool-node output for **C38** to diagnose **per cluster** (INV-2).

**Re-computation.** Because C37 owns no source-of-truth (INV-5), a fresh clustering over a (possibly enlarged)
trajectory population can be requested at any time; the result is a pure function of the current trajectories +
the pinned models/params. There is no checkpoint to recover.

> [FAITHFUL-FILL] **Representation default (I2/G32).** v4 names no representation. The minimal faithful default
> consistent with "**sentence-transformers** … standard recipe" (AI-CONTEXT:406) is to embed a **textual
> rendering of the trajectory's turns** (the conversation/turn text CXDB already stores) — i.e. use the
> sentence-transformer on the trajectory-as-text, the library's intended use. Richer/structured representations
> (tool-call sequences, error signatures, last-N turns only) are a **sweep-2** optimization (OQ-2). This default
> requires no custom feature engineering — exactly the "standard recipe" posture; anything beyond it is flagged
> against the bar.

> The exact embedding-model id, the HDBSCAN parameter set (min cluster size / metric / cluster-selection), the
> representation projection, and the cluster-record schema are **sweep-2+** (frozen with C38 + C22). Sequence/
> state diagrams (Mermaid) and pseudocode are sweep-2/3.

## 6. Failure modes & handling

C37 carries gaps **G32** (cost) and **G33** (partial-failure of the Python OSS stack) at this component.

**G32 (major) — cost is essentially unmodeled; specifically "embedding all trajectories (sentence-transformers)"
is named as an unmodeled cost. ADDRESSED HERE (bounded + deferred to C46).**
> [AMBIGUITY: G32] G32 flags that v4 has **no cost model** for, among others, **embedding all trajectories**
> (ambiguities-and-gaps G32, naming "embedding all trajectories (sentence-transformers)"), while P12's headline
> meta-metric is cost-per-satisfaction (README:269). Two readings of C37's obligation. **(a)** C37 must embed
> **every** trajectory continuously (embed-all), making embedding a standing cost the system must model; **(b)**
> C37 embeds **only the population it is asked to cluster** — typically C36's **anomalous window**, not the full
> corpus — so the per-run cost is bounded by the anomalous set, and the *cost-per-satisfaction* accounting is
> **C46's**, not C37's. **Chosen: (b).** It is most consistent with v4: C37 sits in the loop **after** anomaly
> detection ("Observability → **anomaly** → diagnosis", README:248; build order README:466), so the natural
> input is the flagged window, not the entire store; and v4 explicitly places the **cost-per-satisfaction
> model** at the meta-metric layer (**C46** — whose inventory row is "Records cost-per-satisfaction … needs a
> defined cost model" and which carries G32 alongside C37; the explicit deferral ruling is review-log:154
> "C29:G32 — cost-per-satisfaction model deferred to C46"), not inside a P11 stage. Faithful handling: (1) C37
> embeds **the supplied population** (bounded by the
> selector, default = the anomalous set), not the whole corpus; (2) embeddings **may be cached** (content-keyed
> on the trajectory) so re-clustering does **not** re-pay embedding — a cheap, faithful cost lever using
> sentence-transformers as-is, no custom infra; (3) the **cost figure itself** (tokens/compute per embedding ×
> population size) is **surfaced to C46** and **not modelled in C37** (OQ-3). Note that the named library runs
> **local embedding models** (sentence-transformers is local/CPU-capable and needs no judge-provider tokens —
> a property of the library, not a v4 statement), so this cost is compute, not per-call LLM spend — materially
> cheaper than the C32 judge or C38 diagnosis costs. *Whether an embed-all
> background mode is ever needed (reading (a)) is a sweep-2/C46 question, not a Sweep-1 design force.*

**G33 (major) — no story for partial/cascading failure of the OSS stack; specifically "When a Python tool node
OOMs?" and "When CXDB is down mid-run?". ADDRESSED HERE (fail-isolated; loop is best-effort).**
> [AMBIGUITY: G33] G33 names exactly C37's situation — a **Python tool node** (PyOD, **sentence-transformers,
> HDBSCAN**) that can **OOM**, plus the **CXDB-down** read dependency (ambiguities-and-gaps G33). Two readings.
> **(a)** Self-healing is **load-bearing online** — a C37 failure must not stall the factory, but also must not
> silently skip failures that need healing. **(b)** Self-healing is a **best-effort background loop** layered on
> a substrate whose source-of-truth already survives (beads + event bus + CXDB), so a C37 failure **degrades the
> loop, not the factory**. **Chosen: (b), with fail-isolation.** Consistency with v4: P11 is an **additive**
> observability→diagnosis loop over a substrate that runs without it (spec/C21 chose the same fail-open reading
> for CXDB-down — the run proceeds on beads+events, G33 at C21); and v4 places durable-workflow survival on
> **Gas City Orders / C40**, not on the clustering stage. Faithful handling: (1) **CXDB read unavailable (C21
> down)** → C37 **defers/yields** (no population to read) rather than crashing; the loop retries on the next
> tick (this mirrors spec/C21's fail-open + the C40 durable-Order retry, **not** a custom buffer in C37). (2)
> **Python-tool-node OOM / library crash** → the tool node **fails as a unit** (the Gas City tool-node boundary
> contains it; the factory's other work is unaffected) and is **re-dispatchable**; the honest Sweep-1 mitigation
> for OOM is **bounding the population** (reading (b) of G32 — cluster the anomalous window, not the whole
> corpus) and treating a too-large population as a **sweep-2 batching/streaming** concern, not in-stage HA. (3)
> **Embedding/clustering partial failure** (a malformed trajectory the embedder rejects) → **exclude that
> trajectory with a counted exclusion** and cluster the rest (fail-open per record; mirrors spec/C33's
> exclude-and-continue). C37 introduces **no** circuit-breaker/replication of its own — the durability seam is
> **C40 (Orders)** and the read fail-open is **C21**'s; inventing in-stage HA would exceed faithful scope (the
> bar). *The OOM-ceiling / batch-size for a very large anomalous window is OQ-4.*

**Other failure cases.**
- **Empty / too-small population (I1 returns 0 or n<min-cluster-size).** Emit an explicit *insufficient-data*
  result (HDBSCAN cannot form clusters below its min size) rather than a fabricated grouping; never invent
  clusters from too few trajectories. *[FAITHFUL-FILL]: minimal honest choice; mirrors C33's small-n honesty
  and INV-4.*
- **Everything is noise (HDBSCAN labels all points outliers).** Surface that **no dense failure-mode emerged**
  (all-noise is a *legible* result for C38/operators — the failures were too dissimilar to group), not an error.
  *[FAITHFUL-FILL]: HDBSCAN-native outcome surfaced, not suppressed (INV-4).*
- **Degenerate single giant cluster.** Report it as one cluster (a single dominant failure mode is a valid,
  useful result for C38); parameter tuning to split it is a **sweep-2** concern (OQ-2), not a Sweep-1 algorithm
  change.

> F-mode applicability is owned by **C57** (coverage map). C37 is the **grouping** stage that makes several P11
> failure classes *diagnosable per-mode* rather than per-run — it underwrites, but does not by itself resolve,
> the modes F-MODE-COVERAGE §3 routes to the self-healing loop: **F22** (zombie agents — anomaly→diagnosis over
> clustered liveness failures), **F23** (stalled-vs-thinking), **F40** (last-mile drift), and the
> drift/subversion classes **F54/F55** (objective drift over cycles — clustering recurring anomalous
> trajectories is what makes a drift *pattern* visible). C37 **detects nothing and decides nothing** about these
> (that is C36/C38); it makes them **clusterable**. The canonical F-mode mapping is deferred to **C57**.

**The bar — what got DROPPED.** Per the ruthless bar, C37 is held to *only* the P11-tied capability (group
similar failures so C38 diagnoses per-cluster — INV-2) plus the **low-effort wiring** v4 explicitly frames as
glue around a "standard recipe" (AI-CONTEXT:406). **Dropped / refused as non-principle, stack-already-does-it,
or not-C37's:** (1) any **custom embedding model, distance metric, dimensionality reduction, or clustering
algorithm** — the stack is **sentence-transformers + HDBSCAN**, both mature/clean-licensed and explicitly the
named choice (README:254–255/261/312–313; AI-CONTEXT:329–330/406); a bespoke vectorizer or clusterer would be
exactly the over-engineering the bar rejects (INV-1). (2) **Anomaly detection** (is-this-wrong) — that is
**C36**; C37 only groups a supplied set. (3) **Root-cause / diagnosis** (why) — that is **C38**; C37 hands over
clusters and makes no claim. (4) **A cost model** (cost-per-embedding/satisfaction accounting) — that is
**C46**; C37 surfaces the figure but models none (G32 reading (b)). (5) **In-stage HA / circuit-breakers /
replication** — durability is **C40 (Orders)** + the **C21** read fail-open; C37 fail-isolates only (G33 reading
(b)). (6) **Cluster *quality* metrics / auto-tuning** (silhouette sweeps, parameter search) — a sweep-2 polish,
not a Sweep-1 principle capability. What is **kept**: the **wiring** (read C21 → embed → cluster → emit), the
**representation choice** (I2/G32 — the one genuinely-custom, load-bearing decision, defaulted minimally), and
the **cluster representation handed to C38** (I5/INV-2 — the per-cluster contract that makes the whole P11 batch
work).

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security.** C37 reads **trajectory bodies** (turn text) from CXDB — more sensitive than C33's scores-only
  path; it inherits **C21**'s access posture (and the BLAKE3 tamper-evidence on what it reads) and adds no new
  exposure. It performs **no** model/judge call (no provider credential — the embedder is local; D-1 is
  irrelevant to C37). Trajectory text may contain secrets/PII — handling inherits the CXDB/observability posture
  (G37 thread), not a new C37 control.
- **Cost.** A **local/CPU** sentence-transformers embedding + HDBSCAN clustering over the **anomalous
  population** (not the whole corpus — G32 reading (b)) — **compute, not LLM tokens**; materially cheaper than
  C32 (judge) or C38 (diagnosis). **Embedding caching** (content-keyed on the trajectory) avoids re-paying on
  re-cluster. The cost **figure** feeds **C46**; C37 models no cost itself (G32).
- **Scale.** Cost is roughly linear in population size (embed n trajectories, cluster n vectors). The honest
  scale note: a **very large anomalous window** could pressure a single Python tool node's memory (G33 OOM) —
  handled at sweep-2 by **bounding/batching** the population, not by bespoke scaling machinery (the bar). HDBSCAN
  over large n is a known cost; parameter/algorithm tuning for scale is sweep-2 (OQ-4).
- **Observability.** C37's own health (population size clustered, cluster count, noise fraction, exclusion count,
  embedding cache hit-rate) is worth emitting as events for auditability — and the **cluster count / noise
  fraction** is itself a useful P11 signal (how many distinct failure modes are live). C37 is a stage *in* the
  observability loop, not a heavy emitter.
- **Ops.** Pack-delivered **Python** tool node operated with the self-healing pack in Phase 3b (README:459–461).
  **Pin the embedding-model id + the sentence-transformers/HDBSCAN versions** so the clustering is reproducible
  (INV-5; inherits the eval/P11-tier version-pin discipline). Comes up only after **C21** is proven.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (groups similar failures — INV-2, P11):** given a population of trajectories, C37 emits a **set of
   clusters**, each with member trajectory ids + a **representative/exemplar**, so C38 can diagnose **per
   cluster** (README:255; inventory C37/C38).
2. **AC-2 (reads trajectories from CXDB — I1):** C37 reads the trajectory population from **C21** via its
   retrieval seam (spec/C21 I6) and clusters exactly that population.
3. **AC-3 (off-the-shelf engines — INV-1, the bar):** the embedder is **sentence-transformers** and the
   clusterer is **HDBSCAN** (README:254–255; AI-CONTEXT:329–330/406); **no** custom embedding/clustering
   algorithm is present. (Verifiable: the pack declares the two pinned libraries as its engines.)
4. **AC-4 (no diagnosis / no judgement — INV-3):** C37 makes **no** LLM/judge call, renders **no** root-cause
   and **no** satisfaction/pass-fail, and writes **no** work bead; it emits **only** a clustering. (Verifiable:
   C37 runs with no judge provider configured.)
5. **AC-5 (noise surfaced — INV-4):** HDBSCAN **noise/outlier** trajectories are reported as an explicit noise
   set + count, never folded into a nearest cluster; an all-noise outcome is a legible result, not an error.
6. **AC-6 (reproducible clustering — INV-5):** the same population + pinned models/params re-produces the **same**
   clustering (C37 owns no source-of-truth; it is a re-derivable view over C21).
7. **AC-7 (consumable by C38 — I5):** the emitted cluster set (members + size + representative + noise) is
   consumable by **C38** for per-cluster diagnosis (inventory C38 `depends on C37`).
8. **AC-8 (bounded population / cost — addresses G32):** C37 embeds **only the supplied population** (default =
   the anomalous window), **not** the whole corpus; embeddings are **cacheable** so re-clustering does not
   re-embed; the cost figure is **surfaced** (for C46), not modelled in C37.
9. **AC-9 (fail-isolated — addresses G33):** with **C21 down**, C37 **defers** (does not crash the factory); on
   **OOM/library crash** the Python tool node **fails as a contained unit** and is re-dispatchable; a **malformed
   trajectory** is **excluded-with-count**, not allowed to poison the clustering.

**Test strategy.** A **trajectory-clustering pack** that seeds a synthetic trajectory population in CXDB (C21) —
several *known* failure families plus some singleton/odd trajectories and a few malformed ones — and drives
AC-1…AC-9: in particular that **known-similar failures land in the same cluster** (AC-1, the headline behaviour;
the *clustering-match* half of v4's **Healer-scenario** check, README:499 "feed it failure trajectories the team
manually clustered, ensure its clusters match" — a line v4 attributes to the Healer scenario set, shared with
**C38** which owns the *diagnosis-match* half; C37 owns the clustering-fidelity half it rests on), that **noise
is surfaced** (AC-5), that the clustering is **reproducible** (AC-6) and uses the
**off-the-shelf** engines (AC-3), and that it **fail-isolates** on a down store / malformed record (AC-9). This
suite **must pass before C38 consumes C37's clusters**, since C38 assumes the per-cluster contract is the unit
of diagnosis — and it runs **only after C21's conformance suite passes** (spec/C21 §8).

## 9. Open questions

- **OQ-1 (→ review-log, top): C36↔C37 population seam.** C36's side already commits the *carrier*: spec/C36 I3
  emits a typed **`anomaly` signal** (carrying a trajectory pointer into C21) and names "the **anomaly→cluster
  trigger seam is C36's signal (I3)**", with C37 consuming it (spec/C36 §1/§2); spec/C36 also co-freezes the
  `anomaly`-record shape "with C37/C38, the principal consumers". So the carrier into I1 is **C36's `anomaly`
  signal (C36 I3)**, not an open question. What *remains* open is the **granularity/aggregation**: does C37's I1
  input arrive as the **aggregated anomalous window** (C37 batches the individual per-anomaly C36 signals into a
  population to cluster) or does C36 hand C37 a window directly — i.e. does C37 cluster exactly C36's flagged set
  or a broader set C36 merely scores ("anomaly → diagnosis", README:248)? This shapes I1 and is **co-owned with
  C36 OQ-2** (the signal carrier C20-bead-vs-C23-event + record shape); freeze jointly with C36 at sweep-2.
- **OQ-2 (→ review-log): trajectory representation (I2/G32) + HDBSCAN parameters + distribution of clusters.**
  The Sweep-1 default embeds trajectory-as-text; the canonical representation (turn text vs tool-call sequences
  vs error signatures vs last-N turns), the embedding-model id, and the HDBSCAN parameter set (min cluster size,
  metric, cluster-selection) — which jointly determine cluster quality — freeze at sweep-2 with **C38** (the
  consumer) against real trajectories.
- **OQ-3 (→ review-log): G32 cost figure ownership.** §6 binds C37 to embed **the bounded anomalous population**
  (not the corpus) and surface the cost to **C46**; confirm the **cost-per-satisfaction / cost-per-embedding**
  accounting lives at **C46**, not in C37, and whether any **embed-all background mode** (reading (a)) is ever
  required.
- **OQ-4 (→ review-log): G33 OOM ceiling + batching.** §6 fail-isolates the Python tool node and bounds the
  population; confirm the **memory ceiling / batch size** for a large anomalous window (when does it need
  streaming/batched embedding+clustering at sweep-2), and that the **durability seam is C40 (Orders)** + the
  **C21** read fail-open, not in-stage HA in C37.
