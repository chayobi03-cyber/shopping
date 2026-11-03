---
name: shopping-product-identity
description: Use when resolving whether product evidence belongs to a specific product or variant, especially similar models, manufacturer part numbers, seasons, markets, colors, sizes, GTINs, MPNs, or seller SKUs.
---

# Shopping Product Identity Verification

## Objective

Resolve product identity without merging similar but distinct products. Return evidence-backed identity status and reasons.

## Procedure

1. Read the applicable Product and ProductVariant schema and category rules.
2. Normalize identifier representation without changing its raw value.
3. Keep identifier type and issuer namespace explicit: GTIN, MPN, manufacturer SKU, seller SKU, OEM part number, and other identifiers are not interchangeable.
4. Compare manufacturer/brand, exact manufacturer part number, season/revision, market, and variant attributes.
5. Use title or image similarity only to discover candidate records. Never use similarity alone to mark identity VERIFIED.
6. Check whether the source evidence explicitly applies to the exact candidate model and variant.
7. Preserve competing credible claims. Do not resolve a conflict by selecting the most recent title, the most popular listing, or the highest similarity score.
8. Return a structured result with identity status, candidate, matched dimensions, mismatched dimensions, evidence references, ruleset version, and rationale.
9. If a critical identifier is absent or the variant cannot be distinguished, use PARTIALLY_VERIFIED, UNKNOWN, or DATA_NOT_READY.
10. If authoritative evidence contradicts the proposed match, use CONFLICT or NO_MATCH and send it for review.

## Hard rules

- Never merge products solely because brand and marketing name match.
- Never assume GTIN exists for every product.
- Never compare SKU values without their issuer and identifier type.
- Never transfer specifications across different seasons, markets, or revisions without explicit equivalence evidence.
- Never overwrite a prior identity decision; create a new decision with supersession and audit metadata.
- Do not fetch pages, inspect stock, or place orders as part of identity resolution.

## Output contract

Return:
- identity_status
- product_id / product_variant_id, if confirmed
- candidate_ids
- identifier_matches
- matched_dimensions
- mismatched_dimensions
- evidence_ids
- ruleset_version
- rationale
- unresolved_questions
- review_required

## Skill checks

- Exact MPN and matching manufacturer: candidate can be VERIFIED when all required dimensions are supported.
- Similar title but different MPN: do not auto-match.
- Same raw identifier text under different issuer/type: do not assume identity.
- Different season or market with no equivalence evidence: keep separate or unresolved.
