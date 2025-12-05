from uuid import UUID
from fastapi import HTTPException

from core.config import Settings
from database.relational_db import (
    UoW,
    User,
    UserInterface,
)
from domain.statistics import Interaction

settings = Settings() # type: ignore

class StatService:
    def __init__(
        self,
        uow: UoW,
        user_repo: UserInterface,
    ):
        self.uow = uow
        self.user_repo = user_repo

        
    # async def active_users(self, days: int):
    #     return await self.be_repo.users_by_day(days)

    async def new_registrations(self, days: int):
        return await self.user_repo.registrations_by_days(days)
