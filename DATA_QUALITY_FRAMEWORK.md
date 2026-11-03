# Data Quality Framework and KPIs

## 1. 목적

제품 데이터 품질을 사용 목적에 맞게 측정하고 데이터 결함이 제품 비교나 구매 판단으로 전파되지 않게 통제한다. 품질은 하나의 점수로 축약하지 않고 7개 차원과 필드별 판정으로 관리한다.

## 2. 7대 데이터 품질 차원

| Dimension | Definition | Example defect |
|---|---|---|
| Accuracy 정확성 | 실제 대상 제품 및 기준 자료와 값이 일치하는 정도 | 잘못된 충전량/전압 |
| Completeness 완전성 | 사용 목적상 필수인 데이터가 채워진 정도 | 모델 품번 누락 |
| Consistency 일관성 | 동일한 정의·범위의 값이 출처/시스템 간 모순되지 않는 정도 | 같은 변형의 상이한 중량 |
| Validity 유효성 | 스키마, 단위, 값 범위, 도메인 규칙을 만족하는 정도 | 음수 용량, 잘못된 통화 |
| Uniqueness 고유성 | 동일 제품/오퍼가 부적절하게 중복되지 않는 정도 | 한 판매 오퍼가 여러 번 등록 |
| Integrity 무결성 | 제품·변형·출처·근거 간 관계와 참조가 온전한 정도 | 고아 SpecAssertion |
| Timeliness 적시성 | 해당 필드의 의사결정에 충분히 최신인 정도 | 오래된 가격/재고 |

## 3. KPI 정의 및 계산

KPI는 분모, 측정 대상, 집계 기간, 표본 추출 방법을 함께 기록한다.

| KPI | Suggested calculation | Notes |
|---|---|---|
| Gold-set accuracy | 검증 정답과 일치한 평가 필드 수 / 평가한 필드 수 | 독립적인 수동 판정 표본 필요 |
| Critical completeness | 값과 유효 근거가 존재하는 필수 필드 수 / 요구된 필수 필드 수 | null이 아닌 값만으로 충족 처리하지 않음 |
| Conflict rate | 동일 제품·필드·범위에서 미해결 충돌이 있는 assertion group 수 / 비교 가능한 assertion group 수 | 해소된 충돌과 미해결 충돌 구분 |
| Validity pass rate | 자동 규칙을 통과한 값 수 / 규칙 적용 가능한 값 수 | 적용 불가능한 값은 별도 집계 |
| Duplicate rate | 중복으로 판정된 레코드 수 / 검사한 레코드 수 | 제품과 판매 오퍼의 중복 규칙 분리 |
| Referential integrity | 모든 필수 참조가 유효한 레코드 수 / 참조 검사 레코드 수 | source/evidence/product 관계 검사 |
| Freshness SLA rate | 해당 필드 TTL 안에 확인된 관측 수 / 유효한 관측 수 | 필드별 TTL 적용 |
| Collection success rate | 성공한 source fetch 수 / 예정된 fetch 수 | 실패 유형별 분리 |
| Parse success rate | 정상 파싱된 응답 수 / 수집 성공 응답 수 | source schema 변경 탐지 |
| Provenance coverage | source와 evidence가 연결된 중요 assertion 수 / 전체 중요 assertion 수 | 근거 없는 값은 검증 PASS 금지 |

## 4. 기준값과 게이트

초기 임계값은 운영 데이터로 보정해야 하며 아래는 파일럿 시작을 위한 제안값이지 업계 표준 또는 보증값이 아니다.

| Metric | Initial pilot target | Hard gate |
|---|---:|---|
| Product identity match | Shortlist 후보 100% | 미확인 시 shortlist 보류 |
| Critical completeness | >= 95% | 사용자 지정 필수 필드 누락 시 판정 보류 |
| Provenance coverage | 핵심 주장 100% | 근거 없는 핵심 주장은 사용 금지 |
| Validity pass rate | >= 99% | 치명적 범위 위반은 격리 |
| Referential integrity | 100% | 고아 근거/제품 참조는 배포 차단 |
| Stock freshness | 카테고리/채널별 TTL | TTL 초과 재고는 STALE |
| Price freshness | 카테고리/채널별 TTL | TTL 초과 가격은 현재가로 표시 금지 |

정확도 목표는 gold set을 구축한 뒤 카테고리별로 설정한다. 검증 정답이 없는 상태에서 98% 등의 정확도를 선언하지 않는다.

## 5. 필드별 신선도 정책

가격·재고·사양·리뷰는 변경 주기가 다르므로 하나의 TTL을 공유하지 않는다.

| Data class | Freshness policy |
|---|---|
| Price | 조사 시점의 판매처 관측을 우선. TTL 초과 시 STALE |
| Stock/availability | 가장 짧은 TTL 적용. 옵션·판매처 단위로 관리 |
| Product specification | 공식 변경 공지, 시즌/리비전 변경, 정기 재검토를 기준으로 갱신 |
| Certification | 인증기관의 최신 상태/유효기간 확인 |
| Review aggregate | 집계 기준 기간과 수집 시점을 함께 표시 |
| Patent metadata | 검색·출원·등록 상태의 기준일을 보존 |

TTL은 카테고리와 판매 채널별 설정값으로 구성하며 checked_at과 함께 표시한다.

## 6. 신뢰도와 품질의 분리

Source reliability는 출처가 해당 필드를 제공하기에 얼마나 적절한지 평가한다. Data quality는 실제로 수집된 값이 정확하고 완전하며 유효하고 최신인지 평가한다. 두 개념을 동일시하지 않는다.

권장 평가 축:

- Source suitability: 해당 필드에 대한 출처의 권한/전문성
- Product identity match: 근거가 정확한 모델/변형에 적용되는지
- Evidence integrity: 원문 위치·수집 시각·해시가 보존되는지
- Temporal freshness: 데이터가 현재 판단에 충분히 최신인지
- Cross-source agreement: 독립 출처 간 일치/충돌 여부

필드별 점수는 설명 가능한 하위 점수와 규칙을 보존한다. 단순 가중평균이 필수 검증 실패나 충돌을 상쇄하게 해서는 안 된다.

## 7. 품질 상태 산정 규칙

- VERIFIED: 필수 검증 규칙 통과, 제품/변형 일치, 유효한 근거 확보
- PARTIALLY_VERIFIED: 일부 속성/범위/단위가 확인되지 않음
- CONFLICT: 해결되지 않은 유효 근거 간 값의 충돌
- UNKNOWN: 확인 가능한 값 또는 근거가 없음
- STALE: 과거에는 확인되었으나 TTL 초과
- DATA_NOT_READY: 의사결정 필수 조건을 평가할 만큼 데이터가 충분하지 않음

## 8. 품질 리포트

주기별 리포트에 포함할 항목:

- 카테고리·브랜드·source별 품질 추세
- 필드별 정확성 표본 결과와 표본 크기
- 필수 필드 완전성
- 충돌 유형 및 해결 리드타임
- source fetch/parse 실패율
- 가격·재고 신선도 SLA 준수율
- 중복·참조 무결성 오류
- 수정 전후 품질 변화 및 재발 결함

## 9. 개선 루프

1. KPI 저하를 source/field/category 단위로 분해한다.
2. 원본 evidence까지 역추적한다.
3. 원인 유형(오식별, 원천 변경, 파서 오류, 오래된 데이터, 단위 오류)을 분류한다.
4. 데이터 또는 파서를 수정하고 regression fixture를 추가한다.
5. 같은 표본 및 규칙으로 재측정한다.
6. 품질 변화와 변경 이력을 기록한다.
