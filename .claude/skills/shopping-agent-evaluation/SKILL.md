---
name: shopping-agent-evaluation
description: Use when changing product-research prompts, LLM agents, identity matching, evidence extraction, conflict handling, stock verification, or any agent behavior that can assert product facts.
---

# Shopping Agent Evaluation

## Objective

Measure whether product-research agents produce correct, evidence-grounded outcomes on a manually adjudicated evaluation set. Do not rely on fluent explanations or LLM-as-judge scores as the sole proof of correctness.

## Procedure

1. Define the evaluation unit: product, variant, field assertion, seller offer, or stock observation.
2. Build a versioned gold set with manually adjudicated expected identity, fields, statuses, source references, and timestamps.
3. Include hard negatives and adversarial cases: similar titles, wrong MPN, different seasons, identifier namespace collisions, missing data, copied seller pages, conflicting sources, stale prices, and sold-out requested sizes.
4. Separate development, validation, and holdout sets. Do not tune prompts and thresholds on the holdout set.
5. Run deterministic tests for parsers, normalization, state transitions, and hard gates before evaluating model behavior.
6. Evaluate agent outputs against gold labels and evidence references.
7. Report false-positive rates separately from coverage/recall. False VERIFIED and false AVAILABLE are critical errors.
8. Compare each prompt/model/ruleset version to the prior baseline using the same dataset and evaluation policy.
9. Store run metadata, raw outputs, failures, and adjudication notes.
10. Require human review for any proposed change to critical thresholds or acceptance criteria.

## Required metrics

- Identity precision and false identity-match rate
- False VERIFIED rate for critical specification fields
- Evidence provenance coverage
- Unsupported-claim rate
- Conflict detection precision/recall
- Normalization accuracy by field/unit
- False AVAILABLE rate for seller options
- Stock/price freshness SLA compliance
- Required-field coverage, with missingness reported separately
- Human adjudication disagreement rate

Each metric must include numerator, denominator, sample size, data split, and evaluation timestamp. Accuracy cannot be reported without a labeled gold set.

## Hard rules

- Do not use an LLM judge as the sole ground truth for factual correctness.
- Never merge a different manufacturer part number, season, market, or variant because the response sounds plausible.
- A false VERIFIED or false AVAILABLE result must be recorded as a critical failure.
- Do not hide failures inside a composite score.
- Do not compare runs made on materially different datasets without labeling the difference.
- Do not claim regression-free behavior unless the same baseline and holdout sets were run.
- Do not relax product-data hard gates merely to improve aggregate coverage.

## Output contract

Return:
- evaluation_run_id
- agent/model/prompt/ruleset versions
- dataset and split identifiers
- sample size and timestamp
- metric definitions and raw counts
- critical false-positive examples
- regression/improvement vs baseline
- unresolved errors and severity
- human review requirement
- release recommendation: PASS, WARN, FAIL, or DATA_NOT_READY

## Skill checks

- Similar model title with wrong MPN is a hard negative; any VERIFIED match is a critical failure.
- Manufacturer does not publish fill weight; agent invents a value; count as unsupported claim and false VERIFIED.
- Listing exists but requested size is sold out; AVAILABLE is a critical failure.
- No gold set exists; report accuracy as NOT_MEASURED, not as a guessed percentage.
