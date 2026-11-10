# Phase 2 Implementation Status
As of: 2026-11-10
Branch: feature/hybrid-agentic-spec-kit
PR: https://github.com/chayobi03-cyber/shopping/pull/2

## Selected operating model
- Hybrid orchestration: orchestrator, bounded specialist agents, deterministic validators, independent reviewer.
- Artifact approval: automatic only after complete CI and independent-review gates.
- Data: Git as version control and audit trail; CSV/JSON for registries and immutable observations.
- No database in MVP.
- Purchase execution is explicitly out of scope.

## Implemented
- Superpowers + Spec Kit operating instructions in AGENTS.md.
- Spec Kit active feature pointer, project constitution mirror, templates, clarify record, requirements checklist, and cross-artifact analysis.
- Men's apparel pilot request: cardigan, zip hoodie, knit zip-up; men's KR 110; new condition; total known payable price <= KRW 40,000.
- Specialist agent prompts for identity/source, material/design, price/deal, size/stock, and independent reviewer.
- JSON schemas for request, product, source, evidence, offer, availability, review, run manifest, and decision.
- CSV templates for product, source, evidence, offer, and availability records.
- Deterministic validators for gender, condition, identity, size mapping, total price, discount baseline, freshness, stock proof, evidence coverage, and independent review.
- Decision engine requires all mandatory gates, evidence coverage, and an independently validated reviewer result.
- Test suite for unit behavior, adversarial cases, schema contracts, and policy configuration.
- GitHub Actions workflow configured for PRs, main, and feature branches.

## Important validation semantics
- XXL is not treated as KR 110 without a verified, exact-product size chart.
- Unknown shipping does not become free shipping.
- Price cap uses item price + shipping + known mandatory charges.
- A seller's crossed-out price is not accepted as an established discount baseline without independent supporting evidence.
- Stock requires exact selected size/color, an accepted proof method, evidence reference, and fresh observation.
- Price and stock freshness are separate decision gates.
- Missing, stale, conflicting, or unproven data cannot pass the BUY gate.
- Reviewer run ID must differ from primary run ID; HIGH/CRITICAL findings block positive review.

## Not yet complete
- Automated run-manifest and decision-snapshot writer.
- Report generator.
- Live source-backed apparel pilot data and candidate comparison.
- Independent reviewer execution against current PR diff.
- Latest GitHub Actions result for the most recent commits.

## Test status
Test cases and CI workflow are committed. Earlier commit ae31a21 had a successful GitHub Actions run (6 workflow steps, including deterministic gate tests), but subsequent code and test additions have not yet been confirmed by a newer run. Local execution was blocked because this runtime could not resolve github.com for cloning. Therefore the latest tests are NOT VERIFIED as passing.

## Release status
NOT RELEASE-APPROVED. Do not merge until the latest CI run and independent PR review are confirmed.
