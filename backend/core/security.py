from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
import jwt
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config import settings
from database.models import User_DB, RefreshToken_DB
from database.basedao import BaseDao
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

user_dao = BaseDao(User_DB)
refresh_token_dao = BaseDao(RefreshToken_DB)

# Проверка мобильного клиента
async def verify_mobile_client(client_mobile: Optional[str] = Header(None)):
    """Проверяет, является ли клиент мобильным приложением"""
    if client_mobile != "true":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is only for mobile clients"
        )
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_user(username: str) -> Optional[User_DB]:
    return await user_dao.get_by_username(username)

async def authenticate_user(username: str, password: str) -> Optional[User_DB]:
    user = await get_user(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token() -> str:
    """Создает случайный refresh token"""
    return secrets.token_urlsafe(64)

async def save_refresh_token(user_id: int, refresh_token: str, expires_delta: timedelta):
    """Сохраняет refresh token в базу данных"""
    # Используем naive datetime для PostgreSQL
    expires_at = datetime.now() + expires_delta
    token_data = {
        "token": refresh_token,
        "user_id": user_id,
        "expires_at": expires_at,
        "is_blacklisted": False
    }
    await refresh_token_dao.create_entity(token_data)

async def get_refresh_token(token: str) -> Optional[RefreshToken_DB]:
    """Получает refresh token из базы с eager loading пользователя"""
    async with refresh_token_dao.async_session_maker() as session:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from datetime import datetime
        
        result = await session.execute(
            select(RefreshToken_DB)
            .options(selectinload(RefreshToken_DB.user))
            .where(
                RefreshToken_DB.token == token,
                RefreshToken_DB.is_blacklisted == False,
                RefreshToken_DB.expires_at > datetime.now()
            )
        )
        return result.scalars().first()

async def blacklist_refresh_token(token: str):
    """Добавляет refresh token в черный список"""
    async with refresh_token_dao.async_session_maker() as session:
        from sqlalchemy import select
        from datetime import datetime
        
        result = await session.execute(
            select(RefreshToken_DB)
            .where(
                RefreshToken_DB.token == token,
                RefreshToken_DB.expires_at > datetime.now()
            )
        )
        refresh_token = result.scalars().first()
        
        if refresh_token:
            refresh_token.is_blacklisted = True
            await session.commit()

async def get_user_by_id(user_id: int) -> Optional[User_DB]:
    """Получает пользователя по ID"""
    return await user_dao.get_entity_by_id(user_id)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User_DB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Проверяем, что это access token
        if payload.get("type") != "access":
            raise credentials_exception
            
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User_DB, Depends(get_current_user)]) -> User_DB:
    return current_user