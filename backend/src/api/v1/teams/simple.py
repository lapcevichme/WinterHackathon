from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import auth_user
from database.relational_db import get_uow, UoW, TeamsInterface, User
from domain.users import TeamModel, TeamJoinRequest
from service.users import UserService, get_user_service

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=list[TeamModel])
async def list_teams(
    uow: Annotated[UoW, Depends(get_uow)],
):
    teams_repo = TeamsInterface(uow.session)
    teams = await teams_repo.list()
    return [
        TeamModel(
            id=team.id,
            name=team.name,
            score=team.score,
            max_score=team.max_score,
        )
        for team in teams
    ]


@router.post("/join", response_model=TeamModel)
async def join_team(
    payload: TeamJoinRequest,
    user: Annotated[User, Depends(auth_user)],
    uow: Annotated[UoW, Depends(get_uow)],
    svc: Annotated[UserService, Depends(get_user_service)],
):
    teams_repo = TeamsInterface(uow.session)
    team = await teams_repo.get(payload.team_id)
    if team is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Team not found")

    await svc.set_team(user, team.id)

    return TeamModel(
        id=team.id,
        name=team.name,
        score=team.score,
        max_score=team.max_score,
    )
