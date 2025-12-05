from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path

from api import get_api_routers
from webhooks import get_webhooks
from core.config import Settings, configure_logging, BASE_DIR
from database.redis import get_redis
# from scheduler import init_scheduler


config = Settings() # pyright: ignore[reportCallIssue]
configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = get_redis()
    try:
        await FastAPILimiter.init(redis)
        yield
    finally:
        await redis.aclose()


app = FastAPI(
    lifespan=lifespan,
    title='Winter Hack',
    debug=True
)

# Mount static
# app.mount('/media', StaticFiles(directory=config.MEDIA_DIR, check_dir=False), 'media')
app.mount(
    '/.well-known',
    StaticFiles(directory=Path(BASE_DIR, ".well-known"), check_dir=False),
    name='well-known'
)

# Including routers
app.include_router(get_api_routers())
app.include_router(get_webhooks())

@app.get('/')
@app.get('/ping')
async def ping():
    return {'status': 'operating'}


# Adding middlewares
allowed_origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

if config.SITE_URL:
    allowed_origins.append(config.SITE_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers=['X-CSRF-Token', 'X-Requested-With', 'Accept', 'Content-Type', 'Authorization', 'X-Client'],
    allow_credentials=True,
)
