from fastapi import APIRouter
from database.models import User_DB
from database import BaseDao


casino_router = APIRouter()
user_basedao = BaseDao(User_DB)

@casino_router.get("/prize")
async def get_prize():
    ...