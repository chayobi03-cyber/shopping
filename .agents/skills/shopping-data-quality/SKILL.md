---
name: shopping-data-quality
description: Use when auditing product datasets, shortlisted candidates, specifications, offers, stock observations, evidence coverage, or data quality before comparison or release.
---

# Shopping Product Data Quality Audit

## Objective

Evaluate data readiness at field, variant, and dataset levels. Do not hide hard failures inside a composite score.

## Procedure

1. Confirm dataset scope, snapshot/as-of time, category profile, and ruleset version.
2. Check product identity and variant boundaries.
3. Evaluate the seven dimensions: accuracy, completeness, consistency, validity, uniqueness, integrity, and timeliness.
4. Measure provenance coverage for every critical claim.
5. Calculate metrics with explicit numerator, denominator, sample size, and time window.
6. Check field-specific TTL for price, stock, specifications, certification, and review aggregates.
7. Detect duplicate products/offers, orphan evidence, incompatible units, stale observations, and unresolved source conflicts.
8. Apply hard gates before any ranking or recommendation.
9. Return a structured report with PASS/WARN/FAIL/DATA_NOT_READY and the exact affected records.

## Hard rules

- Null or unsupported values do not count as complete.
- An assertion without required evidence cannot pass provenance.
- A critical identity mismatch blocks downstream verification.
- CONFLICT cannot be hidden by averaging values.
- STALE price/stock cannot be presented as current.
- No gold-set means accuracy is NOT_MEASURED, not 0% and not 100%.
- Every KPI must include denominator, scope, and time window.
- A high overall percentage cannot override a failed critical-field gate.

## Output contract

Return:
- dataset_snapshot and as_of
- category/ruleset version
- metric name, numerator, denominator, result, sample size
- critical missing fields
- identity errors and conflicts
- duplicate/orphan counts
- stale price/stock/specification counts
- gate status and blocked records
- corrective actions and owner

## Skill checks

- Expired stock observation: STALE.
- Conflicting official specifications: CONFLICT and hold critical decision.
- No manually adjudicated gold set: accuracy NOT_MEASURED.
- Required field has a non-null value but no evidence: incomplete for critical completeness.
