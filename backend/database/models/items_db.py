from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional, TYPE_CHECKING
import uuid
from database import Base

if TYPE_CHECKING:
    from .user_db import User_DB
    
class Items_DB(Base):
    __tablename__ = "items"
    
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    casino_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("casino.item_id"),
        nullable=False
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )
    user: Mapped[Optional['User_DB']] = relationship('User_DB', back_populates='items', lazy="joined")