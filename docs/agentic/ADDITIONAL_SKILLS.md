# Agent Methods and Optional Skill Adapters

## 1. Purpose

This catalog records the engineering practices adopted by the Shopping Rulebook and the optional ways an AI agent may operationalize them.

**The practices are mandatory where their trigger conditions apply. Installing a plugin or skill package is not mandatory.** The repository documents remain authoritative even when no coding-agent integration is available.

## 2. Superpowers-derived practices

| Practice | Trigger | Required behavior |
|---|---|---|
| Brainstorming | New feature or materially unclear requirement | Explore intent, constraints, trade-offs, non-goals, and failure cases before committing to a design |
| Test-driven development | Deterministic logic, parsers, validators, and bug fixes | Demonstrate a failing test, implement the smallest passing change, then refactor |
| Systematic debugging | Unexpected behavior or failed checks | Reproduce, gather evidence, isolate root cause, fix, and verify |
| Verification before completion | Before declaring material work complete | Run relevant checks and report exact evidence and limitations |
| Requesting/receiving review | Material implementation slices and before merge | Obtain independent review; answer findings using evidence |
| Worktree/isolation discipline | Parallel or risky feature work | Isolate changes and preserve explicit ownership |
| Subagent/parallel execution | Only when tasks are independent and interfaces are stable | Split bounded work, review each result, and integrate deliberately |
| Branch completion | Feature completion | Inspect tests, diff, outstanding risks, PR, and human merge decision |

The upstream Superpowers library is a reference for these methods, not a runtime dependency:
https://github.com/obra/superpowers

## 3. Spec Kit-derived specification practices

For material features, use the following artifact lifecycle:

1. Constitution — project-wide invariants, maintained through reviewed amendments.
2. Specify — user problem, desired outcome, functional requirements, constraints, and acceptance criteria.
3. Clarify — unresolved ambiguity that can change behavior, scope, risk, or acceptance.
4. Plan — architecture, interfaces, dependencies, data contracts, and risks.
5. Checklist — requirement and risk completeness.
6. Tasks — small, ordered, dependency-aware work units.
7. Analyze — consistency across Constitution, spec, plan, tasks, standards, and architecture.
8. Implement — execute approved tasks with test-first discipline.
9. Converge — compare implementation and evidence against the approved artifacts; record remaining gaps.

These are workflow stages, not required commands. The canonical Markdown artifacts remain usable without the Spec Kit CLI or an installed agent plugin.

Upstream references:
- https://github.com/github/spec-kit
- https://github.github.com/spec-kit/quickstart.html
- https://github.github.com/spec-kit/reference/agentic-sdd.html

## 4. Shopping domain skill catalog

Seven project-specific skill definitions are present under \`.agents/skills/\` and \`.claude/skills/\` as optional agent-facing adapters. They are not the policy source of truth. Their authoritative requirements live in the Rulebook and domain standards.

| Skill | Trigger | Expected output |
|---|---|---|
| shopping-product-identity | Resolve model, manufacturer part number, season, market, or variant | Identity status, identifier matches, evidence links, unresolved ambiguity |
| shopping-field-evidence | Verify a specification or factual claim | Field-level source assessment, locator, retrieval time, confidence rationale |
| shopping-spec-normalization | Normalize measurements, dimensions, materials, units, or technical properties | Raw and normalized values, conversion, scope, validation status |
| shopping-stock-options | Verify seller, color, size, price, and current orderability | Variant-specific availability observation and checked_at |
| shopping-data-quality | Audit candidates or datasets before comparison/release | Completeness, conflict, validity, uniqueness, integrity, freshness, provenance |
| shopping-agent-evaluation | Change prompts, LLM agents, identity/evidence/stock behavior, or thresholds | Gold-set evaluation, false-positive rate, regression report, release recommendation |
| shopping-source-policy | Add or automate a source | Terms/license/privacy/rate-limit review and ACTIVE/BLOCKED decision |

When an adapter copy is changed, compare its mirrored counterpart. Never let a tool-specific skill weaken the canonical rule.

## 5. Optional integrations

A team may install an agent, plugin, CLI, browser automation package, or data-quality library only when there is a concrete need and an approved setup decision. Record the chosen product, version, permissions, cost, owner, and verification evidence. Do not add a dependency merely because an upstream method mentions it.

Examples:
- Humanizer: optional final prose cleanup only. Never apply it to facts, numbers, units, identifiers, URLs, citations, schemas, tests, or legal wording.
- Browser automation: only for permitted sources when simpler access methods are insufficient. It does not grant permission to bypass controls or submit purchases.
- Pandera/Great Expectations-style validation: consider only after real structured datasets and representative fixtures exist.
- Security review: required when adding credentials, authentication, external data transfer, customer information, or automated collection.

## 6. Acceptance tests for the domain practices

Before trusting an automated adapter, test at least one positive and one negative case:

- Identity: exact manufacturer part number matches; similar title with a different season must not auto-match.
- Evidence: official document with a page locator is strong field evidence; a search snippet alone is not final evidence.
- Normalization: down fill weight and total garment weight remain separate fields.
- Stock: product page exists but requested size is sold out; result must not be AVAILABLE.
- Data quality: expired stock observation becomes STALE; unresolved specification conflict prevents VERIFIED.
- Source policy: a source that prohibits the intended automated reuse is BLOCKED pending review.

## 7. Adoption rule

Adopt practices, not vendor lock-in. A future agent may use these methods through native instructions, repository files, prompt templates, automation, or manual checklists. The acceptance criteria do not change with the selected tool.
