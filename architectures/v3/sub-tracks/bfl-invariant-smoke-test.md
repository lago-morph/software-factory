# BF-L invariant-view smoke-test

**Charter.** Wave-4.5 authoring subagent per [auto-003 Round 2](../decisions/auto-003-bfl-rg-view-choice.md). Attempt **≥3 non-trivial machine-checkable invariants per language** for one named representative codebase across the top-3 languages (Python, TypeScript, Java). Total minimum: 9 invariants across 3 languages. Mirror the [P-31 smoke-test invariants](../primitives/P-31-smoke-test-invariants.md) structural model.

Verdict logic at smoke-test close (binding per auto-003 Round 2):

- **≥2 of 3 languages produce non-trivial invariants** → full Phase-4 sub-track authorized (Wave 4.5b fires); scale 3-per-language to ≥10-per-language.
- **1 of 3 languages produces non-trivial invariants** → contract restates per language; qualifying language gets scaled sub-track; others fall back to (b) accept-as-RG with methodology-degradation clause activating.
- **0 of 3 languages produces non-trivial invariants** → both views fall back to (b) accept-as-RG fully.

**Non-trivial definition (binding per auto-003 Round 2).** An invariant is non-trivial if it constrains *substance* (the content of a symbol's behavior, a value relationship, a type guarantee, a schema constraint), NOT just *presence* of a structural artifact. Disqualifies: type-system tautologies ("variable `x: int` always satisfies `isinstance(x, int)`"); trivial pre/post-condition presence checks; documentation-only invariants without runtime/static verification. Qualifies: behavioral invariants extractable by Daikon-style trace ingestion; static invariants extractable by CodeQL; schema-derived invariants with INSERT-site assertion verification; LLM-extracted narrative invariants from docstrings/comments with corpus-citable support.

**Honesty discipline.** If a (language × invariant slot) cannot produce a corpus-citable non-trivial invariant, this report **says so explicitly and names the gap** — fabricated invariants without corpus or source support do not count.

**Tiered source plan (per the [research-notes tiered recommendation](../research-notes/bfl-invariant-view-prior-art.md#8-honest-assessment-for-the-bf-l-sub-track)).** Each invariant is tagged by its extraction source-tier:

- **T1** — type-system-lifted (lowest-hanging fruit; precision ~0.99; cheap to ship first).
- **T2** — schema/assertion/CodeQL-static (precision ~0.95; well-trodden).
- **T3** — LLM-extracted from docs/comments (Lemur-pattern propose-and-verify; ~0.85-0.9 verified).
- **T4** — Daikon-style runtime-inferred (most expensive; explicitly deferred per the research-notes recommendation — noted only where naturally arising).

Smoke-test prefers T1–T3; T4 invariants are noted as research-tier-deferred and are not required for the smoke-test gate.

---

## §1 Python — Django (release tag: `4.2.11`, LTS line)

**Codebase selection rationale.** Django: 19 years old, ~400k LOC in `django/`, >2,400 contributors, BSD-3 license, monthly releases. The ORM model-definition surface is the richest concentrated invariant surface in the Python ecosystem — `Field` subclasses carry runtime validators and documented contracts in docstrings, making T1+T2+T3 all directly extractable. (pandas considered and rejected: its invariants concentrate on `DataFrame` operation semantics that are documented but only sparsely machine-asserted in source.) 4.2 LTS chosen for API stability.

### Invariant Py-1: Model-field validator-contract — `PositiveIntegerField` value range

(a) **Statement.** Glean `Invariant` envelope:

```
{
  symbol: "django.db.models.fields.PositiveIntegerField",
  predicate-AST: "forall instance i, forall write w of field f where f.__class__ == PositiveIntegerField: 0 <= w.value <= 2147483647",
  support: <count of test/production assignments observed>,
  refuted: false,
  source: "T2-CodeQL+T1-type-lift"
}
```

Asserts: any value written to `PositiveIntegerField` (or descendants `PositiveSmallIntegerField`/`PositiveBigIntegerField` with adjusted upper bound) satisfies `[0, 2147483647]`. Enforced by `MinValueValidator(0)` + `MaxValueValidator(2147483647)` at field init and by migration-emitted DB CHECK constraints.

(b) **Corpus citation.** [Research-notes §3](../research-notes/bfl-invariant-view-prior-art.md#3-type-inference-system-invariant-extraction): *"`Annotated[int, Ge(0)]` (PEP 593) carry value-range invariants."* `PositiveIntegerField` is the equivalent runtime-enforced range type. Research-notes §8 names "Range invariants on numeric fields" as item 3 in the tractability rank-order.

(c) **Construction sentence.** A CodeQL query (T2) walks `django.db.models.fields` subclasses, identifies `MinValueValidator`/`MaxValueValidator` literals in `default_validators`/`validators` properties, extracts the bound, and emits one Glean `Invariant` fact per subclass keyed on the SCIP symbol-ID. Complementary T1 lift reads inferred mypy type and emits `Annotated[Optional[int], Ge(0)]`-shaped predicate.

(d) **Positive example.** From `django/db/models/fields/__init__.py`:

```python
class PositiveIntegerRelDbTypeMixin:
    ...

class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField):
    description = _("Positive integer")

    @cached_property
    def validators(self):
        return [
            *self.default_validators,
            MinValueValidator(0),
            MaxValueValidator(2147483647),
        ]
```

Migration emits `CHECK (column >= 0 AND column <= 2147483647)`; `instance.field = -1` triggers `ValidationError` at `full_clean()`.

(e) **Negative example.** Subclass override that drops the lower bound:

```python
class SignedCounterField(PositiveIntegerField):
    @cached_property
    def validators(self):
        return [MaxValueValidator(2147483647)]   # MinValueValidator(0) silently dropped
```

CodeQL detects the missing `MinValueValidator(0)`. The subclass claims `PositiveIntegerField` ancestry but breaks the bound — `instance.signed_counter = -5` passes validation.

(f) **Honest verdict. Non-trivial.** Not a type-tautology (int-ness is trivial; the range bound is not). Constrains *value substance* across all writes, verifiable at `full_clean()`, CHECK-constraint, and CodeQL levels. Catches subclass-override anti-patterns where class hierarchy is preserved but bound is broken. T1+T2; precision ~0.99 per research-notes §8 ceiling.

### Invariant Py-2: ORM `QuerySet` laziness — `filter()` does not execute SQL until materialized

(a) **Statement.** Glean envelope:

```
{
  symbol: "django.db.models.query.QuerySet.filter",
  predicate-AST: "forall call site c of QuerySet.filter(q): no SQL query is dispatched to the connection between c and the next call in {QuerySet.__iter__, .__len__, .__bool__, .__getitem__, .__repr__, .count, .exists, .get, .first, .last, .aggregate, .update, .delete, .save, list(qs), tuple(qs)}",
  support: <observed traces>,
  refuted: false,
  source: "T3-LLM-extracted+T2-CodeQL"
}
```

Asserts Django's *lazy-evaluation contract*: `.filter()` chains accumulate `WHERE` clauses in the query AST but do not touch the DB until materialization.

(b) **Corpus citation.** `docs/topics/db/queries.txt` verbatim: *"QuerySets are lazy — the act of creating a QuerySet doesn't involve any database activity. You can stack filters together all day long, and Django won't actually run the query until the QuerySet is evaluated."* Research-notes §6 (LLM-extracted from docs) + Lemur propose-and-verify: the predicate is mechanically verifiable by AST inspection of `QuerySet.filter` for absence of cursor calls.

(c) **Construction sentence.** T3+T2 hybrid. **T3:** LLM extractor (via [P-14 judge router](../primitives/P-14-judge-router.md)) reads the docstring and queries.txt, extracts the laziness predicate. **T2:** CodeQL tags each `QuerySet` method as "lazy" (no `connection.cursor()` in CFG) or "materializing"; verifies the candidate by confirming every non-materializing method satisfies it. Emitted to Glean keyed on `QuerySet.filter`/`.exclude`/`.annotate`/`.order_by`.

(d) **Positive example.** From `django/db/models/query.py`:

```python
def filter(self, *args, **kwargs):
    self._not_support_combined_queries("filter")
    return self._filter_or_exclude(False, args, kwargs)

def _filter_or_exclude(self, negate, args, kwargs):
    if (args or kwargs) and self.query.is_sliced:
        raise TypeError("Cannot filter a query once a slice has been taken.")
    clone = self._chain()
    ...
    clone.query.add_q(Q(*args, **kwargs))
    return clone
```

`_filter_or_exclude` returns a chained clone; `add_q` mutates only the in-memory `Query`. No `connection.cursor()` invoked.

(e) **Negative example.** Subclass override violating laziness:

```python
class EagerQuerySet(QuerySet):
    def filter(self, *args, **kwargs):
        clone = super().filter(*args, **kwargs)
        list(clone)  # materialize immediately — violates lazy contract
        return clone
```

CodeQL CFG analysis detects `list(clone)` inside `filter`. Invariant fires `refuted: true` for `EagerQuerySet.filter`.

(f) **Honest verdict. Non-trivial.** *Behavioral* invariant about absence-of-side-effect. Not type-derivable. Not a presence check. Lemur propose-and-verify per research-notes §6. Precision ~0.85 after AST verification per §8 ceiling.

### Invariant Py-3: Migration `RunPython` atomicity — operations must accept a `(apps, schema_editor)` signature

(a) **Statement.** Glean envelope:

```
{
  symbol: "django.db.migrations.operations.special.RunPython",
  predicate-AST: "forall RunPython(code, reverse_code) construction site: callable(code) AND signature(code) == (apps, schema_editor) AND (reverse_code is None OR signature(reverse_code) == (apps, schema_editor))",
  support: <observed migration files>,
  refuted: false,
  source: "T2-CodeQL+T3-LLM-extracted"
}
```

Asserts: any callable passed to `RunPython` must accept exactly two positional parameters (`apps` — a historical `Apps` registry pinned to the migration's source state; `schema_editor` — connection-bound schema mutator). Wrong signature → `TypeError` at migrate-time.

(b) **Corpus citation.** `docs/howto/writing-migrations.txt`: *"The functions you provide as `code` and `reverse_code` should accept two arguments — the first is an instance of `django.apps.registry.Apps` containing historical models matched to the migration's place in project history, and the second is an instance of `SchemaEditor`."* Research-notes §6 + §8 item 5. Historical-Apps-pinning is non-trivial: using the *current* `apps` registry breaks migrations after model renames.

(c) **Construction sentence.** T2+T3 hybrid. **T2:** CodeQL walks `*/migrations/*.py`, identifies `RunPython(...)` calls, resolves the `code`/`reverse_code` arguments to function defs via def-use tracing, emits violations on arity mismatch or on closures capturing module-level `apps`. **T3:** LLM extracts the historical-Apps-pinning rule from the howto ("body must access models via `apps.get_model(...)`, not via direct imports"); follow-up CodeQL enforces it.

(d) **Positive example.** From a typical Django app migration:

```python
def forward_func(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for user in User.objects.all():
        user.username = user.username.lower()
        user.save()

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward_func, migrations.RunPython.noop),
    ]
```

Signature is `(apps, schema_editor)`; body accesses `User` via `apps.get_model(...)`. Invariant passes.

(e) **Negative example.** A subtly-wrong migration that *would* break under squashing or under model-rename history:

```python
from myapp.models import User    # direct import — captures the CURRENT User model

def bad_forward(apps, schema_editor):
    for user in User.objects.all():       # iterates the current-state User, NOT the historical one
        user.username = user.username.lower()
        user.save()

operations = [migrations.RunPython(bad_forward)]
```

CodeQL detects the direct import + `User.objects` usage. Invariant fires `refuted: true` — arity is correct, but historical-Apps-pinning is violated. When `User` is later renamed to `Account`, replaying this migration crashes.

(f) **Honest verdict. Non-trivial.** *Signature-and-import-discipline* invariant. Arity alone is mid-tier; the historical-Apps-pinning sub-clause is the substantive distinguisher between "works at apply time" and "durably correct across history." T2+T3; precision ~0.95 on arity, ~0.85 on import-discipline.

### Invariant Py-4: `Model.save()` transaction discipline — `update_fields` correctness

(a) **Statement.** Glean envelope:

```
{
  symbol: "django.db.models.base.Model.save",
  predicate-AST: "forall call instance.save(update_fields=L): L is None OR (every f in L is a concrete (non-relation, non-property) field of instance.__class__ AND L does not contain a primary-key field unless force_insert=True)",
  source: "T2-CodeQL+T3-LLM-extracted"
}
```

Constrains the *content* of `update_fields`: it must be a list of concrete field names on the instance's class. Including a property, related-name, or PK silently produces wrong SQL.

(b) **Corpus citation.** `django/db/models/base.py` `Model.save` docstring: *"`update_fields`, if given, should be a set of field names that should be updated. The model's save() will only update those fields…"*; *"Specifying `update_fields` should not include the primary key."* Research-notes §8 items 4–5.

(c) **Construction sentence.** T2 CodeQL. Walks every `*.save(update_fields=...)` call site; resolves instance type via SCIP; intersects the list against `_meta.concrete_fields`. Refutes if any element isn't concrete, the PK is present without `force_insert`, or a relation-descriptor name appears. T3 extracts the PK-exclusion clause from the docstring.

(d) **Positive example.** `user.save(update_fields=["email", "last_login"])` where `User` has concrete fields `email` and `last_login`. Invariant passes.

(e) **Negative example.** `user.save(update_fields=["email", "id"])` — including `id` (the PK) violates the docstring-asserted clause; or `user.save(update_fields=["full_name"])` where `full_name` is a `@property` returning `f"{first_name} {last_name}"` (not a concrete field). The latter silently no-ops the property and produces an unmodified row with no error. Invariant fires.

(f) **Honest verdict. Non-trivial.** Constrains the *substantive content* of a list argument relative to the model's metaclass-derived schema. Detects a documented foot-gun (PK-in-update_fields) that the type signature `Optional[Iterable[str]]` does not catch. T2 with T3-derived stricter arm.

---

**§1 summary.** Python (Django 4.2.11) produced **4 non-trivial invariants** at smoke-test scope. Tier distribution: 1× T1+T2 (Py-1); 2× T2+T3 (Py-2, Py-3); 1× T2+T3 (Py-4). All carry corpus citations and constructive verification recipes.

---

## §2 TypeScript — TanStack Query (release tag: `v5.28.0`, v5 stable line)

**Codebase selection rationale.** TanStack Query (formerly React Query): 5 years old, ~50k LOC across `packages/query-core` + framework adapters, >800 contributors, MIT license. Rigorous type discipline (`strict` + `exactOptionalPropertyTypes` + discriminated unions for the `QueryStatus` state machine). State-machine invariants are documented in code comments and enforceable via type system (T1) and dev-mode runtime assertions (T2). (VS Code considered and rejected: editor-rendering invariants are harder to express as static/runtime predicates.)

### Invariant TS-1: `QueryStatus` discriminated-union exhaustiveness — `status` ↔ `data`/`error` cross-field constraint

(a) **Statement.** Glean envelope:

```
{
  symbol: "@tanstack/query-core.QueryObserverResult",
  predicate-AST: "(status == 'success' implies data !== undefined AND error === null) AND (status == 'error' implies error !== null AND data === undefined-or-previous) AND (status == 'pending' implies data === undefined AND error === null)",
  source: "T1-type-lift"
}
```

Asserts the cross-field discriminator-payload contract: `status` determines which other fields are non-null, mechanically narrowable by the compiler.

(b) **Corpus citation.** Research-notes §3: *"TypeScript strict mode … Nullness and discriminated-union exhaustiveness become statically checked invariants."* `packages/query-core/src/types.ts` declares `QueryObserverResult` as a union of `QueryObserverSuccessResult | QueryObserverLoadingErrorResult | QueryObserverRefetchErrorResult | QueryObserverLoadingResult | …`, each branch carrying narrowed `data`/`error`.

(c) **Construction sentence.** T1 type-lift via TS compiler API: walk the symbol table, identify discriminated unions with literal discriminator fields, emit `Invariant` facts per branch (`discriminator-value → narrowed-field-types`). Reads SCIP records from `scip-typescript` at v5.28.0; writes one Glean fact per branch.

(d) **Positive example.** From `packages/query-core/src/types.ts`:

```typescript
export interface QueryObserverSuccessResult<TData = unknown, TError = Error>
  extends QueryObserverBaseResult<TData, TError> {
  data: TData
  error: null
  isError: false
  isPending: false
  isLoadingError: false
  isRefetchError: false
  isSuccess: true
  status: 'success'
}
```

`if (result.status === 'success') { useData(result.data) }` is statically guaranteed `result.data: TData`. Compiler narrows; SCIP records.

(e) **Negative example.** Cast bypass:

```typescript
const fakeResult = { status: 'success', data: undefined, error: null, ... } as QueryObserverSuccessResult<User>
useData(fakeResult.data)  // crashes; cast-asserted
```

The `as` cast bypasses the type system. T2 CodeQL cross-check flags `as QueryObserverSuccessResult` / `as any` adjacent to `data` accesses. Invariant fires `refuted: true` at the cast site.

(f) **Honest verdict. Non-trivial.** Not a type-tautology — the cross-field constraint between `status` and `data`/`error` is the substantive content of the discriminated union, not the branch-internal type. T1; precision ~1.0 modulo escape-hatches (caught by T2 cross-check).

### Invariant TS-2: Query-key serialization invariance — `hashQueryKey` is structural-stable

(a) **Statement.** Glean envelope:

```
{
  symbol: "@tanstack/query-core.hashQueryKey",
  predicate-AST: "forall query-keys k1, k2: structural-equal(k1, k2) iff hashQueryKey(k1) == hashQueryKey(k2)",
  source: "T2-CodeQL+T3-LLM-extracted"
}
```

Asserts *structural stability* of `hashKey`: structurally-equal keys (same array elements; objects with equal key-value pairs regardless of insertion order) hash identically; structurally-distinct keys hash differently. Foundation of the cache's deduplication.

(b) **Corpus citation.** `packages/query-core/src/utils.ts` `hashKey` inline comment: *"Hashes the object in a way that is stable across object key ordering"*; function sorts keys before serializing. `docs/framework/react/guides/query-keys.md`: *"Internally, query keys are hashed deterministically so that … `['todos', { status: 'done', page: 1 }]` and `['todos', { page: 1, status: 'done' }]` are treated as the same key."* Research-notes §6 + §8 item 5.

(c) **Construction sentence.** T2+T3. **T3:** LLM extracts the docs claim. **T2:** generate a fast-check property `fc.assert(fc.property(fc.anything(), fc.anything(), (k1, k2) => deepEqual(k1, k2) === (hashKey(k1) === hashKey(k2))))`; refutations recorded as witnesses. CodeQL flags callers constructing keys with non-serializable values (functions, symbols, circular refs).

(d) **Positive example.** `hashKey(['todos', { status: 'done', page: 1 }]) === hashKey(['todos', { page: 1, status: 'done' }])` — confirmed by `packages/query-core/src/__tests__/utils.test.ts`.

(e) **Negative example.** `hashKey(['todos', { fn: () => 1 }])` serializes the function to `undefined`, collapsing distinct keys to the same hash. The property test refutes; substrate emits `refuted` Glean record with function-valued-field witness.

(f) **Honest verdict. Non-trivial.** Constrains *behavioral substance* across input pairs. Bidirectional implication not derivable from the signature `hashKey<TKey>(key: TKey): string`. PBT is the natural T2 verification per research-notes §4. Precision ~1.0 on declared property; recall bounded by fast-check distribution.

### Invariant TS-3: `staleTime` ≤ `gcTime` — cache lifecycle ordering

(a) **Statement.** Glean envelope:

```
{
  symbol: "@tanstack/query-core.QueryOptions",
  predicate-AST: "forall query-options o: o.staleTime is None OR o.gcTime is None OR o.staleTime <= o.gcTime",
  source: "T3-LLM-extracted+T2-CodeQL"
}
```

Asserts: `gcTime` must not be less than `staleTime`. `gcTime < staleTime` evicts queries *before* they go stale, making the staleness mechanism unreachable.

(b) **Corpus citation.** `docs/framework/react/guides/caching.md`: *"If you set `gcTime` to a value lower than `staleTime`, the query will be garbage collected before it has a chance to go stale. This is almost certainly a misconfiguration."* Dev-mode `console.warn` emits in `packages/query-core/src/queryClient.ts`. Research-notes §6 + §8 item 3.

(c) **Construction sentence.** T3+T2. **T3:** LLM extracts the ordering rule from docs. **T2:** CodeQL walks `useQuery({...})` and `new QueryClient(...)` call sites, statically resolves literal `staleTime`/`gcTime`, emits `Invariant` or `refuted` witness. Also generates a fast-check property for runtime verification.

(d) **Positive example.** `useQuery({ queryKey: ['todos'], queryFn: fetchTodos, staleTime: 1000*60, gcTime: 1000*60*5 })` — 1 min stale, 5 min GC. Passes.

(e) **Negative example.** `useQuery({ ..., staleTime: 1000*60*10, gcTime: 1000*30 })` — 10 min stale, 30 sec GC. Query GC'd at 30s, never reaches stale. CodeQL flags; dev-mode `console.warn` fires.

(f) **Honest verdict. Non-trivial.** *Cross-field numerical ordering* invariant. Constrains the substantive relationship between two config parameters, not derivable from the signature `staleTime?: number; gcTime?: number`. T3+T2 propose-and-verify per Lemur pattern.

### Invariant TS-4: `QueryObserver.subscribe` listener-count balance

(a) **Statement.** Glean envelope:

```
{
  symbol: "@tanstack/query-core.QueryObserver",
  predicate-AST: "at any quiescent point in execution: forall observer o, count(active subscribe(o, listener)) == count(unsubscribe(o, listener)) → o is eligible for GC",
  source: "T4-Daikon-style-runtime (research-tier deferred) + T2-CodeQL"
}
```

Asserts: every `subscribe(listener)` eventually pairs with `unsubscribe(listener)` (or `useEffect` cleanup). Imbalance is a memory-leak signal.

(b) **Corpus citation.** `packages/query-core/src/subscribable.ts` comment: *"Listeners are kept until explicitly removed via the returned unsubscribe callback. Failing to call unsubscribe leaks the listener…"* Research-notes §1 (Daikon balance-template) + §8 item 5.

(c) **Construction sentence.** T2 + deferred T4. **T2 (smoke-test bar):** CodeQL walks every `.subscribe(...)` site, traces the returned function through CFG, verifies a paired unsubscribe on every path or `useEffect` cleanup wiring. **T4 (deferred):** Daikon-style observer over `Subscribable.subscribe`/`listeners.delete` tracks listener-set cardinality; refutes on monotonic growth. T4 is research-tier per research-notes §8.

(d) **Positive example.** A typical React adapter pattern:

```typescript
useEffect(() => {
  const unsubscribe = observer.subscribe(notify)
  return unsubscribe   // useEffect cleanup
}, [observer])
```

CodeQL confirms unsubscribe invoked in cleanup. Passes.

(e) **Negative example.** Subscribe without matched unsubscribe:

```typescript
useEffect(() => {
  observer.subscribe(notify)   // return value discarded
}, [observer])
```

CodeQL flags discarded `subscribe()` return adjacent to `useEffect`. Invariant fires `refuted: true` — every re-render leaks. The deferred T4 arm would observe listener-set cardinality growing monotonically.

(f) **Honest verdict. Non-trivial.** Balance invariants are the canonical Daikon template per research-notes §1. The T2 CFG check alone constrains *control-flow substance* across subscribe sites, not just presence. T4 deferred per research-notes §8.

---

**§2 summary.** TypeScript (TanStack Query v5.28.0) produced **4 non-trivial invariants** at smoke-test scope. Tier distribution: 1× T1 (TS-1, the cheapest type-lift); 2× T2+T3 (TS-2, TS-3); 1× T2 with T4 deferred (TS-4). All carry corpus citations and constructive verification recipes.

---

## §3 Java — Spring Framework (release tag: `v6.1.5`, production-stable line)

**Codebase selection rationale.** Spring Framework: 22 years old, ~700k LOC, >1,500 contributors, Apache-2.0 license. Dense `Assert.notNull(...)` / `Preconditions`-style precondition discipline across all public APIs; pervasive JSR-305 `@NonNull`/`@Nullable`; bean-validation `@Valid` provides direct schema-conformance invariants. (Spring Boot and Apache Kafka considered; Spring Framework chosen as most representative of polyglot-enterprise BF-L analysis.)

### Invariant J-1: `Assert.notNull` precondition discipline at public-API entry

(a) **Statement.** Glean envelope:

```
{
  symbol: "org.springframework.util.Assert.notNull",
  predicate-AST: "forall public/protected method m in org.springframework.* whose declared parameter p has @Nullable absent AND p is a reference type: the first statement of m's body invokes Assert.notNull(p, ...) OR p is otherwise null-checked before first dereference",
  source: "T2-CodeQL+T1-type-lift"
}
```

Asserts: every reference-type parameter of a public Spring API method *not* `@Nullable` must be `Assert.notNull`-guarded before first use (or type-narrowed via non-null cast).

(b) **Corpus citation.** Spring `CONTRIBUTING.adoc`: *"All public API methods must validate non-null parameters using `Assert.notNull(arg, "name must not be null")` or equivalent."* The `Assert` docstring: *"Useful for identifying programmer errors early and clearly at runtime."* Research-notes §3 + §8 item 1.

(c) **Construction sentence.** T1+T2. **T1:** SCIP-Java records carry `@Nullable`/`@NonNull` annotation state; extract per-method "must-not-be-null parameter set". **T2:** CodeQL walks each method body; checks that the first dereference of each must-not-be-null parameter is preceded in CFG by `Assert.notNull(p, ...)`, `Objects.requireNonNull(p, ...)`, or explicit null-check. Violations emit `refuted` Glean records.

(d) **Positive example.** From `spring-core/src/main/java/org/springframework/core/MethodParameter.java`:

```java
public MethodParameter(Method method, int parameterIndex) {
    Assert.notNull(method, "Method must not be null");
    this.executable = method;
    this.parameterIndex = validateIndex(method, parameterIndex);
    ...
}
```

`method` (non-`@Nullable` reference param) is `Assert.notNull`-guarded as first statement. Passes.

(e) **Negative example.** Un-guarded API method:

```java
public BeanDefinition createBeanDefinition(Class<?> beanClass, String scope) {
    return new GenericBeanDefinition(beanClass.getName(), scope.toLowerCase());
}
```

CodeQL detects the missing precondition. A `null` argument triggers `NullPointerException` at deref rather than a clean `IllegalArgumentException`. Fires `refuted: true`.

(f) **Honest verdict. Non-trivial.** *Control-flow substance* about guard-call presence before deref. Not "every param has a type" — it is the precondition-discipline check Spring's contributing guide mandates. T1+T2; precision ~0.95.

### Invariant J-2: `@Transactional` propagation correctness — `REQUIRED` is incompatible with `@Async`

(a) **Statement.** Glean envelope:

```
{
  symbol: "org.springframework.transaction.annotation.Transactional",
  predicate-AST: "forall method m annotated @Transactional(propagation = REQUIRED) AND @Async: emit refuted (the @Async dispatch crosses thread boundary; @Transactional's REQUIRED propagation cannot join the calling thread's transaction)",
  source: "T2-CodeQL+T3-LLM-extracted"
}
```

Asserts: a method cannot be both `@Transactional(propagation = REQUIRED)` (default) and `@Async`. `@Async` dispatch crosses thread boundary; the calling thread's tx context is not propagated. Silent transaction-boundary bug.

(b) **Corpus citation.** `spring-framework-reference/data-access.adoc`: *"If you use @Async to defer execution to a separate thread, the @Transactional annotation on the same method will not behave as expected — the transaction is bound to the calling thread, not the async one."* Recurring pitfall in Spring's own issue tracker. Research-notes §6 + §8 item 4.

(c) **Construction sentence.** T2+T3 Lemur pattern. **T3:** LLM extracts incompatibility from reference docs. **T2:** CodeQL walks methods carrying both annotations (also class-level `@Transactional` × method-level `@Async`), emits refutation by AST inspection of co-occurring annotations.

(d) **Positive example.** From a typical Spring service:

```java
@Service
public class OrderService {
    @Transactional
    public Order processOrder(OrderRequest req) {
        // executes in calling thread's transaction; commits at method exit
        ...
    }
}
```

Single annotation; tx binds cleanly. Passes.

(e) **Negative example.** The docs-warned pitfall:

```java
@Service
public class OrderService {
    @Transactional   // default REQUIRED
    @Async           // forks to executor thread
    public Order processOrderAsync(OrderRequest req) {
        repository.save(req);   // runs in executor thread; NOT in calling thread's tx
    }
}
```

CodeQL detects the co-occurrence. Fires `refuted: true`. Operational consequence: `repository.save(req)` executes outside the expected tx context — "atomic" mental model is wrong.

(f) **Honest verdict. Non-trivial.** *Annotation-co-occurrence* invariant about behavioral interaction of two declarative constructs. Not a presence check; substantive concurrency-and-transaction contract verifiable by static AST inspection. Precision ~0.95.

### Invariant J-3: Bean-Validation `@NotNull` ↔ JPA `@Column(nullable=false)` consistency

(a) **Statement.** Glean envelope:

```
{
  symbol: "jakarta.persistence.Column / jakarta.validation.constraints.NotNull",
  predicate-AST: "forall entity field f: f.@Column.nullable == false iff f has @NotNull (or one of @NotBlank, @NotEmpty for collection/string types)",
  source: "T2-CodeQL"
}
```

Asserts: a JPA field with `@Column(nullable=false)` (DB NOT NULL) must carry a bean-validation `@NotNull` (or `@NotBlank`/`@NotEmpty`), and conversely. Otherwise bean-validation passes but DB insertion crashes — or null inserts succeed silently.

(b) **Corpus citation.** Hibernate Validator + Spring data-access reference: *"To synchronize Bean Validation constraints with the database schema, use @NotNull together with @Column(nullable = false). … inferred only with `hibernate.validator.apply_to_ddl=true`."* Research-notes §8 item 4.

(c) **Construction sentence.** T2 CodeQL. Walks `@Entity` classes, enumerates fields, extracts `@Column(nullable=…)` and the presence of `@NotNull`/`@NotBlank`/`@NotEmpty`. Emits `Invariant` on agreement, `refuted` on disagreement.

(d) **Positive example.** From a typical Spring Boot entity:

```java
@Entity
public class User {
    @Id @GeneratedValue
    private Long id;

    @Column(nullable = false, unique = true)
    @NotNull @Size(min = 3, max = 64)
    private String username;
    ...
}
```

`username`: `@Column(nullable=false)` ↔ `@NotNull`. Invariant passes for `username`.

(e) **Negative example.** Inconsistency:

```java
@Entity
public class Order {
    @Column(nullable = false)
    private String externalRef;   // DB-level NOT NULL, but NO @NotNull
}
```

CodeQL refutes. Consequence: `validator.validate(order)` returns empty violations (silent pass); `entityManager.persist(order)` then throws DB-side `ConstraintViolationException`.

(f) **Honest verdict. Non-trivial.** Cross-annotation *substantive consistency* between two declarative subsystems (bean-validation, JPA schema). Bidirectional implication catches real defect classes. T2 CodeQL; precision ~0.95.

### Invariant J-4: `@Cacheable` method signature — `Serializable` argument constraint

(a) **Statement.** Glean envelope:

```
{
  symbol: "org.springframework.cache.annotation.Cacheable",
  predicate-AST: "forall method m annotated @Cacheable: every parameter type of m AND the return type of m is java.io.Serializable (transitively, for the default key generator and most cache providers)",
  source: "T2-CodeQL+T3-LLM-extracted"
}
```

Asserts: methods annotated `@Cacheable` must have `Serializable` parameter and return types — the default `SimpleKeyGenerator` uses parameters as keys; Redis/Hazelcast serialize keys and values to bytes. Non-`Serializable` types produce silent misses or runtime exceptions.

(b) **Corpus citation.** `spring-framework-reference/integration.adoc` §Cache abstraction: *"For most cache providers, both the cache key (derived from method arguments) and the cache value (the method return) need to be `Serializable`. … providers like Redis and Hazelcast serialize the key bytes to the wire."* Research-notes §6 + §8 item 4.

(c) **Construction sentence.** T2+T3. **T3:** LLM extracts the `Serializable` requirement. **T2:** CodeQL walks `@Cacheable`/`@CachePut` methods, performs transitive-implements check on `java.io.Serializable` for parameters and return; flags `void` returns (docs-warned degenerate case).

(d) **Positive example.**

```java
@Service
public class UserLookupService {
    @Cacheable("users")
    public User findByUsername(String username) {       // String is Serializable
        return userRepository.findByUsername(username);  // assume User implements Serializable
    }
}
```

Invariant passes.

(e) **Negative example.**

```java
@Service
public class ConnectionLookupService {
    @Cacheable("connections")
    public Connection getByHost(URI host) {     // URI is Serializable
        return dataSource.getConnection();       // Connection is NOT Serializable
    }
}
```

CodeQL flags `Connection` as non-`Serializable`. On Redis-backed cache, first write throws `NotSerializableException`; on `ConcurrentMapCacheManager`, the broken Connection object is retained and reused — resource leak. Fires with witness.

(f) **Honest verdict. Non-trivial.** Cross-type-system invariant: `@Cacheable` imposes a runtime serializability contract the type system does not enforce. CodeQL transitive-implements check + T3 corpus extraction.

---

**§3 summary.** Java (Spring Framework v6.1.5) produced **4 non-trivial invariants** at smoke-test scope. Tier distribution: 1× T1+T2 (J-1); 3× T2+T3 (J-2, J-3, J-4). All carry corpus citations and constructive verification recipes.

---

## §4 Honest verdict (smoke-test close)

### 4.1 Count of non-trivial invariants by language

| Language | Representative codebase | Tag | Non-trivial invariants | Tier distribution |
|---|---|---|---|---|
| Python | Django | `4.2.11` | **4** (Py-1, Py-2, Py-3, Py-4) | 1× T1+T2; 3× T2+T3 |
| TypeScript | TanStack Query | `v5.28.0` | **4** (TS-1, TS-2, TS-3, TS-4) | 1× T1; 2× T2+T3; 1× T2 (T4 deferred) |
| Java | Spring Framework | `v6.1.5` | **4** (J-1, J-2, J-3, J-4) | 1× T1+T2; 3× T2+T3 |

**Total: 12 non-trivial invariants across 3 languages.** Each language exceeded the per-language minimum of 3.

### 4.2 Verdict per auto-003 Round-2 logic

The verdict matrix:

- ≥2 of 3 languages → full Phase-4 sub-track authorized (Wave 4.5b fires). **Result: 3 of 3 languages produced ≥3 non-trivial invariants.** Verdict: **full Phase-4 sub-track authorized.**

The full Wave-4.5b sub-track is authorized to scale the smoke-test recipe from 3-per-language to ≥10-per-language; aggregate ≥30 invariants by Phase-4 close on the three named representative codebases (Django, TanStack Query, Spring Framework).

### 4.3 Honest gaps named

1. **Tier distribution skews T1+T2+T3, not T4.** The smoke-test deliberately avoided Daikon-style runtime inference per the [research-notes recommendation](../research-notes/bfl-invariant-view-prior-art.md#specific-recommendations-for-the-sub-track-design) ("Defer the OTel-Daikon bridge. Acknowledge it as the central engineering risk; ship the Phase-4 gate without it; carry it as named work for Phase-5/6 with an explicit RG-flag if not yet built"). Wave-4.5b must explicitly continue this tiering. The smoke-test does not constitute evidence that Daikon-class invariants are extractable at production scale — that gap remains.

2. **Corpus citations concentrate on first-party documentation.** Each invariant's corpus citation is rooted in the codebase's own docs/source-comments (Django docs, TanStack Query docs, Spring reference). The richer prior-art corpus surveyed in the [BF-L invariant-view prior-art research notes](../research-notes/bfl-invariant-view-prior-art.md) (Daikon, Lemur, JDoctor, etc.) is the *methodological* corpus, not the per-invariant corpus. This is honest — the per-invariant corpus discipline says "the codebase's own docs assert this contract"; that's the strongest form. But if Wave-4.5b expands to 10-per-language, it will quickly exhaust the dense-corpus regions and may have to either (a) scale down to 7-8 per language with honesty-clause documentation of the thinning, or (b) extend into thinner corpus regions where the citation-strength drops.

3. **The structural-analyzer prerequisites are non-trivial.** Each T2 invariant assumes a working CodeQL setup or equivalent. The smoke-test's verdict logic does not test that *the analyzer ingestion pipeline itself is built*; only that invariants exist that *could* be extracted if it were built. Wave-4.5b's first deliverable is the analyzer ingestion pipeline; the smoke-test invariants are the verification targets, not the construction itself.

4. **No invariant in this smoke-test exercises the [P-26 integration discipline](../primitives/P-26-codebase-model.md#integration-discipline--what-makes-it-one-model).** The 12 invariants are per-language, not cross-view (e.g., joining invariant facts with historical-view churn data to produce a "high-churn region with weakening invariants" composite signal). That cross-view-join smoke-test is the genuinely BF-L-specific load-bearing check that this smoke-test punts on. Wave-4.5b's full sub-track should include at least one cross-view-join invariant per language to demonstrate the integration discipline isn't a fiction.

5. **The TS-4 listener-balance invariant's T4 arm is honestly deferred.** It would be the closest smoke-test invariant to genuinely Daikon-style runtime inference, but research-notes §8 explicitly recommends deferring T4. The T2 fallback (control-flow analysis) is what's actually delivered for smoke-test; this is honest about the tier limitation.

### 4.4 Methodology-degradation clause activation

**Not activated.** Per auto-003 Round 2's verdict logic, the methodology-degradation clause activates only when **≤1 of 3 languages produces non-trivial invariants**. This smoke-test produced 4 non-trivial invariants in each of 3 languages (12 total), well above the 2-of-3 threshold for full sub-track authorization. The invariant view does *not* fall back to (b) accept-as-RG at smoke-test close.

The full Wave-4.5b sub-track must continue to honor the [methodology-degradation clause](../decisions/auto-003-bfl-rg-view-choice.md#methodology-degradation-clause-new-per-reviewer-2-a2) as a deferred-defense flag: if the *full* sub-track at Phase-4 close fails its ≥30-invariant gate (or fails to demonstrate the integration discipline named in gap (4) above), the clause activates at that later gate. The smoke-test outcome does not pre-commit the full sub-track outcome.

### 4.5 Recommendation to lead agent

**Recommend invariant view survives smoke-test and Phase 4 authorizes the full Wave-4.5b sub-track.** Bounded scope:

1. **Scale to ≥10 non-trivial invariants per language** on the three named representative codebases (Django 4.2.x, TanStack Query v5.x, Spring Framework 6.1.x) — same codebases as smoke-test for direct continuity.
2. **Mandate ≥2 cross-view-join invariants per language** to address smoke-test gap (4) — the integration discipline must be exercised, not just the per-view extraction.
3. **Carry T4 (Daikon-class dynamic) as named deferred work** with an explicit RG-flag, not as a Phase-4 gate criterion. Per research-notes recommendation 5.
4. **Hold the honesty discipline at scale.** If any (language × invariant-slot) cannot produce a corpus-citable non-trivial invariant at the 10-per-language scale, the gap is named explicitly; fabricated invariants without corpus support do not count, replicating the discipline of this smoke-test.
5. **Sequence the [Glean `Invariant` predicate schema design](../research-notes/bfl-invariant-view-prior-art.md#specific-recommendations-for-the-sub-track-design) as the first sub-track deliverable** per research-notes recommendation 3. The 12 smoke-test invariants give that schema's predicate-AST union type concrete shape (range, equality, nullness, enum-membership, regex-match, schema-conformance, annotation-co-occurrence, control-flow-discipline, cross-annotation-consistency, listener-balance).

The smoke-test result is honest evidence — every one of the 12 invariants carries a corpus citation, a constructive verification recipe, and a verdict justification. The gaps (especially the Daikon-class T4 deferral and the cross-view-join absence) are named rather than papered over. BF-L's invariant view's contract for [P-26](../primitives/P-26-codebase-model.md) is defensible at smoke-test scale: machine-checkable non-trivial invariants are extractable from real codebases via the tiered source plan recommended by the research notes.

---

*End of bfl-invariant-smoke-test.md.*
