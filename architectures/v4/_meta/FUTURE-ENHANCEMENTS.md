# Future Enhancements Bucket

Deliberately deferred capabilities — not Phase-0/foundation scope, parked here by explicit decision so
the spec/plan stay honest about what is in vs out. Each item records why it was deferred and what would
trigger pulling it back in.

| ID | Enhancement | Deferred from | Decision / trigger to revisit |
|----|-------------|---------------|-------------------------------|
| FE-1 | **Cross-provider / cross-family judge** — judge model from a different provider-family than the coder, for independence against shared-model blind spots. | C29 model-floor, C32 judge-harness, C34 holdout-integrity | Decision D-1 (user, 2026-05-30): Phase-0 judge uses the **same provider** as the coder; holdout integrity comes from rig partitioning + role/prompt isolation. Revisit when a second-provider credential path exists (Max issues no second key today) or when same-family judge bias is measured as material. |

> Builders for C29/C32/C34 MUST treat cross-family judging as FE-1 (out of foundation scope) and spec the
> same-provider judge as the baseline, while leaving a clean seam (a `judge_family` policy hook) so FE-1
> can be switched on later without re-architecture.
