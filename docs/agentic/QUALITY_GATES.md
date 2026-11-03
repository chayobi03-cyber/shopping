# Quality Gates and Completion Evidence

## 1. Purpose

This document defines the gates that prevent unsupported product claims, unsafe code changes, and false completion. Each gate has a required evidence artifact and an explicit failure outcome.

A gate is not passed because an agent says it passed. A person or automation must be able to inspect the evidence.

## 2. Change-intake gates

| Gate | PASS condition | Failure handling |
|---|---|---|
| Scope | Desired outcome, in-scope work, non-goals, and constraints are explicit | CLARIFY_REQUIRED |
| Baseline | Branch, base commit, existing behavior, and relevant standards are known | DATA_NOT_READY |
| Impact | Affected schemas, identity rules, source permissions, data flows, and users are assessed | BLOCKED until assessed |
| Approval | Material scope or hard-gate changes have human approval | BLOCKED |

## 3. Product identity and evidence gates

These gates apply before downstream specifications, reviews, certifications, offers, or stock observations are attached to a product.

| Gate | PASS condition | Failure handling |
|---|---|---|
| Identity | Manufacturer and issuer-scoped identifiers support the exact product/variant match | AMBIGUOUS / CONFLICT / DATA_NOT_READY |
| Variant scope | Season, market, color, size, gender, and revision are resolved where material | PARTIALLY_VERIFIED or DATA_NOT_READY |
| Source authority | Source identity, source grade, and intended claim coverage are understood | BLOCKED or lower evidence grade |
| Field evidence | Each critical field has a source, locator, retrieval time, raw value, and applicable scope | UNKNOWN / DATA_NOT_READY |
| Normalization | Units, definitions, measurement conditions, and parser/ruleset version are explicit | NOT_VERIFIED |
| Conflict handling | Credible conflicting claims remain visible and are not averaged or silently overwritten | CONFLICT |
| Freshness | Evidence and commercial observations are within field-specific freshness policy | STALE |
| Availability | Exact seller, color, size, condition, and orderability are checked at a timestamp | UNVERIFIED / UNAVAILABLE |

A failed identity or evidence gate cannot be offset by a high aggregate score. If a critical field is unverified, the whole comparison must disclose that limitation.

## 4. Engineering quality gates

### Requirements gate

Before implementation, acceptance criteria must be testable, externally observable where possible, and linked to the relevant feature. Material ambiguities, non-goals, error states, and data constraints must be explicit.

### Design gate

The plan must identify affected components, interfaces, data contracts, source permissions, dependencies, failure modes, migration/rollback needs, and the smallest viable architecture. New infrastructure requires a documented justification.

### Test gate

- Deterministic business logic must have automated tests.
- Bug fixes must include a regression test or a documented reason why automation is infeasible.
- Parsers and source adapters must include representative positive, negative, malformed, and changed-source fixtures.
- Identity tests must include hard negatives such as similar titles with different manufacturer part numbers, seasons, or variants.
- Numeric normalization tests must check units, scopes, rounding, and measurement definitions.
- Tests must not pass by mocking away the behavior being verified.
- A test report must identify the command, environment, test selection, result, and failure details.

### Data-quality gate

Use the quality dimensions applicable to the dataset: accuracy, completeness, consistency, validity, uniqueness, integrity, and timeliness. Record numerator/denominator, sample size, ruleset version, and excluded records. Do not turn unmeasured metrics into zero or PASS.

### Source-policy and security gate

Before adding or automating a data source, review terms, permission, API limits, copyright/licensing, privacy, retention, authentication, and logging. A robots.txt check alone is insufficient. Any prohibited or unclear access is BLOCKED pending review.

For credentials and external transfers, use least privilege, secret storage, redacted logs, dependency review, and explicit retention rules.

## 5. Review and release gates

Before merge/release:

- requirements and implementation are aligned;
- relevant automated checks have run, or omissions are explicitly justified;
- the complete diff has been inspected for accidental files, secrets, unsafe defaults, and unrelated changes;
- identity, evidence, data-quality, source-policy, and privacy effects have been reviewed;
- open defects and risks are listed with severity and disposition;
- material review findings are resolved or explicitly accepted by an authorized human;
- no purchase, payment, order, or external irreversible action has been triggered without user approval.

The implementation agent must not be the only source of review evidence for a material change.

## 6. Status model

Keep **product-data status** separate from **work-execution status**.

### Product-data status

- VERIFIED
- PARTIALLY_VERIFIED
- UNKNOWN
- CONFLICT
- STALE
- BLOCKED
- DATA_NOT_READY
- AVAILABLE / UNAVAILABLE (only for time-bounded seller/variant observations)

### Work-execution status

- NOT_STARTED
- IN_PROGRESS
- NOT_RUN
- PASS
- FAIL
- NOT_VERIFIED
- BLOCKED
- DEFERRED

Do not translate UNKNOWN into FAIL, NOT_RUN into PASS, or a product-data status into a CI status.

## 7. Completion evidence record

For a material change, provide:

| Field | Required content |
|---|---|
| Change | Outcome and scope |
| Baseline | Repository, branch, base commit |
| Artifacts | Spec/plan/tasks and policy versions |
| Diff | Changed paths and meaningful behavior |
| Checks | Exact command/check and environment |
| Results | Pass/fail counts, logs, or links |
| Data scope | Dataset/sample/source coverage, if relevant |
| Limitations | NOT_RUN, BLOCKED, conflicts, risks, deferred work |
| Review | Findings and disposition |
| Delivery | Commit SHA and PR URL |

A report that says "tests passed" without command and scope is insufficient. A check that was not run must be labeled NOT_RUN.
