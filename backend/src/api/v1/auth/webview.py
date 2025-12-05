from typing import Annotated
from fastapi import APIRouter, Depends, Response, HTTPException, Header
from pydantic import BaseModel, Field

from core.config import Settings
from core.security import auth_user
from service.auth import TokenService, get_token_service
from service.gameplay.launch_service import LaunchService, get_launch_service
from domain.auth import TokenPair
from database.relational_db import User

settings = Settings()  # pyright: ignore[reportCallIssue]
router = APIRouter()


class LaunchExchangeRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=128)


@router.post(
    path="/webview/exchange",
    response_model=TokenPair,
    summary="Exchange launch code for web session tokens",
)
async def exchange_code(
    response: Response,
    payload: LaunchExchangeRequest,
    token_svc: Annotated[TokenService, Depends(get_token_service)],
    launch_svc: Annotated[LaunchService, Depends(get_launch_service)],
):
    user = await launch_svc.consume_code(payload.code)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid or expired code")

    access, refresh, csrf = await token_svc.issue_tokens(user, src="web")

    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=settings.REFRESH_TTL,
        httponly=True,
        secure=True,
        samesite="none",
        path='/',
    )
    response.set_cookie(
        'csrf_token',
        csrf,
        max_age=settings.REFRESH_TTL,
        secure=True,
        httponly=False,
        samesite='none',
        path='/',
    )

    return TokenPair(access_token=access, refresh_token=None)
