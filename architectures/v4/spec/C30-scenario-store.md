# C30 — Scenario Authoring & Store (read-isolation)  (Spec, canonical track)

> Source: README §"Principle 5 — Scenarios as held-out test set" (L164–177: L166 "Scenarios are external
> to the codebase. The agent **cannot see** them during work."; the 4-row table — "Scenario **authoring
> format**" = "Defines a scenario's structure" / "**Inspect AI Task DSL (Python)**" / MIT / "Gas City pack
> wraps Inspect AI"; "Scenario **storage** with read-isolation" = "Prevents agent from reading scenarios
> during work" / "**Separate git repo + file permissions + Gas City rig partition**"; "Holdout integrity
> audit" = "Detects if isolation has been violated" — *that row is C34, not C30*; L175 "Inspect AI has the
> strongest **agent-trajectory model**"; L177 placement "Install Inspect AI, write a small pack that
> exposes it as a tool node"); README §Phase 2 (L417–442: L423 "Install Inspect AI (MIT)"; L424 "Gas City
> pack wrapping Inspect AI as a scenario provider (the `[[service]] type = "inspect_ai"` block)"; L425
> "Set up **scenario storage: separate git repo + filesystem permissions** enforcing
> read-only-from-implementer; OPA policy for finer control later"; L442 "the harder parts are the Inspect
> AI wrap and the scenario isolation policy"); README §Part 7 (L500 foundational OSS adopted verbatim; L526
> "No specific scenario suite at the start … the broader scenario library grows over time"); README §"the
> bets" (L499 "Factory-built components have their own scenarios … the Healer agent's scenarios are
> adversarial … the twins' scenarios verify behavioral fidelity"); AI-CONTEXT §1.3 (L35 "Scenarios as
> held-out test set — External, unread-by-agent, independently judged"); AI-CONTEXT §6.2 "Layer 2"
> (L294–305: L298 "Scenario authoring | **Inspect AI** | MIT | Mature; recommended"; L303 "Holdout
> isolation | **None purpose-built** | DIY | OPA + file permissions composition"); AI-CONTEXT §7 layer
> map (L373 "Inspect AI | L2: authoring + runner + judge + aggregation | MIT"); AI-CONTEXT §11 decisions
> (L467 "Inspect AI for Layer 2 | Yes | Most mature general-purpose; agent-trajectory model fits"); AI-CONTEXT
> §13.3 (L582–608: the `[[rig]]` blocks `scenario_authoring`/`implementer` with `read_partition`/
> `write_partition`; the comment "explicitly does NOT include scenarios in read_partition"; the
> `inspect_eval` `[[tool]]` subprocess with `work_partition = "scenarios"`); AI-CONTEXT §12 open questions
> (L512 "Inspect AI's session-id model vs Gas City's … likely needs adapter layer"; L513 "OPA policy for
> scenario isolation"); AI-CONTEXT §15.2 repo (L638 "Inspect AI: `github.com/UKGovernmentBEIS/inspect_ai`");
> AI-CONTEXT §16.4 (L698 "Find the scenarios at `scenarios/<component>/`"); F-MODE-COVERAGE §1 (F1 "held-out
> scenarios (P5)"; F9 "**Cryptographically signed scenarios at day-0**"; **F28** "Holdout leakage" →
> "Scenario storage with read-isolation … file permissions + OPA + rig partition" — Addressed), §6 (F55
> "held-out scenarios from human-authored corpus" — Partial); component-inventory C30 row (subsystem
> Evaluation & Judge; kind data-store; "Inspect AI scenario DSL authored in an isolated rig; separate repo +
> perms + partition keep scenarios unread by implementer"; maps A45/A46/A22i-rig/B22/B40; **depends on C17,
> C42**; gaps **G10, G21, G28**; foundational: **yes**; Batch 3); review-log **D-1** (judge SAME provider as
> coder ⇒ holdout rests on rig partition + role isolation, not model family), **D-2** (bundle-id namespace —
> if scenarios are CXDB-typed, the root is `softwarefactory.v4.*`), **D-6** (canonical track), **D-13**
> (holdout **enforcement + audit is C34**; **C42 provides** the partition; **C30 stores/authors** inside the
> isolated rig but does **not** itself enforce read-isolation); the C42 spec (`spec/C42-rig-partitioning.md`
> §1/§2 — the partition/role policy C30 sits inside) and C17 spec (`spec/C17-tool-node-abstraction.md` §1 —
> the tool-node abstraction the Inspect AI wrap is realized over).
> Inventory ID: C30   Kind: data-store   Status: sweep-1
> Track: canonical (faithful posture — elaborate v4 exactly; mark inferred fills)

## 1. Purpose & responsibility

C30 is the factory's **scenario authoring + storage layer**: it owns *where scenarios live and how they
are authored*, in a form that is **held out** from the implementer. Scenarios are authored in the
**Inspect AI Task DSL** — an *adopted, off-the-shelf* Python eval framework
(`github.com/UKGovernmentBEIS/inspect_ai`, MIT; "Inspect AI has the strongest agent-trajectory model",
README:175; "Most mature general-purpose; agent-trajectory model fits", AI-CONTEXT:467) — and **stored in a
separate git repo** that the implementer rig cannot read (README:171/425). C30 is the *spec-of-record for
the scenario corpus as a held-out artifact*: the DSL it is written in, the repo it lives in, and the
**`scenarios` partition** and **`scenario_authoring` rig** it is bound to. Phase-0/2 **tamper-evidence +
provenance** for the corpus come from the **separate git repo's content-addressed commit history** (git's
object store is content-addressed — AI-CONTEXT:404 — and v4 treats content-addressing as tamper-evidence,
AI-CONTEXT:236), *not* from custom cryptographic signing: per **D-14**, cryptographic scenario signing is
**deferred to FE-3, blocked on the open secrets gap G37** (a plaintext key collapses the assurance —
XC-6/D-14). See §1 bullet 4 + §6 + §7.

C30 delivers the *storage half* of **Principle 5 (scenarios as a held-out test set)**: "Scenarios are
external to the codebase. The agent cannot see them during work." (README:166; AI-CONTEXT §1.3 L35
"External, unread-by-agent, independently judged"). It is the upstream of the whole evaluation tier — the
scenario **runner** (C31) executes what C30 stores, the **judge** (C32) scores trajectories against it, and
**holdout-integrity enforcement/audit** (C34) polices the read-isolation C30's storage layout makes
auditable.

**Critical boundary (D-13).** C30 **stores and authors** scenarios *inside* the isolated rig; it does **NOT
enforce read-isolation**. Per review-log D-13: **C42 PROVIDES** the role/partition (the `scenario_authoring`
rig + the `scenarios` partition, and the invariant `scenarios ∉ read_partition(worker)`), and **C34 OWNS**
the holdout-integrity *enforcement + after-the-fact audit*. C30's job is to *put the scenarios in the place
C42 partitioned and C34 audits* — author them in the `scenario_authoring` rig, persist them in the separate
repo / `scenarios` partition — not to police access. Per D-1 the judge is the *same provider/family* as the
coder, so the holdout guarantee rests on **rig partitioning (C42) + role isolation**, not model-family
diversity; C30's contribution to that guarantee is *correct placement of the corpus*, nothing more.

**Responsibilities (what C30 is the spec-of-record for):**
- **Scenario authoring in the Inspect AI Task DSL** — scenarios are Inspect AI `Task` objects (Python),
  *adopted as-is*; C30 owns *that this is the authoring format* and the small Gas City pack that exposes
  Inspect AI as a scenario provider (the `[[service]] type = "inspect_ai"` block, README:424; AI-CONTEXT
  §6.2 L298). C30 does **not** author a DSL — Inspect AI provides it (the bar: off-the-shelf ⇒ adopt).
- **Held-out storage layout** — scenarios live in a **separate git repo** + the **`scenarios` partition**
  (README:171/425; AI-CONTEXT §13.3), organized as `scenarios/<component>/` (AI-CONTEXT §16.4 L698) so the
  runner/judge/audit can resolve a component's scenarios by path. C30 owns *the repo + the on-disk layout*;
  the *partition policy* over it is C42's, the *audit of reads against those paths* is C34's.
- **Authoring confined to the `scenario_authoring` rig** — scenarios are written by the `scenario_authoring`
  rig (`read_partition`/`write_partition = "scenarios"`, AI-CONTEXT §13.3), never by the implementer rig.
  C30 owns *that authoring happens in that rig*; C42 owns *the rig/partition definition* and C34 *enforces
  the implementer's exclusion* (D-13).
- **Corpus tamper-evidence + provenance via the git repo (custom signing DEFERRED → FE-3/G37)** — silent
  scenario edits are detectable because the corpus lives in the **separate, content-addressed git repo**
  (INV-1): git's commit history is immutable + content-addressed (AI-CONTEXT:404) and attributable to the
  committing `scenario_authoring` rig, and v4 treats content-addressing as tamper-evidence (AI-CONTEXT:236).
  This is the Phase-0/2 mechanism. **Custom cryptographic "day-0 signing" is DEFERRED, not a KEEP** — it
  fails the capability-for-principle bar (it adds no tamper-evidence the content-addressed git repo +
  `scenarios`-partition isolation do not already provide at Phase-0; the *only* delta it could add —
  non-repudiation against an attacker who can rewrite git history — needs a key, and there is **no secrets
  store**: G37 is open, owned by C03, plaintext today, which collapses the assurance, XC-6). Per **D-14**
  this is the materially-identical signing question already settled **optional/deferred → FE-3 (blocked on
  G37)**; C30 does not re-open it. *(v4's only signing source — F9 "Cryptographically signed scenarios at
  day-0 **(gene transfusion from GF-C pattern)**" — scopes signing as a **Phase-3+ transfused** artifact, not
  a Phase-2 storage primitive; the README Principle-5 section names signing nowhere. See §6/§7/OQ-3.)*
- **Scenario-corpus versioning & growth** — the corpus is version-controlled and *grows over time*
  ("No specific scenario suite at the start … the broader scenario library grows over time", README:526);
  factory-built components, the Healer, and the twins each get their own scenarios (README:499). C30 owns
  the corpus as a versioned, append-growing artifact.

**Explicitly NOT (boundaries):**
- **NOT the holdout-integrity ENFORCEMENT or audit (C34).** This is the load-bearing boundary (D-13). C34
  owns the read-isolation *enforcement* (perms + OPA + rig partition) and the *after-the-fact audit*
  ("Holdout integrity audit — Detects if isolation has been violated", README:173; inventory C34
  "enforcement … after-the-fact audit"). C30 stores the corpus so it *is* held-out-able and auditable; it
  writes no enforcement and runs no audit. **C30 does not itself enforce read-isolation** — it relies on
  C42's partition + C34's enforcement (D-13).
- **NOT the rig / partition policy (C42).** C42 *provides* the `scenario_authoring`/`implementer` rigs, the
  `read_partition`/`write_partition` model, and the holdout invariant `scenarios ∉ read_partition(worker)`
  (AI-CONTEXT §13.3; C42 §1). C30 *places its corpus inside* the `scenarios` partition C42 defines; it does
  not define partitions or roles. (Inventory: C30 depends on C42.)
- **NOT the scenario runner (C31).** Executing scenarios against the system — the Inspect AI runner wrapped
  as a pack, plus the session-id adapter (G25) — is **C31** (README:172; inventory C31). C30 owns *authoring
  + storage*; C31 owns *execution*. (Inventory: C31 depends on C30.)
- **NOT the judge harness (C32) or satisfaction metric (C33).** Scoring trajectories against scenarios is
  the LLM-as-judge **C32** (README:185); aggregating scores into a satisfaction distribution is **C33**
  (README:188). C30 supplies the scenarios they consume; it does not score or aggregate. (C32 is a
  model-calling step, *not* a C17 tool node — C17 §2.)
- **NOT a custom scenario DSL.** The authoring DSL is **Inspect AI's** Task DSL, adopted verbatim (README:170;
  AI-CONTEXT:467). v4 lists promptfoo / OpenAI Evals / DeepEval / AgentDojo as *alternatives* (README:175;
  AI-CONTEXT §6.2 L299) — the choice is Inspect AI, not an in-house format. Authoring no DSL of our own.
- **NOT the OPA policy engine.** OPA is named "for finer control **later**" (README:425; AI-CONTEXT §12 L513
  "OPA policy for scenario isolation … needs concrete enforcement design") — it is a *deferred enforcement*
  mechanism owned by C34, not a C30 storage concern.
- **NOT the trajectory store (C21/CXDB).** Scenarios are an authored, held-out *input corpus* in a git repo;
  trajectories (the runs scored against scenarios) are the CXDB content-addressed log (C21). C30 stores
  scenarios, not trajectories. (If scenario *records* are ever CXDB-typed, the bundle root is
  `softwarefactory.v4.*` per D-2 — but the corpus's home is the separate git repo, not CXDB.)
- **NOT secrets/key management.** Cryptographic signing (DEFERRED → FE-3) would *use* a key; *where that key
  lives* is the open secrets gap **G37** (plaintext `city.toml`/env today), owned by C03 — not C30. The
  Phase-0/2 corpus integrity story (content-addressed git history) needs no key, which is exactly why signing
  is deferred until G37 lands (D-14; §7).

## 2. Context & dependencies

| Direction | Component | Relationship |
|---|---|---|
| Upstream (depends on) | **C17** Tool-node abstraction | The Inspect AI scenario-provider pack is wrapped as a **tool node** over C17's abstraction (the `inspect_eval` `[[tool]] type="subprocess"`, AI-CONTEXT §13.3 L599–608; README:177 "expose it as a tool node"). C17 §2 routes C30 explicitly through it. Inventory: C30 `depends on C17`. |
| Upstream (depends on) | **C42** Rig / agent-role partitioning | **C42 PROVIDES** the `scenario_authoring` rig + the `scenarios` partition + the holdout invariant `scenarios ∉ read_partition(worker)` (C42 §1; AI-CONTEXT §13.3). C30 authors/stores *inside* that partition. Inventory: C30 `depends on C42`. **C30 does not enforce; C42 provides, C34 enforces (D-13).** |
| Upstream (DSL — external OSS) | **Inspect AI** (`github.com/UKGovernmentBEIS/inspect_ai`, MIT) | The adopted authoring DSL + Task model (README:170; AI-CONTEXT §15.2 L638). Adopted verbatim as upstream OSS (README:500). The session-id-vs-Gas-City impedance (AI-CONTEXT §12 L512) lands on C31 (runner), not C30. |
| Upstream (secrets — deferred) | **C03** Config / secrets | Custody of a signing key is G37 (plaintext `city.toml`/env today); deferred to C03's SecretResolver. C30's Phase-0/2 corpus integrity uses content-addressed git history (no key); **cryptographic signing is deferred to FE-3, blocked on G37 (D-14)** — C30 neither signs nor stores a key at sweep 1. |
| Downstream (executes) | **C31** Scenario runner | Runs C30's stored scenarios via the Inspect AI runner; needs the session-id adapter (G25). Inventory: C31 `depends on C30`. |
| Downstream (scores) | **C32** Judge harness | Scores work trajectories against C30's scenarios (same provider as coder, D-1). Inventory: C32 `depends on C30`. |
| Downstream (enforces + audits) | **C34** Holdout integrity & isolation enforcement | **Enforces** read-isolation (perms + OPA + rig partition) and **audits** actual reads vs C30's scenario paths (README:173; inventory C34). C30's repo/path layout + signatures are *what C34 audits against*. **Enforcement is C34's, not C30's (D-13).** Inventory: C34 `depends on C30`. |
| Downstream (consumes corpus) | **C35** Override→rule loop, **C53/C55** bootstrap-validation / methodology loop | Override rules become new Inspect AI rubrics (README:216); bootstrap validation needs a scenario set for the factory-built component (G23); methodology experiments run "the same scenarios" (README:31). All read the corpus C30 owns. |

**Position in the system.** C30 is **foundational** (inventory: yes) within the Evaluation & Judge
subsystem and is the **head of the evaluation tier** — C31 (runner), C32 (judge), C33 (satisfaction), C34
(holdout enforcement) all sit downstream of "scenarios exist, authored in isolation." It is delivered in
**Phase 2 / Batch 3** ("Layer 2 (scenarios + judge)", README:417), whose "harder parts are the Inspect AI
wrap and the scenario isolation policy" (README:442). Because D-1 removes the model-family fallback, the
*correctness of C30's placement* (scenarios in the right repo/partition/rig) is load-bearing for the whole
holdout claim — but the *enforcement* of that placement is C34's, and the *partition* is C42's (D-13).

## 3. Interfaces / contracts

Sweep-1: interfaces are **named and described**; concrete Inspect AI `Task` signatures, the repo/path
grammar, the signature format, and the pack manifest defer to sweep 2 (and the *runner* contract to C31,
the *enforcement/audit* contract to C34, the *partition* contract to C42).

| # | Interface | Direction | Description | Owning/detailing component |
|---|---|---|---|---|
| I1 | **Inspect AI Task DSL (authoring format)** | inbound (author) | Scenarios are Inspect AI `Task` objects (Python), authored as-is (README:170; AI-CONTEXT:467). C30 *adopts* the DSL; it does not define it. | Inspect AI (DSL); C30 (adoption) |
| I2 | **Scenario repo + layout** (`scenarios/<component>/`) | storage | The separate git repo and on-disk path layout scenarios live in (README:171/425; AI-CONTEXT §16.4 L698). The unit C31/C32/C34 resolve by path. | C30 (this) |
| I3 | **`[[service]] type="inspect_ai"` provider pack** | inbound (config) | The small Gas City pack that exposes Inspect AI as a scenario provider (README:424). Wrapped as a C17 tool node (`inspect_eval`, AI-CONTEXT §13.3). | C30 (this); C17 (abstraction) |
| I4 | **`scenarios` partition / `scenario_authoring` rig binding** | placement | C30 stores into the `scenarios` partition and authors in the `scenario_authoring` rig (AI-CONTEXT §13.3). C30 *binds to* these; **C42 defines them**, **C34 enforces** the implementer's exclusion (D-13). | **C42** (defines), **C34** (enforces), C30 (binds) |
| I5 | **Corpus integrity = git revision (signing DEFERRED → FE-3)** | storage + verify | Phase-0/2 tamper-evidence/provenance is the **content-addressed git commit identity** of each scenario in the separate repo (AI-CONTEXT:236/404); C34/baselining (F7) verify the corpus against its git revision. **Cryptographic per-scenario signing is DEFERRED to FE-3 (blocked on G37/D-14)** — not a sweep-1 interface. | C30 (git revision); C34 (verify); *FE-3/C03 (signing+key, deferred)* |
| I6 | **Scenario-path feed (to enforcement/audit)** | outbound (read) | The set of scenario paths/labels C34's audit compares actual implementer reads against ("agent reads vs scenario paths", README:173). C30 *publishes the corpus layout*; C34 *audits against it*. | C30 (publishes); **C34** (audits) |
| I7 | **Corpus retrieval (to runner/judge)** | outbound (read) | The runner (C31) and judge (C32) resolve a component's scenarios by path/`Task` from the corpus. C30 owns *the corpus*; C31 owns *execution*. | C30 (corpus); C31/C32 (consume) |

**Invariants C30 must uphold (store-level):**
- **INV-1 (separate-repo holdout):** scenarios live in a **separate git repo** from the code the implementer
  works in (README:171/425). The corpus is never co-located in the implementer's `code` partition.
- **INV-2 (authoring-rig confinement):** scenarios are authored **only** by the `scenario_authoring` rig
  (`*_partition = "scenarios"`), never by the implementer rig (AI-CONTEXT §13.3). C30 writes only via the
  scenario rig.
- **INV-3 (partition placement):** every stored scenario is in the **`scenarios` partition** C42 defines, so
  the holdout invariant `scenarios ∉ read_partition(worker)` (C42) and C34's audit have a well-defined
  target. C30 places; it does not enforce (D-13).
- **INV-4 (git-revision integrity):** every scenario has an immutable, content-addressed **git commit
  identity** in the separate repo, so a tampered/edited scenario is detectable as a history change and is
  attributable to the committing rig (AI-CONTEXT:236/404; INV-1/INV-6). *(Cryptographic per-scenario signing
  is DEFERRED → FE-3, blocked on G37/D-14; it is **not** an INV-4 obligation at sweep 1. The git-revision
  identity is the Phase-0/2 mechanism F7 baselining verifies against.)*
- **INV-5 (DSL-faithful):** scenarios validate against the **pinned** Inspect AI `Task` schema; C30
  introduces no bespoke scenario format (README:170). *(Task validity is an **adopted-upstream property**
  verified by the conformance pack / version pin, G11 — not a format C30 itself defines; the corpus is
  Inspect-AI-native.)*
- **INV-6 (versioned, append-growing):** the corpus is version-controlled and grows additively over time
  (README:526); scenario history is preserved (git), not overwritten.

> **C30 explicitly does NOT carry an enforcement invariant.** "The implementer cannot read scenarios" is an
> invariant of **C42 (partition) + C34 (enforcement/audit)**, not C30 (D-13). C30's invariants are about
> *correct placement and provenance of the corpus*, which is what makes that enforcement possible.

## 4. Data model / state

C30 *owns the scenario corpus + its layout + signatures*; the *partition policy* over it is C42's, the
*enforcement/audit* is C34's. State C30 is the spec-of-record for at sweep 1:

| State | Description | Persistence | Detailed by |
|---|---|---|---|
| **Scenario repo** | The separate git repo holding all scenarios (README:171/425). | Git repository (separate from code). | C30 |
| **`scenarios/<component>/` layout** | Per-component scenario directories (AI-CONTEXT §16.4 L698); the path the runner/judge/audit resolve. | Files in the scenario repo. | C30 |
| **Inspect AI `Task` scenarios** | The scenario bodies, authored in the Inspect AI Task DSL (README:170). | Python files under the layout. | Inspect AI (format); C30 (corpus) |
| **Git-revision integrity** | Content-addressed commit identity per scenario = Phase-0/2 tamper-evidence/provenance (AI-CONTEXT:236/404). *(Cryptographic signing DEFERRED → FE-3/G37, D-14.)* | Git commit history of the separate repo. | C30 (git); *FE-3/C03 (signing+key, deferred)* |
| **`[[service]] type="inspect_ai"` pack** | The Gas City pack exposing Inspect AI as a provider + the `inspect_eval` tool node (README:424; AI-CONTEXT §13.3). | Version-controlled pack (TOML + glue). | C30 (this); C02/C17 (ABI/abstraction) |
| **`[[rig]] scenario_authoring` binding** | *Reference only* — the rig C30 authors in. The block itself is **C42-owned** (`city.toml`, AI-CONTEXT §13.3). | C42 config. | **C42** (owns); C30 (binds) |

**The scenario unit (faithful from README:170, AI-CONTEXT §13.3).** A *scenario* is an **Inspect AI `Task`**
stored at `scenarios/<component>/…` in the separate repo, authored by the `scenario_authoring` rig, and
signed at day-0. A *scenario suite* is the set of scenarios for a component (or the Healer/twins — README:499).

> [FAITHFUL-FILL] v4 names the *format* (Inspect AI Task DSL, README:170) and the *location* (separate repo +
> `scenarios/<component>/`, README:171/425, AI-CONTEXT §16.4) but not the concrete on-disk scenario record
> (e.g. scenario id, component binding, corpus manifest). The minimal faithful elaboration is: **a stored
> scenario = {an Inspect AI `Task` file under `scenarios/<component>/`} committed to the separate repo**,
> whose **provenance + tamper-evidence are the git commit identity** (immutable, content-addressed,
> attributable to the committing `scenario_authoring` rig — AI-CONTEXT:236/404), so no separate signature or
> `created_by` field is required at Phase-0 (the git commit *author* already records the rig; P9 attribution
> is satisfied natively, README:226–231 — an *inference*, not a v4 mandate that scenario files carry
> `created_by`). The exact `Task` record shape and whether an explicit `created_by` field is added are
> sweep-2 (OQ-1); the *runner-facing* execution contract is C31's. *(Cryptographic signing is DEFERRED →
> FE-3/G37, D-14 — see §1 bullet 4.)*

> [FAITHFUL-FILL] **Scenarios are stored in the git repo, not in CXDB.** v4 locates scenarios in a "separate
> git repo" (README:171/425) and CXDB stores *trajectories* (C21), not scenario inputs. The minimal faithful
> reading is that the corpus's authoritative home is the git repo; if any scenario *metadata* is ever
> mirrored into a typed store, the bundle root is `softwarefactory.v4.*` (D-2). No CXDB dependency is added
> for C30 at sweep 1.

**Consistency / lifecycle.** The corpus is **version-controlled and append-growing** (README:526): scenarios
are authored in the `scenario_authoring` rig, signed, and committed to the separate repo; the corpus is read
(never written) by the runner/judge/audit. The store is added in **Phase 2** (additive to the Phase-0/1
substrate; README:417). Because scenarios "grow over time" (README:526) and "factory-built components have
their own scenarios" (README:499), the corpus has no fixed size — only the *layout* and *signing* are fixed.

## 5. Behavior

**Stand up (Phase 2).** Operator installs Inspect AI (MIT), builds the small Gas City pack exposing it as a
scenario provider (the `[[service]] type="inspect_ai"` block + the `inspect_eval` tool node), and sets up
the **separate scenario git repo** with filesystem permissions read-only-from-implementer (README:423–425).
C42's `scenario_authoring`/`implementer` `[[rig]]` blocks are in place (the partition C30 binds to). Result:
a held-out scenario corpus standing alongside the runner/judge tier, ready for P5/P6 (README:438–440).

**Author a scenario.**
1. The **`scenario_authoring` rig** (never the implementer) writes an Inspect AI `Task` under
   `scenarios/<component>/…` (AI-CONTEXT §13.3, §16.4).
2. C30 **signs** the scenario at authoring time (day-0 signature; F9) and records `created_by` (the
   scenario-author rig).
3. The scenario is committed to the **separate repo** (INV-1/INV-6). It is now resolvable by path by the
   runner/judge/audit.

**Hold out from the implementer (relied-upon, not owned).** The implementer rig's `read_partition` excludes
`scenarios` (C42 invariant); the implementer cannot read the corpus. **C30 does not enforce this** — it
relies on C42's partition + C34's enforcement/audit (D-13). C30's only obligation is that the corpus *is in*
the `scenarios` partition / separate repo so that exclusion is well-defined (INV-3).

**Serve to runner/judge/audit.** C31 resolves a component's scenarios by path and executes them; C32 scores
trajectories against them; **C34** compares actual implementer reads against the scenario paths to *detect*
a holdout violation after the fact, and may *verify the day-0 signatures* during baselining (F7). C30
*publishes the corpus + signatures*; it does not run the runner, the judge, or the audit.

> Sequence/state diagrams (Mermaid), the exact `Task`/repo/signature wire contracts, and the pack manifest
> are **sweep-2+**. The *execution* contract is owned by **C31**; the *enforcement/audit* contract by **C34**;
> the *partition* contract by **C42**.

## 6. Failure modes & handling

C30 carries the holdout/isolation gaps assigned to it (G10, G21, G28) **at the storage/authoring altitude**,
routing the *enforcement* obligations to C34 per D-13.

**G10 (minor) — "held-out" implies a guarantee the mechanism doesn't provide.** "P5 says the agent 'cannot
see' scenarios, but the enforcement is file permissions + agent-prompt discipline + audit logging;
'discipline' is not enforcement" (G10). For C30 the faithful resolution is to **state the boundary
honestly**: C30 *stores* the corpus so it *can* be held out (separate repo + `scenarios` partition placement,
INV-1/INV-3), but "held-out" is a **policy intent realized by C42's partition and verified after the fact by
C34's audit**, not a hard guarantee C30 provides. C30 adds the **day-0 signature** (F9) so a scenario that
*was* leaked-and-edited is at least tamper-evident. C30 thus *addresses* G10 for the storage layer (correct,
auditable placement + provenance) and **defers the enforcement-strength question to C42/C34** (D-13).

**G21 (major) — holdout-integrity enforcement has no real mechanism.** "The implementer agent runs as a
Claude Code subprocess with broad tool access (Bash, Read); nothing prevents it reading outside its declared
partition. The audit is detection after the fact, not prevention" (G21). **This is not C30's to solve
(D-13).** C30's faithful posture: store the corpus *only* in the `scenarios` partition / separate repo
(INV-1/INV-3) so the read-escape has a well-defined boundary, and route **enforcement + after-the-fact audit
to C34** and the **broad-tool-access blast-radius bound to C43** (D-13; C42 §6). C30 records that, against a
broad-tool-access implementer, its stored corpus is protected by **config + filesystem perms + C42 partition
+ C34 detect-after-the-fact audit**, *not* by anything C30 itself enforces. *(RESOLVED-ownership by D-13:
C34 enforces+audits, C42 provides the partition, C30 stores/authors. C30 does not over-claim prevention.)*

**G28 (major) — three/four mechanisms named for one boundary, no authority statement.** "Separate git repo +
filesystem permissions + rig `read_partition` + OPA-later — no statement of which is authoritative or how
they compose" (G28). For C30 the faithful resolution is to **own the two storage-side mechanisms and name
their relation, deferring the policy authority to C42**: C30 owns **(a) the separate git repo** (the corpus
home) and **(b) the on-disk layout** that filesystem permissions are applied to; the **authoritative
*partition* declaration** (rig `read_partition` excludes `scenarios`) is **C42's** (C42 §4.3 names it the
authoritative declarative unit), and **OPA is deferred to C34** ("for finer control later", README:425).
C30's one-line authority note: *the corpus lives in a separate repo (C30) realized on disk with read-only
perms; the authoritative access policy over it is C42's rig `read_partition`; enforcement+audit is C34's;
OPA is deferred.* This is the storage-side half of the G28 resolution C42 §4.3 owns for the policy side.

**F-modes (storage/authoring slice; canonical mapping owned by C57).**

| F-mode | Relevance | Handling in C30 (faithful) |
|---|---|---|
| **F28** Holdout leakage (F-MODE §1, "Addressed") | The core mode: the implementer reading the scenarios it is judged on. | C30's contribution is **correct held-out placement** (separate repo + `scenarios` partition, INV-1/INV-3) so the boundary is well-defined + auditable; **enforcement + audit is C34, partition is C42 (D-13)**. *Caveat (G21):* against a broad-tool-access implementer the realized boundary is config + perms + partition + detect-after-the-fact audit, not tool-call-time prevention until C43. C30 surfaces this rather than absorbing the "Addressed" silently. |
| **F9** Spec overfitting ("signed scenarios at day-0") | The implementer overfitting to scenarios it shouldn't have seen, or scenarios silently edited. | **Addressed (storage-side):** day-0 signing (I5/INV-4) makes a scenario tamper-evident; periodic baselining (F7) verifies signatures. C30 *signs*; C34/baselining *verify*; the key is G37/C03. |
| **F1** Hallucination loop ("held-out scenarios") | Held-out scenarios are part of the guard. | C30 provides the held-out corpus; the judge (C32) closes the loop. |
| **F55** Behavioural drift (F-MODE §6, "Partial") | "drift in synthetic scenarios still possible" — held-out human-authored corpus is the external grounding. | C30 keeps the corpus **human-authored + version-controlled** (README:526); residual synthetic-drift risk is acknowledged, not closed (Partial, per F-MODE). |

**Degraded behaviour.** Scenario repo unavailable ⇒ the runner/judge cannot fetch scenarios (an evaluation
outage, not a factory-run crash — evaluation is downstream of the build). Corrupt/edited scenario ⇒
detectable via day-0 signature mismatch (INV-4). C30 holds no in-store HA design; the corpus is a git repo
with git's own durability/replication story.

> F-mode applicability is owned by C57 (coverage map); C30 surfaces the storage-level classes (holdout
> leakage F28, spec-overfitting F9, scenario tamper) and defers the canonical mapping there.

## 7. Cross-cutting (security / cost / scale / observability / ops)

- **Security (the central concern).** C30 is the **storage substrate** of the holdout boundary, but **not its
  enforcer** (D-13). Per D-1 there is no model-family fallback, so the *placement* C30 owns (separate repo +
  `scenarios` partition, INV-1/INV-3) is load-bearing input to the holdout guarantee — but the **enforcement +
  audit is C34's** and the **partition is C42's**. The **day-0 signature** (F9) is C30's genuine security
  contribution: tamper-evidence/provenance for the corpus. *Key custody is G37* — the signing key lives in
  plaintext `city.toml`/env today, deferred to C03's SecretResolver; until then the signature's assurance is
  capped by G37 (flagged, not absorbed). The `created_by` on each scenario preserves the P9 attribution chain
  (C41).
- **Cost.** No cost model in v4 for the corpus itself (G32); storage is a git repo (no managed-DB fees).
  Inspect AI is MIT (free to adopt). The *scenario-run* token spend (running suites at L5 volume on one Max
  seat — G13/G34) belongs to C31/C32/C29, not the store.
- **Scale.** The corpus "grows over time" (README:526) with no fixed bound; scale is git-repo scale (many
  small Python files). No multi-node store; the per-component layout keeps retrieval path-scoped.
- **Observability.** C30's repo + path layout + signatures are exactly **what makes the holdout-integrity
  audit (C34) possible** — C34 compares actual implementer reads against C30's scenario paths (README:173)
  and verifies signatures during baselining (F7). C30's published corpus *is* the observability surface for
  holdout violations.
- **Ops.** Install = Inspect AI (MIT) + the small `[[service]] type="inspect_ai"` pack + the separate
  scenario repo with read-only-from-implementer perms (README:423–425). "The harder parts are the Inspect AI
  wrap and the scenario isolation policy" (README:442) — the *wrap* is C30's, the *isolation policy* is
  C42's/C34's. The **Inspect-AI session-id ↔ Gas City session-id adapter** (AI-CONTEXT §12 L512) is a
  *runner* (C31) concern, not C30's storage concern. *Spelling caveat (XC-9):* C30 binds to the `[[rig]]`
  form (AI-CONTEXT §13.3); canonical `[rigs]`/`[[rig]]` spelling is C07/integrator's call.

## 8. Acceptance criteria & test strategy

Sweep-1 = high-level criteria (concrete tests at sweep 2).

1. **AC-1 (DSL adopted — I1/INV-5):** scenarios are authored as **Inspect AI `Task`** artifacts; no bespoke
   scenario format is introduced (README:170; AI-CONTEXT:467). *Proves the off-the-shelf DSL is the format.*
2. **AC-2 (separate-repo holdout — INV-1):** the scenario corpus lives in a **separate git repo** from the
   implementer's code partition; it is never co-located in `code` (README:171/425).
3. **AC-3 (authoring-rig confinement — INV-2):** scenarios are authored **only** by the `scenario_authoring`
   rig; an attempt to author from the implementer rig is invalid (AI-CONTEXT §13.3). *Placement is correct;
   enforcement of the implementer's read-exclusion is C34's (D-13).*
4. **AC-4 (partition placement — INV-3):** every stored scenario resolves under the **`scenarios` partition**
   C42 defines, so the holdout invariant `scenarios ∉ read_partition(worker)` and C34's audit have a
   well-defined target (AI-CONTEXT §13.3; C42 §3).
5. **AC-5 (day-0 signing — INV-4/F9):** every scenario is **signed at authoring time**; a tampered/edited
   scenario yields a signature mismatch detectable by baselining (F9; F7). *Key custody is G37 (C03) — the AC
   asserts C30 signs on store, not that the key is secured.*
6. **AC-6 (layout resolvable by path — I2/I7):** a component's scenarios are resolvable at
   `scenarios/<component>/…` by the runner (C31), the judge (C32), and the audit (C34) (AI-CONTEXT §16.4).
7. **AC-7 (scenario-path feed to enforcement/audit — I6, addresses G10/G21/G28):** C30 **publishes** the
   scenario corpus layout/paths so **C34** can enforce+audit actual implementer reads against them
   (README:173). *C30 publishes; C34 enforces+audits — C30 runs no enforcement (D-13).*
8. **AC-8 (versioned, append-growing — INV-6):** the corpus is version-controlled and grows additively;
   scenario history is preserved (git), not overwritten (README:526).

**Test strategy.** A **scenario-store conformance pack** that: authors a sample Inspect AI `Task` from the
`scenario_authoring` rig, signs it, commits it to the separate repo at `scenarios/<component>/`, and asserts
AC-1…AC-8 — in particular the separate-repo holdout (AC-2), the `scenarios`-partition placement (AC-4), the
day-0 signature round-trip (AC-5), and the scenario-path feed C34 audits against (AC-7). The suite proves
*correct held-out placement + provenance*; it does **not** test enforcement (C34) or execution (C31). It is
the storage-side de-risking gate before C31/C32/C34 build on C30.

## 9. Open questions

- **OQ-1 (→ review-log, top):** **Scenario record + signing format.** Exactly which fields are C30's stored
  scenario record (the §4 [FAITHFUL-FILL]: `Task` file + day-0 signature + `created_by`), where the signature
  lives (sidecar vs embedded vs commit-signature), and what the corpus manifest is. Freeze at sweep 2 before
  C31/C32/C34 build against the corpus. *(Interacts with G37: the signing key's custody is C03's.)*
- **OQ-2 (→ review-log):** **D-13 storage/enforcement seam.** Confirm the split: C30 *stores/authors* in the
  isolated rig, C42 *provides* the partition, C34 *enforces + audits*. In particular, confirm C30 publishes
  exactly the scenario-path/label feed (I6) that C34's audit needs, and that no enforcement obligation leaks
  back onto C30. *(Pre-constrains unbuilt C34, Batch 3.)*
- **OQ-3 (→ review-log):** **G37 — signing-key custody.** The day-0 signature (F9) needs a key; v4 has no
  secrets story (plaintext `city.toml`/env). Until C03's SecretResolver lands, the signature's tamper-evidence
  assurance is capped. Confirm signing stays C30's *act* while key custody is C03's. *(G37 ≠ FE-3 per D-14.)*
- **OQ-4 (→ review-log):** **CXDB vs git for scenario metadata.** Sweep-1 keeps the corpus's authoritative
  home in the separate git repo (§4 [FAITHFUL-FILL]). Confirm whether any scenario *metadata* (e.g. for the
  satisfaction aggregator C33 or methodology loop C55) is ever mirrored into a typed store — and if so, that
  it uses the `softwarefactory.v4.*` bundle root (D-2), without making the git repo non-authoritative.
