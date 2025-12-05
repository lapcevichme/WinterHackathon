from datetime import datetime, UTC
from fastapi import HTTPException, status

from database.relational_db import (
    UoW,
    TokenQRInterface,
    InventoryInterface,
    PrizesInterface,
    User,
)
from domain.gameplay import AdminRedeemResponse, ItemStatus


class AdminService:
    def __init__(
        self,
        uow: UoW,
        token_repo: TokenQRInterface,
        inventory_repo: InventoryInterface,
        prizes_repo: PrizesInterface,
    ):
        self.uow = uow
        self.token_repo = token_repo
        self.inventory_repo = inventory_repo
        self.prizes_repo = prizes_repo

    async def redeem(self, redeem_token: str) -> AdminRedeemResponse:
        token_row = await self.token_repo.get_by_token(redeem_token)
        if token_row is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Token not found")
        if token_row.expires_at < datetime.now(UTC):
            await self.token_repo.delete(token_row)
            await self.uow.commit()
            raise HTTPException(status.HTTP_410_GONE, detail="Token expired")

        item = await self.inventory_repo.get_by_id(token_row.item_id)
        if item is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Item not found")
        prize = await self.prizes_repo.get_by_id(item.prize_id)
        user = await self.uow.session.get(User, item.user_id)

        await self.inventory_repo.set_status(item.id, ItemStatus.REDEEMED.value)
        await self.token_repo.delete(token_row)
        await self.uow.commit()

        return AdminRedeemResponse(
            item_name=prize.name if prize else "Prize",
            user_display_name=user.display_name if user else None,
            redeemed_at=datetime.now(UTC),
        )
