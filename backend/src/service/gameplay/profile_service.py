from datetime import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.config import Settings
from database.relational_db import (
    UoW,
    User,
    InventoryItem,
    TeamsInterface,
    InventoryInterface,
    PrizesInterface,
    TokenQRInterface,
)
from domain.gameplay import (
    ProfileResponse,
    ProfilePatch,
    Balance,
    MainResponse,
    GameConfig,
    GameStartResponse,
    GameScoreRequest,
    GameScoreResponse,
    ItemStatus,
    PrizeType,
    UserSummary,
    EnergyState,
    ActiveGame,
    InventoryItem as InventoryItemSchema,
)
from service.gameplay.utils import refill_energy

settings = Settings()  # type: ignore


class ProfileService:
    def __init__(
        self,
        uow: UoW,
        teams_repo: TeamsInterface,
        inventory_repo: InventoryInterface,
        prizes_repo: PrizesInterface,
        token_repo: TokenQRInterface,
    ):
        self.uow = uow
        self.teams_repo = teams_repo
        self.inventory_repo = inventory_repo
        self.prizes_repo = prizes_repo
        self.token_repo = token_repo

    async def _load_user(self, user_id: UUID) -> User:
        user = await self.uow.session.scalar(
            select(User)
            .options(
                selectinload(User.team),
                selectinload(User.items).selectinload(InventoryItem.prize),
            )
            .where(User.id == user_id)
        )
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    async def get_profile(self, user: User) -> ProfileResponse:
        db_user = await self._load_user(user.id)
        return ProfileResponse(
            id=db_user.id,
            username=db_user.username,
            display_name=db_user.display_name or db_user.username,
            department=db_user.team.name if db_user.team else None,
            avatar_url=db_user.url or db_user.profile_pic_url,
            level=db_user.level,
            xp=db_user.score,
            max_xp=db_user.max_score,
            inventory=[
                InventoryItemSchema(
                    id=item.id,
                    prize_id=item.prize_id,
                    name=item.prize.name,
                    type=PrizeType(item.prize.type),
                    status=ItemStatus(item.status),
                    amount=item.prize.amount,
                    emoji=item.prize.emoji,
                    color_hex=item.prize.color_hex,
                )
                for item in db_user.items
            ],
        )

    async def patch_profile(self, payload: ProfilePatch, user: User) -> ProfileResponse:
        db_user = await self._load_user(user.id)
        data = payload.model_dump(exclude_none=True)
        if "avatar_url" in data:
            db_user.url = data.pop("avatar_url")
        for key, value in data.items():
            setattr(db_user, key, value)
        await self.uow.commit()
        await self.uow.session.refresh(db_user)
        return await self.get_profile(db_user)

    async def balance(self, user: User) -> Balance:
        db_user = await self._load_user(user.id)
        return Balance(amount=db_user.amount, currency_symbol="❄️")

    async def main(self, user: User) -> MainResponse:
        db_user = await self._load_user(user.id)
        new_energy, next_refill = refill_energy(db_user.energy, db_user.updated_at)
        if new_energy != db_user.energy:
            db_user.energy = new_energy
            await self.uow.commit()
            await self.uow.session.refresh(db_user)

        return MainResponse(
            user_summary=UserSummary(
                id=db_user.id,
                display_name=db_user.display_name or db_user.username,
                balance=Balance(amount=db_user.amount, currency_symbol="❄️"),
                energy=EnergyState(
                    current=db_user.energy,
                    max=10,
                    next_refill_in_seconds=next_refill,
                ),
            ),
            active_game=ActiveGame(
                name="Snowball Fight",
                energy_cost=settings.GAME_ENERGY_COST,
                is_available=db_user.energy >= settings.GAME_ENERGY_COST,
            ),
            quests=[],
        )

    async def game_config(self, user: User) -> GameConfig:
        return GameConfig(
            game_url=settings.GAME_URL,
            energy_cost=settings.GAME_ENERGY_COST,
            user_energy=user.energy,
            can_play=user.energy >= settings.GAME_ENERGY_COST,
        )

    async def apply_game_start(self, user: User) -> GameStartResponse:
        db_user = await self._load_user(user.id)
        if db_user.energy < settings.GAME_ENERGY_COST:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not enough energy")
        db_user.energy -= settings.GAME_ENERGY_COST
        await self.uow.commit()
        await self.uow.session.refresh(db_user)
        from database.relational_db import GameSessionInterface, GameSession  # local import to avoid cycle

        session_repo = GameSessionInterface(self.uow.session)
        session_obj = GameSession(user_id=db_user.id, game_id="default", energy_cost=settings.GAME_ENERGY_COST)
        await session_repo.add(session_obj)
        await self.uow.commit()
        return GameStartResponse(session_id=session_obj.id, energy_left=db_user.energy)

    async def apply_game_score(self, user: User, payload: GameScoreRequest) -> GameScoreResponse:
        from database.relational_db import GameSessionInterface

        session_repo = GameSessionInterface(self.uow.session)
        session = await session_repo.get(payload.session_id)
        if session is None or session.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Session not found")

        session.score = payload.score
        session.completed_at = datetime.now()

        db_user = await self._load_user(user.id)

        db_user.score += payload.score
        if db_user.team_id:
            team = await self.teams_repo.get(db_user.team_id)
            if team:
                team.score += payload.score
                team.max_score = max(team.max_score, team.score)
                total_team_score = team.score
            else:
                total_team_score = None
        else:
            total_team_score = None

        await self.uow.commit()
        return GameScoreResponse(
            team_score_added=payload.score,
            total_team_score=total_team_score,
        )
