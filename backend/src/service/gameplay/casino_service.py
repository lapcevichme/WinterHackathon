import random
from datetime import timedelta, UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import Settings
from database.relational_db import (
    UoW,
    User,
    Prize,
    InventoryItem,
    TokenQR,
    PrizesInterface,
    InventoryInterface,
    TokenQRInterface,
)
from domain.gameplay import (
    BetRequest,
    PrizeType,
    ItemStatus,
    SpinResponse,
    RedeemTokenResponse,
)
from service.gameplay.utils import generate_qr_token

settings = Settings()  # type: ignore


class CasinoService:
    def __init__(
        self,
        uow: UoW,
        prizes_repo: PrizesInterface,
        inventory_repo: InventoryInterface,
        token_repo: TokenQRInterface,
    ):
        self.uow = uow
        self.prizes_repo = prizes_repo
        self.inventory_repo = inventory_repo
        self.token_repo = token_repo

    async def _pick_prize(self) -> Prize:
        prizes = await self.prizes_repo.list_all()
        if not prizes:
            raise HTTPException(status.HTTP_409_CONFLICT, "No prizes configured")
        return random.choice(prizes)

    async def spin(self, bet: BetRequest, user) -> SpinResponse:
        db_user = await self.uow.session.get(User, user.id)
        if db_user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        if db_user.amount < bet.bet:
            raise HTTPException(
                status.HTTP_402_PAYMENT_REQUIRED,
                detail={"error_code": "insufficient_funds", "message": "Not enough coins"},
            )

        prize = await self._pick_prize()

        # Apply winnings
        if prize.type == PrizeType.MONEY:
            db_user.amount += prize.amount - bet.bet
        else:
            db_user.amount -= bet.bet
            item = InventoryItem(
                prize_id=prize.id,
                user_id=db_user.id,
                status=ItemStatus.AVAILABLE.value,
            )
            await self.inventory_repo.add(item)

        await self.uow.commit()

        return SpinResponse(
            winner=prize,
            new_balance={"amount": db_user.amount, "currency_symbol": "❄️"},
        )

    async def generate_redeem_token(self, item_id: UUID, user) -> RedeemTokenResponse:
        item = await self.inventory_repo.get_by_id(item_id)
        if item is None or item.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Item not found")

        token_value = generate_qr_token()
        token_row = TokenQR(
            token=token_value,
            user_id=user.id,
            item_id=item_id,
            expires_at=datetime.now(UTC) + timedelta(seconds=300),
        )
        await self.token_repo.add(token_row)
        await self.uow.commit()
        return RedeemTokenResponse(redeem_token=token_value, expires_in_seconds=300)
