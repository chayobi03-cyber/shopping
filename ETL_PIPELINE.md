# ETL / ELT Pipeline Design

## 1. 목표

제품별 정보 수집을 source adapter 기반으로 모듈화하고 원본 보존부터 검증·배포까지 추적 가능한 파이프라인으로 운영한다.

## 2. End-to-end flow

~~~mermaid
flowchart TD
  A[Schedule or User Request] --> B[Source Policy Check]
  B --> C[Fetch via API / Feed / Permitted Access]
  C --> D[Persist Raw Payload + Metadata]
  D --> E[Parse and Extract]
  E --> F[Normalize Units and Identifiers]
  F --> G[Resolve Product / Variant]
  G --> H[Validate Schema and Business Rules]
  H --> I[Cross-source Verification]
  I --> J[Quality Evaluation]
  J --> K[Curated Store]
  K --> L[Report / Search / Export]
  C --> M[Run Logs and Metrics]
  E --> M
  H --> M
  I --> M
  J --> M
~~~

## 3. Pipeline stages

| Stage | Input | Output | Failure handling |
|---|---|---|---|
| Policy gate | Source registry, planned request | Approved collection plan | BLOCKED, no fetch |
| Extract | API/feed/permitted page | Raw payload | retryable vs permanent failure 분리 |
| Raw persist | Response + metadata | Immutable evidence object | persistence 실패 시 downstream 중지 |
| Parse | Raw payload | Structured fields | parser error + fixture 저장 |
| Normalize | Structured fields | Canonical values | raw value 보존, 변환식 기록 |
| Identity resolve | Identifiers and context | Product/Variant link | ambiguity → review queue |
| Validate | Values and category rules | Validation results | invalid field quarantine |
| Verify | Assertions and evidence | Verified/Conflict states | conflict 유지, 단일값 강제 금지 |
| Quality | Verification data | Quality report | hard gate 실패 시 배포 보류 |
| Load/Publish | Curated records | Search/report/export | versioned snapshot |

## 4. Source adapter contract

각 adapter는 공통 인터페이스를 제공한다.

- source_id: Source Registry의 ID
- fetch(request, context): 허용된 방식으로 payload 취득
- parse(raw_payload): source-specific parser
- normalize(parsed): canonical field mapping
- health_check(): 출처 접근/스키마 상태 확인
- rate_limit_policy: 동시 요청 및 호출 빈도 제어
- terms_reference: 적용 권한·약관 메타데이터

Adapter별 테스트 fixture에 정상 응답, 빈 응답, 오류 응답, 필드 추가/삭제, 잘못된 인코딩 사례를 포함한다.

## 5. 데이터 적재 및 이력

- Raw payload는 수집 시각, source ID, 요청 식별자, HTTP/API 상태(가능한 경우), 파일 해시와 연결한다.
- 정규화 결과는 raw evidence를 참조하고 parser/normalizer 버전을 기록한다.
- 동일 payload 재처리 시 중복 생성이 없도록 idempotency key를 정의한다.
- 기존 assertion을 덮어쓰기보다 새 관측/버전을 추가하고 현재 유효값은 별도 view 또는 계산 결과로 제공한다.
- 삭제·정정은 감사 로그와 변경 사유를 남긴다.

## 6. 스케줄과 재시도

초기에는 작업량에 맞춘 단순 스케줄러로 시작한다. 운영 복잡도, 동시 작업, 의존성, 재처리 요구가 커질 때 전용 오케스트레이터를 검토한다.

- 지수형 backoff와 최대 retry 횟수를 source별로 설정한다.
- 권한/요청 오류를 무조건 재시도하지 않는다.
- rate-limit 응답은 source 정책에 따라 대기한다.
- 타임아웃, DNS, 일시적 서버 오류는 제한적으로 재시도한다.
- 재시도 실패는 DLQ 또는 재처리 큐에 남긴다.
- 실패한 한 source가 다른 독립 source의 정상 수집을 막지 않도록 한다.

## 7. 데이터베이스 및 스토리지 권장안

MVP:

- PostgreSQL: 제품, 변형, assertion, 출처, 오퍼, 재고 관측, 판정 스냅샷
- 파일/객체 저장소: PDF, 원본 응답 등 보존이 허용된 evidence
- JSON/Markdown/CSV: 초기 결과 교환 및 리포트
- DuckDB: 로컬 분석/대량 비교가 필요할 때 보조 활용

확장 조건이 충족될 때 검색 엔진, 데이터 웨어하우스, 메시지 큐, 분산 처리 등을 추가한다.

## 8. 관측성(Observability)

필수 로그/메트릭:

- fetch success/failure, latency, status code
- source별 호출량과 rate-limit 응답
- parser success/failure 및 schema drift
- identity resolution ambiguity
- 검증 통과/충돌/누락 건수
- data freshness 및 stale record 비율
- pipeline run ID, code version, dataset version

알림은 사용자에게 영향을 주는 실패와 내부 재시도성 경고를 구분한다. 비밀키, 세션 쿠키, 개인정보는 로그에 기록하지 않는다.

## 9. 테스트 전략

- Unit test: parser, normalizer, identifier resolver, validation rules
- Contract test: API/feed schema 및 adapter contract
- Fixture regression: 과거 원본 payload로 파서 회귀 확인
- Integration test: raw → normalized → curated end-to-end
- Data quality test: 필수 필드, 단위, 무결성, freshness
- Failure test: timeout, rate limit, malformed payload, source schema change
- Snapshot test: 동일 입력과 버전에서 결정 결과가 재현되는지 확인

## 10. 배포 게이트

다음 조건을 충족해야 curated data를 최신 결과로 배포한다.

- Source policy 확인 완료
- 원본 evidence 저장 성공
- 핵심 필드 스키마 검증 통과
- 제품/변형 식별이 명확하거나 ambiguity 표시
- 중요 필드 provenance 연결
- 미해결 충돌 및 stale 상태 노출
- Quality hard gate 통과 또는 제한된 상태로 명시적 배포 승인
