from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from core import create_access_token
from database.models import User_DB
from database.basedao import BaseDao


admin_router = APIRouter()
user_basedao = BaseDao(User_DB)

@admin_router.post("/prizes/redeem")
async def post_prizes_qr():
    pass