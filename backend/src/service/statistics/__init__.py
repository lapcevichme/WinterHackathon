from fastapi import Depends

from database.relational_db import (
    get_uow,
    UoW,
    BookEventsInterface,
    UserInterestInterface,
    BooksInterface,
    BookStatsInterface,
    UserInterface,
)
from .statistics_service import StatService


async def get_stats_service(
    uow: UoW = Depends(get_uow),
) -> StatService:
    bv_repo = BookEventsInterface(uow.session)
    ui_repo = UserInterestInterface(uow.session)
    book_repo = BooksInterface(uow.session)
    bs_repo = BookStatsInterface(uow.session)
    user_repo = UserInterface(uow.session)
    
    return StatService(uow, bv_repo, ui_repo, book_repo, bs_repo, user_repo)
