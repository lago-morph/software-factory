# agent instruction

**Verify upstream behavior claims via the actual source.** "When a spec asserts X about an external library or upstream component ('Gas City provides Y', 'library X handles Z natively', 'the upstream uses GPG signing'), verify against the actual source before designing around the claim. Open the repo, fetch the README, search the docs. If the claimed behavior does not exist upstream, downstream design framing of 'we add a thin contract over the upstream capability' is wrong — it is greenfield bolt-on, with different cost and risk."

*Grounded in: PR #218 research into gastownhall/gascity and gastownhall/wasteland: Gas City has no actor signing, Wasteland uses GPG only for inter-rig federation. The v4 spec's "C41 signing is a portability contract over upstream" framing was unanchored.*

# justification

Mid-session, the operator pushed back on the optimized track's C41 signing model with a substantive concern: "doesn't this just turn an *available* feature into a *requirement*?" My initial framing of C41 had implicitly assumed Gas City provided actor signing the spec was wrapping a contract around. The operator's question forced a check, and the WebFetch into the actual `gastownhall/gascity` repo found: zero mentions of signing, cryptography, HMAC, identity attribution, or keypair in the README, no signing-related files in `internal/mail/`, no actor signing in the session architecture. The only crypto in the repo is for release-artifact integrity (SHA-256 + GitHub artifact attestations), which is a completely different concern.

A follow-up fetch on `gastownhall/wasteland` (the federation companion the operator referenced) confirmed GPG signing exists there — but only for inter-rig federation across operators (multi-machine reputation stamps on a shared DoltHub commons), not for intra-rig actor signing between agents on one operator's setup. Different threat model, different scope, different problem.

That verification changed the analysis decisively. C41's signing model in the optimized track is not "we wrap a contract around an existing upstream capability"; it is greenfield bolt-on for a threat model that doesn't apply to a single-operator personal factory. The cost-benefit calculus flipped: less defensible without the upstream-capability framing, more clearly a candidate to defer (FE-3). The convergence ADR would have been miscalibrated without the verification.

The cost of the verification: one or two WebFetch calls, ~30 seconds total. The cost of designing around a phantom upstream capability: structural mis-design that's hard to unwind once specs and plans build on the assumed capability.

The rule applies any time a spec uses "native", "provides", "handles natively", "supports out-of-the-box", or similar phrasing about an external dependency. If you cannot point at the source line that implements the claim, you cannot design around it as if it existed.
