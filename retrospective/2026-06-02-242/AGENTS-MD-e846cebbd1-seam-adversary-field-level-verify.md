# agent instruction

**A seam adversary verifies field-level matches; it never trusts a builder's self-attested 'seam matches'.** "When two components share a contract (a record schema, a wire type, an enum), the cross-component reviewer MUST diff the producing and consuming field lists by name and type — a builder reporting 'consumes X's schema, matches' is not sufficient evidence. The producer's frozen field names are authoritative; the consumer's reading of them must be checked character-for-character."

*Grounded in: a builder self-reported its `ScoreRecord` consumption matched while reading `score_value` where the producer froze `satisfaction_score`.*

# justification

A builder's receipt explicitly stated its record consumption "matched the frozen set, no missing fields." It did not — it read `score_value` while the producer froze `satisfaction_score`, a mismatch that would have silently dropped every record and left empty the satisfaction distribution that the entire downstream build trusts as its quality signal. The builder genuinely believed it matched; self-attestation of a cross-component seam is worth nothing because the builder only sees its own side. A reviewer that diffs the two field lists by name catches the highest-severity class of silent failure (a contract that type-checks but never carries data) in a few minutes.
