from fastapi import APIRouter
from schemas import User
from database.models import User_DB
from database.basedao import BaseDao


auth_router = APIRouter()
user_basedao = BaseDao(User_DB)


@auth_router.post("/register", status_code=201)
async def user_register(user: User):
    await user_basedao.create_entity(user.model_dump())
    return {"user": user}

@auth_router.get("/prize")
async def get_prize():
    ...