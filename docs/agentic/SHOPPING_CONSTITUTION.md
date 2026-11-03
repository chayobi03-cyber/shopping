# Shopping Project Constitution

**Status:** Proposed baseline for Spec Kit adoption  
**Version:** 1.0.0  
**Effective date:** Upon approval and installation into .specify/memory/constitution.md

This document is the source text for the project's Spec Kit Constitution. During bootstrap, initialize Spec Kit first, then create or update the generated Constitution from these principles and review the generated diff.

## Principle 1 — Identity Before Enrichment

A product identity must be established before specifications, certifications, reviews, or offers are attached. Brand, manufacturer model number, season, market, color, size, and variant boundaries must be preserved where they affect identity. Similar names or images are candidate-discovery signals, not proof of identity.

## Principle 2 — Evidence Before Claims

Every critical product claim must have traceable evidence. Record source identity, source type/grade, URL or document locator, retrieval time, applicable product variant, raw value, normalized value, and verification status. Search snippets and unattributed reposts are discovery hints only.

## Principle 3 — Field-Level Verification

Verification is performed per field and per product variant, not only at whole-product level. Source reliability, evidence confidence, and data quality are separate dimensions. A high source grade does not automatically make a claim correct, current, or applicable to the exact variant.

## Principle 4 — Preserve Raw Evidence and Provenance

Raw payloads and original values must not be overwritten by normalized output. Persist hashes and parser/ruleset versions where applicable. Corrected observations supersede earlier observations through explicit relationships and audit history.

## Principle 5 — Uncertainty Must Remain Visible

Never invent missing data. Use UNKNOWN for unavailable knowledge, CONFLICT for incompatible credible evidence, STALE for expired freshness, BLOCKED for policy/access restrictions, and DATA_NOT_READY when required inputs are insufficient. Hard-gate failures cannot be cancelled by averaging or aggregate confidence scores.

## Principle 6 — Time-Bound Commercial Data

Prices and availability are observations tied to a seller, offer, exact option, market, and checked_at timestamp. Product-page existence is not stock evidence. Previous stock-outs do not permanently exclude a candidate; subsequent research must recheck the exact option.

## Principle 7 — Deterministic Critical Logic

Product matching, identifier comparison, unit normalization, validation, quality gates, and state transitions must be deterministic and testable. LLMs may assist discovery, extraction, explanation, and triage, but may not silently promote unverified facts or override hard gates.

## Principle 8 — Test Before Implementation

For code changes, define acceptance tests before implementation and use Red-Green-Refactor where practical. Parser and source changes require regression fixtures. Defect fixes require a reproducible failure or clearly described evidence. A passing test suite does not prove factual correctness without a representative gold set.

## Principle 9 — Source Policy and Privacy by Design

Use permitted APIs, feeds, documents, and web access. Review terms, licenses, rate limits, copyright, privacy, and retention before automated collection. robots.txt alone is not legal permission. Never bypass authentication, access controls, CAPTCHAs, rate limits, or paywalls. Keep secrets and personal data out of the repository and logs.

## Principle 10 — Human Approval for Consequential Actions

Human approval is required before purchases, payments, order submissions, credential/scope changes, hard-gate relaxation, and merge/release changes affecting identity or decision semantics. Agents must report evidence and uncertainty so a human can make an informed decision.

## Principle 11 — Smallest Sufficient Architecture

Start with the smallest maintainable implementation that satisfies the feature contract. Add new services, databases, queues, crawlers, browser automation, orchestration platforms, or paid APIs only when an explicit requirement and decision record justify them.

## Principle 12 — Verifiable Completion

A completion claim must be supported by inspectable evidence: changed files, test commands and results, quality checks, known limitations, and commit/PR references. A task is not complete merely because code was generated or an agent says it is complete.

## Governance

- Constitution amendments require a rationale, impact review, and human approval.
- Any exception must identify the affected principle, scope, reason, expiry/review date, and approver.
- No feature plan may weaken these principles by omission.
- If requirements conflict with a principle, stop and surface the conflict rather than silently choosing a weaker interpretation.
