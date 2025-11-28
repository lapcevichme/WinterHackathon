from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header

from schemas import Token, User, User_Login, RefreshTokenRequest
from core.security import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    get_password_hash,
    create_refresh_token,
    save_refresh_token,
    get_refresh_token,
    blacklist_refresh_token,
    verify_mobile_client,
    get_user_by_id
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
    # Проверяем мобильный клиент
    await verify_mobile_client(client_mobile)
    
    # Проверяем, существует ли пользователь
    existing_user = await user_basedao.get_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    user.password = get_password_hash(user.password)
    created_user = await user_basedao.create_entity(user.model_dump())
    
    # Создаем токены
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token()
    
    # Сохраняем refresh token
    await save_refresh_token(created_user.user_id, refresh_token, refresh_token_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
@auth_router.post("/login", response_model=Token)
async def login_for_access_token(
    credentials: User_Login,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Логин и получение JWT токенов через JSON для мобильного приложения"""
    # Проверяем мобильный клиент
    await verify_mobile_client(client_mobile)
    
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токены
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token()
    
    # Сохраняем refresh token
    await save_refresh_token(user.user_id, refresh_token, refresh_token_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/refresh")
async def refresh_tokens(
    request: RefreshTokenRequest,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Обновление пары токенов"""
    # Проверяем мобильный клиент
    await verify_mobile_client(client_mobile)
    
    # Проверяем refresh token
    refresh_token_obj = await get_refresh_token(request.refresh_token)
    if not refresh_token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Получаем пользователя из refresh token (уже загружен через eager loading)
    user = refresh_token_obj.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found for this refresh token"
        )
    
    # Создаем новые токены
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    new_access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token()
    
    # Старый refresh token добавляем в черный список
    await blacklist_refresh_token(request.refresh_token)
    
    # Сохраняем новый refresh token
    await save_refresh_token(user.user_id, new_refresh_token, refresh_token_expires)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/logout")
async def logout(
    request: RefreshTokenRequest,
    client_mobile: str = Header(..., alias="Client-Mobile")
):
    """Выход из системы - добавление refresh token в черный список"""
    # Проверяем мобильный клиент
    await verify_mobile_client(client_mobile)
    
    await blacklist_refresh_token(request.refresh_token)
    
    return {"message": "Successfully logged out"}

@auth_router.get("/verifytoken")
async def verify_token(current_user: User_DB = Depends(get_current_active_user)):
    """Проверка валидности токена"""
    return {
        "message": "Token is valid",
        "username": current_user.username,
        "user_id": current_user.user_id
    }