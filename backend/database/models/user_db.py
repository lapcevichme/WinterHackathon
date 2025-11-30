from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING, List
import uuid
from database import Base

if TYPE_CHECKING:
    from .team_db import Team_DB
    from .items_db import Items_DB
    from .refresh_token_db import RefreshToken_DB
    from .quest_bd import Quests_DB

def generate_uuid7():
    """Генератор UUID v7 (time-ordered UUID)"""
    return uuid.uuid4()

class User_DB(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=generate_uuid7
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=0)
    amount: Mapped[int] = mapped_column(Integer, default=0)
    energy: Mapped[int] = mapped_column(Integer, default=10)
    team_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('teams.team_id'), 
        nullable=True
    )
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="player")
    team: Mapped[Optional['Team_DB']] = relationship('Team_DB', back_populates='users', lazy="joined")
    items: Mapped[List['Items_DB']] = relationship('Items_DB', back_populates='user', lazy="joined")
    quests: Mapped[List['Quests_DB']] = relationship('Quests_DB', back_populates='user', lazy="joined")
    refresh_tokens: Mapped[List['RefreshToken_DB']] = relationship(
        'RefreshToken_DB', 
        back_populates='user',
        cascade="all, delete-orphan"
    )