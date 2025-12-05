from typing import Annotated
from fastapi import Depends

from database.relational_db import (
    UoW,
    get_uow,
    PrizesInterface,
    InventoryInterface,
    TokenQRInterface,
    TeamsInterface,
)
from .casino_service import CasinoService
from .profile_service import ProfileService
from .leaderboard_service import LeaderboardService
from .admin_service import AdminService


async def get_casino_service(uow: Annotated[UoW, Depends(get_uow)]) -> CasinoService:
    prizes_repo = PrizesInterface(uow.session)
    inventory_repo = InventoryInterface(uow.session)
    token_repo = TokenQRInterface(uow.session)
    return CasinoService(uow, prizes_repo, inventory_repo, token_repo)


async def get_profile_service(uow: Annotated[UoW, Depends(get_uow)]) -> ProfileService:
    teams_repo = TeamsInterface(uow.session)
    prizes_repo = PrizesInterface(uow.session)
    inventory_repo = InventoryInterface(uow.session)
    token_repo = TokenQRInterface(uow.session)
    return ProfileService(uow, teams_repo, inventory_repo, prizes_repo, token_repo)


async def get_leaderboard_service(uow: Annotated[UoW, Depends(get_uow)]) -> LeaderboardService:
    return LeaderboardService(uow)


async def get_admin_service(uow: Annotated[UoW, Depends(get_uow)]) -> AdminService:
    prizes_repo = PrizesInterface(uow.session)
    inventory_repo = InventoryInterface(uow.session)
    token_repo = TokenQRInterface(uow.session)
    return AdminService(uow, token_repo, inventory_repo, prizes_repo)
