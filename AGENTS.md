# Repository Agent Instructions

## Required reading

Before changing this repository, read:

1. README.md
2. AGENT_WORKFLOW.md
3. docs/agentic/SHOPPING_CONSTITUTION.md
4. The relevant standards under SYSTEM_ARCHITECTURE.md, DATA_SOURCE_CATALOG.md, DATA_QUALITY_FRAMEWORK.md, ETL_PIPELINE.md, DATA_GOVERNANCE.md, and EVIDENCE_SCHEMA.md

For feature work, also read the active feature artifacts under specs/.

## Workflow authority

- Spec Kit is the source of truth for feature intent, requirements, technical plan, task breakdown, and convergence status.
- Superpowers supplies the engineering execution practices: brainstorming when scope is unclear, isolated workspaces, TDD, systematic debugging, code review, and verification before completion.
- Do not create a second competing feature plan. When a Spec Kit plan exists, update that plan rather than creating a separate Superpowers plan.
- The active Spec Kit feature is determined by Spec Kit project state, not merely by the checked-out Git branch. Verify the active feature directory before issuing feature commands.
- Use the project-local skills under .agents/skills (Codex) or .claude/skills (Claude Code) when their trigger conditions match. Keep the mirrored shopping-* skill files identical. Do not edit generated Spec Kit or third-party plugin skill files.

## Non-negotiable product-data rules

- Never combine facts from similar model names, different manufacturer part numbers, seasons, regions, or variants without evidence of identity equivalence.
- Treat GTIN, MPN, manufacturer SKU, and seller SKU as different identifier types with issuer namespaces. Do not assume every product has a GTIN.
- Preserve raw source values and evidence. Store normalized values separately with parser/ruleset versions.
- Every critical product claim must be traceable to the exact source, evidence locator, retrieval time, and product-identity match.
- Keep source reliability, evidence confidence, and data quality as separate concepts.
- Never invent missing specifications. Use UNKNOWN, CONFLICT, STALE, or DATA_NOT_READY as appropriate.
- Never convert title similarity, a search snippet, or a seller listing into proof of model identity or official specification.
- Do not infer actual stock from the existence of a product page. Verify the requested color/size option and record the verification method and timestamp.
- Keep price and availability observations time-bounded and seller/variant-specific.
- A failed verification gate cannot be overridden by an aggregate score or by another successful field.

## Engineering requirements

- For code changes, write or update tests before implementation and demonstrate the failing test when practical.
- Use deterministic code for identity matching, validation, state transitions, normalization, and release gates. LLMs may discover, extract, summarize, and propose; they do not silently approve critical facts.
- Add regression fixtures for parsing, identity, units, source drift, and conflict cases.
- Do not introduce a new database, queue, crawler framework, browser automation dependency, or orchestration platform without a documented need and decision record.
- Do not parallelize edits to shared schemas, migrations, central contracts, or the same file. Use subagents only for independent, bounded tasks.
- Do not claim a test, CI run, plugin installation, CLI initialization, or end-to-end verification occurred unless there is direct evidence.

## Data governance

- Review source terms, API policy, licensing, privacy, and retention before automating collection.
- robots.txt is not a substitute for permission, copyright, contractual, or privacy review.
- Do not commit API keys, cookies, access tokens, personal data, or restricted source content.
- Do not bypass access controls, authentication, rate limits, CAPTCHAs, or paywalls.

## Human approval boundaries

Human approval is required before:
- purchasing, paying, ordering, or submitting an order;
- changing source accounts, credentials, or access scopes;
- relaxing a hard validation or quality gate;
- merging or releasing a change that alters product identity, evidence, or decision semantics.

## Completion evidence

A change is complete only when:
- Spec Kit artifacts and implementation are aligned;
- the relevant tests and quality checks have run;
- unresolved failures, conflicts, and limitations are reported;
- evidence includes command, result, timestamp, and commit/PR reference where applicable;
- a human reviewer can inspect the diff and approve merge.
