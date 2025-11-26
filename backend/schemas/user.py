from pydantic import BaseModel, EmailStr, field_validator


class User():
    username: str
    password: str
    email: EmailStr
    max_score: int | 0
    ord_id: int | None
    
    @field_validator('password', mode='before')
    def password_validate(self):
        if len(self.password) < 8:
            raise ValueError("The password length is too small")