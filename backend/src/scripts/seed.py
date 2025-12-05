import asyncio
from datetime import datetime
from uuid import uuid4

from sqlalchemy import text, select

from core.crypto import hash_password
from core.config import Settings
from database.relational_db import (
    UoW,
    get_uow,
    User,
    Team,
    Prize,
    InventoryItem,
    RolesInterface,
    UserInterface,
    PrizesInterface,
    InventoryInterface,
    TeamsInterface,
)
from domain.gameplay import PrizeType, ItemStatus


settings = Settings()  # type: ignore


TEAMS = [
    {"name": "Backend", "score": 1500, "max_score": 2000},
    {"name": "Frontend", "score": 900, "max_score": 1300},
    {"name": "Mobile", "score": 1200, "max_score": 1600},
    {"name": "Data", "score": 600, "max_score": 800},
]

PRIZES = [
    {"name": "100 Coins", "type": PrizeType.MONEY, "amount": 100, "emoji": "💰", "color_hex": "#FFD700"},
    {"name": "500 Coins", "type": PrizeType.MONEY, "amount": 500, "emoji": "💰", "color_hex": "#FFD700"},
    {"name": "Sticker Pack", "type": PrizeType.ITEM, "amount": 1, "emoji": "😎", "color_hex": "#FF0000"},
    {"name": "T-Shirt", "type": PrizeType.ITEM, "amount": 1, "emoji": "👕", "color_hex": "#336699"},
    {"name": "Mystery Trash", "type": PrizeType.TRASH, "amount": 1, "emoji": "🗑️", "color_hex": "#777777"},
]

USERS = [
    {
        "email": "admin@example.com",
        "username": "admin",
        "display_name": "Admin",
        "password": "Admin123!",
        "role": "admin",
        "amount": 5000,
        "score": 2000,
        "max_score": 2500,
    },
    {
        "email": "player1@example.com",
        "username": "player1",
        "display_name": "Player One",
        "password": "player123",
        "role": "player",
        "amount": 1500,
        "score": 1200,
        "max_score": 1500,
    },
    {
        "email": "player2@example.com",
        "username": "player2",
        "display_name": "Player Two",
        "password": "player123",
        "role": "player",
        "amount": 900,
        "score": 800,
        "max_score": 1000,
    },
    {
        "email": "player3@example.com",
        "username": "player3",
        "display_name": "Player Three",
        "password": "player123",
        "role": "player",
        "amount": 400,
        "score": 300,
        "max_score": 600,
    },
]


async def seed(reset: bool = True) -> None:
    async for uow in get_uow():
        user_repo = UserInterface(uow.session)
        team_repo = TeamsInterface(uow.session)
        prize_repo = PrizesInterface(uow.session)
        inventory_repo = InventoryInterface(uow.session)
        role_repo = RolesInterface(uow.session)

        if reset:
            # Truncate in FK-safe order
            for table in ("token_qr", "inventory_items", "game_sessions", "users", "prizes", "teams"):
                await uow.session.execute(text(f'TRUNCATE "{table}" CASCADE;'))
            await uow.session.commit()

        # Teams
        teams = []
        for t in TEAMS:
            team = Team(**t)
            uow.session.add(team)
            teams.append(team)
        await uow.session.flush()

        # Users
        for i, u in enumerate(USERS):
            password_hash = await hash_password(u.pop("password"))
            team_id = teams[i % len(teams)].id if teams else None
            user = User(
                password_hash=password_hash,
                team_id=team_id,
                **u,
            )
            uow.session.add(user)
        await uow.session.flush()

        # Roles assignment (admin/member)
        admin_role = await role_repo.get_by_slug("admin")
        member_role = await role_repo.get_by_slug("member")
        if admin_role or member_role:
            users_list = await uow.session.scalars(select(User.id))
            for user_id in users_list.all():
                user_obj = await user_repo.get_by_id(user_id)
                if user_obj is None:
                    continue
                roles = []
                if member_role:
                    roles.append(member_role)
                if user_obj.username == "admin" and admin_role:
                    roles.append(admin_role)
                if roles:
                    await user_repo.assign_roles(user_obj, roles)

        # Prizes
        prize_objs = []
        existing_names = {p.name for p in await prize_repo.list_all()}
        for p in PRIZES:
            if p["name"] in existing_names:
                continue
            prize = Prize(**p)
            prize_objs.append(prize)
            uow.session.add(prize)
        await uow.session.flush()

        # Inventory for first two players
        user_list = await uow.session.scalars(select(User.id).order_by(User.created_at))
        user_ids = list(user_list.all())
        if prize_objs and len(user_ids) >= 2:
            sample_prizes = prize_objs[:2]
            for uid in user_ids[:2]:
                for prize in sample_prizes:
                    item = InventoryItem(
                        prize_id=prize.id,
                        user_id=uid,
                        status=ItemStatus.AVAILABLE.value,
                    )
                    uow.session.add(item)

        await uow.commit()


if __name__ == "__main__":
    asyncio.run(seed(reset=True))
