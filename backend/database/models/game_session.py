from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING
import uuid
from database import Base


if TYPE_CHECKING:
    from .user_db import User_DB
    

class Game_session_DB(Base):
    __tablename__ = "game_session"
    
    game_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    user_1: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )
    user_2: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )
    winner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey('users.user_id'), 
        nullable=True
    )
    game_score: Mapped[int] = mapped_column(Integer, default=0)