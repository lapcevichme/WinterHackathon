from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    max_score: int = 0
    team_id: Optional[int] = None
    
    @field_validator('password')
    @classmethod
    def password_validate(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("The password length is too small")
        return v
    
class User_Login(BaseModel):
    username: str
    password: str
    