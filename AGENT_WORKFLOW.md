# Agentic Engineering Workflow

## 1. Purpose and authority

This file defines the repeatable delivery process for this repository.

- The **Rulebook and Constitution** define invariants and decision boundaries.
- The **feature artifacts** define what is being changed and how acceptance will be judged.
- The **domain standards** define product identity, evidence, source, stock, and data-quality requirements.
- Superpowers contributes engineering practices such as brainstorming, TDD, systematic debugging, review, and verification.
- Spec Kit contributes the specification lifecycle: specify, clarify, plan, tasks, analyze, implement, and converge.

These are process concepts, not required software commands. Use the process manually or through any coding agent. Do not assume that a plugin, CLI, or command invocation exists.

## 2. Change classification

Before work begins, classify the request:

| Class | Minimum workflow |
|---|---|
| Typo or isolated documentation correction | Inspect context → edit → link/consistency check |
| Material documentation or policy change | Clarify intent → assess impact/conflicts → edit → independent review |
| Defect fix | Reproduce → regression test → root-cause analysis → fix → verify |
| New feature | Specify → clarify → plan → tasks → analyze → approve → implement → converge → review |
| Schema, identity, evidence, or hard-gate change | Full feature workflow plus explicit human approval and expanded regression coverage |
| New/automated data source | Source-policy review → access/terms/privacy decision → source contract → tests → implementation |

Do not impose the full feature workflow on trivial changes. Do not shortcut the full workflow for material changes.

## 3. Feature delivery workflow

For a production feature, maintain one canonical feature directory under \`specs/\`. The expected artifacts are:

- \`FEATURE_BRIEF.md\`: intake and initial scope, when useful;
- \`spec.md\`: approved problem, users, functional requirements, constraints, and acceptance criteria;
- \`plan.md\`: architecture, interfaces, dependencies, and design decisions;
- \`tasks.md\`: dependency-aware, testable implementation tasks;
- \`acceptance.md\` or a requirements checklist: explicit acceptance tests and release conditions.

Follow these stages in order:

1. **Baseline** — inspect the current branch, base commit, repository instructions, related standards, existing implementation, and tests.
2. **Brainstorm** — when scope, user intent, trade-offs, or boundaries are unclear, explore alternatives and record decisions. Do not convert brainstorming notes into an unapproved commitment.
3. **Specify** — define what must change and why. Keep implementation detail out unless it is a true constraint.
4. **Clarify** — resolve ambiguities that affect behavior, safety, data semantics, scope, or acceptance. Record unresolved issues explicitly.
5. **Plan** — select the smallest architecture that satisfies the approved requirements. Record interfaces, data contracts, dependencies, risks, and rejected alternatives where material.
6. **Decompose** — split the plan into small, dependency-aware tasks with observable completion criteria.
7. **Analyze** — check consistency among the Constitution, domain standards, spec, plan, tasks, tests, and existing architecture. Fix conflicts at their source before implementation.
8. **Human checkpoint** — obtain approval for material scope, architecture, identity semantics, source-policy, or hard-gate decisions before implementation.
9. **Implement** — use test-first development for deterministic behavior. Keep changes small and traceable to tasks.
10. **Converge** — compare the implementation and evidence against the approved spec, plan, tasks, and acceptance criteria. Record every remaining gap as a task or an explicit accepted deferral.
11. **Review and release** — inspect the diff, test evidence, data effects, and limitations. Human approval is required before merge/release.

Do not create a separate implementation plan when \`plan.md\` already exists. Update the canonical artifact when the approved design changes.

### Meaning of convergence

Convergence is an assessment loop, not permission to rewrite requirements to match the code. When implementation does not meet the approved intent, either fix the implementation or explicitly revise the specification through review. Never silently lower acceptance criteria. Repeat implementation and convergence until the agreed scope is complete or remaining work is explicitly deferred and approved.

## 4. Defect workflow

For an existing defect:

1. Capture the observed behavior, expected behavior, environment, inputs, logs, and reproduction steps.
2. Create a failing regression test or equivalent deterministic reproduction evidence before changing the implementation.
3. Trace the root cause rather than patching the visible symptom.
4. Identify the earliest incorrect state or violated contract.
5. Apply the smallest root-cause fix.
6. Add defense-in-depth validation when a single missed invariant could corrupt product identity, evidence, availability, or user decisions.
7. Run the focused regression suite and related broader tests.
8. Confirm that no hard gate, status meaning, or unrelated behavior was weakened.
9. Update domain standards or feature artifacts when the defect reveals a missing or incorrect rule.

A trivial typo does not need a feature spec. A bug that changes a schema, data contract, identity rule, or externally observable decision requires a reviewed specification update.

## 5. Engineering execution practices

### Brainstorming and design

- Ask what outcome is needed before choosing an implementation.
- Separate constraints from preferences.
- Identify non-goals and failure cases.
- Present material trade-offs and recommend the smallest sufficient design.
- Record decisions, assumptions, and unresolved questions in the canonical feature artifact.

### Test-driven development

- Write a test that expresses one requirement or defect.
- Run it and confirm it fails for the intended reason (RED).
- Implement the smallest change that makes it pass (GREEN).
- Refactor while keeping tests green.
- Add boundary, negative, conflict, and regression cases.
- Avoid tests that merely reproduce implementation details or mock away the behavior being tested.

### Systematic debugging

- Do not guess-and-patch.
- Reproduce and gather evidence first.
- Form a falsifiable root-cause hypothesis.
- Instrument or inspect the narrowest relevant boundary.
- Verify the fix against the original failure and neighboring cases.
- If evidence is insufficient, report the blocker instead of claiming a cause.

### Code review

- Review requirement compliance before style.
- Inspect for data loss, identity merges, unsafe defaults, stale values, unhandled conflicts, permission violations, and weakened gates.
- Treat agent-generated claims as hypotheses; inspect code, tests, logs, and source evidence.
- Reviewers should be independent of the implementation where practical.
- Review feedback must be answered with evidence or an explicit, reasoned disagreement. Do not dismiss it by authority.

### Parallel work

Parallelize only independent tasks with stable contracts and explicit file ownership. Use a single writer for shared schemas, enums, migrations, identity rules, source reliability scoring, global instructions, and release gates. Integrate and review each independent result before merging it into the main workstream.

## 6. Feature artifact ownership

- One feature has one canonical \`spec.md\`, \`plan.md\`, and \`tasks.md\`.
- Brainstorming is input to the spec, not a second specification.
- TDD tests map to acceptance criteria or documented quality requirements.
- Review findings become task updates or tracked defects.
- Implementation discoveries that change user-visible behavior must be reflected in the spec before being treated as approved scope.
- Tool-specific generated files are not authoritative unless explicitly adopted and reviewed.

## 7. Evidence and status rules

Every material change records:

- repository, branch, base commit, and changed paths;
- relevant feature artifact and ruleset versions;
- commands/checks actually run and their scope;
- pass/fail counts or exact results;
- data-quality and source-policy findings where applicable;
- unresolved conflicts, limitations, and deferred work;
- final commit and PR references.

Use execution statuses such as NOT_RUN, PASS, FAIL, BLOCKED, NOT_VERIFIED, and DEFERRED. Keep them separate from product-data statuses such as UNKNOWN, CONFLICT, STALE, and DATA_NOT_READY.

## 8. Lightweight path

For a small change that does not alter behavior or policy:

1. Read the relevant instructions and source document.
2. Make the smallest edit.
3. Check links, references, terminology, and formatting affected by the edit.
4. Report exactly what was and was not validated.

No agent skill or CLI invocation is required for this path.
