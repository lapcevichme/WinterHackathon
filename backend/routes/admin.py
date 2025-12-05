from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from core import decode_role, get_time_diff_seconds
from database.models import User_DB, Token_qr_DB
from database.basedao import BaseDao


admin_router = APIRouter()
user_basedao = BaseDao(User_DB)
item_token_dao = BaseDao(Token_qr_DB)

@admin_router.post("/prizes/redeem", tags=["admin"])
async def post_prizes_qr(token, user: User_DB = Depends(decode_role)):
    token_db: Token_qr_DB = await item_token_dao.get_by_token(token)
    if get_time_diff_seconds(token_db) > 0:
        return {"status": "success"}
    await item_token_dao.delete_entity_by_id(token_db.token_id)
    return {"status": "success"}