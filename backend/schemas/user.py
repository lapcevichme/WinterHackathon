from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class User(BaseModel):
    username: str
    display_name:str
    password: str
    email: EmailStr
    max_score: int = 0
    amount: int = 0
    role: str = "player"
    url: Optional[str] = None
    
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
    
class Redact_User(BaseModel):
    display_name: str
    url: str