# Evidence Schema

## 1. 목적

조사 결과를 출처·시간·제품 식별자와 연결해 재현 가능하게 저장한다. 아래는 구현 언어에 종속되지 않는 논리 스키마다.

## 2. Product

```json
{
  "product_id": "brand-model-sku-season",
  "brand": "string",
  "model_name": "string",
  "manufacturer_sku": "string|null",
  "season": "string|null",
  "category": "string",
  "gender": "string|null",
  "color": "string|null",
  "color_code": "string|null",
  "identity_status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|UNKNOWN"
}
```

## 3. Specification

```json
{
  "product_id": "string",
  "field": "fill_power",
  "value": 800,
  "unit": "FP",
  "scope": "men / size 110 / season 2026",
  "status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|UNKNOWN|NOT_APPLICABLE",
  "source_ids": ["source-001"],
  "notes": "Measurement standard or caveat"
}
```

미확인 값은 `null`로 저장한다. 추정값을 확인값 필드에 넣지 않는다. 추정이 별도 목적상 필요하면 `estimated_value`와 산출 근거를 분리하고 검증값으로 취급하지 않는다.

## 4. Source

```json
{
  "source_id": "source-001",
  "url": "https://example.com/product",
  "source_type": "manufacturer|authorized_retailer|marketplace|seller_qa|review|search_snippet",
  "grade": "A|B|C|D|E",
  "title": "string|null",
  "published_at": "ISO-8601|null",
  "checked_at": "ISO-8601",
  "model_match": "VERIFIED|PARTIAL|NO_MATCH|UNKNOWN",
  "evidence_note": "Short factual note"
}
```

## 5. Offer / Stock

```json
{
  "offer_id": "seller-product-option",
  "product_id": "string",
  "seller": "string",
  "platform": "string",
  "url": "https://example.com/offer",
  "condition": "NEW|USED|UNKNOWN",
  "color": "string|null",
  "size": "110",
  "price": 150000,
  "currency": "KRW",
  "shipping_cost": null,
  "availability": "AVAILABLE|LOW_STOCK|SOLD_OUT|OPTION_MISSING|PREORDER|BACKORDER|UNVERIFIED|UNKNOWN",
  "checked_at": "ISO-8601",
  "notes": "Option-specific evidence"
}
```

## 6. Research decision

```json
{
  "product_id": "string",
  "required_conditions": {
    "size": "110",
    "condition": "NEW",
    "long_length_required": true,
    "max_total_price": 200000
  },
  "condition_result": "PASS|FAIL|UNKNOWN",
  "specification_status": "VERIFIED|PARTIALLY_VERIFIED|CONFLICT|DATA_NOT_READY",
  "purchase_status": "AVAILABLE|UNAVAILABLE|UNVERIFIED",
  "decision": "SHORTLIST|REJECT|HOLD_FOR_EVIDENCE",
  "as_of": "ISO-8601",
  "rationale": ["Evidence-backed reason"],
  "open_questions": ["Missing evidence"]
}
```

## 7. Data integrity rules

- 모든 시간은 ISO-8601 형식과 시간대(offset)를 포함한다.
- 각 사양 값은 하나 이상의 출처와 연결한다.
- 가격·재고는 시점이 지나면 stale 상태로 재평가한다.
- `CONFLICT`를 단일 값으로 덮어쓰지 않는다.
- 동일 제품이라도 색상/사이즈별 판매 오퍼는 별도 레코드다.
- 원문 URL, 확인 시각, 모델 일치 여부를 보존한다.
- 삭제·수정 시 이전 판정에 영향을 준 근거의 변경 이력을 남긴다.
