from fastapi import FastAPI

from items.routers import router as item_router
from users.routers import router as user_router

app = FastAPI()
app.include_router(item_router)
app.include_router(user_router)
