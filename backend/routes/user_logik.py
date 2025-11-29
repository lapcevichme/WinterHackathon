from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB, Quests_DB
from database import BaseDao
import random
from schemas import Prize, get_prize, User_Bet, Redact_User
from core import decode_access_token, generate_qr_base64
import uuid
user_router = APIRouter()

user_basedao = BaseDao(User_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)
quest_dao = BaseDao(Quests_DB)
@user_router.get("/profile/balance")
async def get_user_amount(user: User_DB = Depends(decode_access_token)):
    return {
        "amount": user.amount,
        "currency_symbol": random.choice(["❄️", "💰", "$", "RUB"])
    }
    
@user_router.get("/profile/me")
async def get_user_info(user: User_DB = Depends(decode_access_token)):
    return {
  "id": user.user_id,
  "username": user.username,
  "department": user.team,
  "avatar_url": user.url,
  "level": user.level,
  "xp": user.score,
  "max_xp": user.max_score,
  "inventory": user.items
}

@user_router.patch("/profile/me")
async def patch_user(redact_info: Redact_User, user: User_DB = Depends(decode_access_token)):
    user.display_name = redact_info.display_name
    user.url = redact_info.url
    await user_basedao.update_entity(user.id, user)
    return user

@user_router.get("/profile/inventory/{id}/code")
async def get_qr(id: str):
    return {
        "redeem_token": generate_qr_base64(id),
        "expires_in_seconds": 300
    }
    
@user_router.get("/leaderboard")
async def get_leaderboard():
    leader = await user_basedao.get_entities()
    leader = sorted(leader.__dict__.items(), key=lambda x: x[1][5])
    return leader[:10]

@user_router.post("/quests/{id}/claim")
async def claim_quest(id: uuid.UUID):
    quest:Quests_DB = quest_dao.get_by_name(id)
    quest.user.amount += quest.amount
    quest.status = "completed"
    quest_dao.update_entity(quest.quest_id, quest)
    user_basedao.update_entity(quest.user_id, quest.user)
    return {
        "balance":{
            "amount": quest.amount,
            "currency_symbol": "❄️"
        }
    }
    
@user_router.get("/main")
async def get_main_info(user: User_DB = Depends(decode_access_token)):
    return{
  "user_summary": {
    "id": user.user_id,
    "display_name": user.display_name,
    "balance": {
      "amount": user.amount,
      "currency_symbol": "❄️"
    },
    "energy": {
      "current": user.energy,
      "max": 5,
      "next_refill_in_seconds": user.next_refill_in_seconds
    }
  },
  "quests":user.quests
}