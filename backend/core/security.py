from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from config import settings
from database.models import User_DB, RefreshToken_DB
from database import BaseDao
from schemas import User_Login
import secrets

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
user_dao = BaseDao(User_DB)
token_dao = BaseDao(RefreshToken_DB)

async def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)

async def get_password_hash(password) -> str:
    return password_hash.hash(password)

async def get_user(username: str) -> Optional[User_DB]:
    return await user_dao.get_by_username(username)

async def authenticate_user(user_login: User_Login) -> Optional[User_DB]:
    user: User_DB = await get_user(user_login.username)
    if not user:
        return False
    if not await verify_password(user_login.password, user.password):
        return False
    return user


async def create_access_token(user: User_DB, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub":user.username,
        "exp":expire,
        "type":"access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)

async def save_refresh_token(token: str, user_id):
    await token_dao.create_entity({"name": token, "user_id":user_id, "expires_at":datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)})
    
async def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User_DB:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        user = await get_user(username)
        return user
    except InvalidTokenError:
        raise HTTPException("inkorrect token")

async def get_refresh_token(refresh_token:str):
    token: RefreshToken_DB = await token_dao.get_by_name(refresh_token)
    return token
    

async def delete_refresh_token(refresh_token:str):
    token: RefreshToken_DB = await token_dao.get_by_name(refresh_token)
    await token_dao.delete_entity_by_id(token.id)

