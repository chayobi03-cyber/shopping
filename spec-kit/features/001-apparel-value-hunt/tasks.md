# Feature 001 Tasks
Status: READY_FOR_IMPLEMENTATION

- [x] T001 Define pilot requirements and hard constraints.
- [x] T002 Define hybrid agent boundaries and approval policy.
- [x] T003 Define Git + CSV/JSON persistence contract.
- [ ] T004 Add JSON Schemas for request, product, evidence, offer, availability, decision.
- [ ] T005 Add CSV headers and data dictionary.
- [ ] T006 Implement deterministic validators for identity, price, size, stock freshness, and BUY gate.
- [ ] T007 Add unit tests and adversarial regression fixtures.
- [ ] T008 Add independent reviewer checklist and report schema.
- [ ] T009 Add report generator and run manifest.
- [ ] T010 Run pilot on current apparel candidates; mark unverifiable prior claims as unverified.
- [ ] T011 Produce validation report and update changelog.

## Dependency order
T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011.

## Definition of done
All schema/rule tests pass; adversarial tests prove unknown size, stale stock, price above cap, identity mismatch, and unverified listing cannot reach BUY; reviewer report exists; output snapshots and changelog are committed.
