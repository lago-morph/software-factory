# C06 — Messaging (Mail + Nudge)  (Build Plan, canonical track)

> Source / Spec ref: spec/C06-agent-messaging.md

## 1. Work breakdown

C06 is a **config-and-contract** component, not a build: Mail (durable) + Nudge (ephemeral) are native Gas
City primitives (AI-CONTEXT §3.2 concept 6). The work is *naming the two semantics + envelope, gating
Mail, and proving no custom delivery/signing machinery is introduced* — not implementing a queue.

| Task | Description | Size | Prereqs |
|---|---|---|---|
| T1 | **Adopt the native Mail + Nudge primitives.** Use Gas City's `[mail]` (durable) + Nudge (ephemeral) as the coordination transport; **no custom queue/broker/retry code** (spec §1, §7). Config/wiring only. | S | C01, C04 |
| T2 | **Envelope + addressing contract.** Name the Mail/Nudge envelope shape: `from` (`created_by`), `to` (recipient address keyed on C04 `session.id` + C41/C42 actor), payload, durability flag. Freeze the addressing surface for dependents (spec §3 family 1–4). | M | T1, C04, C41 |
| T3 | **Attribution pass-through.** Verify `created_by` is stamped on **every** Mail and Nudge by the substrate (I3) — C06 adds no anonymous path and **no identity machinery** (inherited from C41/P9). | S | T1, C41 |
| T4 | **Mail config gate.** Wire `[mail]`-section-presence ⇒ durable Mail enabled (C03 capability-by-presence); confirm Phase-0 dark posture (`[mail]` absent ⇒ Nudge/bead fallback) per AI-CONTEXT L122 / README L364. | S | T1, C03 |
| T5 | **Durable-on-resume delivery.** Prove a Mail sent to a suspended/offline recipient is delivered when its **C04 session resumes** (I1, AC1) — the one functional claim that crosses the C04 seam. | M | T2, C04 |
| T6 | **Anti-build audit (the bar).** Import/usage audit proving C06 introduces **no** message queue/broker/pub-sub/retry/durable-inbox/**signing** subsystem — only native Mail/Nudge (AC5, spec §7). HMAC signing stays **dropped/deferred** (D-14). | S | T1 |
| T7 | **Gap spike (G36).** Document (not design) that message *authenticity* is unverified on the canonical track (self-asserted `created_by`); record the integrity residual → FE-3 signing, **blocked on G37** (secret, C03-owned, D-14); escalate to review-log. *No signing/secrets build.* | S | T3, T6 |

## 2. Dependency graph

Critical path: **C01 + C04 → T1 (adopt Mail/Nudge) → T2 (envelope/addressing contract) → T5 (durable-on-resume)**.
- **T1 is the gate**: nothing else lands until the native primitives are wired (it is pure adoption — no build).
- **T2 freezes the envelope/addressing contract** that coordinator roles (Mayor), C18 reconciler, and C05
  dispatch bind to — the highest-leverage early freeze (more dependents than the resume path itself).
- **T5 (durable-on-resume)** is the only task that hard-crosses the **C04** seam — it needs C04's
  suspend/resume (C04 §5) working, so it follows C04's continuity tasks.
- **Must precede C06:** **C04** (declared dep — recipients are sessions; durable Mail delivers on resume),
  **C03** (gates `[mail]`), **C41** (`created_by` stamp). C42 partition policy lands concurrently.
- **C06 must precede:** the coordination consumers (C18 reconciler wake-via-Nudge, coordinator/Mayor
  hand-offs via Mail) — none are *declared* deps of C06, so C06 has light downstream pressure.

## 3. Parallelization

After T1 lands, three small workstreams fan out:
- **WS-A (contract):** T2 — envelope + addressing. The shape dependents stub against; build first.
- **WS-B (attribution + gate):** T3 + T4 — `created_by` pass-through and `[mail]` config gate. Independent
  of WS-A's envelope internals; both are small.
- **WS-C (durability + bar):** T5 + T6 — durable-on-resume proof and the anti-build audit. T5 waits on C04
  continuity; T6 can run anytime after T1.
T7 (G36 spike) runs parallel once T3/T6 establish the attributed-but-unsigned posture.

## 4. Interfaces-first / contract milestones (freeze early)

1. **Mail/Nudge envelope + addressing contract (T2)** — `from`/`to`/payload/durability + the recipient
   address space (C04 `session.id` + C41/C42 actor). Freeze FIRST so coordinator roles and the reconciler
   build their coordination against a stub.
2. **Two-semantics contract (T1/spec §3)** — *Mail = at-least-once durable on resume (I1); Nudge =
   best-effort, droppable (I2)*. Freeze so callers choose the right primitive (must-deliver ⇒ Mail).
3. **Attribution invariant (T3)** — `created_by` on every message (I3), self-asserted (I4). Freeze so
   downstream attribution-consumers know what is (presence) and is not (integrity) guaranteed.
4. **Config gate (T4)** — `[mail]` presence ⇒ Mail; absent ⇒ dark. Freeze so phase-plan/Phase-0 (C54) and
   coordinating components know when durable Mail is available.

## 5. Risks & de-risking order

1. **G36 — attribution integrity (highest, the assigned gap).** Spike first: confirm the canonical-track
   posture is *attribution present, authenticity deferred*; record the residual (forged-sender undetected)
   → FE-3 signing, blocked on G37 (D-14). **Do not** build signing/secrets — record, do not invent.
2. **Durable-on-resume delivery (T5).** The riskiest functional claim — a Mail queued while the recipient
   was suspended is delivered on **C04 resume** (I1/AC1). Spike against a real suspend→resume early; it is
   the one cross-seam behaviour, and it depends on C04's resume fidelity (which is itself Partial, C04 F16).
3. **Anti-build creep (T6).** The standing temptation is to "improve" delivery with a custom retry/queue/
   dead-letter/signing layer. The audit (AC5) is the guard: anything beyond native Mail/Nudge is a flagged
   DROP (the bar). De-risk by auditing early, before any such code is written.
4. **Addressing granularity (T2).** v4 names the primitives but not the address space (per-`session.id` vs
   role vs topic — OQ4). Freeze a minimal address shape early so dependents are not blocked; refine in
   sweep-2.

## 6. Definition of done

- **Per spec ACs:** AC1 (durable Mail survives offline recipient, delivered on C04 resume, attributed),
  AC2 (Nudge ephemeral — dropped with no listener, no error/queue), AC3 (attribution totality — no
  anonymous message), AC4 (capability-by-presence — `[mail]` gates Mail, Phase-0 dark), AC5 (anti-build
  audit — no custom queue/broker/retry/signing), AC6 (G36 honesty — authenticity-deferred residual recorded).
- **Per-task DoD:** each artifact (the envelope/addressing contract, the `[mail]` gate config, the
  attribution + anti-build audits) is version-controlled as pack/`city.toml` (no Go fork, pack-only per
  AI-CONTEXT §3.5) and exercised by at least one real Mail (durable, delivered-on-resume) and one Nudge
  (best-effort, dropped-when-unheard), each carrying `created_by`.
- **Component DoD:** two agents coordinate end-to-end over native Mail + Nudge; a durable Mail to a
  suspended recipient is delivered on its C04 resume with `created_by` intact; an unheard Nudge is dropped
  without error; the anti-build audit confirms **zero** custom delivery/signing machinery; and the **G36**
  finding (attribution-present-but-unsigned; integrity → FE-3 blocked on G37) is written to
  `_meta/review-log.md` (closed by escalation, not silent acceptance of the "Addressed" F32 label).
