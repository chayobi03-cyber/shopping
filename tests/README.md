# Test Strategy

## Test layers
1. Schema contract tests: reject missing required fields, invalid enums, malformed timestamps, and unknown keys.
2. Unit tests: hard-gate decision logic, price arithmetic, freshness, size evidence, and identity matching.
3. Regression tests: captured permitted fixtures for source parser behavior.
4. Adversarial tests: near-duplicate model, size 110 absent, listing-only stock, stale price, conditional coupon, used item, and source conflict.
5. Independent review: reviewer recomputes gates from structured records and evidence references.

## MVP execution
Run `python -m pytest -q` after installing pytest. Schema validation tests use the optional `jsonschema` package; runtime decision rules must remain deterministic and must not depend on LLM output.

## Release requirement
No claim of passing tests unless the command output is captured in CI or a reproducible local run report. CI should run on pull requests and main-branch updates.
