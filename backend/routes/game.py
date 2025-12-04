from fastapi import APIRouter, HTTPException, Depends
from database.models import User_DB, Casino_DB, Items_DB, Game_session_DB, Team_DB
from database import BaseDao
import random
from core import get_random_item, decode_access_token
from typing import List
from schemas import game_result, game_session

game_router = APIRouter()

user_basedao = BaseDao(User_DB)
team_dao = BaseDao(Team_DB)
casino_basedao = BaseDao(Casino_DB)
items_dao = BaseDao(Items_DB)
game_session_dao = BaseDao(Game_session_DB)

@game_router.get("/start", tags=["game"])
async def get_session_game(user: User_DB = Depends(decode_access_token)):
    score = user.score
    users = await user_basedao.get_all_by_score(score)
    elem = random.choice(users)
    
    while user.user_id == elem:
        elem = random.choice(users)
    
    session = await game_session_dao.create_entity({"status": "start", "user_1":user.user_id, "user_2": elem.user_id})
    return {"session": session.game_session_id,
            "user_1": session.user_1,
            "user_2": session.user_2,
            }

@game_router.post("/result", tags=["game"])
async def set_game_result(game_res: game_result):
    game_session = await game_session_dao.get_entity_by_id(game_res.session_id)
    game_session.winner_id = game_res.winner_id
    game_session.status = "end"
    user_1 = await user_basedao.get_entity_by_id(game_session.user_1)
    user_2 = await user_basedao.get_entity_by_id(game_session.user_2)
    if user_1.user_id == game_session.winner_id:
        user_1.score += game_res.score
        user_2.score -= game_res.score
        if user_1.team_uid:
            team = await team_dao.get_entity_by_id(user_1.team_uid)
            team.score += game_res
            await team_dao.update_entity(team.team_id, team.__dict__)
        if user_2.team_uid:
            team = await team_dao.get_entity_by_id(user_2.team_uid)
            team.score -= game_res
            await team_dao.update_entity(team.team_id, team.__dict__)
    else:
        user_1.score -= game_res.score
        user_2.score += game_res.score
        if user_1.team_uid:
            team = await team_dao.get_entity_by_id(user_1.team_uid)
            team.score -= game_res
            await team_dao.update_entity(team.team_id, team.__dict__)
        if user_2.team_uid:
            team = await team_dao.get_entity_by_id(user_2.team_uid)
            team.score += game_res
            await team_dao.update_entity(team.team_id, team.__dict__)
    game_session.game_score = game_res.score
    await game_session_dao.update_entity(game_session.game_session_id, game_session.__dict__)
    await user_basedao.update_entity(user_1.user_id, user_1.__dict__)
    return game_session
