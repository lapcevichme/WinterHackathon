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

def create_access_token_with_role(user: User_DB, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен с ролью пользователя"""
    to_encode = {
        "sub": user.username,
        "role": user.role,
        "user_id": user.user_id
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

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

async def get_current_user_with_role(token: Annotated[str, Depends(oauth2_scheme)]) -> User_DB:
    """Получает пользователя с проверкой роли в токене"""
    user = await get_current_user(token)
    
    # Дополнительная проверка согласованности роли в токене и БД
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_role = payload.get("role")
        if token_role and token_role != user.role:
            # Логируем несоответствие ролей (для безопасности)
            print(f"Warning: Role mismatch for user {user.username}. Token: {token_role}, DB: {user.role}")
    except Exception:
        pass  # Игнорируем ошибки декодирования для этой проверки
    
    return user

async def get_current_active_user(current_user: Annotated[User_DB, Depends(get_current_user)]) -> User_DB:
    return current_user

async def get_current_active_user_with_role(current_user: Annotated[User_DB, Depends(get_current_user_with_role)]) -> User_DB:
    return current_user

def require_role(required_role: str):
    """Зависимость для проверки ролей"""
    async def role_checker(current_user: User_DB = Depends(get_current_user_with_role)):
        if current_user.role != required_role and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

def require_any_role(required_roles: list):
    """Зависимость для проверки любой из ролей"""
    async def role_checker(current_user: User_DB = Depends(get_current_user_with_role)):
        if current_user.role not in required_roles and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {required_roles}"
            )
        return current_user
    return role_checker

def require_admin():
    """Зависимость для проверки админской роли"""
    return require_role("admin")

def require_moderator_or_admin():
    """Зависимость для проверки роли модератора или админа"""
    return require_any_role(["moderator", "admin"])

def require_player_or_higher():
    """Зависимость для проверки роли игрока или выше"""
    return require_any_role(["player", "moderator", "admin"])

# Вспомогательные функции для работы с ролями
def get_user_roles():
    """Возвращает список доступных ролей"""
    return ["player", "moderator", "admin"]

def is_admin(user: User_DB) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return user.role == "admin"

def is_moderator(user: User_DB) -> bool:
    """Проверяет, является ли пользователь модератором"""
    return user.role == "moderator"

def is_player(user: User_DB) -> bool:
    """Проверяет, является ли пользователь игроком"""
    return user.role == "player"

def has_permission(user: User_DB, required_permission: str) -> bool:
    """Проверяет, имеет ли пользователь определенное разрешение"""
    permissions = {
        "player": ["read_own_profile", "play_games", "buy_items"],
        "moderator": ["read_own_profile", "play_games", "buy_items", "view_stats", "manage_users"],
        "admin": ["read_own_profile", "play_games", "buy_items", "view_stats", "manage_users", "manage_system"]
    }
    
    user_permissions = permissions.get(user.role, [])
    return required_permission in user_permissions

async def create_user_with_role(user_data: dict) -> User_DB:
    """Создает пользователя с указанной ролью"""
    # Валидация роли
    valid_roles = get_user_roles()
    if user_data.get('role') not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    # Хешируем пароль
    if 'password' in user_data:
        user_data['password'] = get_password_hash(user_data['password'])
    
    return await user_dao.create_entity(user_data)

async def update_user_role(user_id: int, new_role: str, current_user: User_DB):
    """Обновляет роль пользователя (только для админов)"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can change user roles"
        )
    
    # Валидация роли
    valid_roles = get_user_roles()
    if new_role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    # Не позволяем убрать админские права у себя
    if user_id == current_user.user_id and new_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove admin role from yourself"
        )
    
    user = await user_dao.get_entity_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Обновляем роль
    user.role = new_role
    await user_dao.update_entity(user_id, {"role": new_role})
    
    return user

# Функции для декодирования токенов без проверки (для тестирования)
def decode_token_without_verification(token: str) -> dict:
    """Декодирует JWT токен без проверки подписи (только для тестирования)"""
    return jwt.decode(token, options={"verify_signature": False})

def get_role_from_token(token: str) -> Optional[str]:
    """Извлекает роль из JWT токена (только для тестирования)"""
    try:
        payload = decode_token_without_verification(token)
        return payload.get('role')
    except Exception:
        return None

def get_username_from_token(token: str) -> Optional[str]:
    """Извлекает username из JWT токена (только для тестирования)"""
    try:
        payload = decode_token_without_verification(token)
        return payload.get('sub')
    except Exception:
        return None