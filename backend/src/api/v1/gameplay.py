from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from core.security import auth_user, require
from core.config import settings
from database.relational_db import User
from service.gameplay import (
    get_casino_service,
    get_profile_service,
    get_leaderboard_service,
    get_admin_service,
    get_launch_service,
)
from domain.gameplay import (
    ProfilePatch,
    ProfileResponse,
    RedeemTokenResponse,
    Balance,
    MainResponse,
    BetRequest,
    SpinResponse,
    LeaderboardType,
    LeaderboardEntry,
    GameConfig,
    GameStartResponse,
    GameScoreRequest,
    GameScoreResponse,
    AdminRedeemRequest,
    AdminRedeemResponse,
)


def get_gameplay_router() -> APIRouter:
    router = APIRouter(prefix="", tags=["Gameplay"])

    @router.post("/games/{game_id}/launch")
    async def launch_game(
        game_id: str,
        user: Annotated[User, Depends(auth_user)],
        launch_svc=Depends(get_launch_service),
    ):
        code, session_id = await launch_svc.create_launch(user, game_id)
        launch_url = f"{settings.GAME_URL}?sid={session_id}#code={code}"
        return {"launch_url": launch_url, "session_id": session_id}

    # Profile
    @router.get("/profile/me", response_model=ProfileResponse)
    async def profile_me(
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.get_profile(user)

    @router.patch("/profile/me", response_model=ProfileResponse)
    async def profile_patch(
        payload: ProfilePatch,
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.patch_profile(payload, user)

    @router.post("/profile/inventory/{item_id}/code", response_model=RedeemTokenResponse)
    async def inventory_code(
        item_id: UUID,
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_casino_service),
    ):
        return await svc.generate_redeem_token(item_id, user)

    @router.get("/profile/balance", response_model=Balance)
    async def profile_balance(
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.balance(user)

    # Main
    @router.get("/main", response_model=MainResponse)
    async def main(
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.main(user)

    # Casino
    @router.post("/casino/spin", response_model=SpinResponse)
    async def casino_spin(
        bet: BetRequest,
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_casino_service),
    ):
        return await svc.spin(bet, user)

    # Leaderboard
    @router.get("/leaderboard", response_model=list[LeaderboardEntry])
    async def leaderboard(
        type: LeaderboardType,
        svc=Depends(get_leaderboard_service),
    ):
        return await svc.get(type)

    # Game
    @router.get("/game/config", response_model=GameConfig)
    async def game_config(
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.game_config(user)

    @router.post("/game/start", response_model=GameStartResponse)
    async def game_start(
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.apply_game_start(user)

    @router.post("/game/score", response_model=GameScoreResponse)
    async def game_score(
        payload: GameScoreRequest,
        user: Annotated[User, Depends(auth_user)],
        svc=Depends(get_profile_service),
    ):
        return await svc.apply_game_score(user, payload)

    # Admin
    @router.post(
        "/admin/prizes/redeem",
        response_model=AdminRedeemResponse,
        dependencies=[Depends(require("admin"))],
    )
    async def redeem_prize(
        payload: AdminRedeemRequest,
        svc=Depends(get_admin_service),
    ):
        return await svc.redeem(payload.redeem_token)

    return router
