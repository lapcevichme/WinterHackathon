# routes/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from schemas import Token, User, User_Login, RefreshTokenRequest
from core.security import (
    authenticate_user, 
    create_access_token_with_role,
    get_current_active_user,
    get_password_hash,
    create_refresh_token,
    save_refresh_token,
    get_refresh_token,
    blacklist_refresh_token,
    verify_mobile_client,
    get_user_by_id,
    require_role,
    require_any_role  # Добавляем этот импорт
)
from database.models import User_DB
from database.basedao import BaseDao
from config import settings

auth_router = APIRouter()
user_basedao = BaseDao(User_DB)

@auth_router.post("/register", status_code=201)
async def user_register(
    user: User,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Регистрация пользователя для мобильного приложения"""
    await verify_mobile_client(client_mobile)
    
    existing_user = await user_basedao.get_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    user.password = get_password_hash(user.password)
    
    # Убедимся, что роль сохраняется
    user_data = user.model_dump()
    print(f"Creating user with data: {user_data}")  # Для отладки
    
    created_user = await user_basedao.create_entity(user_data)
    
    # Создаем токены С РОЛЬЮ
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token_with_role(
        user=created_user, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token()
    
    await save_refresh_token(created_user.user_id, refresh_token, refresh_token_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": created_user.role
    }
    
@auth_router.post("/login")
async def login_for_access_token(
    credentials: User_Login,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Логин и получение JWT токенов через JSON для мобильного приложения"""
    await verify_mobile_client(client_mobile)
    
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токены С РОЛЬЮ
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token_with_role(
        user=user,
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token()
    
    await save_refresh_token(user.user_id, refresh_token, refresh_token_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }

@auth_router.post("/refresh")
async def refresh_tokens(
    request: RefreshTokenRequest,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Обновление пары токенов"""
    await verify_mobile_client(client_mobile)
    
    refresh_token_obj = await get_refresh_token(request.refresh_token)
    if not refresh_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = refresh_token_obj.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for this refresh token"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    new_access_token = create_access_token_with_role(
        user=user, 
        expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token()
    
    await blacklist_refresh_token(request.refresh_token)
    await save_refresh_token(user.user_id, new_refresh_token, refresh_token_expires)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "role": user.role
    }

@auth_router.post("/logout")
async def logout(
    request: RefreshTokenRequest,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Выход из системы - добавление refresh token в черный список"""
    await verify_mobile_client(client_mobile)
    
    await blacklist_refresh_token(request.refresh_token)
    
    return {"message": "Successfully logged out"}

@auth_router.get("/verifytoken")
async def verify_token(current_user: User_DB = Depends(get_current_active_user)):
    """Проверка валидности токена"""
    return {
        "message": "Token is valid",
        "username": current_user.username,
        "user_id": current_user.user_id,
        "role": current_user.role
    }

# ДОБАВЛЯЕМ АДМИН ЭНДПОИНТЫ ДЛЯ ТЕСТИРОВАНИЯ РОЛЕЙ
@auth_router.get("/admin/users")
async def get_all_users(
    current_user: User_DB = Depends(require_role("admin"))
):
    """Только админы могут получать список всех пользователей"""
    users = await user_basedao.get_entities()
    return {
        "users": [
            {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            } for user in users
        ]
    }

@auth_router.get("/user/profile")
async def get_user_profile(
    current_user: User_DB = Depends(get_current_active_user)
):
    """Любой аутентифицированный пользователь может получить свой профиль"""
    return {
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "max_score": current_user.max_score,
        "money": current_user.money
    }

@auth_router.get("/moderator/stats")
async def get_moderator_stats(
    current_user: User_DB = Depends(require_any_role(["moderator", "admin"]))
):
    """Модераторы и админы могут получать статистику"""
    return {
        "message": "Moderator statistics",
        "total_users": 100,
        "active_today": 50
    }

@auth_router.get("/debug/user/{username}")
async def debug_user_info(username: str):
    """Эндпоинт для отладки - получение информации о пользователе"""
    user = await user_basedao.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "max_score": user.max_score,
        "money": user.money
    }