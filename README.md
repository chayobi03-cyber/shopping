# Shopping Research System

제품 탐색을 단순 검색 결과 나열이 아닌, **재현 가능한 근거 기반 조사·검증·구매 가능성 판정**으로 수행하기 위한 표준 저장소입니다.

## 목표

- 제품 모델·품번·시즌·변형을 정확히 식별한다.
- 핵심 사양과 판매 정보의 출처 및 신뢰도를 분리해 기록한다.
- 판매 페이지 존재와 실제 구매 가능 재고를 구분한다.
- 확인되지 않은 값은 추정하지 않고 UNKNOWN 또는 DATA_NOT_READY로 남긴다.
- 데이터 수집, 검증, 품질 측정, 배포 절차를 재현 가능하게 관리한다.

## Documentation map

### Research and verification standards

1. [PRODUCT_RESEARCH_PROTOCOL.md](PRODUCT_RESEARCH_PROTOCOL.md) — 조사 범위와 절차
2. [SOURCE_RELIABILITY.md](SOURCE_RELIABILITY.md) — 출처 신뢰도 및 필드별 근거 평가
3. [SPEC_VERIFICATION.md](SPEC_VERIFICATION.md) — 모델·사양 검증
4. [STOCK_MONITORING.md](STOCK_MONITORING.md) — 옵션별 구매 가능성 확인
5. [EVIDENCE_SCHEMA.md](EVIDENCE_SCHEMA.md) — 제품·사양·출처·재고 데이터 구조

### System and data operations

6. [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) — 전체 시스템 구조와 에이전트/서비스 책임
7. [DATA_SOURCE_CATALOG.md](DATA_SOURCE_CATALOG.md) — 제조사·인증·유통·리뷰 출처 카탈로그
8. [DATA_QUALITY_FRAMEWORK.md](DATA_QUALITY_FRAMEWORK.md) — 데이터 품질 7대 차원과 KPI
9. [ETL_PIPELINE.md](ETL_PIPELINE.md) — 수집·정제·검증·적재 파이프라인
10. [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md) — 저작권·개인정보·약관·보안 통제
11. [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) — 단계별 구현 계획과 비용 산식
12. [TOOL_EVALUATION.md](TOOL_EVALUATION.md) — 도구 후보 및 선정 기준

## End-to-end workflow

Requirement → Product Identity → Source Discovery → Evidence Collection → Normalization → Verification → Quality Evaluation → Comparison → Human Approval → Report

## 기본 원칙

- 모델명, 품번, 시즌이 일치하지 않는 자료를 합쳐 하나의 사양으로 만들지 않는다.
- 제조사 공식 자료와 판매자 설명을 동일한 수준의 근거로 취급하지 않는다.
- 출처의 신뢰도와 데이터 자체의 정확성·최신성은 별도로 평가한다.
- 필파워, 다운 충전량, 완제품 중량, 총장, 충전재 종류는 별도 항목이다.
- 미확인 정보는 추정하지 않고 상태를 명시한다.
- 가격·재고는 변동 정보이므로 판매처·옵션·확인 시각을 함께 기록한다.
- 과거 품절은 영구 제외 사유가 아니다. 재검색 시 후보를 다시 확인한다.
- 원본 evidence와 정규화/판정 결과를 분리해 이력을 보존한다.
- 구매·결제 등 외부 효과가 있는 행동은 사용자의 명시적 승인 없이 실행하지 않는다.

## Common status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | 명시된 기준과 근거로 확인 완료 |
| PARTIALLY_VERIFIED | 일부 필드 또는 범위만 확인 |
| CONFLICT | 유효한 출처 간 정보 충돌 |
| UNKNOWN | 확인 가능한 정보가 없음 |
| DATA_NOT_READY | 판단에 필요한 핵심 데이터 부족 |
| STALE | 정해진 최신성 기준 초과 |
| BLOCKED | 정책·권한·접근 제한으로 수행하지 않음 |
| AVAILABLE | 특정 시점·판매처·옵션에서 구매 가능 확인 |
| UNAVAILABLE | 특정 시점·판매처·옵션에서 구매 불가 확인 |

## Initial implementation direction

- Python 기반 모듈형 source adapters
- PostgreSQL 기반 제품·변형·근거·오퍼 메타데이터
- 파일/객체 저장소 기반 raw evidence 보존
- Pydantic 또는 JSON Schema 기반 데이터 계약 검증
- pytest 기반 parser/adapter regression tests
- Markdown/CSV/JSON 기반 초기 결과 배포

대규모 orchestration, 분산 처리, 상용 PIM은 실제 규모와 운영 요건이 확인된 뒤 도입한다.

## Scope

이 저장소는 제품 정보 조사·검증 시스템의 표준과 구현 설계를 관리한다. 특정 판매처의 재고나 가격을 영구적으로 보증하지 않으며, 수집 방식은 각 출처의 권한·약관·법적 조건을 확인한 범위에서만 사용한다.
