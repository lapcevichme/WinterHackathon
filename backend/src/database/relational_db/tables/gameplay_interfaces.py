from uuid import UUID
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .gameplay import Prize, InventoryItem, TokenQR, GameSession, Team, LaunchCode


class PrizesInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(self) -> Sequence[Prize]:
        prizes = await self.session.scalars(select(Prize))
        return prizes.all()

    async def get_by_id(self, prize_id: UUID) -> Prize | None:
        return await self.session.get(Prize, prize_id)

    async def get_by_name(self, name: str) -> Prize | None:
        return await self.session.scalar(select(Prize).where(Prize.name == name))

    async def add(self, prize: Prize) -> Prize:
        self.session.add(prize)
        await self.session.flush()
        return prize


class InventoryInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: UUID) -> InventoryItem | None:
        return await self.session.get(InventoryItem, item_id)

    async def add(self, item: InventoryItem) -> InventoryItem:
        self.session.add(item)
        await self.session.flush()
        return item

    async def set_status(self, item_id: UUID, status: str) -> int:
        stmt = (
            update(InventoryItem)
            .where(InventoryItem.id == item_id)
            .values(status=status)
        )
        res = await self.session.execute(stmt)
        await self.session.flush()
        return res.rowcount or 0


class TokenQRInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_token(self, token: str) -> TokenQR | None:
        return await self.session.scalar(select(TokenQR).where(TokenQR.token == token))

    async def add(self, token_qr: TokenQR) -> TokenQR:
        self.session.add(token_qr)
        await self.session.flush()
        return token_qr

    async def delete(self, token_qr: TokenQR) -> None:
        await self.session.delete(token_qr)
        await self.session.flush()


class GameSessionInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, session_obj: GameSession) -> GameSession:
        self.session.add(session_obj)
        await self.session.flush()
        return session_obj

    async def get(self, session_id: UUID) -> GameSession | None:
        return await self.session.get(GameSession, session_id)


class TeamsInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Sequence[Team]:
        teams = await self.session.scalars(select(Team))
        return teams.all()

    async def get(self, team_id: UUID) -> Team | None:
        return await self.session.get(Team, team_id)


class LaunchCodeInterface:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, launch_code: LaunchCode) -> LaunchCode:
        self.session.add(launch_code)
        await self.session.flush()
        return launch_code

    async def get_by_code(self, code: str) -> LaunchCode | None:
        return await self.session.scalar(select(LaunchCode).where(LaunchCode.code == code))
