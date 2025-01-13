import asyncio

from fastapi import FastAPI

from items.routers import router as item_router
from users.routers import router as user_router

app = FastAPI()
app.include_router(item_router)
app.include_router(user_router)

import time
import httpx

@app.get("/sync/json")
def sync_json_handler():
    start_time = time.perf_counter()
    urls = [
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
    ]
    responses = []
    for url in urls:
        responses.append(httpx.get(url).json())

    end_time = time.perf_counter()
    return {
        "duration": end_time - start_time,
        "responses": responses
    }


@app.get("/async/json")
async def async_json_handler():
    start_time = time.perf_counter()
    urls = [
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
        "https://jsonplaceholder.typicode.com/posts",
    ]
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(client.get(url))
        responses = await asyncio.gather(*tasks)

        result = []
        for res in responses:
            result.append(res.json())

    end_time = time.perf_counter()
    return {
        "duration": end_time - start_time,
        "responses": result
    }
