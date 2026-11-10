# Feature 001 Implementation Plan
Version: 1.0.0

## Design
Implement a lightweight local-first pipeline. No database or live autonomous scraping in MVP. Data is committed as CSV/JSON with immutable observation IDs. External collection is performed only through permitted sources and available connectors/tools.

## Components
1. Request parser → request JSON.
2. Product identity registry → product/variant JSON.
3. Source and evidence registry → CSV/JSON.
4. Offer and availability observations → append-only CSV/JSON.
5. Deterministic validators → Python package.
6. Decision engine → hard gates then transparent ranking.
7. Independent reviewer checklist → separate report.
8. Report generator → Markdown and CSV.
9. Git release → auto-approval only after CI-equivalent checks pass.

## Decision model
- Gate first: gender, size, condition, total price, identity, option stock.
- If any hard gate is FAIL → REJECT.
- If any hard gate is UNKNOWN or stale → DATA_NOT_READY or WATCH, depending on whether a valid product candidate remains.
- Only all PASS candidates can enter BUY recommendation ranking.
- Preference score is a ranking aid, never a gate override.
- Missing values are null/NOT_ASSESSED; never impute for approval.

## Proposed preference weights
Brand/channel trust 15; material/construction 25; price/deal credibility 20; design/versatility 15; review/durability evidence 15; seller/returns 10. Weights sum to 100. Score only assessed dimensions; show coverage and do not renormalize to conceal missing critical evidence.

## Data freshness defaults (configurable)
Price: 24h; stock/option: 2h; review aggregate: 30d; official product specification: 365d or until season/model revision. These are operational defaults, not guarantees. Always display checked_at.

## Implementation order
A. Commit schemas and sample fixtures.
B. Implement schema and deterministic rule tests.
C. Implement validators and decision engine.
D. Add independent review template and adversarial test cases.
E. Generate first pilot report.
F. Review defects and update protocol.
