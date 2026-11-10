# Changelog

## 2026-11-09 — v1.0.0
- Added hybrid Superpowers × Spec Kit operating model.
- Selected automatic approval for repository artifacts after deterministic and independent quality gates.
- Selected Git + CSV/JSON as the persistence baseline; deferred database infrastructure.
- Added apparel value-hunt pilot specification for men's 110, new condition, <= KRW 40,000.
- Preserved the rule that auto-approval never authorizes purchases or external transactions.


## 2026-11-10 — Phase 2 deterministic shopping engine
- Added product-specific size equivalence checks; never assume XXL means KR 110.
- Added total payable price gate including shipping and mandatory extra costs.
- Added a separate discount-baseline credibility assessment; seller list prices alone do not substantiate genuine discounts.
- Added price/stock freshness checks and option-level availability proof requirements.
- Added evidence coverage checks scoped to exact product variants and required fields.
- Added gender, condition, product identity, and independent-review integrity gates.
- Added structured run-manifest and review schemas, CSV templates, freshness policy, specialist agent prompts, and Spec Kit SDD scaffolding.
- Expanded pytest and JSON Schema contract tests; latest execution evidence remains pending.


### Phase 2 additional hardening — 2026-11-10
- Added evidence-bearing typed hard-gate objects; plain PASS strings and untyped values cannot authorize BUY.
- Added explicit price freshness gate, mandatory-cost unknown state, and same-variant discount baseline verification.
- Added configured freshness-policy evaluation including clock-skew tolerance.
- Added manifest finalization, schema-validated immutable JSON output, append-only CSV observation writer, and immutable Markdown report writer.
- Required every PASS check in independent review records to include evidence references.
- Aligned README and architecture documentation with automatic artifact approval and Git + CSV/JSON persistence.
