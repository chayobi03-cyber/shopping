# Shopping System Constitution
Version: 1.0.0
Status: APPROVED_BY_POLICY
Effective: 2026-11-09

## Non-negotiable principles
1. User constraints are immutable unless the user explicitly changes them.
2. Product identity precedes enrichment. Never merge similar models, seasons, SKUs, colors, or size charts without evidence.
3. Every decision-critical assertion must link to a source, evidence locator, and observed timestamp.
4. Unknown is not zero. Missing or conflicting evidence remains UNKNOWN, CONFLICT, or DATA_NOT_READY.
5. Source reliability and data quality are separate dimensions.
6. Prices and availability are time-bound observations, never timeless product attributes.
7. Deterministic validation and decision gates are code-owned; LLMs may propose, explain, and investigate but cannot override gates.
8. Recommendation and purchase execution are separate. No checkout, payment, account mutation, or personal-data submission without explicit transaction-specific user approval.
9. Automatic approval applies only to repository artifacts that pass automated quality gates. It never authorizes external purchases or irreversible external actions.
10. Preserve raw evidence metadata, normalized assertions, decisions, and change history independently.
11. Respect source terms, rate limits, copyright, privacy, and access controls. No circumvention.
12. Prefer the simplest architecture that satisfies measured requirements.

## Decision vocabulary
BUY = recommendation gate passed; not a purchase instruction.
WATCH = promising but price, stock, or evidence gate is not met.
REJECT = hard constraint failed or material risk established.
DATA_NOT_READY = evidence insufficient for a defensible decision.
BLOCKED = prohibited or inaccessible operation.

## Quality gate policy
- Missing product identity blocks product-level spec aggregation.
- Missing provenance blocks critical assertions from VERIFIED.
- Listing presence alone cannot establish option-level AVAILABLE.
- Conflicting decision-critical values block BUY.
- Stale price/stock cannot be represented as current.
- Any failed critical test blocks artifact auto-approval.

## Change control
Constitution changes require a version increment, rationale, migration note, and regression review. Existing decisions retain the policy version under which they were produced.
