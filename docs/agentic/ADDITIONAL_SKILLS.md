# Recommended Agent Skills for Shopping

## 1. Skill strategy

Use a small skill set with clear activation conditions. Skills should perform bounded, repeatable work and return structured evidence. Do not install every available skill or activate multiple overlapping workflows for every task.

The primary workflow remains:
- Spec Kit: requirement/specification authority.
- Superpowers: engineering execution discipline.
- Project-local Shopping skills: domain-specific research and data-quality controls.
- Humanizer: optional prose cleanup only.

## 2. Core Superpowers skills

| Skill | Priority | Trigger | Expected value |
|---|---|---|---|
| using-superpowers | Required | Every coding-agent session involving engineering work | Skill discovery and workflow discipline |
| brainstorming | High | New feature or unclear requirement | Scope and tradeoff clarification |
| test-driven-development | Required for code | Deterministic logic or parser implementation | Regression prevention |
| systematic-debugging | Required for non-trivial defects | Unexpected behavior or failing tests | Root-cause diagnosis |
| verification-before-completion | Required | Before declaring implementation complete | Evidence-backed completion |
| requesting-code-review | High | Before merge or after material implementation slice | Independent review |
| receiving-code-review | High | When review feedback arrives | Evidence-based response |
| using-git-worktrees | High | Parallel or isolated feature work | Change isolation |
| subagent-driven-development | Conditional | Multiple independent tasks with stable contracts | Parallel execution and review |
| dispatching-parallel-agents | Conditional | Independent research or code tasks | Controlled parallelism |
| writing-plans | Conditional | Only when no Spec Kit plan exists | Avoid duplicate planning artifacts |
| finishing-a-development-branch | High | When the feature is ready | Test, diff and merge/PR decision |

## 3. Spec Kit quality-gate skills

For production work, use the full process:

- constitution: once per project and on approved policy changes;
- specify: every bounded feature;
- clarify: material ambiguity or missing acceptance criteria;
- plan: architecture and implementation approach;
- checklist: requirement and risk completeness;
- tasks: dependency-aware task breakdown;
- analyze: cross-artifact consistency before implementation;
- implement: execute approved tasks;
- converge: compare code and artifacts, then record remaining work.

A trivial documentation typo does not require the full sequence.

## 4. Project-local Shopping skills

These are recommended custom skills mirrored in .agents/skills (Codex) and .claude/skills (Claude Code). Keep both copies identical when updating them. They complement rather than replace Spec Kit or Superpowers.

| Skill | Trigger | Output |
|---|---|---|
| shopping-product-identity | Resolve a model, manufacturer part number, season, market, or variant | Identity status, identifier matches, evidence links, unresolved ambiguity |
| shopping-field-evidence | Verify a product specification or factual claim | Field-level source assessment, locator, retrieval time, confidence rationale |
| shopping-spec-normalization | Normalize product measurements, dimensions, materials, units, or technical properties | Raw and normalized values, unit conversion, scope, validation status |
| shopping-stock-options | Verify seller, color, size, price, and current orderability | Variant-specific availability observation and checked_at |
| shopping-data-quality | Audit a candidate set or dataset before comparison/release | Completeness, conflict, validity, uniqueness, integrity, freshness and provenance report |
| shopping-agent-evaluation | Change prompts, LLM agents, identity/evidence/stock behavior, or thresholds | Gold-set evaluation, false-positive rate, regression report, release recommendation |
| shopping-source-policy | Add or automate a source | Terms/license/privacy/rate-limit review and ACTIVE/BLOCKED decision |

## 5. Optional external skills/tools

### Humanizer

Use only for final prose such as buyer-facing comparison reports, help text, and README explanations. Never apply it to source values, specifications, numeric values, URLs, identifiers, citations, schemas, tests, policies, or generated machine-readable output.

### Security review

Add a dedicated security review skill/workflow when the repository introduces API credentials, authentication, external data transfer, storage of customer information, or automated web collection. The review should cover secrets, least privilege, input validation, dependency risk, logging, source permissions, privacy and retention.

### Browser automation

Use a Playwright-oriented skill only when a permitted source cannot be reliably inspected through an API, feed, PDF, or static page. Browser automation does not confer permission to bypass controls, and it must not purchase, submit orders, or store authenticated session data without explicit authorization.

### Data-quality validation

A Pandera/Great Expectations-style validation workflow can be introduced when the project has real structured datasets and repeatable pipeline runs. Do not add the dependency before the initial schema and representative test fixtures exist.

## 6. Skill acceptance tests

Before trusting a skill in the workflow, test it with at least one positive and one negative case. Examples:

- identity: exact manufacturer part number matches; similar title with a different season must not auto-match;
- evidence: official manual with page locator is accepted as a strong source; search snippet alone is rejected as final evidence;
- normalization: down fill weight and total garment weight remain separate fields;
- stock: product page exists but size 110 option is sold out; result must be UNAVAILABLE, not AVAILABLE;
- data quality: an expired stock observation becomes STALE; unresolved specification conflict blocks verified status;
- source policy: robots is allowed but terms prohibit automated reuse; collection must be BLOCKED pending review.

## 7. Adoption priority

1. Superpowers core skills and Spec Kit production quality gates.
2. shopping-product-identity, shopping-field-evidence and shopping-stock-options.
3. shopping-spec-normalization and shopping-data-quality.
4. shopping-source-policy and optional security review.
5. Humanizer only for approved human-facing prose.
