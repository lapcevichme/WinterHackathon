from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter


def get_auth_routers() -> APIRouter:
    from .registration import router as register_router
    from .login import router as login_router
    from .refresh import router as refresh_router
    
    router = APIRouter(
        prefix='/auth', 
        tags=['Auth'],
        responses={
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            429: {"description": "Too Many Requests"}
        },
        dependencies=[Depends(RateLimiter(times=10, seconds=60))]
    )
    
    router.include_router(register_router)
    router.include_router(login_router)
    router.include_router(refresh_router)
    
    return router
