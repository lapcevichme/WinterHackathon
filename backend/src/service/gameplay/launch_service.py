import secrets
from datetime import datetime, UTC, timedelta
from uuid import UUID

from fastapi import HTTPException, status

from core.config import Settings
from database.relational_db import (
    UoW,
    LaunchCode,
    LaunchCodeInterface,
    GameSessionInterface,
    GameSession,
    User,
)

settings = Settings()  # pyright: ignore[reportCallIssue]


class LaunchService:
    def __init__(
        self,
        uow: UoW,
        launch_repo: LaunchCodeInterface,
        session_repo: GameSessionInterface,
    ):
        self.uow = uow
        self.launch_repo = launch_repo
        self.session_repo = session_repo

    async def create_launch(self, user: User, game_id: str) -> tuple[str, UUID]:
        """
        Creates a game session and one-time launch code.
        Returns launch_code and session_id.
        """
        session = GameSession(
            user_id=user.id,
            game_id=game_id,
            energy_cost=settings.GAME_ENERGY_COST,
        )
        await self.session_repo.add(session)

        code = secrets.token_urlsafe(32)
        launch = LaunchCode(
            code=code,
            user_id=user.id,
            session_id=session.id,
            expires_at=datetime.now(UTC) + timedelta(seconds=120),
        )
        await self.launch_repo.add(launch)
        await self.uow.commit()
        return code, session.id

    async def consume_code(self, code: str) -> User | None:
        launch = await self.launch_repo.get_by_code(code)
        if launch is None:
            return None
        if launch.used_at or launch.expires_at < datetime.now(UTC):
            return None

        user = await self.uow.session.get(User, launch.user_id)
        if user is None:
            return None

        launch.used_at = datetime.now(UTC)
        await self.uow.commit()
        return user


# Dependency
from typing import Annotated
from fastapi import Depends
from database.relational_db import get_uow

async def get_launch_service(
    uow: Annotated[UoW, Depends(get_uow)],
) -> LaunchService:
    launch_repo = LaunchCodeInterface(uow.session)
    session_repo = GameSessionInterface(uow.session)
    return LaunchService(uow, launch_repo, session_repo)
