from fastapi import FastAPI

app = FastAPI()

items = [
    {"id": 1, "name": "i-phone 16", "price": 100},
    {"id": 2, "name": "Galaxy 25", "price": 200},
    {"id": 3, "name": "Huawei", "price": 50},
]


# 전체 상품 목록 조회 API
# Query Parameter: 127.0.0.1:8000/items?min_price=100
@app.get("/items")
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
@app.get("/items/{item_id}")
def item_handler(
    item_id: int,  # path 변수
    max_price: int | None = None,  # query param
):
    result = None
    for item in items:
        if item["id"] == item_id:
            result = item
            print(f"max_price: {max_price}")
    return {"item": result}
