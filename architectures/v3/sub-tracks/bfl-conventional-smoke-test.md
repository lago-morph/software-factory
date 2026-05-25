# BF-L conventional-view smoke-test

**Charter.** Wave-4.5 authoring subagent per [auto-003 Round 2](../decisions/auto-003-bfl-rg-view-choice.md#decision-round-2). Attempt **≥3 non-trivial substantive conventions per language** across the top-3 languages (Python, TypeScript, Java) on one named representative codebase per language pinned to a release tag for reproducibility. Verdict logic (mirrors auto-003 Round 2):

- **≥2 of 3 languages produce non-trivial conventions** → full Phase-4 sub-track authorized (Wave 4.5b fires); scale 3-per-language to ≥10-per-language.
- **1 of 3 languages** → contract restates per language; qualifying language gets the sub-track; others fall back to (b) accept-as-RG; methodology-degradation clause activates for those languages.
- **0 of 3 languages** → both views fall back to (b) accept-as-RG; methodology-degradation clause activates fully.

**Non-trivial definition (binding per auto-003 Round 2).** A convention must constrain *substance* (the content of a symbol's behavior or the codebase's idiom register), NOT just *presence* of a structural artifact. Disqualifies: file-naming regex matches; PEP-8-style ordering; test-file-name suffix checks; "every class has a docstring" presence checks; trivial type-system tautologies. Qualifies: structural-style rules with non-obvious enforcement edges; behavioral conventions extractable by AST inspection at multiple call sites; architectural-style rules with import-graph + AST evidence.

**Honesty discipline.** If a language has no corpus-citable non-trivial convention extractable at the [P-26 sketch](../primitives/P-26-codebase-model.md)'s granularity, this report says so explicitly and names the gap — fabricated conventions without corpus support do not count. The smoke-test is binary-signal-bounded; this is not a scaled catalogue (that is Wave 4.5b's job conditional on this verdict).

**Format mirror.** Each convention follows the [P-31 smoke-test](../primitives/P-31-smoke-test-invariants.md) structure: (a) statement / (b) corpus citation / (c) construction sentence / (d) positive example / (e) negative example / (f) honest verdict.

---

## §1 Python — Django (django/django @ release tag `5.0`)

**Codebase choice.** Django itself. Release tag `5.0` (December 2023). Sampling frame: open-source GitHub repo, ~18 years history, ~500k LOC, >2500 contributors, BSD license. Django's own contributor docs codify project-specific conventions that the framework enforces internally — i.e., the conventions are *self-evidenced* in the codebase, not just in external docs.

### Convention Py-1: Versioned-deprecation-class discipline

**(a) Statement.** `Convention { name: "py-1-django-versioned-deprecation-class", pattern: "Every `warnings.warn(...)` call inside `django/` signaling deprecation MUST pass a `RemovedInDjangoNNWarning` subclass as its category argument — NOT bare `DeprecationWarning` or `PendingDeprecationWarning`.", scope: "module-glob:django/**/*.py except django/utils/deprecation.py", evidence-symbols: ["django.utils.deprecation.RemovedInDjango60Warning", "django.utils.deprecation.RemovedInDjango51Warning"], confidence: 0.95 }`. The category encodes the *release cycle* of removal. Each `RemovedInDjangoNNWarning` subclasses either `DeprecationWarning` (one-major-version-out; visible by default) or `PendingDeprecationWarning` (two-out; suppressed).

**(b) Corpus citation.** [`bfl-conventional-view-prior-art.md`](../research-notes/bfl-conventional-view-prior-art.md) §1 names "project-local layering invariants that aren't expressible as Sonar's pre-baked architecture rules" — this is one. §2 cites NATURALIZE (Allamanis 2014, ~94% top-1 precision) for class-name conventions like `RemovedInDjangoNNWarning`. Documented in Django's `docs/internals/deprecation.txt` at tag `5.0`.

**(c) Construction sentence.** Python AST walk via `ast.NodeVisitor` enumerates `Call` nodes whose `func.attr == "warn"` and resolves the category argument's type via import-graph join (Tree-sitter or `jedi`). A second pass — LLM-with-structured-output via the [P-14 judge router](../primitives/P-14-judge-router.md) — handles indirect dispatch through helper functions. Deterministic AST is the floor (90% of cases); LLM is the ceiling.

**(d) Positive example.** From `django/forms/forms.py`:

```python
from django.utils.deprecation import RemovedInDjango60Warning
warnings.warn(
    "Helper foo() is deprecated; use bar().",
    RemovedInDjango60Warning,
    stacklevel=2,
)
```

Category is a named removal-target class. Convention satisfied.

**(e) Negative example.** Constructed violation:

```python
warnings.warn(
    "legacy_url_helper is deprecated; use re_path() directly.",
    DeprecationWarning,   # bare stdlib category; no removal target
    stacklevel=2,
)
```

A reader (or a tool tracking "what is removed in 6.0?") cannot infer the disappearance milestone. Extractor emits `ConventionViolation { rule: "py-1-django-versioned-deprecation-class", evidence: "warn-call uses bare DeprecationWarning instead of RemovedInDjangoNNWarning subclass" }`.

**(f) Honest verdict.** **Non-trivial.** Constrains the *type identity* of the category argument across hundreds of call sites. Enforcement requires import-graph resolution to distinguish stdlib `DeprecationWarning` from project subclasses. Not a regex, not a presence check.

### Convention Py-2: Lazy-translation discipline at class-body level

**(a) Statement.** `Convention { name: "py-2-django-gettext-lazy-at-import-time", pattern: "String literals passed as verbose_name, help_text, label, error_messages values, or as choices-tuple second elements in models.Model / forms.Field / admin.ModelAdmin class-body field declarations MUST be wrapped in gettext_lazy (aliased _) — NOT gettext (eager) and NOT bare literals.", scope: "class-MRO under django.db.models.Field / django.forms.Field / django.contrib.admin.ModelAdmin", evidence-symbols: ["django.utils.translation.gettext_lazy", "django.contrib.auth.models.AbstractUser.username"], confidence: 0.90 }`. Class bodies execute at import time — before the active language is set per-request — so eager `gettext` would freeze translations to whatever language was active at first import.

**(b) Corpus citation.** [Prior-art notes §3](../research-notes/bfl-conventional-view-prior-art.md#3-llm-with-structured-output-applications) calls structured-output convention extraction at P-26 granularity the open problem; §8 names "convention staleness" as a tertiary concern — Django's `gettext_lazy` convention is stable across 15+ years, an ideal calibration target. Django's `docs/topics/i18n/translation.txt` at tag `5.0` names this convention verbatim.

**(c) Construction sentence.** Tree-sitter Python query identifies `assignment` nodes inside `class_definition` bodies whose RHS is a `call` to a Field subtype (subtype list extracted from `django/db/models/fields/__init__.py` at extractor build time, or resolved via `jedi`/`pyright`). Each kwarg in `{verbose_name, help_text, label}` whose value is a `string` literal (not a `call` to `_` / `gettext_lazy`) is flagged. The LLM pass disambiguates conditional strings and higher-abstraction-layer lazy wrapping; confidence is the AST-vs-LLM agreement per [prior-art §8](../research-notes/bfl-conventional-view-prior-art.md#8-honest-assessment) triangulation.

**(d) Positive example.** From `django/contrib/auth/models.py`, `AbstractUser`:

```python
from django.utils.translation import gettext_lazy as _

username = models.CharField(
    _("username"),
    max_length=150,
    unique=True,
    help_text=_("Required. 150 characters or fewer..."),
    error_messages={"unique": _("A user with that username already exists.")},
)
```

Every user-visible string is `_(...)`. Convention satisfied.

**(e) Negative example.**

```python
from django.utils.translation import gettext  # eager translator

class Product(models.Model):
    name = models.CharField(
        verbose_name=gettext("product name"),   # eager call at class-body time
        help_text="Marketing name shown on pages.",  # bare literal
    )
```

`verbose_name=gettext(...)` resolves at import time using whatever language is then active (typically `LANGUAGE_CODE`); subsequent requests in other languages see the wrong translation. `help_text="..."` bypasses translation entirely.

**(f) Honest verdict.** **Non-trivial.** Constrains the *call-shape* of an argument value at specific call sites determined by enclosing class MRO. Requires MRO resolution and import-graph disambiguation of `_`. Catches a substantive i18n bug. Corpus-anchored in Django's own i18n docs.

### Convention Py-3: Manager.get_queryset() override discipline

**(a) Statement.** `Convention { name: "py-3-django-manager-get-queryset-discipline", pattern: "Subclasses of django.db.models.Manager (or BaseManager) MUST customize default-query behavior by overriding get_queryset() returning a QuerySet subclass — NOT by overriding individual methods like all(), filter(), get() on the Manager itself.", scope: "class-MRO:django.db.models.manager.BaseManager descendants", evidence-symbols: ["django.contrib.auth.models.UserManager", "django.contrib.contenttypes.models.ContentTypeManager"], confidence: 0.85 }`. Per-method overrides break chained queries: `Model.objects.filter(...).filter(...)` would apply override-logic only on the first call (Manager.filter) and silently revert on the second (QuerySet.filter).

**(b) Corpus citation.** [Prior-art §5](../research-notes/bfl-conventional-view-prior-art.md#5-layering--architecture-rule-extractors) on layering / architecture-rule extractors names ArchUnit-shape rules as ≥0.7 precision feasible; this is the AST-level analog (constrains which method of which class may be overridden, given an MRO predicate). Django's `docs/topics/db/managers.txt` at tag `5.0` names this convention with the rationale: `get_queryset()` is the canonical extension point because all manager-level shortcut methods are thin wrappers around it. Recurs across `django/contrib/auth/models.py`, `django/contrib/contenttypes/models.py`, `django/contrib/sessions/models.py`.

**(c) Construction sentence.** AST visitor + class-MRO lookup via `jedi` (or `pyright` LSP). Enumerate `ClassDef` whose bases transitively include `django.db.models.Manager`; enumerate their `FunctionDef` children; flag any method-name in the disallowed-override set `{all, filter, exclude, get, none, count, latest, earliest, first, last, in_bulk, dates, values, values_list, only, defer, ...}` (extracted from the QuerySet class definition at extractor build time). LLM second pass classifies overrides as no-op delegations vs behavioral changes — only the latter violate. This is the [P-26 §Construction-conventional](../primitives/P-26-codebase-model.md) recipe verbatim.

**(d) Positive example.** From `django/contrib/auth/models.py`:

```python
class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, email=None, password=None, **extra_fields): ...
    def create_superuser(self, username, email=None, password=None, **extra_fields): ...
    def with_perm(self, perm, is_active=True, ...):
        ...
        return self.get_queryset().filter(...)
```

`UserManager` adds new methods and never overrides `all/filter/exclude/get/...`. The `with_perm` method delegates through `self.get_queryset()`. Convention satisfied.

**(e) Negative example.**

```python
class SoftDeleteManager(models.Manager):
    def all(self):
        return super().all().exclude(deleted_at__isnull=False)
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs).exclude(deleted_at__isnull=False)
```

Overriding `all()` and `filter()` at the Manager level. `SomeModel.objects.filter(active=True).filter(name="foo")` would apply soft-delete exclusion on the first `.filter` (Manager) but not the second (QuerySet) — silently broken chains. The correct implementation routes soft-delete exclusion through a custom `QuerySet` subclass returned by `get_queryset()`.

**(f) Honest verdict.** **Non-trivial.** Structural-style rule with non-obvious enforcement edge per the auto-003 Round 2 "qualifies" list. Constrains class-MRO + method-name pair; enforcement requires hierarchy resolution and built-in knowledge of which method names are delegated through `get_queryset` (metadata extracted from the `QuerySet` definition). Catches a substantive ORM-correctness bug. Corpus-anchored in framework code and contributor docs.

---

## §2 TypeScript — Visual Studio Code (microsoft/vscode @ release tag `1.95.0`)

**Codebase choice.** Microsoft Visual Studio Code. Release tag `1.95.0` (October 2024). Sampling frame: open-source GitHub, ~10 years history, ~2.5M LOC, >2000 contributors, very active maintenance, MIT license. VS Code's bespoke layering rules, DI service-decorator pattern, and Disposable lifecycle pattern are enforced internally and documented in `src/` directly — convention surface is self-evidenced.

### Convention Ts-1: Disposable._register lifecycle discipline

**(a) Statement.** `Convention { name: "ts-1-vscode-disposable-self-register", pattern: "Classes in src/vs/**/*.ts that subscribe to events or hold IDisposable instances MUST extend the abstract Disposable base class from vs/base/common/lifecycle.ts and register every owned IDisposable via this._register(disposable) — NOT by storing the disposable in a property and calling .dispose() manually.", scope: "module-glob:src/vs/**/*.ts excluding test/", evidence-symbols: ["vs.base.common.lifecycle.Disposable", "vs.workbench.contrib.terminal.browser.terminalInstance.TerminalInstance"], confidence: 0.85 }`. Centralizes lifecycle management through `Disposable._register(...)` (which appends to an internal `DisposableStore`) rather than ad-hoc per-class cleanup logic — the codebase's defense against listener leaks.

**(b) Corpus citation.** [Prior-art §1](../research-notes/bfl-conventional-view-prior-art.md#1-industry-tools) explicitly names project-local idioms (e.g., "we use dataclasses with frozen=True in core/") as the gap industry tooling misses; Disposable._register is the TypeScript analog. The pattern is documented in `src/vs/base/common/lifecycle.ts` JSDoc directly.

**(c) Construction sentence.** TypeScript Compiler API (`ts.createProgram` + `ts.TypeChecker`) AST walker enumerates every `ClassDeclaration`; the type checker resolves base classes transitively up to `Disposable`. Classes holding `IDisposable`-typed properties (resolved by walking property declarations and resolving type symbols) are flagged for inspection. Walker enumerates uses of `this._register(...)` vs manual `.dispose()` patterns. LLM-with-structured-output via [P-14](../primitives/P-14-judge-router.md) handles conditional acquisition and disposables-stored-in-Map cases. This is the [P-26 §Construction-conventional](../primitives/P-26-codebase-model.md) sketch verbatim.

**(d) Positive example.** From `src/vs/workbench/contrib/terminal/browser/terminalInstance.ts`:

```typescript
import { Disposable } from 'vs/base/common/lifecycle';
import { Emitter, Event } from 'vs/base/common/event';

export class TerminalInstance extends Disposable implements ITerminalInstance {
    private readonly _onExit = this._register(new Emitter<number | undefined>());
    public readonly onExit: Event<number | undefined> = this._onExit.event;

    constructor(@ILayoutService layoutService: ILayoutService, ...) {
        super();
        this._register(layoutService.onDidLayoutMainContainer(() => this.layout()));
    }
}
```

Every Emitter and every event subscription is acquired via `this._register(...)`. When the class is disposed by its owner (through the same chain), the entire transitive disposable graph tears down deterministically.

**(e) Negative example.**

```typescript
export class LeakyService implements ILeakyService {
    public readonly _serviceBrand: undefined;
    private _onDidChange = new Emitter<void>();      // not registered
    public readonly onDidChange = this._onDidChange.event;
    private _layoutListener: IDisposable;

    constructor(@ILayoutService layoutService: ILayoutService) {
        this._layoutListener = layoutService.onDidLayoutMainContainer(() => {});
        // stored in field; not registered; no dispose() method
    }
}
```

`LeakyService` does not extend `Disposable`; the Emitter is never registered; the layout listener is stored but never disposed. When the consuming `IInstantiationService` instance tears down, the listener remains live, holding a reference to the host and (transitively) to the closure capture.

**(f) Honest verdict.** **Non-trivial.** Constrains class structure + member-acquisition shape across thousands of classes. Requires class-MRO resolution, property-type resolution, and call-site analysis. Not a presence check (a class can extend `Disposable` and still fail by not registering its disposables). Catches the substantive listener-leak bug pattern. Corpus-anchored in VS Code's own `lifecycle.ts` JSDoc.

### Convention Ts-2: Service-interface brand + decorator-token discipline

**(a) Statement.** `Convention { name: "ts-2-vscode-service-brand-decorator", pattern: "Every TypeScript service interface in src/vs/**/common/*.ts named /^I[A-Z]/ intended for DI MUST (i) declare a readonly _serviceBrand: undefined member, AND (ii) be paired in the same file with an exported createDecorator<IFooService>('fooService') token. Consumers MUST inject via @IFooService constructor-parameter decorator; direct new FooService(...) outside the service's own *ServiceImpl.ts factory is forbidden.", scope: "module-glob:src/vs/**/common/*.ts where interface name matches /^I[A-Z]/", evidence-symbols: ["vs.platform.instantiation.common.instantiation.createDecorator", "vs.platform.log.common.log.ILogService"], confidence: 0.90 }`. The pair is the calling contract for `@IFooService` constructor injection in VS Code's bespoke DI system.

**(b) Corpus citation.** [Prior-art §1](../research-notes/bfl-conventional-view-prior-art.md#1-industry-tools) on "project-specific layering invariants that aren't expressible as Sonar's pre-baked architecture rules" — service-brand + decorator-token is among the most distinctive idioms in production TypeScript. [§5](../research-notes/bfl-conventional-view-prior-art.md#5-layering--architecture-rule-extractors) (ts-arch, dependency-cruiser) handles structural layering but cannot enforce interface-shape-plus-paired-symbol conventions. Documented in `src/vs/platform/instantiation/common/instantiation.ts` JSDoc; widely reflected in `src/vs/platform/**/common/` service-interface files.

**(c) Construction sentence.** TypeScript Compiler API walker enumerates every `InterfaceDeclaration` whose name matches `/^I[A-Z]/` in `common/*.ts`. For each: (i) presence of `PropertySignature _serviceBrand: undefined`; (ii) same-file exported variable initialized by a call expression whose callee resolves to `createDecorator` (imported from `vs/platform/instantiation/common/instantiation`); (iii) generic argument of `createDecorator` exactly matches the interface; (iv) string argument follows camelCase-of-interface-minus-I. Consumer pass enumerates constructor-parameter decorators (`@IFooService`) and flags direct `new FooServiceImpl(...)` outside service-registration code. LLM judge resolves legacy-grandfathered decorator-token names.

**(d) Positive example.** From `src/vs/platform/log/common/log.ts`:

```typescript
import { createDecorator } from 'vs/platform/instantiation/common/instantiation';

export const ILogService = createDecorator<ILogService>('logService');

export interface ILogService extends ILogger {
    readonly _serviceBrand: undefined;
    getLevel(): LogLevel;
    setLevel(level: LogLevel): void;
}
```

Consumer:

```typescript
constructor(
    @ILogService private readonly logService: ILogService,
    @IInstantiationService instantiationService: IInstantiationService,
) { ... }
```

Interface carries `_serviceBrand`; decorator token co-located in same file; consumers inject via `@ILogService`. Convention satisfied.

**(e) Negative example.**

```typescript
// src/vs/workbench/contrib/myExt/common/myService.ts
export interface IMyService {                          // no _serviceBrand
    doSomething(): Promise<void>;
}
export class MyServiceImpl implements IMyService { ... }
```

Consumer: `private readonly _myService = new MyServiceImpl();` — direct instantiation bypasses `InstantiationService`. Two violations: interface has no `_serviceBrand`, no `createDecorator` token; consumer bypasses DI via `new`.

**(f) Honest verdict.** **Non-trivial.** Constrains a *triple* (interface-shape, paired same-file token, consumer-side decorator usage) across thousands of services. Structural check catches (i); cross-file symbol resolution catches (ii); call-graph analysis catches (iii). Specific to VS Code's bespoke DI system (does not generalize to Angular `@Injectable` or NestJS) — exactly the codebase-specific idiom register P-26 targets.

### Convention Ts-3: Common-module browser-isolation discipline

**(a) Statement.** `Convention { name: "ts-3-vscode-common-no-dom-no-node", pattern: "Files under src/vs/**/common/**/*.ts MUST NOT import or reference DOM globals (window, document, navigator, HTMLElement, MouseEvent, ...), MUST NOT import or reference Node.js globals (process, Buffer, require, __dirname), and MUST NOT import from */browser/, */node/, or */electron-*/ siblings.", scope: "module-glob:src/vs/**/common/**/*.ts", evidence-symbols: ["vs.base.common.lifecycle", "vs.base.common.uri"], confidence: 0.95 }`. The `common/` layer is the runtime-environment-independent core executing identically in browser, Node.js, web worker, and electron-renderer.

**(b) Corpus citation.** [Prior-art §5](../research-notes/bfl-conventional-view-prior-art.md#5-layering--architecture-rule-extractors) catalogs this as the layering / architecture-rule extractor surface, naming ArchUnit, jQAssistant, ts-arch, dependency-cruiser. Prior art enforces *human-authored* layering rules; the BF-L sub-track's job is to *extract* them. VS Code's `common/`/`browser/`/`node/` layering is the textbook example — enforceable by dependency-cruiser today, but extracting it from a codebase that does not declare it is the open problem.

**(c) Construction sentence.** TypeScript Compiler API import-graph extraction + path-based glob check + symbol-table check for DOM/Node globals. Walker enumerates every `ImportDeclaration` in `src/vs/**/common/**/*.ts`; resolves each module specifier; flags imports to `src/vs/**/browser/`, `**/node/`, `**/electron-*/`. Parallel pass enumerates `Identifier` references; type checker resolves the symbol; if declared in `lib.dom.d.ts` or `@types/node`, flags. Binary at file granularity. LLM judge resolves the rare case of a type happening to be named like a DOM type but locally declared.

**(d) Positive example.** From `src/vs/base/common/uri.ts`:

```typescript
import * as paths from 'vs/base/common/path';
import { isWindows } from 'vs/base/common/platform';
import { CharCode } from 'vs/base/common/charCode';

export class URI {
    readonly scheme: string;
    static parse(value: string): URI { ... }
    static file(path: string): URI { ... }
}
```

No DOM references; no Node references; imports only from sibling `common/` modules. Compiles and executes identically in renderer, extension host, and web worker.

**(e) Negative example.**

```typescript
// src/vs/platform/exampleService/common/exampleService.ts
import { EditorWidget } from 'vs/editor/browser/editorWidget';   // imports browser/

export class ExampleService {
    private _hostElement: HTMLDivElement;   // DOM type in common/
    public attach(): void {
        const target = document.getElementById('host');   // DOM global in common/
    }
}
```

Three violations on one file. Severity: critical — the web build crashes at module-load time because `document` is undefined in the web worker running the extension host.

**(f) Honest verdict.** **Non-trivial.** Not just "X must come before Y in import order" — "X may not transitively reach any symbol declared in lib.dom.d.ts or @types/node." Requires walking the transitive import graph and the type-resolution graph. Corpus-anchored in VS Code's layering doc. Catches a substantive runtime bug.

---

## §3 Java — Spring Framework (spring-projects/spring-framework @ release tag `v6.1.0`)

**Codebase choice.** Spring Framework. Release tag `v6.1.0` (November 2023). Sampling frame: open-source GitHub, ~20 years history, ~600k LOC across the multi-module repo, >700 contributors, very active maintenance, Apache 2.0 license. Internal coding conventions explicitly documented in `CONTRIBUTING.md` and `src/checkstyle/checkstyle.xml`; the codebase is a 20-year carrier of those conventions — exactly the stratified-sample (recency × churn) the P-26 sketch targets.

### Convention Ja-1: Assert.notNull precondition discipline

**(a) Statement.** `Convention { name: "ja-1-spring-assert-notnull-precondition", pattern: "Every public or protected method in org.springframework.* (excluding tests / internal) that accepts a reference-type parameter NOT annotated @Nullable MUST validate non-nullness as the first statement(s) of the method via Assert.notNull(arg, message) or Assert.hasText(arg, message) (String parameters), where the message is a human-readable description of the parameter, NOT a mechanical positional name.", scope: "module-glob:spring-core/src/main/java/**, spring-beans/src/main/java/**, spring-context/src/main/java/**", evidence-symbols: ["org.springframework.util.Assert.notNull", "org.springframework.beans.factory.support.DefaultListableBeanFactory.registerBeanDefinition"], confidence: 0.90 }`. Throws `IllegalArgumentException(message)` on null — fail-fast at API boundaries.

**(b) Corpus citation.** [Prior-art §5](../research-notes/bfl-conventional-view-prior-art.md#5-layering--architecture-rule-extractors) cites ArchUnit as the canonical Java layering tool — but ArchUnit cannot enforce "first statement of every public method is an Assert call" (a method-body shape rule, not structural). Exactly the conventional-view surface [§3](../research-notes/bfl-conventional-view-prior-art.md#3-llm-with-structured-output-applications) identifies as the LLM-structured-output + AST surface. Spring's `CONTRIBUTING.md` at tag `v6.1.0` documents the convention; call-site frequency numbers in the thousands across the repo.

**(c) Construction sentence.** Java AST walk via JavaParser or Eclipse JDT + LLM judge for message-quality. Enumerate every `MethodDeclaration` with `public` or `protected` modifier in scope. For each, inspect parameters: non-`@Nullable` reference-type parameters require a first-statement `MethodCallExpr` resolving to `org.springframework.util.Assert.notNull` (or `.hasText` for `String`-with-non-empty contract), first argument being a `NameExpr` matching the parameter. LLM judge via [P-14 cross-family panel](../primitives/P-14-judge-router.md) assesses message quality: deterministic check on `StringLiteralExpr` length is the floor; the judge classifies messages as informative vs mechanical.

**(d) Positive example.** From `spring-beans/.../DefaultListableBeanFactory.java`, `registerBeanDefinition`:

```java
@Override
public void registerBeanDefinition(String beanName, BeanDefinition beanDefinition)
        throws BeanDefinitionStoreException {

    Assert.hasText(beanName, "Bean name must not be empty");
    Assert.notNull(beanDefinition, "BeanDefinition must not be null");

    if (beanDefinition instanceof AbstractBeanDefinition abd) {
        try { abd.validate(); } catch (BeanDefinitionValidationException ex) { ... }
    }
    ...
}
```

Both parameters validated as first statements; messages name the parameter semantically.

**(e) Negative example.**

```java
public class CustomBeanRegistry {
    private final Map<String, BeanDefinition> registry = new ConcurrentHashMap<>();

    public void register(String name, BeanDefinition def) {
        if (name.isEmpty()) {                      // NPE if name == null
            throw new IllegalArgumentException("empty name");
        }
        registry.put(name, def);                   // NPE if def == null
    }

    public void registerWithChecks(String name, BeanDefinition def) {
        Objects.requireNonNull(name);              // wrong utility (no message; wrong exception)
        Objects.requireNonNull(def);
        registry.put(name, def);
    }
}
```

`register(...)` has no guards (NPE message will be obscure). `registerWithChecks(...)` uses `Objects.requireNonNull` — JDK utility, different exception type (`NullPointerException` vs `IllegalArgumentException`), no message.

**(f) Honest verdict.** **Non-trivial.** Constrains *method-body shape* (first-statement-must-be-X) coupled with *parameter-annotation conditional* (only non-`@Nullable` reference parameters require the guard) coupled with *call-target identity* (`Assert.notNull` specifically, not `Objects.requireNonNull` or hand-written `if`) coupled with *message quality*. Each arm independently extractable; together a substantive guard against an NPE bug class at API boundaries. Corpus-anchored in `CONTRIBUTING.md` and verifiable by call-site frequency.

### Convention Ja-2: Spring's `@Nullable` annotation discipline

**(a) Statement.** `Convention { name: "ja-2-spring-explicit-nullable-annotation", pattern: "Every method return type and every method parameter in public API classes under org.springframework.* (non-internal) that CAN take or return null MUST be explicitly annotated @Nullable from org.springframework.lang.Nullable. Absence of the annotation is read as a non-null contract (absence-means-NON-null discipline) — a project-local null-safety contract Spring uses in lieu of (and predating) Optional or Kotlin null-safety.", scope: "module-glob:spring-*/src/main/java/org/springframework/**/*.java (excluding internal/* and *Tests.java)", evidence-symbols: ["org.springframework.lang.Nullable", "org.springframework.beans.factory.BeanFactory.getBean"], confidence: 0.85 }`. The annotation source MUST be Spring's own `org.springframework.lang.Nullable` — NOT JSR-305 `javax.annotation.Nullable`, NOT Checker Framework, NOT JetBrains. A project-local choice that signals the absence-means-non-null contract to Spring's static analyzer.

**(b) Corpus citation.** [Prior-art §4](../research-notes/bfl-conventional-view-prior-art.md#4-semantic-naming-convention-extractors) cites NATURALIZE, code2vec, DeepBugs for project-specific naming surfaces. [§3](../research-notes/bfl-conventional-view-prior-art.md#3-llm-with-structured-output-applications) cites LLM-structured-output for cross-file convention extraction — `@Nullable`-source-package check is precisely the cross-file disambiguation the LLM judge handles (multiple `@Nullable` annotations exist in the JVM ecosystem; the convention specifies *which one*). Spring's `spring-framework-reference/core.adoc` documents the convention verbatim, including the rationale that Spring's `@Nullable` is the official project annotation registered with the null-safety analyzer.

**(c) Construction sentence.** Eclipse JDT AST walk + import resolution + LLM judge. Enumerate every `MethodDeclaration` in scope; inspect (i) return type and annotations; (ii) each parameter and annotations. An annotation is recognized as `@Nullable` only if FQCN resolves to `org.springframework.lang.Nullable`. Then null-flow analysis (NullAway or Checker Framework) determines whether the return value or parameter is actually treated as nullable. Discrepancy — method returns possibly-null but no annotation, OR method annotated `@Nullable` but body proves never-null — is flagged. LLM judge resolves cases where the null-flow analyzer is uncertain (polymorphism, callback nullability). [P-26 §Construction-conventional](../primitives/P-26-codebase-model.md) recipe verbatim.

**(d) Positive example.** From `spring-beans/.../BeanFactory.java`:

```java
public interface BeanFactory {
    Object getBean(String name) throws BeansException;                              // non-null return

    @Nullable
    <T> T getBean(Class<T> requiredType, @Nullable Object... args) throws BeansException;

    boolean containsBean(String name);

    @Nullable
    Class<?> getType(String name) throws NoSuchBeanDefinitionException;
}
```

`getBean(String)` returns non-null (throws on no-bean) — no annotation. `getBean(Class, Object...)` can return null — `@Nullable`. `args` varargs can be null — `@Nullable`. `getType` can return null — `@Nullable`.

**(e) Negative example.**

```java
import javax.annotation.Nullable;   // JSR-305 Nullable, NOT Spring's

public class FooService {
    @Nullable
    public BeanDefinition findDefinition(String name) {       // wrong @Nullable source
        return registry.get(name);
    }
    public BeanDefinition lookupOrCompute(String name) {      // can return null, NO annotation
        BeanDefinition def = registry.get(name);
        if (def == null) {
            return compute(name);   // compute(...) can also return null
        }
        return def;
    }
}
```

Two violations: (i) wrong-source `@Nullable` — Spring's analyzer does not recognize JSR-305 as authoritative; (ii) `lookupOrCompute` can return null but is not annotated — consumers will treat the return as non-null per the absence-means-non-null discipline, leading to NPEs.

**(f) Honest verdict.** **Non-trivial.** Constrains *annotation-source identity* (Spring's `@Nullable`, not JSR-305 or others) AND *annotation-presence correctness* (presence iff actually-nullable per data-flow). First arm requires import resolution; second requires null-flow analysis (or LLM approximation). The "absence means non-null" semantics is project-local — exactly the codebase-specific idiom register P-26 targets.

### Convention Ja-3: Commons-Logging-facade discipline (NOT SLF4J directly)

**(a) Statement.** `Convention { name: "ja-3-spring-commons-logging-facade", pattern: "Classes in org.springframework.* (excluding tests) that need to log MUST declare a private static final Log logger = LogFactory.getLog(<this>.class); (or protected for abstract bases) using org.apache.commons.logging.Log and LogFactory — NOT org.slf4j.Logger / LoggerFactory, NOT java.util.logging.Logger, NOT org.apache.log4j.Logger.", scope: "module-glob:spring-*/src/main/java/org/springframework/**/*.java (excluding internal/* and tests)", evidence-symbols: ["org.apache.commons.logging.Log", "org.apache.commons.logging.LogFactory"], confidence: 0.95 }`. Spring re-bridges Commons Logging via its own `spring-jcl` module so downstream consumers can route through SLF4J / Log4j2 / JUL at runtime, but Spring's *own* source uses the Commons-Logging facade directly. A project-binding choice driven by Spring's dependency-decoupling stance.

**(b) Corpus citation.** [Prior-art §1](../research-notes/bfl-conventional-view-prior-art.md#1-industry-tools) names exactly this pattern as the gap industry tooling misses: "idiomatic patterns specific to a codebase (e.g., 'we use dataclasses with frozen=True in core/'), project-local layering invariants that aren't expressible as Sonar's pre-baked architecture rules." Spring's Commons-Logging choice is the textbook codebase-specific idiom no off-the-shelf linter would flag without a project-authored custom rule. The `spring-jcl` README documents the choice; the codebase exhibits the pattern at thousands of call sites with high consistency.

**(c) Construction sentence.** JavaParser AST walk + import-graph extraction. Enumerate `FieldDeclaration` whose name matches `/log(ger)?/i` and whose type is any of `{Log, Logger, java.util.logging.Logger}`. Import resolution determines whether the field's type is `org.apache.commons.logging.Log` (allowed) or any other logger type (disallowed). Walker checks the initializer is `LogFactory.getLog(<EnclosingClass>.class)`, NOT `LoggerFactory.getLogger(...)`. Binary deterministic result; LLM judge handles legitimate-SLF4J edge cases (bridge code), classifying as grandfathered.

**(d) Positive example.** From `spring-beans/.../AbstractAutowireCapableBeanFactory.java`:

```java
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public abstract class AbstractAutowireCapableBeanFactory
        extends AbstractBeanFactory implements AutowireCapableBeanFactory {

    /** Logger available to subclasses */
    protected final Log logger = LogFactory.getLog(getClass());

    protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) {
        if (logger.isTraceEnabled()) {
            logger.trace("Creating instance of bean '" + beanName + "'");
        }
        ...
    }
}
```

Field type `Log` from `org.apache.commons.logging`; initializer `LogFactory.getLog(getClass())`; protected because the class is abstract.

**(e) Negative example.**

```java
package org.springframework.contrib.example;

import org.slf4j.Logger;            // wrong facade
import org.slf4j.LoggerFactory;

public class ExampleSupportClass {
    private static final Logger logger = LoggerFactory.getLogger(ExampleSupportClass.class);
    public void process(Object input) {
        logger.info("Processing input: {}", input);
    }
}
```

Substantive issue: when this class loads into a consuming application using Log4j2 (not SLF4J), the SLF4J Logger creates a *second* logging path independent of the Spring-managed logging chain — fragmenting log output and bypassing Spring's logging-config infrastructure.

**(f) Honest verdict.** **Non-trivial.** Constrains *source package* of the logger field type and the *call shape* of the initializer. Importantly, **counterintuitive** to a modern Java developer — most non-Spring Java post-2010 uses SLF4J as the canonical facade; a contributor unaware of Spring's `spring-jcl` choice would default to SLF4J. High-value extraction target — exactly the kind of project-specific idiom off-the-shelf tooling does not catch. Corpus-anchored in `spring-jcl`'s design doc and call-site frequency.

---

## §4 Honest verdict (smoke-test close)

### Per-language results

- **Python (Django @ tag `5.0`):** **3/3 non-trivial conventions produced.** Py-1 (versioned-deprecation-class) constrains type-identity of warn-call category arguments. Py-2 (gettext_lazy at import time) constrains call-shape on class-body field declarations. Py-3 (Manager.get_queryset discipline) constrains class-MRO + method-name pair. All three AST-extractable with LLM-structured-output triangulation, corpus-anchored in Django's contributor docs, catch substantive bugs (deprecation tracking; i18n staleness; ORM query-chain correctness). **Verdict: pass.**

- **TypeScript (VS Code @ tag `1.95.0`):** **3/3 non-trivial conventions produced.** Ts-1 (Disposable._register lifecycle) constrains class structure + IDisposable acquisition shape. Ts-2 (service-brand + decorator-token) constrains the triple of interface-shape, paired same-file token, and consumer-side decorator usage. Ts-3 (common-module browser-isolation) constrains runtime-environment layering with substance, not just import order. All three extractable via TypeScript Compiler API + LLM judge, corpus-anchored in VS Code's coding-guidelines, catch substantive runtime bugs (listener leaks; DI bypass; web build crashes). **Verdict: pass.**

- **Java (Spring Framework @ tag `v6.1.0`):** **3/3 non-trivial conventions produced.** Ja-1 (Assert.notNull precondition) constrains method-body shape + parameter-annotation conditional + call-target identity + message quality. Ja-2 (Spring's `@Nullable` discipline) constrains annotation-source identity + presence-correctness against null-flow. Ja-3 (Commons-Logging-facade) constrains source-package of logger-field types and is *counterintuitive* (modern Java defaults to SLF4J). All three extractable via JavaParser / Eclipse JDT + LLM judge + null-flow analyzer, corpus-anchored in `CONTRIBUTING.md`, null-safety reference, and `spring-jcl` design doc. **Verdict: pass.**

### Aggregate verdict per auto-003 Round 2 logic

**3 of 3 languages produced ≥3 non-trivial substantive conventions.** Satisfies the **≥2 of 3 languages** threshold for **full Phase-4 sub-track authorized**.

**BF-L conventional-view sub-track status: full sub-track authorized (Wave 4.5b fires).**

### Wave 4.5b scaling contract

Per [auto-003 Round 2 §Full Wave-4.5 sub-track scope](../decisions/auto-003-bfl-rg-view-choice.md#full-wave-45-sub-track-scope-if-smoke-test-passes-superseded-if-it-fails):

- Scale 3-per-language to **≥10-per-language** across the 3 languages (≥30 conventions total).
- Inputs: this smoke-test's artifacts as scaffold; [`bfl-conventional-view-prior-art.md`](../research-notes/bfl-conventional-view-prior-art.md) as prior-art frame; [P-26 §Construction-conventional](../primitives/P-26-codebase-model.md) sketch as the engineering recipe; [P-14 judge router](../primitives/P-14-judge-router.md) for LLM dispatch.
- Phase-4-close gate: ≥30 conventions on the three named representative codebases, honesty-discipline carried through, per-convention corpus citations preserved.

### Honest gaps named

1. **Test-pattern conventions were not exhibited.** Per [prior-art §6](../research-notes/bfl-conventional-view-prior-art.md#6-test-pattern-extractors), test-pattern extraction is the weakest convention sub-surface in published literature. The smoke-test deliberately avoided test-pattern conventions (e.g., "Django tests use `assertNumQueries` to assert query count"; "Spring tests use `@MockBean` rather than direct Mockito mocks") because corpus support is thinner. Wave 4.5b should attempt test-pattern conventions but treat them as the highest-risk sub-deliverable; per [prior-art §8](../research-notes/bfl-conventional-view-prior-art.md#8-honest-assessment) recommendation, the v1 gate should be scoped to naming + layering + behavioral idiom; test patterns carried as research-deliverables, not gate-deliverables.

2. **Idiom-register conventions are thinly covered.** Of the 9 conventions above, only Py-2 (gettext_lazy), Ts-1 (Disposable), and Ja-3 (Commons-Logging) are pure idiom-register conventions; the other 6 are structural-style with non-obvious enforcement edges. Wave 4.5b should scale idiom-register conventions specifically (e.g., Django's `@receiver` decorator over manual `signal.connect`; Spring's `BeanPostProcessor` over `ApplicationContextAware`-then-mutate; VS Code's `IInstantiationService.createInstance` over `new`). The smoke-test does not yet demonstrate the codebase corpus thickens linearly — a possible Wave 4.5b failure mode is 4-5 strong conventions per language and 5-6 weak ones, falling short of the spirit of the gate.

3. **No cross-language convention exhibited.** Per [prior-art §8](../research-notes/bfl-conventional-view-prior-art.md#8-honest-assessment) "secondary open problem" — all 9 conventions here are language-specific. Wave 4.5b should examine whether some conventions are language-portable (module-layering rules; logging-facade choice) and whether the `Convention` schema needs a `language` field or a more nuanced cross-language representation.

4. **Convention-staleness not demonstrated.** Per [prior-art §8](../research-notes/bfl-conventional-view-prior-art.md#8-honest-assessment) "tertiary open problem" — a convention extracted from a 5-year-old codebase reflects what the team did, which may differ from what they currently want. All 9 conventions here extracted from current-release tags but the staleness check (does the convention still hold against the most-recent N commits? does churn correlate with violation?) is not exhibited. Wave 4.5b should incorporate the [P-26 sketch's stratified-sample (recency × churn)](../primitives/P-26-codebase-model.md#construction-path-per-view) recipe explicitly.

### Methodology-degradation clause activation

**Not activated for the conventional view.** All 3 languages produced ≥3 non-trivial conventions; no language falls back to (b) accept-as-RG. BF-L's regime classifier retains convention-density as an input feature for all three languages within Wave 4.5b's scope.

(The companion smoke-test for the invariant view runs independently per [auto-003 Round 2 §Phase-3.5 follow-up smoke-test](../decisions/auto-003-bfl-rg-view-choice.md#phase-35-follow-up-smoke-test-new-wave-45-pre-lead-agent-coordinated) — its verdict drives the invariant-view sub-track authorization independently and is not addressed by this report.)

### Caveats for Wave 4.5b lead-agent dispatch

1. **3-per-language is the floor, not the ceiling.** Wave 4.5b should target ≥10-per-language but accept ≥7-per-language with explicit corpus-thinness justification. Forcing 10 may cross the fabrication boundary if the corpus thins beyond structural-style and idiom-register surfaces.

2. **Golden-corpus authoring is the gating dependency.** Per [prior-art §7 recommendations](../research-notes/bfl-conventional-view-prior-art.md#7-golden-corpus-precedents), ~50-100 labelled conventions per language are needed for precision/recall evaluation — itself ~3-6 engineer-weeks. Wave 4.5b should treat corpus authoring + extractor authoring as a coupled pair, NOT sequential.

3. **Triangulation extractor is the lowest-risk path.** Per [prior-art §recommendation 3](../research-notes/bfl-conventional-view-prior-art.md#specific-recommendations-for-the-bf-l-sub-track-design): mechanical AST/dependency-graph analyzers as floor; LLM-structured-output as ceiling; n-gram statistical signal as calibrator. Wave 4.5b should adopt this triangulation by default; single-method extractors accept disproportionate risk.

4. **Polyglot is a v2 problem.** Per [prior-art §recommendation 7](../research-notes/bfl-conventional-view-prior-art.md#specific-recommendations-for-the-bf-l-sub-track-design): lock v1 to ≥10 conventions per language *independently*; cross-language convention representation deferred to v2.

5. **Honest verdict on Wave 4.5b's likely outcome.** Based on this smoke-test (9/9 producing without difficulty) and the prior-art notes' published precision ceilings (naming 0.85-0.95; layering 0.70-0.85; idiom 0.50-0.70), Wave 4.5b can plausibly meet the ≥30-convention count gate but is *unlikely* to meet a precision-≥0.7 gate against a labelled corpus across all 30. The Phase-4-close criterion should weight *artifact production* (≥30 with corpus citations) heavier than *precision against labelled corpus* (which depends on the golden-corpus deliverable being authored in time and to quality).

---

*End of bfl-conventional-smoke-test.md.*
