# Rulebook Adoption and Verification Status

## 1. Current policy

The repository adopts Superpowers and Spec Kit as **methodological references expressed in tool-independent Markdown rules**.

- No Codex CLI installation is required.
- No Spec Kit CLI installation is required.
- No Superpowers plugin installation is required.
- No specific coding-agent product is required.
- GitHub Codespaces is an optional development environment, not an agent runtime requirement.

## 2. Documentation status

| Item | Repository status | Runtime status |
|---|---|---|
| Shopping Constitution | Proposed policy document | Human review/merge pending |
| Rulebook | Proposed canonical operating policy | Applies after approved merge |
| Agent workflow | Documented as tool-independent stages | Can be followed manually or by any agent |
| Quality gates | Documented acceptance and verification controls | Automated enforcement not yet implemented unless separately evidenced |
| Superpowers methods | Practices adapted into workflow documentation | Plugin not installed or required |
| Spec Kit methods | Artifact lifecycle adapted into workflow documentation | CLI not installed or required |
| Shopping domain skills | Seven definitions present in two agent-facing directories | Discovery/invocation depends on the selected agent and is not required |
| Codespaces environment | Devcontainer and mobile guide committed | Codespace creation/runtime not verified |

## 3. Verification record

| Check | Result |
|---|---|
| Repository documents read from PR branch | PASS — read-back completed |
| Seven Shopping skill mirrors | PASS — previously compared byte-for-byte |
| Rulebook document changes | PENDING — verify after commit |
| Markdown links and terminology | PENDING — verify after commit |
| Tests | NOT_RUN — documentation/configuration-only change |
| CI | NOT_RUN — no CI evidence collected in this task |
| Codespaces startup | NOT_VERIFIED |
| Agent/plugin installation | NOT_REQUIRED |

A repository file existing does not prove that a tool is installed, active, or able to discover it. Conversely, the documented practices can be used without installing a tool.

## 4. Optional future tool record

Only fill this section if a tool is deliberately adopted later:

| Field | Value |
|---|---|
| Tool / agent | NOT_SELECTED |
| Version / revision | NOT_RECORDED |
| Owner / environment | NOT_RECORDED |
| Permissions / scopes | NOT_RECORDED |
| Install date | NOT_RECORDED |
| Verification command and result | NOT_RUN |
| Review / expiry date | NOT_RECORDED |
