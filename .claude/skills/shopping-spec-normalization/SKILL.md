---
name: shopping-spec-normalization
description: Use when converting raw product specifications, measurements, dimensions, materials, weights, capacities, electrical ratings, currencies, or category-specific properties into canonical fields and units.
---

# Shopping Specification Normalization

## Objective

Normalize product facts consistently while preserving raw values, measurement context, and category-specific meaning.

## Procedure

1. Confirm the product/variant identity and applicable category profile.
2. Preserve the source's exact raw value and text.
3. Map the fact to a canonical field_key; do not merge semantically different fields.
4. Convert units only when the source unit and conversion rule are known and deterministic.
5. Record normalized value, normalized unit, conversion rule/version, source scope, measurement condition, and applicable variant.
6. Validate range and type against the category schema.
7. Keep missing, ambiguous, or conflicting values explicit.
8. Add tests for unit conversion, precision, invalid values, and category-specific distinction.

## Hard rules

- Never overwrite raw values.
- Never compare measurements with different methods or scopes as if equivalent.
- Keep down fill power, down fill weight, total garment weight, down/feather ratio, and garment length as separate fields.
- Never infer down fill weight from fill power or from total garment weight.
- Never infer garment length class from a marketing label alone; preserve measured length and measurement method.
- Never silently apply rounding that changes ranking or eligibility.
- Currency conversion requires rate source, rate timestamp, and fee/tax treatment.

## Output contract

Return:
- raw_field and raw_value
- canonical_field_key
- normalized_value and unit
- conversion_rule and ruleset_version
- measurement_scope and condition
- source/evidence references
- validation_status
- notes and unresolved questions

## Skill checks

- "800 FP" may normalize to fill_power=800 FP, not to a fill-weight value.
- "Down 300 g" and "whole coat 1.6 kg" remain separate measures.
- Unknown units do not produce fabricated normalized values.
