import aiofiles
import shutil
from datetime import datetime

from uuid import UUID, uuid4
from pathlib import Path
from fastapi import UploadFile, status, HTTPException

from core.config import Settings
# from core.rbac import permissions_cache_key
from database.redis import CacheRepo
from domain.users import UserPatch
from database.relational_db import (
    LanguagesInterface,
    RolesInterface,
    UserInterface,
    UoW,
    User,
    Role,
)

settings = Settings()  # type: ignore


class UserService:
    def __init__(
        self,
        uow: UoW,
        user_repo: UserInterface,
        lang_repo: LanguagesInterface,
        role_repo: RolesInterface,
        cache_repo: CacheRepo | None = None,
    ):
        self.uow = uow
        self.user_repo = user_repo
        self.lang_repo = lang_repo
        self.role_repo = role_repo
        self.cache_repo = cache_repo
        
    async def get_user(self, user_id: UUID | str) -> User | None:
        return await self.user_repo.get_by_id(user_id)
        
    async def patch_user(self, payload: UserPatch, user: User):
        data = payload.model_dump(exclude_none=True)
        
        for field, value in data.items():
            setattr(user, field, value)
            
        await self.uow.commit()
            
        await self.uow.session.refresh(user)

    async def add_picture(
        self,
        file: UploadFile,
        user: User
    ) -> None:
        folder = Path(settings.MEDIA_DIR, "users", str(user.id))
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)

        if file.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only jpg / png allowed"
            )

        ext  = ".jpg" if file.content_type == "image/jpeg" else ".png"
        name = f"{uuid4()}{ext}"

        file_path = folder / name
        limit_bytes = settings.MAX_PHOTO_SIZE * 1024 * 1024
        written = 0
        async with aiofiles.open(file_path, "wb") as out:
            while chunk := await file.read(1024 * 1024):
                if written + len(chunk) > limit_bytes:
                    try:
                        await out.flush()
                        await out.close()
                    except Exception:
                        pass
                    try:
                        file_path.unlink(missing_ok=True)
                    except Exception:
                        pass
                    raise HTTPException(
                        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File too large. Max {settings.MAX_PHOTO_SIZE} MB"
                    )
                await out.write(chunk)
                written += len(chunk)

        url = f"{settings.SITE_URL}/{settings.MEDIA_DIR}/users/{user.id}/{name}"

        user.profile_pic_url = url

    async def admin_list_users(
        self,
        *,
        banned: bool | None = None,
        search: str | None = None,
        limit: int = 50,
        cursor: str | None = None,
    ) -> tuple[list[User], str | None]:
        cursor_created_at = None
        cursor_id = None
        if cursor:
            try:
                ts_str, id_str = cursor.split("_", 1)
                cursor_created_at = datetime.fromisoformat(ts_str)
                cursor_id = UUID(id_str)
            except Exception:
                raise HTTPException(400, detail='Invalid cursor')

        users = await self.user_repo.admin_list_users(
            banned=banned,
            search=search,
            limit=limit,
            cursor_created_at=cursor_created_at,
            cursor_id=cursor_id,
        )

        next_cursor = None
        if len(users) == limit:
            last = users[-1]
            if last.created_at is None:
                next_cursor = None
            else:
                next_cursor = f"{last.created_at.isoformat()}_{last.id}"

        return users, next_cursor

    async def admin_set_ban(self, target: User, banned: bool) -> User:
        previous_version = target.auth_version
        target.banned = banned
        target.bump_auth_version()
        await self.uow.commit()
        await self.uow.session.refresh(target)
        # await self._invalidate_permissions_cache(target.id, previous_version)
        return target

    async def list_languages(self, search: str, limit: int):
        return await self.lang_repo.search(search, limit)

    async def admin_assign_roles(
        self,
        target: User,
        role_slugs: list[str],
    ) -> User:
        unique_slugs = list(dict.fromkeys(role_slugs))
        roles = await self.role_repo.get_by_slugs(unique_slugs)
        found_slugs = {role.slug for role in roles}
        missing = [slug for slug in unique_slugs if slug not in found_slugs]
        if missing:
            missing_sorted = ", ".join(sorted(missing))
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"Unknown roles: {missing_sorted}",
            )

        previous_version = target.auth_version
        await self.user_repo.assign_roles(target, roles)
        target.bump_auth_version()
        await self.uow.commit()
        await self.uow.session.refresh(target)

        # await self._invalidate_permissions_cache(target.id, previous_version)
        return target

    # async def _invalidate_permissions_cache(
    #     self,
    #     user_id: UUID | str,
    #     previous_version: int | None,
    # ) -> None:
    #     if not self.cache_repo or previous_version is None:
    #         return
    #     cache_key = permissions_cache_key(user_id, previous_version)
    #     await self.cache_repo.delete(cache_key)
