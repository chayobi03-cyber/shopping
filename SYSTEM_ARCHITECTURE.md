# Shopping Research System Architecture

## 1. 목적과 설계 원칙

제품 정보 수집·검증·비교·배포 시스템의 논리 아키텍처와 컴포넌트 책임을 정의한다. 제품 카테고리는 확장 가능하게 설계하되 모든 카테고리에 동일한 수집 필드를 강제하지 않는다.

1. Identity before enrichment: 제품 식별이 확정되기 전에 유사 모델의 사양을 합치지 않는다.
2. Evidence before assertion: 중요한 사양·가격·재고 주장은 출처와 관측 시각을 가진다.
3. Field-level quality: 제품 전체가 아니라 필드별로 근거와 품질을 평가한다.
4. Immutable raw evidence: 원본 응답/문서와 수집 메타데이터는 정규화 결과와 분리해 보존한다.
5. Time-aware data: 사양, 가격, 재고, 리뷰는 서로 다른 변경 주기와 유효기간을 가진다.
6. Fail visibly: 불확실하거나 상충하는 데이터는 UNKNOWN, CONFLICT, DATA_NOT_READY로 명시한다.
7. Automatic artifact approval: 버전관리 산출물은 결정론적 테스트와 독립 리뷰를 포함한 모든 품질 게이트 통과 시 자동 승인한다. 구매·결제·계정 변경·개인정보 전송은 별도 명시적 사용자 승인 없이는 실행하지 않는다.

## 2. 논리 아키텍처

~~~mermaid
flowchart LR
  U[Research Request] --> P[Policy and Requirement Parser]
  P --> I[Product Identity Resolver]
  I --> D[Source Discovery]
  D --> C[Source Adapters]
  C --> R[(Raw Evidence Store)]
  R --> N[Parser and Normalizer]
  N --> V[Identity and Spec Verification]
  V --> Q[Data Quality Evaluation]
  Q --> M[(Curated Product Store)]
  M --> S[Comparison and Decision Service]
  S --> IR[Independent Reviewer]
  IR --> G{Deterministic Quality Gates}
  G -->|PASS| AA[Automatic Artifact Approval]
  G -->|FAIL| QH[Quarantine / DATA_NOT_READY]
  AA --> O[Git + CSV/JSON Report / Export]
  O -. transaction only .-> TA[Explicit User Transaction Approval]
  C --> X[Pipeline Observability]
  N --> X
  V --> X
  Q --> X
~~~

## 3. 계층별 책임

| Layer | 책임 | 산출물 |
|---|---|---|
| Request & Policy | 사용자 조건, 필수 조건, 금지 행동, 카테고리 프로파일 정의 | ResearchRequest |
| Identity | 브랜드·모델·품번·GTIN·시즌·변형 옵션 식별 | ProductIdentity |
| Source Discovery | 제품별 공식·인증·유통·리뷰 출처 후보 탐색 | SourcePlan |
| Collection | API, 파일, 허용된 웹 수집, 수동 입력 | RawEvidence |
| Normalization | 단위, 통화, 날짜, 명칭 및 카테고리 표준화 | NormalizedAssertion |
| Verification | 제품 일치, 필드 근거, 교차 출처 충돌 검사 | VerificationResult |
| Quality | 7대 데이터 품질 지표 및 신선도 평가 | QualityReport |
| Decision | 필수 조건 판정, 비교, 추천 후보 구성 | DecisionSnapshot |
| Independent Review | 원본 증거 재확인, 반례 탐색, 게이트 재계산 | ReviewRecord |
| Artifact Release | 모든 품질 게이트 통과 시 산출물 자동 승인 | ReleaseRecord |
| Delivery | Git, CSV/JSON, Markdown 보고서 및 내보내기 | ResearchReport |
| Transaction Boundary | 실제 구매·결제 등 외부 효과의 별도 사용자 승인 | TransactionAuthorization |
| Governance | 권한, 보존, 개인정보, 저작권, 이용약관 준수 | AuditRecord |

## 4. 에이전트/서비스 계약

에이전트는 역할을 분리하되 초기 구현은 일반 Python 서비스로 시작해도 된다. LLM을 사용하더라도 검증 로직과 상태 전이는 결정론적 코드로 유지한다.

| Agent / Service | 입력 | 책임 | 금지 사항 |
|---|---|---|---|
| RequirementParser | 사용자 요청 | 필수·선호·제외 조건 구조화 | 사용자 조건 임의 완화 |
| ProductIdentityAgent | 후보명, 품번, 문서 근거 | 정확한 모델·변형 식별 | 유사한 이름만으로 동일 제품 확정 |
| SourceDiscoveryAgent | ProductIdentity | 필드별 유효 출처 탐색 | 검색 스니펫만 최종 근거로 사용 |
| EvidenceCollector | SourcePlan | 출처별 허용된 방식으로 원본 수집 | 접근제한 우회, 비인가 데이터 취득 |
| NormalizationService | RawEvidence | 값·단위·통화·날짜 정규화 | 원본 값 덮어쓰기 |
| SpecVerificationAgent | Assertion + Evidence | 모델 일치·단위·충돌 검증 | 누락값 추정 |
| StockVerificationAgent | Offer + Variant | 사이즈/색상별 구매 가능 상태 검증 | 상품 페이지 존재만으로 재고 확정 |
| QualityEvaluator | Curated data | 7대 품질 차원 측정 | 낮은 점수를 평균으로 숨김 |
| ComparisonDecisionService | Requirement + Verified data | 필수 조건 판정 및 근거 기반 비교 | 미확인 필수 항목을 PASS 처리 |
| IndependentReviewer | DecisionSnapshot + raw evidence | 주 조사 경로와 분리해 원본 근거 재검증 | 요약문만 보고 승인 |
| ArtifactReleaseController | QualityReport + ReviewRecord + CI result | 모든 릴리스 게이트 통과 시 산출물 자동 승인 | 실패/미실행 테스트를 통과 처리 |
| TransactionApprovalBoundary | 외부 거래 요청 | 별도 사용자 승인 여부 확인 | 산출물 자동 승인을 거래 승인으로 해석 |

## 5. 데이터 저장 계층

### Raw

원본 응답, 허용된 원천 자료, API 요청·응답 메타데이터, 파일 해시, 수집 시각을 저장한다. 원본을 정규화 데이터로 대체하지 않는다.

### Normalized

제품 식별자, 표준 필드명, 표준 단위, 통화, 날짜 형식으로 정규화한 사실 주장(assertion)을 저장한다. 각 assertion은 source/evidence와 연결된다.

### Curated

검증 결과가 반영된 제품·변형·판매 오퍼·인증·리뷰 집계 데이터를 저장한다. 충돌은 별도 상태로 보존한다.

### Decision Snapshot

특정 시점의 사용자 조건, 데이터 버전, 품질 결과, 구매 가능성, 비교 결과를 함께 고정한다. 이후 최신 데이터가 들어와도 과거 판단을 재현할 수 있어야 한다.

## 6. 권장 핵심 엔티티

- Product: 브랜드와 제품군 수준의 논리 제품
- ProductVariant: 모델/품번/시즌/색상/규격 등 실제 변형
- Identifier: GTIN, 제조사 SKU, MPN, 판매자 SKU 등 식별자와 발급 주체
- SpecAssertion: 특정 제품·변형의 특정 필드에 대한 값과 근거
- Source: 출처 레지스트리 및 접근·라이선스 메타데이터
- Evidence: 원본 파일/응답, 해시, 수집 시각, 추출 위치
- Offer: 판매처별 가격·배송·판매 조건
- AvailabilityObservation: 옵션별 재고 관측값과 확인 시각
- Certification: 인증기관·인증번호·적용 모델·유효 상태
- ReviewAggregate: 리뷰 수·평점·기간 등 집계값
- QualityReport: 필드 및 제품 단위 품질 평가
- DecisionSnapshot: 특정 시점의 조건·근거·판정 스냅샷

GTIN은 존재할 때 유용하지만 모든 제품에 반드시 존재하지는 않는다. SKU는 발급 주체 범위 안에서만 유일할 수 있으므로 identifier_type과 issuer를 함께 저장한다.

## 7. 공통 상태 모델

| Status | Meaning |
|---|---|
| VERIFIED | 정해진 검증 기준을 충족 |
| PARTIALLY_VERIFIED | 값은 있으나 식별/범위/근거 일부 미확인 |
| CONFLICT | 유효한 근거들 사이에 상충 존재 |
| UNKNOWN | 확인 가능한 값/근거 없음 |
| DATA_NOT_READY | 현재 데이터로 필수 판단 수행 불가 |
| STALE | 정해진 신선도 기준을 초과 |
| BLOCKED | 정책·권한·접근 제한으로 수행하지 않음 |
| AVAILABLE | 특정 시각·판매처·옵션에서 구매 가능 확인 |
| UNAVAILABLE | 특정 시각·판매처·옵션에서 구매 불가 확인 |

상태는 데이터 유형별로 분리한다. 재고 상태와 사양 검증 상태를 하나의 필드로 합치지 않는다.

## 8. MVP 기술 구성

초기 버전은 단일 애플리케이션과 모듈형 어댑터로 시작한다.

- Runtime: Python
- Schema/validation: JSON Schema
- Versioning/audit: Git
- Structured persistence: CSV observation ledgers + JSON snapshots
- Raw artifacts: 사용 권한이 있는 근거의 URL, locator, retrieval metadata, permitted hash/excerpt only; 전체 원문 저장은 별도 권한 검토
- Collection: 공식 API/피드 우선, 허용된 정적 페이지는 HTTP 파서, 동적 페이지는 필요성과 허용 여부를 확인한 뒤 브라우저 자동화
- Scheduling: 낮은 작업량은 cron 또는 단순 workflow부터 시작
- Testing: pytest + fixture 기반 parser regression test
- Delivery: Markdown/CSV/JSON 리포트와 GitHub 변경 이력
- Database: MVP에서는 사용하지 않음; 필요성이 실측되면 별도 ADR로 SQLite/PostgreSQL 검토

Airflow, Spark, Kafka, 상용 PIM, PostgreSQL 등은 데이터량·동시성·운영 인력이 실제로 요구할 때 도입한다.

## 9. 필수 운영 통제

- 원본과 정규화 결과를 분리하고 모든 변환 버전을 기록한다.
- 수집기는 source별 rate limit, timeout, retry/backoff 정책을 가진다.
- 재시도는 중복 레코드나 중복 오퍼를 만들지 않도록 멱등성을 보장한다.
- 출처 접근 실패와 제품 정보 부재를 구분한다.
- 모든 가격·재고 결과에 checked_at을 저장한다.
- 비밀정보와 개인정보는 로그에 남기지 않는다.
- 품질 게이트를 통과하지 못한 데이터는 추천 결과에서 근거 수준을 낮추거나 제외한다.
- 구매·결제·외부 계정 변경은 명시적인 사용자 승인 없이는 실행하지 않는다.

## 10. 아키텍처 완료 기준

- 모든 핵심 사양이 제품 변형과 evidence/source에 연결된다.
- 모델 식별 실패 시 관련 제품의 사양을 섞지 않는다.
- 상충 데이터가 단일 값으로 조용히 덮어써지지 않는다.
- 가격과 재고에 확인 시각이 존재한다.
- Decision Snapshot으로 과거 결과를 재현할 수 있다.
- 수집 실패, 파싱 실패, 검증 실패를 서로 다른 오류로 관측할 수 있다.
