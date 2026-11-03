# Implementation Roadmap

## 1. 목표

문서 기반 표준을 실행 가능한 제품 조사 파이프라인으로 전환한다. 대규모 인프라를 먼저 구축하지 않고 제품 식별·근거 수집·사양 검증·재고 검증을 작은 범위에서 검증한 뒤 확장한다.

일정은 개발 리소스와 source 접근 권한에 따라 조정하는 초기 제안이다. 확정 프로젝트 일정이나 납기 보증이 아니다.

## 2. 단계별 마일스톤

| Phase | 예상 기간 | 주요 작업 | 완료 기준 |
|---|---:|---|---|
| P0 — Scope & contracts | 1주 | 카테고리 1개 선정, 핵심 필드와 상태 정의, source 정책 검토 | 샘플 요청·제품·근거 계약 확정 |
| P1 — Data foundation | 1~2주 | PostgreSQL 스키마, evidence 저장, source registry, JSON schema | 제품/변형/근거/오퍼를 연결해 저장 |
| P2 — Collection MVP | 1~2주 | 공식 문서와 1~2개 판매처 adapter, raw capture, 파서 fixture | 수동 실행으로 end-to-end 수집 가능 |
| P3 — Verification & quality | 1~2주 | 모델 식별, 필드 검증, 교차검증, KPI 리포트 | 핵심 필드 상태 및 충돌을 정확히 표시 |
| P4 — Stock & comparison | 1주 | 옵션별 구매 가능 확인, 가격 정규화, 조건 판정 | 사이즈/색상별 상태와 확인 시각 표시 |
| P5 — Automation & monitoring | 1~2주 | 스케줄, 재시도, 알림, 회귀 테스트, 실행 로그 | 실패 감지 및 안전한 재실행 가능 |
| P6 — Controlled expansion | 지속 | 카테고리/채널 추가, 비용·성능 최적화 | 새 source가 기존 contract/test를 통과 |

## 3. Illustrative Gantt

시작 시점이 확정되지 않았으므로 상대 단계 기준 일정 초안이다.

~~~mermaid
gantt
    title Shopping Research MVP Roadmap (Illustrative)
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    section Foundation
    Scope and contracts          :p0, 2026-11-03, 7d
    Database and evidence model  :p1, after p0, 10d
    section Collection
    Source adapters              :p2, after p1, 10d
    section Quality
    Identity and spec validation :p3, after p2, 10d
    Stock and comparison         :p4, after p3, 7d
    section Operations
    Scheduling and monitoring    :p5, after p4, 10d
~~~

위 날짜는 2026-11-03을 기준으로 생성한 계획 초안이다. 실제 착수일, 투입 인력, source 승인 상태를 확인한 뒤 기준선을 갱신한다.

## 4. 비용 추정 — 산식 검증용 시나리오

아래는 제공된 가정의 산술 검산 예시다. 인건비는 팀 전체 월 비용, 도구·인프라도 월 비용이라고 가정한다. 시장 견적 또는 실제 인건비 검증값이 아니다.

| Scenario | Team | Duration | Labor / month | Infra / month | Formula | Total |
|---|---:|---:|---:|---:|---|---:|
| Small | 2 | 3 months | 20M KRW | 5M KRW | (20 + 5) × 3 | 75M KRW |
| Medium | 5 | 6 months | 100M KRW | 20M KRW | (100 + 20) × 6 | 720M KRW |
| Large | 10 | 12 months | 240M KRW | 50M KRW | (240 + 50) × 12 | 3,480M KRW |

원안의 Medium 320M, Large 1,000M은 위 월 비용·기간 가정과 산술적으로 일치하지 않는다. 위 합계는 계산식만 바로잡은 것이며 실제 예산 산정에는 직무별 인건비, 외주, 클라우드 사용량, 데이터 구매, 법률 검토, 부가세 및 예비비를 별도로 산정해야 한다.

MVP는 소규모 단일 카테고리와 소수 source로 시작해 실제 운영 비용을 측정한 후 확대 여부를 결정한다.

## 5. MVP 범위 제안

초기 제품군은 한 카테고리로 제한한다. 현재 쇼핑 프로젝트에서는 의류/다운 제품을 파일럿으로 사용할 수 있다.

파일럿 필드 예시:

- 제품 식별: 브랜드, 모델명, 제조사 품번, 시즌, 색상 코드
- 사양: 충전재 종류, 다운/깃털 비율, 필파워, 다운 충전량, 완제품 중량, 총장
- 오퍼: 판매처, 옵션, 가격, 배송비, 상품 URL
- 재고 관측: 색상·사이즈별 상태, 확인 시각
- 근거: source grade, URL, 확인 시각, 해당 필드, identity match
- 판정: 필수 조건 PASS/FAIL/UNKNOWN, 구매 상태, 남은 확인 항목

미공개 사양을 추정하지 않는지, 이전 품절 후보도 다시 검색하는지, 110 사이즈 등 옵션 단위 재고를 분리하는지 검증한다.

## 6. Release gates

### Data collection gate
- Source Registry 등록 완료
- 사용 권한 및 요청 정책 확인
- raw evidence 저장 및 provenance 부여
- adapter regression fixture 통과

### Verification gate
- 제품·변형 식별 상태 표시
- 필수 필드 단위/범위 검사
- 충돌 및 미확인 필드 표시
- 신뢰도와 데이터 품질 분리

### Decision gate
- 사용자 필수 조건을 임의 변경하지 않음
- 필수 데이터 누락 시 DATA_NOT_READY
- 가격·재고에 확인 시각 표시
- 구매/결제 등은 승인 전 실행 금지

### Release gate
- 테스트 통과
- quality report 첨부
- 변경 내역과 버전 기록
- 롤백/재처리 절차 확인

## 7. 다음 실행 항목

1. 파일럿 카테고리와 필수 필드를 확정한다.
2. 공식 사양 출처와 판매처 source를 1~2개씩 선정한다.
3. 샘플 제품 5~10개를 정해 수동 정답 세트를 만든다.
4. source adapter와 schema validation을 구현한다.
5. 수집/검증 결과를 사람이 대조해 오류 유형을 수집한다.
6. KPI와 TTL을 실측 데이터에 맞춰 보정한다.
7. 파일럿 통과 후 카테고리와 수집 채널을 확대한다.
