from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING, List
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB

def generate_uuid7():
    """Генератор UUID v7 (time-ordered UUID)"""
    return uuid.uuid4()

class Team_DB(Base):
    __tablename__ = "teams"
    
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuid7
    )
    
    team_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    
    users: Mapped[List['User_DB']] = relationship('User_DB', back_populates='team', lazy="joined")