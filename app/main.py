from fastapi import FastAPI

from app.api.bot import bot_router
from app.api.application import application_router
from app.api.user import user_router


app = FastAPI()
app.include_router(bot_router)
app.include_router(application_router)
app.include_router(user_router)
