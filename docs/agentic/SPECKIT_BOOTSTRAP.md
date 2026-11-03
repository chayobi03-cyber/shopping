# Method Reference: Spec Kit and Superpowers (Documentation-only)

> Legacy path retained to avoid breaking existing links. This file is no longer an installation or CLI bootstrap guide.

## 1. Why these references are used

This repository extracts useful process ideas from two upstream projects:

- **Spec Kit**: define the problem and acceptance contract before implementation; maintain a Constitution; create specification, plan, and tasks artifacts; analyze consistency; implement; and assess convergence.
- **Superpowers**: brainstorm before unclear work, use test-first implementation, debug through evidence and root-cause analysis, request independent review, and verify before completion.

These concepts are translated into local Markdown policies. Their original command names, plugins, integrations, and generated file layouts are not required.

## 2. Canonical documents

- \`docs/agentic/RULEBOOK.md\` — overall operating model and policy authority.
- \`docs/agentic/SHOPPING_CONSTITUTION.md\` — project invariants.
- \`AGENT_WORKFLOW.md\` — workflow stages and artifact ownership.
- \`docs/agentic/QUALITY_GATES.md\` — acceptance and enforcement gates.
- \`docs/agentic/TOOL_INDEPENDENCE.md\` — agent/tool independence.
- Domain standards in the repository root — product identity, evidence, source policy, stock, data quality, and schema.

## 3. Feature artifacts

For a material feature, maintain one canonical feature record under \`specs/<feature-id>/\`:

- \`FEATURE_BRIEF.md\` (optional intake brief)
- \`spec.md\` (approved requirements and acceptance criteria)
- \`plan.md\` (technical approach and decisions)
- \`tasks.md\` (dependency-aware implementation work)
- \`acceptance.md\` or a checklist (observable acceptance tests)

Do not create parallel planning documents for the same feature. The agent may help draft artifacts, but the human remains responsible for approving scope and consequential decisions.

## 4. Process mapping

| Local stage | Spec Kit concept | Superpowers concept |
|---|---|---|
| Explore intent and trade-offs | Input to Specify | Brainstorming |
| Define requirements and acceptance | Specify / Clarify | Design review |
| Define architecture | Plan | Review assumptions and alternatives |
| Decompose work | Tasks | Writing/executing plans |
| Check cross-document consistency | Analyze / Checklist | Pre-implementation review |
| Implement | Implement | TDD, bounded task execution |
| Investigate failure | Bug triage / revised tasks | Systematic debugging |
| Assess remaining gaps | Converge | Verification before completion |
| Inspect and release | Human review | Requesting/receiving review; branch completion |

## 5. Important semantics

- A feature specification is not a prompt transcript; it is the approved contract.
- A plan is not a second competing specification.
- Tests must map to acceptance criteria or explicit quality requirements.
- Analysis identifies gaps; it does not silently approve them.
- Convergence assesses implementation against approved intent. It must not rewrite intent to excuse incomplete implementation.
- A discovery that changes behavior or scope must be reflected in the feature artifacts and reviewed.
- Completion is based on inspectable evidence, not a model's claim.

## 6. Upstream references

- Superpowers: https://github.com/obra/superpowers
- Spec Kit: https://github.com/github/spec-kit
- Spec Kit quickstart: https://github.github.com/spec-kit/quickstart.html
- Spec Kit Agentic SDD reference: https://github.github.com/spec-kit/reference/agentic-sdd.html

The local Rulebook may adapt, narrow, or extend these practices to satisfy Shopping-specific requirements. Upstream updates do not automatically change local policy.
