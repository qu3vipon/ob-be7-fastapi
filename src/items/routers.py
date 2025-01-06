from fastapi import APIRouter, Query

router = APIRouter(prefix="/items", tags=["Items"])

items = [
    {"id": 1, "name": "i-phone 16", "price": 100},
    {"id": 2, "name": "Galaxy 25", "price": 200},
    {"id": 3, "name": "Huawei", "price": 50},
]

# 전체 상품 목록 조회 API
@router.get("")
def items_handler(
    min_price: int | None = None,
    max_price: int | None = None,
):
    result = items
    if min_price:  # min_price = 100
        # 가격이 min_price 이상인 상품
        new_result = []
        for item in result:
            if item["price"] >= min_price:
                new_result.append(item)
        result = new_result

    if max_price:
        # 가격이 max_price 이하인 상품
        result = [item for item in result if item["price"] <= max_price]

    return {"items": result}

# 특정 상품 반환 API
@router.get("/{item_id}")
def item_handler(
    item_id: int,
    max_price: int = Query(..., ge=10_000, lt=1_000_000),
):
    result = None
    for item in items:
        if item["id"] == item_id:
            result = item
            print(f"max_price: {max_price}")
    return {"item": result}
