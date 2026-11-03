---
name: shopping-stock-options
description: Use when checking whether a particular seller currently sells a specific product option such as color and size, including orderability, price, shipping, and stock freshness.
---

# Shopping Seller and Variant Stock Verification

## Objective

Verify purchase availability for the exact seller offer and option, with explicit time and method.

## Procedure

1. Confirm product identity and seller offer separately.
2. Identify the exact market, seller, condition (new/used), color, size, and option code.
3. Inspect the option selector and current seller status using an allowed source access method.
4. Where permitted and without submitting an order, confirm that the selected option can proceed to the cart/order-information stage.
5. Record price, discounts, shipping, taxes/import costs where known, and checked_at separately.
6. Record the exact verification method and evidence locator.
7. Apply the source/category-specific TTL. Mark expired observations STALE and recheck before claiming current availability.
8. Retain previously sold-out candidates in the search pool for future refreshes.

## Availability states

- AVAILABLE: exact requested option is selectable and current orderability evidence exists.
- LOW_STOCK: seller explicitly reports low stock for the exact option.
- SOLD_OUT: exact option explicitly unavailable.
- OPTION_MISSING: seller listing exists but the requested option is not offered.
- PREORDER / BACKORDER: seller permits an order under those explicit terms.
- UNVERIFIED: listing exists but exact option/orderability cannot be established.
- UNKNOWN: no reliable availability evidence.

## Hard rules

- Product page existence is not proof of inventory.
- A different size or color does not prove requested-option availability.
- Search snippets and cached stock labels are not current stock proof.
- Do not log in, bypass CAPTCHA, bypass access controls, or evade rate limits.
- Do not add an item to a paid order, submit checkout, purchase, or reserve without user approval.
- A prior SOLD_OUT result never permanently excludes the candidate.

## Output contract

Return:
- product_variant_id and offer_id
- seller and market
- requested color/size/condition
- displayed price, shipping and known taxes
- availability state
- checked_at and TTL
- verification method
- evidence_id / URL
- unresolved questions and next check

## Skill checks

- Listing exists but size 110 is sold out: SOLD_OUT, not AVAILABLE.
- Size 110 can be selected but orderability cannot be checked: UNVERIFIED.
- A sold-out item appears in a later recheck: create a new observation; do not erase the prior state.
