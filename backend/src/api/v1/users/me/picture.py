from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File

from database.relational_db import User
from domain.users import UserModel
from core.config import Settings
from core.security import auth_user
from service.users import UserService, get_user_service

router = APIRouter()
config = Settings() # pyright: ignore[reportCallIssue]


@router.put(
    path='/picture',
    response_model=UserModel,
    summary='Update user profile picture'
)
async def update_profile(
    file: Annotated[UploadFile, File(..., description=f"JPEG or PNG files (max {config.MAX_PHOTO_SIZE} MB)")],
    user: Annotated[User, Depends(auth_user)],
    svc: Annotated[UserService, Depends(get_user_service)],
):
    await svc.add_picture(file, user)
    return user
