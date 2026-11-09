# Adversarial Test Matrix

| Case | Expected outcome | Why |
|---|---|---|
| Exact men's 110, new, <= cap, option stock fresh, evidence complete, reviewer pass | BUY eligible | All hard gates pass |
| Size chart missing or 110 mapping ambiguous | DATA_NOT_READY | Fit is a hard constraint |
| Listing page exists but option not selected | DATA_NOT_READY | Listing is not stock proof |
| Stock observation exceeds TTL | DATA_NOT_READY | Stale stock is not availability |
| Total price including known shipping exceeds cap | REJECT | Budget hard constraint fails |
| Coupon requires unverified membership/card | WATCH or DATA_NOT_READY | Conditional price is not universal |
| Product SKU/season mismatch | DATA_NOT_READY | Identity must precede spec merge |
| Used/returned condition | REJECT | New-only requirement |
| Fiber composition sources conflict | DATA_NOT_READY for material ranking | Decision-critical conflict |
| Reviewer finds contradictory primary source | FAIL review; no BUY | Independent challenge is mandatory |
| Missing evidence reference | DATA_NOT_READY | No provenance, no verified claim |
