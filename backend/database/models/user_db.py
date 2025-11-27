from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from typing import Optional, TYPE_CHECKING, List
from database import Base

if TYPE_CHECKING:
    from .team_db import Team_DB
    from .items_db import Items_DB
    
class User_DB(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    money: Mapped[int] = mapped_column(Integer, default=0)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey('teams.team_id'), nullable=True)
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # ✅ Правильно: back_populates='users' (ссылается на Team_DB.users)
    team: Mapped[Optional['Team_DB']] = relationship('Team_DB', back_populates='users')
    items: Mapped[List['Items_DB']] = relationship('Items_DB', back_populates='user')  # ✅ Исправлено на 'user'