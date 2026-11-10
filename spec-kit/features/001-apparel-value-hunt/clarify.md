# Clarification Record — Feature 001
As of: 2026-11-10

## Resolved
- Target user segment: men's apparel.
- Target size: Korean men's 110.
- International labels such as XXL are not assumed equivalent; they require exact product-specific chart evidence.
- Target maximum: KRW 40,000 total known payable price, including mandatory shipping.
- Unknown shipping means price gate UNKNOWN, not zero.
- Product condition: new.
- Categories: cardigan, zip hoodie, knit zip-up.
- Design is broadly accepted; aesthetics are a preference, not a hard gate.
- Automatic approval is for artifacts after automated and independent checks; it does not authorize purchase transactions.
- Git + CSV/JSON is the MVP persistence model.

## Explicit unknowns retained
- Shipping cannot be assumed free when not published.
- Coupon/card/member discounts are not included unless eligibility and resulting price are evidenced.
- A seller's crossed-out/list price alone is not a verified reference price.
- Material quality beyond published composition and verified construction evidence remains NOT_ASSESSED.
- No current item candidate is promoted from previous chat text alone; revalidate sources before loading a BUY shortlist.
