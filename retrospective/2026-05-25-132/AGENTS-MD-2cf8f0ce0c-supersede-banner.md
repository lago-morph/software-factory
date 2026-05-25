# agent instruction

**Add a SUPERSEDED banner to a document whose framing has been invalidated.** When later decisions invalidate a document's framing (e.g., the user reframes the question the document was answering), add a prominent SUPERSEDED block at the top of the affected file pointing at the replacement doc(s) and briefly explaining why. Preserve the original content below for historical context. Do not silently let stale framing continue to be the apparent authority.

*Grounded in: original DEC-1 brief's option-pick framing was invalidated by the user's reframe; SUPERSEDED banner added so the next agent wouldn't trust it.*

# justification

When the user reframed DEC-1 at session end, the original `decisions/dec-1-unification-verdict.md` brief (with its option-pick framing) was no longer the question the project was asking. Without a banner, the next agent picking up cold would see the brief, treat it as authoritative, and re-author DEC-1 in the wrong frame. A 5-line SUPERSEDED block at the top, pointing at the replacement docs and explaining briefly why, prevents that. Cost of the banner: 30 seconds and ~80 words. Cost of not having it: 30 minutes of next-agent confusion plus a second corrective reframe by the user.
