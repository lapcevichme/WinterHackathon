from typing import Annotated
from fastapi import APIRouter, Depends, Header, Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_limiter.depends import RateLimiter

from service.auth import TokenService, get_token_service
from domain.auth import TokenPair
from core.config import Settings
from core.security import extract_jti

router = APIRouter()
config = Settings() # pyright: ignore[reportCallIssue]
security = HTTPBearer(
    auto_error=False, 
    description='Send refresh token as Bearer for non-browser clients'
)


@router.post(
    path='/refresh',
    response_model=TokenPair,
    summary='Rotate tokens',
    dependencies=[Depends(RateLimiter(times=10, seconds=60, identifier=extract_jti))],
)
async def refresh_tokens(
    request: Request,
    response: Response,
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    svc: Annotated[TokenService, Depends(get_token_service)],
    x_csrf: str | None = Header(
        default=None, alias="X-CSRF-Token", 
        description='Must only be passed for requests from browsers'
    ),
) -> TokenPair:
    cookie_refresh = request.cookies.get("refresh_token")
    
    if cookie_refresh:
        if not x_csrf:
            raise HTTPException(status_code=403, detail="Missing CSRF token")
        
        result = await svc.refresh_tokens(cookie_refresh, x_csrf)
        if result is None:
            # token invalid or csrf mismatch
            response.delete_cookie("refresh_token", samesite="lax")
            response.delete_cookie("csrf_token", samesite="lax")
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        new_access, new_refresh, new_csrf = result
        
        # set fresh cookies
        response.set_cookie(
            "refresh_token", new_refresh,
            max_age=config.REFRESH_TTL,
            httponly=True, 
            secure=True,
            samesite="none",
            path='/',
        )
        response.set_cookie(
            "csrf_token", new_csrf,
            max_age=config.REFRESH_TTL,
            httponly=False, 
            secure=True, 
            samesite="none",
            path='/',
        )

        # body: only short-lived access token
        return TokenPair(access_token=new_access, refresh_token=None)
        
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    result = await svc.refresh_tokens(creds.credentials)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access, new_refresh, _ = result
    return TokenPair(access_token=new_access, refresh_token=new_refresh)
