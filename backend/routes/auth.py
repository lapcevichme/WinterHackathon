from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from schemas import Token, User, User_Login, RefreshTokenRequest
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from core import get_password_hash, create_access_token, create_refresh_token, authenticate_user, save_refresh_token, get_user, delete_refresh_token, get_refresh_token
from database.models import User_DB
from database.basedao import BaseDao
from config import settings
auth_router = APIRouter()
user_basedao = BaseDao(User_DB)

@auth_router.post("/register", tags=["auth"])
async def register_user(user: User) -> Token:
    existing_user = await user_basedao.get_by_username(user.username)
    if existing_user :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    existing_user = await user_basedao.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user.password = await get_password_hash(user.password)
    user_db = await user_basedao.create_entity(user.model_dump())
    access_token = await create_access_token(user_db)
    refresh_token = await create_refresh_token()
    await save_refresh_token(token=refresh_token, user_id=user_db.user_id)
    return{
        "access_token":access_token,
        "refresh_token":refresh_token
    }
    
@auth_router.post("/login", tags=["auth"])
async def register_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = await create_access_token(await get_user(user.username))
    refresh_token = await create_refresh_token()
    await save_refresh_token(user_id=user.user_id, token=refresh_token)
    
    return{
        "access_token":access_token,
        "refresh_token":refresh_token
    }

@auth_router.post("/refresh", tags=["auth"])
async def refresh_tokens(
    request: RefreshTokenRequest,
):
    
    refresh_token_obj = await get_refresh_token(request.refresh_token)
    if not refresh_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    
    user = refresh_token_obj.user
    new_access_token = await create_access_token(user)
    new_refresh_token = await create_refresh_token()
    
    await delete_refresh_token(request.refresh_token)
    await save_refresh_token(user_id=user.user_id, token=new_refresh_token)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
    }

@auth_router.post("/logout", tags=["auth"])
async def logout(request: RefreshTokenRequest):
    await delete_refresh_token(request.refresh_token)
    return {"message": "Successfully logged out"}