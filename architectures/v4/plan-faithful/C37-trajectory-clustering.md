# C37 — Trajectory Embedding & Clustering  (Build Plan, canonical track)

> Source / Spec ref: spec/C37-trajectory-clustering.md

## 1. Work breakdown

| Task | Description | Size | Prerequisites |
|---|---|---|---|
| T1 | **Freeze the clustering seam contract (M1)** — the **input** seam (trajectory population read from CXDB/C21 via the replay/retrieval seam, spec/C21 I6; the population *selector* shared with C36), and the **output** contract (the per-cluster record: member trajectory ids + size + representative/exemplar + the noise set — I5). This is the interface **C38** builds against. | S | C21 retrieval seam (spec/C21 I6), C22 trajectory schema, C36 selector seam |
| T2 | **Python pack/tool-node skeleton** — package C37 as a **Python** Gas City tool node per C02/C17 ABI; config surface (embedding-model id + pin, HDBSCAN params, the trajectory→document representation rule, the population selector) per C03 model (README:254–255 "Python tool node"). | S | C02/C17 ABI, T1 |
| T3 | **Trajectory population read (I1)** — read the supplied population's trajectories from **C21** via the retrieval seam; exclude malformed trajectories with a **counted exclusion** (fail-open per record). Bound the population to the selector (default = the anomalous window) — the G32/G33 lever. | M | T2, C21 retrieval seam, C22 type |
| T4 | **Trajectory → embeddable representation (I2 / G32)** — project each trajectory's turn-DAG into the **document/text** the embedder consumes. **Default = trajectory-as-text** (`[FAITHFUL-FILL]`, the "standard recipe" use of sentence-transformers, AI-CONTEXT:406); leave a clean extension point for richer representations (tool-call sequences / error signatures / last-N turns). **The one genuinely-custom decision.** | M | T3 |
| T5 | **Embed (sentence-transformers) (I3)** — invoke the v4-named, **pinned** sentence-transformers (README:254; AI-CONTEXT:329) to produce one fixed-length vector per trajectory; **cache embeddings** content-keyed on the trajectory so re-cluster does not re-embed (G32 cost lever). **No custom vectorizer** (the bar / INV-1). | S | T4, sentence-transformers pinned |
| T6 | **Cluster (HDBSCAN) (I4)** — invoke the v4-named, **pinned** HDBSCAN (README:255; AI-CONTEXT:330) over the embeddings → a cluster label per trajectory; **preserve HDBSCAN's native noise/outlier label** (INV-4). **No custom clustering algorithm** (the bar / INV-1). | S | T5, HDBSCAN pinned |
| T7 | **Cluster-record output (I5 / INV-2)** — for each cluster emit members + size + a **representative/exemplar** (e.g. medoid) + the noise set; shape it as the tool-node declared output for **C38** to diagnose **per cluster**. **The load-bearing keep.** | M | T6 |
| T8 | **Degenerate-case honesty (INV-4)** — n<min-cluster-size → explicit *insufficient-data*; all-noise → legible "no dense failure-mode"; single-giant-cluster → reported as one cluster (tuning is sweep-2). | S | T6, T7 |
| T9 | **Fail-isolation wiring (addresses G33)** — C21-down → **defer/yield** (retry next tick; durability seam is C40 Orders + C21 fail-open, not in-stage); OOM/library crash → fail as a **contained, re-dispatchable** tool-node unit (bound the population). **No in-stage HA/circuit-breaker** (the bar). | S | T3, T5, T6 |
| T10 | **Clustering pack (AC-1…AC-9)** — synthetic CXDB trajectory population (known failure families + singletons + malformed) driving all acceptance tests; especially **known-similar-failures-co-cluster** (the adversarial check, README:499 "ensure its clusters match"), noise-surfaced, reproducible, off-the-shelf-engines, fail-isolated. | L | T3–T9, C21 test fixture |

## 2. Dependency graph

**Must precede C37:**
- **C21** (the CXDB trajectory store C37 reads — its retrieval seam, spec/C21 I6) — and C21's **conformance
  suite must pass first** (spec/C21 §8: "must pass before … C36–C38 … build on C21"). **C37's sole inventory
  dependency.**
- **sentence-transformers** + **HDBSCAN** (the engines, version-pinned) + **C02/C17** (Python pack + tool-node
  ABI to package/invoke).
- *(Seam, not a hard dep edge)* **C36** anomaly detection — the population selector C37 typically clusters
  (OQ-1); and **C22** — the trajectory schema T4 reads.

**C37 must precede:**
- **C38** diagnosis agent (Healer) — it diagnoses **per cluster** against C37's output (inventory C38 `depends
  on C37, C21`). C37's clusters are the unit C38 assumes.

**Critical path inside C37:** T1 → T3 → T4 → T6 → T7 → T10. The load-bearing tasks are **T4 (representation —
the one custom decision, G32)** and **T7 (the per-cluster contract handed to C38, INV-2)** — but note both are
*thin*: T5/T6 wrap **sentence-transformers + HDBSCAN** with **no** custom algorithm (INV-1), and C37 owns **no**
durable state (a re-derivable view over C21, INV-5). The **G32 cost bound** (T3 population-bounding + T5 caching)
and the **G33 fail-isolation** (T9) are deliberately scoped to *avoid* new capability (no cost model in C37 —
that's C46; no in-stage HA — that's C40 + C21).

## 3. Parallelization

Once **T1 (seam freeze)** and **T2 (Python skeleton)** land, two thin workstreams fan out concurrently:
- **WS-A (read/represent):** T3 (population read) → T4 (representation). The input spine; can build against a
  synthetic CXDB trajectory fixture while C36's selector firms up.
- **WS-B (embed/cluster/emit):** T5 (embed) → T6 (cluster) → T7 (cluster-record output) → T8 (degenerate-case
  honesty). The recipe spine; can build against synthetic embedding inputs before WS-A's real read lands.
- **T9 (fail-isolation)** rides across both (read-side defer + tool-node OOM containment); **T10** (clustering
  pack) joins both.
WS-A and WS-B meet at the T4→T5 handoff (the per-trajectory representation feeding the embedder).

## 4. Interfaces-first / contract milestones

- **M1 — clustering seam contract freeze (T1):** the two contracts dependents/sub-streams build against:
  (a) **input** = trajectory population read from C21 (spec/C21 I6) + the population selector (C36 seam, OQ-1);
  (b) **output** = the **per-cluster record** (members + size + representative + noise set, I5).
  Freezing M1 lets WS-A build against synthetic CXDB trajectories and WS-B against synthetic embeddings in
  parallel, and lets **C38** stub against the cluster-record output shape.
- **M2 — recipe + representation fixed (T4/T6):** the **trajectory→document representation** (default
  trajectory-as-text, G32), the **pinned** sentence-transformers model id, and the **pinned** HDBSCAN parameter
  set — frozen with **C38** (the consumer) against real trajectories, **before** C38 reasons over clusters.
- **M3 — cost/failure posture fixed (T3/T5/T9):** the population is **bounded** (default = anomalous window, not
  the corpus — G32), embeddings are **cached** (re-cluster ≠ re-embed), and C37 **fail-isolates** (durability =
  C40 Orders + C21 fail-open) — confirmed before scale/throughput claims.

## 5. Risks & de-risking order

1. **Confirm first — C21 read seam + conformance (T3).** C37 cannot cluster what it cannot read; verify the
   **C21 retrieval seam** (spec/C21 I6) and that **C21's conformance suite passes** (spec/C21 §8) before deep
   build. This retires the foundational read dependency.
2. **Spike — representation + cluster quality (T4/T6/OQ-2).** The **one genuinely-custom decision** is the
   trajectory→document representation; cluster *quality* depends on it + the HDBSCAN params. De-risk with the
   **clustering-match** half of v4's Healer-scenario check (README:499: "feed it failure trajectories the team
   manually clustered, ensure its clusters match" — v4 frames this as the Healer scenario set, shared with C38;
   C37 owns the clustering-fidelity half) on a small labelled set, against the **pinned** sentence-transformers
   + HDBSCAN, so no custom algorithm creeps in (the bar / AC-3).
3. **Confirm — C36↔C37 population seam (T1/OQ-1).** The carrier is settled on C36's side — C37's I1 selector is
   **C36's `anomaly` signal (spec/C36 I3)**, the committed "anomaly→cluster trigger seam", record shape
   co-frozen with C37. The open residual is the **granularity**: whether C37 batches per-anomaly C36 signals
   into the population or C36 hands a window directly (and whether C37 clusters exactly the flagged set or a
   broader one) — it shapes I1 and the cost bound; freeze jointly with C36 OQ-2.
4. **Bound — G32 cost (T3/T5/OQ-3).** Confirm C37 embeds the **bounded anomalous window** (not the corpus) and
   that the **cost-per-satisfaction** accounting lives at **C46**, not C37; verify **embedding caching** is the
   cheap, off-the-shelf cost lever (no custom infra).
5. **Confirm — G33 fail-isolation + OOM ceiling (T9/OQ-4).** Verify a C21-down read **defers** (no factory
   crash), the Python tool node **fails as a contained unit** on OOM, the durability seam is **C40 Orders + C21
   fail-open** (not in-stage HA), and establish the **batch-size/memory ceiling** for a large window (streaming
   = sweep-2).

## 6. Definition of done

**Per-component DoD:** the clustering pack (T10) passes **AC-1…AC-9** against a synthetic CXDB trajectory
population — **groups similar failures** into clusters each with a **representative** so **C38 diagnoses per
cluster** (P11/INV-2), **reads trajectories from C21**, uses the **off-the-shelf** sentence-transformers +
HDBSCAN with **no custom embedding/clustering algorithm** (the bar/INV-1), makes **no LLM/judge call and no
diagnosis/satisfaction claim** (INV-3), **surfaces HDBSCAN noise** (INV-4), is **reproducible** owning no
source-of-truth (INV-5/a re-derivable view over C21), **bounds the population + caches embeddings** (G32 cost),
and **fail-isolates** on a down store / OOM / malformed record (G33 — durability is C40 + C21, not in-stage). C37
is a **Python** tool node in a Gas City pack.

**Per-task DoD:**
- T1: M1 contracts written + agreed with C21/C22/C36/C38 owners; sub-streams + C38 can stub against them.
- T3/T4: a synthetic population reads + represents correctly; malformed trajectories excluded-with-count;
  population bounded to the selector (AC-2/AC-8/AC-9).
- T5/T6: embeddings via **pinned** sentence-transformers (cached); clusters via **pinned** HDBSCAN with noise
  preserved (AC-3/AC-5); **no custom algorithm** present (AC-3, the bar).
- T7: per-cluster record (members + size + representative + noise) consumable by **C38** (AC-1/AC-7, INV-2).
- T8: n<min → insufficient-data; all-noise legible; single-giant-cluster reported (AC-5).
- T9: C21-down → defer; OOM → contained/re-dispatchable; durability = C40 + C21 fail-open (AC-9).
- T10: full AC suite green, including the **known-similar-failures-co-cluster** adversarial check (README:499);
  **must pass before C38 consumes C37's clusters**, and runs only **after C21's conformance suite passes**.

**Open questions to resolve before sweep 2** (mirrored to review-log): OQ-1 (C36↔C37 population seam), OQ-2
(trajectory representation/G32 + HDBSCAN params + cluster distribution — frozen with C38), OQ-3 (G32 cost figure
ownership at C46; any embed-all background mode), OQ-4 (G33 OOM ceiling/batching + durability seam = C40 Orders +
C21 fail-open).
