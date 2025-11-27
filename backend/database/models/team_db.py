from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING, List
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Team_DB(Base):
    __tablename__ = "teams"
    
    team_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    money: Mapped[int] = mapped_column(Integer, default=0)
    
   
    users: Mapped[List['User_DB']] = relationship('User_DB', back_populates='team')