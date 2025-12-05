from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Quests_DB(Base):
    __tablename__ = "quests"
    
    quest_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status:Mapped[str] = mapped_column(String(50), default="isnt active")
    progress:Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )
    user: Mapped['User_DB'] = relationship('User_DB', back_populates='quests', lazy="joined")
    