from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

from items.routers import router as item_router
from users.routers import router as user_router

app = FastAPI()
app.include_router(item_router)
app.include_router(user_router)


class NowResponse(BaseModel):
    now: datetime


@app.get("/now", response_model=NowResponse)
def get_now_handler():
    # return {"now": datetime.now()}
    return NowResponse(now=datetime.now())
