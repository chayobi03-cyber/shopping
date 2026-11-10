# Feature 001 — Apparel Value Hunt
Status: APPROVED
Version: 1.0.0
Created: 2026-11-09

## User story
As a shopper, I want to discover high-value new men's apparel from established brands so that I can buy a well-made item at a genuinely discounted price in my required size.

## Current pilot requirements
- Categories: cardigans, zip hoodies, knit zip-ups; extensible to other apparel.
- Gender: men's.
- Required size: KR 110; equivalent labels such as XXL must be verified against brand-specific size charts.
- Maximum target purchase price: KRW 40,000, including mandatory shipping where known.
- Condition: new only.
- Brand priority: established/mainstream brands, including official outlets and authorized sellers.
- Design: broad acceptance; evaluate visual appeal without over-constraining style.
- Quality: fiber composition, fabric construction/weight where published, finish, durability signals, and review patterns.
- Deal quality: compare actual payable price with credible reference price; record coupon/card/member conditions separately.
- Availability: exact size and color option, seller, and checked timestamp.

## Hard constraints
1. Men's product.
2. Size 110 or explicitly verified equivalent.
3. New condition.
4. Total known payable price <= KRW 40,000.
5. Product identity sufficiently verified.
6. Purchase option verified, not merely listing found.

## Preferences
- Established brand / authorized channel.
- Better natural-fiber content or demonstrably durable technical fabric.
- High credible discount and good price-to-quality ratio.
- Attractive, versatile design.
- Reliable seller and favorable review evidence.

## Out of scope
- Used goods.
- Unverified size equivalence.
- Purchase, checkout, payment, or account mutation.
- Treating coupon/card discounts as universal prices.
- Inferring fabric quality from brand name or product photography alone.

## Acceptance criteria
- Every shortlisted item has model/SKU, season if available, seller, URL, size option, price, shipping, and checked_at.
- Fiber composition and size chart are field-level sourced or marked UNKNOWN.
- Reference price and discount calculation disclose source and eligibility.
- Hard constraints are evaluated independently of preference score.
- Any missing hard-constraint evidence prevents BUY.
- Independent reviewer examines all BUY candidates and at least one plausible rejected alternative.
- CSV and JSON outputs validate against committed schemas.
- Report is reproducible from a run manifest and source/evidence IDs.

## Failure states
Identity mismatch, unknown 110 fit, stale stock, unverified final price, conflicting material claims, or inaccessible source must be visible and cannot silently pass.
