# Shopping Agentic Engineering Rulebook

**Version:** 1.0.0  
**Status:** Proposed; human review required before merge  
**Scope:** All people, AI assistants, coding agents, scripts, and automation contributing to this repository

## 1. Purpose

This Rulebook converts useful Superpowers and Spec Kit methods into durable repository rules. It is designed to work without Codex, without a Spec Kit CLI, without a Superpowers plugin, and without any particular coding-agent product.

The goal is not to reproduce upstream tools. The goal is to preserve their useful engineering discipline in inspectable Markdown documents that remain valid when tools change.

## 2. Authority hierarchy

When instructions conflict, apply this order:

1. Applicable law, platform/source terms, privacy/security obligations, and explicit human safety boundaries.
2. The Shopping Constitution.
3. Domain standards and schemas for the affected subject (identity, evidence, source policy, stock, data quality, and architecture).
4. The approved feature specification and acceptance criteria.
5. The approved implementation plan and task breakdown.
6. This workflow and quality-gate documentation.
7. Tool defaults, agent-generated suggestions, prompts, and convenience instructions.

A lower-level instruction cannot waive a higher-level requirement. If two authoritative documents conflict, stop, identify the exact conflict, and request a reviewed resolution. Do not choose the weaker rule silently.

## 3. Three policy layers

### A. Constitution layer — what must never be weakened casually

The Constitution defines stable invariants: identity before enrichment, evidence before claims, field-level verification, provenance preservation, visible uncertainty, deterministic critical logic, source-policy compliance, human approval boundaries, smallest sufficient architecture, and evidence-backed completion.

Constitution changes require a rationale, impact analysis, and human approval.

### B. Workflow layer — how work is performed

The workflow adapts the following concepts:

- Superpowers: brainstorming, TDD, systematic debugging, independent review, and verification before completion.
- Spec Kit: specify, clarify, plan, checklist, tasks, analyze, implement, and converge.

These are process stages, not software dependencies or required command names. See [AGENT_WORKFLOW.md](../../AGENT_WORKFLOW.md).

### C. Enforcement layer — how compliance is demonstrated

Quality gates define testable acceptance conditions, regression checks, data-quality checks, source-policy controls, review requirements, and completion evidence. Automate a gate when a deterministic check is feasible; keep human approval for consequential decisions.

See [QUALITY_GATES.md](QUALITY_GATES.md).

## 4. Single source of truth

- Project policy lives in this Rulebook, the Constitution, and the relevant domain standards.
- Feature intent lives in one canonical feature record under \`specs/<feature-id>/\`.
- The approved \`spec.md\` defines what must be built and how success is judged.
- The approved \`plan.md\` defines how the change is intended to be implemented.
- The approved \`tasks.md\` defines dependency-aware units of work.
- Tests express acceptance criteria and quality requirements.
- Tool-specific instruction files, plugins, prompts, and skill folders are adapters. They do not own policy.

Do not create competing plans or specifications for the same feature. If approved intent changes, update the canonical artifacts and review the change.

## 5. Required work discipline

### Before work

- Classify the change.
- Inspect repository baseline, relevant policies, existing behavior, and tests.
- State the outcome, scope, non-goals, assumptions, and unresolved questions.
- For material features, create or update the canonical feature artifacts before implementation.

### During work

- Use brainstorming when the goal or trade-offs are unclear.
- Resolve ambiguity before encoding it into code.
- Select the smallest sufficient architecture.
- Write tests before deterministic implementation where practical.
- Debug through reproducible evidence and root-cause analysis.
- Keep changes small, reviewable, and traceable to tasks.
- Parallelize only independent work with stable contracts and explicit ownership.

### Before completion

- Run relevant tests and quality checks.
- Inspect the complete diff.
- Compare implementation against specification, plan, tasks, and acceptance criteria.
- Obtain independent review for material changes.
- Report exactly what ran, what passed, what failed, what was blocked, and what remains unverified.
- Obtain human approval before consequential actions and merge/release.

See [QUALITY_GATES.md](QUALITY_GATES.md) for PASS conditions.

## 6. Product-data hard rules

1. Establish exact product identity before attaching specifications, certifications, reviews, offers, or availability.
2. Do not merge products solely because names, images, or marketing descriptions look similar.
3. Keep identifier type and issuer namespace; MPN, GTIN, manufacturer SKU, OEM part number, and seller SKU are not interchangeable.
4. Verify claims per field and per applicable variant.
5. Preserve raw evidence separately from normalized values.
6. Separate source reliability, evidence confidence, data accuracy, and freshness.
7. Preserve credible conflicts; do not average them or select a winner without a defined rule.
8. Never infer unknown specifications or actual orderability.
9. Keep price/stock observations tied to seller, exact option, market, and checked_at.
10. A failed hard gate cannot be overridden by a score, majority vote, or model confidence.

The detailed data rules remain in the domain standards; this summary does not replace them.

## 7. Status semantics

Do not mix the status of a product-data assertion with the status of an engineering task.

| Domain | Status examples | Meaning |
|---|---|---|
| Product data | VERIFIED, PARTIALLY_VERIFIED, UNKNOWN, CONFLICT, STALE, BLOCKED, DATA_NOT_READY | What is known about the evidence or data |
| Availability | AVAILABLE, UNAVAILABLE, UNVERIFIED, UNKNOWN | Orderability for a specific seller/variant/time |
| Work execution | NOT_STARTED, IN_PROGRESS, NOT_RUN, PASS, FAIL, NOT_VERIFIED, BLOCKED, DEFERRED | What was done and checked |

Never infer PASS from absence of an error message or missing test evidence. Never present NOT_RUN as PASS. Never turn DATA_NOT_READY into a recommendation.

## 8. Human approval boundaries

Human approval is required before:

- purchase, payment, order submission, or any checkout action;
- changing credentials, source accounts, permissions, or scopes;
- weakening validation, identity, freshness, or source-policy gates;
- materially changing product identity or evidence semantics;
- merging or releasing material repository changes.

An agent may prepare the evidence and recommendation, but it cannot self-approve these actions.

## 9. Tool independence

No agent product is mandatory. Use the repository documents through any interface that can read and edit the files, including a manual Git workflow. Tool evaluation must consider privacy, data retention, permissions, cost, reproducibility, and portability.

The exact policy is in [TOOL_INDEPENDENCE.md](TOOL_INDEPENDENCE.md).

## 10. Governance and exceptions

- The Rulebook is versioned with the repository.
- Amendments require the proposed change, rationale, affected rules, compatibility/impact analysis, and human review.
- Any temporary exception must state the affected rule, scope, reason, owner/approver, expiry date, and compensating control.
- An exception cannot be used to bypass law, privacy, access restrictions, or user approval.
- Upstream changes to Superpowers or Spec Kit do not automatically amend this Rulebook.
