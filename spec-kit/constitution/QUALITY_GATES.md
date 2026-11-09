# Quality Gates
Version: 1.0.0

| Gate | Checks | Blocking failure |
|---|---|---|
| G0 Requirements | Explicit hard constraints, preference ranking, budget basis | Ambiguous hard constraint |
| G1 Identity | Brand, exact model/SKU, season/variant and option scope | Identity mismatch or unresolved ambiguity |
| G2 Evidence | Source suitability, locator, observed_at, provenance | Critical claim without evidence |
| G3 Normalization | Currency, units, size-system, decimal handling | Invalid or incomparable value |
| G4 Freshness | Field-specific TTL for price and stock | Stale observation presented as current |
| G5 Decision | Hard constraints before weighted preference score | Unknown hard constraint treated as pass |
| G6 Independent review | Separate reviewer checks evidence and counterexamples | Reviewer not independent or unresolved critical defect |
| G7 Release | Tests, schemas, changelog, reproducible snapshot | Any critical test failure |

## Auto-approval
Artifacts may move from DRAFT to VERIFIED to APPROVED only when:
- schema validation passes;
- all required references resolve;
- no critical contradiction remains;
- tests pass;
- reviewer report is present;
- generated outputs are deterministic or timestamped appropriately.

A failed gate results in REVIEW_REQUIRED or DATA_NOT_READY, never forced approval.
