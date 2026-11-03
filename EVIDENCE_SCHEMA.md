# Evidence and Product Data Schema

## 1. 설계 원칙

이 스키마는 제품·제품 변형·사양 주장·출처·원본 증거·판매 오퍼·재고 관측·인증·리뷰 집계·품질 결과·판정 스냅샷을 분리한다.

- 하나의 제품(Product)은 여러 변형(ProductVariant)을 가질 수 있다.
- 하나의 사양 필드에는 여러 출처의 주장(SpecAssertion)이 공존할 수 있다.
- 원본 증거(Evidence)는 수정하지 않고 정규화 값은 별도 assertion으로 저장한다.
- 가격과 재고는 판매처·옵션·관측 시각에 종속된다.
- 식별자는 유형과 발급 주체를 함께 저장한다. SKU 값만으로 전역 유일성을 가정하지 않는다.
- 모든 시간 값은 시간대 offset이 포함된 ISO-8601을 사용한다.
- 미확인 값은 null로 저장하고 상태를 별도로 기록한다. 추정값을 검증값에 넣지 않는다.

## 2. Entity relationship overview

~~~mermaid
erDiagram
  PRODUCT ||--o{ PRODUCT_VARIANT : has
  PRODUCT ||--o{ IDENTIFIER : identified_by
  PRODUCT_VARIANT ||--o{ IDENTIFIER : identified_by
  PRODUCT_VARIANT ||--o{ SPEC_ASSERTION : has_assertions
  SOURCE ||--o{ EVIDENCE : provides
  SOURCE ||--o{ SPEC_ASSERTION : supports
  EVIDENCE ||--o{ SPEC_ASSERTION : supports
  PRODUCT_VARIANT ||--o{ OFFER : sold_as
  OFFER ||--o{ AVAILABILITY_OBSERVATION : observed_as
  PRODUCT_VARIANT ||--o{ CERTIFICATION : covered_by
  PRODUCT_VARIANT ||--o{ REVIEW_AGGREGATE : reviewed_as
  PRODUCT ||--o{ QUALITY_REPORT : evaluated_by
  PRODUCT ||--o{ DECISION_SNAPSHOT : included_in
~~~

## 3. Product

제품군/논리 제품 수준의 엔티티다.

~~~json
{
  "schema_version": "1.1",
  "product_id": "brand-category-model-family",
  "brand": "string",
  "canonical_name": "string",
  "category": "string",
  "description_summary": null,
  "created_at": "2026-11-03T10:00:00+09:00",
  "updated_at": "2026-11-03T10:00:00+09:00"
}
~~~

## 4. ProductVariant

실제 사양·색상·사이즈·시즌 차이를 관리하는 단위다. 비교와 재고 검증은 가능한 한 variant 수준에서 수행한다.

~~~json
{
  "product_variant_id": "brand-model-sku-season-color",
  "product_id": "brand-category-model-family",
  "manufacturer_model_name": "string",
  "manufacturer_model_number": "string|null",
  "season": "string|null",
  "market": "KR|null",
  "gender": "string|null",
  "color": "string|null",
  "color_code": "string|null",
  "size_system": "KR|null",
  "variant_attributes": {
    "size": "110"
  },
  "identity_status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|UNKNOWN",
  "created_at": "2026-11-03T10:00:00+09:00"
}
~~~

## 5. Identifier

GTIN, 제조사 모델번호, MPN, OEM 부품번호, 판매자 SKU 등을 공통 구조로 보관한다.

~~~json
{
  "identifier_id": "identifier-001",
  "entity_type": "PRODUCT|PRODUCT_VARIANT|OFFER",
  "entity_id": "string",
  "identifier_type": "GTIN_13|GTIN_14|MPN|MANUFACTURER_SKU|OEM_PART_NO|SELLER_SKU|OTHER",
  "value": "string",
  "issuer": "GS1|manufacturer-name|seller-name|unknown",
  "market": "KR|null",
  "valid_from": null,
  "valid_to": null,
  "source_id": "source-001",
  "status": "VERIFIED|PARTIALLY_VERIFIED|UNKNOWN"
}
~~~

GTIN은 보유한 경우 활용하되 필수값으로 강제하지 않는다. 동일 문자열이라도 identifier_type 또는 issuer가 다르면 동일 식별자로 취급하지 않는다.

## 6. Source

출처의 운영 주체, 유형, 접근 방식, 사용 조건과 신뢰도 등급을 기록한다.

~~~json
{
  "source_id": "source-001",
  "organization": "string",
  "source_name": "string",
  "source_type": "manufacturer|certification|distributor|retailer|marketplace|review|community|manual",
  "officialness": "official|authorized|third_party|user_generated|unknown",
  "grade": "A|B|C|D|E",
  "url": "https://example.com/resource",
  "access_method": "api|feed|download|permitted_web|manual",
  "terms_url": "https://example.com/terms",
  "coverage": ["model", "specification"],
  "rate_limit_note": "string|null",
  "retention_policy": "string|null",
  "status": "ACTIVE|DEGRADED|BLOCKED|RETIRED|UNKNOWN",
  "last_checked_at": "2026-11-03T10:00:00+09:00"
}
~~~

## 7. Evidence

원본 문서/응답의 위치와 무결성 메타데이터를 보존한다. 원본 콘텐츠 전체를 저장할 수 있는지는 라이선스와 보존 정책을 먼저 확인한다.

~~~json
{
  "evidence_id": "evidence-001",
  "source_id": "source-001",
  "uri": "https://example.com/product-spec.pdf",
  "storage_uri": "object://bucket/key|null",
  "content_type": "application/pdf",
  "content_hash_sha256": "hex-string|null",
  "retrieved_at": "2026-11-03T10:00:00+09:00",
  "published_at": null,
  "document_version": "string|null",
  "locator": {
    "page": 3,
    "section": "Specifications",
    "field_path": null
  },
  "capture_method": "api|download|permitted_web|manual",
  "retention_class": "short|standard|restricted",
  "notes": "string|null"
}
~~~

## 8. SpecAssertion

각 사양 필드는 단일 제품값으로 덮어쓰지 않고 출처별 assertion으로 보관한다. raw_value와 normalized_value를 분리한다.

~~~json
{
  "assertion_id": "assertion-001",
  "product_variant_id": "brand-model-sku-season-color",
  "field_key": "fill_power",
  "raw_value": "800 fill power",
  "normalized_value": 800,
  "unit": "FP",
  "scope": "men / size 110 / season 2026",
  "source_id": "source-001",
  "evidence_id": "evidence-001",
  "identity_match": "VERIFIED|PARTIAL|NO_MATCH|UNKNOWN",
  "verification_status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|UNKNOWN|NOT_APPLICABLE",
  "observed_at": "2026-11-03T10:00:00+09:00",
  "valid_from": null,
  "valid_to": null,
  "parser_version": "1.0.0",
  "supersedes_assertion_id": null,
  "notes": "Measurement standard or caveat"
}
~~~

숫자 필드는 숫자형으로 정규화할 수 있지만 원문 표기, 단위, 측정 범위, 적용 사이즈를 함께 보존한다. 필파워, 충전량, 완제품 중량, 총장 등은 별도 field_key를 사용한다.

## 9. Offer

판매처별 판매 오퍼를 제품 변형과 분리해 기록한다.

~~~json
{
  "offer_id": "seller-product-option",
  "product_variant_id": "brand-model-sku-season-color",
  "seller": "string",
  "platform": "string",
  "url": "https://example.com/offer",
  "condition": "NEW|USED|UNKNOWN",
  "currency": "KRW",
  "list_price": "189000",
  "sale_price": "159000",
  "shipping_cost": "0|null",
  "checked_at": "2026-11-03T10:00:00+09:00",
  "seller_identity_status": "VERIFIED|PARTIALLY_VERIFIED|UNKNOWN"
}
~~~

금액은 부동소수점 오차를 피하도록 decimal 문자열 또는 DB DECIMAL 타입으로 저장한다. 할인 쿠폰, 카드 혜택, 배송비, 관부가세 포함 여부는 별도 조건으로 기록한다.

## 10. AvailabilityObservation

재고는 판매처·오퍼·색상·사이즈·확인 시각 단위로 기록한다.

~~~json
{
  "availability_observation_id": "availability-001",
  "offer_id": "seller-product-option",
  "variant_attributes": {
    "color": "black",
    "size": "110"
  },
  "availability": "AVAILABLE|LOW_STOCK|SOLD_OUT|OPTION_MISSING|PREORDER|BACKORDER|UNVERIFIED|UNKNOWN",
  "quantity": null,
  "checked_at": "2026-11-03T10:00:00+09:00",
  "verification_method": "option_selection|cart_step|seller_api|seller_confirmation|listing_only",
  "evidence_id": "evidence-001",
  "ttl_seconds": 1800,
  "notes": "string|null"
}
~~~

상품 페이지가 열리는 것과 특정 옵션이 구매 가능한 것은 다른 상태다. listing_only 방식만으로 AVAILABLE을 부여하지 않는다.

## 11. Certification

인증은 인증기관과 적용 제품 범위를 포함한다.

~~~json
{
  "certification_id": "cert-001",
  "product_variant_id": "brand-model-sku-season-color",
  "authority": "string",
  "certification_type": "KC|CE|UL|ENERGY_STAR|OTHER",
  "certificate_number": "string|null",
  "status": "VALID|EXPIRED|SUSPENDED|UNKNOWN",
  "scope": "string",
  "issued_at": null,
  "expires_at": null,
  "source_id": "source-001",
  "evidence_id": "evidence-001",
  "checked_at": "2026-11-03T10:00:00+09:00"
}
~~~

인증 정보는 인증 범위 내에서만 해석한다. 특정 인증이 제품의 모든 사양이나 성능을 보증한다고 확대 해석하지 않는다.

## 12. ReviewAggregate

리뷰는 원문 수집을 기본값으로 삼지 않는다. 가능한 경우 집계값과 집계 기준만 저장한다.

~~~json
{
  "review_aggregate_id": "review-agg-001",
  "product_variant_id": "brand-model-sku-season-color",
  "source_id": "source-001",
  "rating_average": 4.3,
  "rating_scale": 5,
  "review_count": 125,
  "period_start": "2026-01-01",
  "period_end": "2026-11-03",
  "sentiment_topics": ["warmth", "sizing", "durability"],
  "checked_at": "2026-11-03T10:00:00+09:00",
  "sampling_method": "platform_aggregate"
}
~~~

리뷰 수·평균 평점·표본 기간을 분리한다. 리뷰 텍스트나 사용자 식별정보 저장은 권한과 개인정보 검토 없이는 수행하지 않는다.

## 13. QualityReport

품질은 전체 제품 단일 점수보다 필드와 데이터셋 단위 결과를 우선한다.

~~~json
{
  "quality_report_id": "quality-001",
  "entity_type": "PRODUCT|PRODUCT_VARIANT|DATASET",
  "entity_id": "string",
  "evaluated_at": "2026-11-03T10:00:00+09:00",
  "metrics": {
    "accuracy": null,
    "completeness": 0.95,
    "consistency": null,
    "validity": 0.99,
    "uniqueness": null,
    "integrity": 1.0,
    "timeliness": null
  },
  "sample_size": null,
  "ruleset_version": "1.0.0",
  "status": "PASS|WARN|FAIL|DATA_NOT_READY",
  "failed_rules": [],
  "notes": "Accuracy is null until an adjudicated gold set is available."
}
~~~

측정하지 않은 지표는 0으로 간주하지 않고 null로 저장한다. 분모와 표본 수, 규칙 버전을 별도로 보존한다.

## 14. DecisionSnapshot

특정 시점의 사용자 조건, 참조 데이터 버전, 품질 상태, 구매 가능성을 고정해 판단을 재현한다.

~~~json
{
  "decision_snapshot_id": "decision-001",
  "product_variant_id": "brand-model-sku-season-color",
  "request_id": "request-001",
  "required_conditions": {
    "size": "110",
    "condition": "NEW",
    "long_length_required": true,
    "max_total_price": "200000",
    "currency": "KRW"
  },
  "condition_result": "PASS|FAIL|UNKNOWN",
  "specification_status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|DATA_NOT_READY",
  "purchase_status": "AVAILABLE|UNAVAILABLE|UNVERIFIED",
  "quality_report_id": "quality-001",
  "evidence_ids": ["evidence-001"],
  "as_of": "2026-11-03T10:00:00+09:00",
  "decision": "SHORTLIST|REJECT|HOLD_FOR_EVIDENCE",
  "rationale": ["Evidence-backed reason"],
  "open_questions": ["Missing evidence"]
}
~~~

필수 조건이 UNKNOWN인 경우 PASS로 처리하지 않는다. 구매 가능성은 해당 판매처·옵션·관측 시점에 한정한다.

## 15. Common enums and integrity rules

- 모든 상태값은 해당 문서의 허용 enum만 사용한다.
- 모든 사양 assertion은 제품 변형과 source를 참조한다.
- 가능한 경우 assertion은 evidence를 참조하며, 핵심 주장에는 evidence 연결을 필수로 한다.
- 각 evidence는 source와 retrieved_at을 가진다.
- 가격/재고에는 checked_at과 판매처/옵션이 있어야 한다.
- 원본 값과 정규화 값을 별도 필드로 유지한다.
- 수집·파서·규칙 버전을 기록해 재처리 결과를 비교할 수 있게 한다.
- CONFLICT를 평균값이나 최신 수집값으로 조용히 덮어쓰지 않는다.
- stale 판정은 데이터 유형별 TTL 정책을 따른다.
- 개인정보와 비밀정보를 예시 데이터 또는 로그에 포함하지 않는다.
