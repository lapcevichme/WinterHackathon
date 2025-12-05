from typing import Sequence
from fastapi import HTTPException
from sqlalchemy import select

from database.relational_db import UoW, User, Team
from domain.gameplay import LeaderboardType, LeaderboardEntry, Trend


class LeaderboardService:
    def __init__(self, uow: UoW):
        self.uow = uow

    async def _players(self) -> list[LeaderboardEntry]:
        users = await self.uow.session.scalars(select(User))
        ranked = sorted(users.all(), key=lambda u: u.score, reverse=True)
        return [
            LeaderboardEntry(rank=i + 1, name=u.display_name or u.username or "Player", score=u.score, trend=Trend.SAME)
            for i, u in enumerate(ranked)
        ]

    async def _departments(self) -> list[LeaderboardEntry]:
        teams = await self.uow.session.scalars(select(Team))
        ranked = sorted(teams.all(), key=lambda t: t.score, reverse=True)
        return [
            LeaderboardEntry(rank=i + 1, name=t.name, score=t.score, trend=Trend.SAME)
            for i, t in enumerate(ranked)
        ]

    async def get(self, lb_type: LeaderboardType) -> list[LeaderboardEntry]:
        if lb_type == LeaderboardType.PLAYERS:
            return await self._players()
        if lb_type == LeaderboardType.DEPARTMENTS:
            return await self._departments()
        raise HTTPException(400, "Unknown leaderboard type")
