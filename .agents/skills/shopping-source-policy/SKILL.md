---
name: shopping-source-policy
description: Use before adding a new product data source, automating collection, storing source content, extracting reviews, using an external AI service, or redistributing collected data.
---

# Shopping Source Policy Review

## Objective

Determine whether a proposed source and collection method fit documented legal, contractual, privacy, security, and operational constraints.

## Procedure

1. Identify the source operator, data owner, target fields, and collection purpose.
2. Locate official API/feed documentation, terms, license, robots policy, rate limits, and data-retention rules.
3. Distinguish access permission from permission to store, process, or redistribute content.
4. Identify personal data, review/user content, credentials, cookies, and any sensitive content.
5. Assess source-specific access method, request rate, retries, and impact on the source.
6. Identify data residency, external AI processing, retention, and deletion implications.
7. Record evidence and unresolved legal/contractual questions.
8. Return ACTIVE only when required conditions are established; otherwise return BLOCKED or NEEDS_REVIEW.

## Hard rules

- robots.txt is not legal permission and does not override terms or licenses.
- Publicly accessible content is not automatically available for unrestricted copying or redistribution.
- Do not bypass authentication, CAPTCHAs, paywalls, rate limits, or technical access restrictions.
- Do not collect personal or sensitive information unless the purpose, legal basis, and controls have been specifically approved.
- Do not place API keys, session cookies, or personal information in code, repository files, or logs.
- This skill does not provide legal advice; ambiguous or high-risk cases must be escalated.

## Output contract

Return:
- source identity and owner
- target fields and purpose
- collection method
- terms/license/API/robots evidence
- rate-limit and retention rules
- privacy/security risks
- storage/redistribution permission status
- decision: ACTIVE, BLOCKED, or NEEDS_REVIEW
- open issues, evidence, reviewer, and review date

## Skill checks

- robots permits crawling but terms prohibit automated reuse: BLOCKED pending review.
- API permits querying but not bulk redistribution: limit use to the permitted purpose.
- Reviews include user handles and personal details: do not ingest raw records by default.
