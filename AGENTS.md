# Repository Agent Instructions

## 1. Entry point and required reading

Before changing this repository, read:

1. \`README.md\`
2. \`docs/agentic/RULEBOOK.md\`
3. \`docs/agentic/SHOPPING_CONSTITUTION.md\`
4. \`AGENT_WORKFLOW.md\`
5. \`docs/agentic/QUALITY_GATES.md\`
6. The relevant domain standards, especially \`PRODUCT_RESEARCH_PROTOCOL.md\`, \`SOURCE_RELIABILITY.md\`, \`SPEC_VERIFICATION.md\`, \`STOCK_MONITORING.md\`, \`EVIDENCE_SCHEMA.md\`, and the applicable architecture/data-governance documents.
7. The active feature brief/specification and its approved plan/tasks, when working on a feature.

Read only the additional standards needed for the task, but never skip the Rulebook or Constitution for a material change.

## 2. Authority and tool independence

- The repository documents are the policy source of truth. A coding agent, model, plugin, CLI, IDE, or workflow engine is only an execution interface.
- No specific coding agent, including Codex, Claude Code, Copilot, or any other product, is mandatory.
- Superpowers and Spec Kit are methodological references. Their principles are expressed as repository rules and artifacts; installing their plugins or CLIs is not a completion requirement.
- Tool-generated instruction files and skill folders are adapters only. They must not create competing or weaker policy.
- When a tool instruction conflicts with repository policy, stop and report the conflict. Do not silently follow the weaker instruction.
- Keep feature intent in one canonical feature record. Do not create a second plan for the same work.

## 3. Non-negotiable product-data rules

- Never combine facts from similar model names, different manufacturer part numbers, seasons, regions, or variants without explicit identity-equivalence evidence.
- Treat GTIN, MPN, manufacturer SKU, OEM part number, and seller SKU as different identifier types with issuer namespaces. Do not assume every product has a GTIN.
- Preserve raw source values and evidence. Store normalized values separately with parser/ruleset versions.
- Every critical product claim must be traceable to the exact source, evidence locator, retrieval time, applicable product identity, and verification status.
- Keep source reliability, evidence confidence, and data quality as separate concepts.
- Never invent missing specifications. Use UNKNOWN, CONFLICT, STALE, BLOCKED, or DATA_NOT_READY as appropriate.
- Never convert title similarity, a search snippet, or a seller listing into proof of model identity or an official specification.
- Do not infer actual stock from the existence of a product page. Verify the requested color/size option and record the verification method and timestamp.
- Keep price and availability observations time-bounded and seller/variant-specific.
- A failed verification gate cannot be overridden by an aggregate score or another successful field.

## 4. Engineering requirements

- Classify the change before choosing a workflow: documentation-only, defect fix, feature, schema/contract change, or security/source-policy change.
- For deterministic code changes, define acceptance tests before implementation and use Red-Green-Refactor where practical.
- Defect fixes require a reproducible failure or clearly described evidence and a regression test.
- Use deterministic code for identity matching, validation, state transitions, normalization, and release gates. LLMs may discover, extract, summarize, and propose; they do not silently approve critical facts.
- Add regression fixtures for parsing, identity, units, source drift, and conflict cases.
- Do not introduce a new database, queue, crawler framework, browser automation dependency, or orchestration platform without a documented need and decision record.
- Do not parallelize edits to shared schemas, migrations, central contracts, or the same file. Parallelize only independent tasks with stable interfaces.
- Do not claim a test, CI run, plugin installation, CLI initialization, or end-to-end verification occurred without direct evidence.

## 5. Data governance and security

- Review source terms, API policy, licensing, privacy, and retention before automating collection.
- robots.txt is not a substitute for permission, copyright, contractual, or privacy review.
- Do not commit API keys, cookies, access tokens, personal data, or restricted source content.
- Do not bypass access controls, authentication, rate limits, CAPTCHAs, or paywalls.
- Use least privilege and avoid placing credentials or private source content in prompts, logs, fixtures, or generated reports.

## 6. Human approval boundaries

Human approval is required before:

- purchasing, paying, ordering, or submitting an order;
- changing source accounts, credentials, or access scopes;
- relaxing a hard validation or quality gate;
- changing product identity, evidence, or decision semantics in a way that weakens a control;
- merging or releasing a material change.

## 7. Completion evidence

A change is complete only when:

- requirements, implementation, and feature artifacts are aligned;
- relevant tests and quality checks have actually run;
- unresolved failures, conflicts, and limitations are reported;
- evidence identifies commands/checks, results, scope, and commit/PR reference;
- a human reviewer can inspect the diff and approve merge.

Use NOT_RUN, NOT_VERIFIED, BLOCKED, or DEFERRED where appropriate. Never infer PASS from missing evidence.
