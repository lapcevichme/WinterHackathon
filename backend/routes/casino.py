from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB
from database import BaseDao

from schemas import Prize, get_prize, User_Bet
from core import get_random_item, get_current_active_user
casino_router = APIRouter()

user_basedao = BaseDao(User_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)


@casino_router.get("/prizes")
async def get_prizes_to_front():
    casino = await casino_basedao.get_entities()
    return casino
    
@casino_router.post("/add_prize")
async def add_prize_db(prize: Prize):
    casino = await casino_basedao.get_by_name(prize.name)
    if casino is None:
        await casino_basedao.create_entity(prize.model_dump())
        return {"message": "success"}
    prize.amount += casino.amount
    await casino_basedao.update_entity(casino.item_id, prize.model_dump())
    return {"message": "success"}

@casino_router.get("/user/balance")
async def get_user_balance(user: User_DB = Depends(get_current_active_user)):
    return user.money

@casino_router.post("/spin")
async def user_win_to_db(
    bet: User_Bet,
    user: User_DB = Depends(get_current_active_user)
    ):
    if user.money < bet.bet:
        raise HTTPException(status_code=402, detail={
            "error_code": "insufficient_funds",
            "message": "Не хватает монет для ставки"
        })
        
    win = await get_random_item()
    items_dao.create_entity({"user_id":user.user_id, "casino_id":win["item"].casino_id})
    user.money -= bet.bet + win["itog_rare_price"]
    user_basedao.update_entity(user.user_id, user.__dict__)
    return {
        "winner":{
            "id":win["item"].item_id,
            "name":win["item"].casino_id,
            "description": win["item"].description,
            "type": win["item"].type,
            "amount": 1,
            "emoji":win["item"].amoji,
            "color_hex": win["itog_rare"]
        },
        "new_balance": user.money
    }