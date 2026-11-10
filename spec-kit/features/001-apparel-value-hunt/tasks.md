# Feature 001 Tasks
Status: IMPLEMENTATION_IN_PROGRESS
Updated: 2026-11-10

## Completed design and contract work
- [x] T001 Define pilot requirements and hard constraints.
- [x] T002 Define hybrid agent boundaries and approval policy.
- [x] T003 Define Git + CSV/JSON persistence contract.
- [x] T004 Add JSON Schemas for request, product, source, evidence, offer, availability, review, run manifest, and decision.
- [x] T005 Add CSV headers and data dictionary.
- [x] T006 Implement deterministic validators for identity, gender, condition, price, discount baseline, size, freshness, stock, evidence coverage, independent review, and BUY gate.
- [x] T007 Add unit and adversarial test cases for hard constraints and data contracts.
- [x] T008 Add independent reviewer prompt, review protocol, review-record schema, and reviewer-integrity validator.
- [x] T009a Add run-manifest schema and review artifact template.

## Remaining implementation and release work
- [ ] T009b Implement run-manifest writer, immutable decision snapshot writer, and report generator.
- [ ] T010 Re-search live apparel candidates and write first source-verified pilot dataset. Prior conversation product claims must not be promoted without source revalidation.
- [ ] T011 Produce validation report and update changelog with measured test results.
- [ ] T012 Verify GitHub Actions result for the latest branch commit; resolve all failures.
- [ ] T013 Run independent review against the complete PR diff and pilot artifacts.
- [ ] T014 Run Spec Kit convergence check; add tasks for any remaining spec/code gaps.

## Dependency order
T004/T005 → T006 → T007 → T008 → T009a/T009b → T010 → T011/T012 → T013 → T014.

## Definition of done
- All schema/rule tests pass in CI.
- Unknown size, stale price/stock, price above cap, identity mismatch, unverified listing, insufficient evidence, and non-independent review cannot reach BUY.
- Reviewer run is distinct from primary run.
- Report and run manifest are reproducible from versioned inputs and source/evidence IDs.
- Pilot product claims are traceable to field-level source records.
- Current CI and independent review evidence are committed.
