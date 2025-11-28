import uvicorn
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db, drop_db
from routes import auth_router, casino_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("The app has started!")
    await create_db()
    print("Database connected!")
    yield
    await drop_db()
    print("The app is shutting down!")
    
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/v1/auth")
app.include_router(casino_router, prefix="/roll")
if __name__ == "__main__":
    uvicorn.run(app)