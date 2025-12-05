from fastapi import Depends

from database.redis import CacheRepo, get_redis
from database.relational_db import (
    LanguagesInterface,
    RolesInterface,
    UserInterface,
    UoW,
    get_uow,
)
from .user_service import UserService


async def get_user_service(
    uow: UoW = Depends(get_uow),
    redis = Depends(get_redis),
) -> UserService:
    user_repo = UserInterface(uow.session)
    lang_repo = LanguagesInterface(uow.session)
    role_repo = RolesInterface(uow.session)
    cache_repo = CacheRepo(redis) if redis else None
    return UserService(uow, user_repo, lang_repo, role_repo, cache_repo)
