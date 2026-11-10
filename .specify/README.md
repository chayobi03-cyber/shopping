# Spec Kit Adoption Notes

This repository maintains agent-neutral Spec-Driven Development artifacts and an active feature pointer at `.specify/feature.json`.

The production workflow follows the current GitHub Spec Kit full SDD path:
1. Constitution (once per project)
2. Specify
3. Clarify
4. Plan
5. Checklist
6. Tasks
7. Analyze
8. Implement
9. Converge

To install native Spec Kit command/skill files, use the official Specify CLI from the repository root after reviewing the existing branch baseline:
`uv tool install specify-cli`
`specify init --here --integration generic`

Do not use `--force` blindly on this established repository. Review generated-file conflicts before accepting them. Agent commands such as `/speckit-specify` and `/speckit-converge` run inside the chosen coding agent, not as shell commands.
