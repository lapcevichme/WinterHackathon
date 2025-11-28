from pydantic import BaseModel
from .user import User
class Prize(BaseModel):
    name: str
    type: str
    description: str
    amount: int = 0
    amoji: str = ""
    color: str = ""
    
    rare: str
    
    
class get_prize(BaseModel):
    name: str

class User_Win(BaseModel):
    username: str