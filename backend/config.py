from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER:str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    SECRET_KEY: str
    ALGORITHM: str
    class Config:
        env_file = ".env"
        
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
settings = Settings()