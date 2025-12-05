from fastapi import APIRouter


def get_admins_router() -> APIRouter:
    from .books import get_books_router
    from .users import get_users_router
    from .stats import get_stats_router
    from .exchanges import get_exchanges_router
    
    router = APIRouter(prefix='/admins', tags=['Admins'])

    router.include_router(get_books_router())
    router.include_router(get_users_router())
    router.include_router(get_stats_router())
    router.include_router(get_exchanges_router())
    
    return router
