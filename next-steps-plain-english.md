# What to do next: a board of things to try

**Who this is for.** You — steering this for fun and to learn. You don't write the code; you decide
what to play with next and how much to trust what the factory builds.

**Read the [charter](factory-discovery-charter.md) first** for the *feel* of the whole thing (why we're
doing this, the co-implementation idea, the vocabulary). This report is the practical "so what do I
actually do?" companion; the [methodology companion](methodology-and-formulas-plain-english.md) is the
"how the building works" companion (the Gas City *formulas*).

**The big picture in two sentences.** The factory is a **prototype** we build *alongside* a portfolio
of real projects (agent-os is the first of several) — each real thing we build also stress-tests the
factory and teaches us what to improve. So this isn't a march to a finished factory; it's a **board of
things you can try**, picked by mood, where the only fixed part is a short on-ramp to earn trust in the
factory's *measuring instruments* before you believe anything they tell you.

---

## Part 1 — The one ordered bit: a short on-ramp to trust your instruments

Everything after this is free choice. But three moves genuinely come first, because **until you trust
the factory's instruments, you can't trust the result of *any* card you play.** (These carry the
hard-won fixes from a six-expert review — the [verdict ledger](architectures/v4/_meta/next-steps/panel/VERDICT.md)
has the depth.)

1. **Is the engine real?** Confirm the off-the-shelf engine does what we assumed — in particular,
   whether it *physically refuses* a forbidden action or only *logs it afterward*. If it only logs
   ("detect-only"), the factory stays fully human-supervised until that's fixed. *(A day or two; turns
   the riskiest assumption into a fact — including a quick check that one AI "seat" means the work runs
   one-at-a-time, so don't plan around parallel speed you don't have.)*
2. **Can you trust the judge?** The factory's AI inspector is the most important and most fragile part.
   Before its verdicts drive anything, measure how often it's wrong — especially false "all good"
   calls — on a small set of known-answer builds (two people labelling, so you're not grading a
   fallible judge with a single fallible opinion). Aim for a *different* AI family than the coder where
   you can; the early design relaxes that, so if it's the same family for now, trust it less. Until the
   judge clears a bar, **every build gets full human review.**
3. **Lock the test vault.** The held-out tests only mean something if the coder can't read them *or*
   quietly weaken them, and if someone *other* than the coder wrote them.

That's the whole ordered part. It's short on purpose. Once your instruments are trustworthy, you play
the board.

---

## Part 2 — The board: a menu of things to try

Here's the shift from the old plan: after the on-ramp, **there's no rigid sequence.** There's a
**board of cards** — candidate next things — and you pick whichever you're in the mood for. Each card
honestly says what it stresses, how big it is, how fun, what you'll learn, what it leaves behind, and
what has to be true first. You can **drop in your own** project any time. A soft nudge points at
"lonely" parts of the factory (low trust, not visited lately) — as a *suggestion, never a chore*.

**Trust rises gradually** (it's never "proven"): 🌑 untouched → 🌒 smoke-OK → 🌓 poked → 🌔 worked →
🌕 trusted. Set it by feel; let the playing nudge it.

### A starter board (examples — not an order; pick by mood)

| Card | Flavor · what it pressures | Size · vibe | What you'd learn | What it leaves behind | Needs first |
|---|---|---|---|---|---|
| **"Hello, formula"** | *Smoke-toy* · the pipeline engine + runner + work-ledger | tiny · a quick win | does a 3-step recipe even run end-to-end? | throwaway (a warm engine) | on-ramp #1 |
| **"Tiny event registry"** | *Reduced model of agent-os B12* · spec-intake + the judge on simple data | half-day · clean & satisfying | can the judge tell a *spec* bug from a *code* bug on simple schemas? | scaffold toward real B12 | on-ramp |
| **"Two-rule policy bundle"** | *Reduced model of B3* · the deterministic (no-AI) tool path + judge on policy | half-day | does "deterministic-first" actually pay off? | scaffold toward B3/B16 | on-ramp |
| **"Make formulas visible"** | *Self-build (dogfood)* · the factory-builds-its-own-parts loop, low-risk | a session · genuinely useful to you | can the factory build a small piece of *itself*? | a real factory part (a workflow viewer) | on-ramp; an exemplar to copy |
| **"Glossary"** | *Self-build (dogfood)* · the simplest possible self-build | tiny | the gentlest first dogfood run | a real factory part | on-ramp |
| **"B12 for real (core)"** | *Real driver (agent-os)* · the whole loop, on real work | meaty · the "does this really work?" moment | does factory-builds-product hold up? | a real agent-os component | on-ramp; spec-completion pass; a named, openly-licensed example to copy |
| **"Race two recipes"** | *Experiment* · the methodology-comparison machinery + judge consistency | a session · nerdy-fun | does an extra review step actually raise quality? | a methodology finding (which recipe wins) | a reduced model to race on |
| **"_(your idea here)_"** | *Invented project* · whatever's lonely + sounds fun | your call | depends — and that's the point | maybe throwaway, maybe a gem | tag it so it still counts |

The point of the table isn't the specific cards — it's the *shape*: on a low-energy night you grab a
🌒 smoke-toy; on a "let's go" night you take **B12 for real**; when the policy tooling feels untested
you play the **two-rule bundle**; when you just want to enjoy yourself you **make something up** that
happens to lean on a part you haven't trusted yet.

**Invented projects are first-class.** If a part of the factory needs pressure but nothing on the board
naturally hits it, make up a fun little thing that does — a silly CLI, a toy generator, whatever sounds
good. Pressure-testing and having fun are the same move.

---

## Part 3 — How you find defects, and the two lists you keep

When a build goes wrong, the method is the **triangle**: a build is only "done" when the **spec**, the
**tests**, and the **system** (the built code) all agree, and the AI judge's job is to say *which corner
is at fault* — or that the judge itself misread it. That turns "it's buggy" into a precise,
fixable to-do. (Formal version: [the triangle decision record](docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md).)

You keep exactly **two lists**, and both are *byproducts* of playing — never separate admin:
- **Defect ledger** — each failed build, tagged by triangle corner. Keeps product quality honest.
- **Factory-gap ledger** — each time real work hits a factory limitation (a missing part, an awkward
  recipe, a judge weakness, a substrate surprise, work it can't build yet). **This list — not a roadmap
  guessed in advance — is what tells you which factory part to build next.** When it keeps saying the
  same thing ("can't build cluster stuff without practice twins"), that's your next big factory project.

---

## Part 4 — The decisions that are genuinely yours

1. **How trusting to be, by feel.** There's no formula for "is the factory good enough." Set trust by
   gut, let evidence nudge it, tighten the judge's bar as it earns it. Winging it is allowed and
   expected.
2. **If the engine only *detects*:** stay fully human-in-the-loop until prevention exists (don't run it
   unattended).
3. **Which card to play next** — by mood, by what's lonely, or by what you just feel like building.
4. **Who completes a real spec** (you, or the factory under your review) before a real driver build.

---

## Part 5 — What to honestly expect

- **Few real things, but real ones.** Early on you'll ship a *handful* of trustworthy components, not a
  flood. That's the point — trust and learning are the deliverable.
- **A short "nothing's shipping yet" stretch** during the on-ramp. You can soften it with quick
  smoke-toys and a self-build or two.
- **The factory will sometimes say "no"** (a don't-ship, or a refusal to build something it can't yet).
  That's the system working, not failing.
- **One AI seat, working serially.** Play for *getting it right and enjoying it*, not for speed.
- **You won't have "the factory" at the end — and that's success.** You'll have a prototype that has
  *earned* a real, evidence-backed list of what to build next, plus a handful of real things and a
  methodology you can actually show. Discovery is the win.

---

*Companions: [the charter](factory-discovery-charter.md) (why & how) and
[the methodology & formulas report](methodology-and-formulas-plain-english.md) (the Gas City formulas).
The full reasoning trail is in [`architectures/v4/_meta/next-steps/`](architectures/v4/_meta/next-steps/).
This is a living plan; it evolves as real work teaches us more.*
