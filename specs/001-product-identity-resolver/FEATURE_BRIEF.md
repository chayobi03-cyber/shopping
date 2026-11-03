# Feature Brief: Product Identity Resolver

**Status:** Input brief for Spec Kit; not yet an approved implementation specification  
**Feature ID:** 001-product-identity-resolver  
**Priority:** P0 — data integrity foundation

## Problem

The shopping research workflow may encounter products with similar marketing names, reused model labels, different manufacturer part numbers, different seasons, regional variants, or color/size variants. If evidence from these products is merged, downstream specifications, offers, and purchase decisions can be wrong even when each source page is individually credible.

## Desired outcome

Create a deterministic Product Identity Resolver that determines whether a collected evidence item belongs to a known Product or ProductVariant. It must preserve ambiguity and conflict rather than guessing.

## User story

As a product researcher, I need each specification, certification, review aggregate, offer, and stock observation to be attached only to the correct product or variant, so that comparisons and purchase decisions do not mix data from similar but different products.

## Inputs

- Brand/manufacturer
- Manufacturer model name
- Manufacturer model number / MPN, when available
- Identifier type and issuer namespace (GTIN, manufacturer SKU, seller SKU, OEM part number, etc.)
- Season or revision, when applicable
- Market/region, when applicable
- Color code and size/variant attributes, when applicable
- Source and evidence references
- Raw title or description as a discovery hint only

## Required behavior

1. Identifier types must remain distinct; an unqualified SKU string must not be treated as globally unique.
2. Exact issuer-scoped identifiers and manufacturer identity take precedence over title similarity.
3. Season, market, revision, and variant mismatches must remain explicit and must not be silently merged.
4. Title/image similarity may suggest candidates but cannot by itself promote an identity to VERIFIED.
5. Every identity decision must include matched attributes, rejected attributes, evidence references, and a reason.
6. A credible but incompatible identity claim must return CONFLICT or a review-required result; missing evidence must return UNKNOWN or DATA_NOT_READY.
7. The resolver must be deterministic for the same input, ruleset version, and reference dataset.
8. The resolver must not fetch sources or decide stock; those are separate services.
9. Manual adjudication must preserve reviewer, timestamp, reason, and the prior decision.
10. No downstream assertion may be treated as VERIFIED when its product identity is unresolved.

## Status vocabulary

- VERIFIED: exact identity supported by sufficient matching evidence.
- PARTIALLY_VERIFIED: likely candidate, but one or more critical identity dimensions remain unverified.
- CONFLICT: credible evidence points to incompatible products/variants.
- UNKNOWN: insufficient evidence to identify a candidate.
- DATA_NOT_READY: a required identity input or reference dataset is unavailable.
- NO_MATCH: no candidate meets the deterministic matching rules.

## Acceptance criteria

- Given the same manufacturer and exact manufacturer model number, the resolver returns the same matching product when all applicable variant dimensions agree.
- Given a different manufacturer model number, the resolver does not auto-match solely because titles are similar.
- Given two season-specific variants, the resolver keeps them separate unless an authoritative source explicitly establishes equivalence.
- Given identical identifier text with different identifier types or issuers, the resolver does not assume equivalence.
- Given no GTIN, the resolver can still identify a product using other authoritative identifiers and evidence.
- Given conflicting manufacturer and seller claims, the resolver returns a conflict/review state and provides both evidence references.
- Given incomplete size/color/region information where it is required to distinguish variants, the resolver does not mark the variant VERIFIED.
- Every result includes ruleset version and an auditable rationale.
- Tests cover exact match, near match, identifier collision, season mismatch, market mismatch, variant mismatch, missing fields, and conflicting sources.

## Out of scope

- Web crawling or seller-page collection
- Product recommendation/ranking
- Price and stock availability verification
- LLM-only identity decisions
- Automatic merging of unresolved entities
- Purchase, cart submission, or checkout

## Constraints

- Align with SYSTEM_ARCHITECTURE.md and EVIDENCE_SCHEMA.md.
- Keep raw identifiers and raw source values immutable.
- Preserve the source and evidence provenance for all decisions.
- Do not assume the repository already has a code runtime or database; the Spec Kit plan must state the proposed initial implementation and dependencies explicitly.
