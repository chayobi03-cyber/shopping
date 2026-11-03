---
name: shopping-field-evidence
description: Use when verifying a product fact or specification such as model number, fill power, fill weight, garment weight, dimensions, material, certification, warranty, or compatibility against source evidence.
---

# Shopping Field Evidence Audit

## Objective

Verify each factual field against evidence that applies to the exact product variant.

## Procedure

1. Identify the exact product and variant before evaluating the field.
2. Determine which source types are authoritative for this particular field.
3. Open the source and inspect the relevant document/page section; do not rely on search snippets as final evidence.
4. Record source_id, source grade/type, URL, evidence locator, retrieved_at, published_at where available, and applicable model/variant scope.
5. Preserve the raw text/value and create a separate normalized assertion.
6. Check units, measurement conditions, size/variant scope, season and market.
7. Compare independent sources. Do not count copied listings as independent corroboration.
8. Record missing evidence, source conflict, stale information, and identity uncertainty separately.
9. Return a field-level status and a concise explanation of why the evidence supports or does not support the claim.

## Hard rules

- A source's A/B/C/D/E grade does not automatically verify a value.
- Source reliability, evidence confidence, and data quality are separate.
- Manufacturer sources are normally preferred for official technical specifications; current stock and price must be checked with the seller.
- A patent is not evidence that a commercial model contains the patented feature.
- User reviews can support experience claims, not replace technical specifications.
- Do not invent numerical values or convert subjective statements into measurements.

## Output contract

Return:
- product_variant_id
- field_key
- raw_value and normalized_value
- unit and scope
- source_id and evidence_id
- source_suitability
- identity_match
- freshness_status
- verification_status: VERIFIED, PARTIALLY_VERIFIED, CONFLICT, UNKNOWN, STALE, or DATA_NOT_READY
- rationale and unresolved evidence

## Skill checks

- Official datasheet with exact model and page locator: strong candidate evidence.
- Search snippet without accessible source text: discovery only, not final verification.
- Conflicting values from two credible sources: CONFLICT pending adjudication.
- Missing fill-weight data: UNKNOWN; never estimate it from garment size or fill power.
