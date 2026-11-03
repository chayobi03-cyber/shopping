# Tool and Solution Evaluation

## 1. 목적

제품 수집·검증·저장·운영 도구를 현재 요구 규모에 맞게 선택한다. 아래 목록은 후보군이며 도입 승인이나 현재 기능/가격/라이선스에 대한 보증이 아니다. 실제 도입 전 공식 문서, 유지보수 상태, 라이선스, 보안 및 비용을 재확인한다.

## 2. 도구 평가 기준

각 도구를 다음 기준으로 평가한다.

- 기능 적합성: 필요한 데이터와 workflow를 지원하는가?
- 권한/정책: source 약관과 수집 방식에 부합하는가?
- 신뢰성: 장애 처리, 재시도, 관측성이 충분한가?
- 유지보수성: 커뮤니티/벤더 유지보수와 문서가 있는가?
- 보안: secret 관리, 권한 분리, 감사 로그를 지원하는가?
- 확장성: source 수와 데이터량 증가에 대응 가능한가?
- 운영비용: 라이선스, 인프라, 인력 운영비를 포함해 감당 가능한가?
- 이식성: 데이터와 파이프라인을 다른 도구로 옮길 수 있는가?

## 3. 후보 도구 매트릭스

| Layer | Open-source / low-complexity candidates | Managed / commercial candidates | Selection note |
|---|---|---|---|
| HTTP/API collection | Python requests/httpx | API gateway / vendor feed | 공식 API 또는 계약 feed 우선 |
| HTML parsing | Beautiful Soup, lxml | Managed extraction services | 정적 문서 및 허용된 페이지에 한정 |
| Crawling framework | Scrapy | Apify 등 managed platform | 대량 작업 전에 약관·요금 검토 |
| Browser automation | Playwright, Selenium | Managed browser execution | 동적 페이지 필요 시에만 검토 |
| Scheduling | cron, GitHub Actions | Prefect Cloud, managed Airflow | MVP는 단순 스케줄부터 |
| Orchestration | Prefect, Apache Airflow, Apache NiFi | Managed orchestration services | workflow 복잡도와 운영 인력에 따라 선택 |
| Schema validation | Pydantic, JSON Schema | Commercial data quality suites | API contract와 데이터 모델 검증 |
| Data quality | Pandera, Great Expectations, Deequ | Enterprise data quality platforms | 품질 규칙의 코드화·리포팅 필요 수준에 따라 |
| OLTP storage | PostgreSQL | Managed PostgreSQL | MVP 기본 후보 |
| Local analytics | DuckDB | Cloud warehouse | 데이터량/동시성에 따라 확장 |
| Object storage | S3-compatible storage, MinIO | AWS S3, Azure Blob, Google Cloud Storage | raw evidence 저장 정책과 비용 확인 |
| Search | PostgreSQL full-text search | OpenSearch / Elasticsearch | 실제 검색 규모가 커질 때 도입 |
| Monitoring | Prometheus, Grafana, structured logs | Datadog 등 | 주요 pipeline metric과 alert 우선 |
| PIM | Pimcore, Akeneo | Salsify, Stibo Systems 등 | 제품 콘텐츠 운영이 핵심 요구일 때 평가 |

## 4. 권장 MVP 선택

초기 가설 구성:

- Python + requests/httpx + Beautiful Soup/lxml
- Playwright는 API/정적 수집으로 해결할 수 없는 허용된 동적 수집에만 사용
- Pydantic 또는 JSON Schema로 request/record contract 검증
- PostgreSQL로 제품·변형·근거 메타데이터 관리
- 파일/객체 저장소로 원본 evidence 보관
- pytest로 parser 및 source adapter regression test
- cron 또는 단순 scheduler로 수집 주기 관리
- Markdown/CSV/JSON 리포트로 초기 결과 제공

이 구성은 구현 복잡도를 제한하기 위한 출발점이다. 실제 source와 데이터량을 확인한 뒤 변경한다.

## 5. 도입 보류 기준

다음 요구가 확인되기 전에는 무거운 인프라를 도입하지 않는다.

- Airflow: 여러 workflow의 복잡한 의존성, backfill, 운영 UI가 필요할 때
- Spark: 단일 DB/단일 노드로 처리할 수 없는 규모가 확인될 때
- Kafka: 지속적인 이벤트 스트림과 consumer decoupling이 실제 요구될 때
- Enterprise PIM: 다수 팀의 콘텐츠 승인, 현지화, 채널 배포가 필요할 때
- 상용 데이터 품질 플랫폼: 자체 규칙 엔진/리포트로 운영할 수 없는 규모일 때

## 6. 상용 도구 검토 시 필수 확인

- 최신 가격 및 과금 단위
- 무료/유료 기능 차이와 사용량 제한
- 데이터 저장 위치 및 국외 이전
- 고객 데이터의 모델 학습/재사용 조건
- SLA, 장애 대응 및 지원 범위
- 계정/권한/감사 로그
- API rate limit 및 export 기능
- 데이터 소유권, 계약 종료 시 반환/삭제 방식
- 라이선스와 내부/상업적 사용 조건

## 7. Architecture Decision Record (ADR)

도구 선정은 다음 형식으로 기록한다.

- ADR-ID
- 문제 및 의사결정 맥락
- 검토한 후보와 평가 기준
- 채택안 및 채택 이유
- 기각안과 기각 이유
- 비용/보안/운영 리스크
- 재검토 조건
- 결정일 및 책임자

도구 이름의 인지도보다 요구사항 충족, 근거 추적, 운영 단순성, 데이터 이식성을 우선한다.
