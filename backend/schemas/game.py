from pydantic import BaseModel
from uuid import UUID
class game_result(BaseModel):
    session_id: UUID
    score: int
    winner_id: int
    
class game_session(BaseModel):
    session_id: UUID
    user_1: UUID
    user_2: UUID
    status: str
    winner_id: UUID
    game_score: UUID