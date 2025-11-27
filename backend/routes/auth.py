from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token, User, User_Login
from core.security import (
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    get_password_hash
)
from database.models import User_DB
from database.basedao import BaseDao
from config import settings

auth_router = APIRouter()
user_basedao = BaseDao(User_DB)


@auth_router.post("/register", status_code=201)
async def user_register(user: User):
    user.password = get_password_hash(user.password)
    await user_basedao.create_entity(user.model_dump())
    return {"user": user}
    
    
@auth_router.post("/login", response_model=Token)
async def login_for_access_token(credentials: User_Login):
    """Логин и получение JWT токена через JSON"""
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@auth_router.get("/verifytoken")
async def verify_token(current_user: User_DB = Depends(get_current_active_user)):
    """Проверка валидности токена"""
    return {
        "message": "Token is valid",
        "username": current_user.username,
        "user_id": current_user.user_id
    }