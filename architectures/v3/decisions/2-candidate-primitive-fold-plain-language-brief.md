# Decision needed: should four shared building blocks be written up once, or once per candidate?

**Audience.** You (the project owner). You know what the project is doing — building a set of AI-agent factory architectures and comparing them — but you're (rightly) frustrated with jargon when I try to explain *how* we're doing it. This brief is written in plain language. No jargon goes by undefined.

**Status.** Open question. Lead-agent recommendation at the end; your call.

---

## What this decision is about, in one paragraph

We have ten architecture proposals (we call them "candidates"). Each candidate is built from a kit of platform building blocks (we call them "primitives" — things like "the sandbox the agent runs in", "the place we store test scenarios", "the cost-cap enforcer"). Some primitives appear in many candidates' kits, some appear in only one. For each primitive that lands in someone's kit, we write a short design-decision document — an ADR — explaining how the primitive is built. **The question is: when a primitive appears in only two candidates' kits, do we write one ADR or two?** Right now we wrote one ADR for each of four such two-candidate primitives. You're being asked to confirm or reject that choice.

---

## A glossary, so the rest of this brief reads cleanly

| Word I keep using | What I mean by it |
|---|---|
| **Candidate** | A proposed methodology for the AI software factory. We have ten of them. Names: `GF-S`, `GF-M`, `GF-C` (three "greenfield" candidates — design from scratch); `BF-S`, `BF-M`, `BF-L` (three "brownfield" — work with legacy code); `U-A`, `U-B`, `U-C`, `D7-U-1` (four "unified-attempt" — try to do both). |
| **Primitive** | A platform building block a candidate's design needs. Numbered P-01 through P-34. Each has a one-line job description. For example: P-01 = "the sandbox the agent runs in"; P-08 = "where test scenarios are stored"; P-14 = "the router that picks which LLM to use as the judge for a given task". |
| **ADR** | Architecture Decision Record. A short markdown file (≤1000 words, fixed sections) explaining the decision we made for one design question, with alternatives and consequences. Lives at `docs/adr/NNNN-some-title.md`. We have 36 so far (0001-0036), with ~30 more coming. |
| **Common ADR** | One ADR for a primitive that multiple candidates share, written in a way that names the shared parts and lets each candidate cite it. |
| **Per-candidate ADR** | A separate ADR for each candidate that uses a primitive, explaining how *that* candidate specifically uses it. Used when the candidates use the primitive in incompatibly different ways. |
| **"Fold"** | What I should have said: "we wrote ONE common ADR instead of two per-candidate ADRs." When I said "fold P-25 into Wave 5.1b as a common ADR", I meant: "we decided to write the P-25 ADR once and have both candidates that use it cite the same ADR, rather than writing a separate P-25 ADR for each of the two candidates." The word "fold" was unhelpful jargon. |

With those definitions in hand, here's the concrete situation.

---

## The specific four primitives in question

Each of these is used by exactly two candidates. The question is: for each, did we make the right call by writing a single common ADR rather than two per-candidate ADRs?

### P-25 — CaMeL perimeter

**What it is in plain language.** A "perimeter" is the boundary between untrusted external input (what users or external systems hand to the agent) and the trusted execution environment (where the agent actually runs code). The perimeter is the place where we check inputs to make sure nothing malicious or malformed gets past. "CaMeL" is a specific style of perimeter (Constraint-Authority + Member-Logic) that uses strict typed contracts at the boundary.

**Who uses it.** Two candidates: `BF-S` (the brownfield-substrate-first methodology) and `BF-M` (the brownfield-methodology-first methodology).

**Why we wrote one ADR.** Both candidates need the same perimeter — same Python `pydantic` typed envelopes, same Rust syscall wrapper, same OPA-Rego rules inside. There's no place where BF-S and BF-M's perimeters differ structurally; they just use the same one with the same configuration.

**The ADR.** [`docs/adr/0033-p-25-camel-perimeter.md`](docs/adr/0033-p-25-camel-perimeter.md).

**Risk of having written one ADR (your concern, if any):** if you later decide BF-S and BF-M *should* have different perimeters, both candidates' architecture specs in Phase 6 will inherit the same ADR and you'd have to retrofit the difference. Lead-agent view: I don't see a reason BF-S and BF-M would diverge on this; they're both brownfield, and the perimeter's job is the same in both.

### P-27 — archaeological-brief tooling

**What it is in plain language.** When the agent works on legacy code, it needs to know the *history* of the code region it's touching — when was it introduced, who wrote it, what was the original intent, what's changed since, who depends on it. The "archaeological brief" is a structured report of all that, produced on demand by an LLM-judge synthesis loop over `git blame` + the code-fact-store. "Archaeological" is the metaphor — the agent is digging through historical layers of the codebase.

**Who uses it.** Two candidates: `BF-M` and `BF-L` (brownfield-methodology-first and brownfield-legacy-ingestion-first).

**Why we wrote one ADR.** Both candidates produce the same shape of archaeological brief (same three sections: introduction-cycle, intent-decay-log, contemporary-references). BF-M uses it per-cycle when starting work on a code region; BF-L uses it at ingestion time when first bringing legacy code into the factory. The brief's *content* is the same; just the *trigger* differs.

**The ADR.** [`docs/adr/0034-p-27-archaeological-brief-tooling.md`](docs/adr/0034-p-27-archaeological-brief-tooling.md).

**Risk.** If you decide BF-M and BF-L should produce *different* brief shapes (say, BF-L wants extra ingestion-context fields), the common ADR doesn't capture that. Lead-agent view: the per-cycle vs ingestion-time distinction is a methodology layer concern, not a substrate-building-block concern. The tool is the same; the methodology decides when to call it.

### P-24 — attribution store

**What it is in plain language.** When the factory produces code or specs, we need a durable record of *who/what* produced each artifact — which agent, which model version, which methodology cycle. That record is what lets us debug failures ("this regression came from cycle 47, agent-3, model-snapshot X") and audit compliance ("who introduced this code?"). The attribution store is the typed-object store that holds those records, indexed by the artifact's content-hash.

**Who uses it.** Two candidates: `BF-S` directly, and `BF-L` indirectly (via its P-26 Codebase Model, which composes attribution into its larger code-knowledge graph).

**Why we wrote one ADR.** Both candidates need the same underlying attribution store. BF-S queries it directly; BF-L treats it as one input to P-26. The store's contract is identical.

**The ADR.** [`docs/adr/0035-p-24-attribution-store.md`](docs/adr/0035-p-24-attribution-store.md).

**Risk.** If you decide BF-L's P-26 needs an *enriched* attribution store (extra fields for region-graph context), the common ADR is silent on that enrichment. Lead-agent view: enrichments belong in the P-26 ADR (Wave 5.3 next, deferred), not in P-24's ADR. P-24 stays a clean store.

### P-30 — event registrar (substrate only)

**What it is in plain language.** Two candidates need a workflow engine that handles event-driven state machines: U-A uses it for "re-entry-interval" workflows (when an interval is paused, what happens when it wakes up?); D7-U-1 uses it for "survival-window" workflows (when a falsification commitment is made, how long does it stay open before it expires?). Both use the same underlying engine (Temporal, an open-source workflow engine with signal/timer/query primitives).

**Why we wrote ONE ADR for the substrate, but the two state machines are NOT folded.** This is the asymmetric case — and it's important. The *engine* is shared (one ADR: "we use Temporal for event-driven workflows"). The *state machines* are genuinely different (U-A re-entry is event-driven with operator acknowledgement; D7-U-1 survival-window is timer-driven with cascading wake-up of dependent workflows). The two state-machine ADRs are NOT in this ADR — they're deferred to the next run's Wave 5.3, where each candidate will get its own per-candidate state-machine ADR.

**The ADR (substrate part).** [`docs/adr/0036-p-30-event-registrar-substrate.md`](docs/adr/0036-p-30-event-registrar-substrate.md).

**What the ADR explicitly carries.** A "scope-boundary" paragraph in its Consequences section saying: "this ADR covers the Temporal substrate ONLY; the per-candidate state machines are separate ADRs in Wave 5.3 next run; Phase-6 architecture specs MUST reference BOTH this ADR AND the candidate's state-machine ADR." This is the only ADR among the four where we deliberately preserved a downstream split.

**Risk.** This is the case where the risk is highest, because the engine is shared but the semantics aren't. If a Phase-6 architecture-spec author reads only the substrate ADR and doesn't realize they also need the candidate-specific state-machine ADR, they'll under-specify their architecture. That's why we built the scope-boundary text into the ADR — but it's a discipline, not a guarantee.

---

## What you're being asked to confirm

For each of the four primitives above, you have three options:

**Option A — Keep all four folds (lead-agent recommendation).** All four ADRs as written. Phase 6 architecture specs inherit the common ADRs.

**Option B — Keep three, unfold one (the riskiest case is P-30).** Keep P-25, P-27, P-24 as common ADRs. Split P-30 substrate into separate "P-30 (U-A)" and "P-30 (D7-U-1)" ADRs that include both the substrate choice AND the state machine in one file per candidate. This would eliminate the scope-boundary risk on P-30 at the cost of duplicating the Temporal-engine decision in two ADRs.

**Option C — Unfold all four.** Write 8 ADRs total (2 candidates × 4 primitives) instead of the current 4. Each candidate has its own ADR for each shared primitive. Most conservative; highest ADR count.

**My recommendation: Option A.** Here's why:

1. **P-25, P-27, P-24 are unambiguously shared.** The detailed primitive analysis in [`architectures/v3/primitives/overlap.md`](architectures/v3/primitives/overlap.md) (the file where I worked out which primitives are the same across candidates and which differ) showed no contested variation for these three. Writing two ADRs for each would say the same thing twice.
2. **P-30 is the genuinely-asymmetric case** but the substrate ADR carries an explicit scope-boundary paragraph that says "this is the engine ONLY — see the per-candidate state-machine ADR for semantics." A Phase-6 architecture-spec author who reads the ADR cannot miss this; it's in the Consequences section verbatim.
3. **Cost of the fold being wrong is low and reversible.** If a Phase-6 spec author finds they need a separate ADR, we add a new ADR at that time. The common ADR doesn't block that.
4. **Cost of un-folding is non-trivial.** Each split would add 1 more ADR (Option B) or 4 more ADRs (Option C). That's authoring time, review time, and link-maintenance overhead. For ADRs that would say the same thing as the existing ones.

---

## What changes if you pick differently

- **You pick Option A (recommended):** nothing changes. PR #167 stays as is; the four ADRs are accepted as written.
- **You pick Option B:** I revert the part of PR #167 that authored `docs/adr/0036-p-30-event-registrar-substrate.md`, and author two new ADRs in its place (one for U-A, one for D7-U-1) each covering the Temporal substrate + the state machine. Estimated effort: one stacked PR, ~2 hours including adversarial review of the split.
- **You pick Option C:** I revert four ADRs from PR #167 and author eight new ones. Estimated effort: 2-3 stacked PRs.

Any choice is fully reversible at this stage — none of the Phase-6 architecture specs have been written yet, so no downstream artifact has yet read these ADRs. Once Phase 6 starts, splitting becomes more expensive (because Phase-6 specs would need to be edited too).

---

## Where the underlying analysis lives, if you want to dig in

- **The primitive overlap analysis** (worked out which primitives are the same across candidates and which differ): [`architectures/v3/primitives/overlap.md`](architectures/v3/primitives/overlap.md), especially the section "§2 Primitive overlap counts (by candidate-coverage)" which lists every primitive's claiming candidates.
- **The Wave 5.1 dispatch decision** (where I argued for the fold in the first place — Round-1 cost-hawk objection #3 and Round-2 decision): [`architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md`](architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md).
- **The four ADRs themselves** are linked inline above.

If you tell me your decision (A / B / C), I'll execute it immediately rather than queue it.
