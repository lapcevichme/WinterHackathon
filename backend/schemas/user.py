from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    max_score: int = 0
    team_id: Optional[int] = None
    role: str = "player"  # Добавляем роль по умолчанию
    
    @field_validator('password')
    @classmethod
    def password_validate(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("The password length is too small")
        return v
    
    @field_validator('role')
    @classmethod
    def role_validate(cls, v: str) -> str:
        valid_roles = ["player", "admin", "moderator"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")
        return v
    
class User_Login(BaseModel):
    username: str
    password: str