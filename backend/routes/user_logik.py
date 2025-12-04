from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB, Quests_DB, Token_qr_DB, Team_DB
from database import BaseDao
import random
from schemas import Prize, get_prize, User_Bet, Redact_User
from core import decode_access_token, generate_qr_base64, get_time_diff_seconds, research_user_energy
import uuid
user_router = APIRouter()

user_basedao = BaseDao(User_DB)
team_basedao = BaseDao(Team_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)
quest_dao = BaseDao(Quests_DB)
item_token_dao = BaseDao(Token_qr_DB)

@user_router.get("/profile/balance", tags=["user"])
async def get_user_amount(user: User_DB = Depends(decode_access_token)):
    return {
        "amount": user.amount,
        "currency_symbol": random.choice(["❄️", "💰", "$", "RUB"])
    }
    
@user_router.get("/profile/me", tags=["user"])
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

@user_router.patch("/profile/me", tags=["user"])
async def patch_user(redact_info: Redact_User, user: User_DB = Depends(decode_access_token)):
    user.display_name = redact_info.display_name
    user.url = redact_info.url
    await user_basedao.update_entity(user.user_id, user)
    return user

@user_router.get("/profile/inventory/{id}/code", tags=["qr"])
async def get_qr(id: uuid.UUID, user: User_DB = Depends(decode_access_token)):
    token = generate_qr_base64()
    await item_token_dao.create_entity({"token":token, "user_id":user.user_id, "item_id":id})
    return {
        "redeem_token": token,
        "expires_in_seconds": 300
    }
    
@user_router.get("/leaderboard/team", tags=["team"])
async def get_leaderboard():
    leaders = await team_basedao.get_entities()
    for team in leaders:
        if team.score > team.max_score:
            team.max_score = team.score
            await team_basedao.update_entity(team.user_id, team.__dict__)
    leaders_sorted = sorted(leaders, key=lambda team: team.max_score, reverse=True)
    top_teamss = leaders_sorted[:10]
    return [
        {
            "username": team.username,
            "max_score": team.max_score,
            "amount": team.amount
        }
        for team in top_teamss
    ]
    

@user_router.get("/leaderboard/user", tags=["user"])
async def get_leaderboard():
    leaders = await user_basedao.get_entities()
    for user in leaders:
        if user.score > user.max_score:
            user.max_score = user.score
    leaders_sorted = sorted(leaders, key=lambda user: user.max_score, reverse=True)
    top_users = leaders_sorted[:10]
    return [
        {
            "username": user.username,
            "max_score": user.max_score,
            "amount": user.amount
        }
        for user in top_users
    ]

@user_router.post("/quests/{id}/claim", tags=["quest"])
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
    
@user_router.get("/main", tags=["user"])
async def get_main_info(user: User_DB = Depends(decode_access_token)):
  next_refill = research_user_energy(user)
  user = user_basedao.get_entity_by_id(user.user_id)
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
      "max": 10,
      "next_refill_in_seconds": next_refill
    }
  },
  "quests":user.quests
}