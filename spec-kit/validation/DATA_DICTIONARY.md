# Data Dictionary — MVP

## Product variant
- product_variant_id: stable internal ID for one exact model/season/option identity.
- manufacturer_sku: maker-issued model identifier; null when not published.
- size_label: seller/manufacturer's original option label.
- size_system: explicit size system such as KR or INTL; never inferred from XXL.
- size_chart_evidence_ref: evidence backing any equivalence mapping.
- fiber_composition_json: original fiber percentages by garment component where disclosed.

## Offer
- sale_price: observed item price in KRW, before separately represented shipping.
- shipping_cost: mandatory shipping charge; null means unknown, not free.
- price_conditions: coupon/member/card conditions, each described separately.
- checked_at: time the price was observed.

## Availability
- selected_options_json: exact color and size option actually selected.
- verification_method: evidence method; listing_only cannot establish AVAILABLE.
- checked_at / ttl_seconds: time-bounded availability observation.

## Evidence
- raw_value: source wording or raw structured value.
- normalized_value: normalized value without deleting the raw value.
- locator: page, section, table, API field, or DOM selector identifying the claim.
- product_identity_match: whether the evidence applies to the exact product variant.

## General rules
- Money uses integer KRW in CSV/JSON exports; SQL, if later added, must use DECIMAL/integer types, never binary float.
- Unknown values are blank/null with a separate verification state.
- CSV files are UTF-8; JSON-in-CSV columns use compact JSON strings.
- Every observation is append-only and includes its own ID and timestamp.
